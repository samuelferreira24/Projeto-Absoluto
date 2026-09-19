import argparse,json
from .core import MiniCerebro

def main():
    p=argparse.ArgumentParser(prog="mini-cerebro")
    sub=p.add_subparsers(dest="cmd",required=True)
    i=sub.add_parser("ingest"); i.add_argument("--source",required=True); i.add_argument("--db",default="mini_cerebro.sqlite3")
    s=sub.add_parser("search"); s.add_argument("query"); s.add_argument("--db",default="mini_cerebro.sqlite3"); s.add_argument("--limit",type=int,default=20)
    c=sub.add_parser("classify"); c.add_argument("--db",default="mini_cerebro.sqlite3")
    e=sub.add_parser("evidence"); e.add_argument("id",type=int); e.add_argument("--db",default="mini_cerebro.sqlite3")
    x=sub.add_parser("export"); x.add_argument("--out",default="mini_cerebro_export.json"); x.add_argument("--db",default="mini_cerebro.sqlite3")
    a=p.parse_args(); m=MiniCerebro(a.db)
    if a.cmd=="ingest": print(json.dumps(m.ingest_path(a.source),ensure_ascii=False,indent=2))
    elif a.cmd=="search": print(json.dumps(m.search(a.query,a.limit),ensure_ascii=False,indent=2))
    elif a.cmd=="classify": print(json.dumps(m.classify_documents(),ensure_ascii=False))
    elif a.cmd=="evidence": print(json.dumps(m.evidence(a.id),ensure_ascii=False,indent=2,default=str))
    elif a.cmd=="export": print(m.export(a.out))
if __name__=="__main__": main()
