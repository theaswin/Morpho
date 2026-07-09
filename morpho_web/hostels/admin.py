from django.contrib import admin

from .models import Hostel, Room, Bed


class BedInline(admin.TabularInline):
    model = Bed
    extra = 0


class RoomInline(admin.TabularInline):
    model = Room
    extra = 0


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ("name", "area", "gender", "status", "price_min", "price_max")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [RoomInline]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "hostel", "floor", "type", "price")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [BedInline]


@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ("code", "room", "status", "price")
