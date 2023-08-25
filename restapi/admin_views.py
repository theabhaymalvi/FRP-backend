from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import JobSerializer,application_Serializer,UserLoginSerializer,dept_Serializer,spez_Serializer,post_Serializer
from .models import job,User,application,spez,department,post
from .views import register,authuser,authMMe,authCce,authCse,authEce,authDofa,authAdmin
from django.db.models.query import QuerySet
from .generateMeet import sendMail




@api_view(['POST'])
def create_job(request):
    dept_id = request.data.get("dept")
    depart  = department.objects.get(id=dept_id)
    code = depart.code
    user=None
    if code == 'cse':
        print("auth tried")
        user = authCse(request)
    if code == 'ece':
        user = authEce(request)
    if code == 'cce':
        user = authCce(request)
    if code == 'mec':
        user = authMMe(request)
    if user:
        jb =job.objects.filter(dept=dept_id,post=request.data.get("post"),spez_Req=request.data.get("spez_Req"))
        if jb:
            return Response({"error":"Job with these specifications already exists"},400)
        dept = department.objects.filter(id=dept_id).first()
        js = JobSerializer(data=request.data)
        print(dept.id)
        if js.is_valid():
            jb=js.save()
        else:
            return Response(js.errors,400)
        
        return Response(jb.dept.name)
    else:
        return Response({"error":"Admin Authorization Failure"},401)

@api_view(['POST'])
def delete_job(request):
    jb = job.objects.get(id=request.data.get("id"))
    print(jb.dept)
    dept_id = jb.dept.id
    depart  = department.objects.get(id=dept_id)
    code = depart.code
    user=None
    if code == 'cse':
        print("auth tried")
        user = authCse(request)
    if code == 'ece':
        user = authEce(request)
    if code == 'cce':
        user = authCce(request)
    if code == 'mec':
        user = authMMe(request)
    if user:
        jb.delete()
        return Response({"success":"Job deleted"})
        
    else:
        return Response({"error":"Admin Authorization Failure"},401)
        



@api_view(['POST'])
def nextRnd(request):
    app=application.objects.filter(id=request.data.get("id")).first()
    jb = job.objects.get(id=app.job.id)
    dept_id = jb.dept.id
    depart  = department.objects.get(id=dept_id)
    code = depart.code
    user=None
    if code == 'cse':
        print("auth tried")
        user = authCse(request)
    if code == 'ece':
        user = authEce(request)
    if code == 'cce':
        user = authCce(request)
    if code == 'mec':
        user = authMMe(request)
    if user:
        app.roundNum+=1
        app.save()
        return Response({"success":"Round updated to "+str(app.roundNum)})
    else:
        return Response({"error":"Admin Authorization Failure"},401)

@api_view(['POST'])
def schedule(request):
    app=application.objects.filter(id=request.data.get("id")).first()
    jb = job.objects.get(id=app.job.id)
    dept_id = jb.dept.id
    depart  = department.objects.get(id=dept_id)
    code = depart.code
    user=None
    if code == 'cse':
        print("auth tried")
        user = authCse(request)
    if code == 'ece':
        user = authEce(request)
    if code == 'cce':
        user = authCce(request)
    if code == 'mec':
        user = authMMe(request)
    if user:

        app.schedule = request.data.get("datetime")
        app.save()
        return Response({"success":"Schedule Updated "+request.data.get("datetime")})
    else:
        return Response({"error":"Admin Authorization Failure"},401)


@api_view(['GET'])
def getSchedule(request):
    app=application.objects.filter(id=request.data.get("id")).first()
    jb = job.objects.get(id=app.job.id)
    dept_id = jb.dept.id
    depart  = department.objects.get(id=dept_id)
    code = depart.code
    user=None
    if code == 'cse':
        print("auth tried")
        user = authCse(request)
    if code == 'ece':
        user = authEce(request)
    if code == 'cce':
        user = authCce(request)
    if code == 'mec':
        user = authMMe(request)
    if user:
        return Response({"success":"updated schedule -"+str(app.schedule)})
    else:
        return Response({"error":"Admin Authorization Failure"},401)

@api_view(['GET'])
def Fetch_Jobs(request):
    jobs = QuerySet(job)
    user = authCse(request)
    if user:
        jobs|=job.objects.filter(dept=department.objects.filter(code="cse").first())
    user=None
    user = authEce(request)
    if user:
        jobs|=job.objects.filter(dept=department.objects.filter(code="ece").first())
    user=None
    user = authCce(request)   
    if user:
        jobs|=job.objects.filter(dept=department.objects.filter(code="cce").first())
    user=None
    user = authMMe(request)
    if user:
        jobs|=job.objects.filter(dept=department.objects.filter(code="mec").first())
    user=None
    if len(jobs):
        return Response(JobSerializer(jobs,many=True).data)
    else:
        return Response({"error":"Admin Authorization Failure"},401)


