from ReBloger import db
from ReBloger import login_manager
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is nor a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate():
        init = Author(name='realityone', email='realityone@me.com', password='123456')
        db.session.add(init)
        db.session.commit()

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Author name:%s>' % self.name


@login_manager.user_loader
def load_author(author_id):
    return Author.query.get(int(author_id))