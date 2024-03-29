# Generated by Django 5.0.3 on 2024-03-27 20:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postgres', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.CharField(max_length=255)),
                ('hash', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('alt', models.TextField(blank=True, null=True)),
                ('original_alt', models.TextField(blank=True, null=True)),
                ('gen_alt', models.TextField(blank=True, null=True)),
                ('gen_image_caption', models.TextField(blank=True, null=True)),
                ('ocr', models.TextField(blank=True, null=True)),
                ('before_context', models.TextField(blank=True, null=True)),
                ('after_context', models.TextField(blank=True, null=True)),
                ('additional_context', models.TextField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postgres.book')),
            ],
            options={
                'unique_together': {('book', 'src')},
            },
        ),
    ]
