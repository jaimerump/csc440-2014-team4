# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from scoreboard.models import Player

def index(request):
    context = {'message':"Words"}
    return render(request, 'scoreboard/index.html', context)

def login(request):
    post_username = request.POST['username']
    password = request.POST['password']
    player = Player.objects.get(username=post_username)

    if not player.check_password(password):
	return render(request, 'scoreboard/index.html', {'error_message':"Username or password incorrect"})

    request.session['player_id'] = player.player_id
    return HttpResponseRedirect('/scoreboard/')

def logout(request):
    request.session['player_id'] = None
    return HttpResponseRedirect('/')

def scoreboard(request):
    player_id = request.session['player_id']
    current_player = Player.objects.get(player_id=player_id)
    context = {'player':current_player}
    return render(request, 'scoreboard/scoreboard.html', context)

