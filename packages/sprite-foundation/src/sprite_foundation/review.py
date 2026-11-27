"""Offline diagnostic sheet, NOT an AI artist or aesthetic acceptance model."""
from collections import Counter
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from .audit import _safe_child,_frame_png_path


def write_review_sheet(manifest_file: str | Path, root: str | Path,
                       report_file: str | Path, output: str | Path, scale: int = 4) -> None:
    manifest=json.loads(Path(manifest_file).read_text(encoding="utf-8"))
    report=json.loads(Path(report_file).read_text(encoding="utf-8"))
    root=Path(root).resolve()
    w,h=manifest["canvas"]
    count=manifest["frame_count"]
    scale=max(1,min(8,scale))
    cols=min(4,count)
    rows=(count+cols-1)//cols
    cell_w=max(200,w*scale+16)
    cell_h=h*scale+65
    img=Image.new("RGB",(cell_w*cols,cell_h*rows+65),(21,32,46))
    draw=ImageDraw.Draw(img)
    reject=report.get("visual_review_status")=="REJECTED"
    draw.text((12,8),f"{manifest.get('project_id')} / {manifest.get('asset_id')}",fill=(244,246,252))
    draw.text((12,25),f"STRUCTURE: {report['structure_status']}   VISUAL: {report['visual_review_status']}   RELEASE: {report['release_status']}",fill=(245,125,115) if reject else (239,194,105))
    all_warnings=report.get("diagnostic_warnings",[])
    for k in range(1,count+1):
        col=(k-1)%cols;row=(k-1)//cols
        x=col*cell_w+8;y=row*cell_h+59
        src=_frame_png_path(root,manifest["render_template"],"",k)
        with Image.open(src) as source:
            frame=source.convert("RGBA").resize((w*scale,h*scale),Image.Resampling.NEAREST)
        bg=Image.new("RGBA",frame.size,(40,59,76,255))
        bg.alpha_composite(frame)
        img.paste(bg.convert("RGB"),(x,y))
        count_warn=sum(v.get("frame")==k for v in all_warnings)
        draw.text((x,y+h*scale+5),f"Frame {k}/{count} | style review: {count_warn}",fill=(232,234,241))
        if count_warn:
            draw.rectangle((x-1,y-1,x+w*scale,y+h*scale),outline=(250,153,101),width=2)
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    img.save(output)