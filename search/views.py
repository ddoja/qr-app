# -*- coding: utf-8 -*-
import re
import uuid

from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse

from unicodedata import normalize
from weasyprint import HTML, CSS

from .forms import ParticipanteForm
from .models import Participante
from courses.models import Curso

# Create your views here.
def student_create(request, curso=None):
	# obj = Participante.objects.all()
	# if curso:
	#   qs = get_object_or_404(Curso, slug=curso)
	#   nombre_curso = qs.nombre
	# else:
	#   qs = create() # Colocar los valores por defecto de DB, dejar opción para colocar nombre
	curso_obj = get_object_or_404(Curso, slug=curso)
	form = ParticipanteForm(request.POST or None)
	code_gen = uuid.uuid4()
	if form.is_valid():
		obj = Participante()
		obj.name = form.cleaned_data['name']
		obj.last_name = form.cleaned_data['last_name']
		obj.student_id = form.cleaned_data['student_id']
		obj.email = form.cleaned_data['email']
		obj.phone_number = form.cleaned_data['phone_number']
		obj.validation_url = 'https:www.consultalegalddoja.com/seminarios/participantes/validacion?q=' + str(code_gen)
		#obj.qr_url = 'https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=' + validation_url
		obj.UUID = code_gen
		obj.curso = curso_obj
		obj.save()
		messages.success(request, 'Participante guardado de forma exitosa')
		# return HttpResponseRedirect(Curso.get_course_list_url())
		return HttpResponseRedirect(curso_obj.get_absolute_url())
		# return reverse('search:detail', kwargs={'student_id': self.id})
		# return HttpResponseRedirect(obj.get_absolute_url()) este era el último que funciona
		#return HttpResponseRedirect('/seminarios/create')
	# else:
	#     messages.error(request, 'Error al intentar guardar el participante.')

	context = {
		'form': form,
		'curso': curso_obj.slug,
	}

	return render(request, 'registro.html', context)

def student_list(request, q=None):
	obj = Participante.objects.all()
	query = Participante.objects.filter(student_id=request.GET.get('q'))
	if query:
		context = {
			'obj': query,
		}
	else:
		context = {
			'obj': obj
		}
	return render(request, 'list.html', context)

def student_detail(request, student_id=None):
  instance = get_object_or_404(Participante, id=student_id)
  #instance = get_object_or_404(Participante, UUID=student_id)

  context = {
	  'title': "Lista de participantes",
	  'instance': instance
  }
  return render(request, 'student_detail.html', context)

def student_certificate(request, student_id=None):
	instance = get_object_or_404(Participante, id=student_id)

	course_name = instance.curso.nombre
	characters = 0
	words = 0
	text = []

	if len(course_name)> 45:
		course_name_chunks = course_name.split()
		for x in course_name_chunks:
			text.append(course_name_chunks[words])
			characters += len(text) + words
			if characters < 48:
				line1 = ' '.join(text)
			words += 1
			line2 = course_name[len(line1):len(course_name)]
	else:
		line1 = course_name
		line2 = ""

	context = {
		'title': "Lista de participantes",
		'instance': instance,
		'line1': line1,
		'line2': line2,
	}

	html_string = render_to_string('student_certificate.html', context)

	#Se eliminan las tíldes o cualquier carácter no ASCII del nombre
	nombre = instance.name
	nombre = re.sub(
		r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
		normalize( "NFD", nombre), 0, re.I
	)
	nombre = normalize( 'NFC', nombre)
	nombre = nombre.replace("ñ", "n").replace("Ñ", "N").replace(" ", "-")

	#Se eliminan las tíldes o cualquier carácter no ASCII del apellido
	apellido = instance.last_name
	apellido = re.sub(
		r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
		normalize( "NFD", apellido), 0, re.I
	)
	apellido = normalize( 'NFC', apellido)
	apellido = apellido.replace("ñ", "n").replace("Ñ", "N").replace(" ", "-")

	#html = HTML(string=html_string)
	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	#html.write_pdf(target='/tmp/mypdf.pdf');
	html.write_pdf(target='/tmp/mypdf.pdf', stylesheets=[CSS(settings.STATIC_ROOT +  '/css/detail_pdf_gen.css')], presentational_hints=True);

	fs = FileSystemStorage('/tmp')
	with fs.open('mypdf.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		response['Content-Disposition'] = "inline; filename=certificado-{name}-{last_name}.pdf".format(
				name=nombre,
				last_name=apellido,).lower()
		return response

	return response

def student_certificate_data_only(request, student_id=None):
	instance = get_object_or_404(Participante, id=student_id)

	course_name = instance.curso.nombre
	characters = 0
	words = 0
	text = []

	if len(course_name)> 45:
		course_name_chunks = course_name.split()
		for x in course_name_chunks:
			text.append(course_name_chunks[words])
			characters += len(text) + words
			if characters < 48:
				line1 = ' '.join(text)
			words += 1
			line2 = course_name[len(line1):len(course_name)]
	else:
		line1 = course_name
		line2 = ""

	context = {
		'title': "Lista de participantes",
		'instance': instance,
		'line1': line1,
		'line2': line2,
	}

	html_string = render_to_string('student_certificate_data_only.html', context)

	#Se eliminan las tíldes o cualquier carácter no ASCII del nombre
	nombre = instance.name
	nombre = re.sub(
		r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
		normalize( "NFD", nombre), 0, re.I
	)
	nombre = normalize( 'NFC', nombre)
	nombre = nombre.replace("ñ", "n").replace("Ñ", "N").replace(" ", "-")

	#Se eliminan las tíldes o cualquier carácter no ASCII del apellido
	apellido = instance.last_name
	apellido = re.sub(
		r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
		normalize( "NFD", apellido), 0, re.I
	)
	apellido = normalize( 'NFC', apellido)
	apellido = apellido.replace("ñ", "n").replace("Ñ", "N").replace(" ", "-")

	html = HTML(string=html_string)
	html.write_pdf(target='/tmp/mypdf.pdf');

	fs = FileSystemStorage('/tmp')
	with fs.open('mypdf.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		response['Content-Disposition'] = "inline; filename=certificado-{name}-{last_name}.pdf".format(
				name=nombre,
				last_name=apellido,).lower()
		return response

	return response

def student_update(request, student_id=None):
	instance = get_object_or_404(Participante, id=student_id)
	form = ParticipanteForm(request.POST or None, instance=instance)
	if form.is_valid():
		form.save()
		messages.success(request, 'Participante actualizado de forma exitosa')
		return HttpResponseRedirect(instance.curso.get_absolute_url())
	
	context = {
		'instance': instance,
		'form': form,
		'curso': instance.curso.slug,
	}
	return render(request, 'registro.html', context)

def student_delete(request, student_id=None):
	instance = get_object_or_404(Participante, id=student_id)
	obj = instance.curso
	instance.delete()
	messages.success(request, "El participante ha sido eliminado satisfactoriamente")
	return HttpResponseRedirect(obj.get_absolute_url())

def validation(request, q=None):
	uuid_string = str(request.GET.get('q'))
	query = Participante.objects.filter(UUID=request.GET.get('q'))
	if query:
		context = {
			'participantes': query,
		}
	else:
		context = {}
	return render(request, 'validation.html', context)
