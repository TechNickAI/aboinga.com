from django.db import models

class Moment(models.Model):

    slug = models.CharField(max_length = 255, db_index = True, unique = True)
    photo = models.FileField(upload_to = 'moments')
    upload_ip = models.IPAddressField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True, db_index = True)
    updated_at = models.DateTimeField(auto_now_add = True, auto_now = True)
    expires = models.DateTimeField(null = True, blank = True)
    public = models.BooleanField(default = True)

    def __unicode__(self):
        return '%s - (%s)' % (self.slug, self.photo.name)

    class Meta:
        db_table = 'moments'
