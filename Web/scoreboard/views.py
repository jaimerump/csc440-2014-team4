# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from scoreboard.models import Player
import random

def index(request):
    # Displays the login form
    player_id = request.session['player_id']
    if player_id:
	return HttpResponseRedirect('/scoreboard/')
    return render(request, 'scoreboard/index.html')

def login(request):
    # Processes the login form
    post_username = request.POST['username']
    password = request.POST['password']
    player = Player.objects.get(username=post_username)

    if not player.check_password(password):
	return render(request, 'scoreboard/index.html', {'error_message':"Username or password incorrect"})

    request.session['player_id'] = player.player_id
    return HttpResponseRedirect('/scoreboard/')

def logout(request):
    # Logs the user out
    request.session['player_id'] = None
    return HttpResponseRedirect('/')

def scoreboard(request):
    # Displays the scoreboard page to logged in users
    player_id = request.session['player_id']
    if not player_id:
	return HttpResponseRedirect('/')
    current_player = Player.objects.get(player_id=player_id)
    context = {'player':current_player}
    return render(request, 'scoreboard/scoreboard.html', context)

def registration(request):
    # Displays the registration form
    player_id = request.session['player_id']
    if player_id:
	HttpResponseRedirect('/scoreboard/')
    return render(request, 'scoreboard/registration.html')

def register(request):
    # Processes the registration form
    username = request.POST['username']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    if not( confirm_password == password ):
	return render(request, 'scoreboard/registration.html', {'error_message':"Password confirmation doesn't match."})

    salt = random.randint(0, 1000000)
    hash = Player.hash_password(password, salt)
    player = Player(username=username, password=hash, salt=salt)
    player.save()

    # Fetch the player to access the id
    fetched_player = Player.objects.get(username=username)
    request.session['player_id'] = fetched_player.player_id

    return HttpResponseRedirect('/scoreboard/')
