# server.py
# small runner: prefer waitress if available, fallback to Flask's builtin server
import os
try:
    from waitress import serve
    has_waitress = True
except Exception:
    has_waitress = False

from app import app

if __name__ == "__main__":
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", "5000"))
    if has_waitress:
        serve(app, host=host, port=port)
    else:
        app.run(host=host, port=port)
