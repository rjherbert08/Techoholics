from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.http import HttpResponseRedirect
from django.urls import reverse

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'                        # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']                             # changing the order from newest to oldest from top
    paginate_by = 5                                         # controls the amount of post per page

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html'                  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5                                         # controls the amount of post per page

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):      #
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):                             #adds the authors name to the new post
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):      #
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):                             #adds the authors name to the new post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):                                    #prevents users from updating other users post
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):                                    #prevents users from updating other users post
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


