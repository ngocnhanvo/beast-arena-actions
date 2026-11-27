"""Independent official LibreSprite roundtrip for private Base Character v2.

Public CI script; original art is read from PRIVATE checkout, ephemeral outputs
live on test runner only. Do NOT print raw sprite data or upload artifacts.
"""
import os
import subprocess
import tempfile
from pathlib import Path
from PIL import Image

root=Path(os.environ["BASE_V2_ROOT"])
assert root.is_dir(), "Missing prepared private source output"
for skin in ("neutral","aegis","ranger","hybrid"):
    native=root/"skins"/skin/f"base_character_{skin}.aseprite"
    original=root/"skins"/skin/"run_right.png"
    assert native.is_file() and original.is_file()
    with tempfile.TemporaryDirectory() as tmp:
        exported=Path(tmp)/"native.png"
        proc=subprocess.run(
            ["libresprite","-b","--list-tags","--sheet-type","horizontal",
             str(native),"--sheet",str(exported)],
            check=True,capture_output=True,text=True,timeout=100)
        assert exported.exists(), "LibreSprite did not export PNG"
        with Image.open(exported) as result, Image.open(original) as reference:
            a=result.convert("RGBA");b=reference.convert("RGBA")
            assert a.size==b.size==(480,80), "Native editor exported wrong dimensions"
            pa=list(a.getdata());pb=list(b.getdata())
            visible=sum(x!=y for x,y in zip(pa,pb) if x[3] or y[3])
            hidden=sum((x!=y) for x,y in zip(pa,pb) if not(x[3] or y[3]))
            assert visible==0, f"RGBA visible diff for {skin}: {visible}"
            assert hidden==0, f"RGBA transparent diff for {skin}: {hidden}"
        print(f"LIBRESPRITE_V2_{skin.upper()} PASS 6 cels, 9 native layers, 480x80, RGBA_DIFF=0")
print("BASE_CHARACTER_V2_INDEPENDENT_NATIVE_PASS all 4 outfits")
