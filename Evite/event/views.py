# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import EventForm,RSVPForm,FEEDBACKForm
from django.contrib.auth.decorators import login_required
import pymysql
from django.http import HttpResponseRedirect
import uuid
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from django.contrib import messages

# Create your views here.

eventid = 0

def rsvp(request,guid):
    if request.method == 'POST':
        form = RSVPForm(request.POST)
        if form.is_valid():
            comingornot = form.cleaned_data['Coming_to_party']
            noofguest = form.cleaned_data['no_of_guests']
            con = pymysql.connect(host='localhost',
                                user='root',
                                password='9853155341',
                                db='evite')
            cur = con.cursor()
            cur.execute("update invitation set rsvp = %s, additionalGuest = %s where guid = %s" , [comingornot,noofguest,guid])
            con.commit()
            return render(request, 'event/thankyou.html',{})
        else:
            #form = RSVPForm()
            return render(request, 'event/form1.html', {'form': form})
    else:
        form = RSVPForm()
        return render(request, 'event/form1.html', {'form': form})
        
def feedback(request,guid):
    if request.method == 'POST':
        form = FEEDBACKForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            rating = form.cleaned_data['rating']
            con = pymysql.connect(host='localhost',
                                user='root',
                                password='9853155341',
                                db='evite')
            cur = con.cursor()
            cur.execute("update feedback set comment = %s, feedbackrating = %s where guid = %s" , [comment,rating,guid])
            con.commit()
            return render(request, 'event/thankyou1.html',{})
        else:
            #form = RSVPForm()
            return render(request, 'event/form2.html', {'form': form})
    else:
        form = FEEDBACKForm()
        return render(request, 'event/form2.html', {'form': form})
        
@login_required
def event(request):
    con = pymysql.connect(host='localhost',
                                user='root',
                                password='9853155341',
                                db='evite')
    cur = con.cursor()
    current_user = request.user
    cur.execute("select * from event where userId = %s" , [current_user.id])
    result = cur.fetchall()
    eventlist = []
    for row in result:
        #date_dict = { i:row }
        eventlist.append(row)

    event_dict = {"key":eventlist}
    rsvpsent = 'N'
    return render(request, 'event/event.html',event_dict)

@login_required
def details(request,pk):
    
    con = pymysql.connect(host='localhost',
                                user='root',
                                password='9853155341',
                                db='evite')
    cur = con.cursor()
    #To get the event details
    cur.execute("select * from event where eventID = %s" , [pk])
    result = cur.fetchone()
    pk1 = result[0]
    
    #To get the invitation details
    cur.execute("select count(*),COALESCE(sum(additionalGuest),0) from invitation where eventID = %s and RSVP = 'Y'" , [pk1])
    result1 = cur.fetchone()
    #To get the feedback details
    cur.execute("select avg(feedbackrating) from feedback where eventID = %s and feedbackrating != 0", [pk1])
    result2 = cur.fetchone()
    #To get the no of people yet to RSVP
    cur.execute("select count(*) from invitation where eventID = %s and RSVP = 'N'" , [pk1])
    result3 = cur.fetchone()
    
    #To get all the email ids
    cur.execute("select emailId,RSVP from invitation where eventID = %s" , [pk1])
    result4 = cur.fetchall()
    print(result4)
    details_dict = {"key":result,"headcount":(result1[0]+int(result1[1])),"rating":result2[0],"nrsvp":result3[0],"eventid":pk,"email":result4}
    return render(request, 'event/details.html',details_dict)
    
