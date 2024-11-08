from typing import Union
from .other_source import OtherSource
from .pure_ad import PureAd
from .whatsapp_default_source import WhatsAppDefaultSource
from .topic_default_source import TopicDefaultSource
from .utm_source import UTMSource
from .helpers import SourceHelpers

Source = Union[OtherSource, PureAd, WhatsAppDefaultSource, TopicDefaultSource, UTMSource]