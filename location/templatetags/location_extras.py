from django import template
from weibousers.models import PROVINCE_CHOICES
register = template.Library()

@register.filter
def post_page_num(value, page_num=None):
	page_volume = (page_num-1)*20
	return value + page_volume

@register.simple_tag
def next_page_url(request):
    dict_ = request.GET.copy()
    page = int(request.GET.get('page', '1'))
    dict_['page'] = page + 1
    return dict_.urlencode()

@register.simple_tag
def prev_page_url(request):
    dict_ = request.GET.copy()
    page = int(request.GET.get('page', None))
    if page:
        dict_['page'] = page - 1
    return dict_.urlencode()

@register.filter
def get_province(value):
    return dict(PROVINCE_CHOICES).get(value)
