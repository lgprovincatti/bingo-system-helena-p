import socket
import threading
import time
import webbrowser

import requests
import uvicorn

from app.main import app


PORT = 8000


def get_local_ip():

    try:

        s = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        s.connect(("8.8.8.8", 80))

        ip = s.getsockname()[0]

        s.close()

        return ip

    except Exception:

        return "127.0.0.1"


LOCAL_IP = get_local_ip()


def start_server():

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        reload=False
    )


def wait_server():

    url = f"http://127.0.0.1:{PORT}"

    for _ in range(30):

        try:

            requests.get(url)

            return True

        except Exception:

            time.sleep(1)

    return False


if __name__ == "__main__":

    print("\n==============================")
    print("BINGO INICIADO")
    print("==============================")
    print(f"Local: http://127.0.0.1:{PORT}")
    print(f"Rede : http://{LOCAL_IP}:{PORT}")
    print("==============================\n")

    server_thread = threading.Thread(
        target=start_server,
        daemon=True
    )

    server_thread.start()

    if wait_server():

        webbrowser.open(
            f"http://127.0.0.1:{PORT}"
        )

    else:

        print("Servidor não respondeu.")

    while True:
        time.sleep(1)