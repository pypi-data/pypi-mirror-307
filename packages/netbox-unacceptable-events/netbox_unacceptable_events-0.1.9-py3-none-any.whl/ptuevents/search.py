from netbox.search import SearchIndex, register_search
from . import models


@register_search
class PTUsersIndex(SearchIndex):
    model = models.PTUsers
    fields = (
        ('sAMAccountName', 100),
        ('vpnIPaddress', 300),
        ('firstname', 500),
        ('lastname', 500),
        ('ad_description', 500),
        ('description', 500),
        ('comment', 5000),
    )


@register_search
class PTWorkstationsIndex(SearchIndex):
    model = models.PTWorkstations
    fields = (
        ('name', 100),
        ('ad_description', 500),
        ('description', 500),
    )


indexes = [PTUsersIndex, PTWorkstationsIndex]
