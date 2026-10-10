import os
import re
import shutil
from pathlib import Path
from typing import Literal

import docker
from mcp.server.fastmcp import FastMCP

API_KEY = os.environ.get("VPS_MCP_API_KEY", "")
REPO_ROOT = Path("/repo").resolve()
WORKSPACE_ROOT = Path("/workspace").resolve()
MUTABLE_CONTAINERS = {
    name.strip()
    for name in os.environ.get(
        "VPS_MCP_MUTABLE_CONTAINERS",
        "code-server-bb55qbolrf4pqfl45gomnzyl",
    ).split(",")
    if name.strip()
}

if len(API_KEY) < 48:
    raise RuntimeError("VPS_MCP_API_KEY must be a strong secret (at least 48 characters)")

mcp = FastMCP(
    "VPS Direct Admin",
    instructions=(
        "Administre a VPS do usuário por ferramentas explícitas. "
        "Nunca tente executar comandos arbitrários. Antes de ações que parem "
        "serviços, confirme que o usuário pediu essa alteração. O ABS e os "
        "navegadores alternativos devem permanecer desligados até nova autorização."
    ),
)

docker_client = docker.DockerClient(base_url="unix:///var/run/docker.sock")


def _safe_relative_path(root_name: str, relative_path: str) -> Path:
    if root_name == "repo":
        root = REPO_ROOT
    elif root_name == "workspace":
        root = WORKSPACE_ROOT
    else:
        raise ValueError("root deve ser 'repo' ou 'workspace'")

    rel = Path(relative_path or ".")
    if rel.is_absolute():
        raise ValueError("Use caminho relativo à raiz escolhida")
    if any(part in {".git", ".ssh", "__pycache__"} for part in rel.parts):
        raise ValueError("Acesso a diretório restrito")
    if any(part.lower() in {".env", "id_rsa", "id_ed25519", "credentials.json", "secrets.json"} for part in rel.parts):
        raise ValueError("Acesso a arquivo de credenciais bloqueado")

    target = (root / rel).resolve()
    if target != root and root not in target.parents:
        raise ValueError("Caminho fora da raiz autorizada")
    return target


def _redact(text: str) -> str:
    patterns = [
        (r"(?i)(authorization\s*[:=]\s*bearer\s+)[^\s,;]+", r"\1[REDACTED]"),
        (r"(?i)((?:password|passwd|token|secret|api[_-]?key|client_secret)\s*[:=]\s*)[^\s,;]+", r"\1[REDACTED]"),
        (r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b", "[REDACTED_GITHUB_TOKEN]"),
    ]
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)
    return text


def _container(name: str):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", name):
        raise ValueError("Nome de contêiner inválido")
    return docker_client.containers.get(name)


@mcp.tool()
def vps_status() -> dict:
    """Retorna carga, memória e espaço em disco do host VPS, sem expor segredos."""
    host_proc = Path("/host/proc")
    load = (host_proc / "loadavg").read_text().strip()
    uptime_seconds = float((host_proc / "uptime").read_text().split()[0])
    meminfo = {}
    for line in (host_proc / "meminfo").read_text().splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meminfo[key] = value.strip()
    disk = shutil.disk_usage("/host")
    return {
        "host": os.environ.get("VPS_HOST_LABEL", "abs-vps-01"),
        "load_average": load,
        "uptime_seconds": int(uptime_seconds),
        "memory": {
            "total": meminfo.get("MemTotal"),
            "available": meminfo.get("MemAvailable"),
            "swap_total": meminfo.get("SwapTotal"),
            "swap_free": meminfo.get("SwapFree"),
        },
        "disk_root": {
            "total_bytes": disk.total,
            "used_bytes": disk.used,
            "free_bytes": disk.free,
            "percent_used": round(disk.used / disk.total * 100, 1) if disk.total else None,
        },
    }


@mcp.tool()
def list_containers(include_stopped: bool = True) -> list[dict]:
    """Lista contêineres Docker com estado, imagem, portas e reinicializações; omite variáveis de ambiente."""
    items = docker_client.containers.list(all=include_stopped)
    result = []
    for item in sorted(items, key=lambda c: c.name):
        ports = item.attrs.get("NetworkSettings", {}).get("Ports") or {}
        health = (item.attrs.get("State", {}).get("Health") or {}).get("Status")
        result.append({
            "name": item.name,
            "image": item.image.tags[0] if item.image.tags else item.image.short_id,
            "status": item.status,
            "health": health,
            "restart_count": item.attrs.get("RestartCount", 0),
            "ports": ports,
        })
    return result


@mcp.tool()
def inspect_container(name: str) -> dict:
    """Inspeciona estado não secreto de um contêiner existente."""
    item = _container(name)
    item.reload()
    state = item.attrs.get("State", {})
    return {
        "name": item.name,
        "image": item.image.tags[0] if item.image.tags else item.image.short_id,
        "status": item.status,
        "state": state.get("Status"),
        "health": (state.get("Health") or {}).get("Status"),
        "started_at": state.get("StartedAt"),
        "finished_at": state.get("FinishedAt"),
        "exit_code": state.get("ExitCode"),
        "restart_count": item.attrs.get("RestartCount", 0),
        "ports": item.attrs.get("NetworkSettings", {}).get("Ports") or {},
    }


