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
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



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
    '''
    username=request.POST['username']
    print username
    password=request.POST['password']
    print password
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            #login(request, user)
            return HttpResponseRedirect("/blog/")
            #print("User is valid, active and authenticated")
        else:
            print("The password is valid, but the account has been disabled!")
    else:
        # the authentication system was unable to verify the username and password
        print("The username and password were incorrect.")
    return HttpResponseRedirect("/blog/")
    '''
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

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/blog/")

























