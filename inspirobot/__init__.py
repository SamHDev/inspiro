__name__ = "InspiroBot API"
__version__ = "0.0.1"
__author__ = "SamHDev"

# Endpoint & Url Handlers
ENDPOINT = "inspirobot.me/api"
HTTPS = True


def url():
    """
    Get the url of the api endpoint
    :rtype: str
    :return: a url
    """
    return "{}://{}".format({True: "https", False: "http"}[HTTPS], ENDPOINT)


def https(value = None):
    global HTTPS
    if value is not None:
        HTTPS = value
    return HTTPS

from .flow import flow
from .generate import generate