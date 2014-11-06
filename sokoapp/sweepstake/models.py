from django.db import models
from django.utils import timezone

class LiveSweepManager(models.Manager):
    """
    Manager that returns sweeps with status = LIVE_STATUS.
    """
    def get_query_set(self):
        return super(LiveSweepManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)

class Sweep(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )

    objects = models.Manager()
    live = LiveSweepManager()

    title = models.CharField(max_length=200)
    created = models.DateTimeField(default=timezone.now)
    closed = models.DateTimeField(null=True, blank=True)
    closed_message = models.TextField(blank=True)
    slug = models.SlugField(unique=True, max_length=128)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT_STATUS)
    source_type = models.CharField(max_length=50, blank=True)
    source_id = models.CharField(max_length=50, blank=True)
    brand_id = models.CharField(max_length=50, blank=True)
    list_id = models.CharField(max_length=50, blank=True)
    acquisition_partner_id = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ["-created"]

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('sokoapp_sweep_detail', (), {'slug': self.slug})

class SweepEntry(models.Model):
    MALE_GENDER = 1
    FEMALE_GENDER = 2
    GENDER_CHOICES = [
        (MALE_GENDER, 'Male'),
        (FEMALE_GENDER, 'Female'),
    ]

    sweep = models.ForeignKey(Sweep)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField()
    date_of_birth = models.DateField(blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=FEMALE_GENDER)
    receive_email = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created"]
        verbose_name_plural = "Sweep Entries"

    def __unicode__(self):
        return "%s %s <%s>" % (self.first_name, self.last_name, self.email)
