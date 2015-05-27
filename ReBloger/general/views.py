from flask import current_app, render_template, request, abort, redirect, url_for
from flask.views import MethodView
from models import Post, Navigation, Category, Tag
from ReBloger.manager.models import Author
from ReBloger.general import general


class RBBaseView(MethodView):
    template = 'general/base.html'

    def __init__(self, *args, **kwargs):
        super(RBBaseView, self).__init__()
        self.content = {
            'blog_title': current_app.config['REBLOGER_TITLE'],
            'blog_details': current_app.config['REBLOGER_DETAILS'],
            'nav_list': Navigation.enumerate_all(),
            'category_list': Category.enumerate_all(),
            'tag_list': Tag.enumerate_all(),
            'recent_post_list': Post.get_recent_post()
        }

    def get(self, *args, **kwargs):
        return render_template(self.template, **self.content)


class RBIndexView(RBBaseView):
    template = 'general/index.html'

    def __init__(self, *args, **kwargs):
        super(RBIndexView, self).__init__(*args, **kwargs)
        self.new_content = dict()

    def get(self, *args, **kwargs):
        if 'p' not in kwargs:
            paginate_archive = Post.paginate_archive(page_num=1)
        elif kwargs['p'] == 1:
            return redirect(url_for('.index'))
        else:
            paginate_archive = Post.paginate_archive(page_num=kwargs['page_num'])
            self.new_content['archive_title'] = 'Index Page'

        self.new_content['post_paginate'] = paginate_archive
        self.content.update(self.new_content)
        return render_template(self.template, **self.content)


class RBPostView(RBBaseView):
    template = 'general/post.html'

    def __init__(self, *args, **kwargs):
        super(RBPostView, self).__init__(*args, **kwargs)
        self.new_content = dict()

    def get(self, post_id, *args, **kwargs):
        current_post_pag = Post.paginate_post(post_id=post_id)

        self.new_content['current_post_pag'] = current_post_pag
        self.content.update(self.new_content)
        return render_template(self.template, **self.content)


class RBArchiveView(RBBaseView):
    template = 'general/archive.html'

    def __init__(self, *args, **kwargs):
        super(RBArchiveView, self).__init__(*args, **kwargs)
        self.content['archive_title'] = 'Archive Page'
        self.new_content = dict()

    def get(self, *args, **kwargs):
        raise NotImplementedError('RBArchiveView not implemented yet.')


class RBCategoryView(RBArchiveView):
    template = 'general/category.html'

    def __init__(self, *args, **kwargs):
        super(RBCategoryView, self).__init__(*args, **kwargs)

    def get(self, category_name, *args, **kwargs):
        page_num = request.args.get('page_num', 1, type=int)
        current_category = Category.query.filter_by(name=category_name).first()
        if current_category is None:
            abort(404)
        post_paginate = current_category.posts.paginate(
            page_num, per_page=current_app.config['ARCHIVE_QUANTITY'], error_out=True
        )
        self.new_content['current_category'] = current_category
        self.new_content['post_paginate'] = post_paginate
        self.content.update(self.new_content)
        return render_template(self.template, **self.content)


class RBTagView(RBArchiveView):
    template = 'general/tag.html'

    def __init__(self, *args, **kwargs):
        super(RBTagView, self).__init__(*args, **kwargs)

    def get(self, topic, *args, **kwargs):
        page_num = request.args.get('page_num', 1, type=int)
        current_tag = Tag.query.filter_by(topic=topic).first()
        if current_tag is None:
            abort(404)
        post_paginate = current_tag.posts.paginate(
            page_num, per_page=current_app.config['ARCHIVE_QUANTITY'], error_out=True
        )
        self.new_content['current_tag'] = current_tag
        self.new_content['post_paginate'] = post_paginate
        self.content.update(self.new_content)
        return render_template(self.template, **self.content)


class RBAuthorView(RBArchiveView):
    template = 'general/author.html'

    def __init__(self, *args, **kwargs):
        super(RBAuthorView, self).__init__(*args, **kwargs)

    def get(self, author_name, *args, **kwargs):
        page_num = request.args.get('page_num', 1, type=int)
        current_author = Author.query.filter_by(name=author_name).first()
        if current_author is None:
            abort(404)
        post_paginate = current_author.posts.paginate(
            page_num, per_page=current_app.config['ARCHIVE_QUANTITY'], error_out=True
        )
        self.new_content['current_author'] = current_author
        self.new_content['post_paginate'] = post_paginate
        self.content.update(self.new_content)
        return render_template(self.template, **self.content)


general.add_url_rule('/', view_func=RBIndexView.as_view('index'))
general.add_url_rule('/archive/<int:p>', view_func=RBArchiveView.as_view('archive'))
general.add_url_rule('/page/<int:p>', view_func=RBIndexView.as_view('page'))
general.add_url_rule('/post/<int:post_id>', view_func=RBPostView.as_view('post'))
general.add_url_rule('/tag/<string:topic>', view_func=RBTagView.as_view('tag'))
general.add_url_rule('/author/<string:author_name>', view_func=RBAuthorView.as_view('author'))
general.add_url_rule('/category/<string:category_name>', view_func=RBCategoryView.as_view('category'))


@general.route('/search')
def search():
    return '<h1>search %s</h1>' % request.args.get('key', '')
