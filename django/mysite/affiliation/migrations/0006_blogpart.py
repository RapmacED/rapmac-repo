# Generated by Django 4.1.5 on 2023-01-31 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliation', '0005_blogpost'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('picture', models.ImageField(upload_to='')),
                ('link', models.URLField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateField(blank=True, null=True)),
                ('description', models.TextField(verbose_name='Contenu')),
                ('positive', models.TextField()),
                ('negative', models.TextField()),
            ],
        ),
    ]
