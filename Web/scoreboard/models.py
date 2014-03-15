# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models
import crypt

class GameEvent(models.Model):
    ge_id = models.BigIntegerField(primary_key=True)
    player = models.ForeignKey('Player', null=True, blank=True)
    game = models.ForeignKey('Game', null=True, blank=True)
    weapon = models.ForeignKey('Weapon', null=True, blank=True)
    score = models.DecimalField(null=True, max_digits=4, decimal_places=0, blank=True)
    kills = models.DecimalField(null=True, max_digits=4, decimal_places=0, blank=True)
    deaths = models.DecimalField(null=True, max_digits=4, decimal_places=0, blank=True)
    kd_ratio = models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)
    accuracy = models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)
    class Meta:
        db_table = 'game_events'

class Game(models.Model):
    game_id = models.BigIntegerField(primary_key=True)
    started_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'games'

class Player(models.Model):
    player_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=60L)
    password = models.TextField()
    salt = models.BigIntegerField()

    @staticmethod
    def hash_password(given_password, given_salt):
	# Hashes the password passed in
	return crypt.crypt(given_password, str(given_salt))

    def check_password(self, given_password):
   	# Checks if the given password matches the user's
	given_hash = Player.hash_password(given_password, self.salt)
	return (given_hash == self.password)

    def set_password(self, given_password):
	# Sets the user's password to the given one
	given_hash = Player.hash_password(given_password, self.salt)
	self.password = given_hash
	self.save()

    class Meta:
        db_table = 'players'

class Weapon(models.Model):
    weapon_id = models.BigIntegerField(primary_key=True)
    damage = models.DecimalField(null=True, max_digits=4, decimal_places=0, blank=True)
    fire_rate = models.DecimalField(null=True, max_digits=4, decimal_places=0, blank=True)
    accuracy = models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)
    class Meta:
        db_table = 'weapons'

