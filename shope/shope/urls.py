"""shope URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

import debug_toolbar
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('i18n', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),

    path('', include('core.urls')),
    path('profile/', include('profile_app.urls')),

    path('auth/', include("auth_app.urls")),
    path('catalog/', include('catalog_app.urls')),
    path('cart/', include('cart_app.urls')),
    path('order/', include('order_app.urls')),
    path('pay/', include('pay_app.urls')),
]

if settings.DEBUG:
    urlpatterns.extend(
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # type: ignore
    )
    urlpatterns.extend(
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore
    )
    urlpatterns.append(
        path('__debug__/', include(debug_toolbar.urls))
    )
