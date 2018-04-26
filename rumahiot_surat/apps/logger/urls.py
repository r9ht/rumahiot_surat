"""rumahiot_surat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rumahiot_surat.apps.logger.views import device_panel_notification, clear_device_panel_notification, clear_all_device_panel_notification, get_all_device_panel_notification

urlpatterns = [
    url(r'^device/sensor/notification$', device_panel_notification, name='device_panel_notification'),
    url(r'^device/sensor/notification/get/all$', get_all_device_panel_notification, name='get_all_device_panel_notification'),
    url(r'^device/sensor/notification/clear/(?P<device_sensor_notification_log_uuid>.+)$', clear_device_panel_notification, name='clear_device_panel_notification'),
    url(r'^device/sensor/notification/clearall$', clear_all_device_panel_notification, name='clear_all_device_panel_notification')
]
