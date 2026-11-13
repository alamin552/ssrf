from flask import Flask, request, redirect
from datetime import datetime

app = Flask(__name__)

@app.route('/hop-internal', methods=['GET', 'POST'])
def hop_internal():
    target = request.args.get('to', 'http://169.254.169.254/latest/meta-data/')
    print(f"[hop-internal] {request.method} -> {target} at {datetime.utcnow().isoformat()}")
    print("Headers:", dict(request.headers))
    print("Body:", request.get_data())
    return redirect(target, code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
