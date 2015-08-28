from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views import generic

import django.contrib.auth.forms as authForms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
create_user = User.objects.create_user
from django.template import Context, RequestContext

from django.forms.models import model_to_dict, fields_for_model
from django.db.models import Q
from django.utils.datastructures import SortedDict

import datetime
from datetime import date, timedelta
today = datetime.date.today
from django.utils import timezone

import random

from scheduler.models import *
from scheduler.forms import *

is_staff = lambda user: user.is_staff
is_active = lambda user: user.is_active

# Create your views here.
def blank_view(request, **kwargs):
    if request.user.is_anonymous():
        return redirect('login')
    else:
        return redirect('home')

@login_required
def home_view(request, **kwargs):

    context = RequestContext(request)
    if 'context' in kwargs:
        context.update(kwargs['context'])

    mod_pk = -1
    if request.user.is_staff:
        if 'edit' in request.GET:
            mod_pk = request.GET['edit']
            context['edit'] = True
        elif 'delete' in request.GET:
            mod_pk = request.GET['delete']

        try:
            instance = Announcement.objects.get(pk=mod_pk)
        except ObjectDoesNotExist:
            instance = None

    try:
        all_unit_anns = Announcement.objects.filter(
            unit__short_name=request.session['current_unit']
        ).exclude(pk=mod_pk).order_by('kind')
    except KeyError:
        
        return render(request, 'scheduler/home.html', context)
##    all_unit_anns = all_unit_anns.filter(kind='Al') | all_unit_anns.filter(kind='No') | all_unit_anns.filter(kind='An')

##    if request.user.is_staff:
##        for ann in all_unit_anns.filter(date_to_delete__lte = today()):
##            ann.delete()

    context['announcements'] = all_unit_anns.filter(date_to_delete__gt = today())
    print(context['announcements'])

    if request.user.is_staff:
        ##add announcement form##
        if request.method == 'POST' and 'add announcement' in request.POST:
##            print("This should work...?")
            if 'edit' not in request.GET or not instance:
                add_announcement_form = AddAnnouncementForm(request.POST, request.FILES)
            else:
                add_announcement_form = AddAnnouncementForm(request.POST, request.FILES, instance=instance)

            if add_announcement_form.is_valid():
##                print("form is valid")
                new_ann = add_announcement_form.save(commit=False)
                try:
                    new_ann.unit
                except ObjectDoesNotExist:
                    new_ann.unit = Unit.objects.get(short_name=request.session['current_unit'])
                new_ann.save()
##                add_announcement_form = AddAnnouncementForm()
##                request.GET.pop('edit')
                return redirect(reverse('home'))
        else:
            if 'edit' in request.GET and instance:
                add_announcement_form = AddAnnouncementForm(instance=instance)
##                context['edit'] = True
            else:
                if 'delete' in request.GET and instance:
                    instance.delete()
                add_announcement_form = AddAnnouncementForm()
        context['add_announcement_form'] = add_announcement_form

        ##users to approve##
        users = User.objects.filter(is_active=True,
                                    worker__isnull=False,
                                    worker__is_approved=False)
        users = list(users)
        
        i = 0
        while i < len(users):
            try:
                u_s = users[i].worker.unitstatus_set.get(unit__short_name=request.session['current_unit'])

                if u_s.work_status != 'AA':
                    users.pop(i)
                else:
                    i += 1
            except ObjectDoesNotExist:
                users.pop(i)

        context['users_to_approve'] = users

        ##shifts to approve##
        shifts = Shift.objects.filter(status__in=['Sr','SR'],
                                      unit__short_name=request.session['current_unit']
                                      )#.order_by('date_start', 'time_start', 'position__name')
        list_of_shifts = []
        for shift in shifts:
            for weekNum in shift.get_sub_weeks():
                date = shift.date_start + timedelta(weeks=weekNum-shift.week_first-1)
                #date_str = "{:%A %B %d, %Y}".format(date)
                list_of_shifts.append({'date': date,
                                       'date_str': shift.date_str(weekNum),
                                       'shift': shift,
                                       'weekNum': weekNum})
        list_of_shifts.sort(key=lambda x:x['date'])
        context['shifts_to_approve'] = list_of_shifts

        ##subs to approve##
        subs = Shift.objects.filter(pick_requests__isnull=False,
                                    unit__short_name=request.session['current_unit']
                                    ).distinct().order_by('date_start','time_start','position','pk')
        list_of_subs = []
        for sub in subs:
            pick_requests = []
            for worker in sub.pick_requests.all():
                pick_requests.append( (worker, sub.experience_level(worker)) )
            list_of_subs.append( (sub, pick_requests) )
        context['subs_to_approve'] = list_of_subs

    return render(request, 'scheduler/home.html', context)

@login_required
def schedule_view(request, *args, **kwargs):
    if request.user.is_staff and 'otheruser' not in kwargs:
        return schedule_admin_view(request, *args, **kwargs)
    else:
        return schedule_normal_view(request, *args, **kwargs)

@user_passes_test(is_active)
def schedule_admin_view(request, *args, **kwargs):

    if not request.user.is_staff and request.user.worker.rank.rank != 'Ma':
        return redirect(reverse("scheduler:today"))

    context = {}

    ##date selector
    try:
        year = int(kwargs['year'])
        month = int(kwargs['month'])
        day = int(kwargs['day'])
        theday = datetime.date(year, month, day)
    except KeyError:
        theday = today()

    try:
        term = Term.objects.get(date_start__lte=theday, date_end__gte=theday)
    except ObjectDoesNotExist:
        term = None

    days = {'day_current': theday,
            'day_before': theday - timedelta(days=1),
            'day_after': theday + timedelta(days=1),
            'week_before': theday - timedelta(days=7),
            'week_after': theday + timedelta(days=7),}

    if term:
        days.update({
            'term_start': term.date_start,
            'term_end': term.date_end,
            })

    context.update(days)

    for label, day in days.items():
        context[label+'_str'] = '{:%B %d, %Y}'.format(day).replace('201',"'1")
        context[label+'_url'] = reverse('scheduler:otherday', args=[day.year,day.month,day.day])

    context['day_current_wday'] = theday.weekday()
    context['day_current_weekday'] = '{:%A}'.format(theday)

    if request.method == 'POST':
        form = JumpToDateForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data.get('selected_day').day
            month = form.cleaned_data.get('selected_day').month
            year = form.cleaned_data.get('selected_day').year
            return HttpResponseRedirect(reverse('scheduler:otherday', args=(year,month,day)))
    else:
        form = JumpToDateForm()
        
    context['form'] = form

    shifts = getWeekShifts(theday, request.session['current_unit'])
    mon = theday - timedelta(days=theday.weekday())
    sun = theday + timedelta(days=6)

    weekdays = []
    for k in range(7):
        d = mon+timedelta(days=k)
        day_label = '{:%A}'.format(d)
        day_url = None if d.weekday() == theday.weekday() else reverse('scheduler:otherday', args=[d.year,d.month,d.day])
        weekdays.append( [day_label, day_url] )
    context['wday_names'] = weekdays

    shift_dict = {}

    for shift in shifts:
        label = (shift.position.name, shift.time_start, shift.time_end)
        shift_day = shift.date_start
        while shift_day < mon:
            shift_day += timedelta(days=7)

        if label+(1,) not in shift_dict:
            shift_dict[label+(1,)] = {shift_day: shift}
        else:
            i = 1
            while label+(i,) in shift_dict and shift_day in shift_dict[label+(i,)]:
                i += 1

            if label+(i,) in shift_dict:
                shift_dict[label+(i,)][shift_day] = shift
            else:
                shift_dict[label+(i,)] = {shift_day: shift}

    shift_table = []
    for key in sorted(shift_dict, key=lambda x: (x[1],x[2],x[3],x[0])):
        label = "%s\n"%key[0] + '{:%H:%M}'.format(key[1])+'-'+'{:%H:%M}'.format(key[2])
        shift_table.append([label, []])
##        print(key,shift_dict[key], sep=': ')
        for wday in range(7):
            day = mon+timedelta(days=wday)
            if day in shift_dict[key]:
##                print(key, wday, shift_dict[key][day], sep=';')
                s = shift_dict[key][day]
                shift_table[-1][1].append( (s, s.experience_level(s.worker()))  )
            else:
                shift_table[-1][1].append( None )

    context['shift_table'] = shift_table

    return render(request, 'scheduler/schedule_admin.html', context)

