import json
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import ListView,TemplateView,DetailView
from .models import Link,Vote,Comment,UserProfile
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from .forms import RegistrationForm,EditProfileForm,LinkForm,ProfileEditForm,CommentForm,VoteForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator


class LinkListView(ListView):
   template_name = 'hrapp/linklist.html'
   model = Link
   queryset = Link.votecount.all()
   paginate_by = 8
   def proff(request):
      context = {'user':request.user,'domain':Link.objects.all(),}
      return render(request,'hrapp/linklist.html',context)

#def LinkListView(request):
 #  posts = Link.votecount.all()
  # context = {"posts":posts,}
   #return render(request,'hrapp/linklist.html',context)

class RandomGossipMixin(object):
   def get_context_data(self,**kwargs):
      context = super(RandomGossipMixin, self).get_context_data(**kwargs)
      #context[u"randomquip"] = Comment.objects.order_by('?')[0]
      return context


#class ProfileView(RandomGossipMixin, ListView):
 #  template_name = 'hrapp/profile.html'
  # model = Link
   #queryset = Link.votecount.all()
   #paginate_by = 8
   #def get_context_data(self, **kwargs):
    #  context = super(ProfileView, self).get_context_data(**kwargs)
     # voted = Vote.objects.filter(voter=self.request.user)
      #links_in_page = [link.id for link in context["object_list"]]
     # voted =voted.filter(link_id__in=links_in_page)
     # voted = voted.values_list('link_id',flat=True)
     # context["voted"] = voted
     # return context 

class ProfileView(RandomGossipMixin, ListView):
   template_name = 'hrapp/profile.html'
   model = Link
   queryset = Link.votecount.all()
   paginate_by = 8
   def get_context_data(self, **kwargs):
      context = super(ProfileView, self).get_context_data(**kwargs)
      voted = Vote.objects.filter(voter=self.request.user)
      links_in_page = [link.id for link in context["object_list"]]
      voted =voted.filter(link_id__in=links_in_page)
      voted = voted.values_list('link_id',flat=True)
      context["voted"] = voted
      return context 



   #def prof(request):
    #  context = {'user':request.user,'domain':Link.objects.all(),"comments":comments,}
     # return render(request,'hrapp/profile.html',context)






class LinkCreateView(CreateView):
   template_name = 'hrapp/create.html'
   model = Link
   form_class = LinkForm
   def form_valid(self, form):
      f = form.save(commit = False)
      f.rank_score = 0.0
      f.author = self.request.user
      f.save()
      return super(LinkCreateView ,self).form_valid(form)



def LinkDetailView(request,pk):
   post = Link.votecount.get(id=pk)
   comments = Comment.objects.filter(post = post, reply = None).order_by('-id')
   

   if request.method=='POST':
      comment_form = CommentForm(request.POST or None)
      if comment_form.is_valid():
         content = request.POST.get('content')
         reply_id = request.POST.get('comment_id')
         comment_qs = None
         if reply_id:
            comment_qs = Comment.objects.get(id=reply_id)
         comment = Comment.objects.create(post=post,user=request.user,content=content,reply=comment_qs)
         comment.save()
         return HttpResponseRedirect(".")
   else:
      comment_form = CommentForm()

   context = {"post":post,"comments":comments,"comment_form":comment_form,}
   return render(request,"hrapp/post_detail.html",context)







class SubmissionView(ListView):
   template_name = 'hrapp/submissions.html'
   model = Link
   queryset = Link.votecount.all()
   paginate_by = 8
   def get_queryset(self):

      return self.model.objects.filter(author=self.request.user).order_by('-submitted_on')

   def posts(request):

      context = {'user':request.user,'domain':Link.objects.all(),}
      return render(request,'hrapp/submissions.html',context)



class LinkUpdateView(UserPassesTestMixin,UpdateView):
   template_name = 'hrapp/update.html'
   model = Link
   form_class = LinkForm
   def form_valid(self,form):
      form.instance.author = self.request.user
      return super().form_valid(form)
   def test_func(self):
      post = self.get_object()
      if self.request.user == post.author:
         return True
      else:
         return False


class LinkDeleteView(UserPassesTestMixin,DeleteView):
   template_name = 'hrapp/delete.html'
   model = Link
   success_url="/submissions"
   def test_func(self):
      post = self.get_object()
      if self.request.user == post.author:
         return True
      else:
         return redirect("/submissions")


def register(request):
   if request.method=='POST':
      form = RegistrationForm(request.POST)
      if form.is_valid():
         new_user = form.save(commit = False)
         new_user.save()
         UserProfile.objects.create(user = new_user)
         return redirect('/login')
   else:
      form = RegistrationForm()
      
      context = {'form':form,}
      return render(request,'hrapp/register.html',context)




class ProfileDetailView(ListView):
   model = UserProfile
   #slug_field = "username"
   template_name = 'hrapp/detail.html'

   #def get_object(self,queryset = None):
    #  user = super(ProfileDetailView,self).get_object(queryset)
     # UserProfile.objects.get_or_create(user = user)
      #return user


def edit_profile(request):
   if request.method == 'POST':
      user_form = EditProfileForm(data = request.POST or None, instance = request.user)
      profile_form = ProfileEditForm(data = request.POST or None, instance = request.user.userprofile)
      if user_form.is_valid() and profile_form.is_valid():
         user_form.save()
         profile_form.save()
         return redirect('/detail')
   else:
      user_form = EditProfileForm(instance = request.user)
      profile_form = ProfileEditForm(instance = request.user.userprofile)
      context = {'user_form':user_form, 'profile_form':profile_form,}
      return render(request,'hrapp/edit_profile.html',context)




def change_password(request):
   if request.method =='POST':
      form = PasswordChangeForm(data = request.POST,user=request.user)
      if form.is_valid():
         form.save()
         update_session_auth_hash(request,form.user)
         return redirect('/detail')
      else:
         return redirect('/change_password')
   else:
      form = PasswordChangeForm(user=request.user)
      context = {'form':form}
      return render(request,'hrapp/change_password.html',context)


class JSONFormMixin(object):
   def create_response(self,vdict=dict(),valid_form=True):
      response = HttpResponse(json.dumps(vdict),content_type='application/json')
      response.status = 200 if valid_form else 500
      return response



class VoteFormBaseView(FormView):
   form_class = VoteForm

   def create_response(self,vdict=dict(),valid_form=True):
      response = HttpResponse(json.dumps(vdict))
      response.status = 200 if valid_form else 500
      return response

   def form_valid(self,form):
      link = get_object_or_404(Link,pk=form.data["link"])
      user = self.request.user
      prev_votes = Vote.objects.filter(voter=user,link=link)
      has_voted = (len(prev_votes) > 0)
      ret = {"success":1}
      if not has_voted:
         v = Vote.objects.create(voter=user,link=link)
         ret["voteobj"] = v.id

      else:
         prev_votes[0].delete()
         ret["unvoted"] = 1
      return self.create_response(ret,True)


   def form_invalid(self,form):
      ret ={"success":0,"form_errors":form.errors}
      return self.create_response(ret,False)

class VoteFormView(JSONFormMixin, VoteFormBaseView):
   pass
   #def con(request):
    #  return HttpResponseRedirect("/profile")
