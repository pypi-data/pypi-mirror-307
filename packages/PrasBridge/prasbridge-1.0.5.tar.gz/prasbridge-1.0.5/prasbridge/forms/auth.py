from django import forms
from django.contrib.auth.hashers import check_password  
from ..session import SQLAlchemySessionManager
from django.contrib.auth.hashers import make_password
from ..forms.fields import CharField, EmailField, TextAreaField
import warnings
from ..error import pError

session_manager = SQLAlchemySessionManager()


class AuthenticationForm(forms.Form):
    username = CharField(max_length=255, required=True)
    password = CharField(type="password", required=False)

    def __init__(self, model: object = None, *args, **kwargs):
        self.session = session_manager.get_session()  
        self.User = model
        super().__init__(*args, **kwargs)

        if self.User is None or not hasattr(self.User, 'password') or not hasattr(self.User, 'username'):
            raise pError("AuthenticationForm must be linked to a valid user model.")
        
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = self.session.query(self.User).filter_by(username=username).first()

            if user is None:
                raise forms.ValidationError("Invalid username or password")

            if not check_password(password, user.password):
                raise forms.ValidationError("Invalid username or password")

            cleaned_data['user'] = user

        return cleaned_data
    

class RegistrationForm(forms.Form):
    first_name = CharField(max_length=30, required=True)
    last_name = CharField(max_length=30, required=True)
    username = CharField(max_length=255, required=True)
    email = EmailField(required=True)
    password = CharField(type="password", required=True)
    password_confirm = CharField(type="password", required=True)

    def __init__(self, model: object = None, *args, **kwargs):
        self.session = session_manager.get_session()
        self.User = model
        super().__init__(*args, **kwargs)  

        required_fields = ['username', 'email', 'password']
        if self.User is None:
            raise pError("RegistrationForm must be linked to a valid user model.")
        
        missing_fields = [field for field in required_fields if field not in self.User.__dict__]
        if missing_fields:
            raise pError(f"RegistrationForm must be linked to a valid user model. Your model is missing the following fields: {', '.join(missing_fields)}")


        
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea) and not isinstance(field, TextAreaField):
                warnings.warn(
                    f"The field '{field_name}' is using the Django form 'Textarea'. "
                    "Please use the 'TextAreaField' from PRAS instead to ensure proper functionality.",
                    UserWarning,
                )
            elif isinstance(field, forms.EmailField) and not isinstance(field, EmailField):
                warnings.warn(
                    f"The field '{field_name}' is using the Django form 'EmailField'. "
                    "Please use the 'EmailField' from PRAS instead to ensure proper functionality.",
                    UserWarning,
                )
            elif isinstance(field, forms.CharField) and not isinstance(field, CharField):
                warnings.warn(
                    f"The field '{field_name}' is using the Django form 'CharField'. "
                    "Please use the 'CharField' from PRAS instead to ensure proper functionality.",
                    UserWarning,
                )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.session.query(self.User).filter_by(username=username).first():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.session.query(self.User).filter_by(email=email).first():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    
    def save(self):
        valid_fields = {field.name for field in self.User.__table__.columns}
        user_data = {key: value for key, value in self.cleaned_data.items() if key in valid_fields}

        if 'password' in user_data:
            user_data['password'] = make_password(user_data['password'])

        user = self.User(**user_data)
        self.session.add(user)
        self.session.commit()

        self.cleaned_data['user'] = user
        return user

