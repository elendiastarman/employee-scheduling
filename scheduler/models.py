from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.datastructures import SortedDict
from django.forms.forms import pretty_name

import datetime
from datetime import timedelta

# Create your models here.
class Worker(models.Model):

    #static stuff
    user = models.OneToOneField(User, null=True)
    
    name = models.CharField(max_length=200)
    telephone = models.CharField(max_length=15, default="",blank=True)
    email = models.EmailField(max_length=200)
    secondary_email = models.EmailField(max_length=200, default="",blank=True)
    badge_number = models.CharField(max_length=8, default="",blank=True)
    date_of_birth = models.DateField(null=True)
    is_international = models.BooleanField(default=False)

    #can change

    #<address>
    street_1 = models.CharField(max_length=200, blank=True)
    street_2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True)

    time_updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    def mailing_address(self):
        pass
    #</address>

    LOCATION_CHOICES = (
        ('DM', 'Dorms'),
        ('PG', 'Perkins Green'),
        ('CM', 'Colony Manor'),
        ('Pr', 'Province'),
        ('PP', 'Park Point'),
        ('GV', 'Global Village'),
        ('UC', 'University Commons'),
        ('RK', 'Riverknoll'),
        ('RI', 'RIT Inn'),
        ('RV', 'Rustic Village'),
        ('Ot', 'Other'),
    )
    location = models.CharField(max_length=2,
                                choices=LOCATION_CHOICES,
                                blank=True)
    
    has_a_car = models.BooleanField(default=False)

    TSHIRT_SIZES = (
        ('XS', 'Extra small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra large'),
        ('XX', 'Extra extra large'),
    )
    tshirt_size = models.CharField(max_length=2,
                                   choices=TSHIRT_SIZES,
                                   blank=True)

    availability = models.TextField(editable=False, blank=True)

    #admin only
    pay_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    APPROVAL_STATUS_CHOICES = (
        ('NA', 'Not approved yet'),
        ('A', 'Approved'),
    )
    approval_status = models.CharField(max_length=2,
                                       choices=APPROVAL_STATUS_CHOICES,
                                       default='NA', editable=False)

    is_approved = models.BooleanField(editable=False,default=False)

    hourly_limit = models.IntegerField(default=40)

    rank = models.ForeignKey('Rank', null=True)

    #informational functions
    def shift_set(self):
        shifts = self.shift_originalWorker.all() | self.shift_substituteWorker.all()

        shifts = list(shifts)
        i = 0
        while i < len(shifts):
            if shifts[i].worker() != self:
                shifts.pop(i)
            else:
                i += 1
        return shifts
    
    def is_employed(self, unit):
        try:
            unitstatus = self.unitstatus_set.get(unit=unit)
        except:
            return False
        else:
            return unitstatus.work_status[0] == 'E'
    is_employed.boolean = True
    
    def past_experience(self): #returns all the positions that have been worked
        #specifically, it returns a dictionary of the form
        #{<position>: {'all': <total>, <block>: <block-total>, ...},
        # <position>: ...}
        experience = {}
        records = self.record_set.filter(category='T')

        for r in records:
            r_shift = Shift.objects.get(pk=int(r.info))
            
            #rudimentary safe-guard against record falsification
            if self != r_shift.worker(): continue
            
            position = r_shift.position.name
            block = str(r_shift.position.block)
            
            if position not in experience:
                experience[position] = {'all': 0}
            experience[position]['all'] += 1
        
            if block not in experience[position]:
                experience[position][block] = 0
            experience[position][block] += 1

        return experience

    def get_availability(self): #returns a dictionary 
        text = self.availability
        lines = text.splitlines()
        today = datetime.date.today()

        weekdays = ['{:%a}'.format(today+timedelta(days=k)) for k in range(7)]

        available_blocks = {}

        for line in lines:
            space_pos = line.find(' ')
            if space_pos > -1:
                weekday = line[:space_pos]
                times = line[space_pos+1:]
                wday = weekday[:3].capitalize()

                if wday in weekdays: #allows mon, Mon, monday, Monday
                    try:
                        time_start, time_end = map(lambda s: s.strip(), times.split('-')) #allows 09:20-15:00 and 09:20 - 15:00
                        ts, te = map(lambda time: datetime.time(*map(int, time.split(':'))), [time_start, time_end])
                    except ValueError as e:
                        print(e, times)
                    else:
                        if wday not in available_blocks:
                            available_blocks[wday] = []
                        available_blocks[wday].append( [ts,te] )

        return available_blocks

    def update_availability(self, new_data):
        print("updating availability")
        
        current = self.get_availability()
