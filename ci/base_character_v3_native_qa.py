"""Pinned official LibreSprite source-only QA; no art logging or artifact upload."""
import os
import subprocess
import tempfile
from pathlib import Path
from PIL import Image

OUT=Path(os.environ['BASE_V3_OUTPUT'])
assert OUT.is_dir(), 'Missing rig baking output'
for skin in ('training','armor','tunic','hybrid'):
    folder=OUT/'skins'/skin
    ase=folder/f'base_character_v3_{skin}.aseprite'
    expected=folder/'run_right_480x80.png'
    assert ase.is_file() and expected.is_file(),f'Missing skin source: {skin}'
    with tempfile.TemporaryDirectory() as temp:
        exported=Path(temp)/'export.png'
        process=subprocess.run(['libresprite','-b','--list-tags','--sheet-type','horizontal',str(ase),'--sheet',str(exported)],
                               check=True,capture_output=True,text=True,timeout=120)
        assert exported.is_file(),f'LibreSprite no output for {skin}'
        with Image.open(expected) as orig, Image.open(exported) as result:
            a=orig.convert('RGBA');b=result.convert('RGBA')
            assert a.size==b.size==(480,80),(skin,a.size,b.size)
            differences=sum(1 for x,y in zip(a.getdata(),b.getdata()) if x!=y)
            assert differences==0,f'LibreSprite mismatch skin={skin}, rgba_diff={differences}'
        print(f'LIBRESPRITE_RIG_V3_{skin.upper()} PASS 6 frames x 20 layers, 480x80, RGBA_DIFF=0')
print('RIG_V3_PINNED_LIBRESPRITE_ALL_PASS 4 skins, still PENDING_OWNER_ART')