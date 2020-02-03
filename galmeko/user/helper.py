
from .models import User
from django.db.models import Q

def get_email_by_id(obj):
    user = User.objects.get(id = obj.user_id)
    return user.email

def get_name_by_id(obj):
    user = User.objects.get(id = obj.user_id)
    return user.first_name + ' ' + user.last_name

def get_phone_by_id(obj):
    user = User.objects.get(id = obj.user_id)
    return user.phone