# Generated by Django 4.1.3 on 2022-12-01 16:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('className', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currentSchool', models.CharField(max_length=500)),
                ('currentClass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.currentclass')),
                ('studentName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subjectName', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currentSchool', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='TeacherEnrolment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.teacher')),
            ],
            options={
                'unique_together': {('teacher', 'student')},
            },
        ),
        migrations.AddField(
            model_name='teacher',
            name='students',
            field=models.ManyToManyField(through='base.TeacherEnrolment', to='base.student'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='subjects',
            field=models.ManyToManyField(through='base.TeacherSubject', to='base.subject'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='teacherName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='StudentSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.subject')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='subjects',
            field=models.ManyToManyField(through='base.StudentSubject', to='base.subject'),
        ),
    ]
