# Generated by Django 3.2.8 on 2021-10-18 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_auto_20191216_0937'),
        ('users', '0002_alter_user_avatar_alter_user_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='favs',
            field=models.ManyToManyField(blank=True, related_name='favs', to='rooms.Room'),
        ),
    ]