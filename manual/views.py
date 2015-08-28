from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
##from django.core.exceptions import ObjectDoesNotExist
##from django.views import generic

##import django.contrib.auth.forms as authForms
##from django.contrib.auth import authenticate, login, logout
##from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
##create_user = User.objects.create_user
from django.template import Context, RequestContext

##from django.forms.models import model_to_dict, fields_for_model
##from django.db.models import Q
##from django.utils.datastructures import SortedDict

##import datetime
##from datetime import date
##from django.utils import timezone

##import random

##from scheduler.models import *
from scheduler.models import Record
##from scheduler.forms import *

from django.utils.safestring import mark_safe

from markdown2 import markdown
from datetime import timedelta

is_staff = lambda user: user.is_staff
is_active = lambda user: user.is_active

def get_toc(unit, reqUser, formattify=False, linkifyAll=False):
    try:
        f = open('manual/%s_table-of-contents.txt' % unit)
        lines = f.read().splitlines()
    ##    print(f.read())
        f.close()
    except FileNotFoundError:
        return ['in',
                (unit,
                 mark_safe('<h2>This unit does not have a manual yet.</h2>')),
                'out',
                ]

    def lcount(s, char): #counts the number of -char- characters at the left of string -s-
        t = 0
        while t < len(s) and s[t] == char:
            t += 1
        return t

    def treeprint(T, offset=''):
        S = []

        for t in T:
            if type(t) == list:
                for s in treeprint(t):
                    S.append(offset+' '+str(s))
            else:
                S.append(offset+str(t))

        return S

    stack = []
    n = 0
##    current = [tuple(map(lambda x:x.strip(), lines[0][1:].split(':')))]
    current = []
    formatting = []

    state = ''
    managerOnly = 0

    for line in lines:
        if len(line) == 0:
            continue
        elif line[0] == ';': #ignores comments
            continue
        elif line[0] == '<' and line[-1] == '>':
            state = line[1:-1]
            continue

        if state == 'formatting':
            L = lcount(line, '=')
            if len(formatting) > L:
                formatting[L] = line[L:].split(',')
            else:
                while len(formatting) < L:
                    formatting.append('','')
                formatting.append( line[L:].split(',') )
                
        elif state == 'TOC':
            L = lcount(line, '-')
##            print(L, line)

            if L > n:
                stack.append(current)
                n = L
                current = []
            elif L < n:
                while len(stack) > L:
                    stack[-1].append(current)
                    current = stack.pop()
                n = L

                if managerOnly and n <= managerOnly: managerOnly = 0

            if managerOnly: continue

            code, phrase = map(lambda x:x.strip(), line[n:].split(':'))

            if code[0] == "!" or phrase[0] == '!' or linkifyAll == True:
                offset = lcount(phrase, '!')
                kind = 'page' if offset else 'main'
                
                path = ""
##                print(stack)
                for s in stack:
##                    print(s[-1][0])
                    path += s[-1][0]+'/'
                path += code
##                print(path)

                rev_url = reverse('manual:'+kind, args=(path,))
                phrase = '['+phrase[offset:]+']('+str(rev_url)+')'

                if code[0] == "?": code = code[1:]
            elif phrase[0] == "?":
                print("Mmhmm...?")
                if not reqUser.is_staff and reqUser.worker.rank.rank != "Ma": #staff or managers
                    print("Eh?!?")
                    managerOnly = n
                    continue
                if code[0] == "?": code = code[1:]
                if phrase[0] == "?": phrase = phrase[1:]

            if formattify:
                phrase = formatting[n][0] + phrase + formatting[n][1]
            phrase = mark_safe( markdown(phrase) )
            
            current.append( (code, phrase) )

            #print(current, '\n\n', stack)
##            print('\n'.join( treeprint(stack) ))
##            print('\n'.join( treeprint(current, offset=' '*(len(stack)-1)) ))
##            print()

    while len(stack) > 0:
        stack[-1].append(current)
        current = stack.pop()

##    print(current)

##    print("\nFinal current:")
##    print('\n'.join( treeprint(current) ))
##
##    print("\nraw form:\n",current)

    def flatten(T):
        S = []
        S.append('in')

        for t in T:
            if type(t) == list:
##                S.append('in')
                for s in flatten(t):
                    S.append(s)
##                S.append('out')
            else:
                S.append(t)

        S.append('out')
        return S

    F = flatten(current)

    return F

# Create your views here.
@login_required
def main_view(request, path="", **kwargs):

    context = RequestContext(request)

    if path:
##        print("Path:",path)
        path_pieces = path.split('/')
        if path_pieces[0] != request.session['current_unit']:
            path_pieces = [request.session['current_unit']] + path_pieces
##        print(path_pieces)
    else:
        path_pieces = []

    F = get_toc(request.session['current_unit'], request.user, formattify=True)
##    print("\nFlattened form:",'\n'.join([str(f) for f in F]))

    P = []
    to_expand = [0]
    idx = 0
    
    for i in range(len(F)):
        if F[i] == 'in':
            P.append(i-1)

        if idx < len(path_pieces) and F[i][0] == path_pieces[idx]:
            to_expand.append(i+1)
            idx += 1

    context['P'] = P
    context['to_expand'] = to_expand

    context['flattened_tree'] = F

    return render(request, 'manual/table_of_contents.html', context)

@login_required
def page_view(request, path, **kwargs):
##    print(path)

    context = RequestContext(request)
    content = ""

    path_input = path

    context['parent'] = path[: path.rfind('/') ]

    path = path.replace('/','_')
    path = "manual/pages/" + path + ".txt"

