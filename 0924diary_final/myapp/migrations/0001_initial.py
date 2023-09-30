# Generated by Django 2.2.12 on 2023-09-24 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Diary2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content1', models.TextField()),
                ('content2', models.TextField()),
                ('content3', models.TextField()),
                ('todo1', models.CharField(max_length=200)),
                ('todo2', models.CharField(max_length=200)),
                ('todo3', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
