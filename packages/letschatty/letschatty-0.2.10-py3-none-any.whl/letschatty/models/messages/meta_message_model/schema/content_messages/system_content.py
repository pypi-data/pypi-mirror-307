from pydantic import BaseModel
from enum import StrEnum

class MetaSystemTypeMessage(StrEnum):
    CUSTOMER_CHANGED_NUMBER = "customer_changed_number"
    CUSTOMER_IDENTITY_CHANGED = "customer_identity_changed"

class MetaSystemContent(BaseModel):
    """When messages type is set to system, a customer has updated their phone number or profile information, this object is included in the messages object. System objects have the following properties:
    body – String. Describes the change to the customer's identity or phone number.
    identity – String. Hash for the identity fetched from server.
    new_wa_id – String. New WhatsApp ID for the customer when their phone number is updated. Available on webhook versions v11.0 and earlier.
    wa_id – String. New WhatsApp ID for the customer when their phone number is updated. Available on webhook versions v12.0 and later.
    type – String. Type of system update. Will be one of the following:.
    customer_changed_number – A customer changed their phone number.
    customer_identity_changed – A customer changed their profile information.
    customer – String. The WhatsApp ID for the customer prior to the update."""
    body: str
    identity: str
    wa_id: str
    type: MetaSystemTypeMessage
    customer: str