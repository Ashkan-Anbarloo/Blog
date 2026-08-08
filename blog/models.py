from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django_resized import ResizedImageField
import os
from django.template.defaultfilters import slugify
# Create your models here.

class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = Post.Status.PUBLISHED)

class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF' , 'Draft'
        PUBLISHED = 'PB' , 'Published'
        REJECTED = 'RJ' , 'Rejected'

    CATEGORY_CHOICES = (
        ('tk' , 'تکنولوژی'),
        ('pro' , 'برنامه نویس'),
        ('hosh' , 'هوش مصنوعی'),
        ('blak' , 'بلاکچین'),
    )

    author = models.ForeignKey(User , on_delete=models.CASCADE , related_name='user_posts')
    title = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(max_length=250)
    #date
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=2 , choices=Status.choices , default=Status.DRAFT)
    reading_time = models.PositiveBigIntegerField(default=0)
    category = models.CharField(max_length=20 , choices=CATEGORY_CHOICES , default='سایر')

    objects = models.Manager()
    published = PublishManager()
    
    class Meta:
        ordering = ['-publish',]
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.id])
    
    def save(self , *args , **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args , **kwargs)
    
class Ticket(models.Model):
    massage = models.TextField()
    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    subject = models.CharField(max_length=250)

    class Meta:
        pass

    def str(self):
        return self.name
    

class Comment(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name='comments')
    name = models.CharField(max_length=250)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created',]
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'{self.name} : {self.post.title}'
    

class Image(models.Model):
    def user_directory_path(instance, filename):
        try:
            username = instance.post.author.username
        except AttributeError:
            username = "anonymous"

        return os.path.join('post_images', username, filename)


    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name='images')
    # image_file = models.ImageField(upload_to='post_images/')
    image_file = ResizedImageField(upload_to=user_directory_path , size=[400,300] , quality=75 , crop=['middle' , 'center'])
    title = models.CharField(max_length=250 , null=True , blank=True)
    description = models.TextField(null=True , blank=True)
    created = models.DateTimeField(auto_now_add=True)    

    class Meta:
        ordering = ['-created',]
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        # return self.title if self.title else os.path.basename(self.image_file.name)
        if self.title : 
            return self.title
        if self.image_file:
            return os.path.basename(self.image_file.name)
        return "No Title/Image"


class Account(models.Model):
    user = models.OneToOneField(User , related_name='account' , on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True , null=True)
    bio = models.TextField(blank=True , null=True)
    photo = ResizedImageField(upload_to='account_image/',size=[300,300],quality=60,crop=['middle' , 'center'],blank=True , null=True)
    job = models.CharField(max_length=250 , blank=True , null=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        pass



        