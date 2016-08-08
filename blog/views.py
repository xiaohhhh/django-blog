from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render
from django.template import loader
from .models import Entry
from .models import Comment
from .models import Category
from django import forms
from datetime import *
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import HTMLParser

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def index(request):
    if request.user.is_authenticated():
        # Do something for authenticated users.
        login=True
    else:
        # Do something for anonymous users.
        login = False
    latest_entry_list = Entry.objects.all()
    template = loader.get_template('index.html')
    #print latest_entry_list
    context = {
        'latest_entry_list': latest_entry_list,
        'login':login,
    }
    return HttpResponse(template.render(context, request))


def entry(request,entry_id):
    entry = Entry.objects.get(id = entry_id)
    template = loader.get_template('entry.html')
    html_parser = HTMLParser.HTMLParser()
    entry.body_text== html_parser.unescape(entry.body_text)
    print (entry)
    #print (entry.body_text)
    context = {
        'entry': entry
    }
    return HttpResponse(template.render(context, request))

@login_required
@csrf_exempt
def post(request):
    template = loader.get_template('post.html')
    return  HttpResponse(template.render(request))

@login_required
@csrf_exempt
def add_entry(request):
    html_parser = HTMLParser.HTMLParser()
    user_id=request.user.id
    now = datetime.now()
    body_text = request.POST['body_text']
    #print (body_text)
    txt = html_parser.unescape(body_text)
    #print(txt)
    entry=Entry(head_line=request.POST['head_line'],body_text=txt,pub_date = now,
                mod_date = now,n_comments = 0,n_pingbacks = 0,rating = 0,category_id=1,user_id=user_id)
    entry.save()
    context = {'form_comment': request.POST['head_line']}
    template = loader.get_template('add_entry.html')
    return HttpResponse(template.render(context, request))

@login_required
@csrf_exempt
def add_comment(request):
    html_parser = HTMLParser.HTMLParser()
    now = datetime.now()
    comments = request.POST['comments']
    user_id = request.user.id
    entry_id=request.POST['entry_id']
    print entry_id
    comments = html_parser.unescape(comments)
    comment=Comment(comments=comments,pub_date = now,mod_date = now,entry_id = entry_id,user_id = user_id)
    comment.save()
    return HttpResponseRedirect("/blog/")

def register(request):
    class RegisterForm(forms.Form):
        username = forms.CharField()
        password = forms.CharField()
        email = forms.CharField()

    print(vars(Entry))
    register_comment = RegisterForm(initial={}, auto_id=False)
    print (register_comment)
    context = {'register_comment': register_comment.as_ul()}
    template = loader.get_template('register.html')
    return  HttpResponse(template.render(context, request))

def add_user(request):
    user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
    user.save()
    return HttpResponseRedirect("/blog/")


def login(request):
    class RegisterForm(forms.Form):
        username = forms.CharField()
        password = forms.CharField()

    login_form = RegisterForm(initial={}, auto_id=False)
    print (login_form)
    context = {'login_form': login_form.as_ul()}
    template = loader.get_template('login.html')
    return  HttpResponse(template.render(context, request))

def is_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
            pass
    else:
        # Return an 'invalid login' error message.
        pass
    return HttpResponseRedirect("/blog/")

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/blog/")

























