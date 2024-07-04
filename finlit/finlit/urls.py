"""
URL configuration for finlit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('webinar.urls', namespace='webinar')),
    path('api/', include('user.urls', namespace='user')),
    # path('api/', include('career.urls', namespace='career')),
    # path('api/', include('course.urls', namespace='course')),
    # path('api/', include('counseling.urls', namespace='counseling')),
    path('api/', include('order.urls', namespace='order')),
]
