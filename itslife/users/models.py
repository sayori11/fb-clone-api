from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The email must be set')
        if not password:
            raise ValueError('The password must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    gender_choices = (
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Custom', 'Custom')
    )

    username = None
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=20, choices=gender_choices)
    profile_pic = models.ImageField(default='default_user.jfif', upload_to = 'profile_pics')
    cover_pic = models.ImageField(default='default_cover.jfif', upload_to = 'cover_pics')
    bio = models.TextField(blank=True)
    friends = models.ManyToManyField('self', symmetrical=True, related_name='friends', blank=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birthday', 'gender']

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class FriendRequest(models.Model):
    
    sender = models.ForeignKey(User, on_delete = models.CASCADE, related_name='friend_requests_sent')
    receiver = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'friend_requests_received')
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f'{self.sender} to {self.receiver}'
