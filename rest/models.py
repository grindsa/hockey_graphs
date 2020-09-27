from django.db import models

# Create your models here.
class Season(models.Model):
    """ season table """
    name = models.CharField(max_length=15)
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

class Team(models.Model):
    """ team table """
    team_id = models.IntegerField(default=0)
    team_name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=5)

class Match(models.Model):
    """ match table """
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    match_id = models.IntegerField(default=0)
    date = models.CharField(max_length=10, blank=True)
    time = models.CharField(max_length=8, blank=True)
    home_team = models.ForeignKey(Team, related_name='home_team', on_delete=models.CASCADE)
    visitior_team = models.ForeignKey(Team, related_name='visitor_team', on_delete=models.CASCADE)

class Player(models.Model):
    """ player """
    player_id = models.IntegerField()
    date = models.CharField(max_length=10, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    jersey = models.IntegerField(default=0)

class Shot(models.Model):
    """ player """
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    match_shot_resutl_id = models.IntegerField()
    timestamp = models.IntegerField()
    coordinate_x = models.IntegerField()
    coordinate_y = models.IntegerField()
    real_date = models.CharField(max_length=20)
    polygon = models.CharField(max_length=20)
    zone = models.CharField(max_length=10)
