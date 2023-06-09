# Generated by Django 4.1.7 on 2023-05-15 06:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='post',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Blogs.post'),
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(null=True, upload_to='files'),
        ),
    ]
