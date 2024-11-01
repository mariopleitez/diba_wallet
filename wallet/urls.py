from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_overview, name='api_overview'),  # Home page showing the API overview
    path('wallets/', views.create_wallet, name='create_wallet'),
    path('wallets/<int:pk>/create-transaction/', views.create_transaction, name='create_transaction'),
    path('wallets/transfer/create/', views.create_transfer_transaction, name='create_transfer_transaction'),
    path('transactions/<int:transaction_id>/process/', views.process_transaction, name='process_transaction'),
    path('wallet/check_balance/', views.check_balance, name='check_balance'),
    path('wallet/details/', views.get_wallet_details, name='get_wallet_details'),
    path('wallet/transaction_history/', views.get_wallet_transaction_history, name='get_wallet_transaction_history'),
]
