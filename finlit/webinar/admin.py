from django.contrib import admin

from .models import Webinar, WebinarTag


@admin.register(Webinar)
class WebinarModelAdmin(admin.ModelAdmin):
    ...


@admin.register(WebinarTag)
class WebinarTagModelAdmin(admin.ModelAdmin):
    ...
