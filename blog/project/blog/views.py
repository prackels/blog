from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator 
from .models import Post, Comment
from django.views.generic import ListView, DetailView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
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
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'form': form})
    
    
    
    
def post_share(request, post_id):
    # Retrieve the post by its identifier
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        # The form was submitted
        form = EmailPostForm(request.POST)

        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, 'prackels@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})



@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None # Empty value to store data
    # A comment was posted
    form = CommentForm(data=request.POST) # call form
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False) # the model instance is created but not saved tothe database. This allows us to modify the object before finally saving it
        # Assign the post to the comment
        comment.post = post #  We assign the post to the comment we created
        # Save the comment to the database
        comment.save() # finally save
    return render(request, 'blog/post/comment.html', {'post': post, 'form': form, 'comment': comment})