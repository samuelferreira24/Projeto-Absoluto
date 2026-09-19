from __future__ import annotations
import hashlib,json,mimetypes,os,re,sqlite3,subprocess,zipfile
from datetime import datetime,timezone
from pathlib import Path

TEXT_EXT={".txt",".md",".markdown",".py",".js",".ts",".json",".jsonl",".yaml",".yml",".xml",".html",".htm",".css",".sh",".bash",".toml",".ini",".cfg",".csv",".sql",".java",".kt",".c",".cpp",".h",".hpp",".rs",".go",".swift",".php",".jsx",".tsx",".mjs",".log",".rst"}
IGNORE={".git",".venv","__pycache__","node_modules"}

def now(): return datetime.now(timezone.utc).isoformat()
def sha256(data): return hashlib.sha256(data).hexdigest()

class MiniCerebro:
    def __init__(self, db_path="mini_cerebro.sqlite3", store_dir=None):
        self.db=sqlite3.connect(db_path)
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.executescript(Path(__file__).with_name("schema.sql").read_text())
        self.store=Path(store_dir) if store_dir else Path(db_path).parent/"raw"
        self.store.mkdir(parents=True,exist_ok=True)
        self.db.commit()

    def _raw(self,data):
        h=sha256(data); p=self.store/h
        if not p.exists(): p.write_bytes(data)
        return str(p)

    def source(self,key,kind,path=None,meta=None,data=b""):
        cur=self.db.execute("""INSERT OR IGNORE INTO sources
        (source_key,kind,path,sha256,size,mime,captured_at,metadata_json)
        VALUES(?,?,?,?,?,?,?,?)""",(key,kind,path,sha256(data) if data else None,len(data) if data else None,
        mimetypes.guess_type(path or "")[0],now(),json.dumps(meta or {},ensure_ascii=False)))
        self.db.commit()
        return self.db.execute("SELECT id FROM sources WHERE source_key=?",(key,)).fetchone()[0]

    def document(self,source_id,path,data):
        ext=Path(path).suffix.lower()
        text=None; enc=None; status="binary"
        if ext in TEXT_EXT or data[:1] in (b"{",b"[",b"#"):
            try:
                text=data.decode("utf-8"); enc="utf-8"; status="extracted"
            except UnicodeDecodeError:
                try: text=data.decode("latin-1"); enc="latin-1"; status="extracted"
                except Exception: status="decode_error"
        self._raw(data)
        cur=self.db.execute("""INSERT OR IGNORE INTO documents
        (source_id,path,name,extension,sha256,size,content_text,encoding,extraction_status)
        VALUES(?,?,?,?,?,?,?,?,?)""",(source_id,path,Path(path).name,ext,sha256(data),len(data),text,enc,status))
        self.db.commit()
        return self.db.execute("SELECT id FROM documents WHERE source_id=? AND path=?",(source_id,path)).fetchone()[0]

    def ingest_path(self,src):
        src=Path(src).resolve()
        if src.is_file() and src.suffix.lower()==".zip": return self.ingest_zip(src)
        if src.is_dir(): return self.ingest_dir(src)
        raise ValueError("Fonte deve ser diretório ou ZIP")

    def ingest_dir(self,root):
        sid=self.source(str(root),"directory",str(root),{"readonly":True})
        count=0
        for p in root.rglob("*"):
            if not p.is_file() or any(part in IGNORE for part in p.parts): continue
            try: data=p.read_bytes()
            except OSError: continue
            self.document(sid,str(p.relative_to(root)),data); count+=1
        self.ingest_git(root,sid)
        return {"source_id":sid,"documents":count}

    def ingest_zip(self,zpath):
        raw=zpath.read_bytes()
        sid=self.source(str(zpath),"zip",str(zpath),{"readonly":True},raw)
        count=0
        with zipfile.ZipFile(zpath) as z:
            for info in z.infolist():
                if info.is_dir(): continue
                data=z.read(info)
                self.document(sid,info.filename,data); count+=1
        return {"source_id":sid,"documents":count,"zip_sha256":sha256(raw)}

    def ingest_git(self,root,sid):
        if not (root/".git").exists(): return
        try:
            out=subprocess.check_output(["git","-C",str(root),"log","--format=%H%x1f%an%x1f%aI%x1f%s%x1f%b%x1e","--all"],text=True,stderr=subprocess.DEVNULL)
        except Exception: return
        for rec in out.split("\x1e"):
            if not rec.strip(): continue
            a=rec.split("\x1f")
            if len(a)<5: continue
            self.db.execute("""INSERT OR IGNORE INTO git_commits(source_id,sha,author,date,subject,body)
            VALUES(?,?,?,?,?,?)""",(sid,*a[:5]))

        self.db.commit()

    def classify_documents(self):
        rows=self.db.execute("SELECT id,name,path,content_text FROM documents").fetchall()
        rules=[
          ("implementation",r"\b(class |def |function |import |require\(|CREATE TABLE|INSERT INTO|async |return )"),
          ("experiment",r"\b(experiment|teste|test|prototype|proof of concept|POC)\b"),
          ("failure",r"\b(falha|erro|bug|failure|limitation|problema|não funciona|nao funciona)\b"),
          ("decision",r"\b(decis[aã]o|decision|escolh|adotad|abandon|rejected)\b"),
          ("discovery",r"\b(descobert|discovery|aprend|lesson|lição|insight)\b"),
          ("hypothesis",r"\b(hip[oó]tese|hypothesis|poss[ií]vel|possibility|poderia|maybe)\b"),
        ]
        out=[]
        for did,name,path,text in rows:
            text=text or ""
            kinds=[k for k,p in rules if re.search(p,text,re.I)]
            if not kinds: kinds=["document"]
            for k in kinds:
                statement=f"Documento {path} classificado como {k}"
                cur=self.db.execute("""INSERT INTO claims(kind,statement,confidence,source_document_id,evidence,created_at)
                VALUES(?,?,?,?,?,?)""",(k,statement,"derived",did,"heuristic classification",now()))
                out.append(cur.lastrowid)
        self.db.commit(); return out

    def search(self,q,limit=20):
        return self.db.execute("""SELECT d.id,d.name,d.path,s.kind,
        snippet(documents_fts,2,'[',']','…',20)
        FROM documents_fts JOIN documents d ON d.id=documents_fts.rowid
        JOIN sources s ON s.id=d.source_id
        WHERE documents_fts MATCH ? LIMIT ?""",(q,limit)).fetchall()

    def evidence(self,claim_id):
        return self.db.execute("""SELECT c.*,d.path,s.path FROM claims c
        LEFT JOIN documents d ON d.id=c.source_document_id
        LEFT JOIN sources s ON s.id=d.source_id WHERE c.id=?""",(claim_id,)).fetchone()

    def export(self,out="mini_cerebro_export.json"):
        payload={}
        for table in ("sources","documents","git_commits","claims","relations","investigations"):
            rows=self.db.execute(f"SELECT * FROM {table}").fetchall()
            cols=[x[1] for x in self.db.execute(f"PRAGMA table_info({table})")]
            payload[table]=[dict(zip(cols,r)) for r in rows]
        Path(out).write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8")
        return out
