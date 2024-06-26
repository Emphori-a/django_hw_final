from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import include, path, reverse_lazy


urlpatterns = [
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('login'),
        ),
        name='registration',
    ),
]

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.internal_server_error'
