from aboinga_web.moments.models import Moment
from django.conf.urls.defaults import url
from django.core.files import File
from django.http import HttpResponseBadRequest
from tastypie.api import Api
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
import os
import repoze.timeago

UPLOADED_FILES_DIR = "/var/www/aboinga.com/upload/php/files"

class MomentResource(ModelResource):

    class Meta:
        # TODO: cache
        # TODO: throttle
        # TODO: filtering
        include_resource_uri = False
        limit = 100 
        ordering = ['created_at']
        queryset = Moment.objects.all()
        resource_name = 'moment'

    def dehydrate(self, bundle):
        # Human readable times
        bundle.data["created_at_ago"] = repoze.timeago.get_elapsed(bundle.obj.created_at)
        bundle.data["updated_at_ago"] = repoze.timeago.get_elapsed(bundle.obj.updated_at)
        bundle.data["expires_in"] = repoze.timeago.get_elapsed(bundle.obj.expires)

        return bundle

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/upload%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('api_upload'), name="api_upload"),
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
        my_moment.save()
        os.remove(fullfile)

        bundle = self.build_bundle(obj=my_moment, request=request)
        bundle = self.full_dehydrate(bundle)
        return self.create_response(request, bundle)


# This is called from urls.py
ABOINGA_API = Api(api_name='v1')
ABOINGA_API.register(MomentResource())
