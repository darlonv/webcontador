from flask import Flask, Response, render_template, request, after_this_request
import os, time, threading

app = Flask(__name__)
APP_VERSION = os.getenv("APP_VERSION", "dev")

counter = 0
_running = True

def ticker():
    global counter, _running
    while _running:
        counter += 1
        time.sleep(1)

@app.route("/")
def index():
    return render_template("index.html", version=APP_VERSION)

@app.route("/events")
def events():
    def stream():
        # avisa a versão logo no início (para o cliente decidir se recarrega)
        yield f"event: version\ndata: {APP_VERSION}\n\n"
        last_sent = None
        while True:
            if last_sent != counter:
                yield f"data: {counter}\n\n"
                last_sent = counter
            time.sleep(1)
    return Response(stream(), mimetype="text/event-stream")

@app.after_request
def add_header(resp):
    resp.headers["Cache-Control"] = "no-store"
    return resp

if __name__ == "__main__":
    t = threading.Thread(target=ticker, daemon=True)
    t.start()
    try:
        app.run(host="0.0.0.0", port=8000)
    finally:
        _running = False

