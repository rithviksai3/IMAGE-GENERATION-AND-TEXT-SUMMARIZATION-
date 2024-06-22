from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers
from .models import Detail
from .models import Contact
from .models import Idetail
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from PIL import Image
import requests,io
import base64
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Create your views here.
@login_required
def Home(request):
     if request.method=='POST':
          try:
               Detail.objects.filter(user=request.user).delete()
               Idetail.objects.filter(user=request.user).delete()
               Contact.objects.filter(user=request.user).delete()
               User.objects.get(username=request.user).delete()
               return redirect('/')
          except:
               messages.error(request,'wrong credentials')
               return render(request,'Home.html')
     return render(request,'Home.html')

def Signup(request):
     if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            if password == password2:
                  if User.objects.filter(email=email).exists():
                       messages.error(request,'Email Already used')
                       return redirect('/')
                  elif User.objects.filter(username=username).exists():
                       messages.error(request,'Username Already exists')
                       return redirect('/')
                  else:
                       user=User.objects.create_user(username=username, email=email,password=password)
                       user.save()
                       return redirect('/signin')
            else:
                  messages.error(request, 'Password not same')
                  return redirect('/')
     else:
            return render(request,'Signup.html') 

def Signin(request):
     if request.method == 'POST':
            username=request.POST['username']
            email=request.POST['email']
            password=request.POST['password']
            user=auth.authenticate(username=username,email=email,password=password)
            if user is not None:
                  auth.login(request, user)
                  return redirect('/home')
            else:
                  messages.error(request, 'username/password is incorrect')
                  return redirect('/signin')
                  
     else:      
            return render(request,'Signin.html')
     
@login_required
def Text(request):
     if request.method=='POST':
          user=request.user
          prompt=request.POST['prompt']
          date=datetime.now()     
          API_URL = "https://api-inference.huggingface.co/models/google/pegasus-newsroom"
          headers = {"Authorization": "Bearer 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"}

          def query(payload):
               try:
                    response = requests.post(API_URL, headers=headers, json=payload)
                    return response.json()
               except:
                     return [{'summary_text':"Error try again"}]
          if len(prompt.split(' '))<15:
               output=[{'summary_text':"Error : input is small"}]
          else:
               output = query({
                    "inputs": prompt,
               })
          messages.error(request,prompt)
          messages.error(request,'summary_text:')
          
          if len(prompt.split(' '))<15:
               messages.error(request,output[0]['summary_text'])
          else:
               try:     
                    messages.error(request,output[0]['summary_text'])
                    obj=Detail()
                    obj.user=user
                    obj.prompt=prompt
                    obj.date=date
                    obj.save()
               except:
                    messages.error(request,'wait for sometime from one query to other or reload page')
     data=serializers.serialize("python",Detail.objects.filter(user=request.user).order_by('date').reverse())
     context={
           'data':data,
     }
     return render(request,'Text.html',context)

@login_required
def Image(request):
     if request.method=='POST':
          user=request.user
          prompt=request.POST['prompt']
          date=datetime.now()
          obj=Idetail(user=user,prompt=prompt,date=date)
          obj.save()
          API_URL = "https://api-inference.huggingface.co/models/alvdansen/soft-and-squishy-linework"
          headers = {"Authorization": "Bearer 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"}

          def query(payload):
               response = requests.post(API_URL, headers=headers, json=payload)
               return response.content
          image_bytes = query({
               "inputs": prompt,
          })
          image_base64 = base64.b64encode(image_bytes).decode('utf-8')
          messages.success(request, image_base64)
     from django.core import serializers
     data=serializers.serialize("python",Idetail.objects.filter(user=request.user).order_by('date').reverse())
     context={
          'data':data,
     }
     return render(request,'Image.html',context)

@login_required
def Signout(request):
      auth.logout(request)
      return redirect('/signin')

@login_required
def Contactus(request):
     if request.method == 'POST':
          user=request.user
          fname = request.POST['fname']
          lname = request.POST['lname']
          cname = request.POST['cname']
          subject= request.POST['subject']
          obj = Contact()
          obj.user=user
          obj.fname=fname
          obj.lname=lname
          obj.cname=cname
          obj.subject=subject
          obj.save()
     return render(request,'Contactus.html') 

@login_required
def Ddelete(request,prompt):
     event=Detail.objects.get(user=request.user,prompt=prompt)
     event.delete()
     return redirect('/text')

@login_required
def Idelete(request,msg):
     event=Idetail.objects.get(user=request.user,prompt=msg);
     event.delete()
     return redirect('/image')