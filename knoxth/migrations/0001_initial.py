# Generated by Django 3.2.2 on 2021-05-06 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Context',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Scope',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permissions', models.IntegerField(choices=[('ACCESS', 2), ('MODIFY', 4), ('DELETE', 8)], default=14)),
                ('context', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scopes.context')),
            ],
        ),
    ]