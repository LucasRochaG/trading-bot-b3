import threading
import time
from main import main as run_bot
from dashboard.app import app as flask_app, os


def start_dashboard():
    port = int(os.getenv("PORT", "5000"))
    flask_app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False,
    )


if __name__ == "__main__":
    print("🚀 Iniciando Servidor do Dashboard em segundo plano...")
    dashboard_thread = threading.Thread(target=start_dashboard, daemon=True)
    dashboard_thread.start()

    time.sleep(2)
    print("🟢 Dashboard rodando em: http://localhost:5000")
    print("🤖 Iniciando o Robô B3...")

    run_bot()
