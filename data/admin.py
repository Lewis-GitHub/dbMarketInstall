from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from models import *


class DataFileInline(admin.TabularInline):
    model = DataFile


class AddressInline(admin.TabularInline):
    model = CustomerAddress


class EmailInline(admin.TabularInline):
    model = CustomerEmail


class PhoneInline(admin.TabularInline):
    model = CustomerPhone


class CustomerAdmin(SimpleHistoryAdmin):
    inlines = [AddressInline, EmailInline, PhoneInline]


class ImportAdmin(SimpleHistoryAdmin):
    inlines = [DataFileInline]

admin.site.register(Organization, SimpleHistoryAdmin)
admin.site.register(CodeTable, SimpleHistoryAdmin)
admin.site.register(CodeField, SimpleHistoryAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(CustomerAddress, SimpleHistoryAdmin)
admin.site.register(DataFile, SimpleHistoryAdmin)
admin.site.register(DataImport, ImportAdmin)
admin.site.register(ImportEntry, SimpleHistoryAdmin)
admin.site.register(ImportField, SimpleHistoryAdmin)
admin.site.register(ImportTable, SimpleHistoryAdmin)
admin.site.register(Location, SimpleHistoryAdmin)
admin.site.register(MasterEntry, SimpleHistoryAdmin)
admin.site.register(UsageReading, SimpleHistoryAdmin)
