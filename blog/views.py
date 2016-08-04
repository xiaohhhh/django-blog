from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render
from django.template import loader
from .models import Entry
from .models import Author
from .models import Blog
from django import forms
from datetime import *
from django.http import HttpResponseRedirect


def index(request):
    if request.COOKIES.has_key("username"):
        print request.COOKIES['username']
    else:
        pass
    latest_entry_list = Entry.objects.all()
    template = loader.get_template('index.html')
    print latest_entry_list
    context = {
        'latest_entry_list': latest_entry_list,
    }
    return HttpResponse(template.render(context, request))


def entry(request,entry_id):
    entry = Entry.objects.get(id = entry_id)
    template = loader.get_template('entry.html')
    print type(entry)
    context = {
        'entry': entry,
    }
    return HttpResponse(template.render(context, request))

def post(request):
    class CommentForm(forms.Form):
        head_line = forms.CharField()
        body_text = forms.CharField(widget=forms.Textarea)

    print(vars(Entry))
    form_comment = CommentForm(initial={}, auto_id=False)
    print (form_comment)
    context = {'form_comment': form_comment.as_ul()}
    template = loader.get_template('post.html')
    return  HttpResponse(template.render(context, request))

def add_entry(request):
    print request.POST['head_line']
    now = datetime.now()
    entry=Entry(head_line=request.POST['head_line'],body_text=request.POST['body_text'],pub_date = now,
                mod_date = now,n_comments = 10,n_pingbacks = 10,rating = 10,)
    entry.save()
    context = {'form_comment': request.POST['head_line']}
    template = loader.get_template('add_entry.html')
    return HttpResponse(template.render(context, request))

def add_blog(request):
    blog=Blog(name = "hello",tagline = "hello")
    blog.save()

def register(request):
    class RegisterForm(forms.Form):
        username = forms.CharField()
        password = forms.CharField()

    print(vars(Entry))
    register_comment = RegisterForm(initial={}, auto_id=False)
    print (register_comment)
    context = {'register_comment': register_comment.as_ul()}
    template = loader.get_template('register.html')
    return  HttpResponse(template.render(context, request))

def add_user(request):
    user=Author(username=request.POST['username'],password=request.POST['password'])
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
    user=Author.objects.filter(username=request.POST['username'],password=request.POST['password'])
    print user
    response = HttpResponse()
    if(user):
        response.set_cookie('username', user)
    else:
        return HttpResponseRedirect("/login/")
    return HttpResponseRedirect("/blog/")

def logout(request):
    response = HttpResponse()
    response.delete_cookie('username')
    return HttpResponseRedirect("/blog/")

























