from django.db import models

class UserData(models.Model):
    # Demographic Information
    id = models.AutoField(primary_key=True, unique=True)
    full_name = models.CharField(max_length=100, null=False, blank=False)
    age = models.PositiveIntegerField()
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    # Lifestyle Information
    ALCOHOL_CONSUMPTION_CHOICES = [
        ('None', 'None'),
        ('Rarely', 'Rarely'),
        ('Weekly', 'Weekly'),
        ('Daily', 'Daily'),
    ]
    alcohol_consumption = models.CharField(max_length=20, choices=ALCOHOL_CONSUMPTION_CHOICES)
    ACTIVITY_LEVEL_CHOICES = [
        ('Sedentary', 'Sedentary'),
        ('Lightly Active', 'Lightly Active'),
        ('Moderately Active', 'Moderately Active'),
        ('Very Active', 'Very Active'),
    ]
    physical_activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES)
    SMOKING_STATUS_CHOICES = [
        ('Non-Smoker', 'Non-Smoker'),
        ('Former Smoker', 'Former Smoker'),
        ('Current Smoker', 'Current Smoker'),
    ]
    smoking_status = models.CharField(max_length=20, choices=SMOKING_STATUS_CHOICES)
    DIET_TYPE_CHOICES = [
        ('Omnivore', 'Omnivore'),
        ('Vegetarian', 'Vegetarian'),
        ('Vegan', 'Vegan'),
        ('Pescatarian', 'Pescatarian'),
    ]
    diet_type = models.CharField(max_length=30, choices=DIET_TYPE_CHOICES)

    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.timestamp}'

    class Meta:
        verbose_name = 'User Data'
        verbose_name_plural = 'User Data'
        db_table = 'tb_user_info'


class UserScoring(models.Model):
    user = models.OneToOneField(UserData, on_delete=models.CASCADE, related_name='scoring')
    insurance_risk_score = models.FloatField()
    diabetes_risk_score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    last_scored = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Scoring for {self.user_data.first_name} {self.user_data.last_name} - {self.timestamp}'

    class Meta:
        verbose_name = 'Scoring'
        verbose_name_plural = 'Scorings'
        db_table = 'tb_last_user_scoring'