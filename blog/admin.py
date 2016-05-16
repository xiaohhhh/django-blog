from django.contrib import admin
from .models import Entry
from .models import Author
from .models import Blog

# Register your models here.
admin.site.register(Blog)
admin.site.register(Author)
admin.site.register(Entry)
