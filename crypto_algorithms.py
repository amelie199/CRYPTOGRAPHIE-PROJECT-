"""
=============================================================================
  CryptoLab — Secure Chat Server  (TP6 Ex6.1)
=============================================================================
  python chat_server.py

  - No external libraries: pure stdlib + project AES from crypto_algorithms.py
  - Persistent connections: clients stay connected and receive all messages
  - Broadcast: when A sends → server forwards encrypted copy to ALL other clients
  - HTTP API on port+1 (e.g. 10000): lets the Streamlit app poll new messages
=============================================================================
"""

import sys, os, socket, struct, threading, hashlib, hmac as _hmac, secrets
import random, json, time
from http.server import BaseHTTPRequestHandler, HTTPServer

# ── Load project AES ──────────────────────────────────────────────────────────
try:
    from crypto_algorithms import AES as _AES
    print("[ok] crypto_algorithms.py loaded — pure-Python AES ready")
except ImportError:
    print("[!!] crypto_algorithms.py not found — place it in the same folder!")
    sys.exit(1)


# ══════════════════════════════════════════════════════════════════════════════
#  CRYPTO HELPERS  (no external libs)
# ══════════════════════════════════════════════════════════════════════════════

def aes_enc(pt: bytes, key_hex: str, iv: bytes) -> bytes:
    return _AES.encrypt_cbc(pt, key_hex, iv)

def aes_dec(ct: bytes, key_hex: str, iv: bytes) -> bytes:
    return _AES.decrypt_cbc(ct, key_hex, iv)

def hmac_hex(key: bytes, data: bytes) -> str:
    return _hmac.new(key, data, hashlib.sha256).hexdigest()   # 64 chars

def hmac_ok(key: bytes, data: bytes, got: str) -> bool:
    return _hmac.compare_digest(hmac_hex(key, data), got)

# Packet: IV(16) | HMAC_hex(64 ASCII) | AES-CBC ciphertext
def pack(text: str, key_hex: str) -> bytes:
    data = text.encode()
    iv   = secrets.token_bytes(16)
    mac  = hmac_hex(bytes.fromhex(key_hex), data)
    ct   = aes_enc(data, key_hex, iv)
    return iv + mac.encode() + ct

def unpack(payload: bytes, key_hex: str):
    """Returns (plaintext_str, iv_hex, mac_hex, ct_hex) or raises."""
    iv  = payload[:16]
    mac = payload[16:80].decode()
    ct  = payload[80:]
    pt  = aes_dec(ct, key_hex, iv)
    if not hmac_ok(bytes.fromhex(key_hex), pt, mac):
        raise ValueError("HMAC FAILED")
    return pt.decode(), iv.hex(), mac, ct.hex()


# ══════════════════════════════════════════════════════════════════════════════
#  RSA  (stdlib only, 1024-bit)
# ══════════════════════════════════════════════════════════════════════════════

def _mr(n, k=20):
    if n < 2: return False
    if n in (2,3): return True
    if n%2==0: return False
    r,d=0,n-1
    while d%2==0: r+=1; d//=2
    for _ in range(k):
        a=random.randrange(2,n-1); x=pow(a,d,n)
        if x in(1,n-1): continue
        for _ in range(r-1):
            x=pow(x,2,n)
            if x==n-1: break
        else: return False
    return True

def _prime(b):
    while True:
        p=random.getrandbits(b)|(1<<b-1)|1
        if _mr(p): return p

def _modinv(a,m):
    g,x=m,0; b,y=a%m,1
    while b: q=g//b; g,x,b,y=b,y,g-q*b,x-q*y
    return x%m

