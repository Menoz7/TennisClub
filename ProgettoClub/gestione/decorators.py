from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def is_member(user):
    return user.groups.filter(name='Membri').exists()

def is_maestro_or_staff(user):
    return user.groups.filter(name='Maestri').exists() or user.is_staff


def is_superuser(user):
    return user.is_superuser



#Decoratore per utenti membri
def membro_required(view_func):
    return user_passes_test(is_member, login_url='login')(view_func)

#decoratore per maestri e staff
def maestro_or_staff_required(view_func):
    return user_passes_test(is_maestro_or_staff, login_url='login')(view_func)

#decoratore per superutenti
def superuser_required(view_func):
    return user_passes_test(is_superuser, login_url='login')(view_func)