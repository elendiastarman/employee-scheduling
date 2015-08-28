from django import forms
from django.forms.formsets import formset_factory
from django.forms.widgets import SelectMultiple
from django.forms.extras.widgets import SelectTimeWidget
from django.contrib.admin.widgets import AdminDateWidget

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator

from django.contrib.sites.models import get_current_site
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from datetime import date

from scheduler.models import Position, Worker, Block, Unit, Announcement

class JumpToDateForm(forms.Form):
    selected_day = forms.DateField(widget=AdminDateWidget)

class SelectPositions(forms.Form):
    selected_positions = forms.ModelMultipleChoiceField(
        #widget=SelectMultiple,
        queryset=Position.objects.all()
    )

class CreateUserForm(forms.Form):

    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("These password fields don't match."),
        'email_mismatch': _("These email fields don't match."),
    }

    name_first = forms.CharField(label=_("First name"), max_length=30,
        help_text=_("30 characters or fewer."))
    name_last = forms.CharField(label=_("Last name"), max_length=30,
        help_text=_("30 characters or fewer."))
    
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    
    password1 = forms.CharField(label=_("Password"),
        help_text = _("Must be at least 8 characters."),
        widget=forms.PasswordInput,
        min_length=8)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Re-enter your password."))

    email1 = forms.EmailField(label=_("Email"))
    email2 = forms.EmailField(label=_("Email confirmation"),
        help_text=_("Re-enter your email."))

    UNIT_CHOICES = [(unit.short_name, unit.name) for unit in Unit.objects.all()]
    unit_choice = forms.ChoiceField(label=_("Unit choice"),
        help_text=_("Which Dining Services unit are you signing up for?"),
        choices=UNIT_CHOICES)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    
    def clean_email2(self):
        email1 = self.cleaned_data.get("email1")
        email2 = self.cleaned_data.get("email2")
        if email1 and email2 and email1 != email2:
            raise forms.ValidationError(
                self.error_messages['email_mismatch'],
                code='email_mismatch',
            )
        return email2

class PasswordResetForm(forms.Form):
    username = forms.CharField(label=_("Username"), max_length=254)
    email = forms.EmailField(label=_("Email"), max_length=254)

    def clean_email(self):
        username = self.cleaned_data.get("username")
        user = User.objects.get(username__exact=username)
        if user.email != self.cleaned_data.get("email"):
            raise forms.ValidationError(
                _("Username and email don't match."),
                code='username_email_mismatch',
            )
        return username

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        from django.core.mail import send_mail
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        username = self.cleaned_data["username"]
        user = User.objects.get(username__exact=username)

        if user.is_active and user.has_usable_password():
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            send_mail(subject, email, from_email, [user.email])

def ProfileEditForm(*args, **kwargs):

    exclude_list = ['user', 'pay_rate',
                    'rank', 'is_approved']

    if 'is_staff' in kwargs:
        if kwargs['is_staff']:
            exclude_list = ['user','id']
        
    class ProfileEditForm(forms.ModelForm):

        def __init__(self, *args, **kwargs):
                
            if 'is_staff' in kwargs:
                is_staff = bool(kwargs.pop('is_staff'))
            else:
                is_staff = False
            super(ProfileEditForm, self).__init__(*args, **kwargs)

            if 'instance' in kwargs and is_staff:
##                self.fields['approval_status'].initial = kwargs['instance'].approval_status
                self.fields['rank'].initial = kwargs['instance'].rank

        class Meta:
            model = Worker
            exclude = exclude_list

    return ProfileEditForm(*args, **kwargs)

class TimeBlockForm(forms.Form):
    widget = forms.TimeInput(attrs={'size':6})
    
    time_start = forms.TimeField(widget=widget)
    time_end = forms.TimeField(widget=widget)

    def __init__(self, *args, **kwargs):
        if 'initial_data' in kwargs:
            init_data = kwargs.pop('initial_data')
        else:
            init_data = None

        super(TimeBlockForm, self).__init__(*args, **kwargs)

        if init_data:
            self.fields['time_start'].initial = init_data[0]
            self.fields['time_end'].initial = init_data[1]

    def clean_time_end(self):
        time_start = self.cleaned_data['time_start']
        time_end = self.cleaned_data['time_end']
        
        if time_end <= time_start:
            raise forms.ValidationError(
                _("End time must be later than start time."),
                code='Time misorder',
            )
        return time_end
##
##class PositionBlockForm(forms.ModelForm):
##
##    def clean_rank(self):
##        r = self.cleaned_data['rank']
##        if r <= 0:
##            raise forms.ValidationError(
##                _("Rank must be positive."),
##                code='Rank is not positive',
##            )
##
##    class Meta:
##        model = Block
##        exclude = ['unit']

class AddAnnouncementForm(forms.ModelForm):

    def clean_date_to_destroy(self):
        dtd = self.cleaned_data['date_to_destroy']
        if dtd <= datetime.date.today():
            raise forms.ValidationError(
                _("Date to delete must be after today."),
                code='Date to delete before today',
            )

    class Meta:
        model = Announcement
        include = ['title','body','image','kind','date_to_destroy']

def AddUnitForm(*args, **kwargs):

    if 'worker' not in kwargs:
        raise TypeError("'worker' keyword argument is required.")

    worker = kwargs.pop('worker')

    worker_units = [unitstatus.unit for unitstatus in worker.unitstatus_set.all()]
    choices = []
    for unit in Unit.objects.all():
        if unit not in worker_units:
            choices.append( (unit.short_name, unit.name) )

    class AddUnitForm(forms.Form):
        unit_choices = forms.ChoiceField(choices=choices, required=False)

    return AddUnitForm(*args, **kwargs)
