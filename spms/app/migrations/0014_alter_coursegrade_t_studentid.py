# Generated by Django 4.1.7 on 2023-04-15 20:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_section_t_faculty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursegrade_t',
            name='studentID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]