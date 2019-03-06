from django.urls import path
from . import views
from django.conf.urls import url
from .views import LinkListView,ProfileView,LinkCreateView,LinkDetailView,SubmissionView,LinkUpdateView,LinkDeleteView,ProfileDetailView,VoteFormView
from django.contrib.auth.views import login,logout
from django.contrib.auth.decorators import login_required as auth

urlpatterns = [
    path('',LinkListView.as_view(),name='home'),
    url(r'^login/$',login,{'template_name':'hrapp/login.html'}),
    url(r'^logout/$',logout,{'template_name':'hrapp/logout.html'}),
    path('register/',views.register,name='register'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('edit/',auth(views.edit_profile),name='edit_profile'),
    path('change_password/',auth(views.change_password),name='change_password'),
    path('create/',auth(LinkCreateView.as_view()),name='create'),
    path('<int:pk>/',auth(views.LinkDetailView),name='post_detail'),
    path('submissions/',auth(SubmissionView.as_view()),name='submissions'),
    path('update/<int:pk>/',auth(LinkUpdateView.as_view()),name='update'),
    path('<int:pk>/delete/',auth(LinkDeleteView.as_view()),name='delete'),
    path("detail/",auth(ProfileDetailView.as_view()),name='profile_detail'),
    path('vote/',auth(VoteFormView.as_view()),name='vote'),
]
