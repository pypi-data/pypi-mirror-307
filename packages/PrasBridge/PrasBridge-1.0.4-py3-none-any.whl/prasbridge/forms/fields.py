from django import forms
from django.core.exceptions import ValidationError
from typing import Optional, Dict, List, Any, Callable
from django.core.validators import EmailValidator

class BaseFieldAttrs:
    """Type definitions for base field attributes."""
    required: bool = True
    disabled: bool = None
    classes: str = ''
    id: Optional[str] = None
    style: str = ''
    value: str = ''
    autocomplete: str = ''
    readonly: bool = None
    label: Optional[str] = None
    initial: Optional[Any] = None
    help_text: Optional[str] = None
    show_hidden_initial: bool = False
    label_suffix: Optional[str] = None
    localize: bool = None
    validators: List[Callable] = []
    data_attrs: Dict[str, Any] = {}
    aria_attrs: Dict[str, Any] = {}
    error: Dict[str, str] = {}

class PreparetingAttrs:
    """Base class for form fields."""

    base_attrs = [
        'required',
        'disabled',
        'classes',
        'id',
        'style',
        'value',
        'autocomplete',
        'readonly',
        'label',
        'initial',
        'help_text',
        'show_hidden_initial',
        'label_suffix',
        'localize',
        'type',
        'onchange',
        'onfocus',
        'onblur',
        'onclick',
    ]

    def _get_widget(self, widget: forms.Widget) -> forms.Widget:
        """Build widget attributes dict from instance attributes."""
        attrs: Dict[str, Any] = {'type': getattr(self, 'type', None)}
        for attr in self.base_attrs:
            value = getattr(self, attr, None)
            if value:
                if attr == 'classes':
                    attrs['class'] = value
                elif attr in ['required', 'disabled', 'readonly']:
                    if value:
                        attrs[attr] = attr
                else:

                    attrs[attr] = value

        self._add_data_attrs(attrs)
        self._add_aria_attrs(attrs)

        w = widget(attrs=attrs)
        w.attrs['type'] = self.type
        return w

    def _add_data_attrs(self, attrs: Dict[str, Any]) -> None:
        """Add data-* attributes."""
        for key, value in self.data_attrs.items():
            attrs[f'data-{key}'] = value

    def _add_aria_attrs(self, attrs: Dict[str, Any]) -> None:
        """Add aria-* attributes."""
        for key, value in self.aria_attrs.items():
            attrs[f'aria-{key}'] = value

    def _validate(self, value, validate):
        if self.disabled:
            return
        validate(value)


