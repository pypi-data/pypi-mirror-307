from warnings import warn, formatwarning
from django.utils.safestring import mark_safe
from ...error import pWarning

formatwarning = pWarning

def __parse_boolean(value, name):
    """Convert string representation of boolean to actual boolean."""
    if isinstance(value, str):
        if value.lower() in ["false", "0"]:
            return False
        elif value.lower() in ["true", "1"]:
            return True
        else:
            warn(f"{name} must be either 'false' or 'true' instead of {value}", UserWarning)
    return bool(value)

def __prepare_input_attributes(field, placeholder, defaultValue):
    """Prepare input attributes dictionary."""
    input_attrs = field.field.widget.attrs.copy()
    input_attrs['placeholder'] = placeholder if placeholder else input_attrs.get('placeholder', '')
    input_attrs['value'] = defaultValue if defaultValue else input_attrs.get('value', '')
    return input_attrs

def __create_label(field, LabelClass, LabelText, label, defaultEv, html):
    """Generate the HTML for the label."""
    if not label:
        return ""
    
    label_style = "" if LabelClass or not defaultEv else "font-weight: bold; margin-bottom: 5px; display: block; color: white" 
    label_classes = LabelClass or ""
    return f'<label for="{field.id_for_label}" class="{label_classes}" style="{label_style}">{(field.label if not LabelText else LabelText) if  not html else mark_safe(html)}</label>'

def __create_error_html(field, ErrorClass, error, defaultEv):
    """Generate the HTML for errors."""
    if not error or not field.errors:
        return ""

    error_style = "" if ErrorClass or not defaultEv else 'color: #e53e3e; font-size: 0.875rem; margin-top: 5px;'
    error_classes = ErrorClass or ""
    errors = ''.join([f'<p>{error}</p>' for error in field.errors])
    return f'<div style="{error_style}" class="{error_classes}">{errors}</div>'

def __create_input_html(field, input_attrs, InputClass, defaultEv, style):
    """Generate the HTML for the input field."""
    input_attrs_str = ' '.join([f'{key}="{value}"' for key, value in input_attrs.items()])
    input_type = input_attrs.get('type', 'text')
    input_class = InputClass if InputClass else input_attrs.get('class', '')
    input_attrs['class'] = input_class
    input_style = style if style else "" if InputClass or not defaultEv else ("padding: 10px; border-radius: 5px; border: 1px solid #ccc; width: 100%; box-sizing: border-box;" if input_type != "checkbox" else "width: 20px; height: 20px;")

    input_id = input_attrs.pop('id', field.id_for_label)
    input_value = input_attrs.get('value') or field.value() or ""

    if input_type == 'select':
        options_html = ''.join(
            [f"<option value='{val}' {'selected' if input_attrs['value'] == val else ''}>{label}</option>" 
             for val, label in field.field.choices]
        )
        return f"<select style='{input_style}' name='{field.name}' id='{input_id}' class='{input_class}' {input_attrs_str}>{options_html}</select>", input_class
    elif input_type == "textarea":
        return f'<textarea name="{field.name}" id="{field.id_for_label}" class="{input_class}" style="{input_style}" {input_attrs_str}>{input_value}</textarea>', input_class
    else:

        if input_type == "checkbox":
            return f'<input type="checkbox" name="{field.name}" id="{field.id_for_label}" onclick="this.value = this.checked ? \'True\' : \'False\';" style="{input_style}" class="{input_class}" {input_attrs_str} {"checked" if field.value() else ""} value="True" />', input_class
        else:
            return f'<input type="{input_type}" name="{field.name}" id="{field.id_for_label}" class="{input_class}" style="{input_style}" {input_attrs_str} value="{input_value}" />', input_class


def __wrap_with_div(label_html, input_html, error_html, input_attrs, Class, wrapper_style):
    """Wrap label, input, and error in a div."""
    if input_attrs.get('type') == "checkbox":
        return f'<div style="{wrapper_style}" class="{Class if Class else ''}"><div class="pras-checkbox-wrapper" style="display: flex; align-items: center; gap:10px;">{input_html}{label_html}</div>{error_html}</div>'
    return f'<div style="{wrapper_style}" class="{Class if Class else ""}">{label_html}{input_html}{error_html}</div>'
