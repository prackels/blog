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
    

"""
In Django, all fields are searched, but by placing one field, “Public,” only it is searched for,
and this speeds up the search process in queries.
https://docs.djangoproject.com/en/4.1/ref/models/indexes/
"""
