from django.urls import path
from . import views
from .views import logged_out
from django.contrib.auth.views import LogoutView

urlpatterns = [
path('', views.index, name='index'),
path('<str:username>/', views.chat_room, name='chat_room'),
 path('logout/', LogoutView.as_view(next_page='/logged-out/'), name='logout'),
    path('logged-out/', logged_out, name='logged_out'),
    
]