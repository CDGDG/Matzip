# Generated by Django 3.2.5 on 2022-08-19 12:50

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
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', default='정보없음', max_length=11)),
                ('type', models.CharField(db_column='type', default='기타', max_length=16)),
                ('address', models.CharField(db_column='address', max_length=100, null=True)),
                ('phone', models.CharField(db_column='phone', max_length=12, null=True)),
                ('user', models.ForeignKey(db_column='user', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'mz_matzip',
            },
        ),
    ]
