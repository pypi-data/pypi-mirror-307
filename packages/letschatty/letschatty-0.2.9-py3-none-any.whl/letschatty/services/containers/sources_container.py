from .base_container import BaseContainer
from ...models.analytics.sources import Source

class SourcesContainer(BaseContainer[Source]):
    def __init__(self):
        super().__init__(item_type=Source)
