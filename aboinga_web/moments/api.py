from aboinga_web.moments.models import Moment
from tastypie.api import Api
from tastypie.resources import ModelResource

class MomentResource(ModelResource):

    class Meta:
        # TODO: cache
        # TODO: throttle
        # TODO: filtering
        # TODO: file handling
        include_resource_uri = False
        limit = 100 
        ordering = ['-created_at']
        queryset = Moment.objects.all()
        resource_name = 'moment'

# This is called from urls.py
ABOINGA_API = Api(api_name='v1')
ABOINGA_API.register(MomentResource())
