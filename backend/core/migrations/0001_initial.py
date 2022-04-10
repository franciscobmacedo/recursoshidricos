# Generated by Django 4.0.3 on 2022-04-05 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=200)),
                ('nome', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=200)),
                ('nome', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=200)),
                ('codigo', models.CharField(max_length=200)),
                ('nome', models.CharField(max_length=200)),
                ('altitude', models.CharField(max_length=200, null=True)),
                ('latitude', models.CharField(max_length=200, null=True)),
                ('longitude', models.CharField(max_length=200, null=True)),
                ('coord_x', models.CharField(max_length=200, null=True)),
                ('coord_y', models.CharField(max_length=200, null=True)),
                ('bacia', models.CharField(max_length=200, null=True)),
                ('distrito', models.CharField(max_length=200, null=True)),
                ('concelho', models.CharField(max_length=200, null=True)),
                ('freguesia', models.CharField(max_length=200, null=True)),
                ('entidade_responsavel_automatica', models.CharField(max_length=200, null=True)),
                ('entidade_responsavel_convencional', models.CharField(max_length=200, null=True)),
                ('tipo_estacao_automatica', models.CharField(max_length=200, null=True)),
                ('tipo_estacao_convencional', models.CharField(max_length=200, null=True)),
                ('entrada_funcionamento_convencional', models.CharField(max_length=200, null=True)),
                ('entrada_funcionamento_automatica', models.CharField(max_length=200, null=True)),
                ('encerramento_convencional', models.CharField(max_length=200, null=True)),
                ('encerramento_automatica', models.CharField(max_length=200, null=True)),
                ('telemetria', models.BooleanField(max_length=200, null=True)),
                ('estado', models.CharField(max_length=200, null=True)),
                ('indice_qualidade', models.CharField(max_length=200, null=True)),
                ('network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stations', to='core.network')),
            ],
        ),
        migrations.CreateModel(
            name='PSA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='psa', to='core.parameter')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='psa', to='core.station')),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('value', models.FloatField()),
                ('psa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data', to='core.psa')),
            ],
        ),
    ]
