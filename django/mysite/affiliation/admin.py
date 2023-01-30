from django.contrib import admin
from affiliation.models import Band, Listing, BlogPost

class BandAdmin(admin.ModelAdmin):
    list_display = ('name', 'year_formed', 'genre', 'id')

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'band')

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'created_on', 'last_updated', 'id')
    list_editable = ('published',)


admin.site.register(Band, BandAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(BlogPost, BlogPostAdmin)