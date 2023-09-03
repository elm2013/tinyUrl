# Generated by Django 4.2.4 on 2023-09-03 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_url', models.URLField(unique=True)),
                ('tiny_url', models.CharField(max_length=255)),
                ('expiration_date', models.DateTimeField()),
            ],
        ),
    ]