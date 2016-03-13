from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
import uuid

__all__ = ['CodeField', 'CodeTable', 'Customer', 'CustomerAddress', 'CustomerEmail', 'CustomerPhone', 'DataFile',
           'DataImport', 'ImportEntry', 'ImportField', 'ImportTable', 'Location', 'MasterEntry', 'Organization',
           'UsageReading']


class Item(models.Model):

    is_hidden = models.BooleanField(default=False)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Entry(Item):

    name = models.CharField(max_length=32)
    description = models.CharField(max_length=128, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class CodeField(Entry):

    code_table = models.ForeignKey("CodeTable", related_name="field_table", on_delete=models.CASCADE)

    code = models.CharField(max_length=8)
    priority = models.PositiveIntegerField(default=1)

    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __unicode__(self):
        return '{0}: {1}'.format(self.code_table.name, self.description)

    def organization(self):
        return self.code_table.organization

    class Meta:
        ordering = ["priority"]


class CodeTable(Entry):

    organization = models.ForeignKey("Organization", related_name="table_organization", on_delete=models.CASCADE)

    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __unicode__(self):
        return '{0}: {1}'.format(self.organization, self.name)

    def codes(self):
        return CodeField.objects.filter(code_table=self)

    class Meta:
        ordering = ["name"]


class Contact(Item):

    priority = models.PositiveIntegerField(default=1)

    def active(self):
        return not self.is_hidden


class Customer(Item):

    customer_number = models.PositiveIntegerField()

    name = models.CharField(max_length=32, blank=True)
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)

    connect_date = models.DateField(blank=True, null=True)
    service_address = models.CharField(max_length=64, blank=True)
    active = models.BooleanField(default=True)
    annual_usage = models.PositiveIntegerField(null=True, blank=True)
    rate_class = models.CharField(max_length=8, blank=True)
    rate_code = models.CharField(max_length=8, blank=True)
    revenue_class = models.CharField(max_length=8, blank=True)

    organization = models.ForeignKey("Organization", related_name="customer_organization", on_delete=models.CASCADE)

    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __unicode__(self):

        if self.name != "":
            return '({0}) {1}'.format(self.customer_number, self.name)

        elif self.first_name != "" and self.last_name != "":
            return '({0}) {1} {2}'.format(self.customer_number, self.last_name, self.first_name)

        elif self.last_name != "":
            return '({0}) {1}'.format(self.customer_number, self.last_name)

        elif self.first_name != "":
            return '({0}) {1}'.format(self.customer_number, self.first_name)

        else:
            return '{0}'.format(self.customer_number)

    class Meta:
        ordering = ["customer_number"]


class CustomerAddress(Contact):

    ADDRESS_TYPES = (('R', 'Residence'), ('W', 'Work'), ('B', 'Business'), ('O', 'Other'))

    customer = models.ForeignKey("Customer", related_name="customer_address", on_delete=models.CASCADE)
    address_type = models.CharField(max_length=1, choices=ADDRESS_TYPES, default='R')

    address_1 = models.CharField(max_length=64, blank=True)
    address_2 = models.CharField(max_length=64, blank=True)
    address_3 = models.CharField(max_length=64, blank=True)
    address_4 = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=32, blank=True)
    state = models.CharField(max_length=64, blank=True)
    postal_code = models.CharField(max_length=16, blank=True)

    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __unicode__(self):
        address = '\n'.join((self.address_1, self.address_2, self.address_3, self.address_4))
        return '{0}\n{1}, {2} {3}'.format(address, self.city, self.state, self.postal_code)

    class Meta:
        ordering = ["priority"]


class CustomerEmail(Contact):

    EMAIL_TYPES = (('P', 'Personal'), ('W', 'Work'), ('O', 'Other'))

    customer = models.ForeignKey("Customer", related_name="customer_email", on_delete=models.CASCADE)
    email_type = models.CharField(max_length=1, choices=EMAIL_TYPES, default='P')

    email = models.EmailField()

    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __unicode__(self):
        return '{0}'.format(self.email)

    class Meta:
        ordering = ["priority"]


