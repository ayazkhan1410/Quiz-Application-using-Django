# Generated by Django 5.0.6 on 2024-06-10 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_quizes_is_challenging_quizes_is_popular'),
    ]

    operations = [
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_name', models.CharField(max_length=100)),
                ('image', models.ImageField(default='questions/default.webp', upload_to='game/')),
                ('url', models.URLField()),
                ('description', models.URLField(blank=True, help_text='Enter your Game website URL', max_length=500, null=True)),
            ],
        ),
    ]
