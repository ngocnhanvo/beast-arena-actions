"""CLI for generic layered sprite authoring and independent owner-art gates."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
from .audit import APPROVAL_ENV, audit_manifest_file, sign_approval


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Game-independent layered sprite QA; no false art approvals")
    sub = parser.add_subparsers(dest="command", required=True)
    audit = sub.add_parser("audit", help="check actual part PNGs, rendered cels and external review")
    audit.add_argument("--manifest", required=True)
    audit.add_argument("--root", help="override root of manifest input PNG paths")
    audit.add_argument("--out", required=True)
    audit.add_argument("--approval", help="independently signed approval, stored outside source")
    audit.add_argument("--technical-only", action="store_true", help="0 when structure passes, even if art is blocked; CI must still assert status")
    audit.add_argument("--review-sheet", help="optional local-only annotated PNG (never publish private art in public CI)")
    sign = sub.add_parser("owner-sign", help="requires an OUT-OF-REPO secret; never call from an AI task")
    sign.add_argument("--report", required=True)
    sign.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    if args.command == "audit":
        report = audit_manifest_file(args.manifest, root=args.root,
                                     approval_file=args.approval,
                                     review_key=os.getenv(APPROVAL_ENV))
        output = Path(args.out); output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
        if args.review_sheet:
            from .review import write_review_sheet
            write_review_sheet(args.manifest,args.root or Path(args.manifest).parent,output,args.review_sheet)
        summary={k:report[k] for k in ("asset_id","structure_status","visual_review_status","release_status")}
        summary["errors"]=len(report["structural_errors"])
        summary["warnings"]=len(report["diagnostic_warnings"])
        summary["blockers"]=len(report["approval_blockers"])
        print(json.dumps(summary,ensure_ascii=False))
        if report["structure_status"]=="FAIL":return 2
        if report["release_status"]=="BLOCKED" and not args.technical_only:return 3
        return 0
    if args.command == "owner-sign":
        # This option exists only for owner-operated release tooling, not agents.
        secret=os.getenv(APPROVAL_ENV,"")
        if len(secret)<24:
            print(f"Owner signing is unavailable: set {APPROVAL_ENV} from external secret store")
            return 4
        report=json.loads(Path(args.report).read_text(encoding="utf-8"))
        if report["structure_status"]!="PASS" or report["visual_review_status"]=="REJECTED":
            print("Cannot sign a structurally broken or explicitly rejected source")
            return 2
        data=sign_approval(report["asset_id"],[f["sha256_rgba"] for f in report["frames"]],secret,report["source_contract_sha256"])
        Path(args.out).write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
        print("Owner approval signed; source/frame hashes are immutable for this signature")
        return 0
    return 4

if __name__ == "__main__":
    raise SystemExit(main())