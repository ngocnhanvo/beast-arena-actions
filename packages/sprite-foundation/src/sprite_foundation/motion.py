"""Pure geometry diagnostics for animated 2D sources; NOT contact or art approval.

Render-only measures cannot recover world-space foot trajectories, draw order,
owner aesthetic signoff, or physically planted feet. The output is diagnostic
evidence for a human/engine-reviewed gait test, never an automatic PASS.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

from PIL import Image

from .audit import _frame_png_path, _read_rgba


def _frame_metrics(im: Image.Image, index: int) -> dict:
    w, h = im.size
    pixels = im.getchannel('A').tobytes()
    points = [j for j, a in enumerate(pixels) if a]
    if not points:
        return {'frame': index, 'nonempty': False, 'opaque_pixels': 0,
                'bbox': None, 'bottom_opaque_y': None,
                'centroid_px': None, 'ground_line_candidates': []}
    xs = [i % w for i in points]
    ys = [i // w for i in points]
    bottom = max(ys)
    contacts = [i % w for i in points if i // w == bottom]
    return {'frame': index, 'nonempty': True,
            'opaque_pixels': len(points),
            'bbox': list(im.getchannel('A').getbbox()),
            'bottom_opaque_y': bottom,
            'centroid_px': [round(sum(xs)/len(xs), 3),
                            round(sum(ys)/len(ys), 3)],
            'ground_line_candidates': [min(contacts), max(contacts)],
            'sha256_rgba': hashlib.sha256(im.tobytes()).hexdigest()}


def analyze_motion(manifest_file: str | Path, *, root: str | Path | None = None) -> dict:
    manifest_path = Path(manifest_file).resolve()
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('schema') != 'sprite-foundation/1':
        raise ValueError('INVALID_MOTION_MANIFEST')
    dims = manifest.get('canvas')
    count = manifest.get('frame_count')
    if (not isinstance(dims, list) or len(dims) != 2 or
        any(type(v) is not int or v < 12 or v > 4096 for v in dims)
        or type(count) is not int or not 1 <= count <= 256):
        raise ValueError('INVALID_MOTION_DIMENSIONS')
    root_path = Path(root).resolve() if root is not None else manifest_path.parent
    dimensions = (dims[0], dims[1])
    images = []
    metrics = []
    for i in range(1,count+1):
        img = _read_rgba(
            _frame_png_path(root_path,manifest['render_template'],'',i),
            dimensions)
        metrics.append(_frame_metrics(img,i))
        images.append(img)
    width,height=dimensions
    total=width*height
    adjacent=[]
    for i,source in enumerate(images):
        target=images[(i+1)%len(images)]
        a=source.tobytes();b=target.tobytes()
        changed=sum(x!=y for x,y in zip(a,b))
        # Count changed *pixels*, not channels; alpha and color are both relevant.
        changed_pixels=sum(
            a[j:j+4]!=b[j:j+4] for j in range(0,len(a),4))
        adjacent.append({'from_frame':i+1,'to_frame':((i+1)%len(images))+1,
                         'loop_seam':i==len(images)-1,
                         'changed_pixel_count':changed_pixels,
                         'changed_pixel_fraction':round(changed_pixels/total,6)})
    seam=adjacent[-1]['changed_pixel_fraction']
    internal=[x['changed_pixel_fraction'] for x in adjacent[:-1]]
    reference=sorted(internal)[len(internal)//2] if internal else None
    ratio=round(seam/reference,4) if reference else None
    duplicate_pairs=[{'from':d['from_frame'],'to':d['to_frame']}
                     for d in adjacent if d['changed_pixel_count']==0]
    return {
        'schema':'sprite-foundation/motion-diagnostics-1',
        'project_id':manifest.get('project_id','unspecified'),
        'asset_id':manifest['asset_id'],
        'canvas':list(dimensions),'frame_count':count,
        'frames':metrics,
        'transitions':adjacent,
        'seam_vs_internal_median_ratio':ratio,
        'exact_duplicate_adjacent_frames':duplicate_pairs,
        'diagnostic_status':'MEASURED_ONLY',
        'ground_contact_status':'UNVERIFIED',
        'world_space_foot_trajectory_status':'UNVERIFIED',
        'loop_art_review_status':'UNVERIFIED',
        'release_authorization':'NONE',
        'note':'Visible bottom pixels and frame differences cannot certify planted feet, natural gait, or an approved seam.'
    }
