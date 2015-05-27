from . import manager
from .. import admin
from models import Author, db
from forms import RBLoginForm
from flask import redirect, request, url_for, render_template, current_app, session
from flask.views import MethodView
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user, login_user, logout_user, login_required
from ReBloger.general.models import Navigation, Category, Tag, Post


class RBColumnFmtter(object):
    @staticmethod
    def count_post(v, c, m, p):
        return m.posts.count()


class RBBaseAdmin(ModelView):
    class Meta:
        database = db
    column_auto_select_related = False

    def is_accessible(self):
        return current_user.is_authenticated()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('manager.login'))


class RBAuthorAdmin(RBBaseAdmin):
    column_list = ('name', 'email', 'posts')
    column_searchable_list = ('name', 'email')
    column_formatters = dict(posts=RBColumnFmtter.count_post)


class RBCategoryAdmin(RBBaseAdmin):
    column_list = ('name', 'posts')
    column_formatters = dict(posts=RBColumnFmtter.count_post)


class RBTagAdmin(RBBaseAdmin):
    column_list = ('topic', 'posts')
    column_formatters = dict(posts=RBColumnFmtter.count_post)


class RBPostAdmin(RBBaseAdmin):
    inline_models = (Tag,)


class RBManagerLoginView(MethodView):
    template = 'manager/login.html'

    def __init__(self):
        super(RBManagerLoginView, self).__init__()
        self.content = {
            'title': current_app.config['REBLOGER_TITLE'],
            'form': RBLoginForm(),
            'message': session.get('message', None),
        }

    def get(self):
        return render_template(self.template, **self.content)

    def post(self):
        form = RBLoginForm()
        if form.validate_on_submit():
            author = Author.query.filter_by(email=form.email.data).first()
            if author is not None and author.verify_password(form.password.data):
                login_user(author, form.remember_me.data)
                return redirect(url_for('admin.index'))
            session['message'] = 'Login failed.'
        return render_template(self.template, **self.content)


RBAuthorAdmin = RBAuthorAdmin(Author, db.session)
RBNavigationAdmin = RBBaseAdmin(Navigation, db.session)
RBCategoryAdmin = RBCategoryAdmin(Category, db.session)
RBPostAdmin = RBPostAdmin(Post, db.session)
RBTagAdmin = RBTagAdmin(Tag, db.session)

admin.add_view(RBAuthorAdmin)
admin.add_view(RBNavigationAdmin)
admin.add_view(RBCategoryAdmin)
admin.add_view(RBPostAdmin)
admin.add_view(RBTagAdmin)
manager.add_url_rule('/login', view_func=RBManagerLoginView.as_view('login'))

@manager.route('/logout')
@login_required
def logout():
    logout_user()
    session['message'] = 'you have been logged out.'
    return redirect(url_for('.login'))