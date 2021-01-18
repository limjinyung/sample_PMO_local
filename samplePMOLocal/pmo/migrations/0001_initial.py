# Generated by Django 3.1.5 on 2021-01-17 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('position', models.CharField(choices=[('PM', 'Project Manager'), ('QA', 'Quality Assurance'), ('SD', 'Software Developer')], default='SD', max_length=20, null=True)),
                ('task', models.ManyToManyField(to='pmo.Task')),
            ],
        ),
    ]
