import uuid

from django.contrib import admin

from .models import Participante

# Register your models here.
class ParticipanteAdmin(admin.ModelAdmin):
	#fields = ('name', 'last_name', 'email')
	list_display = ['id', 'name', 'last_name', 'email', 'phone_number']
	class Meta:
		model = Participante

	# def save_model(self, request, obj, form, change):
 #         obj.UUID = uuid.uudi4()
 #         obj.save()

admin.site.register(Participante, ParticipanteAdmin)