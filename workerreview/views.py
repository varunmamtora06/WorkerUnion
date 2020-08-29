from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth, User
#for some weird reason vscode shows error for above eventhoght issa correct
#so to avoid that you could write from django.contrib.auth import models and..
#for the bottom code implementation you have to write models.User instead of just writing User


# from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import review, blog
# you can write from . import forms and then inside all functions forms=forms.CreateBlogForm()
from .forms import *

#for rest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BlogSerializer,UserSerializer,LoginSerializer,RegisterSerializer
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
# from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request, "index.html")


def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                print('Usernme exists')
                messages.info(request, 'Username exists')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                print('email exists')
                messages.info(request, 'Email exists')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password1, first_name=fname, last_name=lname)
                user.save()
                return redirect('login')
        else:
            print('pass dosent match')
            messages.info(request, 'Password didn\'t match')
            return redirect('register')
        return redirect('/')
    else:
        return render(request, "register.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid details')
            return redirect('login')
    else:
        return render(request, "login.html")
    return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect('/')

# @login_required
def writereview(request):
    if request.method == 'POST':
        company = request.POST['companyName']
        currentStat = request.POST['currStat']
        jobtitle = request.POST['jobTit']
        reviewHeadline = request.POST['reviewTopic']
        pros = request.POST['pros']
        cons = request.POST['cons']
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        companyreview = review(company=company, currentStat=currentStat, jobtitle=jobtitle,
                               reviewHeadline=reviewHeadline, pros=pros, cons=cons, person=user)
        companyreview.save()
        return redirect('allReviews')
    else:
        return render(request, 'writereview.html')
    return render(request, 'writereview.html')


# showreview is to show the My blogs i.e. reviews written by user himself
# @login_required
def showreview(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)

    try:
        # print(review)
        reviews = review.objects.filter(person_id=user_id)
        return render(request, 'showreview.html', {'reviews': reviews})
    except Exception:
        return render(request, 'showreview.html', {'reviews': None})


def allReviews(request):
    reviews = review.objects.all()
    return render(request, 'allReviews.html', {'reviews': reviews})


def writeblog(request):
    if request.method == 'POST':
        form = CreateBlogForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            form = CreateBlogForm()  # wrote this line cuz after submit we should clear form fields
            # wrote this blog fetching query here bcuz we are rendering the blogs page and after submitting new blog user
            blogs = blog.objects.all()
            # is redirected to blog page with the newly created blog and he should be able to see all the blogs
            return redirect('blogs')
    else:
        form = CreateBlogForm()
        return render(request, 'writeblog.html', {'form': form})


# showblog is to show the My blogs i.e. blogs written by user himself
def showblog(request):
    user_id = request.user.id

    try:
        # print(blog)
        blogs = blog.objects.filter(owner_id=user_id)
        return render(request, 'showblog.html', {'blogs': blogs})
    except Exception:
        return render(request, 'showblog.html', {'blogs': None})
    return render(request, 'showblog.html')


def blogs(request):
    blogs = blog.objects.all()
    # you  just had to put '-' sign b4 'day' to sort it in ulta order lol spent almost 1.5hrs figuring out
    return render(request, 'blogs.html', {'blogs': blogs.order_by('-day')})



def deleteReview(request, pk):
    selectedReview = review.objects.get(id=pk)
    selectedReview.delete()
    return redirect('showreview')


def deleteBlog(request, pk):
    selectedBlog = blog.objects.get(id=pk)
    # print(selectedBlog.title)
    selectedBlog.delete()
    return redirect('showblog')


def editBlog(request, pk):
    selectedBlog = blog.objects.get(id=pk)
    form =  CreateBlogForm(instance = selectedBlog)
    if request.method == 'POST':
        form =  CreateBlogForm(request.POST, request.FILES, instance = selectedBlog)
        if form.is_valid():
            ins = form.save(commit=False)
            ins.owner = request.user
            ins.save()
            
            # is redirected to blog page with the newly created blog and he should be able to see all the blogs
            return redirect('blogs')

    else:
        form = CreateBlogForm(instance = selectedBlog)
    return render(request, 'writeblog.html', {'form': form})



#REST-implementation

@api_view(['GET'])
def blogList(request):
    blogs = blog.objects.all()
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def userList(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)




# class HelloView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)
    

# from rest_framework.authtoken.views import ObtainAuthToken

# class CustomAuthToken(ObtainAuthToken):

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         print(serializer)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'username':user.username,
#             'email': user.email
#         })


from rest_framework import generics
#to get all list of blogs and create a blog
class BlogCreateGeneric(generics.ListCreateAPIView):
    queryset = blog.objects.all()
    serializer_class = BlogSerializer


#to get a particular blog and update(put) it and delete it
class BlogsListGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = blog.objects.all()
    serializer_class = BlogSerializer


# class CreateUserApi(APIView):

#     def post(self,request):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)

# from django.contrib.auth import login, logout
from rest_framework.authentication import TokenAuthentication

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        auth.login(request,user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        }, status=200)




class LogOutView(APIView):
    authentication_classes=(TokenAuthentication,)

    def post(self,request):
        auth.logout(request)
        return Response(status=204)
    
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user.save()
        return Response({
            'mssg': " registered",
        }, status=200)