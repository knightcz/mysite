# Generated by Django 3.0.4 on 2020-04-03 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blog_readed_num'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='readed_num',
            new_name='read_num',
        ),
    ]
