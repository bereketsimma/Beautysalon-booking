from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class SalonBooking(models.Model):  # <-- check spelling & capitalization
    name = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    date = models.DateTimeField()

    def __str__(self):
        return self.name




class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='customer_profile'
    )
    # phone = models.CharField(max_length=20, blank=True, null=True)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Always gets username from linked User
        return self.user.username

    @property
    def email(self):
        # Access email directly from linked User
        return self.user.email


# Signal: Auto-create Customer when a User is created
@receiver(post_save, sender=User)
def create_or_update_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
    else:
        # Optionally, you can update any Customer fields if needed
        instance.customer_profile.save()

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="service_images/", blank=True, null=True)  # Example image for the service

    def __str__(self):
        return self.name

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, related_name="staffs")  # Staff can perform multiple services
    phone = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True, null=True)  # Staff bio or expertise
    image = models.ImageField(upload_to="staff_images/", blank=True, null=True)  # Staff profile picture

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    @property
    def average_rating(self):
        reviews = self.reviews.all()  # Using related_name from Review model
        if reviews.exists():
            return sum([r.rating for r in reviews]) / reviews.count()
        return None

class Review(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Customer giving the review
    rating = models.PositiveSmallIntegerField(default=5)  # e.g., 1 to 5 stars
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} -> {self.staff.user.get_full_name()} ({self.rating})"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")  # The customer
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.service.name} - {self.date} {self.time}"


class CompletedJob(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, related_name="completed_jobs")
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="completed_jobs")
    image = models.ImageField(upload_to="completed_jobs/")  # Image of the finished job
    description = models.TextField(blank=True, null=True)  # Notes about the job
    rating = models.PositiveSmallIntegerField(default=5)  # e.g., 1 to 5 stars
    review = models.TextField(blank=True, null=True)  # Customer review
    date_done = models.DateTimeField(auto_now_add=True)  # When the job was done

    def __str__(self):
        return f"{self.service.name} by {self.staff} for {self.customer}"








# ----------------------
# Review Model
# ----------------------
# class Review(models.Model):
#     stylist = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="reviews")
#     customer = models.ForeignKey(User, on_delete=models.CASCADE)  # non-nullable
#     rating = models.IntegerField(help_text="Rate 1-5")
#     comment = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('stylist', 'customer')  # One review per stylist per customer

#     def __str__(self):
#         return f"{self.customer.username} - {self.stylist.name} ({self.rating})"

