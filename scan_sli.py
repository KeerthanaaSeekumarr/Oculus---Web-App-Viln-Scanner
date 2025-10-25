# scan_cli.py
import argparse
import json
from scan_worker import run_scan_and_save_report

def main():
    parser = argparse.ArgumentParser(description="Run vuln scanner from CLI")
    parser.add_argument("target", help="Target URL (e.g., http://127.0.0.1:5001)")
    parser.add_argument("--intrusive", action="store_true", help="Enable intrusive tests")
    parser.add_argument("--print", dest="print_report", action="store_true", help="Print JSON report to stdout")
    args = parser.parse_args()

    scan_id = "cli_" + (__import__("uuid").uuid4().hex[:8])
    out = run_scan_and_save_report(args.target, scan_id, intrusive=args.intrusive)
    print("Report saved to:", out)
    if args.print_report:
        with open(out, "r", encoding="utf-8") as fh:
            print(fh.read())

if __name__ == "__main__":
    main()
