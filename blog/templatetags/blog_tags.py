from django import template
from ..models import Post , Comment , User
from django.db.models import Count , Max
from markdown import markdown
from django.utils.safestring import mark_safe
import re


register = template.Library()

@register.simple_tag()
def total_posts():
    return Post.published.count()

@register.simple_tag()
def total_comments():
    return Comment.objects.filter(active=True).count()

@register.simple_tag(name='last')
def last_post_date():
    return Post.published.last().publish


@register.simple_tag
def most_popular_posts(count=2):
    return Post.published.annotate(comment_count=Count('comments')).order_by('-comment_count')[:count]


@register.inclusion_tag('partials/latest_posts.html')
def latest_posts(count=2):
    l_posts = Post.published.order_by('-publish')[:count]
    context = {
        'l_posts' : l_posts,
    }
    return context


@register.filter(name='markdown')
def to_markdown(text):
    return mark_safe(markdown(text))

@register.simple_tag(name='m_reading')
def most_reading_time():
    post = Post.published.order_by('-reading_time').first()
    return f'{post.title} reading time is : {post.reading_time}'

@register.simple_tag(name='l_reading')
def low_reading_time():
    post = Post.published.order_by('-reading_time').last()
    return f'{post.title} reading time is : {post.reading_time}'

@register.simple_tag(name = 'best_user')
def best_user():
    best_user = User.objects.annotate(count_post=Count('user_posts')).order_by('-count_post').first()
    return f'{best_user} count post is : {best_user.count_post}'



BAD_WORDS = ['کصکش', 'خارکصه', 'لاشی']
@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        return value

    censored_text = value

    for word in BAD_WORDS:
        pattern = re.compile(rf'\b{re.escape(word)}\b', flags=re.IGNORECASE)
        replacement = "*" * len(word)
        censored_text = pattern.sub(replacement, censored_text)

    return censored_text



