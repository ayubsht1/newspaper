# Generated by Django 5.1.1 on 2024-09-10 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newspaper', '0003_rename_tag_post_tags_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='view_count',
            new_name='views_count',
        ),
    ]