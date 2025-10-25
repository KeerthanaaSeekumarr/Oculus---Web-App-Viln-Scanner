# app.py
import threading
import uuid
import os
import json
from flask import Flask, request, send_file, jsonify, render_template_string
from scan_worker import run_scan_and_save_report

app = Flask(__name__)

# In-memory store for scan statuses and report paths
# structure: scans[scan_id] = {"status":"running|done|error", "report": "path", "target": "https://..."}
scans = {}

# Simple HTML UI (keeps previous UI but posts to API)
INDEX_HTML = """
<!doctype html>
<html>
  <head><title>Web Vulnerability Scanner</title></head>
  <body>
    <h1>Web Vulnerability Scanner — UI</h1>
    <form id="scanform" method="post" action="/api/scan">
      Target URL: <input name="target" type="text" placeholder="http://127.0.0.1:5001" size="50"/>
      <label><input type="checkbox" name="intrusive"/> Enable Intrusive Tests</label>
      <button type="submit">Start Scan</button>
    </form>
    <hr/>
    <div>
      <h3>Check status</h3>
      <input id="sid" placeholder="scan id" />
      <button onclick="status()">Get Status</button>
      <pre id="out"></pre>
    </div>
    <script>
      async function status(){
        const sid = document.getElementById('sid').value;
        if(!sid){ alert('Enter scan id'); return; }
        const r = await fetch('/api/status/' + sid);
        const j = await r.json();
        document.getElementById('out').textContent = JSON.stringify(j, null, 2);
      }
    </script>
  </body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(INDEX_HTML)

# API: start scan
@app.route("/api/scan", methods=["POST"])
def api_scan():
    # Accept form-data (from UI) or JSON body
    data = request.form.to_dict() or request.get_json(silent=True) or {}
    target = data.get("target")
    intrusive = data.get("intrusive") in ("on", "true", True, "1")
    if not target:
        return jsonify({"error":"target parameter required"}), 400

    scan_id = uuid.uuid4().hex[:12]
    scans[scan_id] = {"status":"running", "report":None, "target": target}

    # start background thread
    thread = threading.Thread(target=_background_scan, args=(scan_id, target, intrusive), daemon=True)
    thread.start()

    return jsonify({"scan_id": scan_id, "status_url": f"/api/status/{scan_id}", "report_url": f"/api/report/{scan_id}"}), 202

def _background_scan(scan_id, target, intrusive):
    try:
        out_path = run_scan_and_save_report(target, scan_id, intrusive=intrusive)
        scans[scan_id]["status"] = "done"
        scans[scan_id]["report"] = out_path
    except Exception as e:
        scans[scan_id]["status"] = "error"
        scans[scan_id]["report"] = None
        scans[scan_id]["error"] = str(e)

# API: status
@app.route("/api/status/<scan_id>", methods=["GET"])
def api_status(scan_id):
    if scan_id not in scans:
        return jsonify({"error":"scan_id not found"}), 404
    return jsonify(scans[scan_id])

# API: download report
@app.route("/api/report/<scan_id>", methods=["GET"])
def api_report(scan_id):
    entry = scans.get(scan_id)
    if not entry:
        return jsonify({"error":"scan_id not found"}), 404
    if entry["status"] != "done" or not entry.get("report"):
        return jsonify({"error":"report not ready", "status": entry["status"]}), 404
    return send_file(entry["report"], as_attachment=True)

if __name__ == "__main__":
    # ensure reports folder exists
    os.makedirs("reports", exist_ok=True)
    app.run(debug=True, port=5000)
