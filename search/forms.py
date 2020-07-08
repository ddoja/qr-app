from django import forms
from django.forms import ModelForm

from .models import Participante

class ParticipanteForm(ModelForm):
	phone_number = forms.IntegerField(widget=forms.TextInput())

	class Meta:
		model 	= Participante
		fields 	= ['name', 'last_name', 'student_id', 'email', 'phone_number']

	def __init__(self, *args, **kwargs):
		super(ParticipanteForm, self).__init__(*args, **kwargs)
		self.fields['phone_number'].label = "Teléfono"