from django.db import models
from django.utils import timezone
from django.urls import reverse

# Model for the blog post

class Post(models.Model):
    author = models.ForeignKey('auth.User' ,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

#Identify the publish date of the blog and save it

    def publish(self):
        self.published_date = timezone.now()
        self.save()

#Display the approved comments to the user. Behind the scenes, unapproved comments will be stored but not approved

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

#Tell Django where it should it take user after creating the blogpost
#In this case, take the user to the post_detail view(the blog itself that the user created)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk':self.pk})

#Define the string representation of the model. In this case, title of the blog

    def __str__(self):
        return self.title

#Create a model for comments

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)#Associate the comment to a post
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

#Create method to approve comments

    def approve(self):
        self.approved_comment = True
        self.save()

    # Tell Django where it should it take user after a user comments on a post.
    # In this case, take the user to the post_list view(page) which is also the home page

    def get_absolute_url(self):
        return reverse("post_list")

#Create a string representation of the model
    def __str__(self):
        return self.text

#Model for leverage calculator

class LeveragePercentage(models.Model):
    name = models.CharField(max_length=200)
    source = models.TextField()
    reference = models.TextField()

    def __str__(self):
        return self.name
