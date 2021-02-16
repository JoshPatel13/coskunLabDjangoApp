from django.urls import path

from . import inventory_views
from . import order_views
from . import message_views

urlpatterns = [
    path('inventory/', inventory_views.getInventory, name = 'inventory'),
    path('get-item/<str:item_id>/', inventory_views.getInventoryItem, name = 'get-item'),
    path('add-item/', inventory_views.addItem, name = 'add-item'),
    path('update-item/<str:item_id>/', inventory_views.updateItem, name = 'update-item'),
    path('delete-item/<str:item_id>/', inventory_views.deleteItem, name = 'delete-item'),

    path('orders/', order_views.getOrders, name = 'orders'),
    path('add-order/', order_views.addOrder, name = 'add-order'),
    path('delete-order/<str:order_id>/', order_views.deleteOrder, name = 'delete-order'),
    
    path('coskun/<str:order_id>/<str:item_id>/', message_views.getApproval, name = 'approval'),
    path('approval/', message_views.AdminApprove, name = 'response'),
    path('financeApproval/<str:order_id>/', message_views.FinanceApprove, name = 'finance-approval'),
    path('financeDeliver/<str:order_id>/<str:item_id>/', message_views.FinanceDeliver, name = 'finance-deliver'),
    path('financeCancel/<str:order_id>/', message_views.FinanceCancel, name = 'finance-cancel')


]
