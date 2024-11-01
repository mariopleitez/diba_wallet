from rest_framework import serializers
from .models import Wallet
from .models import Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'owner', 'balance', 'private_key', 'public_key']
        read_only_fields = ['private_key', 'public_key']



class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'transaction_type', 'amount', 'status', 'timestamp', 'wallet']
