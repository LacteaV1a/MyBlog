from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

class LatestPostFeed(Feed):
    title = 'Мой блог'
    link = '/blog/'
    description = 'Новая статья в моём блоге.'

    def items(self):
        return Post.published.all()[:5]
    
    def items_title(self, item):
        return item.title
    
    def item_description(self, item):
        return truncatewords(item.body, 30)