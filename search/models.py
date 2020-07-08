from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from courses.models import Curso

# Create your models here.
class Participante(models.Model):
	name 			= models.CharField(max_length=30, verbose_name='Nombre')
	last_name 		= models.CharField(max_length=30, verbose_name='Apellido')
	student_id		= models.CharField(max_length=15, verbose_name='Identificación personal')
	email 			= models.EmailField(max_length=200, verbose_name='Correo electrónico')
	phone_number	= models.IntegerField()
	qr_url			= models.CharField(max_length=200)
	UUID			= models.CharField(max_length=60, unique=True)
	curso			= models.ForeignKey(Curso, blank=True, on_delete=models.CASCADE)
	validation_url	= models.CharField(max_length=250)

	def __str__(self):
		return self.last_name

	def get_absolute_url(self):
		return reverse('search:detail', kwargs={'student_id': self.id})

def save_qr_url(sender, instance, *args, **kwargs):
	instance.qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=%s" % instance.validation_url
	# 'https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=' +
	# "Hello %s" % subs

pre_save.connect(save_qr_url, sender=Participante)
