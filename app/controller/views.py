from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from .forms import CKTextAreaField

class CustomView(BaseView):
    """View function of Flask-Admin for Custom page."""

    @expose('/')
    def index(self):
        return self.render('admin/custom.html')

    @expose('/second_page')
    def second_page(self):
        return self.render('admin/second_page.html')

class CustomModelView(ModelView):
    """View function of Flask_Admin for Models page."""
    pass

class PostView(CustomModelView):
    """View function of Flask_Admin for Post create/edit Page includedin Models page"""

    # Using the CKTextAreaField to replace the Field name is 'test'
    form_overrides = dict(body=CKTextAreaField)
    form_overrides = dict(body_html=CKTextAreaField)

    # Using Search box
    column_searchable_list = ('body', 'title')

    # Using Add Fitler box
    column_filters = ('timestamp',)

    # Custom the template for PostView
    # Using js Editor of ckeditor
    create_template = 'admin/post_edit.html'
    edit_template = 'admin/post_edit.html'
