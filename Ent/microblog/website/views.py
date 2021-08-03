import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import  render
from django.urls import reverse
from django.http import  JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import User,Post,Follow,Like

from django.core.paginator import Paginator

def index(request):
    return render(request, "website/index.html", {
        "user" : request.user
    })

def allposts(request,param):
    if param=='all':
        allposts = Post.objects.all()
        posts = allposts.order_by("-timestamp").all()
    elif param!='following' and User.objects.get(username=param):
        user=User.objects.get(username=param)
        posts = Post.objects.filter(user=user)
        posts = posts.order_by("-timestamp").all()
    elif param=='following':
        folobj = Follow.objects.filter(follower=request.user)
        following=[]
        for f in folobj:
            following.append(f.following.username)
        posts= Post.objects.none()
        for f in following:
            us=User.objects.get(username=f)
            posts1 = Post.objects.filter(user=us)
            posts = posts | posts1
            posts = posts.order_by("-timestamp").all()
    return JsonResponse({"postarray":[post.serialize() for post in posts],"user":request.user.username},safe=False)


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
            return render(request, "website/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "website/login.html")


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
            return render(request, "website/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "website/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "website/register.html")

@csrf_exempt
@login_required
def newpost(request):
    if request.method =='POST':
        user = request.user
        data = json.loads(request.body)
        text = data.get("text","")
        post = Post(user=user,text=text)
        post.save()
    elif request.method =='PUT':
        data = json.loads(request.body)
        text = data.get("text", "")
        iden = data.get("id", "")
        post = Post.objects.get(id=iden)
        post.text=text
        post.save()
    else:
        return JsonResponse({"error": "POST request required."}, status=400)
    
    return JsonResponse({"message": "Post successful."}, status=201)

@csrf_exempt
@login_required
def profile(request,user1):
    user=User.objects.get(username=user1)
    following = list(Follow.objects.filter(following=user))
    followers = list(Follow.objects.filter(follower=user))   
    posts = Post.objects.filter(user=user)
    visiter = request.user
    isfollowing=False
    if Follow.objects.filter(following=user,follower=visiter):
        isfollowing=True
    
    details={
        "following_count": len(following),
        "follower_count": len(followers),
        "posts": [post.serialize() for post in posts],
        "visiter" : visiter.username,
        "isfollowing" : isfollowing
    }
    return JsonResponse(details, safe=False)

@csrf_exempt
@login_required
def follow(request, target):
    targetuser=User.objects.get(username=target)

    if Follow.objects.filter(following=targetuser,follower=request.user):
        Follow.objects.filter(following=targetuser,follower=request.user).delete()
        f=False
    else:  
        newfollow= Follow(following=targetuser,follower=request.user)
        newfollow.save()
        f=True
    return JsonResponse({"message": "Successful","followed":f}, status=201)
    
@csrf_exempt
@login_required    
def like(request, postid):
    post = Post.objects.get(id=postid)
    likes=list(Like.objects.filter(post=post))
    num_likes=len(likes)
    if request.method=='PUT':
        if Like.objects.filter(likedby=request.user,post=post):
            Like.objects.filter(likedby=request.user,post=post).delete()
            l=False
        else:  
            newlike=Like(likedby=request.user,post=post)
            newlike.save()
            l=True
        
        likes=list(Like.objects.filter(post=post))
        num_likes=len(likes)
        return JsonResponse({"message": "Successful","liked":l,"likes" : num_likes}, status=201)
    
    elif request.method=='GET':
        l=False
        if Like.objects.filter(likedby=request.user,post=post):
            l=True
        return JsonResponse({"message": "likes returned","liked":l,"likes" : num_likes}, status=201)


