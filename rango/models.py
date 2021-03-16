from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import CASCADE
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=126, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name_plural = 'Categories'


class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'page'


class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


class BootUser(models.Model):
    user = models.CharField(max_length=126, unique=True)
    password = models.CharField(max_length=126)
    email = models.EmailField()

    class Meta:
        db_table = 'Bool_User'
