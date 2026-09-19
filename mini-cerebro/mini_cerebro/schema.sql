CREATE TABLE IF NOT EXISTS sources (
 id INTEGER PRIMARY KEY,
 source_key TEXT UNIQUE NOT NULL,
 kind TEXT NOT NULL,
 path TEXT,
 sha256 TEXT,
 size INTEGER,
 mime TEXT,
 captured_at TEXT NOT NULL,
 metadata_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS documents (
 id INTEGER PRIMARY KEY,
 source_id INTEGER NOT NULL,
 path TEXT NOT NULL,
 name TEXT NOT NULL,
 extension TEXT,
 sha256 TEXT NOT NULL,
 size INTEGER NOT NULL,
 content_text TEXT,
 encoding TEXT,
 extraction_status TEXT NOT NULL,
 FOREIGN KEY(source_id) REFERENCES sources(id),
 UNIQUE(source_id,path)
);
CREATE TABLE IF NOT EXISTS git_commits (
 id INTEGER PRIMARY KEY,
 source_id INTEGER NOT NULL,
 sha TEXT UNIQUE NOT NULL,
 author TEXT,
 date TEXT,
 subject TEXT,
 body TEXT
);
CREATE TABLE IF NOT EXISTS claims (
 id INTEGER PRIMARY KEY,
 kind TEXT NOT NULL,
 statement TEXT NOT NULL,
 confidence TEXT NOT NULL,
 source_document_id INTEGER,
 source_commit_id INTEGER,
 evidence TEXT,
 created_at TEXT NOT NULL,
 FOREIGN KEY(source_document_id) REFERENCES documents(id),
 FOREIGN KEY(source_commit_id) REFERENCES git_commits(id)
);
CREATE TABLE IF NOT EXISTS relations (
 id INTEGER PRIMARY KEY,
 from_claim INTEGER NOT NULL,
 relation TEXT NOT NULL,
 to_claim INTEGER NOT NULL,
 evidence TEXT,
 FOREIGN KEY(from_claim) REFERENCES claims(id),
 FOREIGN KEY(to_claim) REFERENCES claims(id)
);
CREATE TABLE IF NOT EXISTS investigations (
 id INTEGER PRIMARY KEY,
 question TEXT NOT NULL,
 status TEXT NOT NULL,
 result TEXT,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL
);
CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
 name, path, content_text, content='documents', content_rowid='id'
);
CREATE TRIGGER IF NOT EXISTS documents_ai AFTER INSERT ON documents BEGIN
 INSERT INTO documents_fts(rowid,name,path,content_text)
 VALUES(new.id,new.name,new.path,coalesce(new.content_text,''));
END;
CREATE TRIGGER IF NOT EXISTS documents_ad AFTER DELETE ON documents BEGIN
 INSERT INTO documents_fts(documents_fts,rowid,name,path,content_text)
 VALUES('delete',old.id,old.name,old.path,old.content_text);
END;
