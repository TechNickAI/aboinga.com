from aboinga_web.moments.models import Moment
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

def home(request):
    return render_to_response("home.html", {}, RequestContext(request))

def detail(request, slug, public_path = True):
    moment = get_object_or_404(Moment, slug = slug, public = public_path)
    return render_to_response("detail.html", {"moment": moment}, RequestContext(request))
