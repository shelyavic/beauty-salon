from django import template
from main.utils import has_group

register = template.Library() 
register.filter('has_group', has_group)