from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

def post_list(request):
    ##ab hier additions 20160421
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
                             #so far this keeps throwing errors... we need to fix it...
                             #publish_year=year,
                             #publish_month=month,
                             #publish_day=day# )
                             )
    #include the comments from the model we created earlier
    #list of active comments:
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        ##if the method is called with data, which means with POST, we submit the data contained in the
        ##request into the form
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
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