@mcp.tool()
def container_logs(name: str, tail: int = 100) -> str:
    """Lê as últimas linhas dos logs de um contêiner, com redação básica de credenciais."""
    if tail < 1 or tail > 500:
        raise ValueError("tail deve estar entre 1 e 500")
    item = _container(name)
    raw = item.logs(tail=tail, timestamps=True).decode("utf-8", errors="replace")
    return _redact(raw)[-30000:]


@mcp.tool()
def list_files(root: Literal["repo", "workspace"] = "workspace", path: str = ".") -> list[dict]:
    """Lista arquivos dentro do repositório ou workspace autorizados, sem atravessar a raiz."""
    target = _safe_relative_path(root, path)
    if not target.exists():
        raise FileNotFoundError(path)
    if target.is_file():
        return [{"path": str(target.relative_to(REPO_ROOT if root == "repo" else WORKSPACE_ROOT)), "type": "file", "size": target.stat().st_size}]
    base = REPO_ROOT if root == "repo" else WORKSPACE_ROOT
    results = []
    for entry in sorted(target.rglob("*")):
        if len(results) >= 500:
            break
        if any(part in {".git", ".ssh", "__pycache__"} for part in entry.relative_to(base).parts):
            continue
        if entry.is_symlink():
            continue
        results.append({
            "path": str(entry.relative_to(base)),
            "type": "directory" if entry.is_dir() else "file",
            "size": entry.stat().st_size if entry.is_file() else None,
        })
    return results


@mcp.tool()
def read_file(root: Literal["repo", "workspace"], path: str) -> str:
    """Lê um arquivo de texto do repositório/workspace, exceto credenciais e arquivos restritos."""
    target = _safe_relative_path(root, path)
    if not target.is_file():
        raise FileNotFoundError(path)
    if target.stat().st_size > 200_000:
        raise ValueError("Arquivo maior que 200 KB; use leitura por partes em uma futura versão")
    return _redact(target.read_text(encoding="utf-8", errors="replace"))


@mcp.tool()
def write_file(root: Literal["repo", "workspace"], path: str, content: str) -> dict:
    """Cria ou substitui arquivo de texto apenas dentro do repositório/workspace autorizados."""
    if len(content.encode("utf-8")) > 200_000:
        raise ValueError("Conteúdo maior que 200 KB")
    target = _safe_relative_path(root, path)
    if target.exists() and target.is_dir():
        raise ValueError("O destino é um diretório")
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".vps-mcp-tmp")
    temporary.write_text(content, encoding="utf-8")
    os.replace(temporary, target)
    return {
        "written": True,
        "root": root,
        "path": str(target.relative_to(REPO_ROOT if root == "repo" else WORKSPACE_ROOT)),
        "bytes": target.stat().st_size,
    }


@mcp.tool()
def container_action(name: str, action: Literal["start", "stop", "restart"]) -> dict:
    """Inicia, para ou reinicia somente contêineres explicitamente autorizados por lista de permissão."""
    if name not in MUTABLE_CONTAINERS and not name.startswith("vps-workload-"):
        raise PermissionError(
            "Este contêiner não está na lista de alteração permitida. "
            "Não vou parar/reiniciar infraestrutura crítica por esta ferramenta."
        )
    item = _container(name)
    if action == "start":
        item.start()
    elif action == "stop":
        item.stop(timeout=20)
    else:
        item.restart(timeout=20)
    item.reload()
    return {"name": item.name, "action": action, "status": item.status}


class AuthAndHealth:
    """Protect MCP transport with a strong bearer token; expose only a generic health endpoint."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return
        path = scope.get("path", "")
        if path == "/healthz":
            body = b'{"status":"ok"}'
            await send({
                "type": "http.response.start",
                "status": 200,
                "headers": [(b"content-type", b"application/json"), (b"content-length", str(len(body)).encode())],
            })
            await send({"type": "http.response.body", "body": body})
            return
        if path.startswith("/mcp"):
            headers = dict(scope.get("headers", []))
            auth = headers.get(b"authorization", b"").decode("latin1")
            expected = "Bearer " + API_KEY
            if not auth or not __import__("hmac").compare_digest(auth, expected):
                body = b'{"error":"unauthorized"}'
                await send({
                    "type": "http.response.start",
                    "status": 401,
                    "headers": [
                        (b"content-type", b"application/json"),
                        (b"content-length", str(len(body)).encode()),
                        (b"www-authenticate", b"Bearer"),
                    ],
                })
                await send({"type": "http.response.body", "body": body})
                return
        await self.app(scope, receive, send)


app = AuthAndHealth(mcp.streamable_http_app())
