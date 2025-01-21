
from django.shortcuts import render,redirect,get_object_or_404
from .models import Message
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from .models import Message
def signup(request):
 if request.method=='POST':
  form=UserCreationForm(request.POST)
  if form.is_valid():
   user=form.save()
   login(request,user)
   return redirect('index')
 else:
  form=UserCreationForm()
 return render(request,'registration/signup.html',{'form':form})

  
@login_required
def index(request):
 users = User.objects.exclude(username=request.user.username)
 return render(request, 'chat/index.html', {'users': users})

def chat_room(request, username):
 other_user = get_object_or_404(User,username=username)
 messages = Message.objects.filter(
 sender__in=[request.user, other_user],
 receiver__in=[request.user, other_user]
 ).order_by('timestamp')

 if request.method=="POST":
  content=request.POST.get("message")
  if content:
   Message.objects.create(sender=request.user,receiver=other_user,content=content)
  return redirect('chat_room',username=username)
 return render(request, 'chat/chat_room.html', {'messages': messages,
'other_user': other_user})

def logged_out(request):
    return render(request, 'logged_out.html')

def get_new_messages(request, username):
    user = request.user
    messages = Message.objects.filter(
        sender=user, receiver__username=username
    ) | Message.objects.filter(
        receiver=user, sender__username=username
    )
    messages = messages.order_by('timestamp')  # Order by timestamp to ensure correct order
    message_data = [{"sender": msg.sender.username, "content": msg.content, "timestamp": msg.timestamp} for msg in messages]
    return JsonResponse({'messages': message_data})