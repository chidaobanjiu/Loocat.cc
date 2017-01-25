#-*- coding=utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, widgets, Field
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.widgets import TextInput
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User, Tag, Category

class NameForm(Form):
    name = StringField(u'你的名字。', validators=[Required()], default=u"你的名字")
    submit = SubmitField(u'提交')


class EditProfileForm(Form):
    name = StringField(u'真實姓名', validators=[Length(0, 64)])
    location = StringField(u'位置', validators=[Length(0, 64)])
    about_me = TextAreaField(u'自我介紹')
    submit = SubmitField(u'提交')


class EditProfileAdminForm(Form):
    email = StringField(u'郵箱', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField(u'用戶名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          u'用戶名只能由字母, '
                                          u'數字, 小數點及下劃線組成。')])
    confirmed = BooleanField(u'已確認')
    role = SelectField(u'選擇角色', coerce=int)
    name = StringField(u'真實姓名', validators=[Length(0, 64)])
    location = StringField(u'位置', validators=[Length(0, 64)])
    about_me = TextAreaField(u'自我介紹')
    submit = SubmitField(u'提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(u'該郵箱已經註冊。')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError(u'該用戶名已被佔用。')


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


class TagListField(Field):
    widget = TextInput()

    def __init__(self, label=None, validators=None,
                 **kwargs):
        super(TagListField, self).__init__(label, validators, **kwargs)

    def _value(self):
        if self.data:
            r = u''
            for obj in self.data:
                r += self.obj_to_str(obj)
            return r
        else:
            return u''

    def process_formdata(self, valuelist):
        print 'process_formdata..'
        print valuelist
        if valuelist:
            tags = self._remove_duplicates([x.strip() for x in valuelist[0].split()])
            self.data = [self.str_to_obj(tag) for tag in tags]
        else:
            self.data = None

    def pre_validate(self, form):
        pass

    @classmethod
    def _remove_duplicates(cls, seq):
        d = {}
        for item in seq:
            if item.lower() not in d:
                d[item.lower()] = True
                yield item

    @classmethod
    def str_to_obj(cls, tag):
        tag_obj = Tag.query.filter_by(name=tag).first()
        if tag_obj is None:
            tag_obj = Tag(name=tag)
        return tag_obj

    @classmethod
    def obj_to_str(cls, obj):
        if obj:
            return obj.name
        else:
            return u''

class PostFormM(Form):
    title = StringField(u"標題", validators=[Required()])
    category = SelectField(u"分類", coerce=int)
    tags = TagListField(u"標籤", validators=[Required()])
    body = TextAreaField(u"內容")
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(PostFormM, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                             for category in Category.query.order_by(Category.name).all()]


class PostFormC(Form):
    title = StringField(u"標題")
    category = SelectField(u"", coerce=int)
    tags = TagListField(u"標籤", validators=[Required()])
    body = TextAreaField(u"內容")
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(PostFormC, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                             for role in Category.query.order_by(Category.name).all()]


class CommentForm(Form):
    body = StringField('', validators=[Required()])
    submit = SubmitField(u'提交')
