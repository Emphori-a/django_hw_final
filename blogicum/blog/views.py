from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    CreateView, DeleteView, DetailView, UpdateView, ListView
)
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import CommentForm, PostForm, UserProfileForm
from .models import Category, Comment, Post, User


POSTS_PER_PAGE = 10


class BlogIndexListView(ListView):
    paginate_by = POSTS_PER_PAGE
    template_name = 'blog/index.html'
    queryset = Post.for_page.get_posts_queryset(
        is_today_posts=True,
        is_annotate=True
    ).all()


class BlogPostDetailView(DetailView):
    template_name = 'blog/detail.html'
    queryset = Post.for_page.all()
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if post.author != self.request.user and (
            not post.is_published
            or not post.category.is_published
            or not post.pub_date <= timezone.now()
        ):
            raise Http404
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.select_related('author').filter(
            post=self.object
        )
        form = CommentForm(self.request.POST or None)
        context['comments'] = comments
        context['form'] = form
        return context


class BlogCategoryPostsListView(ListView):
    paginate_by = POSTS_PER_PAGE
    template_name = 'blog/category.html'

    def get_category_posts(self):
        category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True,
        )
        return category

    def get_queryset(self):
        return Post.for_page.get_posts_queryset(
            is_today_posts=True,
            is_annotate=True
        ).filter(
            category=self.get_category_posts()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category_posts()
        return context


class BlogProfileUserDetailView(ListView):
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    paginate_by = POSTS_PER_PAGE

    def get_user(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_queryset(self):
        return Post.for_page.get_posts_queryset(
            is_today_posts=self.request.user != self.get_user(),
            is_annotate=True
        ).filter(author=self.get_user())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_user()
        return context


class BlogProfileUserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogPostMixin:
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return redirect('blog:post_detail', post_id=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class BlogPostUpdateView(BlogPostMixin, UpdateView):
    form_class = PostForm


class BlogPostPostDeleteView(LoginRequiredMixin, BlogPostMixin, DeleteView):
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(
            self.request.POST or None,
            instance=self.object
        )
        return context


class BlogCommentMixin(LoginRequiredMixin):
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class BlogCommentDispath:
    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(
            Comment,
            pk=kwargs['comment_id'],
            post_id=kwargs['post_id']
        )
        if comment.author != self.request.user:
            return redirect('blog:post_detail', post_id=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class BlogCommentCreateView(BlogCommentMixin, CreateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)


class BlogCommentUpdateView(BlogCommentMixin, BlogCommentDispath, UpdateView):
    pass


class BlogCommentDeleteView(BlogCommentMixin, BlogCommentDispath, DeleteView):
    pass
