from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    goal = models.CharField(max_length=20, choices=[('lose_weight', 'Lose Weight'), ('gain_weight', 'Gain Weight')])
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    birthday = models.DateField(default='1900-01-01')
    height = models.CharField(max_length=50)
    current_weight = models.CharField(max_length=50)
    goal_weight = models.CharField(max_length=50)
    activity = models.CharField(max_length=50, choices=[
        ('sedentary', 'Sedentary (little to no exercise)'),
        ('lightly_active', 'Lightly active (light exercise/sports 1-3 days a week)'),
        ('moderately_active', 'Moderately active (moderate exercise/sports 3-5 days a week)'),
        ('very_active', 'Very active (hard exercise/sports 6-7 days a week)'),
        ('extra_active', 'Extra active (very hard exercise/sports & physical job)')
    ], default='sedentary')