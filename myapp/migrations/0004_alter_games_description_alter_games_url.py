# Generated by Django 5.0.6 on 2024-06-10 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_games'),
    ]

    operations = [
        migrations.AlterField(
            model_name='games',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='games',
            name='url',
            field=models.URLField(blank=True, help_text='Enter your Game website URL', max_length=500, null=True),
        ),
    ]