class CharField(forms.CharField, PreparetingAttrs):
    """CharField with additional attributes."""

    def __init__(self, 
                 *args, 
                 # field specific attributes
                 placeholder: Optional[str] = None, 
                 max_length: int = None, 
                 strip: bool = None,
                 empty_value: Optional[str] = None,
                 min_length: int = None, 
                 title: str = '', 
                 size: int = 0, 
                 # base field attributes
                 type: str = 'text', 
                 onclick: Optional[str] = None, 
                 onfocus: Optional[str] = None, 
                 onblur: Optional[str] = None, 
                 onchange: Optional[str] = None,  
                 required: bool = True,
                 disabled: bool = None,
                 classes: str = '',
                 id: Optional[str] = None,
                 style: str = '',
                 value: str = '',
                 autocomplete: str = '',
                 readonly: bool = False,
                 label: Optional[str] = None,
                 initial: Optional[Any] = None,
                 help_text: Optional[str] = None,
                 show_hidden_initial: bool = False,
                 label_suffix: Optional[str] = None,
                 localize: bool = False,
                 validators: List[Callable] = [],
                 data_attrs: Dict[str, Any] = {},
                 aria_attrs: Dict[str, Any] = {},
                 error: Dict[str, str] = {},
                 **kwargs):
        
        self.placeholder = placeholder
        self.max_length = max_length
        self.min_length = min_length
        self.title = title
        self.size = size
        self.strip = strip
        self.empty_value = empty_value


        self.onclick = onclick
        self.onfocus = onfocus
        self.onblur = onblur
        self.onchange = onchange
        self.type = type
        self.required = required
        self.disabled = disabled
        self.classes = classes
        self.id = id
        self.style = style
        self.value = value
        self.autocomplete = autocomplete
        self.readonly = readonly
        self.label = label
        self.initial = initial
        self.help_text = help_text
        self.show_hidden_initial = show_hidden_initial
        self.label_suffix = label_suffix
        self.localize = localize
        self.validators = validators or []
        self.data_attrs = data_attrs or {}
        self.aria_attrs = aria_attrs or {}


        self.error_messages = {
            'required': 'This field is required.',
            'invalid': 'Invalid input.'
        }
        if error:
            self.error_messages.update(error)
  

        widget_classes = {
            'text': forms.TextInput,
            'email': forms.EmailInput,
            'password': forms.PasswordInput,
        }

        widget_class = widget_classes.get(self.type)
        if widget_class is None:
            raise ValidationError(f"Invalid input type: {self.type}. Only 'text', 'email', or 'password' are allowed.")
        
        self.base_attrs.extend(['placeholder', 'max_length', 'min_length', 'title', 'size', 'onclick', 'onfocus', 'onblur', 'onchange', 'strip', 'empty_value'])

        self.widget = self._get_widget(widget=widget_class)

        direct_kwargs = {
            'max_length': self.max_length,
            'min_length': self.min_length,
            'strip': self.strip,
            'empty_value': self.empty_value,
            'required': self.required,
            'widget': self.widget,
            'label': self.label,
            'initial': self.initial,
            'help_text': self.help_text,
            'error_messages': self.error_messages,
            'show_hidden_initial': self.show_hidden_initial,
            'validators': self.validators,
            'localize': self.localize,
            'disabled': self.disabled,
            'label_suffix': self.label_suffix,
        }

        for attr in direct_kwargs:
            value = getattr(self, attr, None)
            if value is not None:
                kwargs[attr] = value
        
        super().__init__(*args, **kwargs)


    def clean(self, value):
        """Validate and clean the input field value."""
        value = super().clean(value)
        self._validate(value, super().validate)
        return value


class EmailField(CharField):
    """
    EmailField with email-specific validations.
    """
    def __init__(self, 
                 *args,
                 # field specific attributes
                 placeholder: Optional[str] = None, 
                 max_length: int = None, 
                 strip: bool = None,
                 empty_value: Optional[str] = None,
                 min_length: int = None, 
                 title: str = '', 
                 size: int = 0, 
                 # base field attributes
                 onclick: Optional[str] = None, 
                 onfocus: Optional[str] = None, 
                 onblur: Optional[str] = None, 
                 onchange: Optional[str] = None,  
                 required: bool = True,
                 disabled: bool = None,
                 classes: str = '',
                 id: Optional[str] = None,
                 style: str = '',
                 value: str = '',
                 autocomplete: str = '',
                 readonly: bool = False,
                 label: Optional[str] = None,
                 initial: Optional[Any] = None,
                 help_text: Optional[str] = None,
                 show_hidden_initial: bool = False,
                 label_suffix: Optional[str] = None,
                 localize: bool = False,
                 validators: List[Callable] = [],
                 data_attrs: Dict[str, Any] = {},
                 aria_attrs: Dict[str, Any] = {},
                 error: Dict[str, str] = {},
                 **kwargs):
        
        # Add EmailValidator to the validators list if not already included
        if EmailValidator not in validators:
            validators.append(EmailValidator())

        super().__init__(*args, type='email', classes=classes, id=id, 
                         placeholder=placeholder, 
                         max_length=max_length, 
                         min_length=min_length, 
                         autocomplete=autocomplete, 
                         required=required, 
                         readonly=readonly, 
                         disabled=disabled, 
                         data_attrs=data_attrs, 
                         aria_attrs=aria_attrs, 
                         style=style, 
                         title=title, 
                         size=size, 
                         value=value, 
                         onclick=onclick, 
                         onblur=onblur, 
                         onfocus=onfocus, 
                         onchange=onchange, 
                         error=error, 
                         label=label,
                         initial=initial,
                         help_text=help_text,
                         strip=strip,
                         empty_value=empty_value,
                         show_hidden_initial=show_hidden_initial,
                         label_suffix=label_suffix,
                         localize=localize,
                         validators=validators, 
                         **kwargs)


    def clean(self, value):
        """Validate the email field value, ensuring proper format and constraints."""
        value = super().clean(value)
        self._validate(value, super().validate)
        return value  
    

