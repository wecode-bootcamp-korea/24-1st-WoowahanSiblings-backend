# Generated by Django 3.2.6 on 2021-09-01 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=45)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=40)),
                ('address', models.CharField(max_length=200)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('NA', 'Not Available')], max_length=10)),
                ('date_of_birth', models.DateField()),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
