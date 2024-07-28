from django.db import models
from django.contrib.auth.models import AbstractUser




class BotUser(AbstractUser):
    phone_number = models.CharField(max_length=120, unique=True)
    photo = models.ImageField(upload_to='users/img', null=True, blank=True)
    # password = models.CharField(max_length=150,null=True,blank=True,default="admin")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.username

    def get_ordered_tariffs(self):
        from sport.models import OrderedTariffs
        return OrderedTariffs.objects.filter(user=self)

    class Meta:
        db_table = "users"
