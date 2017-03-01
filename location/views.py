from django.http import HttpResponse
from .models import Place, Post, PostFilter
from weibousers.models import WeiboUser
from .forms import CategorisePostForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse
from django.db import connection
from django.db.models import Count
from categories.models import Category

import json

def index(request):
	cx = {}
	statistics = []
	places = Place.objects.all()
	posts = Post.objects.count()
	uncategorised_posts = Post.objects.filter(category=None).count()
	users = WeiboUser.objects.count()
	# truncate_date = connection.ops.date_trunc_sql('month', 'created')
	# qs = Post.objects.filter(place=1).extra({'month':truncate_date})
	# report = qs.values('month').annotate(Count('pk')).order_by('month')
	cx['places'] = places.count()
	cx['posts'] = posts
	cx['uncategorised_posts'] = uncategorised_posts
	cx['users'] = users
	return render(request, "index.html", cx)


@user_passes_test(lambda u:u.is_staff, login_url='/admin/')
def place_index(request, place_id, page_num=None):
	page_num = int(request.GET.get('page', '1'))
	cx = {}
	place = Place.objects.get(id=place_id)
	cx['place'] = place
	uncategorised_posts = Post.objects.filter(place=place, category=None)
	cx['total_posts'] = uncategorised_posts.count()
	cx['page_num'] = page_num
	limit_from = 0 if page_num==1 else (page_num-1)*20
	limit_to = page_num*20
	posts = uncategorised_posts.order_by('-created')[limit_from:limit_to]
	main_dict = []
	for post in posts:
		post_dict =  {
			'post': post,
			'form': CategorisePostForm(request.POST or None, instance=post)
		}
		main_dict.append(post_dict)
	cx['main_dict'] = main_dict
	return render(request, "location/place_index.html", cx)


@user_passes_test(lambda u:u.is_staff, login_url='/admin/')
def categorise_post(request, place_id, post_id=None):
	place = Place.objects.get(id=place_id)
	if post_id:
		obj = get_object_or_404(Post, pk=post_id)
	form = CategorisePostForm(request.POST or None, instance=obj)
	if request.is_ajax():
		if form.is_valid():
			form = form.save(commit=False)
			form.category_id = int(request.POST['category']) if request.POST['category'] else None
			form.second_category_id = int(request.POST['second_category']) if request.POST['second_category'] else None
			form.third_category_id = int(request.POST['third_category']) if request.POST['third_category'] else None
			form.save()
        # do stuff, e.g. calculate a score
			dict = {
				'icon': 'ti-thumb-up', 
				'type': 'success',
				'message': 'Updated successfully.'
			}
		return HttpResponse(json.dumps(dict), content_type='application/json')
	return render(request, 'location/categorise_post_form.html', 
			{'form': form, 'obj': obj})


@user_passes_test(lambda u:u.is_staff, login_url='/admin')
class CategorisePostView(UpdateView):
    # form_class = CategorisePostForm
    model = Post
    fields = ('place', 'sub_place', 'user', 'created', 'text', 'weibo_img', 'category',
    		'second_category', 'third_category')
    template_name_suffix = '_update_form'


def post_list(request, page_num=None):
	f = PostFilter(request.GET, queryset=Post.objects.all())
	filtered = False
	total_count = ''
	r_place = request.GET.get('place', None)
	r_sub_place = request.GET.get('sub_place', None)
	r_category= request.GET.get('category', None)
	r_second_category= request.GET.get('second_category', None)
	r_third_category= request.GET.get('third_category', None)
	r_created_0 = request.GET.get('created_0', None)
	r_created_1 = request.GET.get('created_1', None)
	page_num = int(request.GET.get('page', '1'))
	form = f.form
	if r_place or r_category or r_created_0 or r_created_1:
		filtered = True
		total_count = f.count()
		limit_from = 0 if page_num==1 else (page_num-1)*20
		limit_to = page_num*20
		f = f[limit_from:limit_to]
		for item in f:
			item.category_form = CategorisePostForm(request.POST or None, instance=item)
	return render(request, 'location/list.html', {'filter': f, 
		'filtered': filtered, 'form': form, 'total_count': total_count,
		'page_num': page_num})

def analytics(request):
	cx = {}
	statistics = []
	ct_statistics = []
	users_statistics = []
	hunan_statistics = []
	# date_statistics = []
	# total_date_statistics = []
	# weekday_statictics = []
	# hour_statictics = []
	places = Place.objects.all()
	posts = Post.objects.count()
	uncategorised_posts = Post.objects.filter(category=None).count()
	categorised_posts = Post.objects.filter(category__isnull=False).count()
	users = WeiboUser.objects.count()
	f_users = WeiboUser.objects.filter(gender='F').count()
	m_users = WeiboUser.objects.filter(gender='M').count()
	# truncate_date = connection.ops.date_trunc_sql('month', 'created')
	# qs = Post.objects.filter(place=1).extra({'month':truncate_date})
	# report = qs.values('month').annotate(Count('pk')).order_by('month')
	cx['places'] = places.count()
	cx['posts'] = posts
	cx['uncategorised_posts'] = uncategorised_posts
	cx['users'] = users
	cx['f_users'] = f_users
	cx['m_users'] = m_users
	for place in places:
		posts = Post.objects.filter(place=place)
		not_categorised_posts = posts.filter(category=None)
		truncate_date = connection.ops.date_trunc_sql('month', 'created')
		qs = posts.extra({'month':truncate_date})
		report = qs.values('month').annotate(Count('pk')).order_by('month')
		statistics.append({
			'place': place,
			'count': posts.count(),
			'not_categorised_count': not_categorised_posts.count(),
			'report': report
		})
		cx['statistics'] = statistics
	for category in Category.objects.filter(active=True):
		count = Post.objects.filter(category=category).count()
		if count == 0:
			percentage = 0
		else:
			percentage = float(count*100/categorised_posts)
		ct_statistics.append({
			'category': category,
			'count': count,
			'percentage': percentage
		})
		cx['ct_statistics'] = ct_statistics
	cx['users_statistics'] = WeiboUser.objects.values("province")\
							.annotate(count=Count('province'))\
							.order_by('-count')
	cx['hunan_statistics'] = WeiboUser.objects.filter(province=43)\
							.values("city", "location")\
							.annotate(count=Count('city'))\
							.order_by('-count')
	# cx['date_statistics'] = Post.objects.extra({'created': "date(created)"})\
	# 							.values("place__name", "created")\
	# 							.annotate(count=Count("created"))\
	# 							.order_by('-count')[:50]
	# cx['total_date_statistics'] = Post.objects.extra({'created': "date(created)"})\
	# 								.values("created")\
	# 								.annotate(count=Count("created"))\
	# 								.order_by('-count')[:50]
	# cx['weekday_statictics'] = Post.objects.extra({'created': "weekday(created)"})\
	# 								.values("created")\
	# 								.annotate(count=Count("created"))\
	# 								.order_by('created')
	# cx['hour_statictics'] = Post.objects.extra({'created': "hour(created)"})\
	# 								.values("created")\
	# 								.annotate(count=Count("created"))\
	# 								.order_by('created')
	return render(request, "location/analytics.html", cx)