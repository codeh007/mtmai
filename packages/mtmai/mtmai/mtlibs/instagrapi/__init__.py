import logging
from urllib.parse import urlparse

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from mtmai.mtlibs.instagrapi.mixins.account import AccountMixin
from mtmai.mtlibs.instagrapi.mixins.album import DownloadAlbumMixin, UploadAlbumMixin
from mtmai.mtlibs.instagrapi.mixins.auth import LoginMixin
from mtmai.mtlibs.instagrapi.mixins.bloks import BloksMixin
from mtmai.mtlibs.instagrapi.mixins.challenge import ChallengeResolveMixin
from mtmai.mtlibs.instagrapi.mixins.clip import DownloadClipMixin, UploadClipMixin
from mtmai.mtlibs.instagrapi.mixins.collection import CollectionMixin
from mtmai.mtlibs.instagrapi.mixins.comment import CommentMixin
from mtmai.mtlibs.instagrapi.mixins.direct import DirectMixin
from mtmai.mtlibs.instagrapi.mixins.explore import ExploreMixin
from mtmai.mtlibs.instagrapi.mixins.fbsearch import FbSearchMixin
from mtmai.mtlibs.instagrapi.mixins.fundraiser import FundraiserMixin
from mtmai.mtlibs.instagrapi.mixins.hashtag import HashtagMixin
from mtmai.mtlibs.instagrapi.mixins.highlight import HighlightMixin
from mtmai.mtlibs.instagrapi.mixins.igtv import DownloadIGTVMixin, UploadIGTVMixin
from mtmai.mtlibs.instagrapi.mixins.insights import InsightsMixin
from mtmai.mtlibs.instagrapi.mixins.location import LocationMixin
from mtmai.mtlibs.instagrapi.mixins.media import MediaMixin
from mtmai.mtlibs.instagrapi.mixins.multiple_accounts import MultipleAccountsMixin
from mtmai.mtlibs.instagrapi.mixins.note import NoteMixin
from mtmai.mtlibs.instagrapi.mixins.notification import NotificationMixin
from mtmai.mtlibs.instagrapi.mixins.password import PasswordMixin
from mtmai.mtlibs.instagrapi.mixins.photo import DownloadPhotoMixin, UploadPhotoMixin
from mtmai.mtlibs.instagrapi.mixins.private import PrivateRequestMixin
from mtmai.mtlibs.instagrapi.mixins.public import (
    ProfilePublicMixin,
    PublicRequestMixin,
    TopSearchesPublicMixin,
)
from mtmai.mtlibs.instagrapi.mixins.share import ShareMixin
from mtmai.mtlibs.instagrapi.mixins.signup import SignUpMixin
from mtmai.mtlibs.instagrapi.mixins.story import StoryMixin
from mtmai.mtlibs.instagrapi.mixins.timeline import ReelsMixin
from mtmai.mtlibs.instagrapi.mixins.totp import TOTPMixin
from mtmai.mtlibs.instagrapi.mixins.track import TrackMixin
from mtmai.mtlibs.instagrapi.mixins.user import UserMixin
from mtmai.mtlibs.instagrapi.mixins.video import DownloadVideoMixin, UploadVideoMixin

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Used as fallback logger if another is not provided.
DEFAULT_LOGGER = logging.getLogger("instagrapi")


class Client(
    PublicRequestMixin,
    ChallengeResolveMixin,
    PrivateRequestMixin,
    TopSearchesPublicMixin,
    ProfilePublicMixin,
    LoginMixin,
    ShareMixin,
    TrackMixin,
    FbSearchMixin,
    HighlightMixin,
    DownloadPhotoMixin,
    UploadPhotoMixin,
    DownloadVideoMixin,
    UploadVideoMixin,
    DownloadAlbumMixin,
    NotificationMixin,
    UploadAlbumMixin,
    DownloadIGTVMixin,
    UploadIGTVMixin,
    MediaMixin,
    UserMixin,
    InsightsMixin,
    CollectionMixin,
    AccountMixin,
    DirectMixin,
    LocationMixin,
    HashtagMixin,
    CommentMixin,
    StoryMixin,
    PasswordMixin,
    SignUpMixin,
    DownloadClipMixin,
    UploadClipMixin,
    ReelsMixin,
    ExploreMixin,
    BloksMixin,
    TOTPMixin,
    MultipleAccountsMixin,
    NoteMixin,
    FundraiserMixin,
):
    proxy = None

    def __init__(
        self,
        settings: dict = {},
        proxy: str = None,
        delay_range: list = None,
        logger=DEFAULT_LOGGER,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.settings = settings
        self.logger = logger
        self.delay_range = delay_range

        self.set_proxy(proxy)

        self.init()

    def set_proxy(self, dsn: str):
        if dsn:
            assert isinstance(
                dsn, str
            ), f'Proxy must been string (URL), but now "{dsn}" ({type(dsn)})'
            self.proxy = dsn
            proxy_href = "{scheme}{href}".format(
                scheme="http://" if not urlparse(self.proxy).scheme else "",
                href=self.proxy,
            )
            self.public.proxies = self.private.proxies = {
                "http": proxy_href,
                "https": proxy_href,
            }
            return True
        self.public.proxies = self.private.proxies = {}
        return False
