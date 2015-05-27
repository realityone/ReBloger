# encoding=utf-8

from datetime import datetime
from flask import url_for, current_app
from ReBloger import db
from markdown2 import markdown

class Navigation(db.Model):
    __tablename__ = 'navigation_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    endpoint = db.Column(db.String(64), default='wrong.endpoint')
    specific_url = db.Column(db.String(128), default='#index')

    @property
    def target_url(self):
        try:
            return url_for(self.endpoint)
        except Exception, e:
            return self.specific_url

    @classmethod
    def generate(cls):
        db.session.add(cls(name=u'首页', endpoint='general.index'))
        db.session.commit()

    @classmethod
    def enumerate_all(cls):
        return cls.query.order_by(cls.id.asc()).all()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Navigation %r>' % self.name


post_to_tag = db.Table(
    'post_to_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag.id', db.Integer, db.ForeignKey('tags.id'))
)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True)
    markdown = db.Column(db.UnicodeText())
    datetime = db.Column(db.DateTime(), autoincrement=True)
    hidden = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    tags = db.relationship('Tag',
                           secondary=post_to_tag,
                           backref=db.backref('posts', lazy='dynamic'),
                           lazy='dynamic')

    @property
    def markdown_html(self):
        print markdown(self.markdown)
        return markdown(self.markdown)

    @property
    def summary(self):
        more_tag = self.markdown_html.find('<!--more-->')
        return self.markdown_html[:more_tag]

    @classmethod
    def get_recent_post(cls):
        post_list = cls.query.order_by(cls.datetime.desc()).limit(current_app.config['RECENTPOST_QUANTITY'])
        return post_list

    @classmethod
    def paginate_post(cls, post_id=1):
        current_post = cls.query.paginate(
            post_id, per_page=1, error_out=True
        )
        return current_post

    @classmethod
    def paginate_archive(cls, page_num=1, start_datetime=None, end_datetime=None):
        archive_posts = list()
        if start_datetime is None and end_datetime is None:
            archive_posts = cls.query.order_by(cls.id.desc()).paginate(
                page_num, per_page=current_app.config['ARCHIVE_QUANTITY'],
                error_out=True
            )
        else:
            start_datetime = start_datetime or datetime.today()
            end_datetime = end_datetime or datetime.today()
            archive_posts = cls.query.filter_by(cls.datetime <= start_datetime, cls.datetime >= end_datetime).paginate(
                page_num, per_page=current_app.config['ARCHIVE_QUANTITY'],
                error_out=False
            )
        return archive_posts

    @classmethod
    def enumerate_all(cls, limit=None):
        return cls.query.order_by(cls.id.desc()).all()

    @staticmethod
    def generate():
        from ReBloger.manager.models import Author
        from random import seed, randint
        import forgery_py

        seed()
        tag_count = Tag.query.count()
        cat_count = Category.query.count()
        author_count = Author.query.count()
        for i in xrange(30):
            t = Tag.query.offset(randint(0, tag_count - 1)).limit(randint(1, tag_count - 1)).all()
            c = Category.query.offset(randint(0, cat_count - 1)).first()
            a = Author.query.offset(randint(0, author_count - 1)).first()
            p = Post(title=forgery_py.lorem_ipsum.title(),
                     markdown=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                     datetime=forgery_py.date.date(True),
                     author=a,
                     category=c,
                     tags=t)
            db.session.add(p)
            db.session.commit()

    def __unicode__(self):
        return '%s' % self.title

    def __repr__(self):
        return '<Post id: %r title: %r>' % (self.id, self.title)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    posts = db.relationship('Post', backref='category', lazy='dynamic')

    @property
    def post_quantity(self):
        return self.posts.count()

    @classmethod
    def enumerate_all(cls):
        return cls.query.all()

    @classmethod
    def generate(cls):
        init = cls(name=u'测试分类')
        db.session.add(init)
        db.session.commit()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Category %r>' % self.name


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(64), unique=True)

    @property
    def post_quantity(self):
        return self.posts.count()

    @classmethod
    def generate(cls):
        init = []
        for i in xrange(5):
            init.append(cls(topic=u'测试标签%d' % i))
        db.session.add_all(init)
        db.session.commit()

    @classmethod
    def enumerate_all(cls):
        return cls.query.all()

    def __unicode__(self):
        return self.topic

    def __repr__(self):
        return '<Tag %r>' % self.topic
