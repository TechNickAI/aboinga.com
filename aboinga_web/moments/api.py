from aboinga_web.moments.models import Moment, Rating
from decimal import Decimal, getcontext 
from django.conf.urls.defaults import url
from django.core.files import File
from django.db.models import Avg, Count
from django.http import HttpResponseBadRequest
from tastypie.api import Api
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
import datetime
import os
import repoze.timeago

UPLOADED_FILES_DIR = "/var/www/aboinga.com/upload/php/files"
repoze.timeago._NOW = datetime.datetime.now
getcontext().prec = 2

class MomentResource(ModelResource):

    class Meta:
        # TODO: cache
        # TODO: throttle
        # TODO: filtering
        authorization = Authorization()
        include_resource_uri = False
        limit = 25 
        ordering = ['created_at']
        queryset = Moment.objects.all()
        resource_name = 'moment'

    def dehydrate(self, bundle):
        # Human readable times
        bundle.data["created_at_ago"] = repoze.timeago.get_elapsed(bundle.obj.created_at)
        bundle.data["updated_at_ago"] = repoze.timeago.get_elapsed(bundle.obj.updated_at)
        bundle.data["expires_in"] = repoze.timeago.get_elapsed(bundle.obj.expires)

        bundle.data["permalink"] = bundle.obj.get_absolute_url()

        # Ratings
        bundle.data.update(self._get_ratings(bundle.obj))
        return bundle

    def _get_ratings(self, moment): 
        ratings = Rating.objects.filter(moment = moment).aggregate(Avg('stars'), Count('stars'))
        return {
            "ratings": ratings["stars__count"],
            "avg_rating": Decimal(str(ratings["stars__avg"] or 0)) 
        }

    def hydrate(self, bundle):
        # Set the upload_ip
        bundle.obj.upload_ip = get_real_ip(bundle.request)

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/upload%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('api_upload'), name="api_upload"),
            url(r"^(?P<resource_name>%s)/slot_machine%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('api_slot_machine'), name="api_slot_machine"),
        ]

    def api_upload(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        filename = request.POST.get("file", "");
        if filename == "":
            return self.create_response(request, {'success': False, 'msg': 'file is required'}, response_class=HttpResponseBadRequest)

        fullfile = os.path.normpath(os.path.join(UPLOADED_FILES_DIR, filename))
        # Avoid anything trixy.
        assert(UPLOADED_FILES_DIR in fullfile)

        my_moment = Moment()
        photo = File(open(fullfile, 'rw'))
        my_moment.photo = photo
        my_moment.upload_ip = get_real_ip(request)
        expires_at = request.POST.get("expires_at", "")
        # TODO: dynamically parse strings like "1 day" to timedeltas
        if expires_at == "1 day":
            my_moment.expires = datetime.datetime.now() + datetime.timedelta(days=1)
        elif expires_at == "1 week":
            my_moment.expires = datetime.datetime.now() + datetime.timedelta(weeks=1)
        elif expires_at == "1 month":
            my_moment.expires = datetime.datetime.now() + datetime.timedelta(months=1)

        if request.POST.get("public") == "0":
            my_moment.public = 0

        my_moment.save()
        os.remove(fullfile)

        bundle = self.build_bundle(obj=my_moment, request=request)
        bundle = self.full_dehydrate(bundle)
        return self.create_response(request, bundle)


    def api_slot_machine(self, request, **kwargs):
        self.method_check(request, allowed=['post', 'get'])

        if request.method == "POST":
            # They rated a previous one
            moment_id = request.POST.get("moment_id", "")
            rated_moment = Moment.objects.filter(pk = moment_id)
            if len(rated_moment) == 0:
                return self.create_response(request, {'success': False, 'msg': 'Invalid moment_id: %s' % moment_id}, response_class=HttpResponseBadRequest)
            try:
                stars = int(request.POST.get("stars", 0))
                assert(stars >= 1)
                assert(stars <= 10)
            except:
                return self.create_response(request, {'success': False, 'msg': 'Invalid stars (1-10): %s' % stars}, response_class=HttpResponseBadRequest)

            rating = Rating(moment = rated_moment[0], upload_ip = get_real_ip(request), stars = stars)
            rating.save()

            # Get the ratings for the supplied moment
            meta = self._get_ratings(rated_moment)
            exclude_id = rated_moment[0].id
        else:
            meta = {}
            exclude_id = -1

        # Pull one randomly, exclude the one they just saw. 
        # TODO more intelligent mechanism to exclude the ones they've already rated
        random_moment = Moment.objects.exclude(pk = exclude_id).order_by('?')[:1]
        bundle = self.build_bundle(obj=random_moment[0], request=request)
        bundle = self.full_dehydrate(bundle)
        bundle.data["previous_results"] = meta
        return self.create_response(request, bundle)


def get_real_ip(request):
    """ Get the IP from the proxy (varnish, cdn) if one is used"""
    if "HTTP_X_FORWARDED_FOR" in request.META:
        # multiple proxies, take the first one
        if ',' in request.META["HTTP_X_FORWARDED_FOR"]:
            parts = request.META["HTTP_X_FORWARDED_FOR"].split(',')
            return parts[0].strip()
        else:
            return request.META["HTTP_X_FORWARDED_FOR"]
    else:
        return request.META["REMOTE_ADDR"]


# This is called from urls.py
ABOINGA_API = Api(api_name='v1')
ABOINGA_API.register(MomentResource())
