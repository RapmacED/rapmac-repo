from django.contrib import admin
from affiliation.models import Band
from affiliation.models import Listing

class BandAdmin(admin.ModelAdmin):
    list_display = ('name', 'year_formed', 'genre', 'id')

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'band')


admin.site.register(Band, BandAdmin)
admin.site.register(Listing, ListingAdmin)