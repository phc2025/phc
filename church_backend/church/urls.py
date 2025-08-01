from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *

user_list = UserProfileViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('register/', user_registerView.as_view(), name='register'),
    path('count/', user_count.as_view(), name='userscount'),
    path('users/<int:id>/', user_registerView.as_view(), name='user_detail'),
    
    path('login/', user_loginView.as_view(), name='login'),
    path('helping/', HelpingHandView.as_view(), name='helping_hand'),
    path('helping/<int:user_id>/', HelpingHandView.as_view(), name='helping_hand'),
    path('donate/', DonateView.as_view(), name='donate'),
path('donate/<int:user_id>/', DonateView.as_view(), name='donate_detail'),
    path('users/', user_list, name='user_list'),
    path('timings/', TimingSend.as_view(), name='timings_post'),
    path('timingsdata/', TimingView.as_view(), name='timings_get'),
    path('timingdata/<int:pk>/', TimingView.as_view(), name='timings_detail'),
]

# ✅ Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
