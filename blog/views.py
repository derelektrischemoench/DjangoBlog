from __future__ import unicode_literals

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Post, Comment
from .forms import CommentForm


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # 3 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(page.num_pages)

    return render(request,
                  'blog/static/post/list.html',
                  {'page': page,
                   'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day
                             )

    #include the comments from the model we created earlier
    #queryset for filtering active comments:
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        ##if the method is called with data, which means with POST, we submit the data contained in the
        ##request into the form
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)##create instance but don't save it yet
            new_comment.post = post ##this links the form instance to the comment
            new_comment.save()##save the whole thing to the DB
        ##if the request is empty, aka an empty GET request, Django automatically supplies an empty form
    else:
        comment_form = CommentForm()

    return render(request,
                  'blog/static/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog/static/post/list.html'

