from asyncio.windows_events import NULL
from typing import final
from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from matplotlib import gridspec
from numpy import searchsorted
from pymongo import MongoClient
from email import message
from email.policy import HTTP
from lib2to3.pgen2.tokenize import generate_tokens
import re

import datetime
import pytz
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from gfg import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode 
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from django.core.mail import EmailMessage, send_mail
from django.utils.http import urlsafe_base64_decode
from neo4j import GraphDatabase

import requests
from authentication.models import Contribute
import cdata.zohocrm as mod1
import cdata.freshdesk as mod2
import cdata.salesforce as mod3
import cdata.jira as mod4



gfName=""
uniqueId=""
uName=""
ppsummary=""
ppdescription=""
pproducts=[]
pkanalysis=""
pkinsisghts=""
powner=""
pptype=""


taggs=dict()
finaltags=[]
uniqueId2=""

# Create your views here.
def index(request):
    conn = MongoClient()
    db=conn.Lucid
    collection=db.knowledge
    coll =collection.find()
    return render(request, "authentication/index.html", {'defectdata': coll.clone()})

def about(request):
    return render(request, 'authentication/about.html') 

def signup(request):
    
    if request.method == "POST":
        # global username 
        username = request.POST.get('username')
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username")
            return redirect('home')
            
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('home')
        
        # if len(username)>10:
        #     messages.error(request, "Username must be under 10 characters")
            
            
        # if not username.isalnum():
        #     messages.error(request, "Username must be Alpha-Numeric!")
        #     return redirect('home')
        
     
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        
        messages.success(request, " We have sent account activation link to your registered mail id. Kindly click on the link to activate your account .")
        
        
        #welcome email
        
        subject = "Welcome to Knowledge Platform - Login Page!"
        message = "Hello " + myuser.first_name + "! \n" + "Welcome to Knowledge Platform!  \n Thank You for visiting our website \n We have also sent you a confirmation email, Please confirm your email address in order to activate yor account. \n\n Regards\n Team Knowledge Platform"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        
        #Email Address confirmation email
        
        current_site = get_current_site(request)
        email_subject = "Confirm your email @ Knowledge Platform - Django Login"
        message2 = render_to_string('email_confirmation.html',{
            'name':myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('signin')
    
    return render(request, "authentication/signup.html")


def delete_account(request):
    global uName
    print(uName)
    user = User.objects.get(username = uName)
    user.delete()
    messages.success(request, "Account Deleted Successfully")
    subject = "Account Deleted Successfully!!"
    message = "Hello " + user.first_name + "! \n" + "Your Account has been successfully deleted from our Platform.  \nThank You for using our Platform. We hope you definitely got a great experience of using our platform. \nHope to See you soon. \n\n Regards\n Team Knowledge Platform"
    from_email = settings.EMAIL_HOST_USER
    to_list = [user.email]
    send_mail(subject, message, from_email, to_list, fail_silently=True)
    return redirect('home')

def contribute(request):
    if request.method == "POST":
        ptype=request.POST['ptype']
        psummary=request.POST['psummary']
        pdescription=request.POST['pdescription']
        global ppsummary 
        global ppdescription
        ppsummary = psummary
        ppdescription = pdescription
        products=request.POST.getlist('CD')
        kanalysis=request.POST['kanalysis']
        kinsisghts=request.POST['kinsisghts']
        #tags=request.POST['tags']
        owner=request.POST['owner']     
        global pproducts, pkanalysis,pkinsisghts,powner,pptype, finaltags
        pproducts=products
        pkanalysis=kanalysis
        pkinsisghts=kinsisghts
        powner=owner
        pptype=ptype
        datetime_entry = datetime.datetime.now() 
        # username = request.session.get('username') 
        #contr=Contribute(ptype=ptype,psummary=psummary,pdescription=pdescription,products=products,kanalysis=kanalysis,kinsisghts=kinsisghts,tags=tags,owner=owner)
        contr=Contribute(ptype=ptype,psummary=psummary,pdescription=pdescription,products=products,kanalysis=kanalysis,kinsisghts=kinsisghts,owner=owner)
        contr.save()
        conn = MongoClient()
        db=conn.Lucid
        collection=db.knowledge
        # username=signup.username
        
        # # if datetime_logout1 is None:
        #     datetime_logout1=0  
        rec1={
        #   "username":username1,          
          "ptype":ptype,
          "psummary":psummary,
          "pdescription":pdescription,
          "products":products,
          "kanalysis":kanalysis,
          "kinsisghts":kinsisghts,
          "tags":finaltags,
          "owner":owner,
          "ID" : owner[:3] + str(len(psummary)) + str(len(pdescription)) +str(len(kinsisghts) + len(kanalysis)),          

       
        }
        global uniqueId2
        uniqueId2=owner[:3] + str(len(psummary)) + str(len(pdescription)) +str(len(kinsisghts) + len(kanalysis))
        collection.insert_one(rec1)
        tags_string=""
        for i in finaltags:
            tags_string+=i+","   
        print(finaltags,"finaaaaaaaaal",tags_string)     

        # #added neo4j database
       
        graphdb=GraphDatabase.driver(uri = "bolt://localhost:7687", auth=("neo4j", "admin"))
        session=graphdb.session()
        q2='''Merge (kp:knowledge {pdescription: '%s', ptype: '%s', psummary: '%s',id: '%s' , kanalysis:'%s', kinsisghts:'%s', owner:'%s', products:'%s'})
        WITH kp
        UNWIND split('%s',',') AS tag
        MERGE (t:tags_string {tagname: tag})
        MERGE (kp)-[:belongs_to]->(t)'''%(pdescription,ptype,psummary,uniqueId2,kanalysis,kinsisghts,owner,*products,finaltags)
        q5="drop index kpindex"
        q6="drop index rindex"
        q3="CREATE FULLTEXT INDEX kpindex FOR (n: knowledge|tags) ON EACH [n.ptype, n.pdescription,n.owner,n.kanalysis, n.kinsisghts,n.products,n.tags]"
        q4="CREATE FULLTEXT INDEX rindex FOR ()-[r:belongs_to]-() ON EACH [r.tagname]"
        q1=" match(n) return n "
    
        session.run(q2)
        session.run(q5) 
        session.run(q6)
        session.run(q3)
        session.run(q4)
        session.run(q1)

        messages.success(request, 'Your message has been sent!')
        return redirect('filltags')
    return render(request, 'authentication/contribute.html')

def contribute_neo4j(request):
    global ppdescription,ppsummary,pproducts, pkanalysis,pkinsisghts,powner,pptype, uniqueId2,finaltags
    final_Tags=""
    for i in finaltags:
        final_Tags+=i+","
    

    if request.GET.get("contributeneo"):
        #added neo4j database
        neo4j_create_statemenet = "create (a: Problem{name:'%s'}), (k:Owner {owner:'%s'}), (l:Problem_Type{type:'%s'}),(m:Problem_Summary{summary:'%s'}), (n:Probelm_Description{description:'%s'}),(o:Knowledge_Analysis{analysis:'%s'}), (p:Knowledge_Insights{kinsisghts:'%s'}), (a)-[:Owner]->(k), (a)-[:Problem_Type]->(l), (a)-[:Problem_Summary]->(m), (a)-[:Problem_Description]->(n), (a)-[:Knowledge_analysis]->(o), (a)-[:Knowledge_insights]->(p)"%("Problem",powner,pptype,ppsummary,ppdescription,pkanalysis,pkinsisghts)
        graphdb=GraphDatabase.driver(uri = "bolt://localhost:7687", auth=("neo4j", "admin"))
        session=graphdb.session()
        q2='''Merge (kp:knowledge {pdescription: '%s', ptype: '%s', psummary: '%s',id: '%s' , kanalysis:'%s', kinsisghts:'%s', owner:'%s', products:'%s'})
        WITH kp
        UNWIND split('%s',',') AS tag
        MERGE (t:final_Tags {tagname: tag})
        MERGE (kp)-[:belongs_to]->(t)'''%(ppdescription,pptype,ppsummary,uniqueId2,pkanalysis,pkinsisghts,powner,*pproducts,final_Tags[:-1])
        q1=" match(n) return n "

        session.run(q2)
        session.run(q1)
        return redirect("home")
    return redirect(request,'authentication/filltags.html')

def defects(request):
    conn = MongoClient()
    db=conn.Lucid
    collection=db.knowledge
    defectdata =collection.find({'ptype':'defect'})
    return render(request, 'knowledgepages/defects.html', {'defectdata': defectdata.clone()}) 
global searched
# def defect(request):
#     conn = MongoClient()
#     db=conn.Lucid
#     collection=db.knowledge
#     if request.method=="POST":
#         searched=request.POST['searched']
#     graphdb=GraphDatabase.driver(uri = "bolt://localhost:7687", auth=("neo4j", "admin"))
#     session=graphdb.session()
#     q3='''CALL db.index.fulltext.queryNodes("kpindex", %s) YIELD node, score RETURN node.ptype,node.id,node.owner node.pdescription, score''' %(searched)
#     nodes=session.run(q3)
   
#     return render(request, 'knowledgepages/defect.html', {'nodes': nodes}) 

def enhancements(request):
    conn = MongoClient()
    db=conn.Lucid
    collection=db.knowledge
    enhancementdata =collection.find({'ptype':'enhancement'})
    return render(request, 'knowledgepages/enhancements.html', {'enhancementdata': enhancementdata.clone()})

def supportticket(request):
    conn = MongoClient()
    db=conn.Lucid
    collection=db.knowledge
    supportdata =collection.find({'ptype':'supportticket'})
    return render(request, 'knowledgepages/supportticket.html', {'supportdata': supportdata.clone()})

def opportunity(request):
    conn = MongoClient()
    db=conn.Lucid
    collection=db.knowledge
    opportunitydata =collection.find({'ptype':'opportunity'})
    return render(request, 'knowledgepages/opportunity.html', {'opportunitydata': opportunitydata.clone()})


global fname
def signin(request):       
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        global uName
        uName=username
        
    #below we are doing user authentication  
      
        user = authenticate(username=username, password=pass1)   
         
        if user is not None:
             login(request, user)
             fname = user.first_name
             global gfName
             if '@' in fname:
                s=fname.split('@')
                gfName=s[0].capitallize()
             else:
                gfName=fname
            #  gfName+=str(fname)
             current_user = {}
             global username1
             username1=username
             datetime_login = datetime.datetime.now()
             global datetime_login1
             datetime_login1=datetime_login
             return render(request, "authentication/index.html", {'fname': fname})
             
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('signin')
    
    
    return render(request, "authentication/signin.html")



def signout(request):
    logout(request)
    datetime_logout = datetime.datetime.now()
    global datetime_logout1
    datetime_logout1=datetime_logout
    messages.success(request, "Logged Out Successfully")
    return redirect('home')

def activate(request, uidb64, token):
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
        
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')

def freshdesk(request):
    conn = mod2.connect("Domain=knowledgeplatform;  APIKey=OZ1JWc0QQielVNhYIFQ3;")
    cmd = "SELECT Id, Subject, Description FROM Tickets"
    cur = conn.execute(cmd)
    rs = cur.fetchall()
    for row in rs:
    	print(row)

    global d1
    d1 = {'Id':[], 'Subject':[]}

    for t in rs:
        print("Hello")
        d1['Id'].append(t[0]);
        d1['Subject'].append(t[1]);
    print(d1)

    return render(request,'knowledgepages/freshdesk.html')

def freshdeskdisplay(request):
    ml=zip(d1['Id'],d1['Subject'])
    context={'ml':ml,}
    return render(request,'knowledgepages/freshdeskdisplay.html',context)



def jira(request):
    conn = mod4.connect("User=mangalyogesh.22@gmail.com;APIToken=el2xmpup6oRO1ZNcJhWtE902;Url=https://knowledgeplatform.atlassian.net")
    cur = conn.execute("SELECT Id, Name, Key FROM Projects")
    rs = cur.fetchall()
    for row in rs:
        print(row)


    global d
    d = {'Id':[], 'Name':[], 'Key':[]}

    for t in rs:
        # print("Hello")
        d['Id'].append(t[0]);
        d['Name'].append(t[1]);
        d['Key'].append(t[2])
    print(d)

    return render(request,'knowledgepages/jira.html')


def jiradisplay(request):
    ml=zip(d['Id'],d['Name'],d['Key'])
    context={'ml':ml,}
    return render(request,'knowledgepages/jiradisplay.html',context)


def salesforce(request):
    conn = mod3.connect("User='af@gcet.com';Password='admin123';Security Token='G7wSptekqNONY1L3hBSs9T27';")
    cur = conn.execute("SELECT Name,BillingState, Id FROM Account")
    rs = cur.fetchall()
    print(rs)
    for row in rs:
        print(row)
    
    global d2
    d2 = {'name':[], 'billingState':[], 'id' : []}

    for t in rs:
        print("Hello")
        d2['name'].append(t[0]);
        d2['billingState'].append(t[1]);
        d2['id'].append(t[2])

    return render(request, 'knowledgepages/salesforce.html')          


 


def salesforcedisplay(request):
    mlt=zip(d2['name'],d2['billingState'],d2['id'])
    context={'mlt':mlt,}
    return render(request, 'knowledgepages/salesforcedisplay.html',context)



def search(request):
    # conn = MongoClient()
    # db=conn.Lucid
    # collection=db.knowledge
    if request.method=="POST":
        searched=request.POST['searched']
    graphdb=GraphDatabase.driver(uri = "bolt://localhost:7687", auth=("neo4j", "admin"))
    session=graphdb.session()
    q3='''CALL db.index.fulltext.queryNodes("kpindex", "%s") YIELD node RETURN node''' %(searched)
    nodes=session.run(q3) 
    # print(*nodes)
    # we are showing results on page name defect
    return render(request, 'knowledgepages/defect.html', {'nodes': nodes}) 

def your_Contribution(request):
    conn = MongoClient()
    db=conn.Lucid
    collection=db.knowledge
    
    
    owner = gfName
    print(owner)
    #login=Contribute.objects.filter(ptype__contains=searched) 
    defectdata =collection.find({'owner':owner})
    # return render(request, 'knowledgepages/defects.html', {'defectdata': defectdata.clone()}) 
    return render(request,'authentication/your_contribution.html',{'defectdata': defectdata.clone()})


def Zoho(request):
    mod1.connect("InitiateOAuth=GETANDREFRESH;") 
    return render(request, "authentication/zoho.html")   


def update_contribution(request):
    conn=MongoClient()
    db=conn.Lucid
    collection=db.knowledge
    if request.method=="POST":
        kid=request.POST['kid']
        global uniqueId
        uniqueId=kid
    return render(request,'authentication/update_contribution.html')    


def update_contribution_display(request):
    global uniqueId
    print(uniqueId)
    conn = MongoClient()
    db=conn.Lucid
    collection=db.knowledge
    ourdata = collection.find({'ID':uniqueId})
    return render(request,'authentication/update_contribution_display.html',{'ourdata':ourdata.clone()})

def update_data(request):
    global uniqueId
    print("Inside update function",uniqueId)
    conn = MongoClient()
    db=conn.Lucid
    collection=db.knowledge
    udata=collection.find({'ID':uniqueId})
    d={'udata':udata.clone()}
    for x in d['udata']:
        # print(x['ptype'])
        # print(x['psummary'])
        p1=x['ptype']
        p2=x['psummary']
        p3=x['pdescription']
        p4=x['products']
        p5=x['kanalysis']
        p6=x['kinsisghts']
        p7=x['tags']
    if request.method=="POST":
        ptype=request.POST['ptype']
        print(ptype,"ptype h ye")
        if(ptype=="Problem Type"):
            ptype=p1
        psummary=request.POST['psummary']
        if(psummary==""):
            psummary=p2
        pdescription=request.POST['pdescription']
        if(pdescription==""):
            pdescription=p3
        products=request.POST.getlist('CD')
        if(products==[]):
            products=p4
        kanalysis=request.POST['kanalysis']
        if(kanalysis==""):
            kanalysis=p5
        kinsisghts=request.POST['kinsisghts']
        if(kinsisghts==""):
            kinsisghts=p6
        tags=request.POST['tags']
        if(tags==""):
            tags=p7

        db.knowledge.update({'ID':uniqueId},{'ID':uniqueId,'ptype':ptype,'psummary':psummary,'pdescription':pdescription,'products':products,'kanalysis':kanalysis,'kinsisghts':kinsisghts,'tags':tags,'owner':gfName})    
        messages.success(request, "Data Updated Successfully")

    return render(request, "authentication/index.html")       


def delete_data(request):
     global uniqueId
     conn = MongoClient()
     db=conn.Lucid
     collection=db.knowledge
     db.knowledge.remove({'ID':uniqueId})
     messages.success(request, "Data Deleted Successfully")
     return render(request, "authentication/index.html")       


def generate_tags(request):
    if request.GET.get("gentags"):
        s =  ppdescription + ppsummary
        print(s)
        s = s.lower()
        
        keywords=["data", "connect", "bi", "analytics", "arcESB", "IPaas", "cdata", "drivers", "neo4j", "django", "server", "data", " error", "jira" ,"salesforce","test"]
        
        for k in range(0,len(keywords)):
            keywords[k] = keywords[k].lower()

        print("Knowledge Given:")
        arr = s.split(" ")

        dic = {}
        for w in arr:
            dic[w] = arr.count(w)
        
        print(dic)

        st = set(arr)
        print("Suggested Tags for the given content are as follows:")
        tags = {"tag" : []}
        for w in st:
            w=w.lower()
            if ',' in w:
                w=w[:-1]
            if w in keywords:
                w = w.upper()
                print(w)
                tags["tag"].append(w)
        print(tags)     
        global taggs
        taggs = tags
        print("global",taggs)   
        global finaltags
        finaltags=taggs["tag"]
        global uniqueId2
        conn=MongoClient()
        db=conn.Lucid
        collection=db.knowledge
        print(uniqueId2,finaltags, "uid h ye")
        db.knowledge.update({'ID':uniqueId2},{"$set": {'tags':finaltags}})
        #return redirect("home")

    return render(request,"authentication/filltags.html", taggs)




