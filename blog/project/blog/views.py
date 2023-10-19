from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator 
from .models import Post
from django.views.generic import ListView, DetailView
# def post_list(request):
#     post = Post.published.all()
#     # Pagination with 3 posts per page
#     paginator = Paginator(post, 3) # The def Name (Viwe Name) & objs Number in one page
#     page_number = request.GET.get("page")
#     posts = paginator.get_page(page_number) # 
#     return render(request, 'blog/post/list.html', {'posts': posts}) # posts the context of pagination

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
    





def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                            status=Post.Status.PUBLISHED,
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    return render(request,
                    'blog/post/detail.html',
                    {'post': post})