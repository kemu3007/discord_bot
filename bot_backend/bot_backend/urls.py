"""bot_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from rest_framework.routers import DefaultRouter

import bot.views as bot_views

router = DefaultRouter()
router.register("ohayou", bot_views.OhayouViewSets)
router.register("holodule_reminder", bot_views.HoloduleReminderViewSets)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api/v1/holodule/", bot_views.HoloduleView().as_view()),
    path("api/v1/holodule/line/", bot_views.LINEHoloduleView().as_view()),
]

urlpatterns += staticfiles_urlpatterns()
