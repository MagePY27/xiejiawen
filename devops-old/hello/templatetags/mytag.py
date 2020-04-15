from django import template

re = template.Library()

@re.filter()
def fn(x, y):
    return int(x) + int(y)
