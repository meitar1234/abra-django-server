import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import User, Message
from .models import Message
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from datetime import date

@csrf_exempt
def signup(request):
    form=UserForm()
    if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            form=UserForm(body)
            if form.is_valid():
              form.save()
              return HttpResponse(f'created', status=201)
            else:
                return HttpResponse(f'{dict(form.errors.items())}', status=400)


@csrf_exempt
def signout(request):
    logout(request)
    return HttpResponse('signout')

@csrf_exempt
@login_required()
def send_message(request, receiverId):
    try:

      body_unicode = request.body.decode('utf-8')
      body = json.loads(body_unicode)
      subject = body['subject']
      message = body['message']

      if subject is None or message is None:
         return HttpResponse(f'Message or/and subject was null', status=400)
      try:
         receiver = User.objects.get(id=receiverId)
         if receiver.id == request.user.id:
             return HttpResponse(f'cannot send a message to yourself', status=400)
      except:
         return HttpResponse(f'Receiver {receiverId} does not exist', status=404)
      resource = Message.objects.create(sender=request.user, receiver=receiver, subject=subject, message=message)
      resource.save()
      return HttpResponse('created', status=201)
    except Exception as e:
        return HttpResponse(f'error - {e}', status=500)


@csrf_exempt
@login_required()
def get_messages_for_logged_in_user(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-creation_date').values()
    result = list(messages)
    return HttpResponse(json.dumps(result, indent=4, sort_keys=True, default=str), content_type="application/json")


@csrf_exempt
@login_required()
def get_unread_messages_for_logged_in_user(request):
    messages = Message.objects.filter(receiver=request.user, read_date=None).order_by('-creation_date').values()
    result = list(messages)
    return HttpResponse(json.dumps(result, indent=4, sort_keys=True, default=str), content_type="application/json")

@csrf_exempt
@login_required()
def message(request, messageId):
    if request.method=='GET':
        try:
           message = Message.objects.get(receiver=request.user, id=messageId)
           message.read_date=date.today()
           message.save()

           return HttpResponse(json.dumps(message, indent=4, sort_keys=True, default=str), content_type="application/json")
        except:
            return HttpResponse(f'message {messageId} does not exist', status=404)
    if request.method=='DELETE':
        try:
            message = Message.objects.get(sender=request.user, id=messageId)
            message.delete()
        except:
            return HttpResponse(f'message {messageId} does not exist', status=404)
        return JsonResponse('deleted', safe=False)

@csrf_exempt
def signinapi(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        email = body['email']
        password = body['password']
        try:
            user = User.objects.get(email=email)
        except:
            return HttpResponse('Unauthorized', status=401)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('ok')
        else:
            return HttpResponse('Unauthorized', status=401)
