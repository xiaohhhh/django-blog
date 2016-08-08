from django.contrib import admin
from .models import Entry
from .models import Category
from .models import Tag
from .models import Comment


# Register your models here.
admin.site.register(Entry)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)