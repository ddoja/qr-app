from django.urls import path

from . import views

urlpatterns = [
    path('admin', views.course_list, name='list'),
    path('create', views.course_create, name='create'),
    # path('detail/<int:student_id>', views.student_detail, name='detail'),
    path('<slug:course_name>/detalles', views.course_detail, name='detail'),
    path('<slug:course_name>/listado-de-participantes', views.print_participant_list, name='print-list'),
    #path('responsabilidad-medica/detalles', views.course_detail, name='detail'),
    path('<slug:course_name>/edit', views.course_edit, name='edit'),
    # path('<int:student_id>/edit/', views.student_update, name='edit'),
    # path('delete/', views.student_delete, name='delete'),
]