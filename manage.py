
import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db
from app.users.models import User

app = create_app()

manager = Manager(app)
migrate = Migrate(app, db, compare_type=True)


def make_shell_context():
    return dict(app=app, db=db, User=User)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def fake_data(table=None, csv_file=None):
    from app.utils.common import GenerateData

    tables = {klass.__tablename__: klass for klass in
              db.Model._decl_class_registry.values()
              if hasattr(klass, '__tablename__')}

    if table is not None:
        gd = GenerateData(model=tables[table], db=db, csv_file=csv_file)
        gd.generate_fake_data()
    else:
        import const

        for t in tables:
            FAKE_DATA_FILE = os.path.join(const.DATA_DIR, "fake_data",
                                          "%s.csv" % t)
            if os.path.exists(FAKE_DATA_FILE):
                gd = GenerateData(model=tables[t], db=db,
                                  csv_file=FAKE_DATA_FILE)
                gd.generate_fake_data()


if __name__ == "__main__":
    manager.run()
