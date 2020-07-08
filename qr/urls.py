from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('seminarios/participantes/', include(('search.urls', 'search'), namespace='search')),
    path('seminarios/', include(('courses.urls', 'courses'), namespace='courses')),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/seminarios/admin'}, name='logout'),
    #include(('reviews.urls', 'reviews'), namespace='reviews')
]
