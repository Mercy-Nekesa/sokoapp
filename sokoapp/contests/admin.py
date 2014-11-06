from django.contrib import admin

from .models import TimePeriod


class TimePeriodAdminBase(object):
    list_display = ('name', 'period_start', 'period_end',)


class TimePeriodAdmin(TimePeriodAdminBase, admin.ModelAdmin):
    pass


admin.site.register(TimePeriod, TimePeriodAdmin)
