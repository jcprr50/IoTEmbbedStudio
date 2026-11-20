# Catálogo de librerías de IoTEmbedStudio

Librerías de código Python (sensores, pantallas) que el diseñador de Windows baja y sube a las placas.
Los widgets no van aquí.

- `indice.json`: lo que lee el diseñador (se genera con `python construir.py`; no se edita a mano).
- `librerias/<id>/`: `ficha.json` (nombre, versión, qué clases ofrece el editor) y los `.py`.

Para agregar una librería: crea su carpeta con `ficha.json` y los archivos, corre `python construir.py` y sube los cambios.
