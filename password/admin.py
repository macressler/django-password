from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Q

from forms import PasswordForm
from models import Password

class PasswordAdmin(admin.ModelAdmin):
    form = PasswordForm
    list_display = ('__unicode__', 'domain', 'is_public')
    list_filter = ('group',)
    search_fields = ['name', 'username', 'domain']

    def get_form(self, request, obj=None, **kwargs):
         form = super(PasswordAdmin, self).get_form(request, obj, **kwargs)
         form.current_user = request.user
         return form

    def queryset(self, request):
        user = getattr(request, 'user', None)
        qs = super(PasswordAdmin, self).queryset(request)
        if user.is_superuser:
            return qs
        return qs.filter(Q(user=user) | Q(group=Group.objects.filter(user=user))).distinct()

admin.site.register(Password, PasswordAdmin)

