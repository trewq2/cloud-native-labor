from flask import Flask, jsonify
import os
import socket

import redis

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "").strip()
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
APP_VERSION = os.getenv("APP_VERSION", "1.0")


def redis_status(increment=False):
    """Redis állapot és számláló lekérdezése.

    Ha REDIS_HOST nincs beállítva, az alkalmazás Redis nélkül is működik.
    Ez szándékos az önálló Docker- és Kubernetes-feladatoknál.
    """
    if not REDIS_HOST:
        return {
            "configured": False,
            "connected": False,
            "count": None,
            "error": None,
        }

    try:
        client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True,
            socket_connect_timeout=2,
            socket_timeout=2,
        )
        client.ping()
        count = client.incr("cloudlab_visits") if increment else client.get("cloudlab_visits")
        return {
            "configured": True,
            "connected": True,
            "count": int(count) if count is not None else 0,
            "error": None,
        }
    except Exception as exc:
        return {
            "configured": True,
            "connected": False,
            "count": None,
            "error": f"{type(exc).__name__}: {exc}",
        }


@app.get("/")
def index():
    status = redis_status(increment=True)

    if status["connected"]:
        redis_text = "Kapcsolódva"
        counter_text = str(status["count"])
        css_class = "ok"
        diagnostic = ""
    elif not status["configured"]:
        redis_text = "Nincs konfigurálva ebben a futási módban"
        counter_text = "–"
        css_class = "neutral"
        diagnostic = "<p class='hint'>A számláló a Docker Compose + Redis modulban aktiválódik.</p>"
    else:
        redis_text = "NINCS KAPCSOLAT"
        counter_text = "Redis nem érhető el"
        css_class = "bad"
        diagnostic = f"""
        <div class="error">
          <strong>Redis diagnosztika:</strong><br>
          REDIS_HOST = <code>{REDIS_HOST}</code><br>
          REDIS_PORT = <code>{REDIS_PORT}</code><br>
          Hiba: <code>{status['error']}</code>
        </div>
        """

    return f"""<!doctype html>
<html lang="hu">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CloudLab</title>
<style>
body{{font-family:Arial,sans-serif;background:#eef4f7;margin:40px;color:#17324d}}
main{{max-width:760px;margin:auto;background:white;padding:28px;border-radius:16px;box-shadow:0 10px 30px rgba(0,0,0,.08)}}
code{{background:#eaf1f5;padding:3px 6px;border-radius:5px}}
.ok{{color:#0f766e;font-weight:bold}} .bad{{color:#b42318;font-weight:bold}} .neutral{{color:#536471;font-weight:bold}}
.error{{margin-top:20px;padding:14px;background:#fff0ef;border-left:5px solid #b42318;border-radius:8px}}
.hint{{padding:10px 12px;background:#edf5f8;border-radius:8px;color:#536471}}
</style>
</head>
<body><main>
<h1>CloudLab alkalmazás</h1>
<p class="ok">Az alkalmazás működik.</p>
<p><strong>Host:</strong> <code>{socket.gethostname()}</code></p>
<p><strong>Verzió:</strong> <code>{APP_VERSION}</code></p>
<p><strong>Redis állapot:</strong> <span class="{css_class}">{redis_text}</span></p>
<p><strong>Látogatásszámláló:</strong> <code>{counter_text}</code></p>
{diagnostic}
<p>Health endpoint: <code>/health</code></p>
<p>Info endpoint: <code>/api/info</code></p>
</main></body></html>"""


@app.get("/health")
def health():
    return jsonify(status="ok"), 200


@app.get("/api/info")
def info():
    status = redis_status(increment=False)
    return jsonify(
        app="cloudlab",
        version=APP_VERSION,
        hostname=socket.gethostname(),
        redis_configured=status["configured"],
        redis=status["connected"],
        redis_host=REDIS_HOST or None,
        redis_port=REDIS_PORT if REDIS_HOST else None,
        counter=status["count"],
        redis_error=status["error"],
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
