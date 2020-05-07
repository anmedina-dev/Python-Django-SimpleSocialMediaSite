from django.views.generic import (ListView,
                                DetailView, 
                                CreateView,
                                UpdateView,
                                DeleteView)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
#getting the model from the models fils in this directory and importing a model
from .models import Post
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, Block

import operator

from django.db.models import Q


class UserSearchListView(ListView):
    """
    Display a User List page filtered by the search query.
    """
    model = User
    paginate_by = 10
    template_name = 'blog/user_search.html'
    context_object_name = 'users'

    def get_queryset(self):
        result = super(UserSearchListView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = User.objects.filter(username=query)
            result = postresult
        else:
            result = None
        return result
        

# Create your views here.
def home(request):
    context = {
        #Post.objects.all() is a database query to get all the posts
        'posts': Post.objects.all(),
        'friends': Friend.objects.friends(request.user)
    }
    #the context is the posts from the database
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

#posts from a specific user
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    #makes the current logged user the author of post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

#Mixins have to be to the left of the View
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    #makes the current logged user the author of post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    



def about(request):
    #the blog/about.html is in the templates/blog
    return render(request, 'blog/about.html', {'title': 'Blog about'})