@user_passes_test(is_active)
def schedule_normal_view(request, *args, **kwargs):

    #context = {}
    context = RequestContext(request)

    if 'context' in kwargs:
        context.update(kwargs['context'])

    if 'otheruser' in kwargs:
        user = User.objects.get(username=kwargs['otheruser'])
    else:
        user = request.user

    today = datetime.date.today()
    term = Term.objects.get(date_start__lte=today, date_end__gte=today)

    try:
        worker = user.worker
        req_worker = request.user.worker
    except ObjectDoesNotExist:
        worker = None
        req_worker = None

    context['worker'] = worker

    shifts = Shift.objects.filter(
        Q(original_worker=worker)|Q(substitute_worker=worker),
        date_start__gte=term.date_start, date_end__lte=term.date_end,
        unit__short_name = request.session['current_unit'],
        ).order_by('date','time_start')

    context['shift_list'] = shifts

    weekly_shifts = shifts.filter(weekly=True)
    day_shifts = shifts.filter(weekly=False)

    ###figure out a more efficient way###
    ds = term.date_start
    de = term.date_end
    delta = 0
    date = ds + timedelta(days=delta)

##    print()
##    print(today(), ds)
##    print((today()-ds).seconds)
##    print()
    context['current_week'] = (datetime.date.today()-ds).days//7 + 1

    days = []
    weeks = []

    while date <= de:
        weekday_str = '{:%A}'.format(date)
        date_str = '{:%B %d, %Y}'.format(date)

        week_s = weekly_shifts.filter(date__week_day=(date.weekday()+2)%7)
        day_s = day_shifts.filter(date=date)
        date_shifts = (week_s|day_s).order_by('time_start', 'pk')

        if date_shifts:
            shift_info = []
            for d_s in date_shifts:
                if not (d_s.date_start <= date <= d_s.date_end): continue
                if not d_s.is_owned(worker): continue
                
                rerequest = d_s.status == 'Sd'
                button_is_visible, button_message = d_s.is_submit_button_visible(req_worker)
                    
                shift_info.append( (d_s,
                                    {'attr_list': [str(d_s.position),
                                                   d_s.time_str(),
                                                   ("Yes" if d_s.weekly else "No"),
                                                   #"%s"%d_s.original_worker,
                                                   #"%s"%d_s.substitute_worker,
                                                   ],
                                     'submittable': d_s.can_submit(worker, delta//7+1)[0],
                                     'rerequest': rerequest,
                                     'button_is_visible': button_is_visible,
                                     'button_message': button_message,
                                     }
                                    ) )

            if shift_info:
                days.append( (weekday_str, date_str, shift_info) )
        
        delta += 1
        #date = ds + timedelta(days=delta)
        date = date + timedelta(days=1)

        if delta%7 == 0 and days:
            total_time = sum(getWeekShifts(date-timedelta(days=1),
                                           request.session['current_unit'],
                                           worker),
                             timedelta())
            total_hours = total_time.seconds/3600
            weeks.append( (delta//7, total_hours, days) )
            days = []

    if days:
        total_time = sum(getWeekShifts(date,
                                       request.session['current_unit'],
                                       worker),
                         timedelta())
        total_hours = total_time.seconds/3600
        weeks.append( (delta//7+1, total_hours, days) )

    context['weeks'] = weeks

    return render(request, 'scheduler/schedule_normal.html', context)

@user_passes_test(is_active)
def sub_request(request, *args, **kwargs):

    context = RequestContext(request)

    if request.method == 'POST':
        for arg in request.POST:
            if 'shift_' in arg:
                shift_pk, weekNum = map(int, arg[6:].split('_'))
                
                shift = Shift.objects.get(pk=shift_pk)
                if shift.status == 'Sd':
                    shift.status = 'SR' #sub re-requested
                elif shift.status in ['F', 'Sa']:
                    if request.user.worker.rank.rank == 'Ma':
                        shift.status = 'Sa'
                    else:
                        shift.status = 'Sr' #sub requested
                    
                shift.add_sub_week(weekNum)
                shift.save()
                
                context['shift'] = shift
                context['date'] = shift.date_str(weekNum)
                context['action'] = 'request'

                return schedule_normal_view(request, context=context)

    return redirect(reverse('scheduler:today'))

def attendance_view(request, *args, **kwargs):

    if not request.user.is_staff and request.user.worker.rank.rank != 'Ma':
        return redirect(reverse('scheduler:today'))

    context = RequestContext(request)

    if 'print' in kwargs and kwargs['print']: context['print'] = True
    context['date'] = "{:%A, %B %d, %Y}".format(today())

    shifts = getWeekShifts(today(), request.session['current_unit'], singleDay=True)
    shifts = list(shifts)
    shifts.sort(key=lambda s: s.time_start)

    shifts_info = []
    block = ""

    for s in shifts:
        block_name = str(s.position.block)
        if block != block_name:
            shifts_info.append( (None,block_name) )
            block = block_name
        
        attrs = {'position': s.position.name,
                 'name': str(s.worker()) if s.worker() else "___",
                 'time': s.time_str(),
                 'hours': str(s.time_span())[:-3],
                 }

        reqWorker = s.worker() or request.user.worker
        
        try: #checks for existence of presence acknowledgement
            r = Record.objects.get(category='I',
##                                   worker=reqWorker,
                                   info='Attendance:%d'%s.pk,
                                   time_added__year=today().year,
                                   time_added__month=today().month,
                                   time_added__day=today().day,)
        except ObjectDoesNotExist:
            
            if request.method == 'POST' and "c_%d"%s.pk in request.POST.getlist('is_present'):
                r = Record(category='I',
                           worker=reqWorker,
                           info='Attendance:%d'%s.pk)
                r.save()
                attrs['present'] = True
            else:
                attrs['present'] = False
                
        else:
            if request.method == 'POST' and "c_%d"%s.pk not in request.POST.getlist('is_present'):
                r.delete()
                attrs['present'] = False
            else:
                attrs['present'] = True

        try: #checks for existence of attendance note
            r = Record.objects.get(category='I',
##                                   worker=reqWorker,
                                   info='Attendance note:%d'%s.pk,
                                   time_added__year=today().year,
                                   time_added__month=today().month,
                                   time_added__day=today().day,)
        except ObjectDoesNotExist:
            
            if request.method == 'POST' and request.POST['n_%d'%s.pk] != '':
                r = Record(category='I',
                           worker=reqWorker,
                           info='Attendance note:%d'%s.pk,
                           note=request.POST['n_%d'%s.pk],)
                r.save()
                attrs['note'] = r.note
            else:
                attrs['note'] = ""
                
        else:
            if request.method == 'POST' and request.POST['n_%d'%s.pk] == '':
                r.delete()
                attrs['note'] = ""
            elif request.method == 'POST':
                attrs['note'] = r.note = request.POST['n_%d'%s.pk]
            else:
                attrs['note'] = r.note
        
        shifts_info.append( (s, attrs) )

    context['shifts'] = shifts_info

    add = '_table' if 'print' in kwargs and kwargs['print'] else ''

    return render(request, 'scheduler/attendance'+add+'.html', context)

def generate_view(request, *args, **kwargs):

    context = RequestContext(request)

    term_options = SortedDict()
    for term in Term.objects.filter(date_end__gte=today()).order_by('date_start'):
##        print(term)
        term_options[term.descriptor] = term.name

    print(term_options)

    wdays = ['M','T','W','R','F','S','U']
    weekdays = []
    for wday in wdays:
        weekdays.append({'N':wday, 'n':wday.lower()})

    positions = []
    available_positions = Position.objects.all().order_by('block__rank','default_time_start')

    if request.method == 'POST':
        is_valid = True

##        for arg in request.POST:
##            print(arg, request.POST[arg])

        #term option
        if 'term_option' not in request.POST or request.POST['term_option'] not in term_options:
            context['term_option_error'] = "Please pick one of the terms in the list."
            is_valid = False
        else:
            context['term_selected'] = term_selected = request.POST['term_option']

        #date ranges
        date_range_blocks = []
        
        k = 1
        while "sd"+str(k) in request.POST:
            values = {}
            dates_and_times = {}
            empties = 0
            
            for prefix in ["sd","st","ed","et"]:
                arg_name = prefix + str(k)
                value = request.POST[arg_name]
                
                values[prefix] = value

                if value == '':
                    empties += 1

                if value and prefix[1] == 'd': #date validation
                    try:
                        if '/' in value:
                            m, d, y = map(int, value.split('/'))
                        else:
                            y, m, d = map(int, value.split('-'))
                        if y < 1000:
                            y += 2000
                        dates_and_times[prefix] = datetime.date(y,m,d)
                    except (TypeError, ValueError):
                        values[prefix+"_error"] = "Please enter a valid date."
                        is_valid = False

                if value and prefix[1] == 't': #time validation
                    try:
                        if ' ' in value:
                            hhmm, apm = value.split(' ')
                        else:
                            hhmm, apm = value, ''
                        hh, mm = map(int, hhmm.split(':'))
                        if apm:
                            if apm.lower().replace('.','') not in ['am','pm']:
                                values[prefix+"_error"] = "Please enter a valid time."
                                is_valid = False
                            elif apm.lower().replace('.','') == 'pm' and hh != 12:
                                hh += 12
                            elif apm.lower().replace('.','') == 'am' and hh == 12:
                                hh -= 12
                        dates_and_times[prefix] = datetime.time(hh,mm)
                    except (TypeError, ValueError):
                        values[prefix+"_error"] = "Please enter a valid time."
                        is_valid = False
                    
            if empties and (k == 1 or (k > 1 and empties != 4)):
                values['block_error'] = "Please fill in all blanks."
                is_valid = False

            if is_valid: #more in-depth date validation
                if dates_and_times['ed'] < dates_and_times['sd']: #end date is earlier than start date
                    values['ed_error'] = "End date must be no earlier than start date."
                    is_valid = False
                elif dates_and_times['ed'] == dates_and_times['sd']: #same day
                    if dates_and_times['et'] <= dates_and_times['st']:
                        values['et_error'] = "End time must be later than start time."
                        is_valid = False
                elif dates_and_times['sd'] < Term.objects.get(descriptor=term_selected).date_start:
                    values['sd_error'] = "Start date must be no earlier than term start."
                    is_valid = False
                elif dates_and_times['ed'] > Term.objects.get(descriptor=term_selected).date_end:
                    values['ed_error'] = "End date must be no later than term end."
                    is_valid = False

            if k == 1 or empties < 4:
                date_range_blocks.append( (values,dates_and_times) )
                
            k += 1

        #weekdays
        if request.POST.getlist("weekdays"):
            for wday in request.POST.getlist("weekdays"):
                weekdays[wdays.index(wday.upper())]['checked'] = True
        else:
            context['no_weekdays_selected_error'] = "At least one weekday must be selected."
            is_valid = False

        #positions
        for position in available_positions:
            positions.append({'display':str(position),
                              'num':request.POST[str(position)],
                              'name':position.name,
                              'block':str(position.block),
                              'dts':position.default_time_start,
                              'dte':position.default_time_end,
                              })
            if not positions[-1]['num'].isdigit() or not (0 <= int(positions[-1]['num']) <= 9):
                positions[-1]['error'] = "Please enter an integer between 0 and 9 (inclusive)."

        #were all inputs valid?
        if not is_valid:
            context['error_message'] = "Please fix any and all errors and try again."
        else:
            num_shifts = generate_shifts(request,
                                         term_selected,
                                         date_range_blocks,
                                         weekdays,
                                         available_positions,
                                         )

            if num_shifts < 0:
                context['error_message'] = "Something went wrong but I don't know what. \
                                            Please recheck your inputs and try again."
            elif num_shifts == 0:
                context['error_message'] = "No shifts were created."
            else:
                context['success_message'] = "%s shifts were created!" % num_shifts

                #reset forms
                context['term_selected'] = ''
                date_range_blocks = [{'sd':'','st':'','ed':'','et':''}]
                for wday in weekdays:
                    if 'checked' in wday: wday.pop('checked')
                for position in positions:
                    position['num'] = 0
            
    else:
        date_range_blocks = [{'sd':'','st':'','ed':'','et':''}]
        
        for position in available_positions:
            positions.append({'display':str(position),
                              'num':0,
                              'name':position.name,
                              'block':str(position.block),
                              'dts':position.default_time_start,
                              'dte':position.default_time_end,
                              })


    context['term_options'] = term_options
    context['date_range_blocks'] = date_range_blocks
    context['weekdays'] = weekdays
    context['positions'] = positions

    return render(request, 'scheduler/generate.html', context)

def generate_shifts(request, term_selected, date_range_blocks, weekdays, available_positions):
    unit = Unit.objects.get(short_name=request.session['current_unit'])
    term = Term.objects.get(descriptor=term_selected)
    
    positions_to_use = []
    for position in available_positions:
        if str(position) in request.POST:
            positions_to_use.append( [position, int(request.POST[str(position)])] )

    num_shifts = 0

    for drb in date_range_blocks:
        dat = drb[1]
        date = dat['sd']
        k = 0
        weekly = True if (dat['ed']-dat['sd']).days//7 >= 1 else False
        
        while date <= dat['ed'] and k < 7:

            if 'checked' in weekdays[date.weekday()]:
                for position, num in positions_to_use:
                    if date == dat['ed'] and position.default_time_end > dat['et']: #check end
                        continue
                    
                    sd = date
                    if date == dat['sd'] and position.default_time_start < dat['st']: #check beginning
                        sd += timedelta(days=7)
                    
                    ed = sd
                    while ed <= dat['ed']-timedelta(days=7):
                        ed += timedelta(days=7)
                    if position.default_time_end > dat['et']:
                        ed -= timedelta(days=7)

                    if ed >= sd:
                        for n in range(num):
                            s = Shift(unit=unit,
                                      term=term,
                                      position=position,
                                      date_start=sd,
                                      date_end=ed,
                                      weekly=weekly,
                                      time_start=position.default_time_start,
                                      time_end=position.default_time_end,
                                      )
                            s.save()
                            num_shifts += 1

            k += 1
            date += timedelta(days=1)
            
    return num_shifts

@user_passes_test(is_staff)
def term_view(request, *args, **kwargs):

    context={}

    if 'descriptor' in kwargs:
        _descriptor = kwargs.get('descriptor')
        try:
            term = Term.objects.get(descriptor__exact=_descriptor)
        except ObjectDoesNotExist:
            raise Http404
    else:
        try:
            today = date.today()
            term = Term.objects.filter(date_start__lte=today).filter(date_end__gte=today)[0]
        except ObjectDoesNotExist:
            raise Http404
        except IndexError: #meaning that the term doesn't exist
            raise Http404

    context['shift_list'] = Shift.objects.filter(
        date__range=(term.date_start, term.date_end)
    ).order_by('date','time_start','position')

    if request.method == 'POST':
        form = SelectPositions(request.POST)
        if form.is_valid():

            if '_clear' in request.POST:
                for position in form.cleaned_data.get('selected_positions'):
                    context['shift_list'].filter(position__exact=position).delete()
                    
            elif '_generate' in request.POST:
                for position in form.cleaned_data.get('selected_positions'):
                    #weeklys first
                    start_date = term.date_start
                    for day_off in range(7):
                        if random.randint(0,1): #weekly
                            Shift.objects.get_or_create(
                                date=term.date_start + timedelta(days=day_off),
                                weekly=1,
                                position = position
                            )
                        else: #single day
                            week = 0
                            offset = timedelta(days=day_off, weeks=week)
                            
                            while term.date_start + offset <= term.date_end:
                                Shift.objects.get_or_create(
                                    date=term.date_start + offset,
                                    weekly=0,
                                    position = position
                                )

                                week += 1
                                offset = timedelta(days=day_off, weeks=week)

    else:
        form = SelectPositions()
    context['form'] = form

    return render(request, 'scheduler/term.html', context)

@user_passes_test(is_active)
def sublist_view(request, **kwargs):

    context = RequestContext(request)
    if 'context' in kwargs:
        context.update(kwargs['context'])

    if 'otheruser' in kwargs:
        user = User.objects.get(username=kwargs['otheruser'])
    else:
        user = User.objects.get(username=request.user.username)

    if 'open' not in context:
        if 'open' in request.GET and request.GET['open'] in ['True','true']:
            context['open'] = True
        else:
            context['open'] = False

    if context['open']:
        statuses_to_show = ['O'] #shows open shifts
    else:
        statuses_to_show = ['So', 'Sa'] #shows sub shifts

    if 'weekly' not in context:
        if 'weekly' in request.GET and request.GET['weekly'] in ['True','true']:
            context['weekly'] = True
        else:
            context['weekly'] = False
    
    today = datetime.date.today()

    last_monday = today - timedelta(days=today.weekday())
    weekday_tabs = ['{:%A} {:%a}'.format(*[last_monday + timedelta(days=k)]*2).split(' ') for k in range(7)]
    weekdays, wdays = zip(*weekday_tabs)
    context['weekday_tabs'] = weekday_tabs

    if 'current' not in context:
        if 'weekday' in kwargs:
            current = wdays.index(kwargs['weekday']) #weekday should be of the form Sun, Mon, etc.
        else:
            current = today.weekday()
        context['current'] = wdays[current]
    else:
        current = wdays.index(context['current'])

    term = Term.objects.get(date_start__lte=today, date_end__gte=today)
    try:
        worker = user.worker
    except ObjectDoesNotExist:
        worker = user

    shifts = Shift.objects.filter(date_start__gte = term.date_start,
                                  date_end__lte = term.date_end,
                                  status__in = statuses_to_show,
                                  unit__short_name=request.session['current_unit'],
                                  date_start__week_day = (current+2)%7,
                                  weekly = context['weekly'])

    try:
        if request.user.worker.rank.rank == 'SE':
            shifts = shifts.exclude(original_worker__rank__rank='Ma')
    except ObjectDoesNotExist:
        pass

    context['shift_list'] = shifts

    if context['open'] and context['weekly']:
        shifts = shifts.order_by('time_start', 'position', 'pk')
    else:
        shifts = shifts.order_by('date_start', 'time_start', 'position', 'pk')

    weeks = []
        
    if shifts:
        shift_info = []
        
        for k, s in enumerate(shifts):
            button_is_visible, button_message = s.is_pickup_button_visible(worker)
                
            shift_info.append( (s,
                                {'attr_list': ['{:%B %d}'.format(s.date_start),
                                               str(s.position),
                                               s.time_str(),],
                                 'pickupable': s.can_pickup(worker)[0],
                                 'button_is_visible': button_is_visible,
                                 'button_message': button_message,
                                 }
                                ) )

            if context['open']:
                if s.weekly:
                    shift_info[-1][-1]['attr_list'].append(
                        ', '.join(map(str, range(s.week_first+1, s.week_last+2))) )
            else:
                shift_info[-1][-1]['attr_list'].append( s.worker )

            if k+1 < len(shifts) and s.week_first != shifts[k+1].week_first:
                weeks.append( (s.week_first+1, SortedDict(shift_info)) )
                shift_info = []

        weeks.append( (s.week_first+1, SortedDict(shift_info)) )

    context['weeks'] = SortedDict(weeks)

    return render(request, 'scheduler/sublist.html', context)

@user_passes_test(is_active)
def shift_request(request, **kwargs):
    
    context = RequestContext(request)
    more_context = {}

    if request.method == 'POST':

        for word in [('open',eval),('weekly',eval),('current',str)]:
            if word[0] in request.POST:
                context[word[0]] = word[1](request.POST[word[0]])

        for arg in request.POST:
            if 'shift_' in arg:
                shift_pk, worker_pk = map(int, arg[6:].split('_'))
                
                shift = Shift.objects.get(pk=shift_pk)
                worker = Worker.objects.get(pk=worker_pk)

                print(shift.worker(), worker)

                if shift.worker() != worker:
                    if worker.rank.rank == 'Ma':
                        shift.status = 'F'
                        shift.substitute_worker = worker
                        shift.save()
                    
                    else:
                        if shift not in worker.pick_requests.all():
                            shift.pick_requests.add(worker)
                        context['action'] = 'request'
                else:
                    shift.status = 'F'
                    shift.pick_requests.clear()
                    shift.save()
                    context['action'] = 'takeback'
                
                context['shift'] = shift
                context['date'] = shift.date_str()

                return sublist_view(request, context=context)#, more=more_context)

    return redirect(reverse('sublist'))

@user_passes_test(is_staff)
def users_view(request, **kwargs):

    context = RequestContext(request)

    short_names = [unitstatus.unit.short_name for unitstatus in request.user.worker.unitstatus_set.all()]

    users = []
    for user in User.objects.filter(is_active=True, is_staff=False):
        try:
            w = user.worker
        except ObjectDoesNotExist:
            pass
        else:
            if user.worker.unitstatus_set.filter(unit__short_name__in=short_names).exists():
                users.append(user)

    context['users'] = users

    return render(request, 'scheduler/users.html', context)

@user_passes_test(is_staff)
def addeditdelete_view(request, *args, **kwargs):

    if 'obj' not in kwargs:
        return redirect(reverse('aed_positions'))

    context = RequestContext(request)
    unit = Unit.objects.get(short_name=request.session['current_unit'])

    if kwargs['obj'] == 'positions':

        context['action'] = "Add"
        fields = ['name','block','description','time_start','time_end']
        context['block_list'] = Block.objects.filter(unit=unit).order_by('rank')
        POSTargs = {}

        if request.method == 'GET':
            if 'delete' in request.GET:
                try:
                    position = Position.objects.get(pk=request.GET['delete'])
                except ObjectDoesNotExist:
                    return redirect(reverse('aed_positions'))
##                except MultipleObjectsReturned:
##                    i = 0
##                    for term in Term.objects.filter(unit=unit,descriptor=request.GET['delete']):
##                        term.descriptor = "%05d" % i
##                        term.save()
##                        i += 1
##                    context['error_message'] = "Uh-oh! More than one term had the same descriptor! Please fix this error immediately."
                else:
                    if position.shift_set.count() > 0:
                        context['error_message'] = "This position may not be deleted as it has shifts with it."
                    else:
                        position.delete()
                        context['success_message'] = "Position was successfully deleted!"
            
            elif 'edit' in request.GET or 'copy' in request.GET:
                if 'edit' in request.GET:
                    p_pk = request.GET['edit']
                else:
                    p_pk = request.GET['copy']
                    
                try:
                    p = Position.objects.get(pk=p_pk)
                except ObjectDoesNotExist:
                    context['error_message'] = "I'm sorry, but that position appears not to exist."
##                except MultipleObjectsReturned:
##                    i = 0
##                    for term in Term.objects.filter(unit=unit,descriptor=request.GET['edit']):
##                        term.descriptor = "%05d" % i
##                        term.save()
##                        i += 1
##                    context['error_message'] = "Uh-oh! More than one term had the same descriptor! Please fix this error immediately."
                else:
                    context['apf_name'] = p.name
                    context['apf_description'] = p.description
                    context['apf_block'] = p.block
                    context['apf_time_start'] = "{:%I:%M %p}".format(p.default_time_start)
                    context['apf_time_end'] = "{:%I:%M %p}".format(p.default_time_end)

                    if 'edit' in request.GET: context['action'] = "Save"

        if request.method == 'POST':
            is_valid = True
            
            if 'name' in request.POST and request.POST['name'] == '':
                is_valid = False
                context['name_error'] = "Please enter a name."
            elif 'name' not in request.POST:
                is_valid = False
                context['name_error'] = "Invalid input."
            if 'description' not in request.POST:
                is_valid = False
                context['description_error'] = "...invalid input."
            if 'block' not in request.POST or request.POST['block'] == '':
                    is_valid = False
                    context['block_error'] = "Please select a block."
            else:
                try:
                    block = Block.objects.get(pk=request.POST['block'])
                except ObjectDoesNotExist:
                    is_valid = False
                    context['block_error'] = "Please select a valid block."
            
            if 'time_start' in request.POST and request.POST['time_start'] == '':
                is_valid = False
                context['time_start_error'] = "Please enter a start time."
            elif 'time_start' not in request.POST:
                is_valid = False
                context['time_start_error'] = "Once again, that's invalid input."
            if 'time_end' in request.POST and request.POST['time_end'] == '':
                is_valid = False
                context['time_end_error'] = "Please enter an end time."
            elif 'time_end' not in request.POST:
                is_valid = False
                context['time_end_error'] = "C'mon! Invalid input!"

            #might have to fix POST input
            for arg in fields:
                if arg not in request.POST:
                    POSTargs[arg] = ''
                else:
                    POSTargs[arg] = request.POST[arg]


            if is_valid: #non-duplicate check
                try:
                    Position.objects.get(name=request.POST['name'],block=block)
                except ObjectDoesNotExist:
                    pass
                else:
                    is_valid = False
                    context['block_error'] = "Two positions may not have the same name and block."

            if is_valid: #check that times are formatted correctly
                ts = request.POST['time_start']
                te = request.POST['time_end']

                try:
                    apm = ""
                    if ' ' in ts:
                        hhmm, apm = ts.split(' ')
                    else:
                        hhmm = ts
                    if apm and apm.lower().replace('.','') not in ['am','pm']: raise ValueError("Invalid ending")
                    hh,mm = map(int, hhmm.split(':'))
                    if apm.lower().replace('.','') == 'pm' and hh != 12:
                        hh += 12
                    elif apm.lower().replace('.','') == 'am' and hh == 12:
                        hh -= 12
                    time_start = datetime.time(hh,mm)
                except (TypeError, ValueError) as e:
                    context['time_start_error'] = "Please enter a valid time."
                    is_valid = False
                    raise e
                    
                try:
                    apm = ""
                    if ' ' in te:
                        hhmm, apm = te.split(' ')
                    else:
                        hhmm = te
                    if apm and apm.lower().replace('.','') not in ['am','pm']: raise ValueError("Invalid ending")
                    hh,mm = map(int, hhmm.split(':'))
                    if apm.lower().replace('.','') == 'pm' and hh != 12:
                        hh += 12
                    elif apm.lower().replace('.','') == 'am' and hh == 12:
                        hh -= 12
                    time_end = datetime.time(hh,mm)
                except (TypeError, ValueError) as e:
                    context['time_end_error'] = "Please enter a valid time."
                    is_valid = False

            if is_valid: #deeper time validation
                if time_end.hour > 2 and time_end <= time_start:
                    context['time_end_error'] = "End time must be later than start time."
                    is_valid = False

            if not is_valid:
                for arg in fields:
                    context['apf_'+arg] = POSTargs[arg]
                context['error_message'] = "Please fix any and all errors and try again."
                
            else:
                name = request.POST['name'].capitalize()
                description=request.POST['description']

                if request.POST['submit'] == "Add position":
                    try:
                        Position(name=name,
                                 description=description,
                                 block=block,
                                 default_time_start=time_start,
                                 default_time_end=time_end,
                                 ).save()
                        
                    except (TypeError, ValueError) as e:
                        for arg in fields:
                            context['apf_'+arg] = POSTargs[arg]
                        context['error_message'] = "Something went wrong and I don't know what. Please recheck your input and try again.\n%s"%e
                        
                    else:
                        context['success_message'] = "Position was successfully created!"
                            
                elif request.POST['submit'] == "Save term":
                    try:
                        position = Position.objects.get(pk=request.GET['edit'])
                        
                    except (TypeError, ValueError) as e:
                        for arg in fields:
                            context['apf_'+arg] = POSTargs[arg]
                        context['error_message'] = "Something went wrong and I don't know what. Please recheck your input and try again.\n%s"%e

##                    except MultipleObjectsReturned:
##                        for arg in fields:
##                            context['apf_'+arg] = request.POST[arg]
##                        context['atf_descriptor'] = '00000'
##                        context['error_message'] = "Uh-oh! More than one term had the same descriptor! Please fix this error immediately."
                        
                    else:
                        position.name = name
                        position.block = block
                        position.description = description
                        position.default_date_start = time_start
                        position.default_date_end = time_end
                        position.save()
                        
                        context['success_message'] = "Term was successfully saved!"

        if 'apf_block' in context and type(context['apf_block']) == str and context['apf_block'].isdigit():
            try:
                context['apf_block'] = Block.objects.get(pk=context['apf_block'])
            except:
                context['apf_block'] = ''

        positions = Position.objects.filter(block__unit=unit).order_by('block__rank','default_time_start','default_time_end')
        context['position_list'] = positions
        
    elif kwargs['obj'] == 'blocks':

        context['action'] = "Add"

        if request.method == 'GET':
            if 'delete' in request.GET:
                try:
                    Block.objects.get(unit=unit, rank=request.GET['delete']).delete()
                except ObjectDoesNotExist:
                    return redirect(reverse('aed_blocks'))
                except MultipleObjectsReturned:
                    i = 0
                    for block in Block.objects.filter(unit=unit,rank=request.GET['delete']):
                        block.rank = 999-i
                        block.save()
                        i += 1
                    context['error_message'] = "Uh-oh! More than one block had the same rank! Please fix this error immediately."
                else:
                    context['success_message'] = "Block was successfully deleted!"
                    for b in Block.objects.filter(unit=unit,rank__gt=request.GET['delete']):
                        b.rank -= 1
                        b.save()
            
            elif 'edit' in request.GET:
                try:
                    b = Block.objects.get(unit=unit, rank=request.GET['edit'])
                except ObjectDoesNotExist:
                    context['error_message'] = "I'm sorry, but that block appears not to exist."
                except MultipleObjectsReturned:
                    i = 0
                    for block in Block.objects.filter(unit=unit,rank=request.GET['edit']):
                        block.rank = 999-i
                        block.save()
                        i += 1
                    context['error_message'] = "Uh-oh! More than one block had the same rank! Please fix this error immediately."
                else:
                    context['abf_name'] = b.name
                    context['abf_rank'] = b.rank
                    context['abf_description'] = b.description
                    context['action'] = "Save"
        
        if request.method == 'POST':
            print(request.POST['submit'])
            is_valid = True
            
            if 'name' in request.POST and request.POST['name'] == '':
                is_valid = False
                context['name_error'] = "Please enter a name."
            elif 'name' not in request.POST:
                is_valid = False
                context['name_error'] = "Please quit messing with the form."
            
            if 'rank' in request.POST and request.POST['rank'] == '' or not request.POST['rank'].isdigit():
                is_valid = False
                context['rank_error'] = "Please enter a positive integer."
            elif 'rank' not in request.POST:
                is_valid = False
                context['rank_error'] = "Seriously! Quit messing with the form!"

            if 'description' not in request.POST:
                is_valid = False
                context['description_error'] = "STOP SCREWING AROUND!"

            if is_valid:
                try:
                    Block.objects.get(unit=unit, name=request.POST['name'])
                except ObjectDoesNotExist:
                    pass
                else:
                    context['name_error'] = "Names must not be duplicates."
                    is_valid = False

            if not is_valid:
                for arg in ['name','rank','description']:
                    context['abf_'+arg] = request.POST[arg]
                context['error_message'] = "Please fix any and all errors and try again."
                
            else:
                name = request.POST['name'].capitalize()
                rank = int(request.POST['rank'])
                description=request.POST['description']

                if rank > Block.objects.filter(unit=unit).count():
                    rank = Block.objects.filter(unit=unit).count()+1

                if request.POST['submit'] == "Add block":
                    try:
                        Block(unit=unit,
                              name=name,
                              rank=rank,
                              description=description,
                              ).save()
                        
                    except (TypeError, ValueError) as e:
                        for arg in ['name','rank','description']:
                            context['abf_'+arg] = request.POST[arg]
                        context['error_message'] = "Something went wrong and I don't know what. Please recheck your input and try again.\n%s"%e
                        
                    else:
                        context['success_message'] = "Block was successfully created!"
                        
                        for b in Block.objects.filter(unit=unit,rank__gte=rank).exclude(name=name):
                            b.rank += 1
                            b.save()
                            
                elif request.POST['submit'] == "Save block":
                    try:
                        block = Block.objects.get(unit=unit,
                                                  rank=request.GET['edit'])
                        
                    except (TypeError, ValueError) as e:
                        for arg in ['name','rank','description']:
                            context['abf_'+arg] = request.POST[arg]
                        context['error_message'] = "Something went wrong and I don't know what. Please recheck your input and try again.\n%s"%e

                    except MultipleObjectsReturned:
                        for arg in ['name','rank','description']:
                            context['abf_'+arg] = request.POST[arg]
                        context['abf_rank'] = 999
                        context['error_message'] = "Uh-oh! More than one block had the same rank! Please fix this error immediately."
                        
                    else:
                        old_rank = block.rank
                        block.name = name
                        block.rank = rank
                        block.description = request.POST['description']
                        block.save()
                        b_pk = block.pk
                        
                        context['success_message'] = "Block was successfully saved!"

                        if rank > old_rank:
                            for b in Block.objects.filter(unit=unit,
                                                          rank__gt=old_rank,
                                                          rank__lte=rank
                                                          ).exclude(pk=b_pk):
                                b.rank -= 1
                                b.save()
                        elif rank < old_rank:
                            for b in Block.objects.filter(unit=unit,
                                                          rank__lt=old_rank,
                                                          rank__gte=rank
                                                          ).exclude(pk=b_pk):
                                b.rank += 1
                                b.save()


        else:
            pass

        block_list = Block.objects.filter(unit__short_name=request.session['current_unit']).order_by('rank')
        context['block_list'] = block_list
            
    elif kwargs['obj'] == 'terms':

        context['action'] = "Add"

        if request.method == 'GET':
            if 'delete' in request.GET:
                try:
                    term = Term.objects.get(unit=unit, descriptor=request.GET['delete'])
                except ObjectDoesNotExist:
                    return redirect(reverse('aed_terms'))
                except MultipleObjectsReturned:
                    i = 0
                    for term in Term.objects.filter(unit=unit,descriptor=request.GET['delete']):
                        term.descriptor = "%05d" % i
                        term.save()
                        i += 1
                    context['error_message'] = "Uh-oh! More than one term had the same descriptor! Please fix this error immediately."
                else:
                    if term.shift_set.count() > 0:
                        context['error_message'] = "This term may not be deleted as it has shifts in it."
                    else:
                        term.delete()
                        context['success_message'] = "Term was successfully deleted!"
            
            elif 'edit' in request.GET:
                try:
                    t = Term.objects.get(unit=unit, descriptor=request.GET['edit'])
                except ObjectDoesNotExist:
                    context['error_message'] = "I'm sorry, but that term appears not to exist."
                except MultipleObjectsReturned:
                    i = 0
                    for term in Term.objects.filter(unit=unit,descriptor=request.GET['edit']):
                        term.descriptor = "%05d" % i
                        term.save()
                        i += 1
                    context['error_message'] = "Uh-oh! More than one term had the same descriptor! Please fix this error immediately."
                else:
                    if t.date_end < today():
                        context['error_message'] = "This term may not be edited as it is wholly in the past."
                    else:
                        context['atf_name'] = t.name
                        context['atf_descriptor'] = t.descriptor
                        context['atf_date_start'] = "{:%m/%d/%Y}".format(t.date_start)
                        context['atf_date_end'] = "{:%m/%d/%Y}".format(t.date_end)
                        context['action'] = "Save"

        if request.method == 'POST':
            is_valid = True
            
            if 'name' in request.POST and request.POST['name'] == '':
                is_valid = False
                context['name_error'] = "Please enter a name."
            elif 'name' not in request.POST:
                is_valid = False
                context['name_error'] = "Nice job breaking it, hero."
            if 'descriptor' in request.POST and request.POST['descriptor'] == '':
                is_valid = False
                context['descriptor_error'] = "Please enter a descriptor."
            elif 'descriptor' not in request.POST:
                is_valid = False
                context['descriptor_error'] = "Nope. I got this covered too."
            
            if 'date_start' in request.POST and request.POST['date_start'] == '':
                is_valid = False
                context['date_start_error'] = "Please enter a start date."
            elif 'date_start' not in request.POST:
                is_valid = False
                context['date_start_error'] = "Hmmm...I'm starting to wonder..."
            if 'date_end' in request.POST and request.POST['date_end'] == '':
                is_valid = False
                context['date_end_error'] = "Please enter an end date."
            elif 'date_end' not in request.POST:
                is_valid = False
                context['date_end_error'] = "Are you doing this because of these messages?"


            if is_valid: #check that dates are formatted correctly
                ds = request.POST['date_start']
                de = request.POST['date_end']
                try:
                    if '/' in ds:
                        m,d,y = map(int, ds.split('/'))
                    else:
                        y,m,d = map(int, ds.split('-'))
                    date_start = datetime.date(y,m,d)
                except (TypeError, ValueError):
                    context['date_start_error'] = "Please enter a valid date."
                    is_valid = False
                    
                try:
                    if '/' in de:
                        m,d,y = map(int, de.split('/'))
                    else:
                        y,m,d = map(int, de.split('-'))
                    if y < 1000: y += 2000
                    date_end = datetime.date(y,m,d)
                except (TypeError, ValueError):
                    context['date_end_error'] = "Please enter a valid date."
                    is_valid = False

            if is_valid: #deeper date validation
                if date_end <= date_start:
                    context['date_end_error'] = "End date must be later than start date."
                    is_valid = False

                if 'edit' not in request.GET and date_start < today():
                    context['date_start_error'] = "Start date (%s) should be later than today (%s)." % (date_start, today())
                    is_valid = False
                if 'edit' not in request.GET and date_end < today():
                    context['date_end_error'] = "End date (%s) should be later than today (%s)." % (date_end, today())
                    is_valid = False

            if not is_valid:
                for arg in ['name','descriptor','date_start','date_end']:
                    context['atf_'+arg] = request.POST[arg]
                context['error_message'] = "Please fix any and all errors and try again."
                
            else:
                name = request.POST['name'].capitalize()
                descriptor=request.POST['descriptor']

                if request.POST['submit'] == "Add term":
                    try:
                        Term(unit=unit,
                             name=name,
                             descriptor=descriptor,
                             date_start=date_start,
                             date_end=date_end,
                              ).save()
                        
                    except (TypeError, ValueError) as e:
                        for arg in ['name','descriptor','date_start','date_end']:
                            context['atf_'+arg] = request.POST[arg]
                        context['error_message'] = "Something went wrong and I don't know what. Please recheck your input and try again.\n%s"%e
                        
                    else:
                        context['success_message'] = "Term was successfully created!"
                            
                elif request.POST['submit'] == "Save term":
                    try:
                        term = Term.objects.get(unit=unit,
                                                descriptor=request.GET['edit'])
                        
                    except (TypeError, ValueError) as e:
                        for arg in ['name','descriptor','date_start','date_end']:
                            context['abf_'+arg] = request.POST[arg]
                        context['error_message'] = "Something went wrong and I don't know what. Please recheck your input and try again.\n%s"%e

                    except MultipleObjectsReturned:
                        for arg in ['name','descriptor','date_start','date_end']:
                            context['atf_'+arg] = request.POST[arg]
                        context['atf_descriptor'] = '00000'
                        context['error_message'] = "Uh-oh! More than one term had the same descriptor! Please fix this error immediately."
                        
                    else:
                        term.name = name
                        term.descriptor = descriptor
                        term.date_start = date_start
                        term.date_end = date_end
                        term.save()
                        
                        context['success_message'] = "Term was successfully saved!"

        terms = Term.objects.filter(unit=unit).order_by('date_start','date_end')
        context['term_list'] = terms

        context['today'] = today()
                
    elif kwargs['obj'] == 'units':
        context['unit'] = unit

        context['euf_name'] = unit.name
        context['euf_short_name'] = unit.short_name
        context['euf_subreq'] = unit.sub_request_in_advance
        context['euf_hourly'] = unit.hourly_limit

        weekday_names = {'M': 'Monday',
                         'T': 'Tuesday',
                         'W': 'Wednesday',
                         'R': 'Thursday',
                         'F': 'Friday',
                         'S': 'Saturday',
                         'U': 'Sunday',
                         'V': 'Varies',
                         }

        if request.method == 'POST':
            is_valid = True
            
            if 'name' in request.POST and request.POST['name'] == '':
                is_valid = False
                context['name_error'] = "Please enter a name."
            elif 'name' not in request.POST:
                is_valid = False
                context['name_error'] = "You think you're so clever, don'tcha?"
            if 'short_name' in request.POST and request.POST['short_name'] == '':
                is_valid = False
                context['short_name_error'] = "Please enter a short name."
            elif 'short_name' not in request.POST:
                is_valid = False
                context['short_name_error'] = "Ha! Nice try!"
            
            if 'subreq' in request.POST and request.POST['subreq'] == '' or not request.POST['subreq'].isdigit():
                is_valid = False
                context['subreq_error'] = "Please enter a positive integer."
            elif 'subreq' not in request.POST:
                is_valid = False
                context['subreq_error'] = "Really!? I'mma smack ya!"
            if 'hourly' in request.POST and request.POST['hourly'] == '' or not request.POST['hourly'].isdigit() or int(request.POST['hourly'])>100:
                is_valid = False
                context['hourly_error'] = "Please enter a positive integer (that's less than 100)."
            elif 'hourly' not in request.POST:
                is_valid = False
                context['hourly_error'] = "*SMACK!*"

            if 'weekdays' not in request.POST or request.POST.getlist('weekdays') == []:
                is_valid = False
                context['subreq_error'] = "Please select at least one choice."


            if not is_valid:
                for arg in ['name','short_name','subreq','hourly']:
                    context['euf_'+arg] = request.POST[arg]
                context['error_message'] = "Please fix any and all errors and try again."

            else:
                try:
                    unit.name = request.POST['name']
                    unit.short_name = request.POST['short_name']
                    unit.sub_request_in_advance = request.POST['subreq']
                    unit.hourly_limit = request.POST['hourly']

                    wdays = ""
                    for wday in request.POST.getlist('weekdays'):
                        if wday in 'MTWRFSUV': wdays += wday
                    unit.weekdays = wdays
                    
                    unit.save()
                except Exception as e:
                    for arg in ['name','short_name','subreq','hourly']:
                        context['euf_'+arg] = request.POST[arg]
                    context['error_message'] = "Something went wrong and I don't know what. Please recheck your input and try again.\n%s"%e
                else:
                    request.session['current_unit'] = unit.short_name
                    context['success_message'] = "Unit was successfully saved!"

                    context['euf_name'] = unit.name
                    context['euf_short_name'] = unit.short_name
                    context['euf_subreq'] = unit.sub_request_in_advance
                    context['euf_hourly'] = unit.hourly_limit
            
        
        weekdays = []
        for wday in 'MTWRFSUV':
            weekdays.append({'name': weekday_names[wday],
                             'N': wday,
                             'checked': wday in unit.weekdays})
        context['weekdays'] = weekdays
        
    else:
        return redirect(reverse('aed_positions'))

    context['selected_tab'] = kwargs['obj']

    return render(request, 'scheduler/add_edit_delete.html', context)

##################
### right side ###
##################

def loginout_view(request, **kwargs):

    if 'out' in kwargs:
        logout(request)
        request.session['current_unit'] = "dining services"
##        request.user = AnonymousUser()

    context = RequestContext(request)

    if 'out' in kwargs:
##        context['action'] = 'out'
        context['logged_out'] = True

    context['next'] = request.GET['next'] if 'next' in request.GET else ''

    if request.method == 'POST':
        form = authForms.AuthenticationForm(data=request.POST)

        if form.is_valid:
            username = request.POST['username'] #form.cleaned_data.get('username')
            password = request.POST['password'] #form.cleaned_data.get('password')

            if request.user.is_authenticated():
                logout(request)
            user = authenticate(username=username, password=password)

            if user is not None: #password verified
                if user.is_active:
                    login(request, user)

                    try:
                        request.session['current_unit'] = user.worker.unitstatus_set.first().unit.short_name
                    except (ObjectDoesNotExist, AttributeError):
                        request.session['current_unit'] = ''

                    if 'next' in request.POST:
                        return redirect(request.POST['next'])
                    else:
                        return redirect('home')
                else:
                    context['deactive'] = True
            else:
                context['invalid'] = True
                context['form'] = form
    else:
        form = authForms.AuthenticationForm()
        context['form'] = form

    if request.user.is_anonymous():
        context['place_name'] = 'the Dining Commons'
        context['contact_info'] = 'thecommons@rit.edu (placeholder)'

    return render(request, 'scheduler/loginout.html', context)

def register_view(request):

    context = RequestContext(request)

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        context['form'] = form

        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email1']
            password = request.POST['password1']
            name_first = request.POST['name_first']
            name_last = request.POST['name_last']
            
            unit_chosen = request.POST['unit_choice']
            unit = Unit.objects.get(short_name=unit_chosen)
            
            user = create_user(username, email, password,
                               first_name=name_first, last_name=name_last)
            worker = Worker(name=("%s %s"%(name_first, name_last)),
                            email=email)
            worker.user = user
            
            u_s = UnitStatus(worker=worker, unit=unit)
            if request.user.is_staff:
                u_s.work_status = 'EW'
            else:
                u_s.work_status = 'AA'
            
            worker.save()
            #user.save()

            if not request.user.is_staff:
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('profile_edit')
            else:
                context['registered'] = True
                context['new_user'] = user
                return render(request, 'scheduler/register.html', context)
                
    else:
        form = CreateUserForm()
        context['form'] = form

    return render(request, 'scheduler/register.html', context)

@login_required
def reset_view(request):

    context = RequestContext(request)

    if request.method == 'POST':
        pass
    else:
        pass

    return render(request, 'scheduler/reset.html', context)

def availability_table(worker, form=False, request=None):
    has_availability_data = form or bool(worker.availability)

    if has_availability_data:
        availability_data = {}
        
        today = datetime.date.today()
        last_monday = today - timedelta(days=today.weekday())
        weekday_tabs = ['{:%A} {:%a}'.format(*[last_monday + timedelta(days=k)]*2).split(' ') for k in range(-1,6)]
        weekdays, wdays = zip(*weekday_tabs)
        availability_data['weekdays'] = weekdays

        available_blocks = worker.get_availability()

        def time_str(time):
            return "{:%I:%M %p}".format(time)[(time.hour-1)%12 < 9 :]
        def hour_str(time):
            return "{:%I %p}".format(time)[(time.hour-1)%12 < 9 :]

        available_table = []
        block_list = []
        
        block_times = []
        for wday, times in available_blocks.items():
            block_times.extend(times)
        
        for h in range(24):
            hour = datetime.time(h)
            h_str = hour_str(hour)
            delta_neg = timedelta(hours=-1)
            delta_pos = timedelta(hours=1)
            
            available_table.append( [h_str, []] )
            
            for wday in wdays:
                if wday in available_blocks:
                    #print(wday)
                    blocks = []
##                    times = []
                    
                    for b, block in enumerate(available_blocks[wday]):
                        b0 = block[0].hour + block[0].minute/60
                        b1 = block[1].hour + block[1].minute/60

                        if form:
                            if not request:
                                blocks.append( TimeBlockForm(initial_data=block, prefix="tb_"+wday+str(b)) )
                            else:
                                blocks.append( TimeBlockForm(request.POST, initial_data=block, prefix="tb_"+wday+str(b)) )
                        else:
                            blocks.append( list(map(time_str, block)) )
                        
                        if h < b0 < h+1:
                            status = "start"
                        elif h < b1 < h+1-1/60:
                            status = "end"
                        elif b0 <= h < b1:
                            status = "middle"
                        elif h < b0 < b1 < h+1-1/60:
                            status = "singlet"
                        else:
                            status = ""

                        if status != "":
                            break
                            
##                            print(" ",h,b0,b1,status)

                    available_table[h][1].append(status)
                    block_list.append( (wday, blocks) )
##                    block_times.extend( available_blocks[wday] )

                else:
                    available_table[h][1].append('')

        availability_data['block_list'] = SortedDict(block_list)

        if form: availability_data['block_times'] = block_times
        
        availability_data['table'] = SortedDict(available_table)

        return True, availability_data

    return False, {}

@login_required
def profile_view(request, *args, **kwargs):

    context = RequestContext(request)

    if 'otheruser' in kwargs:
        if request.user.is_staff:
            try:
                other_user = get_object_or_404(User, username=kwargs['otheruser'])
                context['other_user'] = other_user
                
                try:
                    context['worker_data'] = other_user.worker.get_fields(
                        exclude=['id', 'availability'])
                    #print(context['worker_data'])
                    context['form'] = PasswordResetForm(
                        initial={'username': other_user.username,
                                 'email': other_user.email}
                    )

                    context['is_approved'] = other_user.worker.is_approved
                    context['has_availability_data'], context['availability_data'] = availability_table(other_user.worker)
                except ObjectDoesNotExist:
                    context['is_approved'] = None
            except Http404 as e:
                context['other_user_dne'] = True
            else:
                print(context['other_user'])
        else:
            return redirect('profile')
    else:
        try:
            worker = request.user.worker
            context['worker_data'] = worker.get_fields(
                exclude=['user','pay_rate','work_status',
                         'is_employed','is_approved','rank',
                         'time_updated','id','availability'])
            context['has_availability_data'], context['availability_data'] = availability_table(worker)
        except ObjectDoesNotExist:
            pass

    #print(context)

    return render(request, 'scheduler/profile.html', context)

@login_required
def profile_edit_view(request, *args, **kwargs):

    context = RequestContext(request)

    if 'otheruser' in kwargs:
        if request.user.is_staff:
            other_user = User.objects.get(username__exact=kwargs['otheruser'])
            worker = other_user.worker
            context['other_user'] = other_user
        else:
            return redirect('profile_edit')
    else:
        worker = request.user.worker

    context['worker'] = worker

    print(request.method, 'save availability' in request.POST)

    if request.method == 'POST' and 'save availability' in request.POST:
        req = request
    else:
        req = None

    context['has_availability_data'], context['availability_data'] = availability_table(worker, form=True, request=req)
    context['formify'] = True
    #initial_data = context['availability_data']['block_times']
    block_list = context['availability_data']['block_list']

    if request.method == 'POST' and 'save availability' in request.POST:
        update_data = {}
        
        if 'picked' in request.POST:
            pick_ids = request.POST.getlist('picked')
            pick_ids.sort(key=lambda x:x[0])
##            print(pick_ids)
            #Checkbox ids were read from left to right, starting at the top
            #the sort function groups the ids into weekdays and
            #incidentally preserves the order of the hours.
            def retrieve_info(s):
                wday, hour = s.split('_')
                hour = (int(hour[:-3])%12) + 12*(hour[-2]=='P')
                return wday, hour

            while pick_ids:
                id0 = pick_ids.pop(0)
                block = []
                wday, beg = retrieve_info(id0)
                end = beg

                while pick_ids and retrieve_info(pick_ids[0])[1] == end+1:
                    pick_ids.pop(0)
                    end += 1

                if wday not in update_data:
                    update_data[wday] = []

                st = datetime.time(beg)
                et = datetime.time(end,59)
                update_data[wday].append( [st,et] )

                req = None
                
        else:
            update_data = {}
            for wday, block_forms in block_list.items():
                for block_form in block_forms:
                    if block_form.is_valid():# and block_form.has_changed():
                        if wday not in update_data:
                            update_data[wday] = []
                        ts_str = block_form['time_start'].value()
                        te_str = block_form['time_end'].value()
                        ts = datetime.time(*map(int,ts_str.split(":")[:2]))
                        te = datetime.time(*map(int,te_str.split(":")[:2]))
                        
                        update_data[wday].append( [ts, te] )
            
        worker.update_availability(update_data)
        context['has_availability_data'], context['availability_data'] = availability_table(worker, form=True, request=req)

    if request.method == 'POST' and 'submit info' in request.POST:
        form_info = ProfileEditForm(request.POST, instance=worker, is_staff=request.user.is_staff, prefix="profile")

        if form_info.is_valid():
##            saved = form_info.save(commit=False)
##            print(saved)
##            saved.save()
##            form_info.save_m2m()
            form_info.save()
            context['saved'] = True
    else:
        form_info = ProfileEditForm(instance=worker, is_staff=request.user.is_staff, prefix="profile")

    if request.method == 'POST' and 'add unit' in request.POST:
        add_unit_form = AddUnitForm(request.POST, worker=worker)

        if add_unit_form.is_valid():
##            add_unit_form.save()
##            print(add_unit_form.cleaned_data['unit_choices'])
            unit = Unit.objects.get(short_name = add_unit_form.cleaned_data['unit_choices'])
            new_unit = UnitStatus(worker=worker, unit=unit)

            if request.user.is_staff: #automatically approve if unit added by staff
                new_unit.work_status = 'EW'
                
            new_unit.save()
            add_unit_form = AddUnitForm(worker=worker)
    else:
        add_unit_form = AddUnitForm(worker=worker)

    context['form_info'] = form_info
    context['add_unit_form'] = add_unit_form
    
    return render(request, 'scheduler/profile_edit.html', context)

@user_passes_test(is_staff)
def profile_deactivate_or_delete_view(request, *args, **kwargs):

    context = RequestContext(request)

    #print(request,'\n',request.POST)

    if request.method == 'POST':
        print(request.POST)
        #if form.is_valid():
        otheruser = User.objects.get(username__exact=kwargs['otheruser'])
        context['otheruser'] = otheruser.username
        if 'deactivate' in request.POST:
            context['action'] = 'deactivated'
            otheruser.is_active = False
            otheruser.save()
        elif 'delete' in request.POST:
            context['action'] = 'deleted'
            otheruser.delete()

        return render(request, 'scheduler/deactivate_delete.html', context)
    else:
        return redirect(reverse('profile'))

@user_passes_test(is_staff)
def approve_deny_users_view(request, *args, **kwargs):

    context = RequestContext(request)

    if request.method == 'POST':
        user_list = request.POST.getlist('picked')
        context['users'] = User.objects.filter(username__in=user_list)

        if 'approve' in request.POST or 'approve_all' in request.POST:
            if 'approve_all' in request.POST:
                context['users'] = User.objects.filter(
                    is_active=True,
                    worker__isnull=False,
                    worker__is_approved=False
                )
            context['action'] = 'approved'
            for user in context['users']:
                try:
                    unitstatus = user.worker.unitstatus_set.get(unit__short_name=request.session['current_unit'])
                    unitstatus.work_status = 'EW' #"Employed - Working"
                    unitstatus.save()
                except ObjectDoesNotExist:
                    print("ERROR: unitstatus for user %s does not exist!" % user)
        elif 'deny' in request.POST:
            context['action'] = 'denied'
            pass
##            for user in context['users']:
##                user.is_active = False
##                user.save()

    return home_view(request, context=context)

@user_passes_test(is_staff)
def approve_deny_shifts_view(request, *args, **kwargs):

    context = RequestContext(request)

    if request.method == 'POST':
        pick_list = request.POST.getlist('picked')
        shift_list = {}
        context['shifts'] = []

        if 'approve_all' not in request.POST: #'approve', 'ignore', and 'deny'
            for pick in pick_list:
                print("Pick:",pick)
                shift_pk, weekNum = map(int, pick.split('_'))
                print(" ",shift_pk, weekNum)
                if shift_pk in shift_list:
                    shift_list[shift_pk].append(weekNum)
                else:
                    shift_list[shift_pk] = [weekNum]
        else:
            for shift in Shift.objects.filter(status__in=['Sr','SR'],
                                              unit__short_name=request.session['current_unit']
                                              ):
                shift_list[shift] = shift.get_sub_weeks()

        for s in shift_list:
            print(s, Shift.objects.get(pk=s), shift_list[s])

        if 'ignore' in request.POST:
            context['action'] = 'ignored'
            
            for shift in shift_list:
                for weekNum in shift_list[shift]:
                    context['shifts'].append( (shift, shift.date_str(weekNum)) )
                    shift.pop_sub_week(weekNum)
                shift.status = 'F'
                shift.save()

            return render(request, 'scheduler/approve_deny.html', context)
        
        elif 'approve' in request.POST or 'approve_all' in request.POST:
            context['action'] = 'approved'
            
        elif 'deny' in request.POST:
            context['action'] = 'denied'

        for shift_pk in shift_list:
##            print(shift_list[shift_pk])
##            shift_list[shift].sort()
##            print(shift_list[shift])
            shift_to_split = Shift.objects.get(pk=shift_pk)
            splitted = [shift_to_split]

            s_pk = shift_pk
            s_str = str(shift_to_split)
##            s_ds = shift.date_start
            w = shift_to_split.substitute_worker or shift_to_split.original_worker

            for weekNum in sorted(shift_list[shift_pk]):
                #add a new record
                r = Record(worker=w,
                           category='I',
                           info="Shift submitted to sublist",
                           note="%d: %s on %s\nRequest approved on %s" % (
                               s_pk,
                               s_str,
                               shift_to_split.date_str(weekNum),
                               today())
                           )
                r.save()

                #commence splitting
                splits = shift_to_split.split(weekNum)

                context['shifts'].append( (splits[0], splits[0].date_str(weekNum)) )

                if 'approve' in request.POST or 'approve_all' in request.POST:
                    splits[0].status = 'Sa' #sub accepted
                elif 'deny' in request.POST:
                    if splits[0].status == 'Sr':
                        splits[0].status = 'Sd' #sub denied
                    elif splits[0].status == 'SR':
                        splits[0].status = 'Sf' #sub forbidden

                splitted += splits[1:]

                for s in splits[1:]:
                    s.status = 'F'

                shift_to_split = splits[-1]

            for s in splitted:
                print(" ",s.pk, s.weekly, s.week_first, s.week_last)
                s.save()

    return home_view(request, context=context)

@user_passes_test(is_staff)
def approve_deny_subs_view(request, *args, **kwargs):

    context = RequestContext(request)

    if request.method == 'POST':
        subs = []
        
        for arg in request.POST:
            if 'picked_' in arg:
                shift_pk = int(arg.split('_')[1])
                worker_pk = request.POST[arg]

                shift = Shift.objects.get(pk=shift_pk)
                worker = Worker.objects.get(pk=worker_pk)

                subs.append([worker, shift])

                if 'approve' in request.POST:
                    if shift.original_worker:
                        shift.substitute_worker = worker
                    else:
                        shift.original_worker = worker
                        
                    shift.pick_requests.clear()
                    shift.status = 'F'
                    context['action'] = "approved"
                    
                    #add a new record
                    r = Record(worker=w,
                               category='I',
                               info="Shift picked up from sublist",
                               note="%d: %s on %s\nRequest approved on %s" % (
                                   shift.pk,
                                   str(shift),
                                   shift.date_str(),
                                   today())
                               )
                    r.save()
                    
                elif 'deny' in request.POST:
                    shift.pick_requests.remove(worker)
                    context['action'] = "denied"

                if shift.weekly == True: #set worker on following shifts as well
                    pass

                shift.save()
                
        context['subs'] = subs

    return home_view(request, context=context)

def change_unit(request, *args, **kwargs):

    if request.POST:
        print(request.POST)
        
        context = RequestContext(request)

        request.session['current_unit'] = request.POST['selected_unit']

        return HttpResponseRedirect(request.POST['next'])
