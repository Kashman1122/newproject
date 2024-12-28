from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns=[
    path('admin/',admin.site.urls),
    # path('login/',views.login,name='login'),
    path('index/',views.index,name='index'),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('',views.landing,name='landing'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)