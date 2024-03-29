"""dbMarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from data import urls as data_urls

from . import views
from data import views as data_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^organization/', include(data_urls)),
    url(r'^$', views.home, name='home'),
    url(r'^login$', views.auth_login, name='login'),
    url(r'^logout$', views.auth_logout, name='logout'),
    url(r'^lockscreen$', views.lockscreen, name='lockscreen'),
    url(r'^setup-client', data_views.setup_client, name='setup_client'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
