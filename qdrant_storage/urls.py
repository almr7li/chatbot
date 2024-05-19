"""
URL configuration for qdrant_storage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views
from django.views.generic import TemplateView



urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", views.login_, name = 'login'),
    path("signup/", views.signup, name = 'signup'),
    path("logout/", views.logout_, name = 'logout'),
    # path('view_chatbot/<int:chatbot_id>/', views.create_chatbot_collection, name="create_chatbot_collection"),#'view_chatbot'),
    path('create_chatbot/', views.create_chatbot, name = 'create_chatbot'),
    path('chatbot/', views.chatbots_page, name='chatbot_page'),
    # path('chatbot/<int:chatbot_id>/create_collection/', views.create_chatbot_collection, name='create_chatbot_collection'),
    path('chatbot/answer/', views.chatbot_answer, name='chatbot_answer'),
    path('chatbot/<int:chatbot_id>/', views.chat_view, name='chat_view'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
]