##        current.update(new_data)
        collated = {}

        today = datetime.date.today()
        wdays = ['{:%a}'.format(today+timedelta(days=k)) for k in range(7)]
        for wday in wdays:
            pre_set = []
            post_set = []
            
            if wday in current:
                pre_set.extend(current[wday])
            if wday in new_data:
                pre_set.extend(new_data[wday])

            print("pre_set pre-sort:",pre_set)

            pre_set.sort() #sorts on time_start then time_end by default

            print("pre_set post-sort:",pre_set)

            while pre_set:
                t0 = pre_set.pop(0)
                ts = t0[0]
                te = t0[1]

                while pre_set:
                    p0 = pre_set[0][0].hour + pre_set[0][0].minute/60
                    if p0 - (te.hour + te.minute/60) <= 1/30:
                        te = max(te, pre_set[0][1])
                        pre_set.pop(0)
                    else:
                        break

                post_set.append( [ts,te] )

            collated[wday] = post_set
        
        lines = []
        
        for wday, blocks in collated.items():
            for block in blocks:
                line = wday+" "
                line += '{:%H:%M}'.format(block[0])
                line += "-"
                line += '{:%H:%M}'.format(block[1])
                print(line)

                lines.append(line)

        self.availability = '\n'.join(lines)
        self.save()

    def absences(self):
        absences = self.record_set.filter(category__in=['As','Ae','Au'])
        a_sick = absences.filter(category='As').count()
        a_emergency = absences.filter(category='Ae').count()
        a_unexcused = absences.filter(category='Au').count()

        absence_info = {'excused': a_sick+a_emergency,
                        'unexcused': a_unexcused,
                        'sick': a_sick,
                        'emergency': a_emergency,}
        
        return absence_info

    def timeliness(self):
        from math import sqrt
        
        time_records = self.record_set.filter(category='T')
        times = [int(record.info.split(' ')[0]) for record in time_records]

        mean = sum(times)/len(times)
        time_info = {'mean': mean,
                     'stddev': sqrt(sum([(t-mean)**2 for t in times]))/len(times),
                     'max': max(times)}

        return time_info

    #"official" class functions
    def get_fields(self, fields=None, exclude=[], bool_raw=False):
        if fields == None:
            fields = [field[0] for field in Worker._meta.get_fields_with_model()]

        data = []
        for field in fields:
            field_name = field.name
            if field_name not in exclude:
                if hasattr(self, "get_"+field_name+"_display"): #has a display name
                    data.append((pretty_name(field_name), getattr(self, "get_"+field_name+"_display")))
                elif hasattr(self, field_name):
                    if field.get_internal_type() == 'BooleanField' and not bool_raw:
                        if getattr(self, field_name):
                            word = "Yes"
                        else:
                            word = "No"
                        data.append((pretty_name(field_name), word))
                    else:
                        data.append((pretty_name(field_name), getattr(self, field_name)))

        return SortedDict(data)
    
    def __str__(self):
        return self.name

    def __iter__(self):
        for field in self._meta.get_all_field_names():
            yield (field, getattr(self, field))

    def save(self):
        if not self.rank:
            self.rank=Rank.objects.get(rank="SE")

        if self.rank.rank in ('Ma','Su','Ad'):
            self.approval_status = 'A'
        else:
            awaiting_approval = False
            for unitstatus in self.unitstatus_set.all():
                if unitstatus.work_status == 'AA':
                    awaiting_approval = True
                    break
            self.approval_status = 'NA' if awaiting_approval else 'A'
            
        self.is_approved = (self.approval_status != 'NA')

        if self.is_international:
            self.hourly_limit = 20
        
        super(Worker, self).save()

        if self.rank.rank in ('Su','Ad') and not self.user.is_staff:
            self.user.is_staff = True
            self.user.save()
        elif self.rank.rank not in ('Su','Ad') and self.user.is_staff:
            self.user.is_staff = False
            self.user.save()

