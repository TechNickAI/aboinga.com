from aboinga_web.moments.models import Moment
from tastypie.api import Api
from tastypie.resources import ModelResource
import repoze.timeago

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

# This is called from urls.py
ABOINGA_API = Api(api_name='v1')
ABOINGA_API.register(MomentResource())
