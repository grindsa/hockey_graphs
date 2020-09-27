""" model.py """
from django.db import models

# Create your models here.
class Season(models.Model):
    """ season table """
    name = models.CharField(max_length=15)
    def __str__(self):
        return self.name

class Team(models.Model):
    """ team table """
    team_id = models.IntegerField(primary_key=True)
    team_name = models.CharField(max_length=30)
    shortcut = models.CharField(max_length=5)
    def __str__(self):
        return self.shortcut

class Match(models.Model):
    """ match table """
    match_id = models.IntegerField(primary_key=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    date = models.CharField(max_length=10, blank=True)
    date_uts = models.IntegerField(default=0)
    home_team = models.ForeignKey(Team, related_name='home_team', on_delete=models.CASCADE)
    visitor_team = models.ForeignKey(Team, related_name='visitor_team', on_delete=models.CASCADE)
    def __str__(self):
        return '{0} ({1}-{2})'.format(self.match_id, self.home_team, self.visitor_team)

class Player(models.Model):
    """ player """
    player_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    jersey = models.IntegerField(default=0)
    def __str__(self):
        return self.last_name

class Shot(models.Model):
    """ player """
    shot_id = models.IntegerField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    match_shot_resutl_id = models.IntegerField()
    timestamp = models.IntegerField()
    coordinate_x = models.IntegerField()
    coordinate_y = models.IntegerField()
    real_date = models.CharField(max_length=20)
    polygon = models.CharField(max_length=20)
    zone = models.CharField(max_length=20)
