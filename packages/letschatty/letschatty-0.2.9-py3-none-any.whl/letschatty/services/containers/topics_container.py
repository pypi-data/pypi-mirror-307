from .base_container import BaseContainer
from ...models.analytics.smart_messages.topic import Topic

class TopicsContainer(BaseContainer[Topic]):
    def __init__(self):
        super().__init__(item_type=Topic)
