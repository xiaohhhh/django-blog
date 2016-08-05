import commands
import os
print (os.chdir("/Users/fendouai/Documents/github/django-blog/"))
print (commands.getstatusoutput("python manage.py runserver"))