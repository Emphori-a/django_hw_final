from django.urls import include, path

from . import views


app_name = 'blog'

post_urls = [
    path('<int:post_id>/edit/',
         views.BlogPostUpdateView.as_view(), name='edit_post'),
    path(
        '<int:post_id>/delete/',
        views.BlogPostPostDeleteView.as_view(),
        name='delete_post'
    ),
    path('<int:post_id>/comment/',
         views.BlogCommentCreateView.as_view(), name='add_comment'),
    path('<int:post_id>/edit_comment/<int:comment_id>/',
         views.BlogCommentUpdateView.as_view(), name='edit_comment'),
    path('<int:post_id>/delete_comment/<int:comment_id>/',
         views.BlogCommentDeleteView.as_view(), name='delete_comment'),
    path('<int:post_id>/',
         views.BlogPostDetailView.as_view(), name='post_detail'),
    path('create/',
         views.BlogPostCreateView.as_view(), name='create_post'),
]

urlpatterns = [
    path('', views.BlogIndexListView.as_view(), name='index'),
    path('posts/', include(post_urls)),
    path('category/<slug:category_slug>/',
         views.BlogCategoryPostsListView.as_view(),
         name='category_posts'),
    path('edit-profile/', views.BlogProfileUserUpdateView.as_view(),
         name='edit_profile'),
    path('profile/<str:username>/',
         views.BlogProfileUserDetailView.as_view(), name='profile'),
]
