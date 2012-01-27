from django.db import models
from hashlib import md5
import os


class Moment(models.Model):

    slug = models.SlugField(max_length = 255, db_index = True, unique = True, blank = True)
    photo = models.FileField(upload_to = 'moments')
    upload_ip = models.IPAddressField(null = True, blank = True, db_index = True)
    photo_md5 = models.CharField(max_length = 32, db_index = True, blank = True, unique = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True, auto_now = True)
    expires = models.DateTimeField(null = True, blank = True)
    public = models.BooleanField(default = True)

    # Override save for some magic
    def save(self, force_insert=False, force_update=False, using=None):

        if self.photo_md5 is None or len(self.photo_md5) == 0:
            self.photo_md5 = md5(self.photo.read()).hexdigest()

        # Auto create the slug if it's empty
        if self.slug is None or len(self.slug) == 0:
            self.slug = self.generate_uniq_slug()

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

    def generate_uniq_slug(self):
        # In an effort to keep the url as small as possible, we start with smaller string
        # and keep trying until we find one that's unique
        for l in range (6, len(self.photo_md5) + 1):
            slugtry  = self.photo_md5[0:l]
            if not Moment.objects.filter(slug = slugtry).count():
                return slugtry

    class Meta:
        db_table = 'moments'


class Rating(models.Model):
    moment = models.ForeignKey(Moment)
    stars = models.SmallIntegerField()
    upload_ip = models.IPAddressField(null = True, blank = True, db_index = True)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'ratings'


class Flag(models.Model):
    FLAG_CHOICES = (
        ('rotation', 'Rotated'),
        ('nasty', 'Nasty'),
        ('spam', 'Spam'),
        ('nsfw', '18+'),
    )
    moment = models.ForeignKey(Moment)
    name = models.CharField(max_length = 25, choices = FLAG_CHOICES)
    upload_ip = models.IPAddressField(null = True, blank = True, db_index = True)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'flags'

class Caption(models.Model):
    moment = models.ForeignKey(Moment)
    text = models.CharField(max_length = 255)
    upload_ip = models.IPAddressField(null = True, blank = True, db_index = True)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'captions'
