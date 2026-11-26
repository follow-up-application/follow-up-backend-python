import hashlib
from pathlib import Path


def sha256_file(path: Path) -> str:
    """
    Calcula el hash SHA-256 de un archivo leyendolo en bloques de 1 MB
    para no sobrecargar la memoria RAM.
    """
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def job_path(storage_dir: Path, job_id, formato: str) -> Path:
    """
    Genera la ruta en disco para un documento organizandolo en subcarpetas
    segun los primeros 2 caracteres del UUID para optimizar el sistema de archivos.
    """
    folder = storage_dir / str(job_id)[:2]
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{job_id}.{formato}"
