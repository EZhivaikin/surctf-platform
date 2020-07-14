from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    PermissionsMixin)
from django.db import models

from tasks.models import Task


class TeamManager(BaseUserManager):
    def create_user(self, team_name, password=None):
        if not team_name:
            raise ValueError("Team must have an team name")

        team = self.model(
            team_name=team_name,
        )
        if password:
            team.set_password(password)
        team.save(self.db)
        return team

    def create_superuser(self, team_name, password):
        user = self.create_user(
            team_name=team_name,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class Team(AbstractBaseUser, PermissionsMixin):
    CLASSIFICATION = [
        ('SCH', 'Школьники'),
        ('UNI', 'Студенты'),
        ('OTH', 'Вне зачёта'),
    ]
    
    team_name = models.CharField(
        verbose_name='team name',
        max_length=255,
        unique=True,
    )
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    scores = models.IntegerField(null=False, default=0)
    organization = models.CharField(max_length=100, null=False, default='', blank=True)
    last_complete_date = models.DateTimeField(blank=True, null=True)

    tasks_solved = models.ManyToManyField(Task, blank=True, related_name='teams_solved')

    classification = models.CharField(
        max_length=15,
        choices=CLASSIFICATION,
        blank=True,
    )
    
    objects = TeamManager()

    USERNAME_FIELD = 'team_name'

    def __str__(self):
        return self.team_name

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_super(self):
        return self.is_admin

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        
        
class Availability(models.Model):
    start_at = models.DateTimeField(null=False)
    end_at = models.DateTimeField(null=False)
    
    class Meta:
        verbose_name_plural = "Avalabilities"