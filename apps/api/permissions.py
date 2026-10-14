"""
Custom permission classes for RocketBank REST API.
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission allowing read-only access to anyone,
    but write operations only to the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check user or owner attribute
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if hasattr(obj, "owner"):
            return obj.owner == user
        if hasattr(obj, "user"):
            return obj.user == user
        if hasattr(obj, "account") and hasattr(obj.account, "owner"):
            return obj.account.owner == user

        return False


class IsAccountOwner(permissions.BasePermission):
    """
    Ensures that the authenticated user is the strict owner of the bank account
    or associated entity (cards, transactions).
    Staff users are also allowed full access.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.is_staff or user.is_superuser:
            return True

        # Direct account object
        if hasattr(obj, "owner"):
            return obj.owner == user

        # Related through user attribute (e.g., LoanApplication, UserDeposit, SavingGoal)
        if hasattr(obj, "user"):
            return obj.user == user

        # Related through account attribute (e.g., BankCard)
        if hasattr(obj, "account") and hasattr(obj.account, "owner"):
            return obj.account.owner == user

        # Transaction sender or receiver
        if hasattr(obj, "sender_account") or hasattr(obj, "receiver_account"):
            is_sender = obj.sender_account and obj.sender_account.owner == user
            is_receiver = obj.receiver_account and obj.receiver_account.owner == user
            return bool(is_sender or is_receiver)

        return False
