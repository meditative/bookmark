from django.contrib.syndication.views import Feed
from bookmarks.models import Bookmark

class RecentBookmarks(Feed):
	title = 'Django Bookmarks | Recent Bookmarks'
	link = '/feeds/latest/'
	description = 'Recent bookmarks posted by Bookmarks'

	def items(self):
		return Bookmark.objects.order_by('-id')[:10]

	def item_title(self, item):
		return item.title


	def item_description(self, item):
		tags = item.tag_set.all()
		tags_list = []
		for tag in tags:
			tags_list.append(tag.name)
		return ' '.join(tags_list)
