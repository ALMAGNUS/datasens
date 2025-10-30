from sqlalchemy import text
from scripts.init_postgres import get_engine


def run_crud_smoke():
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS _crud_test(id SERIAL PRIMARY KEY, name TEXT)"))
        conn.execute(text("INSERT INTO _crud_test(name) VALUES ('alpha'), ('beta')"))
        rows = conn.execute(text("SELECT * FROM _crud_test")).fetchall()
        assert len(rows) >= 2
        conn.execute(text("DELETE FROM _crud_test"))
    print("CRUD smoke OK")


if __name__ == "__main__":
    run_crud_smoke()