class Shift(models.Model):
    original_worker = models.ForeignKey(Worker,
                                      related_name='shift_originalWorker',
                                      default=None,
                                      null=True,
                                      blank=True)
    substitute_worker = models.ForeignKey(Worker,
                                        related_name='shift_substituteWorker',
                                        default=None,
                                        null=True,
                                        blank=True)
    
    sub_requested = models.BooleanField(default=False, editable=False)
    STATUS_CHOICES = (
        ('O', 'Open'),
        ('F', 'Filled'),
        ('Sr', 'Sub requested'),
        ('So', 'Sub open'), #use if a person cannot come in (sickness, etc)
        ('Sa', 'Sub accepted'), #use for a sub request that was accepted
        ('Sd', 'Sub denied'),
        ('SR', 'Sub re-requested'),
        ('Sf', 'Sub forbidden'),
    )
    status = models.CharField(max_length=2,
                              choices=STATUS_CHOICES,
                              default='O')

    date = models.DateField()
    date_start = models.DateField(editable=False, default=None, null=True) #these two are calculated automatically
    date_end = models.DateField(editable=False, default=None, null=True)
    def date_str(self, weekNum=0):
        if weekNum == 0:
            date = self.date
        else:
            date = self.date_start + timedelta(weeks=weekNum-self.week_first-1)
        return "{:%A %B %d, %Y}".format(date)

    time_start = models.TimeField(default=None, null=True, blank=True)
    time_end = models.TimeField(default=None, null=True, blank=True)
    def time_str(self):
        ts = self.time_start
        te = self.time_end
        ts_str = "{:%I:%M %p}".format(ts)[(ts.hour-1)%12 < 9 :]
        te_str = "{:%I:%M %p}".format(te)[(te.hour-1)%12 < 9 :]
        if te.hour <= 1: te_str = "Close"
        return ts_str+"-"+te_str
    
    weekly = models.BooleanField()
    chain_nex = models.OneToOneField('self',
                                     default=None,editable=False,null=True,
                                     related_name='chain_bef')
##    chain_after = models.OneToOneField('self',
##                                       default=None,editable=False,null=True,
##                                       related_name='chain_nex')

    position = models.ForeignKey('Position')

    term = models.ForeignKey('Term', editable=False, null=True)
    unit = models.ForeignKey('Unit', editable=False, null=True)

    sub_weeks = models.CharField(max_length=200, editable=False, default="")
    def get_sub_weeks(self):
        if self.sub_weeks == "": return []
        return list(map(int, self.sub_weeks.split(',')))
    def add_sub_week(self, weekNum):
        if self.sub_weeks == "":
            self.sub_weeks = str(weekNum)
        elif weekNum not in self.get_sub_weeks():
            self.sub_weeks += ","+str(weekNum)
        self.save()
        #return self.get_sub_weeks()
    def pop_sub_week(self, weekNum):
        s_w = self.get_sub_weeks()
        if weekNum in s_w:
            pop = s_w.remove(weekNum)
        self.sub_weeks = ','.join(map(str,s_w))
        self.save()
        return pop
    def clear_sub_weeks(self):
        self.sub_weeks = ""

    pick_requests = models.ManyToManyField(Worker, related_name='pick_requests')

    #somewhat hacky way to add together shifts' time-spans
    def time_span(self):
        day = self.date_start
        ts = datetime.datetime(day.year,day.month,day.day, self.time_start.hour,self.time_start.minute)
        te = datetime.datetime(day.year,day.month,day.day, self.time_end.hour,self.time_end.minute)
        if self.time_end.hour <= 2: #ends shortly after midnight *next* day
            te += timedelta(days=1)
        return te-ts

    def __add__(self, other):
        if type(other) == Shift:
            return self.time_span() + other.time_span()
        elif type(other) == timedelta:
            return self.time_span() + other
        elif type(other) == int and other == 0:
            return self.time_span()
    def __radd__(self, other):
        return self+other

    #info functions
    def worker(self):
        return self.substitute_worker or self.original_worker

    def experience_level(self, worker):
        if not worker:
            return ''
        
        experience = worker.past_experience()
        position = self.position.name

        if position not in experience: return "untrained"
        if experience[position]['all'] < 5: return "trained"
        if experience[position]['all'] >= 5:
            #the following is necessary because some shifts, like salads,
            #may not have all possible blocks, but only some subset
            today = datetime.date.today()
            term = Term.objects.get(date_start__lte=today, date_end__gte=today)
            all_shifts = Shift.objects.filter(position__name=position,
                                              date_start__gte=term.date_start,
                                              date_end__lte=term.date_end,)
            blocks = []
            for shift in all_shifts:
                shift_block = str(shift.position.block)
                if shift_block not in blocks:
                    blocks.append(shift_block)

            #*now* I can make the checks I want to make
            #to be considered "expert", the worker must have had
            #a shift in each block at least three times
            for block in blocks:
                if block not in experience[position]:
                    return "experienced"
                elif experience[position][block] < 3:
                    return "experienced"

            return "expert"
    

    def is_submit_button_visible(self, worker=None):
        if type(worker) == User:
            if worker.is_staff: return False, ''
        if worker.user.is_staff: return False, ''
            
        if worker and worker != self.worker(): return False, 'Not your shift!'
        if self.status == 'Sf': return False, 'Request denied twice'
        if self.status == 'Sa': return False, 'Sub request accepted'

        return True, ''
    
    def can_submit(self, worker=None, weekNum=0):
        foo = self.is_submit_button_visible(worker)
        if foo[0] == False:
            return foo
        
        if worker == None:
            worker = self.worker()
            if worker == None: return False, 'No worker assigned'

        if not worker.user.is_active: return False, 'Inactive worker'
        if self.status in ['Sf','O', 'So']: return False, 'Already on sublist'
        
        if self.substitute_worker and worker != self.substitute_worker: return False, 'Already has a sub'
        if self.weekly and weekNum > 0 and self.status in ['Sr', 'SR'] and weekNum in self.get_sub_weeks(): return False, 'Already submitted request'
        if not self.weekly and self.status in ['Sr', 'SR']: return False, 'Already submitted request'

        return True, ''
    

    def is_pickup_button_visible(self, worker):
        if type(worker) == User:
            if worker.is_staff: return False, ""
        if worker.user.is_staff: return False, ""
            
        if worker == None: return False, "You don't exist!"
