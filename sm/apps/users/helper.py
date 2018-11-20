from django.shortcuts import redirect

from sm import settings


def login_verify(func):
    def verify(request, *args, **kwargs):
        #判断session中是否有地
        if request.session.get("id") is None:
            login_url = settings.LOGIN_URL
            return redirect(login_url)
        else:
            return func(request, *args, **kwargs)
    return verify