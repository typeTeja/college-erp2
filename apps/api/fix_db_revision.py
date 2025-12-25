from sqlalchemy import text
from app.db.session import engine

def fix_revision():
    with engine.connect() as connection:
        # Force set the revision to the last known good state
        # 074c6a62ff84 is the revision for "add_student_import_module_tables"
        # which is the parent of our current "add_fee_management_tables" (b8f3c4d5e6a7)
        connection.execute(text("UPDATE alembic_version SET version_num = '074c6a62ff84'"))
        connection.commit()
        print("Successfully reset alembic_version to '074c6a62ff84'")

if __name__ == "__main__":
    fix_revision()
