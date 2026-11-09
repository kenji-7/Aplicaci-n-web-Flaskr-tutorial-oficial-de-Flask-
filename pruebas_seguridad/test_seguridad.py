"""Prueba 2 - Prueba de seguridad (caja gris) sobre Flaskr.

CP-SEG-01 (RS1): las contrasenas se guardan como hash, nunca en texto plano.
CP-SEG-02 (RS2): el login resiste un intento de inyeccion SQL.
CP-SEG-03 (RS3): las rutas protegidas exigen autenticacion.

Ejecutar con:  pytest pruebas_seguridad -v -s
(-s muestra en consola la evidencia que se imprime en cada caso)
"""
import os
import tempfile

import pytest

from flaskr import create_app
from flaskr.db import get_db
from flaskr.db import init_db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({"TESTING": True, "DATABASE": db_path})
    with app.app_context():
        init_db()
    yield app
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


def test_cp_seg_01_password_hash(client, app):
    """CP-SEG-01: la contrasena se almacena cifrada (hash)."""
    clave = "MiClaveSegura123"
    client.post("/auth/register", data={"username": "alice", "password": clave})

    with app.app_context():
        guardado = (
            get_db()
            .execute("SELECT password FROM user WHERE username = 'alice'")
            .fetchone()["password"]
        )

    print("\n[CP-SEG-01] Contrasena ingresada :", clave)
    print("[CP-SEG-01] Valor guardado en BD  :", guardado[:40] + "...")
    print("[CP-SEG-01] Longitud del hash     :", len(guardado), "caracteres")

    assert clave not in guardado
    assert guardado.startswith("scrypt:")
    print("[CP-SEG-01] RESULTADO: APROBADO - la contrasena NO se guarda en texto plano")


def test_cp_seg_02_sql_injection(client, app):
    """CP-SEG-02: el login rechaza una cadena de inyeccion SQL."""
    client.post("/auth/register", data={"username": "alice", "password": "secreta"})
    ataque = "alice' OR '1'='1"

    response = client.post(
        "/auth/login", data={"username": ataque, "password": "cualquiera"}
    )

    print("\n[CP-SEG-02] Usuario enviado (ataque):", ataque)
    print("[CP-SEG-02] Codigo HTTP recibido    :", response.status_code)

    assert response.status_code == 200  # se queda en el login, no redirige
    assert b"Incorrect username." in response.data
    with client.session_transaction() as sess:
        assert "user_id" not in sess
    print("[CP-SEG-02] Mensaje mostrado        : Incorrect username.")
    print("[CP-SEG-02] RESULTADO: APROBADO - no se concede acceso (consultas parametrizadas)")


@pytest.mark.parametrize("ruta", ("/create", "/1/update", "/1/delete"))
def test_cp_seg_03_rutas_protegidas(client, ruta):
    """CP-SEG-03: sin sesion iniciada, las rutas sensibles redirigen al login."""
    response = client.post(ruta)

    print(f"\n[CP-SEG-03] POST {ruta:<10} -> {response.status_code} "
          f"redirige a {response.headers.get('Location')}")

    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/login"
