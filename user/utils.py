# user/utils.py
from django.contrib.auth.models import User

def get_logged_in_user(request):
    email = request.session.get('email')
    return User.objects.filter(email=email).first()
