from django.db import models
from multiselectfield import MultiSelectField


class RealEstate(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    slug = models.SlugField(max_length=500, unique=True)
    logo = models.URLField(null=True, blank=True)
    web = models.URLField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    html = models.TextField(blank=True, null=True)
    desc = models.TextField(null=True, blank=True)
    telephone = models.CharField(max_length=300, null=True, blank=True)
    address = models.CharField(max_length=2000, null=True, blank=True)
    source = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    '''
    Father Model for all the properties
    '''
    # main data
    title = models.CharField(max_length=500, null=True)
    url = models.URLField(blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True)
    source = models.CharField(max_length=200, null=True, blank=True)
    html = models.TextField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    TRANSACTION_CHOICES = (
        ('rent', 'rent'),
        ('sale', 'sale'),
    )
    transaction = models.CharField(choices=TRANSACTION_CHOICES, null=True, blank=True, max_length=4)
    PROPERTY_CHOICES = (
        ('house', 'house'),
        ('room', 'room'),
        ('office', 'office'),
        ('garage', 'garage'),
        ('land', 'land'),
        ('commercial', 'commercial'),
    )
    property_type = models.CharField(choices=PROPERTY_CHOICES, max_length=200, blank=True, null=True)
    # https://docs.djangoproject.com/en/1.8/ref/contrib/postgres/fields/#arrayfield
    # equipment = ArrayField(models.CharField(max_length=5000, blank=True, null=True), null=True)
    # contact
    name = models.CharField(blank=True, max_length=500, null=True)
    phone_1 = models.CharField(blank=True, max_length=30, null=True)
    phone_2 = models.CharField(blank=True, max_length=30, null=True)
    real_estate = models.ForeignKey(RealEstate, blank=True, null=True, on_delete=models.SET_NULL, help_text='If blank there is not a real estate involved')
    real_estate_raw = models.CharField(blank=True, max_length=200, null=True)
    price_raw = models.IntegerField(blank=True, null=True)
    address_province = models.CharField(max_length=200, blank=True, null=True)
    address_raw = models.CharField(max_length=2000, blank=True, null=True)
    date_raw = models.DateField(blank=True, null=True)
    online = models.NullBooleanField(default=True)

    def __str__(self):
        return self.title


class Price(models.Model):
    value = models.IntegerField(blank=True, null=True)
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    property_price = models.ForeignKey(Property, blank=True, null=True)

    def __str__(self):
        return '[' + str(self.date_start) + ']-[' + str(self.date_end) + ']: ' + str(self.value)


class Date(models.Model):
    online = models.DateField(blank=True, null=True)
    offline = models.DateField(blank=True, null=True)
    property_date = models.ForeignKey(Property, blank=True, null=True)

    def __str__(self):
        return '[' + str(self.online) + ']-[' + str(self.offline) + ']'


class House(Property):
    # house data
    house_type = models.CharField(max_length=200, null=True, blank=True)
    m2_total = models.IntegerField(blank=True, null=True)
    m2_to_use = models.IntegerField(blank=True, null=True)
    m2_terrain = models.IntegerField(blank=True, null=True)
    rooms = models.IntegerField(blank=True, null=True)
    wc = models.IntegerField(blank=True, null=True)
    floor_num = models.CharField(max_length=200, null=True, blank=True)
    outside = models.CharField(max_length=20, null=True, blank=True)
    ORIENTATION_CHOICES = (
        ('norte', 'norte'),
        ('noreste', 'noreste'),
        ('este', 'este'),
        ('sureste', 'sureste'),
        ('sur', 'sur'),
        ('suroeste', 'suroeste'),
        ('oeste', 'oeste'),
        ('noroeste', 'noroeste'),
    )
    orientation = MultiSelectField(choices=ORIENTATION_CHOICES, null=True, blank=True, max_length=30, max_choices=8)
    preservation = models.CharField(max_length=100, null=True, blank=True)
    # equipment
    has_garage = models.NullBooleanField()
    terrace = models.NullBooleanField()
    elevator = models.NullBooleanField()
    chimney = models.NullBooleanField()
    swimming_pool = models.NullBooleanField()
    air_conditioning = models.NullBooleanField()
    store_room = models.NullBooleanField()
    builtin_wardrobes = models.NullBooleanField()
    furnished = models.NullBooleanField()
    furnished_kitchen = models.NullBooleanField()
    garden = models.NullBooleanField()


class Room(Property):
    # Características básicas
    house_type = models.CharField(max_length=200, null=True, blank=True)
    m2_total = models.IntegerField(blank=True, null=True)
    floor_num = models.CharField(max_length=200, null=True, blank=True)
    elevator = models.NullBooleanField()
    wc = models.IntegerField(blank=True, null=True)
    min_month_stay = models.IntegerField(blank=True, null=True)
    people_max = models.IntegerField(blank=True, null=True)
    people_now_living_gender = models.CharField(max_length=200, null=True, blank=True)
    people_now_living_age_min = models.IntegerField(blank=True, null=True)
    people_now_living_age_max = models.IntegerField(blank=True, null=True)
    smoking_allowed = models.NullBooleanField()
    pet_allowed = models.NullBooleanField()
    # Looking for
    looking_for_male = models.NullBooleanField()
    looking_for_female = models.NullBooleanField()
    looking_for_student = models.NullBooleanField()
    looking_for_worker = models.NullBooleanField()
    gay_friendly = models.NullBooleanField()
    # Equipment
    air_conditioning = models.NullBooleanField()
    internet = models.NullBooleanField()
    builtin_wardrobes = models.NullBooleanField()
    furnished = models.NullBooleanField()
    house_cleaners = models.NullBooleanField()


class Office(Property):
    # Basic
    m2_total = models.IntegerField(blank=True, null=True)
    m2_to_use = models.IntegerField(blank=True, null=True)
    m2_terrain = models.IntegerField(blank=True, null=True)
    num_of_floors = models.IntegerField(blank=True, null=True)
    distribution = models.CharField(max_length=200, null=True, blank=True)
    kitchen = models.NullBooleanField()
    wc = models.IntegerField(blank=True, null=True)
    wc_location = models.CharField(max_length=200, null=True, blank=True)
    ORIENTATION_CHOICES = (
        ('norte', 'norte'),
        ('noreste', 'noreste'),
        ('este', 'este'),
        ('sureste', 'sureste'),
        ('sur', 'sur'),
        ('suroeste', 'suroeste'),
        ('oeste', 'oeste'),
        ('noroeste', 'noroeste'),
    )
    orientation = MultiSelectField(choices=ORIENTATION_CHOICES, null=True, blank=True, max_length=30, max_choices=8)
    preservation = models.CharField(max_length=100, null=True, blank=True)
    has_garage = models.NullBooleanField()
    # Building
    floor_num = models.CharField(max_length=200, null=True, blank=True)
    outside = models.CharField(max_length=20, null=True, blank=True)
    elevators = models.IntegerField(blank=True, null=True)
    office_type = models.CharField(max_length=20, null=True, blank=True)
    janitor = models.NullBooleanField()
    access_control = models.NullBooleanField()
    security_system = models.NullBooleanField()
    security_door = models.NullBooleanField()
    fire_extinguishers = models.NullBooleanField()
    fire_detectors = models.NullBooleanField()
    sprinklers = models.NullBooleanField()
    fire_door = models.NullBooleanField()
    emergency_exit = models.NullBooleanField()
    emergency_exit_lights = models.NullBooleanField()
    # Equipment
    store_room = models.NullBooleanField()
    hot_water = models.NullBooleanField()
    heating = models.NullBooleanField()
    air_conditioning_cold = models.NullBooleanField()
    air_conditioning_hot = models.NullBooleanField()
    double_glazed_windows = models.NullBooleanField()
    false_ceiling = models.NullBooleanField()
    false_floor = models.NullBooleanField()


class Garage(Property):
    # Basic
    garage_type = models.CharField(max_length=200, null=True, blank=True)
    garage_number = models.IntegerField(blank=True, null=True)
    covered = models.NullBooleanField()
    elevator = models.NullBooleanField()
    # Equipment
    automatic_door = models.NullBooleanField()
    security_cameras = models.NullBooleanField()
    alarm = models.NullBooleanField()
    security_guard = models.NullBooleanField()


class Land(Property):
    # Basic
    m2_total = models.IntegerField(blank=True, null=True)
    m2_min_rent = models.IntegerField(blank=True, null=True)
    m2_min_sale = models.IntegerField(blank=True, null=True)
    m2_to_build = models.IntegerField(blank=True, null=True)
    access = models.CharField(max_length=200, null=True, blank=True)
    nearest_town = models.CharField(max_length=200, null=True, blank=True)
    # Urban situation
    ground = models.CharField(max_length=200, null=True, blank=True)
    zoned = models.CharField(max_length=200, null=True, blank=True)
    building_floors = models.IntegerField(blank=True, null=True)
    # Equipment
    sewerage = models.NullBooleanField()
    street_lighting = models.NullBooleanField()
    water = models.NullBooleanField()
    electricity = models.NullBooleanField()
    sidewalks = models.NullBooleanField()
    natural_gas = models.NullBooleanField()


class Commercial(Property):
    # Basic
    transfer_price = models.IntegerField(blank=True, null=True)
    m2_total = models.IntegerField(blank=True, null=True)
    m2_to_use = models.IntegerField(blank=True, null=True)
    m2_terrain = models.IntegerField(blank=True, null=True)
    num_of_floors = models.IntegerField(blank=True, null=True)
    distribution = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    corner = models.NullBooleanField()
    show_windows = models.IntegerField(blank=True, null=True)
    last_activity = models.CharField(max_length=200, null=True, blank=True)
    preservation = models.CharField(max_length=100, null=True, blank=True)
    wc = models.IntegerField(blank=True, null=True)
    # Building
    floor_num = models.CharField(max_length=200, null=True, blank=True)
    facade = models.CharField(max_length=200, null=True, blank=True)
    # Equipment
    air_conditioning = models.NullBooleanField()
    alarm_system = models.NullBooleanField()
    store_room = models.NullBooleanField()
    heating = models.NullBooleanField()
    kitchen = models.NullBooleanField()
    security_door = models.NullBooleanField()
    smoke_extractor = models.NullBooleanField()
