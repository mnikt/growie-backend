# Generated by Django 5.2.3 on 2025-07-03 00:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0010_event_alter_challenge_period_alter_challenge_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='period',
            field=models.IntegerField(choices=[(0, 'Jednorazowe'), (1, 'Codzienne'), (2, 'Cotygodniowe'), (3, 'Comiesięczne')]),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='type',
            field=models.IntegerField(choices=[(0, 'Kod QR')]),
        ),
        migrations.CreateModel(
            name='Pets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='pets')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamification.user')),
            ],
        ),
    ]
