from django.db import models


# Create your models here.


class Task(models.Model):
    
    solved: bool
    
    CATEGORIES = [
        ('PWN', 'PWN'),
        ('CRYPTO', 'CRYPTO'),
        ('PPC', 'PPC'),
        ('WEB', 'WEB'),
        ('STEGANO', 'STEGANO'),
        ('REVERSE', 'REVERSE'),
        ('JOY', 'JOY'),
        ('ADMIN', 'ADMIN'),
        ('RECON', 'RECON'),
    ]
    category = models.CharField(
        max_length=15,
        choices=CATEGORIES,
        blank=True,
    )

    title = models.CharField(max_length=100, null=False, blank=True, default='')
    description = models.TextField(blank=True, null=False, default='')
    cost = models.IntegerField(default=0, null=False)
    flag = models.CharField(max_length=100, null=False, default='')
    author = models.CharField(max_length=100, null=False, default='')
    
    def __str__(self):
        return self.title
