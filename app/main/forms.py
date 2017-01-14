# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, widgets, SelectMultipleField
from wtforms.widgets import ListWidget
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User, Tag

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class CKTextAreaWidget(widgets.TextArea):
    """CKeditor form for Flask-Admin."""

    def __call__(self, field, **kwargs):
        """Define callable type(class)."""

        # Add a new class property ckeditor: '<input class=ckeditor...>'
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    """Create a new Field type"""

    # Add a new widget 'CKTextAreaField' inherit from TextAreaField
    widget = CKTextAreaWidget()




class PostFormM(Form):
    title = StringField("Title", validators=[Required()])
    body = TextAreaField("Content")
    tags = SelectMultipleField("Tags", coerce=int)
    new_tag = StringField("New_Tag", validators=[Required()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(PostFormM, self).__init__(*args,**kwargs)
        self.tags.choices = [(tag.id, tag.name)
                                for tag in Tag.query.order_by(Tag.name).all()]

    def validate_tag(self, field, post):
        if field.data != Tag.query.filter_by(name=field.data).first():
            Tag.add_tag(field.data, post)


class PostFormC(Form):
    title = StringField("Title")
    body = TextAreaField("Content")
    tags = SelectMultipleField("Tags", validators=[Required()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(PostFormC, self).__init__(*args,**kwargs)
        self.tags.choices = [(tag.id, tag.name)
                                for tag in Tag.query.order_by(Tag.name).all()]

    def validate_tag(self, field, post):
        if field.data != Tag.query.filter_by(name=field.data).first():
            Tag.add_tag(field.data, post)


class CommentForm(Form):
    body = StringField('Enter your comment', validators=[Required()])
    submit = SubmitField('Submit')
