from django.conf.urls import url
from Basic_App import views

# Template URLs

app_name = 'Basic_App'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
]