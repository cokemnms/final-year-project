# Generated by Django 5.2 on 2025-05-14 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_alter_notification_type_of_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type_of_notification',
            field=models.CharField(choices=[('post_like', 'Post like'), ('post_comment', 'Post comment')], max_length=50),
        ),
    ]
