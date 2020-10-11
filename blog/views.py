from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm,LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.models import Group
# Create your views here.
def home(request):
    posts=Post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})
def about(request):
    return render(request,'blog/about.html')
def contact(request):
    return render(request,'blog/contact.html')
def dashboard(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        user=request.user
        full_name=user.get_full_name()
        grp=user.groups.all()
        return render(request,'blog/dashboard.html',{'posts':posts,'full_name':full_name,'groups':grp})
    else:
        return HttpResponseRedirect('/login')
def user_logout(request):
    # return render(request,'blog/user_logout.html')
    logout(request)
    return HttpResponseRedirect('/')
def user_signup(request):
    if request.method =="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,'WoW! Now you are the User/Author')
            user=form.save()
            group=Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form=SignUpForm()
    return render(request,'blog/signup.html',{'form':form})
def user_login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            form=LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upass=form.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'User has logged in Successfully !')
                    return HttpResponseRedirect('/dashboard')
        else:
            form=LoginForm()
        return render(request,'blog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard')

def add_post(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=PostForm(request.POST)
            if form.is_valid():
                title=form.cleaned_data['title']
                desc=form.cleaned_data['desc']
                mypost=Post(title=title,desc=desc)
                # if mypost is not None:
                #      messages.success(request,'User has added Post Successfully !')
                mypost.save()
                form=PostForm()
        else:
            form=PostForm()

        return render(request,'blog/addPost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login')

def edit_post(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            pos=Post.objects.get(pk=id)
            form=PostForm(request.POST,instance=pos)
            if form.is_valid():
                messages.success(request,'The Post is Editted Successfully !')
                form.save()
        else:
            pos=Post.objects.get(pk=id)
            form=PostForm(instance=pos)
        return render(request,'blog/editPost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login')

def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            pos=Post.objects.get(pk=id)
            pos.delete()
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseRedirect('/login')
