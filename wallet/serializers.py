from rest_framework import serializers
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'owner', 'balance', 'private_key', 'public_key']
        read_only_fields = ['private_key', 'public_key']
