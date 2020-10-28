from app import create_app, db
from flask_script import Manager, Server
from app.models import User
from flask_migrate import Migrate, MigrateCommand


app = create_app('production')
app = create_app('test')

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
manager.add_command('run', Server(use_debugger=True))


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    

def test_get_review_by_id(self, Review):

    self.new_review.save_review()
    got_reviews = Review.get_reviews(12345)
    self.assertTrue(len(got_reviews) == 1)

if __name__ == "__main__":
    manager.run()
