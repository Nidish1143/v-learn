from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from.models import Studreg,question,commends,quizans
from ilapp.models import subject1,course,department,faculty,log
from facultyapp.models import tutorial,quiz
from django.http import JsonResponse
from django.conf import settings
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from datetime import datetime
# Create your views here.
def studentreg(request):
    if request.method=='POST':
        s=Studreg()
        name=request.POST.get("name")
        gender=request.POST.get("gend")
        dob=request.POST.get("dob")
        adm=request.POST.get("admno")
        dpt=request.POST.get("dept")
        cou=request.POST.get("course")
        sem=request.POST.get("sem")
        email=request.POST.get("email")
        phno=request.POST.get("phno")
        uname=request.POST.get("uname")
        pwd=request.POST.get("pwd")
        s.name=name
        s.gender=gender
        s.dob=dob
        s.admno=adm
        s.dept=dpt
        s.course=cou
        s.semester=sem
        s.email=email
        s.phno=phno
        s.uname=uname
        s.pwd=pwd
        s.save()
        l=log()
        l.username=uname
        l.password=pwd
        l.utype='student'
        l.save()
        return HttpResponse("<script>alert('Registered successfully');window.location='/studentreg';</script>")
    else:
        s = subject1.objects.raw("SELECT ilapp_course.*,ilapp_department.* FROM ilapp_course,ilapp_department WHERE ilapp_course.id=ilapp_department.id")
        context = {'k':s}
        template = loader.get_template("studentreg.html")
        return HttpResponse(template.render(context, request))
def downloadtu(request):
    uname=request.session["uname"]
    s1=Studreg.objects.get(uname=uname)
    s=subject1.objects.raw("SELECT ilapp_subject1.id,ilapp_subject1.subject from ilapp_subject1,studentapp_studreg where ilapp_subject1.deptid=studentapp_studreg.dept and ilapp_subject1.courseid=studentapp_studreg.course and studentapp_studreg.id=%s",[s1.id])
    context = {'k':s}
    template = loader.get_template("tutorial.html")
    return HttpResponse(template.render(context, request))
def drop2(request):
    sid=request.POST.get("subject")
    t=tutorial.objects.filter(subid=sid)
    context = {'key': t}
    template = loader.get_template("download.html")
    return HttpResponse(template.render(context, request))
def dwn(request,id):
    t=tutorial.objects.get(id=id)
    t.nov=int(t.nov)+1
    t.save()
    st=str(t.upload)
    file_path = os.path.join(settings.MEDIA_ROOT, st)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.text")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
def cmd(request,id):
    request.session["tid"]=id
    context = {}
    template = loader.get_template("addcommends.html")
    return HttpResponse(template.render(context, request))
def cmd1(request):
    c=commends()
    uname=request.session["uname"]
    sid=Studreg.objects.get(uname=uname)
    c.sid=sid.id
    tid=request.session["tid"]
    c.tid=tid
    c.comm=request.POST.get("commend")
    c.save()
    return HttpResponse("<script>alert('Commends added successfully');window.location='/tutorial';</script>")
def stuviewans(request):
    uname=request.session["uname"]
    uid=Studreg.objects.get(uname=uname)
    q=quizans.objects.raw("SELECT facultyapp_quiz.id,facultyapp_quiz.ques,facultyapp_quiz.ans1,studentapp_quizans.ans from studentapp_studreg,studentapp_quizans,facultyapp_quiz where facultyapp_quiz.id=studentapp_quizans.qid and studentapp_quizans.sid=studentapp_studreg.id and studentapp_studreg.id=%s",[uid.id])
    context = {'key': q}
    template = loader.get_template("stuviewans.html")
    return HttpResponse(template.render(context, request))


def studenthome(request):
    context = {}
    template = loader.get_template("studenthome.html")
    return HttpResponse(template.render(context, request))
