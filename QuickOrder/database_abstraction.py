from .serializers import InventoryItemSerializer
from .models import InventoryItem
from .serializers import OrderSerializer
from .models import Order
from UserManagement.models import User

def getAllInventoryObjects():
    return InventoryItem.objects.filter(is_deleted = False).order_by('item_name')

def getInventoryObject(item_id):
    return InventoryItem.objects.get(id = item_id)

def updateInventoryQuantity(quantity, item_id):
    item = getInventoryObject(item_id)
    item.current_quantity = item.current_quantity + quantity
    item.save() 

def updateRefillNeeded(items):
    for item in items:
        if item.current_quantity < item.min_quantity:
            item.refill_needed = True
            item.save()
        if item.current_quantity > item.min_quantity:
            item.refill_needed = False
            item.save()

def getAllOrderObjects():
    return Order.objects.all().order_by('-order_date', 'order_id')

def getOrderObject(order_id):
    return Order.objects.get(order_id = order_id)

def updateOrderStatus(updated_status, order_id):
    order = getOrderObject(order_id)
    order.status = updated_status
    order.save() 

def updateOrderName(order_id, item_id):
    item = getInventoryObject(item_id)
    order = getOrderObject(order_id)
    order.order_name = item.item_name
    order.save()



def getUserEmail(user_id):
    return User.objects.get(id = user_id).email