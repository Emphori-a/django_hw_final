from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogIndexListView.as_view(), name='index'),
    path('posts/<int:pk>/edit/',
         views.BlogPostUpdateView.as_view(), name='edit_post'),
    path(
        'posts/<int:pk>/delete/',
        views.BlogPostPostDeleteView.as_view(),
        name='delete_post'
    ),
    path('posts/<int:post_id>/comment/',
         views.BlogCommentCreateView.as_view(), name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:pk>/',
         views.BlogCommentUpdateView.as_view(), name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:pk>/',
         views.BlogCommentDeleteView.as_view(), name='delete_comment'),
    path('posts/<int:pk>/',
         views.BlogPostDetailView.as_view(), name='post_detail'),
    path('posts/create/',
         views.BlogPostCreateView.as_view(), name='create_post'),
    path('category/<slug:category_slug>/',
         views.BlogCategoryPostsListView.as_view(),
         name='category_posts'),
    path('profile/edit/', views.BlogProfileUserUpdateView.as_view(),
         name='edit_profile'),
    path('profile/<username>/',
         views.BlogProfileUserDetailView.as_view(), name='profile'),
]
