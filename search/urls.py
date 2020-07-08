from django.urls import path

from . import views

urlpatterns = [
    path('', views.student_list, name='list'),
    #path('create', views.student_create, name='create'),
    path('crear/<slug:curso>', views.student_create, name='create-participante'),
    path('vista-previa-de-certificado/<int:student_id>', views.student_detail, name='detail'),
    path('certificado/<int:student_id>', views.student_certificate, name='certificate'),
    path('certificado/<int:student_id>/data', views.student_certificate_data_only, name='certificate-data'),
    #path('detail/<uuid:student_id>', views.student_detail, name='detail'),
    path('editar/<int:student_id>/', views.student_update, name='update'),
    path('<int:student_id>/delete', views.student_delete, name='delete'),
    path('validacion', views.validation, name='validation'),
]