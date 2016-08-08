from __future__ import unicode_literals

from django.db import models

class Entry(models.Model):
    user_id = models.IntegerField()
    category_id=models.IntegerField()
    head_line = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):              # __unicode__ on Python 2
        return self.head_line

class Tag(models.Model):
    name = models.CharField(max_length=100)
    info = models.TextField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    info = models.CharField(max_length=100)

    def __str__(self):              # __unicode__ on Python 2
        return self.username

class Comment(models.Model):
    comments = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    entry_id=models.IntegerField()
    user_id =models.IntegerField()