class TextAreaField(forms.CharField, PreparetingAttrs):
    """TextAreaField to allow setting various widget attributes directly."""

    def __init__(self, *args, 
                # field specific attributes
                placeholder: Optional[str] = None, 
                max_length: int = None, 
                strip: bool = None,
                empty_value: Optional[str] = None,
                min_length: int = None, 
                size: int = 0, 
                rows: int = None,
                cols: int = None,
                # base field attributes
                onclick: Optional[str] = None, 
                onfocus: Optional[str] = None, 
                onblur: Optional[str] = None, 
                onchange: Optional[str] = None, 
                required: bool = True,
                 disabled: bool = None,
                 classes: str = '',
                 id: Optional[str] = None,
                 style: str = '',
                 value: str = '',
                 autocomplete: str = '',
                 readonly: bool = False,
                 label: Optional[str] = None,
                 initial: Optional[Any] = None,
                 help_text: Optional[str] = None,
                 show_hidden_initial: bool = False,
                 label_suffix: Optional[str] = None,
                 localize: bool = False,
                 validators: List[Callable] = [],
                 data_attrs: Dict[str, Any] = {},
                 aria_attrs: Dict[str, Any] = {},
                 error: Dict[str, str] = {},
                 **kwargs):

        self.rows = rows
        self.cols = cols
        self.placeholder = placeholder
        self.max_length = max_length
        self.min_length = min_length
        self.size = size
        self.strip = strip
        self.empty_value = empty_value

        self.onclick = onclick
        self.onfocus = onfocus
        self.onblur = onblur
        self.onchange = onchange
        self.type = 'textarea'
        self.required = required
        self.disabled = disabled
        self.classes = classes
        self.id = id
        self.style = style
        self.value = value
        self.autocomplete = autocomplete
        self.readonly = readonly
        self.label = label
        self.initial = initial
        self.help_text = help_text
        self.show_hidden_initial = show_hidden_initial
        self.label_suffix = label_suffix
        self.localize = localize
        self.validators = validators or []
        self.data_attrs = data_attrs or {}
        self.aria_attrs = aria_attrs or {}
        

        self.error_messages = {
            'required': 'This field is required.',
            'invalid': 'Invalid input.'
        }
        if error:
            self.error_messages.update(error)
  
        # Prepare the widget with all the attributes
        widget_class = forms.Textarea

        self.base_attrs.extend(['rows', 'cols', 'placeholder', 'max_length', 'min_length', 'size', 'strip', 'empty_value'])

        self.widget = self._get_widget(widget=widget_class)

        direct_kwargs = {
            'max_length': self.max_length,
            'min_length': self.min_length,
            'strip': self.strip,
            'empty_value': self.empty_value,
            'required': self.required,
            'widget': self.widget,
            'label': self.label,
            'initial': self.initial,
            'help_text': self.help_text,
            'error_messages': self.error_messages,
            'show_hidden_initial': self.show_hidden_initial,
            'validators': self.validators,
            'localize': self.localize,
            'disabled': self.disabled,
            'label_suffix': self.label_suffix,
        }

        for attr in direct_kwargs:
            value = getattr(self, attr, None)
            if value is not None:
                kwargs[attr] = value

        # Call the parent constructor
        super().__init__(*args, **kwargs)


    def clean(self, value):
        """Validate the textarea value."""
        value = super().clean(value)
        self._validate(value, super().validate)
        return value


