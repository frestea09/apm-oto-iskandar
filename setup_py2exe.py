import os
from setuptools import setup


def collect_assets(base_dir: str = "assets"):
    data = []
    if not os.path.isdir(base_dir):
        return data

    for root, _, files in os.walk(base_dir):
        if not files:
            continue
        rel_root = os.path.relpath(root, base_dir)
        target_dir = os.path.join(base_dir, rel_root) if rel_root != "." else base_dir
        source_paths = [os.path.join(root, f) for f in files]
        data.append((target_dir, source_paths))
    return data


setup(
    name="PencarianPasien",
    version="1.0.0",
    description="Bundled executable for aplikasi pencarian pasien RSUD Oto Iskandar Dinata",
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
