from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    CreateView, DeleteView, DetailView, UpdateView, ListView
)
from django.urls import reverse_lazy

from .forms import CommentForm, PostForm, UserProfileForm
from .models import Category, Comment, Post


POSTS_PER_PAGE = 10


class BlogIndexListView(ListView):
    model = Post
    paginate_by = POSTS_PER_PAGE
    template_name = 'blog/index.html'

    def get_queryset(self):
        queryset = self.model.today_post.all()
        return queryset.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')


class BlogPostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        post = self.object
        if post.is_published is False and post.author != self.request.user:
            raise Http404
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(post=self.object)
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
        queryset = Post.today_post.filter(category=self.get_category_posts())
        return queryset.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category_posts()
        return context


class BlogProfileUserDetailView(DetailView):
    model = get_user_model()
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    paginate_by = POSTS_PER_PAGE

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(self.model, username=self.kwargs['username'])

        if self.request.user != user:
            post = Post.today_post.filter(author=user)

        else:
            post = Post.objects.all().filter(author=user).select_related(
                'category', 'author', 'location')
        queryset = post.annotate(comment_count=Count(
            'comments')).order_by('-pub_date')
        paginator = Paginator(queryset, self.paginate_by)
        try:
            posts = paginator.page(self.request.GET.get('page'))
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['profile'] = user
        context['page_obj'] = posts
        return context


class BlogProfileUserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
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
        form_post = form.save(commit=False)
        form_post.author = self.request.user
        return super().form_valid(form)


class BlogPostMixin:
    model = Post
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if post.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)


class BlogPostUpdateView(BlogPostMixin, UpdateView):
    form_class = PostForm


class BlogPostPostDeleteView(BlogPostMixin, LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object
        form = PostForm(self.request.POST or None, instance=instance)
        context['form'] = form
        return context


class BlogCommentMixin:
    model = Comment
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'pk': self.kwargs['post_id']}
        )


class BlogCommentCreateView(BlogCommentMixin, LoginRequiredMixin, CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        comment.save()
        return super().form_valid(form)


class BlogCommentUpdateView(BlogCommentMixin, LoginRequiredMixin, UpdateView):
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        if comment.author != self.request.user:
            return redirect('blog:post_detail', pk=kwargs['post_id'])
        else:
            return super().dispatch(request, *args, **kwargs)


class BlogCommentDeleteView(BlogCommentMixin, LoginRequiredMixin, DeleteView):

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        if comment.author != self.request.user:
            return redirect('blog:post_detail', pk=kwargs['post_id'])
        else:
            return super().dispatch(request, *args, **kwargs)
