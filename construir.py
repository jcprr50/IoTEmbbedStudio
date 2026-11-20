"""Arma indice.json a partir de librerias/<id>/ficha.json y los archivos de cada una.

    python construir.py

El indice trae, por librería: la ficha + el sha256 de cada archivo. El diseñador de Windows baja
indice.json, y de ahí los archivos de librerias/<id>/, y comprueba el hash antes de subirlos a la placa.
Este directorio es el contenido del repositorio público del catálogo.
"""
import hashlib
import json
import re
from pathlib import Path

AQUI = Path(__file__).parent
ID = re.compile(r"^[a-z0-9_]{1,24}$")
FORMATO = 1

libs = []
for carpeta in sorted((AQUI / "librerias").iterdir()):
    if not carpeta.is_dir():
        continue
    ficha = json.loads((carpeta / "ficha.json").read_text(encoding="utf-8"))
    if ficha["id"] != carpeta.name or not ID.match(ficha["id"]):
        raise SystemExit(f"{carpeta.name}: el id de la ficha debe ser el nombre de la carpeta (a-z, 0-9, _)")
    hashes = {}
    for nombre in ficha["archivos"]:
        archivo = carpeta / nombre
        if not archivo.exists():
            raise SystemExit(f"{carpeta.name}: falta {nombre}")
        hashes[nombre] = hashlib.sha256(archivo.read_bytes()).hexdigest()
    libs.append({**ficha, "sha256": hashes})

(AQUI / "indice.json").write_text(
    json.dumps({"formato": FORMATO, "librerias": libs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"indice.json: {len(libs)} librería(s)")
