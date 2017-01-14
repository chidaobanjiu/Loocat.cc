from wtforms import (
    widgets,
    StringField,
    TextField,
    TextAreaField,
    PasswordField,
    BooleanField,
    ValidationError
)


class CKTextAreaWidget(widgets.TextArea):
    """CKeditor form for Flask-Admin."""

    def __call__(self, field, **kwargs):
        """Define callable type(class)."""

        # Add a new class property ckeditor: `<input class=ckeditor ...>`
        kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    """Create a new Field type."""

    # Add a new widget `CKTextAreaField` inherit from TextAreaField.
    widget = CKTextAreaWidget()
