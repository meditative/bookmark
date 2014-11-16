from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
# Create your models here.
class Link(models.Model):
	url = models.URLField(unique = True)
	def __str__(self):
		return self.url

class LinkAdmin(admin.ModelAdmin):
	list_display = ('url',)

admin.site.register(Link, LinkAdmin)

class Bookmark(models.Model):
	title = models.CharField(max_length=200)
	user = models.ForeignKey(User)
	link = models.ForeignKey(Link)
	def __str__(self):
		return '%s, %s' % (self.user.username, self.link.url)

	def get_absolute_url(self):
		return self.link.url

class BookmarkAdmin(admin.ModelAdmin):
	list_display = ('title', 'user', 'link')
	ordering = ('title',)
	search_fields = ('title',)

admin.site.register(Bookmark, BookmarkAdmin)
		
class Tag(models.Model):
	name = models.CharField(max_length=64, unique = True)
	bookmarks = models.ManyToManyField(Bookmark)
	def __str__(self):
		return self.name

class TagAdmin(admin.ModelAdmin):
	list_display = ('name',)
admin.site.register(Tag, TagAdmin)

class SharedBookmark(models.Model):
	bookmark = models.ForeignKey(Bookmark, unique = True)
	date = models.DateTimeField(auto_now_add = True)
	votes = models.IntegerField(default = 1)
	users_voted = models.ManyToManyField(User)

	def __str__(self):
		return '%s %s '%(self.bookmark, self.votes)

class SharedBookmarkAdmin(admin.ModelAdmin):
	list_display = ('bookmark', 'date', 'votes', )
	pass
admin.site.register(SharedBookmark, SharedBookmarkAdmin)