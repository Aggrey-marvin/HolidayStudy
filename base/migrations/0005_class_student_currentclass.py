# Generated by Django 4.1.3 on 2022-11-20 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('className', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='currentClass',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='base.class'),
            preserve_default=False,
        ),
    ]
