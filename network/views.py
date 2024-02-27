from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
import json
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User,Post,Profile
import datetime

class CreatePost(forms.ModelForm):
    class Meta:
        model=Post
        fields=['post_content','date']
        widgets = {'date': forms.HiddenInput()}


def index(request):
    all_post = Post.objects.all()[::-1]
    paginator = Paginator(all_post, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method=="POST":
        form=CreatePost(request.POST)
        if form.is_valid():
            post_content=form.cleaned_data['post_content']
            date=datetime.datetime.now()
            poster=request.user
            post=Post(poster=poster,post_content=post_content,date=date)
            post.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"network/index.html",{
                "post_form":form,
                'page_obj':page_obj
            })
    return render(request,"network/index.html",{
        "post_form":CreatePost(),
        'page_obj':page_obj
    }) 

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile=Profile(person=user)
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile_view(request,username):
    profile=User.objects.get(username=username)
    posts_by_this_user=Post.objects.filter(poster=profile)
    follower_following=Profile.objects.get(person=profile)
    is_follow=False
    if request.user in follower_following.follower.all():
        is_follow=True
    posts_by_this_user=posts_by_this_user[::-1]
    paginator = Paginator(posts_by_this_user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"network/profile.html", {
        "page_obj":page_obj,
        "profile":profile,
        "profile_stats":follower_following,
        "is_follow":is_follow
    })

@csrf_exempt
def follow_unfollow(request,username):
    profile=User.objects.get(username=username)
    user=User.objects.get(username=request.user)
    user_id=user.id
    if request.method=="POST":
        data = json.loads(request.body) # getting a fetch request from the following profile page, getting a state variable to follow or unfollow
        if data["to_follow"]==True:
            person=Profile.objects.get(person=profile)
            person.follower.add(user)
            person.save()
            user=Profile.objects.get(person=user_id)
            person=User.objects.get(username=profile)
            user.following.add(person)
            user.save()
            return HttpResponse(status=200)
        else:
            person=Profile.objects.get(person=profile)
            person.follower.remove(user)
            person.save()
            user=Profile.objects.get(person=user_id)
            person=User.objects.get(username=profile)
            user.following.remove(person)
            user.save()
            return HttpResponse(status=200)
    elif request.method=="GET":
        return HttpResponse(status=200)

@csrf_exempt #for testing
def like_unlike(request,id):
    post=Post.objects.get(pk=id)
    user=User.objects.get(username=request.user)
    if request.method=="POST":
        data = json.loads(request.body) # getting a fetch request from the following profile page, getting a state variable to follow or unfollow
        if int(data["like_status"])==1:
            post.likes.add(user)
            post.save()
            like_status="0"
            return JsonResponse({'like_status':like_status,'status':200})
        else:
            post.likes.remove(user)
            post.save()
            like_status="1"
            return JsonResponse({'like_status':like_status,'status':200})
    elif request.method=="GET":
        return JsonResponse({'like_status':like_status,'status':200})

@csrf_exempt
def edit(request,id):
    post=Post.objects.get(pk=id)
    user=User.objects.get(username=request.user)
    if request.method=="POST":
        data = json.loads(request.body)
        print(data['post_content'])
        edited_content=data['post_content']
        post.post_content=edited_content
        post.save()
        return JsonResponse({'status':200})


def following(request):
    user=User.objects.get(username=request.user)
    person=Profile.objects.get(person=user)
    people_following=person.following.all()
    all_posts=Post.objects.all()
    posts=[]
    for post in all_posts:
        for individual in people_following:
            if individual == post.poster:
                posts.append(post)
    posts=posts[::-1]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"network/following.html",{
        "page_obj":page_obj
    })

