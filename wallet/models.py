import os
from django.db import models
from ecdsa import SigningKey, SECP256k1

class Wallet(models.Model):
    owner = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    private_key = models.CharField(max_length=64, unique=True, editable=False)
    public_key = models.CharField(max_length=128, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.private_key:
            sk = SigningKey.generate(curve=SECP256k1)
            self.private_key = sk.to_string().hex()
            self.public_key = sk.verifying_key.to_string().hex()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.owner}'s Wallet - Balance: {self.balance}"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('charge', 'Charge'),
        ('debit', 'Debit'),
        ('transfer', 'Transfer'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} of {self.amount} on {self.timestamp} - Status: {self.status}"
