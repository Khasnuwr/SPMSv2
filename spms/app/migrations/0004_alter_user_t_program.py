# Generated by Django 4.1.7 on 2023-03-28 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_user_t_program'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_t',
            name='program',
            field=models.ForeignKey(blank=True, default='N/A', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.program_t'),
        ),
    ]