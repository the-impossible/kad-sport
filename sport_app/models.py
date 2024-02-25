from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.shortcuts import reverse
import uuid
from datetime import datetime
# My app imports

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None):

        # creates a user with the parameters
        if email is None:
            raise ValueError('Email address is required!')

        if name is None:
            raise ValueError('Full name is required!')

        if phone is None:
            raise ValueError('Phone Number is required!')

        if password is None:
            raise ValueError('Password is required!')

        user = self.model(
            email=self.normalize_email(email),
            name=name.title().strip(),
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, phone, password=None):
        # create a superuser with the above parameters

        user = self.create_user(
            email=email,
            name=name,
            phone=phone,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    email = models.CharField(max_length=100, db_index=True,
                             unique=True, verbose_name='email address', blank=True)
    name = models.CharField(
        max_length=100, db_index=True, blank=True, null=True)
    phone = models.CharField(
        max_length=14, db_index=True, unique=True, blank=True)
    picture = models.ImageField(
        default='img/user.png', upload_to='uploads/', null=True)

    date_joined = models.DateTimeField(
        verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name='last_login', auto_now=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name', 'phone']

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return reverse("app:profile", kwargs={
            'pk': self.user_id
        })

    class Meta:
        db_table = 'Users'
        verbose_name_plural = 'Users'

class Screening(models.Model):

    screening_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    user = models.OneToOneField(
        to="User", on_delete=models.CASCADE, blank=True)

    gender = models.ForeignKey(
        to="Gender", on_delete=models.CASCADE, blank=True, null=True)

    marital_status = models.ForeignKey(
        to="MaritalStatus", on_delete=models.CASCADE, blank=True, null=True)
    age = models.CharField(max_length=3)
    date_of_birth = models.DateField()
    present_weight = models.CharField(max_length=10)
    present_height = models.CharField(max_length=10)
    soccer_position = models.ForeignKey(
        to="SoccerPosition", on_delete=models.CASCADE, blank=True, null=True)
    medical_condition = models.CharField(max_length=255, null=True, blank=True)
    present_weakness = models.CharField(max_length=255, null=True, blank=True, help_text="(Speed, skills, shooting ability, heading, passes, control etc)")
    next_of_kin = models.CharField(max_length=30)
    relationship_to_next_of_kin = models.ForeignKey(
        to="Relationship", on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=False)
    date_applied = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} has applied"

    class Meta:
        db_table = 'Screening'
        verbose_name_plural = 'Screening'

class Gender(models.Model):
    gender_title = models.CharField(max_length=20)

    def __str__(self):
        return self.gender_title

    class Meta:
        db_table = 'Gender'
        verbose_name_plural = 'Genders'

class MaritalStatus(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Marital Status'
        verbose_name_plural = 'Marital Status'

class SoccerPosition(models.Model):
    position = models.CharField(max_length=20)

    def __str__(self):
        return self.position

    class Meta:
        db_table = 'Soccer Position'
        verbose_name_plural = 'Soccer Position'

class Relationship(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Relationship'
        verbose_name_plural = 'Relationships'


class Session(models.Model):
    session_title = models.CharField(max_length=9, unique=True)
    session_description = models.CharField(
        max_length=100, blank=True, null=True)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return self.session_title

    class Meta:
        db_table = 'Session'
        verbose_name_plural = 'Sessions'


class ScreeningStatus(models.Model):
    is_live = models.BooleanField(default=False)
    has_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"LIVE: {self.is_live} | COMPLETED: {self.has_completed}"

    class Meta:
        db_table = 'Screening Status'
        verbose_name_plural = 'Screening Status'