##    print(path)

##    import os
##    print(os.listdir(os.getcwd()+"/manual/pages"))

    try:
        f = open(path)
    except FileNotFoundError:
        context['error_message'] = mark_safe("<p>I'm sorry, but this manual page could not be found.</p>")
        return render(request, 'manual/manual_page.html', context)
    else:
        blob = f.read()
        f.close()
##        content = markdown(blob)

    lines = blob.splitlines()

    ###SPLIT BLOB INTO { <text> | [<img>] } SECTIONS###
    rows = []
    beg = 0
    end = 0

    piece = ""
    building_piece = False

    page_toc = []

    for line in lines:
        if len(line) > 1 and line[:2] == '//': #single-line comment
            continue
        
        if line == '{':
            building_piece = True
            continue
        elif line == '}':
            building_piece = False
            if line != lines[-1]:
                continue

        if building_piece == False:
            if piece:
##                print(piece)
                rows[-1].append(mark_safe(markdown(piece)))
                piece = ""
                
            elif line and line[0] == '<' and line[-1] == '>':
                part1, part2 = map(lambda s:s.strip(), line[1:-1].split(":",1))
                part_id = part2.lower().replace(' ','_')

                try:
                    idx = ['Title', 'Section', 'Subsection'].index(part1)
                except ValueError:
                    idx = -1

                if idx > -1:
                    page_toc.append( [part_id, part2, mark_safe(2*idx*"&nbsp;"+"&ndash;")] )
                
                if part1 == 'Title':
                    part2 = "<h2 id=%s>%s</h2>" % (part_id, part2)
                elif part1 == 'Section':
                    part2 = "<h3 id=%s>%s</h3>" % (part_id, part2)
                elif part1 == 'Subsection':
                    part2 = "<p id=%s><strong>%s</strong></p>" % (part_id, part2)
                elif part1 == 'HTML':
##                    print("HTML!")
                    pass
                elif part1 in ('Tip','Note','Warning'):
                    part2 = markdown(part2)
                    part2 = part2[:2] + " class='%s'"%part1.lower() + part2[2:]
                else:
                    continue
                
                rows.append([mark_safe(part2)])
            elif line:
                if '<DjangoURL:' in line:
                    beg1 = line.find('<DjangoURL')
                    end1 = line.find('>', beg1)
                    beg2 = line.find('</DjangoURL>')
                    end2 = beg2 + len('</DjangoURL>')
##                    print(line[beg1:end2+1])
                    url_part = line[beg1:end1].split(':')[1].strip()
##                    print(url_part)
                    text = line[end1+1:beg2]
                    url_str = eval("reverse("+url_part+")")
##                    print(url_str)
                    line = line[:beg1] + '['+text+']('+url_str+')' + line[end2:]
##                    print(line)
                
                rows.append([mark_safe(markdown(line))])
##                print(rows[-1])
            else:
                if rows[-1] != mark_safe('<br/>'):
                    pass
##                    rows.append([mark_safe('')])
        else:
            if line == '|':
                rows.append([mark_safe(markdown(piece))])
                piece = ""
                continue
##            if line == '':
            piece += '\n'+line

    #convert "[Sign: ---]" into superscript linked numbers
    numSigns = 0
    for row in rows:
        for i,r in enumerate(row):
            if '[Sign:' in r:
                beg = 0
                end = 0
                s = r
                
                while r.find('[Sign:', beg) > -1:
                    beg = r.find('[Sign:', beg)
                    end = r.find(']', beg)
                    numSigns += 1

                    segment = r[beg:end+1]
                    segment_r = segment.replace('<em>','_').replace('</em>','_')

                    imgName = segment_r.replace('[Sign:','').replace(']','').strip()
                    imgSrc = "/static/pages/%s.gif" % imgName
                    tag = "<sup class='show_sign' onmouseover='loadImageNow(\"sign #%d\");'><a href="">#%d</a></sup><img data-src='%s' alt='sign #%d' id='sign #%d'/>" % (numSigns, numSigns, imgSrc, numSigns, numSigns)
                    
                    s = s.replace(segment,tag)

                    print(numSigns, segment_r)
                    
                    beg = end+1

##                s += r[beg:]
                print("s: %s"%s)
                row[i] = mark_safe(s)

    ###

    context['content'] = rows #mark_safe(content)

    context['flattened_tree'] = get_toc(request.session['current_unit'],
                                        request.user,
                                        linkifyAll=True)[1:-1]
    context['page_toc'] = page_toc

    if request.user.worker:
        records = request.user.worker.record_set
        records.filter(category='I', info='manual page viewed')

        record_found = False

        for record in records.all():
            lines = record.note.splitlines()
            if lines[0] == path_input:
                record_found = True
                count = str( int(lines[1])+1 )
                record.note = lines[0] + '\n' + count
                record.save()
                r = record
                break

        if record_found == False:
            new_record = Record()
            new_record.worker = request.user.worker
            new_record.category = 'I'
            new_record.info = 'manual page viewed'
            new_record.note = path_input + '\n' + '1'
            new_record.save()
            r = new_record

##        time_added = r.time_added
        time_added_str = "{:%B %d, %Y at %I:%M %p}".format(r.time_added - timedelta(hours=4))
        time_latest_str = "{:%B %d, %Y at %I:%M %p}".format(r.time_edited - timedelta(hours=4))
        count = int(r.note.splitlines()[1])
        context['record_info'] = 'You have viewed this page %d time%s since %s; last viewed %s.' % (count, ('s' if count-1 else ''), time_added_str, time_latest_str)

    return render(request, 'manual/manual_page.html', context)
