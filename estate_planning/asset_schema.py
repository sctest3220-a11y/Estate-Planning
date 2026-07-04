"""Per-category asset field schemas for the multi-tab asset workbook.

Each category defines its own columns (English + Thai labels, and whether the
field is required). Two special keys are common to every category:
  - "value_thb" — estimated value in THB (optional but recommended)
  - "notes"     — free-text notes (optional)

`primary` is the field shown as the asset's name; `reference` is its key
identifier (account/registration/policy/title number).
"""

from .models import ASSET_CATEGORIES

# field = (key, label_en, label_th, required)
ASSET_FIELD_SCHEMA = {
    "real_estate": {
        "primary": "property_type",
        "reference": "title_deed_no",
        "fields": [
            ("property_type", "Property type (land / house / condo)", "ประเภท (ที่ดิน/บ้าน/ห้องชุด)", True),
            ("title_deed_no", "Title deed no. (Chanote)", "เลขที่โฉนด", False),
            ("location", "Location / address", "ที่ตั้ง / ที่อยู่", False),
            ("land_office", "Land office", "สำนักงานที่ดิน", False),
            ("area", "Area (rai-ngan-wah / sq.m)", "เนื้อที่ (ไร่-งาน-วา / ตร.ม.)", False),
            ("value_thb", "Appraised value ราคาประเมิน (THB)", "ราคาประเมิน (บาท)", False),
            ("notes", "Notes", "หมายเหตุ", False),
        ],
    },
    "vehicle": {
        "primary": "make_model",
        "reference": "registration_no",
        "fields": [
            ("make_model", "Make & model", "ยี่ห้อและรุ่น", True),
            ("registration_no", "Registration no.", "เลขทะเบียนรถ", True),
            ("vehicle_type", "Type (car / motorcycle / other)", "ประเภท (รถยนต์/จักรยานยนต์/อื่น ๆ)", False),
            ("province", "Registered province", "จังหวัดที่จดทะเบียน", False),
            ("value_thb", "Estimated value (THB)", "มูลค่าโดยประมาณ (บาท)", False),
            ("notes", "Notes", "หมายเหตุ", False),
        ],
    },
    "bank_account": {
        "primary": "bank_name",
        "reference": "account_no",
        "fields": [
            ("bank_name", "Bank name", "ชื่อธนาคาร", True),
            ("account_no", "Account number", "เลขที่บัญชี", True),
            ("account_type", "Account type (savings / current / fixed)", "ประเภทบัญชี (ออมทรัพย์/กระแสรายวัน/ประจำ)", False),
            ("branch", "Branch", "สาขา", False),
            ("currency", "Currency", "สกุลเงิน", False),
            ("value_thb", "Balance (THB)", "ยอดเงิน (บาท)", False),
            ("notes", "Notes", "หมายเหตุ", False),
        ],
    },
    "investment": {
        "primary": "institution",
        "reference": "account_no",
        "fields": [
            ("institution", "Institution / broker", "สถาบัน / โบรกเกอร์", True),
            ("account_no", "Account number", "เลขที่บัญชี", False),
            ("investment_type", "Type (stocks / funds / bonds / retirement)", "ประเภท (หุ้น/กองทุน/พันธบัตร/เกษียณ)", False),
            ("value_thb", "Estimated value (THB)", "มูลค่าโดยประมาณ (บาท)", False),
            ("notes", "Notes", "หมายเหตุ", False),
        ],
    },
    "insurance": {
        "primary": "insurer",
        "reference": "policy_no",
        "fields": [
            ("insurer", "Insurer", "บริษัทประกัน", True),
            ("policy_no", "Policy number", "เลขที่กรมธรรม์", True),
            ("policy_type", "Policy type (life / health / other)", "ประเภทกรมธรรม์ (ชีวิต/สุขภาพ/อื่น ๆ)", False),
            ("beneficiary", "Named beneficiary", "ผู้รับผลประโยชน์", False),
            ("value_thb", "Sum insured (THB)", "ทุนประกัน (บาท)", False),
            ("notes", "Notes", "หมายเหตุ", False),
        ],
    },
    "business": {
        "primary": "company_name",
        "reference": "registration_no",
        "fields": [
            ("company_name", "Company name", "ชื่อบริษัท", True),
            ("registration_no", "Registration no.", "เลขทะเบียนนิติบุคคล", False),
            ("shareholding_pct", "Shareholding %", "สัดส่วนการถือหุ้น %", False),
            ("value_thb", "Estimated value (THB)", "มูลค่าโดยประมาณ (บาท)", False),
            ("notes", "Notes", "หมายเหตุ", False),
        ],
    },
    "digital": {
        "primary": "asset_type",
        "reference": "platform",
        "fields": [
            ("asset_type", "Asset type (crypto / domain / online business)", "ประเภท (คริปโต/โดเมน/ธุรกิจออนไลน์)", True),
            ("platform", "Platform / wallet", "แพลตฟอร์ม / กระเป๋าเงิน", False),
            ("access_hint", "Where to find access details (NOT the keys themselves)", "แหล่งข้อมูลการเข้าถึง (ห้ามใส่รหัสจริง)", False),
            ("value_thb", "Estimated value (THB)", "มูลค่าโดยประมาณ (บาท)", False),
            ("notes", "Notes", "หมายเหตุ", False),
        ],
    },
    "other": {
        "primary": "description",
        "reference": "location",
        "fields": [
            ("description", "Description", "รายละเอียด", True),
            ("location", "Location / reference", "ที่ตั้ง / เอกสารอ้างอิง", False),
            ("value_thb", "Estimated value (THB)", "มูลค่าโดยประมาณ (บาท)", False),
            ("notes", "Notes", "หมายเหตุ", False),
        ],
    },
}

# Every category also gets a common "beneficiary" column (inserted before notes)
# so the user can map each asset to the person who inherits it.
BENEFICIARY_FIELD = (
    "beneficiary",
    "Beneficiary (who inherits it)",
    "ผู้รับมรดก (ผู้ที่จะได้รับทรัพย์สินนี้)",
    False,
)
for _schema in ASSET_FIELD_SCHEMA.values():
    _fields = _schema["fields"]
    _idx = next((i for i, f in enumerate(_fields) if f[0] == "notes"), len(_fields))
    _fields.insert(_idx, BENEFICIARY_FIELD)

# Keys handled specially (not folded into an asset's category-specific details).
SPECIAL_KEYS = {"value_thb", "notes", "beneficiary"}

# Sanity: every category has a schema.
assert set(ASSET_FIELD_SCHEMA) == set(ASSET_CATEGORIES), "asset schema/category mismatch"


def field_label(category, key, mode="en"):
    for k, en, th, _req in ASSET_FIELD_SCHEMA[category]["fields"]:
        if k == key:
            if mode == "th":
                return th
            if mode == "dual":
                return f"{en} / {th}"
            return en
    return key
