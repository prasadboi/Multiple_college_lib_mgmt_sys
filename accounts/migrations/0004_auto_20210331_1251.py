# Generated by Django 3.1.7 on 2021-03-31 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210331_1225'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='college_id',
            new_name='College',
        ),
    ]