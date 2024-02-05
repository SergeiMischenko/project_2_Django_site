# Generated by Django 5.0 on 2024-02-03 06:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funnytail', '0004_alter_cats_is_published'),
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='cats',
            name='breed',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='funnytail.breed'),
        ),
    ]