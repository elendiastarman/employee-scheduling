from django.conf.urls import patterns, url

from scheduler import views

urlpatterns = patterns('',
    #url(r'^$', views.ScheduleView.as_view(), name='today'),
    #url(r'^(?P<year>\d{4})-(?P<month>\d+)-(?P<day>\d+)$', views.ScheduleView.as_view(), name='otherday')
    url(r'^$', views.schedule_view, name='today'),
    url(r'^admin/$', views.schedule_admin_view, name='schedule_admin'),
    url(r'^(?P<year>\d{4})-(?P<month>\d+)-(?P<day>\d+)$', views.schedule_view, name='otherday'),
    url(r'^term/$', views.term_view, name='term'),
    url(r'^term/(?P<descriptor>\d{5})$', views.term_view, name='otherterm'),
    url(r'^user/(?P<otheruser>\w+)$', views.schedule_view, name='otheruser'),
    url(r'^attendance/$', views.attendance_view, name='attendance'),
    url(r'^attendance/print$', views.attendance_view, name='print_attendance', kwargs={"print":True}),
    url(r'^generate/$', views.generate_view, name='generate'),

    url(r'^sub_requested$', views.sub_request, name='sub_request'),)
