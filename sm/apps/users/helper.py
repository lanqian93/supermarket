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



def logining(request, user):
        # 登陆保存session的方法
        # 将用户id和手机号码,保存到session中
    request.session['id'] = user.pk
    request.session['phone'] = user.phone
    # request.session['head'] = user.head