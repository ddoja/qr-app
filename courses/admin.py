from django.contrib import admin

from .models import Curso

# Register your models here.
class CursoAdmin(admin.ModelAdmin):
	list_display = ['id', 'nombre', 'fecha_inicio', 'carga_horaria']
	class Meta:
		model = Curso		


admin.site.register(Curso, CursoAdmin)