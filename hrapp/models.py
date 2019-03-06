from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count,Manager
from django.urls import reverse
import datetime
from django.db.models.signals import post_save
from django.utils.timezone import now

class LVCManager(models.Manager):
   def get_queryset(self):
      return super(LVCManager, self).get_queryset().annotate(votes = Count('vote')).order_by("-rank_score","-votes")


class Link(models.Model):
   title = models.CharField("Headline", max_length =200)
   author = models.ForeignKey(User, on_delete=models.CASCADE)
   submitted_on = models.DateTimeField(auto_now_add = True)
   rank_score = models.FloatField(default=0.0)
   url = models.URLField('URL',max_length = 200,blank =True)
   description = models.TextField(blank=True)
   votecount = LVCManager() 
   objects = models.Manager() 

   def __str__(self):
      return self.title
   
   def get_absolute_url(self):
      return reverse("post_detail",kwargs = {"pk":self.id})

   @property
   def domain(self):
      return (self.url.split('//')[-1].split('/')[0])

   def set_rank(self):
      SECS_IN_HOUR = float(60*60)
      GRAVITY = 1.2
      delta = now()-self.submitted_on
      item_hour_age = delta.total_seconds()//SECS_IN_HOUR
      votes = self.votes-1
      self.rank_score = votes / pow((item_hour_age+2),GRAVITY)
      self.save()

class Vote(models.Model):
   voter = models.ForeignKey(User, on_delete=models.CASCADE)
   link = models.ForeignKey(Link , on_delete=models.CASCADE)
   
   def __str__(self):
      return "%s voted %s " % (self.voter.username,self.link.title)



class UserProfile(models.Model):
   user = models.OneToOneField(User,unique = True,on_delete=models.CASCADE)
   bio = models.TextField(null = True,blank = True)

   def __str__(self):
      return "Profile of user {}".format(self.user.username)

   #def CreateProfile(sender ,**kwargs):
    #  if kwargs["created"]:
     #    user_profile = UserProfile.objects.create(user = kwargs["instance"])
      #   post_save.connect(create_profile, sender = User)


class Comment(models.Model):
   post = models.ForeignKey(Link,on_delete=models.CASCADE)
   user= models.ForeignKey(User,on_delete=models.CASCADE)
   content = models.TextField(max_length = 160)
   reply = models.ForeignKey('Comment',null=True,related_name="replies",on_delete=models.CASCADE)
   timestamp =models.DateTimeField(auto_now_add = True)

   def __str__(self):
      return '{}-{}'.format(self.post.title,str(self.user.username))
