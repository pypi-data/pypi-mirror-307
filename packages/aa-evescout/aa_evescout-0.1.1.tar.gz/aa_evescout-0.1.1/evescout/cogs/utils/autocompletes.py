from discord import AutocompleteContext

from eveuniverse.models import EveSolarSystem

from evescout.models import SignatureSystem


def search_solar_system(ctx: AutocompleteContext):
    """Return a list of potential solar systems based on the characters entered"""
    return [
        a
        for a in EveSolarSystem.objects.filter(name__icontains=ctx.value).values_list(
            "name", flat=True
        )[:10]
    ]


def possible_origins(ctx: AutocompleteContext):
    """Return a list of possible signature origins based on the characters entered"""
    return [
        a.name
        for a in SignatureSystem.SignatureOrigin
        if a.name.startswith(ctx.value.upper())
    ]
