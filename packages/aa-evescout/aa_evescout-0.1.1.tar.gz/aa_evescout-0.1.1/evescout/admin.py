"""Admin site."""

from solo.admin import SingletonModelAdmin

from django.contrib import admin

from evescout.models import SignaturePinger, SignatureSystem, Singleton

admin.site.register(Singleton, SingletonModelAdmin)


@admin.register(SignaturePinger)
class SignaturePingerAdmin(admin.ModelAdmin):
    list_display = [
        "system",
        "discord_channel_id",
        "ping_for_thera",
        "ping_for_turnur",
        "ping_type",
        "min_ping_distance_ly",
        "min_ping_distance_jump",
    ]
    fields = [
        ("system"),
        ("discord_channel_id"),
        ("ping_for_thera", "ping_for_turnur"),
        ("ping_type"),
        ("min_ping_distance_ly", "min_ping_distance_jump"),
    ]


@admin.register(SignatureSystem)
class SignatureSystemAdmin(admin.ModelAdmin):
    list_display = ["system", "origin", "size"]
    list_filter = ["origin", "size"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
