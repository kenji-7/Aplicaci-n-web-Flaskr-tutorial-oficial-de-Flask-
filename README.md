# Flaskr – Pruebas de software y métricas de calidad

Caso de estudio: **Flaskr**, aplicación de blog del tutorial oficial de Flask
(origen: https://github.com/pallets/flask, carpeta `examples/tutorial`).

## Contenido
| Carpeta / archivo | Descripción |
|---|---|
| `flaskr/` | Código de la aplicación (`__init__.py`, `auth.py`, `blog.py`, `db.py`, plantillas) |
| `tests/` | **Prueba 1 – Funcional** (24 casos con pytest; CP-FUN-01 y CP-FUN-02 en `test_auth.py`) |
| `pruebas_seguridad/` | **Prueba 2 – Seguridad** (CP-SEG-01 hash, CP-SEG-02 inyección SQL, CP-SEG-03 control de acceso) |
| `COMANDOS.txt` | Todos los comandos en orden (instalación, pruebas y métricas) |

## Instalación (Windows / PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

## Ejecutar
```powershell
flask --app flaskr init-db
flask --app flaskr run --debug          # http://127.0.0.1:5000
pytest -v                               # prueba funcional
pytest pruebas_seguridad -v -s          # prueba de seguridad
coverage run -m pytest; coverage report -m   # métrica 1: cobertura
radon cc flaskr -s -a                   # métrica 2: complejidad ciclomática
radon mi flaskr -s                      # métrica 3: índice de mantenibilidad
```

## Resultados obtenidos
- Prueba funcional: 24/24 aprobadas · Prueba de seguridad: 5/5 aprobadas
- Cobertura: 100 % (178/178 sentencias, 42/42 ramas)
- Complejidad ciclomática promedio: 2,44 (A) · máx. `register()` = 7 (B)
- Índice de mantenibilidad: todos los módulos grado A (promedio ≈ 76,7)
