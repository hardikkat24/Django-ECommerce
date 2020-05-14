from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
	def create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError(_('The email must be set'))

		email = self.normalize_email(email)
		user = self.model(email = email, **extra_fields)
		user.set_password(password)
		user.is_active = False
		user.is_staff = False
		user.is_seller = False
		user.save(using = self.db)
		return user


	def create_superuser(self, email, password, **extra_fields):
		if not email:
			raise ValueError(_('The email must be set'))

		email = self.normalize_email(email)
		user = self.model(email = email, **extra_fields)
		user.set_password(password)
		user.is_active = True
		user.is_staff = True
		user.is_seller = True
		user.is_superuser = True
		user.save(using = self.db)
		return user


	def get_by_natural_key(self, email_):
		print(email_)
		return self.get(email = email_)


class CustomUser(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(max_length = 256, unique = True)
	is_active = models.BooleanField(default = False)
	is_seller = models.BooleanField(default = False)
	is_staff = models.BooleanField(default = False)
	name = models.CharField(max_length = 150, null = False, blank = False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name', 'password']

	objects = CustomUserManager()


	def get_short_name(self):
		return self.email


	def __str__(self):
		return self.email


	def natural_key(self):
		return self.email
