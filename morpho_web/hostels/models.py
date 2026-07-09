from django.db import models


class Hostel(models.Model):
    GENDER_CHOICES = [("ladies", "ladies"), ("gents", "gents"), ("mixed", "mixed")]

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=255)
    area = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="mixed")
    warden = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True)
    status = models.CharField(max_length=50, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    occupied = models.IntegerField(null=True, blank=True)
    review = models.FloatField(default=0)
    price_min = models.IntegerField(null=True, blank=True)
    price_max = models.IntegerField(null=True, blank=True)
    logo = models.ImageField(blank=True)
    photos = models.TextField(blank=True, help_text="Comma-separated photo URLs")

    def __str__(self):
        return self.name

    def counts(self):
        total = sum(r.bed_set.count() for r in self.room_set.all())
        vacant = sum(r.bed_set.filter(status="vacant").count() for r in self.room_set.all())
        return {"total": total, "vacant": vacant, "occupied": total - vacant}


class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    slug = models.SlugField()
    name = models.CharField(max_length=255)
    floor = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=100, blank=True)
    price = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("hostel", "slug")

    def __str__(self):
        return f"{self.hostel.name} - {self.name}"


class Bed(models.Model):
    STATUS = [("vacant", "vacant"), ("occupied", "occupied")]

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS, default="vacant")
    price = models.IntegerField(null=True, blank=True)
    enquiry_mobile = models.CharField(max_length=50, blank=True)
    enquiry_message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.room.name} - {self.code}"
