from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render,redirect
from django.contrib import messages 
from django.contrib.auth.models import User,auth 
# Create your views here.


def loginUser(request):
    
  class given :
     
      def __init__(self,u,p):
        self.u = u
        self.p = p

  if(request.method == 'POST'):
       username=request.POST['username'] 
       password=request.POST['password']
       user = auth.authenticate(username=username,password=password)

       givene = given(username,password)     

       if user is not None :
          auth.login(request,user)
          return redirect('index')
       else:
          return render(request,'login.html',{'message':'Invalid Credentials !','arr':givene})           
  else:
     return render(request,'login.html')

def register(request):

  class given :
     
      def __init__(self,f,l,e,u,p1,p2):
        self.f = f
        self.l = l
        self.e = e
        self.u = u 
        self.p1 = p1
        self.p2 = p2 

  if (request.method == 'POST') :
    first_name=request.POST['first_name']
    last_name=request.POST['last_name']
    username=request.POST['username'] 
    email=request.POST['email']
    password1=request.POST['password1']
    password2=request.POST['password2']

    givene = given(first_name,last_name,email,username,password1,password2)

    if(password1!=password2):
       givene.p1=''
       givene.p2=''
       return render(request,'register.html',{'message':'Passwords Not Matching !','arr': givene }) 

    try : 
        user = User.objects.create_user(
        	username=username,
        	first_name=first_name,
        	last_name=last_name,
        	email=email,
        	password=password1,
        	) 
        user.save()
    except :
        givene.u = ''
        return render(request,'register.html',{'message':"Username Already Taken ! Please Try with Other Username",'arr': givene}) 
    user = authenticate(request,username=username,password=password1) 
    if user is not None :
        login(request,user) 
        return redirect('index')    
  else :  
      return render(request,'register.html')


def logoutUser(request):
    logout(request)  
    return redirect('index')    

