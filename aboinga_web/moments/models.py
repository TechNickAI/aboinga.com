from django.db import models
from hashlib import md5
import os


class Moment(models.Model):

    slug = models.SlugField(max_length = 255, db_index = True, unique = True, blank = True)
    photo = models.FileField(upload_to = 'moments')
    upload_ip = models.IPAddressField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True, db_index = True)
    updated_at = models.DateTimeField(auto_now_add = True, auto_now = True)
    expires = models.DateTimeField(null = True, blank = True)
    public = models.BooleanField(default = True)

    # Override save for some magic
    def save(self, force_insert=False, force_update=False, using=None):
        
        # Auto create the slug if it's empty    
        if self.slug is None or len(self.slug) == 0:
            self.slug = Moment.generate_uniq_slug(self.photo.read())
        
        # Will the real save please stand up?
        super(Moment, self).save()

    # Override delete to remove the file
    def delete(self, *args, **kwargs):
        photofile = self.photo.path
        super(Moment, self).delete(*args, **kwargs) # Call the "real" delete() method.
        os.remove(photofile)

    def get_absolute_url(self):
        if self.public:
            return '/moment/%s' % self.slug
        else:
            return '/moment/not-public/%s' % self.slug

    def __unicode__(self):
        return '%s - (%s)' % (self.slug, self.photo.name)

    @staticmethod 
    def generate_uniq_slug(data):
        myslug = md5(data).hexdigest()

        # In an effort to keep the url as small as possible, we start with smaller string
        # and keep trying until we find one that's unique
        for l in range (6, len(myslug) + 1):
            slugtry  = myslug[0:l]
            if not Moment.objects.filter(slug = slugtry).count():
                return slugtry

    class Meta:
        db_table = 'moments'
