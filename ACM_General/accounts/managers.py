##
#
##
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from core.actions import isValidEmail

class UserManager(BaseUserManager):
    """
    Interface for database query operations for the User model.

    Allows seemless creation of users and superusers necessary for the default
    implementation of django.
    """

    use_in_migrations = True

    def get_by_natural_key(self, email):
        return self.get(email=email)

    def _create_user(self, email, **extra_fields):
        """
        Base create_user function that creates a user based on fields passed
        into it and returns the user.  extra_fields must be a member variable
        of the class which the Manager is apart of.
        """
        domain = email.split('@')[1]
        if not email:
            raise ValueError('create_user must be initialized with email.'
                             ' Server Error.')
        email = isValidEmail(email)

        email = self.normalize_email(email)
        user = self.model(email=email,
                          **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)

        return user

    def create_user(self, email, **extra_fields):
        """
        create_user creates a user based of 'default values' that every user
        should adhere at registration.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, **extra_fields)

    def create_superuser(self, email, **extra_fields):
        """
        create_superuser creates a 'default' superuser which has access to
        the django admin panel.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
	
        return self._create_user(email, **extra_fields)

class PermissionManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, perm_code):
        return self.get(perm_code = perm_code)

    def _create_permission(self, **kwargs):
        if not kwargs.get('perm_code'):
            raise ValueError('create_permission must be passed the keyword'
                             ' argument \'perm_code\'')
        if not kwargs.get('perm_desc'):
            raise ValueError('create_permission must be passed the keyword'
                             ' argument \'perm_desc\'')

    def create_permission(self, **kwargs):
        pass

class GroupManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, name):
        group = self.get(name=name)