##        if worker in self.pick_requests.all(): return False, "Request was received"
        if worker.pick_requests.filter(pk=self.pk).exists(): return False, "Request was received"

        return True, ''

    def can_pickup(self, worker):
        foo = self.is_pickup_button_visible(worker)
        if foo[0] == False:
            return foo

        #non-overlapping limitation
        print("Shift under consideration: %s"%self)
        worker_shifts = worker.shift_set()
        
        for w_s in worker_shifts:
            print(w_s)
            ws_ds = w_s.date_start
            ws_de = w_s.date_end
            ws_ts = w_s.time_start
            ws_te = w_s.time_end
            
            s_ds = self.date_start
            s_de = self.date_end
            s_ts = self.time_start
            s_te = self.time_end

            if ws_te.hour <= 2:
                ws_te = datetime.time(23,59,59)
            if s_te.hour <= 2:
                s_te = datetime.time(23,59,59)

            if w_s.date_start.weekday() == self.date_start.weekday():
                print(ws_ds,ws_de,'',s_ds,s_de)
                if ws_ds <= s_de and s_ds <= ws_de:
                    print(ws_ts,ws_te,'',s_ts,s_te)
                    if ws_ts <= s_te and s_ts <= ws_te:
                        print("BLAM!")
                        return False, 'Conflicting shift'
            print()

        #time limitation
        day = self.date_start
        while day <= self.date_end:
            weekShifts = getWeekShifts(day, self.unit.short_name, worker=worker)

