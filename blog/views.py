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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def login_flag(request):
    if request.user.is_authenticated():
        login_flag=True
    else:
        login_flag = False
    return login_flag

def index(request):
    login=login_flag(request)
    entry_list = Entry.objects.all()
    paginator = Paginator(entry_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        entries = paginator.page(paginator.num_pages)
    context = {
        'latest_entry_list': entries,
        'login':login,
    }
    template = loader.get_template('page.html')
    return HttpResponse(template.render(context, request))

def page(request):
    login = login_flag(request)
    entry_list = Entry.objects.all()
    paginator = Paginator(entry_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        entries = paginator.page(paginator.num_pages)
    context = {
        'latest_entry_list': entries,
        'login':login,
    }
    template = loader.get_template('page.html')
    return HttpResponse(template.render(context, request))


def entry(request,entry_id):
    login = login_flag(request)
    entry = Entry.objects.get(id = entry_id)
    user_id=entry.user_id
    category_id=entry.category_id
    print category_id
    category=Category.objects.get(id = category_id)
    user = User.objects.get(id=user_id)
    comments=Comment.objects.filter(entry_id=entry_id)
    template = loader.get_template('entry.html')
    html_parser = HTMLParser.HTMLParser()
    entry.body_text== html_parser.unescape(entry.body_text)
    #print (entry)
    #print (entry.body_text)
    context = {
        'entry': entry,
        'comments':comments,
        'username':user.username,
        'category':category,
        'login': login
    }
    return HttpResponse(template.render(context, request))

@login_required
@csrf_exempt
def post(request):
    login = login_flag(request)
    category_list = Category.objects.all()
    context = {
        'category_list': category_list,
        'login':login
    }
    template = loader.get_template('post.html')
    return HttpResponse(template.render(context, request))

@login_required
@csrf_exempt
def add_entry(request):
    login = login_flag(request)
    html_parser = HTMLParser.HTMLParser()
    user_id=request.user.id
    now = datetime.now()
    body_text = request.POST['body_text']
    category_id=request.POST['category_id']
    txt = html_parser.unescape(body_text)
    #print(txt)
    entry=Entry(head_line=request.POST['head_line'],body_text=txt,pub_date = now,
                mod_date = now,n_comments = 0,n_pingbacks = 0,rating = 0,category_id=category_id,user_id=user_id)
    entry.save()
    entry_last=Entry.objects.filter(user_id=user_id).last()
    return HttpResponseRedirect("/blog/entry/" + str(entry_last.id) + "/")

@login_required
@csrf_exempt
def add_comment(request):
    login = login_flag(request)
    html_parser = HTMLParser.HTMLParser()
    now = datetime.now()
    comments = request.POST['comments']
    user_id = request.user.id
    entry_id=request.POST['entry_id']
    print entry_id
    comments = html_parser.unescape(comments)
    comment=Comment(comments=comments,pub_date = now,mod_date = now,entry_id = entry_id,user_id = user_id)
    comment.save()
    comment_last = Comment.objects.filter(user_id=user_id,entry_id = entry_id).last()
    print comment_last.id
    return HttpResponse(comment_last.comments)



@login_required
@csrf_exempt
def add_category(request):
    name = request.POST['name']
    info=request.POST['info']
    category=Category(name=name,info = info)
    category.save()
    category_last = Category.objects.all().last()
    print category_last.id
    return HttpResponse(category_last.id)


def register(request):
    login = login_flag(request)
    class RegisterForm(forms.Form):
        username = forms.CharField()
        password = forms.CharField(widget=forms.PasswordInput())
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
    login = login_flag(request)
    class RegisterForm(forms.Form):
        username = forms.CharField()
        password = forms.CharField(widget=forms.PasswordInput())

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


def category(request,category_id):
    login = login_flag(request)
    entries = Entry.objects.filter(category_id = category_id)
    category = Category.objects.get(id = category_id)
    print category.id
    context = {
        'entries': entries,
        'login':login,
        'category':category,
    }
    template = loader.get_template('category.html')
    return HttpResponse(template.render(context, request))

def categories(request,category_id):
    class CategoryForm(forms.Form):
        name = forms.CharField()
        info = forms.CharField()

    category_form = CategoryForm(initial={}, auto_id=False)
    categories_list = Category.objects.all()
    paginator = Paginator(categories_list, 10) # Show 25 contacts per page
    categories_id = request.GET.get('categories_id')
    try:
        categories = paginator.page(categories_id)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        categories = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        categories = paginator.page(paginator.num_pages)
    context = {
        'categories_list': categories,
        'login':login,
        'category_form':category_form.as_ul(),
    }
    template = loader.get_template('categories.html')
    return HttpResponse(template.render(context, request))












