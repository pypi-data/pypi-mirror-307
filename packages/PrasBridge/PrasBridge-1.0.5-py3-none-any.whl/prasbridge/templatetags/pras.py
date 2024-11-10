from django import template
from django.utils.safestring import mark_safe
from django.template import Template, Context
from .helper import __create_label, __create_error_html, __parse_boolean, __prepare_input_attributes, __create_input_html, __wrap_with_div

register = template.Library()

@register.simple_tag(takes_context=True)
def pInput(context, field_name, form=None, html=None, Class=None, style=None, 
            LabelClass=None, InputClass=None, ErrorClass=None, label=True, 
            error=True, placeholder=None, LabelText=None, defaultEv=True, 
            defaultValue=None, **kwargs):
    
    form = context.get('form', None) if not form else context.get(form, None)

    label = __parse_boolean(label, 'label')
    error = __parse_boolean(error, 'error')
    defaultEv = __parse_boolean(defaultEv, 'defaultEv')

    if not form or field_name not in form.fields:
        return mark_safe(f"<div>Error: No field named '{field_name}' found in the form.</div>")
    

    field = form[field_name]
    input_attrs = __prepare_input_attributes(field, placeholder, defaultValue)
    label_html = __create_label(field, LabelClass, LabelText, label, defaultEv, html)

    error_html = __create_error_html(field, ErrorClass, error, defaultEv)
    
    input_html, input_class = __create_input_html(field, input_attrs, InputClass, defaultEv, style)

    wrapper_style = "" if Class or not defaultEv else "margin-bottom: 15px;"
    wrapper = __wrap_with_div(label_html, input_html, error_html, input_attrs, Class, wrapper_style)

    return mark_safe(wrapper)



@register.simple_tag(takes_context=True)
def pForm(context, form, method='post', action=None, Class=None, FormClass=None, InputClass=None, id=None, ButtonLabel='Submit', LabelClass=None, ErrorClass=None, label=True, error=True, ButtonClass=None, defaultEv=True):
    if not form:
        return mark_safe("<div>Error: No form provided.</div>")
    
    csrf_token_template = Template('{% csrf_token %}')
    csrf_token_html = csrf_token_template.render(Context(context))

    form_html = f'<form id="{id}" method="{method}" action="{action}" class="{FormClass or ""}">'
    form_html += csrf_token_html


    for field_name in form.fields:
        field = form[field_name]
        field_html = pInput(context, field_name, Class=Class, InputClass=InputClass, LabelClass=LabelClass, ErrorClass=ErrorClass, label=label, error=error, defaultEv=defaultEv)
        form_html += field_html

    button_classes = ButtonClass or '' 
    button_style = "" if ButtonClass or not defaultEv else "width: 100%; background-color: #2563eb; color: white; font-weight: 600; padding: 0.5rem 0; border-radius: 0.375rem; transition: background-color 0.3s;" 
    button_hover = "" if ButtonClass or not defaultEv else (
        'onmouseover="this.style.backgroundColor=\'#1d4ed8\'" '
        'onmouseout="this.style.backgroundColor=\'#2563eb\'"'
    ) 
    form_html += f'<button {button_hover} style="{button_style}" type="submit" class="{button_classes}">{ButtonLabel}</button>'
    form_html += '</form>'

    return mark_safe(form_html)