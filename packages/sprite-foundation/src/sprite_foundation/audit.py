"""Portable, deterministic, non-AI source QA for multi-project sprite authoring.

The inspector reads *actual raster masks* rather than trusting part-name metadata.
It does not certify natural motion or art quality, and refuses to bootstrap its
own gold-standard from an unchecked generator output.
"""
from __future__ import annotations
from collections import deque
import hashlib
import hmac
import json
import os
from pathlib import Path
from typing import Any

from PIL import Image, ImageFilter

APPROVAL_ENV = "SPRITE_FOUNDATION_REVIEW_KEY"
SCHEMA = "sprite-foundation/1"


def _error(code: str, *, frame: int | None = None, part: str | None = None, **data: Any) -> dict:
    result = {"code": code}
    if frame is not None:
        result["frame"] = frame
    if part is not None:
        result["part"] = part
    result.update(data)
    return result


def _safe_child(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError("UNSAFE_SOURCE_PATH")
    target = (root / relative).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError("UNSAFE_SOURCE_PATH")
    return target


def _read_rgba(path: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(path) as image:
        if image.size != size or image.mode != "RGBA":
            raise ValueError("INVALID_NATIVE_RGBA")
        return image.copy()


def _mask(image: Image.Image) -> Image.Image:
    return image.getchannel("A").point(lambda v: 255 if v else 0)


def _opaque_count(image: Image.Image) -> int:
    return len(image.getchannel("A").tobytes()) - image.getchannel("A").histogram()[0]


def _overlap(a: Image.Image, b: Image.Image) -> int:
    # No NumPy/AI is needed; exact bitmask intersection is stable on Pillow 10-12.
    return sum(1 for x, y in zip(_mask(a).tobytes(), _mask(b).tobytes()) if x and y)


def _touch(a: Image.Image, b: Image.Image, gap: int) -> bool:
    m = _mask(a)
    for _ in range(gap):
        m = m.filter(ImageFilter.MaxFilter(3))
    return any(x and y for x, y in zip(m.tobytes(), _mask(b).tobytes()))


def _components(image: Image.Image) -> int:
    mask = _mask(image)
    w, h = mask.size
    present = mask.tobytes()
    seen = bytearray(w * h)
    n = 0
    for start, value in enumerate(present):
        if not value or seen[start]:
            continue
        n += 1
        queue = deque([start]); seen[start] = 1
        while queue:
            index = queue.popleft();x = index % w;y = index // w
            for xx, yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1),
                            (x-1,y-1),(x+1,y-1),(x-1,y+1),(x+1,y+1)):
                if 0 <= xx < w and 0 <= yy < h:
                    j = yy * w + xx
                    if present[j] and not seen[j]:
                        seen[j] = 1;queue.append(j)
    return n


def _frame_png_path(root: Path, template: str, part: str, frame: int) -> Path:
    # The template accepts only the literal {part} and {frame:02d} placeholders.
    # Manual substitutions prevent string-format field injection.
    if "{" in template.replace("{part}", "").replace("{frame:02d}", ""):
        raise ValueError("INVALID_FRAME_PATH_TEMPLATE")
    return _safe_child(root, template.replace("{part}", part).replace("{frame:02d}", f"{frame:02d}"))


def _hash(image: Image.Image) -> str:
    return hashlib.sha256(image.convert("RGBA").tobytes()).hexdigest()


def _signature_payload(asset: str, hashes: list[str]) -> bytes:
    return json.dumps({"asset": asset, "sha256_rgba_frames": hashes},
                      sort_keys=True, separators=(",", ":")).encode("utf-8")


def sign_approval(asset: str, hashes: list[str], secret: str) -> dict:
    """Only an authorized human pipeline should call this with an OUT-OF-REPO key."""
    if len(secret) < 24:
        raise ValueError("REVIEW_SIGNING_SECRET_TOO_SHORT")
    payload = _signature_payload(asset, hashes)
    return {"schema": "sprite-foundation/owner-approval-1", "asset": asset,
            "sha256_rgba_frames": hashes,
            "hmac_sha256": hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()}


def _verify_approval(approval_file: str | None, asset: str, hashes: list[str], secret: str | None) -> bool:
    if not approval_file or not secret:
        return False
    try:
        data = json.loads(Path(approval_file).read_text(encoding="utf-8"))
        if data.get("schema") != "sprite-foundation/owner-approval-1" or data.get("asset") != asset:
            return False
        if data.get("sha256_rgba_frames") != hashes:
            return False
        check = hmac.new(secret.encode(), _signature_payload(asset, hashes), hashlib.sha256).hexdigest()
        return hmac.compare_digest(check, str(data.get("hmac_sha256", "")))
    except (ValueError, OSError, TypeError):
        return False


