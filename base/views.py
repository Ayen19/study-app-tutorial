from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from .models import Room,Topic 
from .forms import RoomForm
from django.db.models import Q 
#from django.http import HttpResponse
# Create your views here.

#rooms = [

#    {'id':1, 'name':'let us learn python!' },
#    {'id':2, 'name':'Design with me' },
#    {'id':1, 'name':'frontend developers' },

#]


def home(request): 

    q =   request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q) ) #queries. This querie variable is the same as the dict variable  but it will override the dictionary 
    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count }
    return render(request,'base/home.html',context)

def room(request,pk): 
    room = Room.objects.get(id=pk) #nb objects is the model manager. in this case we created a variable that gets information from the databse rather than creating a list of variables. 
  #  for i in rooms: 
  #      if i['id'] == int(pk):
  #           room = i 
    context ={'room':room}
    return render(request,'base/room.html',context)
     

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.method == 'POST' :
        form = RoomForm(request.POST, instance=room)
        if form.is_valid(): 
            form.save()
            return redirect('home')


    context = {'form': form}
    return render(request,'base/room_form.html/', context)


def deleteRoom(request, pk):
    room= Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})
