import requests
import re
from .error import *
from . import url
from . import https as get_https


def flow():
    """
    Generate a Flow Object for interacting with the mindfulness api

    :rtype: InspiroBotFlow
    :return:
    """
    return InspiroBotFlow()


class InspiroBotFlow:
    def __init__(self, session_id=1, flow_id=1):
        r1 = requests.get("{}?getSessionID={}".format(url(), session_id))
        if r1.status_code != 200:
            raise InsprioBotError("API request failed. Invalid response code ({})".format(r1.status_code))
        if len(r1.text) == 0:
            raise InsprioBotError("API request failed. Invalid response body")
        self.session_id = r1.text
        self.flow_id = flow_id
        self.items = []
        self.cursor = 0

        self.fetch()

    def fetch(self):
        """
        Fetch and append a new set of quotes from the api

        :return: None
        """
        r2 = requests.get("{}?generateFlow={}&sessionID={}".format(url(), self.flow_id, self.session_id))
        if r2.status_code != 200:
            raise InsprioBotError("API request failed. Invalid response code ({})".format(r2.status_code))
        if len(r2.text) == 0:
            raise InsprioBotError("API request failed. Invalid response body")

        raw = r2.json()

        last_img = None
        for data in raw["data"]:
            if data["type"] == "transition":
                last_img = data["image"]
            elif data["type"] == "quote":
                self.items.append(InspiroBotFlowQuote(data, last_img))

    def fetch_many(self, size):
        """
        Fetch Multiple times

        :param size: The number of times to fetch
        :type size: int
        :return: None
        """
        for i in range(0, size):
            self.fetch()

    def new(self):
        """
        Clear the current list and fetch a new set of qoutes

        :return:
        """
        self.cursor = 0
        self.items = []
        self.fetch()

    def __getitem__(self, item):
        return self.items[item]

    def __iter__(self):
        self.cursor = 0
        return self

    def next(self):
        """
        Get the next quote in the array

        :rtype: InspiroBotFlowQuote
        :return:
        """
        self.cursor += 1
        if self.cursor >= len(self.items):
            return None
        value = self[self.cursor - 1]
        return value

    def __next__(self):
        a = self.next()
        if a is None:
            raise StopIteration
        else:
            return a

    def __len__(self):
        return len(self.items)


class InspiroBotFlowQuote:
    def __init__(self, raw, image):
        self.duration = raw["duration"]
        self.time = raw["time"]
        self.quote = raw["text"]
        self.image = InspiroBotFlowImage(image)

    def image_url(self, width=1600, height=900):
        """
        :param width: the desired width of the image
        :param height: the desired high of the image
        :rtype: str
        :return: the url of the image
        """
        return self.image.image_url(width, height)

    def __str__(self):
        return self.text

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.text)

    @property
    def text(self):
        """
        get the stripped/printable text of the quote
        :rtype: str
        """
        return re.sub("\[[\w ]+?\]", "", self.quote)


class InspiroBotFlowImage:
    def __init__(self, id):
        self.id = id


    @property
    def url(self):
        """
        get the image url as (1600 x 900)

        :rtype: str or None
        :return: the image url
        """
        return self.image_url()

    def image_url(self, width=1600, height=900, https=None):
        """
        get the image url

        if there is no image, this will return `None`

        :param width: the desired width of the image
        :param height: the desired high of the image
        :param: weather to return the url with HTTPS
        :rtype: str or None
        :return: the url of the image
        """
        if self.id is None:
            return None

        if https is None:
            https = get_https()

        return "{}://source.unsplash.com/{}/{}x{}".format(
            {True: "https", False: "http"}[https],
            self.id, width, height
        )

    def redirected_image_url(self, width=1600, height=900):
        """
        get the redirected image url from unsplash

        if there is no image, this will return `None`

        **(PERFORMS A REQUEST)**

        :param width: the desired width of the image
        :param height: the desired high of the image
        :rtype: str or None
        :return: the full url of the image
        """

        if self.id is None:
            return None

        r = requests.get("{}://source.unsplash.com/{}/{}x{}".format(
            {True: "https", False: "http"}[get_https()],
            self.id, width, height)
        )
        return r.url


    def read(self, width=1600, height=900):
        """
        get the bytes on the image

        if there is no image, this will return `None`

        **(PERFORMS A REQUEST)**

        :param width: the desired width of the image
        :param height: the desired high of the image
        :rtype: Any or None
        :return: the iamge data
        """
        if self.id is None:
            return None
        return requests.get(self.image_url(width=width, height=height)).raw

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.id)

    def __bool__(self):
        return self is not None


