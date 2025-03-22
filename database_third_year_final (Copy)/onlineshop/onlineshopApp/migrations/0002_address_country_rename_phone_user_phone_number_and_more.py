# Generated by Django 5.1.3 on 2025-03-16 16:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineshopApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RenameField(
            model_name='user',
            old_name='phone',
            new_name='phone_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='city',
        ),
        migrations.RemoveField(
            model_name='user',
            name='district',
        ),
        migrations.RemoveField(
            model_name='user',
            name='postal_code',
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlineshopApp.address'),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlineshopApp.country')),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlineshopApp.city')),
            ],
        ),
        migrations.CreateModel(
            name='Postcode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlineshopApp.district')),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='postcode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlineshopApp.postcode'),
        ),
    ]
