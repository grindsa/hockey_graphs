""" model.py """
from django.db import models
import jsonfield

# Create your models here.
class Season(models.Model):
    """ season table """
    name = models.CharField(max_length=20)
    shortcut = models.CharField(max_length=5)
    tournament = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Team(models.Model):
    """ team table """
    team_id = models.IntegerField(primary_key=True)
    team_name = models.CharField(max_length=30)
    shortcut = models.CharField(max_length=5)
    logo = models.CharField(max_length=35, blank=True)
    color_primary = models.CharField(max_length=7, blank=True)
    color_secondary = models.CharField(max_length=7, blank=True)
    color_tertiary = models.CharField(max_length=7, blank=True, default='#b0b3b5')
    color_quaternary = models.CharField(max_length=7, blank=True, default='#68717a')
    color_penalty_primary = models.CharField(max_length=7, blank=True)
    color_penalty_secondary = models.CharField(max_length=7, blank=True)
    twitter_name = models.CharField(max_length=15, blank=True)
    def __str__(self):
        return self.team_name

class Match(models.Model):
    """ match table """
    match_id = models.IntegerField(primary_key=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    date = models.CharField(max_length=10, blank=True)
    date_uts = models.IntegerField(default=0)
    home_team = models.ForeignKey(Team, related_name='home_team', on_delete=models.CASCADE)
    visitor_team = models.ForeignKey(Team, related_name='visitor_team', on_delete=models.CASCADE)
    result = models.CharField(max_length=5, blank=True, null=True)
    finish = models.BooleanField(default=False)
    tweet = models.BooleanField(default=False)    
    disable = models.BooleanField(default=False)
    def __str__(self):
        return '{0} ({1}-{2})'.format(self.match_id, self.home_team, self.visitor_team)

class Comment(models.Model):
    """ shifts """
    name = models.CharField(max_length=30)
    de = models.TextField()
    en = models.TextField()

class Periodevent(models.Model):
    """ shifts """
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    period_event = jsonfield.JSONField(default=dict)

class Player(models.Model):
    """ player """
    player_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    jersey = models.IntegerField(default=0)
    stick = models.CharField(max_length=5, blank=True, null=True)
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    def __str__(self):
        return self.last_name

class Playerstat(models.Model):
    """ shifts """
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    home = jsonfield.JSONField(default=dict)
    visitor = jsonfield.JSONField(default=dict)

class Gameheader(models.Model):
    """ shifts """
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    gameheader = jsonfield.JSONField(default=dict)

class Roster(models.Model):
    """ shifts """
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    roster = jsonfield.JSONField(default=dict)

class Shift(models.Model):
    """ shifts """
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    shift = jsonfield.JSONField(default=dict)

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

class Socialnetworkevent(models.Model):
    """ socialnetwork """
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    source = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    name_alternate = models.CharField(max_length=50, blank=True, null=True)
    identifier = models.CharField(max_length=50)
    created_at = models.CharField(max_length=50)
    created_uts = models.IntegerField(default=0)
    text_raw = models.CharField(max_length=400)
    text_cleaned = models.CharField(max_length=300, blank=True, null=True)
    tag = models.CharField(max_length=10)

class Teamstat(models.Model):
    """ shifts """
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    home = jsonfield.JSONField(default=dict)
    visitor = jsonfield.JSONField(default=dict)

class Teammatchstat(models.Model):
    """ stats per team per match """
    match = models.ForeignKey(Match, on_delete=models.CASCADE, default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=0)
    goals_for = models.IntegerField(default=0)
    goals_for_5v5 = models.IntegerField(default=0)
    goals_pp = models.IntegerField(default=0)
    goals_pp_against = models.IntegerField(default=0)
    goals_sh = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    goals_against_5v5 = models.IntegerField(default=0)
    xgoals_for = models.FloatField(default=0)
    xgoals_against = models.FloatField(default=0)
    matchduration = models.IntegerField(default=0)
    shots_for = models.IntegerField(default=0)
    shots_for_5v5 = models.IntegerField(default=0)
    shots_pctg = models.FloatField(default=0)
    shots_ongoal_for = models.IntegerField(default=0)
    shots_ongoal_for_5v5 = models.IntegerField(default=0)
    shots_ongoal_pctg = models.FloatField(default=0)
    shots_against = models.IntegerField(default=0)
    shots_against_5v5 = models.IntegerField(default=0)
    shots_ongoal_against = models.IntegerField(default=0)
    shots_ongoal_against_5v5 = models.IntegerField(default=0)
    saves = models.IntegerField(default=0)
    saves_pctg = models.FloatField(default=0)
    faceoffslost = models.IntegerField(default=0)
    faceoffswon = models.IntegerField(default=0)
    faceoffswon_pctg = models.FloatField(default=0)
    rebounds_for = models.IntegerField(default=0)
    rebounds_against = models.IntegerField(default=0)
    goals_rebound_for = models.IntegerField(default=0)
    goals_rebound_against = models.IntegerField(default=0)
    breaks_for = models.IntegerField(default=0)
    breaks_against = models.IntegerField(default=0)
    goals_break_for = models.IntegerField(default=0)
    goals_break_against = models.IntegerField(default=0)
    penaltyminutes_drawn = models.IntegerField(default=0)
    penaltyminutes_taken = models.IntegerField(default=0)
    powerplayseconds = models.IntegerField(default=0)
    ppcount = models.IntegerField(default=0)
    shcount = models.IntegerField(default=0)
    ppefficiency = models.FloatField(default=0)
    shefficiency = models.FloatField(default=0)
    points = models.FloatField(default=0)
    goalie_own_pull = models.IntegerField(default=0)
    goalie_own_pulltime = models.IntegerField(default=0)
    goalie_other_pull = models.IntegerField(default=0)
    goals_en_for = models.IntegerField(default=0)
    goals_en_against = models.IntegerField(default=0)
    goals_wogoalie_for = models.IntegerField(default=0)

class Xg(models.Model):
    """ table to store Xg model """
    xg_data = jsonfield.JSONField(default=dict)
