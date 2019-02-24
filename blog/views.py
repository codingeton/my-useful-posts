import io
from django.http import HttpResponse
#importing get_template from loader
from django.template.loader import get_template
from .utils import render_to_pdf
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import Post, Comment, LeveragePercentage
from blog.forms import PostForm, CommentForm, LeveragePercentageForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (View,TemplateView, ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from django.db.models import Q
from fuzzywuzzy import fuzz
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import generics
from .serializers import PostSerializer
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

#PDF Generate view for the list of posts
class BlogListPdf(ListView):
    model = Post
    def get(self, request):
        post_title = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        params = {
            "post_title": post_title
        }
        return render_to_pdf('blog/blog_list_for_pdf.html', params)

#PDF Generation for the blog content

class BlogDetailPDF(DetailView):
    model = Post
    def get(self, request,pk):
        post = get_object_or_404(Post, pk=pk)
        #post_content = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        params = {
            "post": post
        }
        return render_to_pdf('blog/blog_detail_for_pdf.html', params)

#These are class based views

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post
    paginate_by = 2
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        logger.info("Someone viewed the list of blogs")

class PostDetailView(DetailView):
    model = Post

#Use LoginRequiredMixin for Class based views
#It requires two more arguments - login url and redirect field name
class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

#CBV to delete a blog post and using reverse_lazy to redirect user to the posts list(home)
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

#Display all posts that are in draft state
#Using query_set method to identify the posts for which the published date is null
class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_draft_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


##################################################################
#Function based views below to perform actions on posts & comments
##################################################################


@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})

#Refer approve() method in models file for more understanding
@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk #Saving this to a variable before deleting helps to remember the post
    comment.delete()
    return redirect('post_detail', pk=post_pk)

@login_required
def leverage_calculate(request):
    match_percentage = 0
    if request.method == "POST":
        form = LeveragePercentageForm(data = request.POST)
        if form.is_valid():
            source_segment = request.POST.get('source')
            reference_segment = request.POST.get('reference')
            match_percentage = fuzz.ratio(source_segment, reference_segment)
            form.save()
            # if match_percentage:
            #     return render(request, 'blog/leverage_percentage.html',{'form':form,'match_percentage':match_percentage})
        else:
            print(form.errors)
    else:
        form = LeveragePercentageForm()
    return render(request, 'blog/leverage_percentage.html', {'form':form,'match_percentage':match_percentage})

#Method for search

def search(request):
    model = Post
    query = request.GET.get('q')
    posts = Post.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))
    print ("Text length is::::",len(posts))
    params = {
        'posts':posts
    }
    return render(request, 'blog/post_list.html', params)

#Exposing content via Rest APIs
class PostListRest(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetailRest(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
