from .chat.client import ChatAPI
from .constants import PRODUCTION_BASE_URL
from .features.client import FeaturesAPI
from .variants.client import VariantsAPI


class Client:
    def __init__(self, api_key: str, base_url: str = PRODUCTION_BASE_URL):
        self.features = FeaturesAPI(api_key, base_url=base_url)
        self.chat = ChatAPI(api_key, base_url=base_url)
        self.variants = VariantsAPI(api_key, base_url=base_url)
