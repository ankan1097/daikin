from django.db import models

USER_CHOICES = (
    ('customer', 'Customer'),
    ('dealer', 'Dealer'),
    ('SE', 'Service Engineer'),
    ('analyst', 'Analyst'),
    ('expert', 'Expert'),
)

class UserModel(models.Model):
    user = models.CharField(max_length=20, choices=USER_CHOICES, default='Customer')
    userid = models.CharField(max_length=20)

    def __str__(self):
        return self.userid