def rsa_keygen(bits=1024):
    p,q=_prime(bits//2),_prime(bits//2)
    n=p*q; e=65537
    return {'n':n,'e':e,'d':_modinv(e,(p-1)*(q-1))}

def rsa_enc(data:bytes,e,n)->bytes:
    bl=(n.bit_length()+7)//8
    return pow(int.from_bytes(data,'big'),e,n).to_bytes(bl,'big')

def rsa_dec(data:bytes,d,n)->bytes:
    bl=(n.bit_length()+7)//8
    raw=pow(int.from_bytes(data,'big'),d,n).to_bytes(bl,'big')
    return raw.lstrip(b'\x00') or b'\x00'


# ══════════════════════════════════════════════════════════════════════════════
#  SOCKET FRAMING
# ══════════════════════════════════════════════════════════════════════════════

def _exact(sock, n):
    buf=b''
    while len(buf)<n:
        c=sock.recv(n-len(buf))
        if not c: return b''
        buf+=c
    return buf

def send_pkt(sock, data:bytes):
    sock.sendall(struct.pack('>I',len(data))+data)

def recv_pkt(sock)->bytes:
    h=_exact(sock,4)
    return _exact(sock,struct.unpack('>I',h)[0]) if h else b''


# ══════════════════════════════════════════════════════════════════════════════
#  ROOM  — shared state for all connected clients
# ══════════════════════════════════════════════════════════════════════════════

class Room:
    def __init__(self):
        self._lock    = threading.Lock()
        self.clients  = {}   # name → ClientConn
        # Global message log (all messages ever received)
        self.messages = []   # list of dicts

    def add(self, name, client):
        with self._lock:
            self.clients[name] = client
        print(f"  [room] '{name}' joined  ({len(self.clients)} online)")

    def remove(self, name):
        with self._lock:
            self.clients.pop(name, None)
        print(f"  [room] '{name}' left  ({len(self.clients)} online)")

    def broadcast(self, sender_name: str, plaintext: str,
                  iv_hex: str, ct_hex: str, mac_hex: str,
                  sender_key: str):
        """
        Store message + forward an encrypted copy to every OTHER client.
        Each recipient gets the message encrypted with THEIR own session key.
        """
        entry = {
            'id':        len(self.messages),
            'from':      sender_name,
            'text':      plaintext,
            'iv':        iv_hex,
            'ct':        ct_hex,
            'mac':       mac_hex,
            'ts':        time.strftime('%H:%M:%S'),
        }
        with self._lock:
            self.messages.append(entry)
            targets = {n: c for n, c in self.clients.items() if n != sender_name}

        # Forward to each recipient (encrypted with recipient's own key)
        for rname, rclient in targets.items():
            try:
                fwd_text = f"[{sender_name}] {plaintext}"
                fwd_pkt  = pack(fwd_text, rclient.session_key)
                send_pkt(rclient.conn, fwd_pkt)
                print(f"  [fwd] '{sender_name}' → '{rname}'  \"{plaintext}\"")
            except Exception as ex:
                print(f"  [!] forward to '{rname}' failed: {ex}")

    def get_messages_since(self, since_id: int):
        with self._lock:
            return [m for m in self.messages if m['id'] >= since_id]

    def online_names(self):
        with self._lock:
            return list(self.clients.keys())


# ══════════════════════════════════════════════════════════════════════════════
#  CLIENT CONNECTION
# ══════════════════════════════════════════════════════════════════════════════

class ClientConn(threading.Thread):
    def __init__(self, conn, addr, rsa, room: Room):
        super().__init__(daemon=True)
        self.conn        = conn
        self.addr        = addr
        self.rsa         = rsa
        self.room        = room
        self.session_key = None
        self.name        = None

    def run(self):
        try:
            if not self._handshake():
                return
            self._loop()
        except (ConnectionResetError, BrokenPipeError, OSError):
            pass
        except Exception as e:
            print(f"  [!] {self.name or self.addr}: {e}")
        finally:
            if self.name:
                self.room.remove(self.name)
                # notify others
                try:
                    self.room.broadcast(
                        "SERVER",
                        f"{self.name} left the chat.",
                        "0"*32, "0"*32, "0"*64,
                        self.session_key
                    )
                except Exception:
                    pass
            self.conn.close()

    def _handshake(self) -> bool:
        # 1 — send RSA public key
        send_pkt(self.conn, f"{self.rsa['n']:x}|{self.rsa['e']:x}".encode())

        # 2 — receive RSA-encrypted AES session key
        enc = recv_pkt(self.conn)
        if not enc: return False
        kb = rsa_dec(enc, self.rsa['d'], self.rsa['n'])
        self.session_key = kb[:32].hex()

        # 3 — receive device name
        name_pkt = recv_pkt(self.conn)
        if not name_pkt: return False
        self.name = name_pkt.decode(errors='replace')[:32].strip() or f"user_{self.addr[1]}"

        # 4 — send HANDSHAKE_OK
        send_pkt(self.conn, pack("HANDSHAKE_OK", self.session_key))
        print(f"  [hs] '{self.name}' ({self.addr[0]}) — key:{self.session_key[:12]}…")

        self.room.add(self.name, self)

        # Notify others
        self.room.broadcast(
            "SERVER",
            f"{self.name} joined the chat.",
            "0"*32, "0"*32, "0"*64,
            self.session_key
        )
        return True

    def _loop(self):
        while True:
            payload = recv_pkt(self.conn)
            if not payload:
                break
            try:
                text, iv_h, mac_h, ct_h = unpack(payload, self.session_key)
                print(f"\n  📨 '{self.name}': \"{text}\"")
                print(f"     IV : {iv_h}  CT: {ct_h[:32]}…")

                # Broadcast to all others
                self.room.broadcast(self.name, text, iv_h, ct_h, mac_h,
                                    self.session_key)

                # ACK to sender
                send_pkt(self.conn, pack(f"DELIVERED to {len(self.room.clients)-1} client(s)", self.session_key))

            except ValueError as e:
                print(f"  ✗ '{self.name}': {e}")


# ══════════════════════════════════════════════════════════════════════════════
#  HTTP API  (for Streamlit polling — no websockets needed)
# ══════════════════════════════════════════════════════════════════════════════

def make_http_handler(room: Room):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a): pass   # silence access log

        def do_GET(self):
            # GET /messages?since=N  →  JSON list of new messages
            # GET /online            →  JSON list of online names
            path = self.path.split('?')[0]
            params = {}
            if '?' in self.path:
                for p in self.path.split('?')[1].split('&'):
                    if '=' in p:
                        k,v = p.split('=',1)
                        params[k] = v

            if path == '/messages':
                since = int(params.get('since', 0))
                msgs  = room.get_messages_since(since)
                body  = json.dumps(msgs).encode()
            elif path == '/online':
                body  = json.dumps(room.online_names()).encode()
            else:
                body  = b'{"error":"unknown path"}'

            self.send_response(200)
            self.send_header('Content-Type','application/json')
            self.send_header('Content-Length', len(body))
            self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()
            self.wfile.write(body)

    return Handler


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main(tcp_port=9999):
    http_port = tcp_port + 1   # HTTP API on 10000 by default

    print("=" * 62)
    print("  CryptoLab — Secure Chat Server  (TP6 Ex6.1)")
    print("=" * 62)
    print(f"\n  Generating RSA-1024 key pair…", end='', flush=True)
    rsa = rsa_keygen(1024)
    print(" done ✓")
    print(f"  e = {rsa['e']}    n = {hex(rsa['n'])[:22]}…")

    room = Room()

    # ── Start HTTP API thread ─────────────────────────────────────────────────
    api = HTTPServer(('0.0.0.0', http_port), make_http_handler(room))
    threading.Thread(target=api.serve_forever, daemon=True).start()

    print(f"\n  TCP  chat port : {tcp_port}")
    print(f"  HTTP poll port : {http_port}  (used by Streamlit app)")
    print("  ──────────────────────────────────────────────────────")
    print("  Find your local IP:")
    print("    Windows → ipconfig")
    print("    Linux   → ip addr   or   hostname -I")
    print("  ──────────────────────────────────────────────────────")
    print("  Open CryptoLab on BOTH devices → 'Live Secure Chat'")
    print(f"  Enter your PC IP + port {tcp_port} → Connect → Chat!\n")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(('0.0.0.0', tcp_port))
        srv.listen(10)
        print(f"  [*] Waiting for connections…\n")
        try:
            while True:
                conn, addr = srv.accept()
                print(f"  [+] {addr[0]}:{addr[1]} connected")
                ClientConn(conn, addr, rsa, room).start()
        except KeyboardInterrupt:
            print("\n\n  [!] Server stopped.")
            msgs = room.get_messages_since(0)
            if msgs:
                print(f"\n  ── {len(msgs)} message(s) ──")
                for m in msgs:
                    if m['from'] != 'SERVER':
                        print(f"  [{m['ts']}] {m['from']}: \"{m['text']}\"")
                        print(f"    ct: {m['ct'][:40]}…")


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 9999)
