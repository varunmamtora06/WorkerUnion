from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('writereview',views.writereview,name='writereview'),
    path('showreview',views.showreview,name='showreview'),
    path('showblog',views.showblog,name='showblog'),
    path('writeblog',views.writeblog,name='writeblog'),
    path('blogs',views.blogs,name='blogs'),
    path('allReviews',views.allReviews,name='allReviews'),
    path('deleteReview/<int:pk>',views.deleteReview,name='deleteReview'),
    path('deleteBlog/<int:pk>',views.deleteBlog,name='deleteBlog'),
    path('editBlog/<int:pk>',views.editBlog,name='editBlog'),
    #REST-IMplementation
    path('blogList',views.blogList,name='blogList'),
    # path('userList',views.userList,name='userList'),

    # path('blogList',views.BlogCreateGeneric.as_view(),name='blogList'),

    path('api-auth-token', obtain_auth_token, name='api_auth_token'), 
    path('homeview',views.HelloView.as_view(),name='homeview'),

    path('BlogCreateGeneric',views.BlogCreateGeneric.as_view()),
    path('blogslistgeneric/<int:pk>',views.BlogsListGeneric.as_view()),

]
urlpatterns += [
    path('api-token-auth', views.CustomAuthToken.as_view())
]
urlpatterns += static(settings.STATIC_URL)

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)