class ChoiceField(forms.ChoiceField, PreparetingAttrs):
    """ChoiceField to allow setting various widget attributes directly."""

    def __init__(self, *args, 
                # field specific attributes
                 choices: list = ..., 
                # base field attributes
                 onchange: Optional[str] = None,
                 onclick: Optional[str] = None, 
                 onfocus: Optional[str] = None, 
                 onblur: Optional[str] = None, 
                 required: bool = True,
                 disabled: bool = None,
                 classes: str = '',
                 id: Optional[str] = None,
                 style: str = '',
                 value: str = '',
                 autocomplete: str = '',
                 readonly: bool = False,
                 label: Optional[str] = None,
                 initial: Optional[Any] = None,
                 help_text: Optional[str] = None,
                 show_hidden_initial: bool = False,
                 label_suffix: Optional[str] = None,
                 localize: bool = False,
                 validators: List[Callable] = [],
                 data_attrs: Dict[str, Any] = {},
                 aria_attrs: Dict[str, Any] = {},
                 error: Dict[str, str] = {},            
                 **kwargs):
        

        self.choices = choices

        self.onchange = onchange
        self.onclick = onclick
        self.onfocus = onfocus
        self.onblur = onblur
        self.type = 'select'
        self.required = required
        self.disabled = disabled
        self.classes = classes
        self.id = id
        self.style = style
        self.value = value
        self.autocomplete = autocomplete
        self.readonly = readonly
        self.label = label
        self.initial = initial
        self.help_text = help_text
        self.show_hidden_initial = show_hidden_initial
        self.label_suffix = label_suffix
        self.localize = localize
        self.validators = validators or []
        self.data_attrs = data_attrs or {}
        self.aria_attrs = aria_attrs or {}

        self.error_messages = {
            'required': 'This field is required.',
            'invalid': 'Invalid input for the checkbox.'
        }
        
        if error:
            self.error_messages.update(error)

        # Create the Select widget with the attributes
        widget_class = forms.Select

        self.base_attrs.extend(['choices'])

        self.widget = self._get_widget(widget=widget_class)

        direct_kwargs = {
            'choices': self.choices,
            'required': self.required,
            'widget': self.widget,
            'label': self.label,
            'initial': self.initial,
            'help_text': self.help_text,
            'error_messages': self.error_messages,
            'show_hidden_initial': self.show_hidden_initial,
            'validators': self.validators,
            'localize': self.localize,
            'disabled': self.disabled,
            'label_suffix': self.label_suffix,
        }

        for attr in direct_kwargs:
            value = getattr(self, attr, None)
            if value is not None:
                kwargs[attr] = value

        # Call the parent constructor
        super().__init__(*args, **kwargs)

    def clean(self, value):
        """Validate the selected value."""
        value = super().clean(value)
        self._validate(value, super().validate)

        return value


class CheckBoxField(forms.BooleanField, PreparetingAttrs):
    """CheckBoxField (Checkbox) to allow setting various widget attributes directly."""


    def __init__(self, *args, 
                 checked: Optional[bool] = False, 
                 # base field attributes
                 onclick: Optional[str] = None, 
                 onfocus: Optional[str] = None, 
                 onblur: Optional[str] = None, 
                 onchange: Optional[str] = None,  
                 required: bool = True,
                 disabled: bool = None,
                 classes: str = '',
                 id: Optional[str] = None,
                 style: str = '',
                 value: str = '',
                 autocomplete: str = '',
                 readonly: bool = False,
                 label: Optional[str] = None,
                 initial: Optional[Any] = None,
                 help_text: Optional[str] = None,
                 show_hidden_initial: bool = False,
                 label_suffix: Optional[str] = None,
                 localize: bool = False,
                 validators: List[Callable] = [],
                 data_attrs: Dict[str, Any] = {},
                 aria_attrs: Dict[str, Any] = {},
                 error: Dict[str, str] = {}, 
                 **kwargs):
        
        self.checked = checked

        self.type = 'checkbox'
        self.onchange = onchange
        self.onclick = onclick
        self.onfocus = onfocus
        self.onblur = onblur
        self.required = required
        self.disabled = disabled
        self.classes = classes
        self.id = id
        self.style = style
        self.value = value
        self.autocomplete = autocomplete
        self.readonly = readonly
        self.label = label
        self.initial = initial
        self.help_text = help_text
        self.show_hidden_initial = show_hidden_initial
        self.label_suffix = label_suffix
        self.localize = localize
        self.validators = validators or []
        self.data_attrs = data_attrs or {}
        self.aria_attrs = aria_attrs or {}


        # Default error messages
        self.error_messages = {
            'required': 'This field is required.',
            'invalid': 'Invalid input for the checkbox.'
        }
        
        if error:
            self.error_messages.update(error)


        # Create Checkbox widget with the attributes
        widget = forms.CheckboxInput

        self.base_attrs.extend(['checked'])

        self.widget = self._get_widget(widget=widget)

        direct_kwargs = {
            'required': self.required,
            'widget': self.widget,
            'label': self.label,
            'initial': self.initial,
            'help_text': self.help_text,
            'error_messages': self.error_messages,
            'show_hidden_initial': self.show_hidden_initial,
            'validators': self.validators,
            'localize': self.localize,
            'disabled': self.disabled,
            'label_suffix': self.label_suffix,
        }

        for attr in direct_kwargs:
            value = getattr(self, attr, None)
            if value is not None:
                kwargs[attr] = value

        super().__init__(*args, **kwargs)


    def clean(self, value):
        value = super().clean(value)
        self._validate(value, super().validate)
        return value


