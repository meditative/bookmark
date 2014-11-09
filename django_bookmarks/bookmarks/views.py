# Create your views here.
from django.http import HttpResponse, Http404
from django.template import Context
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from bookmarks.forms import *
from bookmarks.models import *
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

def main_page1(request):
	template = get_template('main_page.html')
	variables = Context({'user':request.user})
	output = template.render(variables)
	return HttpResponse(output)
	
def main_page(request):
	return render_to_response('main_page.html',RequestContext(request))
	
def user_page_1(request,username):
	try:
		user = User.objects.get(username = username)
		print username
	except:
		raise Http404('Requested User not found!')
	bookmarks = user.bookmark_set.all()
#	template = get_template('user_page.html')
	variables = RequestContext(request,{'username':username,'user':request.user,
	'bookmarks': bookmarks})
#	output = template.render(variables)
	return render_to_response('user_page.html', variables)

@login_required(login_url = '/login/')	
def user_page(request, username):
	user = get_object_or_404(User, username=username)
	bookmarks = user.bookmark_set.order_by('-id')
	variables = RequestContext(request,{'bookmarks':bookmarks,'username':username,
	'show_tags': True,
	'show_edit': username == request.user.username}, 
	)
	return render_to_response('user_page.html', variables)

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')
	
@csrf_protect	
def register_page(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],	email=form.cleaned_data['email'])
		return HttpResponseRedirect('/')
	else:
		form = RegistrationForm()
		variables = RequestContext(request, {'form': form})
		return render_to_response('registration/register.html', variables)

def _bookmark_save(request, form):
	link,dummy = Link.objects.get_or_create(url=form.cleaned_data['url'])
	bookmark, created = Bookmark.objects.get_or_create(
	user=request.user,
	link=link)
	bookmark.title = form.cleaned_data['title']
	if not created:
		bookmark.tag_set.clear()
	tag_names = form.cleaned_data['tags'].split()
	for tag_name in tag_names:
		tag, dummy = Tag.objects.get_or_create(name=tag_name)
		bookmark.tag_set.add(tag)
	bookmark.save()
	return bookmark

@login_required(login_url = '/login/')
@csrf_protect
def bookmark_save_page(request):
	ajax = request.GET.has_key('ajax')
	if request.method =='POST':
		form = BookmarkSaveForm(request.POST)
		if form.is_valid():
			bookmark = _bookmark_save(request, form)
			if ajax:
				variables = RequestContext(request, {'bookmarks': [bookmark],
					'show_tags': True,
					'show_edit': True})
				return render_to_response('bookmark_list.html', variables)
			else:
				return HttpResponseRedirect('/user/%s/' % request.user.username)
		else:
			if ajax:
				return HttpResponse('failure')
	elif request.GET.has_key('url'):
		url = request.GET['url']
		title = ''
		tags = ''
		try:
			link = Link.objects.get(url = url)
			bookmark = Bookmark.objects.get(user = request.user, link = link)
			title = bookmark.title
			tags = ' '.join(tag.name for tag in bookmark.tag_set.all())
		except ObjectDoesNotExist:
			pass
		form = BookmarkSaveForm({'url':url, 'title': title, 'tags': tags})
	else:
		form = BookmarkSaveForm()
	variables = RequestContext(request, {'form': form})
	if ajax:
		return render_to_response('bookmark_save_form.html', variables)
	else:
		return render_to_response('bookmark_save.html', variables)

def tag_page(request, tag_name):
	tag = get_object_or_404(Tag, name = tag_name)
	bookmarks = tag.bookmarks.order_by('-id')
	variables = RequestContext(request, {
		'bookmarks': bookmarks,
		'tag_name': tag_name,
		'show_tags': True,
		'show_user': True,
		})
	return render_to_response('tag_page.html', variables)

def tag_cloud_page(request):
	MAX_WEIGHT = 5
	tags = Tag.objects.order_by('name')
	min_count = max_count = tags[0].bookmarks.count()
	for tag in tags:
		tag.count = tag.bookmarks.count()
		if tag.count < min_count:
			min_count = tag.count
	if max_count < tag.count:
		max_count = tag.count
	range =float(max_count - min_count)
	if range == 0.0:
		range = 1
	for tag in tags:
		tag.weight = int(MAX_WEIGHT*(tag.count - min_count)/range)
	variables = RequestContext(request, {'tags': tags})
	return render_to_response('tag_cloud_page.html', variables)

def search_page(request):
	form = SearchForm()
	bookmarks = []
	show_results = False
	if request.GET.has_key('query'):
		query = request.GET['query'].strip()
		show_results = True
		if query:
			form = SearchForm({'query': query})
			bookmarks = Bookmark.objects.filter(title__icontains=query)[:10]
	variables = RequestContext(request, {'form': form,
		'bookmarks': bookmarks,
		'show_results': show_results,
		'show_tags': True,
		'show_user': True})
	if request.GET.has_key('ajax'):
		return render_to_response('bookmark_list.html', variables)
	else:
		return render_to_response('search.html', variables)

def ajax_tag_autocomplete(request):
	if request.GET.has_key('q'):
		tags = Tag.objects.filter(name__istartswith = request.GET['q'])[:10]
		return HttpResponse('\n'.join(tag.name for tag in tags))
	return HttpResponse()