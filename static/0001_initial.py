# Generated by Django 2.2.1 on 2019-07-20 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('carga_horaria', models.DecimalField(decimal_places=2, max_digits=4)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('slug', models.SlugField(blank=True)),
            ],
            options={
                'ordering': ['-fecha_inicio'],
            },
        ),
    ]
