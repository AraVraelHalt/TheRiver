import requests
import socks
import socket

# Tell Python to use Tor's SOCKS5 proxy
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket

# Request a Tor-visible IP
try:
    print("[*] Checking IP through Tor...")
    r = requests.get("http://httpbin.org/ip", timeout=10)
    print("Success! IP is:", r.json())
except Exception as e:
    print("Error using Tor:", e)

