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
    g=sub.add_parser("ingest-github"); g.add_argument("repo_url"); g.add_argument("--destination"); g.add_argument("--db",default="mini_cerebro.sqlite3")
    st=sub.add_parser("stats"); st.add_argument("--db",default="mini_cerebro.sqlite3")
    sv=sub.add_parser("serve"); sv.add_argument("--db",default="mini_cerebro.sqlite3"); sv.add_argument("--port",type=int,default=8790)
    a=p.parse_args(); m=MiniCerebro(a.db)
    if a.cmd=="ingest": print(json.dumps(m.ingest_path(a.source),ensure_ascii=False,indent=2))
    elif a.cmd=="search": print(json.dumps(m.search(a.query,a.limit),ensure_ascii=False,indent=2))
    elif a.cmd=="classify": print(json.dumps(m.classify_documents(),ensure_ascii=False))
    elif a.cmd=="evidence": print(json.dumps(m.evidence(a.id),ensure_ascii=False,indent=2,default=str))
    elif a.cmd=="export": print(m.export(a.out))
    elif a.cmd=="ingest-github":
        from .github_source import ingest_github_repo
        print(json.dumps(ingest_github_repo(a.db,a.repo_url,a.destination),ensure_ascii=False,indent=2))
    elif a.cmd=="stats": print(json.dumps(m.stats(),ensure_ascii=False,indent=2))
    elif a.cmd=="serve":
        from .server import run; run(port=a.port)
if __name__=="__main__": main()
