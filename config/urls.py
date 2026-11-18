from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('inscription/', views.register, name='register'),
    path('connexion/', views.login_view, name='login'),
    path('deconnexion/', views.logout_view, name='logout'),
    path('commenter/<int:post_id>/', views.add_comment, name='add_comment'),
    path('aimer/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('modifier-publication/<int:post_id>/', views.edit_post, name='edit_post'),
    path('supprimer-publication/<int:post_id>/', views.delete_post, name='delete_post'),
    path('profil/', views.profile_view, name='profile'),
]