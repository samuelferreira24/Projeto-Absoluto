from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlparse,parse_qs
import json,os
from .core import MiniCerebro
DB=os.environ.get("MINI_CEREBRO_DB","mini_cerebro.sqlite3")
class Handler(BaseHTTPRequestHandler):
    def sendj(self,obj,code=200):
        raw=json.dumps(obj,ensure_ascii=False,default=str).encode()
        self.send_response(code); self.send_header("Content-Type","application/json; charset=utf-8"); self.send_header("Content-Length",str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        u=urlparse(self.path); m=MiniCerebro(DB)
        if u.path=="/v1/status": return self.sendj(m.stats())
        if u.path=="/v1/search":
            q=parse_qs(u.query).get("q",[""])[0]
            if not q: return self.sendj({"error":"q_required"},400)
            return self.sendj([dict(zip(["id","name","path","source_kind","snippet"],r)) for r in m.search(q)])
        if u.path=="/v1/evidence":
            cid=parse_qs(u.query).get("id",["0"])[0]
            return self.sendj(m.evidence(int(cid)))
        return self.sendj({"error":"not_found"},404)
def run(host="127.0.0.1",port=8790): HTTPServer((host,port),Handler).serve_forever()
