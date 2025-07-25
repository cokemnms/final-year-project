# Generated by Django 5.1.7 on 2025-05-15 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='max_price',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Optional maximum price limit a bidder can bid.', max_digits=12, null=True),
        ),
    ]
