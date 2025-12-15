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


# ----------------------
# Customer Model
# ----------------------
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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



# ----------------------
# Service Model
# ----------------------

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in minutes")

    def __str__(self):
        return self.name


# ----------------------
# Staff Model
# ----------------------
class Staff(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        reviews = self.reviews.all()  # related_name from Review
        if reviews.exists():
            return round(sum([r.rating for r in reviews]) / reviews.count(), 2)
        return 0


# ----------------------
# Appointment Model
# ----------------------
class Appointment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Pending')

    def __str__(self):
        return f"{self.customer.username} - {self.service.name} on {self.date}"


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

