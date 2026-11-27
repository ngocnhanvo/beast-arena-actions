"""Independent adversarial tests: green source files do not certify art."""
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from PIL import Image,ImageDraw
from sprite_foundation.audit import audit_manifest_file, sign_approval, _safe_child


class FoundationCoreTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def make_project(self, width=32, frame_count=4):
        """Uses a completely artificial original asset; no real-world game artwork."""
        root=self.root/f'p_{width}_{frame_count}'
        root.mkdir()
        parts=['torso','neck','head']
        for i in range(1,frame_count+1):
            layers={}
            offset=(i-1)
            shapes={
                'torso':(11+offset,15,19+offset,27),
                'neck':(14+offset,12,16+offset,18),
                'head':(10+offset,5,21+offset,15)
            }
            for part in parts:
                im=Image.new('RGBA',(width,width))
                d=ImageDraw.Draw(im)
                d.rectangle(shapes[part], fill={'torso':(180,100,70,255),'neck':(210,130,95,255),'head':(230,150,100,255)}[part])
                path=root/'source'/'body'/part/f'run_{i:02}.png'
                path.parent.mkdir(parents=True,exist_ok=True)
                im.save(path)
                layers[part]=im
            canvas=Image.new('RGBA',(width,width))
            for name in parts:
                canvas.alpha_composite(layers[name])
            render=root/'render'/'neutral'/f'run_{i:02}.png'
            render.parent.mkdir(parents=True,exist_ok=True)
            canvas.save(render)
            for slot in ['hair','shirt']:
                p=root/'source'/'gear'/slot/f'run_{i:02}.png'
                p.parent.mkdir(parents=True,exist_ok=True)
                Image.new('RGBA',(width,width)).save(p)
        manifest={
            'schema':'sprite-foundation/1','project_id':'other-game-any-engine',
            'asset_id':f'actor{width}_{frame_count}', 'canvas':[width,width],
            'frame_count':frame_count,'parts':parts,'layer_order':parts,
            'part_template':'source/body/{part}/run_{frame:02d}.png',
            'render_template':'render/neutral/run_{frame:02d}.png',
            'empty_slots':['hair','shirt'],
            'empty_slot_template':'source/gear/{part}/run_{frame:02d}.png',
            'topology':[{'a':'head','b':'neck','min_overlap_pixels':2,'contact_gap_px':1},
                        {'a':'neck','b':'torso','min_overlap_pixels':2,'contact_gap_px':1}],
            'max_body_components':1,'max_part_components':1,
            'authoring':{'source_kind':'artist','owner_review':'PENDING'},
            'motion':{'ground_contact_verified':False,'loop_review_verified':False}
        }
        filename=root/'sprite_manifest.json'
        filename.write_text(json.dumps(manifest,indent=2))
        return root,filename

    def test_two_different_games_not_hardcoded_80px_or_6frames(self):
        for dimensions,frames in [(32,4),(64,8)]:
            with self.subTest(dimensions=dimensions,frames=frames):
                root,p=self.make_project(dimensions,frames)
                report=audit_manifest_file(p)
                self.assertEqual(report['structure_status'],'PASS',report['structural_errors'])
                self.assertEqual(report['frame_count'],frames)
                self.assertEqual(report['release_status'],'BLOCKED')
                self.assertIn('NO_EXTERNAL_OWNER_APPROVAL_FOR_EXACT_ART_BYTES',[x['code'] for x in report['approval_blockers']])

    def test_true_detached_head_detected_even_if_render_rebuilt_to_match(self):
        root,p=self.make_project()
        path=root/'source/body/head/run_01.png'
        img=Image.open(path).convert('RGBA')
        shifted=Image.new('RGBA',img.size);shifted.alpha_composite(img,(0,-5));shifted.save(path)
        layers={name:Image.open(root/'source/body'/name/'run_01.png').convert('RGBA') for name in ['torso','neck','head']}
        canvas=Image.new('RGBA',img.size)
        for part in ['torso','neck','head']:canvas.alpha_composite(layers[part])
        canvas.save(root/'render/neutral/run_01.png')
        report=audit_manifest_file(p)
        self.assertEqual(report['structure_status'],'FAIL')
        self.assertIn('ANATOMY_JOINT_OVERLAP_MISSING',[x['code'] for x in report['structural_errors']])

    def test_stale_render_pixel_detected_even_if_png_valid(self):
        root,p=self.make_project()
        file=root/'render/neutral/run_01.png'
        image=Image.open(file).convert('RGBA');image.putpixel((1,1),(255,1,2,255));image.save(file)
        report=audit_manifest_file(p)
        self.assertIn('LAYERS_DO_NOT_RECONSTRUCT_RENDER',[x['code'] for x in report['structural_errors']])

    def test_gear_nonempty_on_neutral_is_technical_error(self):
        root,p=self.make_project()
        f=root/'source/gear/hair/run_01.png'
        im=Image.open(f).convert('RGBA');im.putpixel((2,2),(250,0,0,255));im.save(f)
        report=audit_manifest_file(p)
        self.assertIn('NEUTRAL_GEAR_NOT_EMPTY',[x['code'] for x in report['structural_errors']])

    def test_broken_topology_and_path_traversal_fail_closed(self):
        root,p=self.make_project();m=json.loads(p.read_text());m['part_template']='../../{part}/{frame:02d}.png'
        p.write_text(json.dumps(m))
        with self.assertRaisesRegex(ValueError,'UNSAFE_SOURCE_PATH'):
            audit_manifest_file(p)

    def test_part_missing_does_not_make_technical_pass(self):
        root,p=self.make_project();(root/'source/body/neck/run_03.png').unlink()
        report=audit_manifest_file(p)
        self.assertEqual(report['structure_status'],'FAIL')
        self.assertIn('INCOMPLETE_FRAME_SET',[x['code'] for x in report['structural_errors']])

    def test_owner_rejection_must_block_even_if_source_structurally_valid(self):
        root,p=self.make_project();m=json.loads(p.read_text());m['authoring']['owner_review']='REJECTED'
        p.write_text(json.dumps(m))
        report=audit_manifest_file(p)
        self.assertEqual(report['structure_status'],'PASS')
        self.assertEqual(report['visual_review_status'],'REJECTED')
        self.assertEqual(report['release_status'],'BLOCKED')
        self.assertIn('OWNER_REJECTED_ART',[x['code'] for x in report['approval_blockers']])

    def test_signed_owner_review_uses_all_frame_bytes_and_external_secret(self):
        root,p=self.make_project()
        m=json.loads(p.read_text());m['motion']={'ground_contact_verified':True,'loop_review_verified':True}
        p.write_text(json.dumps(m));report=audit_manifest_file(p)
        secret='very-long-out-of-repo-human-reviewer-secret'
        gold=sign_approval(report['asset_id'],[f['sha256_rgba'] for f in report['frames']],secret,report['source_contract_sha256'])
        approval=root/'external_approved.json';approval.write_text(json.dumps(gold))
        checked=audit_manifest_file(p,approval_file=str(approval),review_key=secret)
        self.assertEqual(checked['structure_status'],'PASS')
        self.assertEqual(checked['release_status'],'CANDIDATE_REQUIRES_MANUAL_REVIEW')
        # A wrong secret cannot transform a failed art source into approved.
        tampered=audit_manifest_file(p,approval_file=str(approval),review_key='otherlongsecretotherlongsecret')
        self.assertEqual(tampered['release_status'],'BLOCKED')
        # Changed art (and corresponding render): old approval invalidates.
        i=root/'source/body/torso/run_01.png';a=Image.open(i).convert('RGBA');a.putpixel((14,22),(12,12,12,255));a.save(i)
        composite=Image.new('RGBA',(32,32))
        for part in ['torso','neck','head']:
            composite.alpha_composite(Image.open(root/'source/body'/part/'run_01.png').convert('RGBA'))
        composite.save(root/'render/neutral/run_01.png')
        result=audit_manifest_file(p,approval_file=str(approval),review_key=secret)
        self.assertEqual(result['release_status'],'BLOCKED')

    def test_independent_landmark_detects_moved_part_even_if_mask_still_touching(self):
        root,p=self.make_project()
        m=json.loads(p.read_text())
        m['anchors_by_frame']=[{'head':[15+(i%3),10]} for i in range(4)]
        m['anchor_tolerance_px']=1
        p.write_text(json.dumps(m))
        before=audit_manifest_file(p)
        self.assertEqual(before['structure_status'],'PASS')
        # Body parts may still be contiguous; a semantic anchor checks actual painted pixels.
        m['anchors_by_frame'][0]['head']=[2,2]
        p.write_text(json.dumps(m))
        after=audit_manifest_file(p)
        self.assertEqual(after['structure_status'],'FAIL')
        self.assertIn('PART_MISALIGNED_WITH_ANCHOR',[x['code'] for x in after['structural_errors']])

    def test_same_ratios_not_hardcoded_as_biology(self):
        root,p=self.make_project()
        m=json.loads(p.read_text())
        m['style_review_ratios']={'head_vs_torso':{'numerator':'head','denominator':'torso','max':0.3}}
        p.write_text(json.dumps(m))
        result=audit_manifest_file(p)
        self.assertEqual(result['structure_status'],'PASS')
        self.assertIn('STYLE_RATIO_REVIEW',[x['code'] for x in result['diagnostic_warnings']])
        self.assertEqual(result['release_status'],'BLOCKED')

    def test_does_not_accept_generated_raster_as_its_own_gold_reference(self):
        root,p=self.make_project()
        m=json.loads(p.read_text());m['authoring']['source_kind']='procedural';m['authoring']['owner_review']='REJECTED'
        p.write_text(json.dumps(m))
        report=audit_manifest_file(p)
        codes={x['code'] for x in report['approval_blockers']}
        self.assertIn('PROCEDURAL_ART_REQUIRES_INDEPENDENT_REVIEW',codes)
        self.assertIn('OWNER_REJECTED_ART',codes)
        self.assertIn('NO_EXTERNAL_OWNER_APPROVAL_FOR_EXACT_ART_BYTES',codes)


    def test_hidden_layer_change_invalidates_approval_without_render_change(self):
        root,p=self.make_project()
        m=json.loads(p.read_text());m['motion']={'ground_contact_verified':True,'loop_review_verified':True}
        p.write_text(json.dumps(m))
        key='owner-private-long-review-secret-1234'
        before=audit_manifest_file(p)
        signature=sign_approval(before['asset_id'],[f['sha256_rgba'] for f in before['frames']],key,before['source_contract_sha256'])
        approval=root/'external.json';approval.write_text(json.dumps(signature))
        self.assertEqual(audit_manifest_file(p,approval_file=str(approval),review_key=key)['release_status'],'CANDIDATE_REQUIRES_MANUAL_REVIEW')
        # Torso is opaque at (13,16); later neck/head layer overlaps this point.
        torso=root/'source/body/torso/run_01.png'
        im=Image.open(torso).convert('RGBA')
        im.putpixel((14,16),(1,2,3,255))
        im.save(torso)
        # Render output unchanged: top neck layer still paints same visible byte.
        after=audit_manifest_file(p,approval_file=str(approval),review_key=key)
        self.assertEqual(before['frames'][0]['sha256_rgba'],after['frames'][0]['sha256_rgba'])
        self.assertNotEqual(before['source_contract_sha256'],after['source_contract_sha256'])
        self.assertEqual(after['release_status'],'BLOCKED')

    def test_manifest_motion_flags_change_invalidates_old_review(self):
        root,p=self.make_project()
        m=json.loads(p.read_text());m['motion']={'ground_contact_verified':True,'loop_review_verified':True}
        p.write_text(json.dumps(m))
        key='owner-private-long-review-secret-1234'
        before=audit_manifest_file(p)
        signature=sign_approval(before['asset_id'],[f['sha256_rgba'] for f in before['frames']],key,before['source_contract_sha256'])
        approval=root/'external.json';approval.write_text(json.dumps(signature))
        m['authoring']['source_kind']='licensed'
        p.write_text(json.dumps(m))
        after=audit_manifest_file(p,approval_file=str(approval),review_key=key)
        self.assertEqual(before['frames'][0]['sha256_rgba'],after['frames'][0]['sha256_rgba'])
        self.assertNotEqual(before['source_contract_sha256'],after['source_contract_sha256'])
        self.assertEqual(after['release_status'],'BLOCKED')

    def test_legacy_render_only_signature_is_not_trusted(self):
        root,p=self.make_project()
        m=json.loads(p.read_text());m['motion']={'ground_contact_verified':True,'loop_review_verified':True}
        p.write_text(json.dumps(m))
        key='owner-private-long-review-secret-1234'
        before=audit_manifest_file(p)
        import hmac
        payload=json.dumps({'asset':before['asset_id'],'sha256_rgba_frames':[f['sha256_rgba'] for f in before['frames']]},sort_keys=True,separators=(',',':')).encode()
        legacy={'schema':'sprite-foundation/owner-approval-1','asset':before['asset_id'],
                'sha256_rgba_frames':[f['sha256_rgba'] for f in before['frames']],
                'hmac_sha256':hmac.new(key.encode(),payload,hashlib.sha256).hexdigest()}
        approval=root/'external.json';approval.write_text(json.dumps(legacy))
        self.assertEqual(audit_manifest_file(p,approval_file=str(approval),review_key=key)['release_status'],'BLOCKED')

if __name__=='__main__':unittest.main()