# Generated by Django 4.2.4 on 2023-12-04 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_userprofile_managers_remove_userprofile_login_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='is_sruff',
            new_name='is_staff',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
    ]