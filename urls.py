from  django.urls import path
import studentapp.views
urlpatterns = [

    path('studentreg/',studentapp.views.studentreg,name='studentreg'),
    path('tutorial/',studentapp.views.downloadtu,name='tutorial'),
    path('studenthome/',studentapp.views.studenthome,name='studenthome'),
    path('questions/',studentapp.views.ques,name='questions'),
    path('viewanswer/',studentapp.views.answers,name='viewanswer'),
    path('drop2/',studentapp.views.drop2,name='drop2'),
    path('dwn/<id>',studentapp.views.dwn,name='dwn'),
    path('cmd/<id>', studentapp.views.cmd, name='cmd'),
    path('cmd1/', studentapp.views.cmd1, name='cmd1'),
    path('search/', studentapp.views.search, name='search'),
    path('quiz1/', studentapp.views.quiz1, name='quiz1'),
    path('stuviewans/', studentapp.views.stuviewans, name='stuviewans'),
    path('viewvideo/<id>', studentapp.views.viewvideo, name='viewvideo')

]