class CustomerPhone(Contact):

    PHONE_TYPES = (('H', 'Home'), ('P', 'Personal'), ('W', 'Work'), ('C', 'Cell'), ('F', 'Fax'), ('O', 'Other'))

    customer = models.ForeignKey("Customer", related_name="customer_phone", on_delete=models.CASCADE)
    phone_type = models.CharField(max_length=1, choices=PHONE_TYPES, default='H')

    phone_number = models.CharField(max_length=16, blank=True)

    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __unicode__(self):
        return '{0}'.format(self.phone_number)

    class Meta:
        ordering = ["priority"]


class DataFile(models.Model):

    FILE_TYPES = (('R', 'Raw'), ('C', 'Cleaned'), ('V', 'Validated'))

    import_id = models.ForeignKey("DataImport", related_name="import_file", on_delete=models.CASCADE)
    file_location = models.FileField(upload_to="imports/")
    file_type = models.CharField(max_length=1, default='R', choices=FILE_TYPES)

    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __unicode__(self):
        return


class DataImport(models.Model):

    IMPORT_TYPES = (('M', 'Master Data Import'), ('C', 'Custom Data Import'), ('L', 'Code Lookup Import'))
    STATUS_TYPES = (('S', 'Started'), ('P', 'Processed'), ('E', 'Posted'))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    import_type = models.CharField(max_length=1, default='M', choices=IMPORT_TYPES)
    status_type = models.CharField(max_length=1, default='S', choices=STATUS_TYPES)

    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)

    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __unicode__(self):
        return self.pk


class ImportEntry(Item):

    customer_id = models.ForeignKey("Customer", related_name="customer_entry", on_delete=models.CASCADE)
    location_id = models.ForeignKey("Location", related_name="location_entry", on_delete=models.CASCADE)

    field_id = models.ForeignKey("ImportField", related_name="entry_field", on_delete=models.CASCADE)

    response = models.TextField(blank=True)

    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ["field_id"]


class ImportField(Entry):

    FIELD_TYPES = (('I', 'integer'), ('C', 'character'), ('S', 'string'), ('F', 'float'), ('D', 'date'), ('T', 'time'),
                   ('U', 'datetime'))

    table = models.ForeignKey("ImportTable", related_name="import_field_table", on_delete=models.CASCADE)
    field_type = models.CharField(max_length=1, choices=FIELD_TYPES, default='S')
    validator = models.TextField(blank=True, null=True)
    code_validation = models.ForeignKey("CodeTable", related_name="import_validator", null=True, blank=True,
                                        on_delete=models.SET_NULL)

    length = models.PositiveIntegerField(default=1)
    priority = models.PositiveIntegerField(default=1)

    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ["priority"]


class ImportTable(Entry):

    organization = models.ForeignKey("Organization", related_name="import_organization", on_delete=models.CASCADE)

    update_user = models.ForeignKey(User, related_name="import_upt_user", null=True, blank=True,
                                    on_delete=models.SET_NULL)

    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ["name"]


class Location(Item):

    number = models.PositiveIntegerField()
    map_location = models.PositiveIntegerField(blank=True)

    organization = models.ForeignKey("Organization", related_name="location_organization", on_delete=models.CASCADE)

    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __unicode__(self):

        if self.map_location and self.map_location != '':
            return '{0} ({1})'.format(self.number, self.map_location)

        else:
            return '{0}'.format(self.number)

    class Meta:
        ordering = ["number"]


class MasterEntry(Entry):

    priority = models.PositiveIntegerField(default=1)
    length = models.PositiveIntegerField(default=1)
    validator = models.TextField(blank=True, null=True)
    code_validation = models.ForeignKey("CodeTable", related_name="master_validator", null=True, blank=True,
                                        on_delete=models.SET_NULL)

    organization = models.ForeignKey("Organization", related_name="master_organization", on_delete=models.CASCADE)

    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ["priority"]


class Organization(Entry):

    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ["name"]


class UsageReading(Item):

    customer = models.ForeignKey("Customer", related_name="usage_customer", on_delete=models.CASCADE)

    month = models.CharField(max_length=16, blank=True)
    demand_kw = models.PositiveIntegerField(null=True, blank=True)
    demand_revenue = models.PositiveIntegerField(null=True, blank=True)
    usage = models.PositiveIntegerField(null=True, blank=True)
    usage_revenue = models.PositiveIntegerField(null=True, blank=True)
    read_date = models.DateField(blank=True, null=True)

    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ["update_dt"]
