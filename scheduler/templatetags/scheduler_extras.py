from django import template
from scheduler.models import Unit
from markdown2 import markdown
from django.core.urlresolvers import reverse

register = template.Library()

def unit_selector_form(parser, token):
    try:
        tag_name, user_str, current_unit = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires two arguments" % token.contents.split()[0])

    return UnitSelectorNode(user_str, current_unit)

class UnitSelectorNode(template.Node):
    def __init__(self, user_str, current_unit):
        self.user_str = template.Variable(user_str)
        self.current_unit = template.Variable(current_unit)

    def render(self, context):
        try:
            user = self.user_str.resolve(context)
        except template.VariableDoesNotExist as e:
            print(e)
            return '<p>Worker not found!</p>'

        try:
            short_name = self.current_unit.resolve(context)
        except template.VariableDoesNotExist as e:
            print(e)
            return '<p>Unit not found!</p>'
    
        unit = Unit.objects.get(short_name=short_name)
##            print(user.worker.name)
##            return "<p>%s</p>" % user.worker.name
        rn = '<select name="selected_unit">'
        unitstatuses = user.worker.unitstatus_set.all()
        if len(unitstatuses):
            for unitstatus in unitstatuses:
                rn += '<option '
                if unitstatus.unit.short_name == unit.short_name:
                    rn += 'selected="selected" '
                rn += 'value="%s">%s</option>' % (unitstatus.unit.short_name, unitstatus.unit.name)
        else:
            rn += '<option selected="selected" disabled="disabled">---</option>"'
        rn += "</select>"
        return rn

def markdown_tag(parser, token):
    try:
        tag_name, text = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])

    return MarkdownNode(text)

class MarkdownNode(template.Node):
    def __init__(self, text):
        self.text = template.Variable(text)

    def render(self, context):
        try:
            text = self.text.resolve(context)
        except template.VariableDoesNotExist as e:
            print(e)
            return '<p>Text not found!</p>'

        text = text.replace('\r\n','\n')
        text = text.replace('\n','<br/>')
        text = markdown(text)
        #eliminates the <p> and </p> tags at the beginning and end
        text = text[3:-5]

        return text

def schedule_dropdown_tag(parser, token):
    try:
        tag_name, user_str = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])

    return ScheduleDropdownNode(user_str)

class ScheduleDropdownNode(template.Node):
    def __init__(self, user_str):
        self.user_str = template.Variable(user_str)

    def render(self, context):
        try:
            user = self.user_str.resolve(context)
        except template.VariableDoesNotExist as e:
            print(e)
            return '<p>User not found!</p>'

        if not user.is_staff and user.worker.rank.rank != 'Ma':
            return ""

        s = "<ul>"

        if not user.is_staff and user.worker.rank.rank == 'Ma':
            s += "<li><a href='%s'>Admin</a></li>" % reverse('scheduler:schedule_admin')
            
        if user.is_staff or user.worker.rank.rank == 'Ma':
            s += "<li><a href='%s'>Attendance</a></li>" % reverse('scheduler:attendance')

        if user.is_staff:
            s += "<li><a href='%s'>Generate</a></li>" % reverse('scheduler:generate')

        s += "</ul>"
        
        return s

register.tag("unit_selector", unit_selector_form)
register.tag("markdown", markdown_tag)
register.tag("schedule_dropdown", schedule_dropdown_tag)
