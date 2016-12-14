from django.db import models


class Country(models.Model):
    country_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.country_name


class TerritorialEntity(models.Model):
    territorial_entity_name = models.CharField(max_length=200, null=True, blank=True)
    depth_number = models.IntegerField(null=True, blank=True)
    depth_name = models.CharField(max_length=100, null=True, blank=True)
    depth_last = models.BooleanField(blank=True, default=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    father = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    near_brothers = models.ManyToManyField('self', related_name='near_brother', blank=True)

    def __str__(self):
        return self.territorial_entity_name


# ('rent', 'Alquiler'),
# ('sale', 'Venta'),
# ---------------------
# ('new construction', 'Obra Nueva'),
# ('house', 'Vivienda'),
# ('office', 'Oficina'),
# ('comercial', 'Locales o Naves'),
# ('parking', 'Garajes'),
# ('land', 'Terrenos'),
# ('share', 'Compartir'),
# ('holliday', 'Vacaciones'),
# ---------------------
# ('flat', 'Piso'),
# ('house', 'Chalet'),
# ('rustic', 'Rústico'),
# ('duplex', 'Duplex'),
# ('attic', 'Ático'),
class Transaction(models.Model):
    transaction_name = models.CharField(max_length=50)
    depth_number = models.IntegerField(null=True, blank=True)
    depth_name = models.CharField(max_length=100, null=True, blank=True)
    father = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.transaction_name


class Agency(models.Model):
    agency_name = models.CharField(max_length=200)
    logo = models.ImageField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    agency_localization = models.ManyToManyField(
        TerritorialEntity,
        through='AgencyLocalization',
        blank=True
    )

    def __str__(self):
        return self.agency_name


# Hold the information of an Agency for a specific place
class AgencyLocalization(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    place = models.ForeignKey(TerritorialEntity, blank=True, null=True, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)


# 'id', 'idealista'),
# 'fc', 'fotocasa'),
# 'ea', 'enalquiler'),
class Source(models.Model):
    source_name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=2)
    url = models.URLField(null=True, blank=True)
    url_max_request = models.URLField(null=True, blank=True)
    # logic of the source url contruction
    # type of transaction
    transaction_url = models.ManyToManyField(
        Transaction,
        through='SourceTransaction',
        blank=True
    )
    # separator
    separator_url = models.CharField(max_length=1, null=True, blank=True)
    # for the url characteristics in each territory
    territorial_url = models.ManyToManyField(
        TerritorialEntity,
        through='URLSourceTerritory',
        blank=True
    )
    agency_location_source = models.ManyToManyField(
        AgencyLocalization,
        through='AgencyLocalizationSource',
        blank=True
    )

    def __str__(self):
        return self.source_name


# Hold the information of an Agency for a specific place
class AgencyLocalizationSource(models.Model):
    agency_source_name = models.CharField(max_length=200)
    agency_source_url = models.CharField(max_length=200)
    source = models.ForeignKey(Source, blank=True, null=True, on_delete=models.CASCADE)
    agency_localization = models.ForeignKey(AgencyLocalization, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.agency_source_name


# how do you express in the Source the name of a transaction
class SourceTransaction(models.Model):
    source_transaction_name = models.CharField(max_length=100, null=True, blank=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    def __str__(self):
        return self.source_transaction_name


# how do you express in the Source the url of a territory
class URLSourceTerritory(models.Model):
    url_source_territory_name = models.CharField(max_length=200, null=True, blank=True)
    url_source_territory_name_map = models.CharField(max_length=200, null=True, blank=True)
    url_source_territory_name_list = models.CharField(max_length=200, null=True, blank=True)
    url_source_municipality_name = models.CharField(max_length=200, null=True, blank=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    territory = models.ForeignKey(TerritorialEntity, on_delete=models.CASCADE)

    def __str__(self):
        return self.url_source_territory_name


# a_c, equipped_kitchen, wardrobes, swimming_poll, furnished,
# terrace, parking, storeroom, garden, lift
class Equipment(models.Model):
    equipment_name = models.CharField(max_length=200)

    def __str__(self):
        return self.equipment_name


class House(models.Model):
    # main data
    source = models.ManyToManyField(Source, blank=True)
    house_source_id = models.CharField(max_length=50, null=True)
    url = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=200, null=True)
    price = models.IntegerField(null=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    prepopulated_fields = {"slug": ("source", "house_source_id")}
    territorial_entity = models.ForeignKey(TerritorialEntity, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    transaction_type = models.ForeignKey(Transaction, related_name='get_transition_house', blank=True, null=True)
    # house data
    deposit = models.IntegerField(blank=True, null=True)
    monthly_community_costs = models.IntegerField(blank=True, null=True)
    m2_total = models.IntegerField(blank=True, null=True)
    m2_to_use = models.IntegerField(blank=True, null=True)
    rooms = models.IntegerField(blank=True, null=True)
    bathrooms = models.IntegerField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    flat_num = models.IntegerField(blank=True, null=True)
    outside = models.BooleanField(blank=True)
    ENERGY_CHOICES = (
        ('A+++', 'A+++'),
        ('A++', 'A++'),
        ('A+', 'A+'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('No', 'No'),
    )
    energy_label = models.CharField(
        blank=True, max_length=4, choices=ENERGY_CHOICES, default='No'
    )
    ORIENTATION_CHOICES = (
        ('N', 'N'),
        ('NE', 'NE'),
        ('E', 'E'),
        ('S', 'S'),
        ('SW', 'SW'),
        ('W', 'W'),
        ('NW', 'NW'),
    )
    orientation = models.CharField(
        null=True, blank=True, max_length=2, choices=ORIENTATION_CHOICES
    )
    CONDITIONS_CHOICES = (
        ('good', 'Buena'),
        ('bad', 'A reformar'),
    )
    conditions = models.CharField(
        null=True, blank=True, max_length=4, choices=CONDITIONS_CHOICES
    )
    # building data
    flat_num_total = models.IntegerField(blank=True, null=True)
    # online data
    is_completed = models.BooleanField(default=False)
    is_online = models.BooleanField(blank=True)
    online_date = models.DateField(blank=True, null=True)
    offline_date = models.DateField(blank=True, null=True)
    # owner
    owner_phone = models.CharField(blank=True, max_length=13, null=True)
    agency = models.ManyToManyField(
        Agency,
        blank=True,
        help_text='If blank there is not an agency involved'
    )
    # equipment
    equipment = models.ManyToManyField(Equipment, blank=True)

    def __str__(self):
        return self.title