class ErrorField(forms.Field):
    """A field that is used to store and display form-wide errors."""
    
    def __init__(self, *args, 
                 classes: str = '', 
                 id: str = '', 
                 style: str = '', 
                 **kwargs):
        self.classes = classes
        self.id = id
        self.style = style

        kwargs['required'] = False
        kwargs['widget'] = forms.HiddenInput(attrs={ 
            'class': self.classes,
            'id': self.id,
            'style': self.style,
        })

        super().__init__(*args, **kwargs)
    
    def add_error(self, error_message: str):
        """Add an error message to this field."""
        if not hasattr(self, 'custom_errors'):
            self.custom_errors = []
        self.custom_errors.append(error_message)

    def clean(self, value):
        """Return the stored error messages, or None."""
        return None  # No value for this field


class DateField(forms.DateField, PreparetingAttrs):
    """DateField to allow setting various widget attributes directly."""

    def __init__(self, *args,
                 input_formats: any = None,
                 # base field attributes
                 onclick: Optional[str] = None, 
                 onfocus: Optional[str] = None, 
                 onblur: Optional[str] = None, 
                 onchange: Optional[str] = None,  
                 required: bool = True,
                 disabled: bool = None,
                 classes: str = '',
                 id: Optional[str] = None,
                 style: str = '',
                 value: str = '',
                 autocomplete: str = '',
                 readonly: bool = False,
                 label: Optional[str] = None,
                 initial: Optional[Any] = None,
                 help_text: Optional[str] = None,
                 show_hidden_initial: bool = False,
                 label_suffix: Optional[str] = None,
                 localize: bool = False,
                 validators: List[Callable] = [],
                 data_attrs: Dict[str, Any] = {},
                 aria_attrs: Dict[str, Any] = {},
                 error: Dict[str, str] = {},
                 **kwargs):
        
        # Initialize fields with provided or default values
        self.input_formats = input_formats or ['%Y-%m-%d']

        self.type = 'date'
        self.onchange = onchange
        self.onclick = onclick
        self.onfocus = onfocus
        self.onblur = onblur
        self.required = required
        self.disabled = disabled
        self.classes = classes
        self.id = id
        self.style = style
        self.value = value
        self.autocomplete = autocomplete
        self.readonly = readonly
        self.label = label
        self.initial = initial
        self.help_text = help_text
        self.show_hidden_initial = show_hidden_initial
        self.label_suffix = label_suffix
        self.localize = localize
        self.validators = validators or []
        self.data_attrs = data_attrs or {}
        self.aria_attrs = aria_attrs or {}

        # Setup custom error messages
        self.error_messages = {
            'required': 'This field is required.',
            'invalid': 'Enter a valid date.'
        }
        if error:
            self.error_messages.update(error)

        # Prepare the DateInput widget with custom attributes
        widget = forms.DateInput

        self.widget = self._get_widget(widget=widget)

        # populate kwargs    
        direct_kwargs = {
            'input_formats': self.input_formats,
            'required': self.required,
            'widget': self.widget,
            'label': self.label,
            'initial': self.initial,
            'help_text': self.help_text,
            'error_messages': self.error_messages,
            'show_hidden_initial': self.show_hidden_initial,
            'validators': self.validators,
            'localize': self.localize,
            'disabled': self.disabled,
            'label_suffix': self.label_suffix,
        }

        for attr in direct_kwargs:
            value = getattr(self, attr, None)
            if value is not None:
                kwargs[attr] = value

        # Pass the remaining kwargs and initialize the parent class
        super().__init__(*args, **kwargs)

    def clean(self, value):
        """Validate the input field value."""
        value = super().clean(value)
        self._validate(value, super().validate)
        return value
        

