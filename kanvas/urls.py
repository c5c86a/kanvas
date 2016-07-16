"""kanvas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from app.views import CanvasList, CanvasDetailView, CanvasDelete, company, update_field, create_canvas, voteup, votedown
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),

    url(r'^tinymce/', include('tinymce.urls')),

    url(r'^$', CanvasList.as_view(), name='canvas-list'),
    url(r'^canvas/(?P<pk>[0-9]+)/$', CanvasDetailView.as_view(), name='canvas-detail'),
    url(r'^company/(?P<pk>[0-9]+)/$', company, name='company-detail'),
    url(r'canvas/add/$', create_canvas, name='canvas-add'),
    url(r'canvas/up/(?P<pk>[0-9]+)/$', voteup, name='canvas-up'),
    url(r'canvas/down/(?P<pk>[0-9]+)/$', votedown, name='canvas-down'),
    url(r'canvas/(?P<pk>[0-9]+)/delete/$', CanvasDelete.as_view(), name='canvas-delete'),
    url(r'canvas/(?P<pk>[0-9]+)/(?P<field>.+)/$', update_field, name='canvas-update'),

    url(r'^admin/', include(admin.site.urls)),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
