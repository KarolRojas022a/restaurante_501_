from django.db import migrations, models


def mapear_roles_adelante(apps, schema_editor):
    Perfil = apps.get_model('gestion', 'Perfil')
    mapeo = {
        'camarero': 'mesero',
        'gestor': 'gerente',
        'desarrollador': 'contador',
        'staff': 'staff',
    }
    for perfil in Perfil.objects.all():
        nuevo_rol = mapeo.get(perfil.rol, perfil.rol)
        if perfil.rol != nuevo_rol:
            perfil.rol = nuevo_rol
            perfil.save(update_fields=['rol'])


def mapear_roles_atras(apps, schema_editor):
    Perfil = apps.get_model('gestion', 'Perfil')
    mapeo = {
        'mesero': 'camarero',
        'gerente': 'gestor',
        'contador': 'desarrollador',
        'staff': 'staff',
    }
    for perfil in Perfil.objects.all():
        nuevo_rol = mapeo.get(perfil.rol, perfil.rol)
        if perfil.rol != nuevo_rol:
            perfil.rol = nuevo_rol
            perfil.save(update_fields=['rol'])


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0002_perfilusuario'),
    ]

    operations = [
        migrations.RunPython(mapear_roles_adelante, mapear_roles_atras),
        migrations.AlterField(
            model_name='perfil',
            name='rol',
            field=models.CharField(
                choices=[
                    ('mesero', 'Mesero'),
                    ('gerente', 'Gerente'),
                    ('contador', 'Contador'),
                    ('staff', 'Staff'),
                ],
                default='staff',
                max_length=32,
            ),
        ),
    ]
