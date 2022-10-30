from django.http import HttpResponse

def myview(request):
    oldval = request.COOKIES.get('zap', None)
    resp = HttpResponse('Cookie value in view: ' + str(oldval))

    if oldval :
        resp.set_cookie('zap', int(oldval)+1)
    else:
        resp.set_cookie('zap', 1)

    resp.set_cookie('sakaicar', 1, max_age=1000)
    return resp
