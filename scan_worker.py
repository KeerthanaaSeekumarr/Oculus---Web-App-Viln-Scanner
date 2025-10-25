# scan_worker.py
import json
import os
from datetime import datetime
from scanner.attacker import Attacker

def run_scan_and_save_report(target, scan_id, intrusive=False):
    attacker = Attacker(target)
    findings = attacker.run_scan()  # list of dicts

    report = {
        "scan_id": scan_id,
        "target": target,
        "intrusive": bool(intrusive),
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "findings": findings
    }

    os.makedirs("reports", exist_ok=True)
    out_path = os.path.join("reports", f"report_{scan_id}.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    return out_path
