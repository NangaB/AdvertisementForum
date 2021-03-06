# Generated by Django 3.2.13 on 2022-05-18 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=300)),
                ('adress', models.CharField(max_length=400)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=14)),
                ('desc', models.TextField()),
                ('industry', models.CharField(choices=[('', 'Choose industry'), ('nr', 'Nieruchomości'), ('zd', 'Zdrowie'), ('mt', 'Motoryzacja'), ('ft', 'Fitness')], default='', max_length=2)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
