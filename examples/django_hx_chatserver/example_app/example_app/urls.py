from chat.views import home
from django.conf import settings
from django.urls import re_path
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
               re_path(r'^(?P<chat_channel_name>\w+)$', home, name='home'),
               re_path(r'^$', home, name='home'),
               re_path(r'^admin/', admin.site.urls),
               ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
