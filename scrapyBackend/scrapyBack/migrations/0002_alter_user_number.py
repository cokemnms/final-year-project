# Generated by Django 5.2 on 2025-04-10 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapyBack', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='number',
            field=models.CharField(default=False, max_length=15),
        ),
    ]
