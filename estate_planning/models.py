"""Data structures shared by the advice engine and document renderers."""

from dataclasses import dataclass, field
from typing import List, Optional

STATUS_THAI_NATIONAL = "thai_national"
STATUS_FOREIGN_RESIDENT = "foreign_resident"
STATUS_VISITOR = "visitor"

STATUS_CHOICES = (STATUS_THAI_NATIONAL, STATUS_FOREIGN_RESIDENT, STATUS_VISITOR)

RELATIONSHIP_SPOUSE = "spouse"
RELATIONSHIP_DESCENDANT = "descendant"
RELATIONSHIP_ASCENDANT = "ascendant"
RELATIONSHIP_OTHER = "other"

RELATIONSHIP_CHOICES = (
    RELATIONSHIP_SPOUSE,
    RELATIONSHIP_DESCENDANT,
    RELATIONSHIP_ASCENDANT,
    RELATIONSHIP_OTHER,
)


@dataclass
class Witness:
    name: str
    id_or_passport: str = "TBD"


@dataclass
class Beneficiary:
    name: str
    relationship: str
    asset_description: str = ""
    inherited_value_thb: float = 0.0


# Asset categories (key -> English label). Used by the asset sheet and inventory.
ASSET_CATEGORIES = {
    "real_estate": "Real estate",
    "vehicle": "Vehicle",
    "bank_account": "Bank account",
    "investment": "Investment / retirement",
    "insurance": "Insurance policy",
    "business": "Business interest",
    "digital": "Digital asset",
    "other": "Other",
}


@dataclass
class Asset:
    category: str
    description: str = ""
    value_thb: float = 0.0
    location: str = ""
    notes: str = ""


@dataclass
class EstatePlan:
    full_name: str
    nationality: str
    passport_or_id_number: str
    date_of_birth: str
    thai_address: str

    status: str

    has_thai_will: bool = False
    has_foreign_will: bool = False

    owns_land: bool = False
    owns_condo: bool = False
    has_lease: bool = False
    has_lease_with_succession_clause: Optional[bool] = None

    married_to_thai: bool = False
    spouse_name: str = ""
    marriage_registered_at_amphur: Optional[bool] = None

    executor_name: str = "TBD"
    executor_based_in_thailand: Optional[bool] = None

    healthcare_proxy_name: str = "TBD"

    witnesses: List[Witness] = field(default_factory=list)
    beneficiaries: List[Beneficiary] = field(default_factory=list)
    assets: List[Asset] = field(default_factory=list)


@dataclass
class Advice:
    summary: str
    warnings: List[str]
    recommendations: List[str]
    tax_breakdown: List[str]
