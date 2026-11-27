"""Adversarial tests: motion statistics are never evidence of art approval."""
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image, ImageDraw
from sprite_foundation.motion import analyze_motion


class IndependentMotionDiagnosticsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def make_case(self, width, frame_count, duplicate=False):
        root=self.root/f'case_{width}_{frame_count}_{duplicate}'
        dst=root/'render'
        dst.mkdir(parents=True)
        for frame in range(1,frame_count+1):
            im=Image.new('RGBA',(width,width))
            x=8+(frame-1 if not (duplicate and frame==2) else 0)
            ImageDraw.Draw(im).rectangle((x,3,x+5,width-3),
                                         fill=(190,123,74,255))
            im.save(dst/f'frame_{frame:02d}.png')
        manifest={'schema':'sprite-foundation/1','project_id':'unrelated-test-game',
            'asset_id':'synthetic-actor','canvas':[width,width],
            'frame_count':frame_count,'render_template':'render/frame_{frame:02d}.png',
            'motion':{'ground_contact_verified':False,'loop_review_verified':False}}
        src=root/'manifest.json'
        src.write_text(json.dumps(manifest))
        return src

    def test_multiple_canvas_sizes_and_loop_transition_are_included(self):
        for w,n in [(32,4),(64,8)]:
            with self.subTest(size=w,frames=n):
                src=self.make_case(w,n)
                report=analyze_motion(src)
                self.assertEqual(len(report['frames']),n)
                self.assertEqual(len(report['transitions']),n)
                self.assertEqual(report['canvas'],[w,w])
                self.assertTrue(report['transitions'][-1]['loop_seam'])
                self.assertEqual(report['transitions'][-1]['to_frame'],1)
                self.assertIsNotNone(report['seam_vs_internal_median_ratio'])

    def test_duplicate_phase_is_diagnostic_only(self):
        src=self.make_case(32,4,duplicate=True)
        data=analyze_motion(src)
        self.assertEqual(data['exact_duplicate_adjacent_frames'],[{'from':1,'to':2}])
        self.assertEqual(data['diagnostic_status'],'MEASURED_ONLY')
        self.assertEqual(data['loop_art_review_status'],'UNVERIFIED')
        self.assertEqual(data['release_authorization'],'NONE')

    def test_ground_pixels_cannot_be_mislabeled_physical_contact(self):
        src=self.make_case(32,4)
        report=analyze_motion(src)
        self.assertTrue(all(f['bottom_opaque_y'] == 29 for f in report['frames']))
        self.assertTrue(all(f['ground_line_candidates'] for f in report['frames']))
        self.assertEqual(report['ground_contact_status'],'UNVERIFIED')
        self.assertEqual(report['world_space_foot_trajectory_status'],'UNVERIFIED')

    def test_empty_frame_yields_nonempty_false_not_fabricated_feet(self):
        src=self.make_case(32,4)
        target=src.parent/'render/frame_03.png'
        Image.new('RGBA',(32,32)).save(target)
        result=analyze_motion(src)
        self.assertFalse(result['frames'][2]['nonempty'])
        self.assertIsNone(result['frames'][2]['bottom_opaque_y'])
        self.assertEqual(result['release_authorization'],'NONE')

    def test_missing_render_frame_fails_closed(self):
        src=self.make_case(32,4)
        (src.parent/'render/frame_04.png').unlink()
        with self.assertRaises(FileNotFoundError):
            analyze_motion(src)

if __name__=='__main__':
    unittest.main()
