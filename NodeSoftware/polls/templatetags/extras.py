from django import template

register = template.Library()

def dict_access(dic, key):
    return dic[key]

register.filter('dict_access', dict_access)
