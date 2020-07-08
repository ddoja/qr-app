from django import forms
from django.forms import ModelForm

from .models import Curso

class CursoForm(ModelForm):

	carga_horaria	= forms.DecimalField(widget=forms.TextInput())

	fecha_inicio 	= forms.DateField(
						input_formats=['%d/%m/%Y'],
						widget= forms.DateInput(attrs={'id':'datepicker', 'placeholder': 'Formato dd/mm/aaaa'}))

	fecha_fin 		= forms.DateField(
						input_formats=['%d/%m/%Y'], 
						widget= forms.DateInput(attrs={'id':'datepicker1', 'placeholder': 'Formato dd/mm/aaaa'}))

	class Meta:
		model 	= Curso
		fields 	= ['nombre', 'carga_horaria', 'fecha_inicio', 'fecha_fin']