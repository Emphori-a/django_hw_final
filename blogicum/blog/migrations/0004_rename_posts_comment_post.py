# Generated by Django 3.2.16 on 2023-11-28 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='posts',
            new_name='post',
        ),
    ]