##            print(sum(weekShifts))
            total = sum(weekShifts, timedelta()) + self.time_span()

            if total.seconds/3600 > worker.hourly_limit:
                return False, 'Over weekly hour limit'
            
            day += timedelta(days=7)

        return True, ''
    
    def is_owned(self, worker):
        if self.status in ['O', 'So']: return False
        if worker != self.worker(): return False

        return True

    #copy/split functions
    def copy(self):
        field_names = [field[0].name for field in Shift._meta.get_fields_with_model()]
        shift2 = Shift()
        for field_name in field_names:
            setattr(shift2, field_name, getattr(self, field_name))
        shift2.id = shift2.pk = None
        shift2.save()
        return shift2

    def split(self, weekNum, for_sublist=True):
        if self.date_start == self.date_end:
            return [self]

        shifts = [self]
        new_shift = self.copy()
        
        self.date_start = self.date_end = self.term.date_start + timedelta(weeks=weekNum-1, days=(self.date_start-self.term.date_start).days%7)

        if new_shift.week_first+1 < weekNum < new_shift.week_last:
            new_shift_before = new_shift
            new_shift_after = new_shift.copy()

            new_shift_before.date_end = self.date_end - timedelta(weeks=1)
            new_shift_after.date_start = self.date_start + timedelta(weeks=1)

            for wN in self.get_sub_weeks():
                if wN >= weekNum:
                    new_shift_before.pop_sub_week(wN)
                if wN <= weekNum:
                    new_shift_after.pop_sub_week(wN)

            shifts += [new_shift_before, new_shift_after]
        else:
            if new_shift.week_first == weekNum-1: #first week of shift
                new_shift.date_start = self.date_start + timedelta(weeks=1)
            elif new_shift.week_last == weekNum-1: #last week of shift
                new_shift.date_end = self.date_end - timedelta(weeks=1)

            new_shift.pop_sub_week(weekNum)

            shifts.append(new_shift)
            
        self.clear_sub_weeks()

        for shift in shifts:
            shift.save()
            print(shift.pk, shift.weekly, shift.week_first, shift.week_last, shift.get_sub_weeks())

        return shifts

    #special functions
    @property
    def is_open(self):
        return self.original_worker == None

    day_of_week = ""
    @property
    def get_day_of_week(self):
        self.day_of_week = ("Monday", "Tuesday", "Wednesday", "Thursday",
                            "Friday", "Saturday", "Sunday")[self.date.weekday()]
        return self.day_of_week

    @property
    def week_first(self):
        return (self.date_start - self.term.date_start).days // 7
    @property
    def week_last(self):
        return (self.date_end - self.term.date_start).days // 7

    def __str__(self):
        return "%s %s (%s)" % (self.position.name,
                                    self.time_str(),
                                    str(self.position.block))

    def save(self, *args, **kwargs):
        if self.time_start == None:
            self.time_start = self.position.default_time_start
        if self.time_end == None:
            self.time_end = self.position.default_time_end

        if self.date_start == self.date_end:
            self.weekly = False

        if self.date == None:
            self.date = self.date_start

        if self.term == None:
            try:
                self.term = Term.objects.get(date_start__lte=self.date,
                                             date_end__gte=self.date)
            except ObjectDoesNotExist:
                self.term = None

        if self.term != None:
            if self.date_start == None:
                self.date_start = self.date
            else:
                self.date = self.date_start

            if self.date_end == None:
                if self.weekly:
                    numWeeks = (self.term.date_end - self.date).days//7
                    self.date_end = self.date_start + timedelta(weeks=numWeeks)
                else:
                    self.date_end = self.date_start

        if self.status == 'O':
            if self.substitute_worker:
                self.status = 'Sa'
            elif self.original_worker:
                self.status = 'F'
            
        super(Shift, self).save(*args, **kwargs)

def getWeekShifts(day, unit_name, worker=None, singleDay=False):
##    day_of_week_num = day.weekday
    monday = day - timedelta(days=day.weekday())
    sunday = monday + timedelta(days=6)

    shifts = Shift.objects.filter(
        date_start__lte=sunday,
        date_end__gte=monday,
        unit__short_name = unit_name,
    ).distinct()

    if singleDay: shifts = shifts.filter(date_start__week_day=(day.weekday()+2)%7)

    if worker:
##        shifts.filter(Q(original_worker=worker) | Q(substitute_worker=worker))
        i = 0
        shifts = list(shifts)
        while i < len(shifts):
            if shifts[i].worker() != worker:
                shifts.pop(i)
            else:
                i += 1

    return shifts

class Position(models.Model): #sub shop, grill server, dish, etc.
    #shift = models.ForeignKey(Shift)
    
    name = models.CharField(max_length=20)
    description = models.TextField()

##    (MORNING, MIDDAY, AFTERNOON, CLOSING) = ('A','B','C','D')
##    BLOCK_CHOICES = (
##        (MORNING, 'Morning'),
##        (MIDDAY, 'Midday'),
##        (AFTERNOON, 'Afternoon'),
##        (CLOSING, 'Closing'),
##    )
##    block = models.CharField(max_length = 1,
##                             choices = BLOCK_CHOICES)
    block = models.ForeignKey('Block')

    default_time_start = models.TimeField()
    default_time_end = models.TimeField()

    def __str__(self):
        return self.name+" ("+str(self.block)+")"

