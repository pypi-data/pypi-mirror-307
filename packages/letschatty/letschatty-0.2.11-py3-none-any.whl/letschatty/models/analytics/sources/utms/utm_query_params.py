from __future__ import annotations
from pydantic import BaseModel, Field, field_validator, ConfigDict
from urllib.parse import urlparse, parse_qs
import logging

logger, highlights = logging.getLogger("logger"), logging.getLogger("highlights")
class QueryUTMParams(BaseModel):
    """
    UTM campaign structure with the following parameters:
    - Source: the source of the campaign (whatsapp, facebook, etc.)
    - Medium: the medium of the campaign (social, email, etc.)
    - Campaign: the campaign name (black_friday, summer_sale, etc.)
    - Term: campaign terms/keywords
    - Content: campaign content details (ad copy, image, etc.)
    """
    base_url: str
    utm_campaign: str = ""
    utm_source: str = ""
    utm_medium: str = ""
    utm_term: str = ""
    utm_content: str = ""
    utm_id: str = ""  # Meta uses it as the ad_id

    model_config = ConfigDict(ignore_extra=True)

    @field_validator('base_url')
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        if v.startswith("https://"):
            return v.split("https://")[1]
        return v

    @classmethod
    def from_url(cls, url: str) -> QueryUTMParams:
        """Create UTM parameters from a URL string"""
        try:
            parsed_url = urlparse(url)
            base_url = parsed_url.netloc + parsed_url.path
            query_params = parse_qs(parsed_url.query)
            query_params["base_url"] = base_url
            return cls(**query_params)
        except Exception as e:
            logger.error(f"Invalid URL {url}")
            raise ValueError(f"Invalid URL {url}, must follow format 'https://www.example.com/path' - {e}")

    
    def __eq__(self, other: QueryUTMParams) -> bool:
        if not isinstance(other, QueryUTMParams):
            return False
        return self.base_url == other.base_url and self.utm_campaign == other.utm_campaign and self.utm_source == other.utm_source and self.utm_medium == other.utm_medium and self.utm_term == other.utm_term and self.utm_content == other.utm_content and self.utm_id == other.utm_id
    
    def __hash__(self) -> int:
        return hash((self.base_url, self.utm_campaign, self.utm_source, self.utm_medium, self.utm_term, self.utm_content, self.utm_id))
    
    def get_ponderated_matching_score(self, other: QueryUTMParams) -> int:
        """
        Calculate weighted matching score between UTMs.
        Parameters are checked in order, returning early if any don't match.
        
        Scoring order:
        1. base_url (required match)
        2. utm_campaign
        3. utm_source
        4. utm_medium
        5. utm_term
        6. utm_content
        7. utm_id
        
        Returns:
            int: Score from 0-7, with 7 being a perfect match
        """
        score = 0
        
        # Check parameters in order, return current score if any don't match
        if self.base_url != other.base_url:
            return score
        score += 1
        
        for param in ['utm_campaign', 'utm_source', 'utm_medium', 'utm_term', 'utm_content', 'utm_id']:
            if getattr(self, param) != getattr(other, param):
                return score
            score += 1
            
        return score

    def get_non_ponderated_matching_score(self, other: QueryUTMParams) -> int:
        """Calculate unweighted matching score - one point per matching parameter"""
        params = ['base_url', 'utm_campaign', 'utm_source', 'utm_medium', 'utm_term', 'utm_content', 'utm_id']
        return sum(1 for param in params if getattr(self, param) == getattr(other, param))

    def get_utm(self) -> str:
        """Generate full UTM URL with URI-encoded parameters"""
        from urllib.parse import quote
        
        utm = f"https://{self.base_url}?"
        
        # Build parameter list with URI encoding, excluding empty values
        params = [
            f"{param}={quote(str(getattr(self, param)))}" 
            for param in ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'utm_id']
            if getattr(self, param)
        ]
        
        return utm + "&".join(params)
