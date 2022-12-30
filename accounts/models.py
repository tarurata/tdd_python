from django.db import models
import uuid

class User(models.Model):
    email = models.EmailField(primary_key=True)
    
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True


# class ListUserManager(BaseUserManager):
#     def create_user(self, email):
#         ListUser.objects.create(email=email)
#
#     def create_superuser(self, email, password):
#         self.create_user(email)
#
#
# class ListUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(primary_key=True)
#     USERNAME_FIELD = 'email'
#     # REQUIRED_FIELDS = ['email', 'height']
#
#     objects = ListUserManager()
#
#     @property
#     def is_staff(self):
#         return self.email == 'wmsupo@gmail.com'
#
#     @property
#     def is_active(self):
#         return True
#
#
class Token(models.Model):
    email = models.EmailField()
    uid = models.CharField(default=uuid.uuid4, max_length=40)