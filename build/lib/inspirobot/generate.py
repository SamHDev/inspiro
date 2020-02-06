import requests
import re
from .error import *
from . import url


def generate():
    """
    Generate a classic image quote

    :rtype: InspiroBotImageResponse
    :return: The generated response
    """
    try:
        r = requests.get("{}?generate=true".format(url()))
    except:
        raise InsprioBotError("API request failed. Failed to connect")
    if r.status_code != 200:
        raise InsprioBotError("API request failed. Invalid response code ({})".format(r.status_code))
    return InspiroBotImageResponse(r.text)


class InspiroBotImageResponse:
    def __init__(self, image_url):
        self.url = image_url
        try:
            self.id = re.findall(r"generated\.inspirobot\.me/a/(\w+)\.(?:jpg|png)", image_url)[0]
        except IndexError:
            raise InsprioBotError("Failed to parse response")

    def read(self):
        """
        Download, and read the bytes of the image

        :rtype: bytearray
        :return: The raw bytes on the image
        """
        r = requests.get(self.url)
        return r.raw

    def __str__(self):
        return self.url

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.id)
