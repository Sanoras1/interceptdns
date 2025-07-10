import socketserver, sqlite3, socket
from dnslib import DNSRecord, QTYPE, RR, A
from datetime import datetime

block_file = "blockedList.txt"

def load_local_blocklist():
    try:
        with open(block_file, 'r') as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        print(f"[WARN] {block_file} not found, creating blocklist fromscratch.")
        open(block_file, 'w').close()
        return set()

BLOCKED = load_local_blocklist()

def log_dns_query(client_ip, domain):
    conn = sqlite3.connect("dns_log.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO dns_queries (timestamp, client_ip, domain)
        VALUES (?, ?, ?)
    ''', (datetime.now().isoformat(), client_ip, domain))
    conn.commit()
    conn.close()

class DNSHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data, sock = self.request
        request = DNSRecord.parse(data)
        qname = str(request.q.qname).strip('.')
        client_ip = self.client_address[0]

        log_dns_query(client_ip, qname)
            # middleman sitename and check against list
        if qname in BLOCKED:
            reply = request.reply()
            reply.add_answer(RR(qname, QTYPE.A, rdata=A("0.0.0.0")))
            print(f"[BLOCKED] {qname}")
            sock.sendto(reply.pack(), self.client_address)
        else:
            # Forward to real DNS
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as forward_sock:
                forward_sock.sendto(data, ("8.8.8.8", 53))
                response, _ = forward_sock.recvfrom(512)
            sock.sendto(response, self.client_address)

if __name__ == "__main__":
    print("Starting DNS server on port 53...")
    with socketserver.UDPServer(("0.0.0.0", 53), DNSHandler) as server:
        server.serve_forever()