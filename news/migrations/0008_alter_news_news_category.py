# Generated by Django 3.2.25 on 2024-07-05 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_news_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='news_category',
            field=models.CharField(choices=[('SİYASİ', 'Siyasi'), ('EKONOMİ', 'Ekonomi'), ('TEKNOLOJİ', 'Teknoloji'), ('DÜNYA', 'Dünya')], max_length=50, verbose_name='Haberin Kategorisi'),
        ),
    ]
