from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

"""
هنا هستخدم ال PublishManager دي فلتر بس بيبقى احسن واسرع بتتم من خلال الداتا بيز وبيكون التعديل عليها اسهل وافضل
لو عملت filter من ال Views هيديني نفس النتيجه بس بال manager بيكون اسرع وافضل
"""
class PublishedManager(models.Manager): # هنا بعمل model لل Status Published
    def get_queryset(self): # دي ميثود علشان ارجع ال ص وتحت استخدمت super() علشان اقدر اورث من ال queryset
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED) # هنا بفلتر ال Status علشان اجيب ال Published بس

### Post Model ###
class Post(models.Model): # The Model of Blog
    class Status(models.TextChoices): # Choice Field Variable
        DRAFT = 'DF', 'Draft' # text choice 'DF'= values 'Draft'= label
        PUBLISHED = 'PB', 'Published' # text choice
    title = models.CharField(max_length=250) # The Title of Blog
    slug = models.SlugField(max_length=250, unique_for_date='publish') # Slug Field to customize URL in View.py and unique_for to be unique slug
    body = models.TextField() # Content
    publish = models.DateTimeField(default=timezone.now) # Publish Time
    created = models.DateTimeField(auto_now_add=True) # Create Time
    updated = models.DateTimeField(auto_now=True) # Last Update Time
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT) # Choice Field 
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name='blog_posts') # Choice Field Linked With user with ForeignKey
    objects = models.Manager() # The default manager.
    published = PublishedManager() # The custom Manager
    class Meta:
        ordering = ['-publish'] # To Sort Data From Publish Time
        indexes = [
    models.Index(fields=['-publish']), # To improve searches with this field
    ]
        def __str__(self):
            return self.title
    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.publish.year, self.publish.month, self.publish.day,self.slug])
    
### Comments Model ###
class Comment(models.Model):
    post = models.ForeignKey(Post,
    on_delete=models.CASCADE,
    related_name='comments') # The Relation attribute name, post.comments.all() to call the comments of post
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['created']
        indexes = [
        models.Index(fields=['created']),
        ]
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

"""
In Django, all fields are searched, but by placing one field, “Public,” only it is searched for,
and this speeds up the search process in queries.
https://docs.djangoproject.com/en/4.1/ref/models/indexes/
"""
