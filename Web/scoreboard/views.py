# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from scoreboard.models import Player, Game, GameEvent
import random

def index(request):
    # Displays the login form
    player_id = request.session['player_id'] if "player_id" in request.session else None
    if player_id:
		return HttpResponseRedirect('/scoreboard/')
    return render(request, 'scoreboard/index.html')

def login(request):
    # Processes the login form
    post_username = request.POST['username']
    password = request.POST['password']
    try:
        player = Player.objects.get(username=post_username)
    except Player.DoesNotExist:
    	return render(request, 'scoreboard/index.html', {'error_message':"Username or password incorrect"})
		
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
    player_id = request.session['player_id'] if "player_id" in request.session else None
    if not player_id:
		return HttpResponseRedirect('/')
    current_player = Player.objects.get(player_id=player_id)
	
    # Get game data
    game_id = request.GET['game_id'] if "game_id" in request.GET else 1
    game = Game.objects.get(game_id=game_id)
    game_records = GameEvent.objects.filter(game=game)
	
    context = {'player':current_player, 'game_records':game_records}
    return render(request, 'scoreboard/scoreboard.html', context)

def registration(request):
    # Displays the registration form
    player_id = request.session['player_id'] if "player_id" in request.session else None
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
	
def record_kill(request):
	# Records a kill in the database
	victim_name = request.GET['victim_name'] if "victim_name" in request.GET else "Guest"
	killer_name = request.GET['killer_name'] if "killer_name" in request.GET else "Guest"
	game_id = 1
	
        try:
	    victim = Player.objects.get(username=victim_name)
	except Player.DoesNotExist:
	    victim = Player.objects.get(username="Guest")
	try:
	    killer = Player.objects.get(username=killer_name)
	except Player.DoesNotExist:
	    killer = Player.objects.get(usernam="Guest")
	game = Game.objects.get(game_id=game_id)
	
	# Check if the killer already has a record for this game
	try:
	    kill_record = GameEvent.objects.get(game=game, player=killer)
	except GameEvent.DoesNotExist:
	    kill_record = GameEvent(game=game, player=killer, kills=0, deaths=0)
	kill_record.kills += 1
	kill_record.save()
	
	# Check if the victim already has a record for this game
	try:
	    death_record = GameEvent.objects.get(game=game, player=victim)
	except GameEvent.DoesNotExist:
	    death_record = GameEvent(game=game, player=victim, kills=0, deaths=0)
	death_record.deaths += 1
	death_record.save()
