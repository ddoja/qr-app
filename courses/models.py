from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils.text import slugify

from .utils import create_slug

# Create your models here.
class Curso(models.Model):
	nombre 			= models.CharField(max_length=100)
	carga_horaria	= models.DecimalField(max_digits=4, decimal_places=2)
	fecha_inicio	= models.DateField()
	fecha_fin		= models.DateField()
	slug			= models.SlugField(blank=True)

	def __str__(self):
		return self.nombre

	class Meta:
		ordering = ['-fecha_inicio']

	def get_absolute_url(self):
		return reverse('courses:detail', kwargs={'course_name': self.slug})

	def get_course_list_url():
		return reverse('courses:list')

def save_slug(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(save_slug, sender=Curso)

# def pre_save_video_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = create_slug(instance)

# pre_save.connect(pre_save_video_receiver, sender=Course)