# vuln_app.py - safe local test server (simulated vulnerable endpoints)
from flask import Flask, request
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    file_param = request.args.get("file", "")
    # If someone tries to read "passwd", return fake contents (do NOT read real files)
    if "passwd" in file_param:
        fake_passwd = "root:x:0:0:root:/root:/bin/bash\nuser:x:1000:1000:User:/home/user:/bin/bash\n"
        return f"Simulated file contents:\n\n{fake_passwd}", 200

    q = request.args.get("q", "")
    # reflect q parameter; useful to test reflected XSS
    return f"Echo: {q}", 200

if __name__ == "__main__":
    app.run(port=5001, debug=False)
