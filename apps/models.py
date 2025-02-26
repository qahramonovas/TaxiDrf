from django.contrib.auth.models import PermissionsMixin
from django.db.models import Model, CharField, TextChoices, DecimalField, DateField, TextField, BooleanField, \
    DateTimeField, ForeignKey, IntegerField, CASCADE


#==================================================
class Region(Model):
    name = CharField(max_length=200)

    def __str__(self):
        return self.name

class Discount(Model):
    class Type(TextChoices):
        PERCENTAGE = "percentage", "Percentage"
        FIXED = "fixed", "Fixed"

    code = CharField(max_length=255)
    discount_type = CharField(max_length=255, choices=Type.choices, default=Type.PERCENTAGE)# noqa
    discount_value = DecimalField(max_digits=10, decimal_places=2)
    valid_from = DateField()
    valid_to = DateField()

    def __str__(self):
        return f"{self.code} - {self.discount_type} ({self.discount_value})"

class Notification(Model):
    message = TextField()
    is_read = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class Review(Model):
    route = ForeignKey('management.Route', on_delete=CASCADE)
    rating = IntegerField()
    comment = TextField()
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.rating}/5 - {self.comment[:50]}"


