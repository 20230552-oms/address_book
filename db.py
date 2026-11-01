import sqlite3

import click
from flask import current_app, g

# contacts 테이블 정의
# IF NOT EXISTS: 이미 테이블이 있으면 건너뛰므로 init-db를 다시 실행해도 데이터가 지워지지 않는다
SCHEMA = """
CREATE TABLE IF NOT EXISTS contacts (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    phone      TEXT NOT NULL,
    email      TEXT,
    address    TEXT,
    memo       TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);
"""


def get_db():
    """현재 요청에서 쓸 DB 연결을 돌려준다. 한 요청 안에서는 같은 연결을 재사용한다."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        # 조회 결과를 row["name"]처럼 컬럼 이름으로 꺼낼 수 있게 한다
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """요청이 끝나면 DB 연결을 닫는다."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """테이블을 만든다."""
    db = get_db()
    db.executescript(SCHEMA)
    db.commit()


@click.command("init-db")
def init_db_command():
    """터미널 명령: flask --app app init-db"""
    init_db()
    click.echo("데이터베이스를 초기화했습니다.")


def init_app(app):
    """앱에 DB 관련 기능을 등록한다. create_app()에서 호출한다."""
    # 요청이 끝날 때마다 close_db가 자동으로 호출되게 한다
    app.teardown_appcontext(close_db)
    # flask 명령어에 init-db를 추가한다
    app.cli.add_command(init_db_command)


def list_contacts(q=None):
    """연락처를 이름 가나다순으로 돌려준다.

    q가 있으면 이름 또는 전화번호에 q가 포함된 연락처만 돌려준다.
    전화번호는 하이픈을 빼고 비교한다. (01012 로 검색해도 010-1234-... 가 나온다)
    """
    if not q:
        return get_db().execute(
            "SELECT id, name, phone, email, address FROM contacts ORDER BY name, id"
        ).fetchall()

    name_pattern = "%" + escape_like(q) + "%"
    phone_q = q.replace("-", "")
    # 검색어가 하이픈뿐이면 전화번호 조건은 쓰지 않는다 (LIKE NULL 은 항상 거짓)
    phone_pattern = "%" + escape_like(phone_q) + "%" if phone_q else None

    # 검색어도 SQL 문자열에 붙이지 않고 ? 자리에 바인딩한다
    return get_db().execute(
        "SELECT id, name, phone, email, address FROM contacts"
        " WHERE name LIKE ? ESCAPE '\\'"
        "    OR REPLACE(phone, '-', '') LIKE ? ESCAPE '\\'"
        " ORDER BY name, id",
        (name_pattern, phone_pattern),
    ).fetchall()


def escape_like(text):
    """LIKE 검색에서 %, _ 가 '아무 글자'로 해석되지 않도록 앞에 \\ 를 붙인다."""
    return text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def create_contact(name, phone, email, address, memo):
    """연락처 하나를 저장한다. 값은 반드시 ? 자리에 바인딩한다."""
    db = get_db()
    db.execute(
        "INSERT INTO contacts (name, phone, email, address, memo) VALUES (?, ?, ?, ?, ?)",
        (name, phone, email, address, memo),
    )
    db.commit()


def get_contact(contact_id):
    """id로 연락처 하나를 찾는다. 없으면 None을 돌려준다."""
    return get_db().execute(
        "SELECT * FROM contacts WHERE id = ?", (contact_id,)
    ).fetchone()


def update_contact(contact_id, name, phone, email, address, memo):
    """연락처 내용을 바꾼다."""
    db = get_db()
    db.execute(
        "UPDATE contacts SET name = ?, phone = ?, email = ?, address = ?, memo = ? WHERE id = ?",
        (name, phone, email, address, memo, contact_id),
    )
    db.commit()


def delete_contact(contact_id):
    """연락처를 지운다."""
    db = get_db()
    db.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    db.commit()