def ques(request):
    if request.method=='POST':
        q=question()
        sub=request.POST.get("sub")
        que=request.POST.get("ques")
        uname=request.session["uname"]
        s=Studreg.objects.get(uname=uname)
        q.subid=sub
        q.question=que
        q.sid=s.id
        q.status='pending'
        q.save()
        return HttpResponse("<script>alert('Question Submitted successfully');window.location='/questions';</script>")
    else:
        uname = request.session["uname"]
        s1 = Studreg.objects.get(uname=uname)
        s = subject1.objects.raw("SELECT ilapp_subject1.id,ilapp_subject1.subject from ilapp_subject1,studentapp_studreg where ilapp_subject1.deptid=studentapp_studreg.dept and ilapp_subject1.courseid=studentapp_studreg.course and studentapp_studreg.id=%s",[s1.id])

        context = {'k':s}
        template = loader.get_template("questions.html")
        return HttpResponse(template.render(context, request))
def answers(request):
    uname=request.session["uname"]
    uid=Studreg.objects.get(uname=uname)
    s=question.objects.raw("select studentapp_question.*,ilapp_subject1.subject from studentapp_studreg,studentapp_question,ilapp_subject1 where ilapp_subject1.id=studentapp_question.subid and studentapp_question.sid=studentapp_studreg.id and studentapp_studreg.id=%s",[uid.id])
    context = {'key':s}
    template = loader.get_template("viewanswer.html")
    return HttpResponse(template.render(context, request))
def search(request):
    if request.method=="POST":
        s=request.POST.get("search")
        s="%"+s+"%"
        s1=tutorial.objects.raw("SELECT facultyapp_tutorial.* from facultyapp_tutorial where facultyapp_tutorial.title LIKE %s ",[s])
        context = {'key':s1}
        template = loader.get_template("searchtutorial1.html")
        return HttpResponse(template.render(context, request))
    else:
        context = {}
        template = loader.get_template("searchtutorial.html")
        return HttpResponse(template.render(context, request))
def quiz1(request):
    today=datetime.now().date()
    if request.method=="POST":
        uname=request.session["uname"]
        uid=Studreg.objects.get(uname=uname)
        qid=request.POST.get("add")
        q=quizans()
        q.date=today
        q.sid=uid.id
        q.qid=qid
        q.ans=request.POST.get("opt"+qid)
        q.save()
        return HttpResponse("<script>alert('answered');window.location='/quiz1';</script>")
    else:
        uname = request.session["uname"]
        sid = Studreg.objects.get(uname=uname)
        #q=quiz.objects.raw("select facultyapp_quiz.* from facultyapp_quiz where facultyapp_quiz.id not in(select studentapp_quizans.qid from studentapp_quizans,studentapp_studreg where studentapp_quizans.sid=studentapp_studreg.id and studentapp_studreg.id=%s)",[sid.id])
        #q=quiz.objects.raw("SELECT * FROM facultyapp_quiz INNER JOIN studentapp_studreg ON facultyapp_quiz.dptid = studentapp_studreg.dept WHERE facultyapp_quiz.id NOT IN (SELECT studentapp_quizans.qid FROM studentapp_quizans INNER JOIN studentapp_studreg ON studentapp_quizans.sid = studentapp_studreg.id WHERE studentapp_studreg.id = %s)",[sid.id])
        q = quiz.objects.raw("SELECT facultyapp_quiz.* FROM facultyapp_quiz \
                              LEFT JOIN studentapp_studreg ON facultyapp_quiz.dptid = studentapp_studreg.dept \
                              LEFT JOIN studentapp_quizans ON facultyapp_quiz.id = studentapp_quizans.qid \
                              WHERE studentapp_quizans.qid IS NULL AND studentapp_studreg.id = %s", [sid.id])

        context = {'key':q}
        template = loader.get_template("Quizreg.html")
        return HttpResponse(template.render(context, request))




def viewvideo(request,id):
    s=tutorial.objects.get(id=id)
    context = {'k':s}
    template = loader.get_template("playvideo.html")
    return HttpResponse(template.render(context, request))


