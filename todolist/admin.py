from django.contrib import admin
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.models import Group, Permission
from .models import Request, Detail

mechanics_group, created = Group.objects.get_or_create(name='Mechanics')
if created:
    mechanics_group.permissions.set([
        Permission.objects.get(codename='view_request'),
        Permission.objects.get(codename='add_request'),
        Permission.objects.get(codename='change_request')
    ])

warehouse_group, created = Group.objects.get_or_create(name='Warehouse')
if created:
    warehouse_group.permissions.set([
        Permission.objects.get(codename='view_request'),
        Permission.objects.get(codename='change_request'),
        Permission.objects.get(codename='view_detail'),
        Permission.objects.get(codename='change_detail')
    ])

class RequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'processed_by', 'created_at', 'processed_at')
    actions = ['send_request']

    def send_request(self, request, queryset):
        for obj in queryset:
            # отправить заявку
            # ...
            obj.save()
        self.message_user(request, f"Заявки были отправлены")

    send_request.short_description = "Отправить"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'created_by' and not self.obj:
            kwargs["queryset"] = db_field.related_model.objects.filter(pk=request.user.pk)
            kwargs["disabled"] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def response_change(self, request, obj):
        res = super().response_change(request, obj)
        if '_send_request' in request.POST:
            url = reverse('send_request', args=[obj.pk])
            return HttpResponseRedirect(url)
        return res

    def response_add(self, request, obj, post_url_continue=None):
        res = super().response_add(request, obj, post_url_continue=post_url_continue)
        if '_send_request' in request.POST:
            url = reverse('send_request', args=[obj.pk])
            return HttpResponseRedirect(url)
        return res

admin.site.register(Request, RequestAdmin)
