from django import template

register = template.Library()


@register.filter
def addclass(field, css_class):
    """
    Add the given CSS class to the field and output the rendered field.
    """
    widget = field.field.widget
    if widget.attrs.get('class'):
        css_class = f'{widget.attrs["class"]} {css_class}'.strip()
    return field.as_widget(attrs={'class': css_class})
