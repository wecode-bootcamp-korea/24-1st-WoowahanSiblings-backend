# Generated by Django 3.2.6 on 2021-09-01 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='allergies',
            new_name='allergy',
        ),
    ]
