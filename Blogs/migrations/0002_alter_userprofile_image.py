# Generated by Django 4.1.7 on 2023-05-13 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='profile.png', upload_to='profile_pics'),
        ),
    ]