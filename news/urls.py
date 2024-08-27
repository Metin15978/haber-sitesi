from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),   
    path('authors/', views.authors, name="authors"),    
    path('blog/', views.blog, name="blog"),  
    
    path('category/<str:category_name>/', views.categories, name="category"),  
     
    path('details/<str:newsSlug>/', views.details, name="details"),
    path('profile/<slug:slug>', views.profile, name="profile"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('dashboard/',views.dashboard, name="dashboard"),
    path('news/', views.news_upload, name='news_upload'),
]
