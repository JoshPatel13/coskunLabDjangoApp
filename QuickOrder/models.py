from django.db import models
from django.utils import timezone
from UserManagement.models import User

# Create your models here.

class InventoryItem(models.Model):
    item_name = models.CharField(max_length = 50)
    current_quantity = models.IntegerField()
    min_quantity = models.IntegerField()
    refill_needed = models.BooleanField(default = False)
    is_deleted = models.BooleanField(default = False)

    def __str__(self):
        return self.item_name


class Order(models.Model):
    order_id = models.AutoField(primary_key = True, unique = True)
    item_id = models.ForeignKey(InventoryItem, on_delete = models.CASCADE)
    status = models.TextField(default = "Pending Approval")
    requested_quantity = models.IntegerField(default = 0)
    order_date = models.DateTimeField(default = timezone.now)
    user = models.ForeignKey(User, on_delete = models.SET(0))
    order_name = models.TextField(default = "Loading...")
