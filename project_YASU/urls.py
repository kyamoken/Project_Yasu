
from django.contrib import admin
from django.urls import path, include
from Online_15.views import HomePageView
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('online_15/', include('Online_15.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
