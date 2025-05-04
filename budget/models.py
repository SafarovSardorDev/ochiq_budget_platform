from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from uuid import uuid4

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(
        max_length=9,
        validators=[RegexValidator(regex=r'^\d{9}$', message='Telefon raqami 9 ta raqamdan iborat bo‘lishi kerak')],
        blank=True,
        null=True
    )
    card = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Project(models.Model):
    STATUS_CHOICES = (
        ('active', 'Faol'),
        ('completed', 'Yakunlangan'),
        ('planned', 'Rejalashtirilgan'),
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    region = models.CharField(max_length=100) 
    district = models.CharField(max_length=100)  
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    budget = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Tasdiqlanmagan'),
        ('accepted', 'Qabul qilingan'),
        ('rejected', 'Rad etilgan'),
    )
    TYPE_CHOICES = (
        ('suggestion', 'Taklif'),
        ('complaint', 'Shikoyat'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    comment = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.name} - {self.user.username}"

class Media(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='media_files')
    file = models.FileField(upload_to='media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.feedback.id} - {self.file.name}"

class Reward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    card = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.card:
            self.card = self.user.userprofile.card
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.amount} UZS"

class Check(models.Model):
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=50, unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = f"TX{uuid4().hex[:8]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Chek {self.transaction_id} - {self.reward.amount} UZS"