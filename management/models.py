from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager

from django.db.models import TextChoices, CharField, BooleanField, DateField, Model, ForeignKey, CASCADE, IntegerField, \
    DateTimeField, DecimalField, FloatField


class CustomUserManager(UserManager):

    def _create_user(self, phone_number, email, password, **extra_fields):

        if not phone_number:
            raise ValueError("The given phone_number must be set")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, email, password, **extra_fields)

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", 'admin')


        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    class Role(TextChoices):
        SUPER_ADMIN = 'super admin','Super Admin'
        ADMIN = 'admin','Admin'
        OPERATOR = 'operator','Operator'
        DRIVER = 'driver','Driver'
        PRACTITIONER = 'practitioner','Practitioner'
    objects = CustomUserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    username = None
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    prava = BooleanField(default=False, null=True, blank=True)
    birth_date = DateField(null=True, blank=True)
    phone_number = CharField(max_length=12, unique=True)
    role = CharField(max_length=55, choices=Role.choices, default=Role.PRACTITIONER) # noqa



    def __str__(self):
        return f"{self.get_gender_display()} - {'Bor' if self.prava else 'Yo‘q'}"







#=========================================








class Station(Model):
    class Type(TextChoices):
        BUS = 'bus', 'Bus'
        TRAIN = 'train', 'Train'
        PLANE = 'plane', 'Plane'
    name = CharField(max_length=255)
    latitude = FloatField()
    longitude = FloatField()
    region = ForeignKey('apps.Region', on_delete=CASCADE, related_name='stations')
    type = CharField(max_length=55, choices=Type.choices)# noqa



class Transport(Model):
    class Type(TextChoices):
        BUS = 'bus', 'Bus'
        TRAIN = 'train', 'Train'
        PLANE = 'plane', 'Plane'

    type = CharField(max_length=255, choices=Type.choices, default=Type.BUS)# noqa
    name = CharField(max_length=255)
    capacity = IntegerField()
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.type})"

class Route(Model):
    transport = ForeignKey('management.Transport', on_delete=CASCADE)
    start_location = ForeignKey('management.Station', on_delete=CASCADE, related_name='start_routes')
    end_location = ForeignKey('management.Station', on_delete=CASCADE, related_name='end_routes')
    departure_time = DateTimeField()
    arrival_time = DateTimeField()
    price = DecimalField(max_digits=10, decimal_places=2)
    platform_number = CharField(max_length=50)
    driver = ForeignKey('management.User', on_delete=CASCADE, related_name='drivers')

    def __str__(self):
        return f"{self.start_location} ➝ {self.end_location} ({self.transport.name})"

class RouteStation(Model):
    route = ForeignKey(Route, on_delete=CASCADE)
    station = ForeignKey(Station, on_delete=CASCADE)
    arrival_time = DateTimeField()
    departure_time = DateTimeField()

    def __str__(self):
        return f"{self.route} - {self.station}"

class Seat(Model):
    route = ForeignKey(Route, on_delete=CASCADE)
    seat_number = CharField(max_length=10)
    is_available = BooleanField(default=True)

    def __str__(self):
        return f"Seat {self.seat_number} - {'Available' if self.is_available else 'Booked'}"