def audit_manifest(manifest: dict, *, root: Path, approval_file: str | None = None,
                   review_key: str | None = None) -> dict:
    """Return stable detailed report; absent owner authorization always BLOCKS release.

    Manifest is data, not instructions. The renderer, game engine and source
    layer-count checks remain independent from this acceptance gate.
    """
    if manifest.get("schema") != SCHEMA:
        raise ValueError("UNKNOWN_SCHEMA_VERSION")
    width, height = manifest["canvas"]
    count = manifest["frame_count"]
    if not (isinstance(width, int) and isinstance(height, int)
            and 12 <= width <= 4096 and 12 <= height <= 4096
            and isinstance(count, int) and 1 <= count <= 256):
        raise ValueError("INVALID_CANVAS_OR_FRAME_COUNT")
    size = (width, height)
    asset = manifest["asset_id"]
    parts = manifest["parts"]
    if not isinstance(parts, list) or len(parts) != len(set(parts)) or not parts:
        raise ValueError("INVALID_PART_LIST")
    layer_order = manifest["layer_order"]
    if len(layer_order) != len(set(layer_order)) or set(layer_order) != set(parts):
        raise ValueError("INVALID_LAYER_ORDER")
    joins = manifest["topology"]
    for e in joins:
        if e["a"] not in parts or e["b"] not in parts or e["a"] == e["b"]:
            raise ValueError("INVALID_TOPOLOGY_EDGE")
    body_errors=[]; warnings=[]; gate=[];frames=[]
    pixels=[]
    for frame in range(1,count + 1):
        src={}
        stats={}
        for part in parts:
            name = _frame_png_path(root, manifest["part_template"], part, frame)
            try:
                img = _read_rgba(name, size)
            except (FileNotFoundError, OSError, ValueError) as exc:
                body_errors.append(_error("MISSING_OR_INVALID_PART_PNG",frame=frame,part=part,detail=type(exc).__name__))
                continue
            src[part]=img
            bbox=_mask(img).getbbox()
            pixels_opaque=_opaque_count(img)
            stats[part]={"opaque_pixels":pixels_opaque,"bbox":bbox}
            if pixels_opaque==0 and part not in manifest.get("allowed_empty_parts", []):
                body_errors.append(_error("EMPTY_REQUIRED_BODY_PART",frame=frame,part=part))
            elif pixels_opaque>0 and _components(img)>int(manifest.get("max_part_components", 2)):
                body_errors.append(_error("DISCONNECTED_PART_MASK",frame=frame,part=part))
        for slot in manifest.get("empty_slots", []):
            slot_template=manifest.get("empty_slot_template")
            if not slot_template:
                raise ValueError("MISSING_EMPTY_SLOT_TEMPLATE")
            slot_path=_frame_png_path(root,slot_template,slot,frame)
            try:
                gear=_read_rgba(slot_path,size)
                if _opaque_count(gear)!=0:
                    body_errors.append(_error("NEUTRAL_GEAR_NOT_EMPTY",frame=frame,part=slot))
            except (FileNotFoundError,OSError,ValueError) as exc:
                body_errors.append(_error("MISSING_OR_INVALID_EMPTY_GEAR_SLOT",frame=frame,part=slot,detail=type(exc).__name__))
        if len(src)!=len(parts):
            continue
        # Optional externally reviewed anchors. A generator-derived anchor is
        # useful for catching subsequent source drift, NOT visual truth.
        anchor_frames = manifest.get("anchors_by_frame")
        if anchor_frames is not None:
            if not isinstance(anchor_frames,list) or len(anchor_frames)!=count:
                raise ValueError("INVALID_ANCHOR_FRAME_COUNT")
            for part,location in anchor_frames[frame-1].items():
                if part not in src or (not isinstance(location,list) or len(location)!=2):
                    raise ValueError("INVALID_PART_ANCHOR")
                x,y=location
                if not (isinstance(x,int) and isinstance(y,int) and 0<=x<width and 0<=y<height):
                    raise ValueError("INVALID_PART_ANCHOR")
                threshold=int(manifest.get("anchor_tolerance_px",2))
                if threshold<0 or threshold>20:
                    raise ValueError("INVALID_ANCHOR_TOLERANCE")
                mask=_mask(src[part])
                crop=mask.crop((max(0,x-threshold),max(0,y-threshold),
                                min(width,x+threshold+1),min(height,y+threshold+1)))
                if crop.getbbox() is None:
                    body_errors.append(_error("PART_MISALIGNED_WITH_ANCHOR",frame=frame,part=part,point=[x,y]))
        for edge in joins:
            a,b=edge["a"],edge["b"]
            min_overlap=int(edge.get("min_overlap_pixels", 0))
            contact_gap=int(edge.get("contact_gap_px", 1))
            if min_overlap and _overlap(src[a],src[b])<min_overlap:
                body_errors.append(_error("ANATOMY_JOINT_OVERLAP_MISSING",frame=frame,part=f"{a}->{b}",actual=_overlap(src[a],src[b]),required=min_overlap))
            elif not _touch(src[a],src[b],contact_gap):
                body_errors.append(_error("ANATOMY_JOINT_DISCONNECTED",frame=frame,part=f"{a}->{b}"))
        result=Image.new("RGBA",size,(0,0,0,0))
        for part in layer_order:
            result.alpha_composite(src[part])
        actual_render=_frame_png_path(root,manifest["render_template"],"",frame)
        try:
            actual=_read_rgba(actual_render,size)
            if result.tobytes()!=actual.tobytes():
                body_errors.append(_error("LAYERS_DO_NOT_RECONSTRUCT_RENDER",frame=frame))
        except (FileNotFoundError,OSError,ValueError):
            body_errors.append(_error("MISSING_OR_INVALID_RENDER",frame=frame))
        if _components(result)>int(manifest.get("max_body_components", 1)):
            body_errors.append(_error("BODY_SILHOUETTE_DISCONNECTED",frame=frame))
        bbox=_mask(result).getbbox()
        if bbox and (bbox[0]==0 or bbox[1]==0 or bbox[2]==width or bbox[3]==height):
            warnings.append(_error("BODY_AT_CANVAS_EDGE_REVIEW_CLIPPING",frame=frame))
        # No global biological ratio! Project-specific ranges are optional and
        # become art REVIEW, not a false machine-issued aesthetic certificate.
        for metric, rule in manifest.get("style_review_ratios",{}).items():
            numerator,denominator=rule["numerator"],rule["denominator"]
            if numerator not in src or denominator not in src:continue
            bn=_mask(src[numerator]).getbbox();bd=_mask(src[denominator]).getbbox()
            if not bn or not bd: continue
            v=(bn[3]-bn[1]) / max(1,(bd[3]-bd[1]))
            if v < float(rule.get("min",0)) or v > float(rule.get("max",1e4)):
                warnings.append(_error("STYLE_RATIO_REVIEW",frame=frame,part=metric,ratio=round(v,3),expected=[rule.get("min"),rule.get("max")]))
        pixels.append(_hash(result))
        frames.append({"frame":frame,"sha256_rgba":_hash(result),"silhouette_bbox":bbox,"part_stats":stats})
    if len(frames) != count:
        body_errors.append(_error("INCOMPLETE_FRAME_SET",frames_loaded=len(frames),expected=count))
    if len(set(pixels)) != len(pixels) and not manifest.get("allow_identical_frames", False):
        body_errors.append(_error("DUPLICATED_FRAMES_NEED_ART_REVIEW"))
    author=manifest.get("authoring",{})
    if author.get("source_kind") in ("procedural", "auto_inferred", "traced"):
        gate.append(_error("PROCEDURAL_ART_REQUIRES_INDEPENDENT_REVIEW"))
    if author.get("owner_review") == "REJECTED":
        gate.append(_error("OWNER_REJECTED_ART"))
    if not manifest.get("motion",{}).get("ground_contact_verified",False):
        gate.append(_error("GROUND_CONTACT_NOT_VERIFIED"))
    if not manifest.get("motion",{}).get("loop_review_verified",False):
        gate.append(_error("LOOP_SEAM_NOT_REVIEWED"))
    approval_valid = _verify_approval(approval_file,asset,pixels,review_key)
    if not approval_valid:
        gate.append(_error("NO_EXTERNAL_OWNER_APPROVAL_FOR_EXACT_ART_BYTES"))
    # Even a signed PNG approval is insufficient to claim physics review.
    result={
        "schema": "sprite-foundation/audit-1", "asset_id":asset,
        "project_id":manifest.get("project_id","unspecified"),
        "frame_count":count, "canvas":list(size),
        "structure_status":"FAIL" if body_errors else "PASS",
        "visual_review_status":"REJECTED" if author.get("owner_review")=="REJECTED" else ("PENDING" if gate or warnings else "REVIEW_RECORDED"),
        "release_status":"BLOCKED" if body_errors or gate or warnings else "CANDIDATE_REQUIRES_MANUAL_REVIEW",
        "structural_errors":body_errors,"diagnostic_warnings":warnings,
        "approval_blockers":gate,"frames":frames,
        "note":"Structural source integrity NEVER proves visually correct anatomy, natural gait, or approved art."
    }
    return result


def audit_manifest_file(manifest_file: str | Path, *, root: str | Path | None = None,
                        approval_file: str | None = None,
                        review_key: str | None = None) -> dict:
    mfile=Path(manifest_file).resolve()
    doc=json.loads(mfile.read_text(encoding="utf-8"))
    return audit_manifest(doc,root=Path(root).resolve() if root else mfile.parent,
                          approval_file=approval_file,review_key=review_key)