#-*- coding=utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField(u'郵箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField(u'密碼', validators=[Required()])
    remember_me = BooleanField(u'保持登錄狀態')
    submit = SubmitField(u'登錄')


class RegistrationForm(Form):
    email = StringField(u'郵箱', validators=[Required(), Length(1, 64),
                                           Email()])
    username = StringField(u'用戶名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          u'用戶名只能由字母, '
                                          u'數字, 小數點及下劃線組成。')])
    password = PasswordField(u'密碼', validators=[
        Required(), EqualTo(u'password2', message='兩次密碼輸入必須匹配。')])
    password2 = PasswordField(u'確認密碼', validators=[Required()])
    submit = SubmitField(u'註冊')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'該郵箱已經註冊。')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'該用戶名已被佔用。')


class ChangePasswordForm(Form):
    old_password = PasswordField(u'舊密碼', validators=[Required()])
    password = PasswordField(u'新密碼', validators=[
        Required(), EqualTo(u'password2', message='兩次密碼輸入必須匹配。')])
    password2 = PasswordField(u'確認新密碼', validators=[Required()])
    submit = SubmitField(u'更新密碼')


class PasswordResetRequestForm(Form):
    email = StringField(u'郵箱', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField(u'重設密碼')


class PasswordResetForm(Form):
    email = StringField(u'郵箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField(u'新密碼', validators=[
        Required(), EqualTo(u'password2', message='兩次密碼輸入必須匹配。')])
    password2 = PasswordField(u'確認新密碼', validators=[Required()])
    submit = SubmitField(u'重設密碼')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'未知郵箱地址。')


class ChangeEmailForm(Form):
    email = StringField(u'新的郵箱', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField(u'密碼', validators=[Required()])
    submit = SubmitField(u'更新郵箱地址')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'該郵箱已被註冊。')
