# Generated by Django 3.2.7 on 2023-05-29 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_article_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='author',
            new_name='authors',
        ),
    ]