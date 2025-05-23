from stem.process import launch_tor_with_config
from aiohttp import ClientSession, ClientWebSocketResponse
from aiohttp_socks import ProxyConnector
import socks
import socket
import asyncio
import websockets
import atexit
import time
import threading
import itertools
import sys
import os

# Spinner animation
def show_spinner(stop_event):
    spinner = itertools.cycle(['⣾','⣽','⣻','⢿','⡿','⣟','⣯','⣷'])
    while not stop_event.is_set():
        sys.stdout.write('\033[3J\033c')
        sys.stdout.flush()
        sys.stdout.write(f"[ {next(spinner)} ] Connecting securely through the anonymous network...")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\033[3J\033c')
    sys.stdout.flush()
    sys.stdout.write("[✔] Connection success!\n")
    sys.stdout.flush()

# --- Initialize Terminal ---
sys.stdout.write('\033[3J\033c')
sys.stdout.flush()

# --- Start Spinner ---
stop_spinner = threading.Event()
spinner_thread = threading.Thread(target=show_spinner, args=(stop_spinner,))
spinner_thread.start()

# --- Start Tor internally ---
tor_process = launch_tor_with_config(
    config={
        'SocksPort': '9050',
    },
    init_msg_handler=None
)

# Ensure Tor shuts down when the app exits
atexit.register(tor_process.kill)

# --- Configure Tor SOCKS5 Proxy ---
#socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
#socket.socket = socks.socksocket

# --- WebSocket Test Through Tor ---
async def main():
    try:
        uri = 'ws://shvzeaizsp6brdfida2udgig3rkquzwenmnoqrg4lwr2xrsozzha52ad.onion:13759'

        connector = ProxyConnector.from_url('socks5://127.0.0.1:9050')

        async with ClientSession(connector=connector) as session:
            async with session.ws_connect(uri) as ws:
                stop_spinner.set()
                spinner_thread.join()
                await ws.send_str("__READY__")
                os.write(1, b"__READY__\n")
                async for msg in ws:
                    break
    except Exception as e:
        print("[!] Error:", e)

asyncio.run(main())

