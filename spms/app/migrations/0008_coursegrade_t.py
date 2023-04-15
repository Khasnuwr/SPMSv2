# Generated by Django 4.1.7 on 2023-04-15 18:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_evaluation_t'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseGrade_T',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eduYear', models.CharField(max_length=4)),
                ('eduSemester', models.CharField(max_length=25)),
                ('section', models.IntegerField(default=1)),
                ('grade', models.CharField(max_length=4)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.course_t')),
                ('studentID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]