@login_required  
def add(request):

    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            
            title = form.cleaned_data['title']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            description = form.cleaned_data['description']
            maxinvites = form.cleaned_data['maxinvites']
            maxGuests = form.cleaned_data['maxGuests']
            location = form.cleaned_data['location']
            clubname = form.cleaned_data['clubname']
            current_user = request.user
            
            con = pymysql.connect(host='localhost',
                                user='root',
                                password='9853155341',
                                db='evite')
            
            add_event = ("INSERT INTO event (date, time, description, title, maxInvites,"
            "maxGuests, userId, location, clubId )"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
            pk_list = (date,time,description,title,maxinvites,maxGuests,current_user.id,location,clubname)
            cur = con.cursor()
            cur.execute(add_event,pk_list)
            con.commit()
            
            return HttpResponseRedirect('/event')

    else:
        form = EventForm()
        #form = Choice()

    return render(request, 'event/form.html', {'form': form})

@login_required 
def edit(request,eventid):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            
            title = form.cleaned_data['title']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            description = form.cleaned_data['description']
            maxinvites = form.cleaned_data['maxinvites']
            maxGuests = form.cleaned_data['maxGuests']
            location = form.cleaned_data['location']
            clubname = form.cleaned_data['clubname']
            
            con = pymysql.connect(host='localhost',
                                user='root',
                                password='9853155341',
                                db='evite')
            
            update_event = ("UPDATE event SET date = %s, time = %s, description = %s, title = %s, maxInvites = %s,"
            "maxGuests = %s, location = %s, clubId = %s WHERE eventId = %s")
            pk_list = (date,time,description,title,maxinvites,maxGuests,location,clubname,eventid)
            cur = con.cursor()
            print(update_event)
            cur.execute(update_event,pk_list)
            con.commit()
            
            return HttpResponseRedirect('/event')
        
    else:
        #To find clubid for the eventid
        con = pymysql.connect(host='localhost',
                                user='root',
                                password='9853155341',
                                db='evite')
        cur = con.cursor()
        cur.execute("select clubId,title,date,time,description,maxInvites,maxGuests,location,clubId from event where eventId = %s" , [eventid])
        result = cur.fetchone()
        form = EventForm(initial={'title':result[1],'date':result[2],'time':result[3],
        'description':result[4],'maxinvites':result[5],'maxGuests':result[6],'location':result[7],'clubId':result[8]})
        print("R5:"+str(result[5]))
        print("R6:"+str(result[6]))
        return render(request, 'event/formupdate.html', {'form': form})
    
@login_required  
def send(request,eventid):

            #To find clubid for the eventid
            con = pymysql.connect(host='localhost',
                                user='root',
                                password='9853155341',
                                db='evite')
            cur = con.cursor()
            cur.execute("select clubId,title,date,time,location from event where eventId = %s" , [eventid])
            result = cur.fetchone()
            clubid = result[0]
            eventname = result[1]
            date = result[2]
            time = result[3]
            location = result[4]
            

            #To find emails for the club id
            con1 = pymysql.connect(host='localhost',
                                user='root',
                                password='9853155341',
                                db='evite')
            cur1 = con1.cursor()
            cur1.execute("select email from auth_user where id in (select userId from member where clubId = %s)" , [clubid])
            result1 = cur1.fetchall()
            
            #To insert all the invitation in invitation table   
            con2 = pymysql.connect(host='localhost',
                                user='root',
                                password='9853155341',
                                db='evite')
            cur2 = con2.cursor()
            add_event = ("INSERT INTO invitation (eventId, emailId, guid)"
            "VALUES (%s, %s, %s)")
            add_review = ("INSERT INTO FEEDBACK (eventID,emailId,guid)"
            "VALUES (%s, %s, %s)")
            for emailid in result1:
                guid = uuid.uuid4().hex[:32]
                pk_list = (eventid,emailid[0],guid)
                cur2.execute(add_event,pk_list)
                cur2.execute(add_review,pk_list)
                con2.commit()
                subject = "Event Invitation"
                to = [emailid[0]]
                from_email = 'aloksn4u1@gmail.com'
                ctx = {
                'guid': guid,
                'eventname': eventname,
                'date': date,
                'time': time,
                'location': location,
                }
                message = get_template('event/email.html').render(ctx)
                msg = EmailMessage(subject, message, to=to, from_email=from_email)
                msg.content_subtype = 'html'
                msg.send()
            messages.success(request, 'Invitation emails sent successfully!')    
            return HttpResponseRedirect('/event')
            
@login_required  
def sendr(request,eventid):
            
            print(eventid)
            #To find title for the eventid
            con = pymysql.connect(host='localhost',
                                user='root',
                                password='9853155341',
                                db='evite')
            cur = con.cursor()
            cur.execute("select title from event where eventId = %s" , [eventid])
            result = cur.fetchone()
            title = result[0]
            print(title)
            #To find clubid for the eventid
            con1 = pymysql.connect(host='localhost',
                                user='root',
                                password='9853155341',
                                db='evite')
            cur1 = con1.cursor()
            cur1.execute("select emailId, guid from feedback where eventId = %s" , [eventid])
            result = cur1.fetchall()
            for row in result:
                subject = "Event Feedback"
                to = [row[0]]
                print(to)
                from_email = 'aloksn4u1@gmail.com'
                ctx = {
                'guid': row[1],
                'eventname': title,
                }
                message = get_template('event/emailfeedback.html').render(ctx)
                msg = EmailMessage(subject, message, to=to, from_email=from_email)
                msg.content_subtype = 'html'
                msg.send()
            
            messages.success(request, 'Feedback emails sent successfully!')      
            return HttpResponseRedirect('/event')
            
@login_required  
def delete(request,eventid):

            #To delete an event
            con = pymysql.connect(host='localhost',
                                user='root',
                                password='9853155341',
                                db='evite')
            cur = con.cursor()
            cur.execute("delete from event where eventId = %s" , [eventid])
            con.commit()
                  
            return HttpResponseRedirect('/event')

def signup(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/event')

    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})