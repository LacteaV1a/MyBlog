from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .form import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_list(request, tag_slug=None):
    object_list = Post.published.all() 
    tag = None
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) # по 3 статьи на страницу
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, возвращаем первую страницу.
        posts = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем общее количество страниц, возвращаем последнию.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, 
                            publish__month=month, publish__day=day)
    # Список активных кометариев для данной статьи
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # Пользователь отправил коментарий.
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Создаём коментарий, но пока не сохраняем в базе данных.
            new_comment = comment_form.save(commit=False)
            # Привязка комментария к текущей статье.
            new_comment.post = post
            # Сохраняем комментарий в базе данных.
            new_comment.save()  
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form})

def post_share(request, post_id):
    # Получение статьи по идентификатору
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Форма была отправлена на сохранение.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Все поля формы прошли валидацию
            cd = form.cleaned_data
            # ... Отправка электронной почты
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommeds you reading "\
                        {}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: \
                        {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'lostarkdima1@mail.ru', [cd['to']])
            sent = True
            return render(request, 'blog/post/share.html',
                        {'post': post, 'form': form, 'sent': sent})  
    else:
        form = EmailPostForm()
        return render(request, 'blog/post/share.html',
                        {'post': post, 'form': form, 'sent': sent})           
