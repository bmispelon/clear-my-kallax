from django.contrib import admin, messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import path

from signups.emails import _get_email_body, send_magic_link_email
from signups.models import Request


class ApprovalStatusFilter(admin.SimpleListFilter):
    title = "approval status"
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('0', "Pending"),
            ('1', "Approved"),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.pending()
        elif self.value() == '1':
            return queryset.approved()


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'ip_address', 'approved']
    date_hierarchy = 'sent_on'
    list_filter = [ApprovalStatusFilter]

    @admin.display(description='Approved', boolean=True, ordering='author__isnull')
    def approved(self, obj):
        return not obj.is_pending

    def get_urls(self):
        return [
            path('approve/<int:object_id>/', self.admin_site.admin_view(self.approve_view), name='signups_request_approve'),
            path('send-link/<int:object_id>/', self.admin_site.admin_view(self.send_magic_link_view), name='signups_request_send_magic_link'),
        ] + super().get_urls()

    def approve_view(self, request, object_id):
        obj = get_object_or_404(Request.objects.pending(), pk=object_id)
        if request.method == 'POST':
            obj.approve()
            messages.success(request, f"Request {obj} was approved successfully")
            return redirect('admin:signups_request_changelist')
        else:
            context = {
                **self.admin_site.each_context(request),
                'object': obj,
                'opts': obj._meta,
            }
            return render(request, 'admin/signups/request/approve.html', context)

    def send_magic_link_view(self, request, object_id):
        obj = get_object_or_404(Request.objects.approved(), pk=object_id)
        if request.method == 'POST':
            send_magic_link_email(request, obj.user)
            messages.success(request, f"Magic link sent to {obj.user.email}")
            return redirect('admin:signups_request_changelist')
        else:
            context = {
                **self.admin_site.each_context(request),
                'object': obj,
                'EMAIL_BODY': _get_email_body(request, obj.user),
                'opts': obj._meta,
            }
            return render(request, 'admin/signups/request/send_magic_link.html', context)
