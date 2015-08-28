from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from scheduler.models import *

# Register your models here.
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'telephone', 'email', 'badge_number',
                    'approval_status', 'is_employed')

class ShiftIsOpenFilter(admin.SimpleListFilter):
    title = _('openness')
    parameter_name = 'isOpen'

    def lookups(self, request, model_admin):
        return ((True, _('open')), (False, _('filled')))

    def queryset(self, request, queryset):
        if self.value() not in ('True','False'): return queryset
        
        keep = [q.pk for q in Shift.objects.all() if str(q.is_open)==self.value()]
        return queryset.filter(pk__in=keep)
    
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('position', 'date', 'time_start', 'time_end', 'weekly',
                    'original_worker', 'substitute_worker')
    list_editable = ('original_worker', 'substitute_worker')
    ordering = ('date','time_start','position')
    list_filter = [ShiftIsOpenFilter]
    #list_filter = [is_open]

class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'block', 'default_time_start', 'default_time_end')
    list_editable = ('block', 'default_time_start', 'default_time_end')

class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'descriptor', 'date_start', 'date_end')
    list_editable = ('date_start', 'date_end')

admin.site.register(Worker, WorkerAdmin)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Rank)
admin.site.register(Term, TermAdmin)
