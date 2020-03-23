from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create(self, **data):
        password = data.pop('password')

        user = self.model(**data)
        user.set_password(password)
        user.save(using=self._db)
        return user
