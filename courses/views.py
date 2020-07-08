import re

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from unicodedata import normalize
from weasyprint import HTML, CSS

from .models import Curso
from .forms import CursoForm

# Create your views here.
def course_list(request):
	objects = Curso.objects.all()
	context = {
		'cursos': objects
	}
	return render(request, 'course_list.html', context)

def course_detail(request, course_name=None):
	instance = get_object_or_404(Curso, slug=course_name)
	participantes = instance.participante_set.order_by('name')
	next = instance.slug

	context = {
		'instance': instance,
		'participantes': participantes,
		'next': next
	}

	return render(request, 'course_detail.html', context)

def print_participant_list(request, course_name=None):
	instance = get_object_or_404(Curso, slug=course_name)
	participantes = instance.participante_set.order_by('name')
	next = instance.slug

	context = {
		'instance': instance,
		'participantes': participantes,
		'next': next
	}

	html_string = render_to_string('participant_list.html', context)

	#Se eliminan las tíldes o cualquier carácter no ASCII del apellido
	course_name = instance.nombre
	course_name = re.sub(
		r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
		normalize( "NFD", course_name), 0, re.I
	)
	course_name = normalize( 'NFC', course_name)
	course_name = course_name.replace("ñ", "n").replace("Ñ", "N").replace(" ", "-")

	html = HTML(string=html_string)
	html.write_pdf(target='/tmp/mypdf.pdf');

	fs = FileSystemStorage('/tmp')
	with fs.open('mypdf.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		response['Content-Disposition'] = "inline; filename=listado-participantes-{course}-{date}.pdf".format(
				course=course_name,
				date=instance.fecha_inicio,).lower()
		return response

	return response


def course_create(request):
	form = CursoForm(request.POST or None)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect(Curso.get_course_list_url())

	context = {
		'form': form,
	}
	return render(request, 'course_create.html', context)

def course_edit(request, course_name=None):
	instance = get_object_or_404(Curso, slug=course_name)
	form = CursoForm(request.POST or None, instance=instance)
	fecha_inicio_format = instance.fecha_inicio.strftime("%d/%m/%Y")
	if form.is_valid():
		form.fecha_inicio = fecha_inicio_format
		form.save()
		return HttpResponseRedirect(Curso.get_course_list_url())
	context = {
		'form': form,
		'instance': instance
	}
	return render(request, 'course_create.html', context)

