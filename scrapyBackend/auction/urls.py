from django.urls import path
from . import api

urlpatterns = [
    path('create/', api.create_auction, name='create_auction'),
    path('', api.list_auctions, name='list_auctions'),
    path('<uuid:pk>/', api.auction_detail, name='auction_detail'),
    path('<uuid:pk>/bid/', api.place_bid, name='place_bid'),
    path('<uuid:pk>/cancel/',api.cancel_auction, name='cancel_auction'),
    # path('<uuid:pk>/delete/', api.delete_auction, name='delete_auction'),  
    path('user/<uuid:user_id>/', api.list_auctions_by_user, name='user_auctions'),
    path('<uuid:pk>/delete/', api.delete_auction, name='auction-delete'),


]
