from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Wallet, Transaction
from .serializers import WalletSerializer
import decimal

from django.shortcuts import render

def api_overview(request):
    """
    Renders a page listing all available API methods and descriptions.
    """
    return render(request, 'wallet/api_overview.html')


@api_view(['POST'])
def create_wallet(request):
    owner = request.data.get("owner")
    wallet = Wallet.objects.create(owner=owner)
    serializer = WalletSerializer(wallet)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def create_transaction(request, pk):
    wallet = get_object_or_404(Wallet, pk=pk)
    private_key = request.data.get("private_key")
    transaction_type = request.data.get("transaction_type")
    amount = request.data.get("amount")

    if wallet.private_key != private_key:
        return Response({"error": "Invalid private key"}, status=status.HTTP_403_FORBIDDEN)

    transaction = Transaction.objects.create(wallet=wallet, transaction_type=transaction_type, amount=amount, status='pending')
    return Response({
        "message": f"{transaction_type.capitalize()} transaction of {amount} created and pending confirmation.",
        "transaction_id": transaction.id,
        "transaction_type": transaction.transaction_type,
        "amount": transaction.amount,
        "status": transaction.status
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def create_transfer_transaction(request):
    sender_public_key = request.data.get("sender_public_key")
    receiver_public_key = request.data.get("receiver_public_key")
    private_key = request.data.get("private_key")
    amount = float(request.data.get("amount"))

    sender = get_object_or_404(Wallet, public_key=sender_public_key)
    receiver = get_object_or_404(Wallet, public_key=receiver_public_key)

    if sender.private_key != private_key:
        return Response({"error": "Invalid private key for sender"}, status=status.HTTP_403_FORBIDDEN)

    transaction = Transaction.objects.create(
        wallet=sender, 
        transaction_type='transfer', 
        amount=amount, 
        status='pending'
    )
    return Response({
        "message": f"Transfer transaction of {amount} created and pending confirmation.",
        "transaction_id": transaction.id,
        "sender_wallet_id": sender.id,
        "receiver_wallet_id": receiver.id,
        "transaction_type": transaction.transaction_type,
        "amount": transaction.amount,
        "status": transaction.status
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def process_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, status='pending')

    if transaction.transaction_type == 'charge':
        transaction.wallet.balance += decimal.Decimal(transaction.amount)
        transaction.wallet.save()
    elif transaction.transaction_type == 'debit':
        if transaction.wallet.balance >= decimal.Decimal(transaction.amount):
            transaction.wallet.balance -= decimal.Decimal(transaction.amount)
            transaction.wallet.save()
        else:
            return Response({"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)
    elif transaction.transaction_type == 'transfer':
        sender = transaction.wallet
        receiver_public_key = request.data.get("receiver_public_key")
        receiver = get_object_or_404(Wallet, public_key=receiver_public_key)

        if sender.balance >= decimal.Decimal(transaction.amount):
            sender.balance -= decimal.Decimal(transaction.amount)
            receiver.balance += decimal.Decimal(transaction.amount)
            sender.save()
            receiver.save()
        else:
            return Response({"error": "Insufficient funds in sender's wallet"}, status=status.HTTP_400_BAD_REQUEST)

    transaction.status = 'completed'
    transaction.save()
    return Response({
        "message": f"{transaction.transaction_type.capitalize()} transaction of {transaction.amount} processed successfully.",
        "transaction_id": transaction.id,
        "new_balance_sender": transaction.wallet.balance
    })

@api_view(['POST'])
def check_balance(request):
    """
    Retrieve the balance of a specific wallet using its private key for authentication.
    """
    private_key = request.data.get("private_key")
    wallet = get_object_or_404(Wallet, private_key=private_key)
    
    return Response({"balance": wallet.balance})

@api_view(['POST'])
def get_wallet_details(request):
    """
    Retrieve the public key, owner's name, and balance using the private key for authentication.
    """
    private_key = request.data.get("private_key")
    wallet = get_object_or_404(Wallet, private_key=private_key)

    return Response({
        "public_key": wallet.public_key,
        "owner": wallet.owner,
        "balance": wallet.balance
    }, status=status.HTTP_200_OK)
