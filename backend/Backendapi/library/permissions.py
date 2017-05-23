from accounts.models import PhoneUser

def have_phone_register(user):
    queryset = PhoneUser.objects.filter(user=user)
    if queryset:
        return True
    else:
        return False
