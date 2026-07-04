"""A placeholder EstatePlan used to preview documents without entering real data."""

from .models import STATUS_FOREIGN_RESIDENT, Beneficiary, EstatePlan, Witness


def sample_plan():
    """A plan filled with bracketed placeholders so a preview shows the template
    structure and where each field goes, without any real personal data."""
    return EstatePlan(
        full_name="[Your full legal name]",
        nationality="[Nationality]",
        passport_or_id_number="[Passport / ID number]",
        date_of_birth="[Date of birth]",
        thai_address="[Address in Thailand]",
        status=STATUS_FOREIGN_RESIDENT,
        has_thai_will=False,
        has_foreign_will=False,
        owns_land=False,
        owns_condo=False,
        has_lease=False,
        has_lease_with_succession_clause=None,
        married_to_thai=False,
        spouse_name="[Spouse name]",
        marriage_registered_at_amphur=None,
        executor_name="[Executor name]",
        executor_based_in_thailand=None,
        healthcare_proxy_name="[Healthcare proxy name]",
        living_will_options=["dnr", "ventilator", "comfort_care"],
        living_will_other="[Any additional wishes]",
        witnesses=[Witness(name="[Witness 1 name]", id_or_passport="[ID/Passport]")],
        beneficiaries=[
            Beneficiary(
                name="[Beneficiary name]",
                relationship="descendant",
                asset_description="[Asset(s) bequeathed]",
            )
        ],
    )
