# Generated manually for modelo Perfil (auth local)

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def crear_perfiles_usuarios_existentes(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Perfil = apps.get_model('gestion', 'Perfil')
    for u in User.objects.all():
        Perfil.objects.get_or_create(
            user=u,
            defaults={
                'rol': 'staff',
                'es_admin': bool(u.is_superuser),
            },
        )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gestion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(choices=[('camarero', 'Camarero'), ('gestor', 'Gestor'), ('desarrollador', 'Desarrollador'), ('staff', 'Staff')], default='staff', max_length=32)),
                ('es_admin', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'PerfilUsuario',
            },
        ),
        migrations.RunPython(crear_perfiles_usuarios_existentes, noop_reverse),
    ]