class Block(models.Model):
    unit = models.ForeignKey('Unit')
    
    name = models.CharField(max_length=20)
    rank = models.IntegerField() #this is NOT the rank model! it is only used for temporal ordering
    description = models.TextField(default=None, null=True, blank=True)

    def __str__(self):
        return self.name

class Rank(models.Model): #student employee, manager, supervisor, etc

    RANK_CHOICES = (
        ('Ad', 'Administrator'),
        ('Su', 'Supervisor'),
        ('FT', 'Full Time'),
        ('Ma', 'Manager'),
        ('SE', 'Student Employee'),
    )
    
    rank = models.CharField(max_length = 2,
                            choices = RANK_CHOICES,
                            default = 'SE',
                            unique=True)

    @property
    def is_student(self):
        return self.rank in ('Ma', 'SE')

    description = models.TextField()
    time_updated = models.DateTimeField()

    def __str__(self):
        return self.get_rank_display()

class Record(models.Model):

    worker = models.ForeignKey(Worker)

    CATEGORY_CHOICES = (
        #staff can add these
        ('I', 'Information'), #a purely informational staff-only note
        ('P', 'Personal note'), #viewable by employee
        ('A', 'Annotation'), #not severe, but notable
        ('C', 'Complaint'), #more severe

        #these are automatically maintained by the system
        ('T', 'Time'),
        ('As', 'Absent (sick)'),
        ('Ae', 'Absent (emergency)'),
        ('Au', 'Absent (unexcused)'),
    )
    category = models.CharField(max_length=2,
                                choices=CATEGORY_CHOICES,
                                default='I')

    time_added = models.DateTimeField(auto_now_add=True) #these two are automatically
    time_edited = models.DateTimeField(auto_now=True) #editable = False

    info = models.CharField(max_length=100, blank=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return "%s, %s: %s" % (self.worker, self.category, self.info)

class Announcement(models.Model):

    title = models.CharField(max_length=50)
    body = models.TextField()
    image = models.ImageField(upload_to='images/', max_length=200, blank=True)

    KIND_CHOICES = [
        ('3An', 'Announcement'),
        ('2No', 'Notification'),
        ('1Al', 'Alert'),
    ]
    kind = models.CharField(max_length=3,
                            choices=KIND_CHOICES,
                            default='3An')

    unit = models.ForeignKey('Unit', editable=False)

    date_created = models.DateField(auto_now_add=True)
    date_to_delete = models.DateField(default=datetime.date.today()+timedelta(days=3))

    def __str__(self):
        return self.get_kind_display()+": "+self.title

class Term(models.Model):
    unit = models.ForeignKey('Unit')
    
    name = models.CharField(max_length=100)
    descriptor = models.CharField(max_length=6)

    date_start = models.DateField()
    date_end = models.DateField()

class Unit(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)

    sub_request_in_advance = models.IntegerField(default=72) #hours
    hourly_limit = models.IntegerField(default=40) #max number of hours per week
    weekdays = models.CharField(max_length=8, default="MTWRF")

    def __str__(self):
        return self.name

class UnitStatus(models.Model):
    worker = models.ForeignKey(Worker)
    unit = models.ForeignKey(Unit)
    
    WORK_STATUS_CHOICES = (
        ('AA', 'Awaiting approval'),
        ('EW', 'Employed - Working'),
        ('EE', 'Employed - Emergency leave'), #sickness, broken bone, family death, that sort of thing
        ('EC', 'Employed - Co-op'),
        ('EB', 'Employed - On break'),
        ('EI', 'Employed - Inactive'), #when they are eligible but chosing not to work
        ('UF', 'Unemployed - Fired'),
        ('UG', 'Unemployed - Graduated'),
        ('UR', 'Unemployed - Resigned'),
    )
    work_status = models.CharField(max_length=2,
                                   choices=WORK_STATUS_CHOICES,
                                   default='AA')

    def __str__(self):
        return "%s is %s at %s" % (self.worker.name, self.get_work_status_display(), self.unit.name)

    def save(self):
        super(UnitStatus, self).save()
        self.worker.save()