class IntegerField(forms.IntegerField, PreparetingAttrs):
    """Custom IntegerField to allow setting various widget attributes directly."""

    def __init__(self, *args,
                 min_value: int =None,
                 max_value: int =None,
                 step: int = None,

                 # base field attributes
                 onclick: Optional[str] = None, 
                 onfocus: Optional[str] = None, 
                 onblur: Optional[str] = None, 
                 onchange: Optional[str] = None,  
                 required: bool = True,
                 disabled: bool = None,
                 classes: str = '',
                 id: Optional[str] = None,
                 style: str = '',
                 value: str | int = '',
                 autocomplete: str = '',
                 readonly: bool = False,
                 label: Optional[str] = None,
                 initial: Optional[Any] = None,
                 help_text: Optional[str] = None,
                 show_hidden_initial: bool = False,
                 label_suffix: Optional[str] = None,
                 localize: bool = False,
                 validators: List[Callable] = [],
                 data_attrs: Dict[str, Any] = {},
                 aria_attrs: Dict[str, Any] = {},
                 error: Dict[str, str] = {},
                 **kwargs):
        
        # Initialize fields with provided or default values
        self.min = min_value
        self.max = max_value
        self.step = step

        self.type = 'number'
        self.onchange = onchange
        self.onclick = onclick
        self.onfocus = onfocus
        self.onblur = onblur
        self.required = required
        self.disabled = disabled
        self.classes = classes
        self.id = id
        self.style = style
        self.value = value
        self.autocomplete = autocomplete
        self.readonly = readonly
        self.label = label
        self.initial = initial
        self.help_text = help_text
        self.show_hidden_initial = show_hidden_initial
        self.label_suffix = label_suffix
        self.localize = localize
        self.validators = validators or []
        self.data_attrs = data_attrs or {}
        self.aria_attrs = aria_attrs or {}


        # Setup custom error messages
        self.error_messages = {
            'required': 'This field is required.',
            'invalid': 'Enter a valid integer.',
            'min_value': f'The value must be greater than or equal to {min}.' if max is not None else '',
            'max_value': f'The value must be less than or equal to {max}.' if max is not None else ''
        }
        if error:
            self.error_messages.update(error)

        # Prepare the NumberInput widget with custom attributes
        widget_class = forms.NumberInput

        self.base_attrs.extend(['min', 'max', 'step', 'label'])

        self.widget = self._get_widget(widget=widget_class)
        
        # populate kwargs    
        direct_kwargs = {
            'min_value': self.min,
            'max_value': self.max,
            'required': self.required,
            'widget': self.widget,
            'label': self.label,
            'initial': self.initial,
            'help_text': self.help_text,
            'error_messages': self.error_messages,
            'show_hidden_initial': self.show_hidden_initial,
            'validators': self.validators,
            'localize': self.localize,
            'disabled': self.disabled,
            'label_suffix': self.label_suffix,
        }

        for attr in direct_kwargs:
            value = getattr(self, attr, None)
            if value is not None:
                kwargs[attr] = value
        
        super().__init__(*args, **kwargs)

    def clean(self, value):
        """Validate the input field value."""
        value = super().clean(value)
        self._validate(value, super().validate)
        return value
