from django.contrib import admin
from .models import Cliente, Empleado, Mesa, Plato, Orden, DetalleOrden, Factura, Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'es_admin')
    list_filter = ('rol', 'es_admin')
    search_fields = ('user__username',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        u = obj.user
        if obj.es_admin and not u.is_staff:
            u.is_staff = True
            u.save(update_fields=['is_staff'])
        elif not obj.es_admin and u.is_staff and not u.is_superuser:
            u.is_staff = False
            u.save(update_fields=['is_staff'])


admin.site.register(Cliente)
admin.site.register(Empleado)
admin.site.register(Mesa)
admin.site.register(Plato)
admin.site.register(Orden)
admin.site.register(DetalleOrden)
admin.site.register(Factura)

