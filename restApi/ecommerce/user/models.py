from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, \
    BaseUserManager
    
    
class Address(models.Model):
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=10)
    zipcode = models.CharField(max_length=10)
    district = models.CharField(max_length=255)
    complement = models.CharField(max_length=100)
    city = models.CharField(max_length=500)
    state = models.CharField(max_length=500)
    current = models.BooleanField(default=True)

    def __str__(self):
        return self.street
    

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    username = None
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    phone_number = models.CharField(
        max_length=20, null=False, unique=True, default=None
    )
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    
    objects = UserManager()
    
    class Meta:
        verbose_name = 'user'
        db_table = "user"

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name', 'last_name', 'cpf', 'phone_number',
    ]

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()