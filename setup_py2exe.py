import os
from pathlib import Path
from setuptools import setup

try:
    import py2exe  # noqa: F401
except ImportError:  # pragma: no cover
    raise SystemExit(
        "py2exe belum terpasang. Jalankan `pip install py2exe` di Windows lalu ulangi perintah build."
    )

BASE_DIR = Path(__file__).resolve().parent


def collect_assets(base_dir: Path = BASE_DIR / "assets"):
    """Collect asset files so py2exe copies them next to the executable."""

    data = []
    if not base_dir.is_dir():
        return data

    for root, _, files in os.walk(base_dir):
        if not files:
            continue

        root_path = Path(root)
        rel_root = root_path.relative_to(base_dir)
        target_dir = Path("assets") / rel_root if rel_root != Path(".") else Path("assets")
        source_paths = [str(root_path / f) for f in files]
        data.append((str(target_dir), source_paths))

    return data


setup(
    name="PencarianPasien",
    version="1.0.0",
    description="Bundled executable for aplikasi pencarian pasien RSUD Oto Iskandar Dinata",
    packages=["app"],
    py_modules=["main"],
    windows=[{"script": "main.py"}],
    options={
        "py2exe": {
            "includes": [
                "mysql.connector",
                "mysql.connector.locales.eng.client_error",
            ],
            "compressed": True,
            "optimize": 2,
            "bundle_files": 1,
        }
    },
    data_files=collect_assets(),
    zipfile=None,
)