@api_view(['GET'])
def Fetch_applications(request):
    user = None
    id=request.query_params.get("id")
    jb = job.objects.filter(id=id).first()
    dept_id=jb.dept.id
    depart  = department.objects.get(id=dept_id)
    code = depart.code
    user=None
    if code == 'cse':
        print("auth tried")
        user = authCse(request)
    if code == 'ece':
        user = authEce(request)
    if code == 'cce':
        user = authCce(request)
    if code == 'mec':
        user = authMMe(request)
    if user:
        cand = application.objects.filter(job=jb)
        return Response(application_Serializer(cand,many=True).data)
    else:
        return Response({"error":"Admin Authorization Failure"},401)

@api_view(['GET'])
def Reject(request):
    app=application.objects.filter(id=request.data.get("id")).first()
    jb = job.objects.get(id=app.job.id)
    dept_id = jb.dept.id
    depart  = department.objects.get(id=dept_id)
    code = depart.code
    user=None
    if code == 'cse':
        print("auth tried")
        user = authCse(request)
    if code == 'ece':
        user = authEce(request)
    if code == 'cce':
        user = authCce(request)
    if code == 'mec':
        user = authMMe(request)
    if user:
        app.delete()
        return Response({"success":"Application Deleted"})
    else:
        return Response({"error":"Admin Authorization Failure"},401)


@api_view(['POST'])
def add_dept(request):
    user = authDofa(request)
    ds = dept_Serializer(data=request.data)
    if user and ds.is_valid():
        ds.save()
        return Response(ds.data)
    else:
        if user:
            return Response(ds.errors,400)
        else:
            return Response({"error":"DOFA Authorization Failure"},401)


@api_view(['POST'])
def add_spez(request):
    user = authDofa(request)
    ss = spez_Serializer(data=request.data)
    if user and ss.is_valid():
        ss.save()
        return Response(ss.data)
    else:
        if user:
            return Response({"error":str(ss.errors)},400)
        else:
            return Response({"error":"DOFA Authorization Failure"},401)

@api_view(['POST'])
def send_mail(request):
    app=application.objects.filter(id=request.data.get("id")).first()
    jb = job.objects.get(id=app.job.id)
    dept_id = jb.dept.id
    depart  = department.objects.get(id=dept_id)
    code = depart.code
    user=None
    if code == 'cse':
        print("auth tried")
        user = authCse(request)
    if code == 'ece':
        user = authEce(request)
    if code == 'cce':
        user = authCce(request)
    if code == 'mec':
        user = authMMe(request)
    if user:
        app.meet = request.data.get("meet")
        app.save()
        dt = str(app.schedule.date()).strip().split("-")
        y=dt[0]
        m=dt[1]
        d=dt[2]
        date=d+"/"+m+"/"+y
        body="Dear "+app.name+",\nWe are glad to inform you that your application matches our requirements and we would like to know you better. Following are the details for the online meet session.\nDate - "+date+"\nTime - "+str(app.schedule.time())+"\nLink - "+app.meet
        send = app.user.email
        subject="Regarding your Job Application in LNMIIT"
        sendMail(body,send,subject=subject)
        return Response({"success":"email send"})
    else:
        return Response({"error":"Admin Authorization Failure"},401)

@api_view(['POST'])
def addPost(request):
    user = authDofa(request)
    if user:
        ps = post_Serializer(data=request.data)
        if ps.is_valid():
            ps.save()
            return Response({"success":"post created"})
        else:
            return Response({"error":str(ps.errors)},400)
    else:
            return Response({"error":"DOFA Authorization Failure"},401)
    
@api_view(['GET'])
def getPosts(request):
    user = authAdmin(request)
    if user:
        posts = post.objects.all()
        return Response(post_Serializer(posts, many=True).data)
    else:
        return Response({"error":"Admin Authorization Failure"},401)

@api_view(['POST'])
def delPost(request):
    user = authDofa(request)
    if user:
        pst = post.objects.filter(name=request.data.get("name")).first()
        pst.delete()
        return Response({"success":"post deleted"})
    else:
            return Response({"error":"DOFA Authorization Failure"},401)


def updateMeetLink(request):
    app=application.objects.filter(id=request.data.get("id")).first()
    
    
