from django.contrib import admin
from affiliation.models import Band, Listing, BlogPost, BlogPart

class BandAdmin(admin.ModelAdmin):
    list_display = ('name', 'year_formed', 'genre', 'id')

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'band')

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'created_on', 'last_updated', 'id')
    list_editable = ('published',)

class BlogPartAdmin(admin.ModelAdmin):
    list_display = ('created_on','name','slug','picture','link','description','positive','negative','last_updated')
    list_editable = ('name','slug','picture','link','description','positive','negative')


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogPart, BlogPartAdmin)
