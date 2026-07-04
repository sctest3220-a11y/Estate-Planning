"""Bilingual (Thai/English) draft document generators.

All output is a DRAFT for review by a licensed Thai probate/estate lawyer before
signing or witnessing. Nothing produced here is legal advice.
"""

from .models import EstatePlan

DISCLAIMER_EN = (
    "DRAFT ONLY — not legal advice. Verify with a licensed Thai probate/estate "
    "lawyer and confirm current law before signing or witnessing this document."
)
DISCLAIMER_TH = (
    "ร่างเอกสารเท่านั้น — ไม่ใช่คำแนะนำทางกฎหมาย กรุณาตรวจสอบกับทนายความด้านมรดกที่มีใบอนุญาต "
    "และยืนยันกฎหมายปัจจุบันก่อนลงนามหรือให้พยานลงนามในเอกสารนี้"
)


def _header(title_en: str, title_th: str) -> str:
    return (
        f"# {title_en}\n"
        f"# {title_th}\n\n"
        f"*{DISCLAIMER_EN}*\n"
        f"*{DISCLAIMER_TH}*\n\n"
        "---\n\n"
    )


def _witness_block(plan: EstatePlan) -> str:
    lines = ["## Witnesses / พยาน\n"]
    witnesses = plan.witnesses or []
    for i in range(max(2, len(witnesses))):
        w = witnesses[i] if i < len(witnesses) else None
        name = w.name if w else "TBD"
        id_no = w.id_or_passport if w else "TBD"
        lines.append(
            f"{i + 1}. Name / ชื่อ: {name}   ID/Passport: {id_no}   "
            "Signature / ลายมือชื่อ: ____________________   Date / วันที่: __________"
        )
    return "\n".join(lines) + "\n"


def render_last_will(plan: EstatePlan) -> str:
    out = _header("Last Will and Testament (Ordinary Written Will)", "พินัยกรรมแบบธรรมดา")
    out += (
        f"Testator / ผู้ทำพินัยกรรม: **{plan.full_name}**\n"
        f"Nationality / สัญชาติ: {plan.nationality}\n"
        f"Passport/ID No. / เลขที่หนังสือเดินทาง/บัตรประชาชน: {plan.passport_or_id_number}\n"
        f"Date of birth / วันเกิด: {plan.date_of_birth}\n"
        f"Address in Thailand / ที่อยู่ในประเทศไทย: {plan.thai_address}\n\n"
    )
    out += (
        "Made under Civil and Commercial Code Section 1656 (Ordinary Written Will). "
        "This will disposes of my Thai-situated assets (ทรัพย์สินในประเทศไทย) only.\n"
        "ทำขึ้นตามประมวลกฎหมายแพ่งและพาณิชย์ มาตรา 1656 พินัยกรรมฉบับนี้จัดการเฉพาะทรัพย์สินในประเทศไทยเท่านั้น\n\n"
    )
    if plan.has_foreign_will:
        out += (
            "**Carve-out clause / ข้อกำหนดไม่เพิกถอนพินัยกรรมอื่น:** This will does not revoke, "
            "and is not revoked by, any will executed in another jurisdiction disposing of "
            "assets located outside Thailand.\n"
            "พินัยกรรมฉบับนี้ไม่เพิกถอนและไม่ถูกเพิกถอนโดยพินัยกรรมฉบับอื่นที่ทำขึ้นในต่างประเทศซึ่งจัดการทรัพย์สินนอกประเทศไทย\n\n"
        )
    else:
        out += (
            "**Note:** No foreign will is currently on file. If you hold assets outside "
            "Thailand, consider executing a home-country will with a matching carve-out "
            "clause.\n\n"
        )

    out += "## Executor / ผู้จัดการมรดก\n"
    out += f"Name / ชื่อ: {plan.executor_name}\n"
    if plan.executor_based_in_thailand is False:
        out += (
            "⚠️ Executor is based outside Thailand and must appear in person before the "
            "Thai probate court. Consider naming a Thai-based executor.\n"
        )
    out += "\n## Beneficiaries and Bequests / ผู้รับพินัยกรรมและทรัพย์สินที่ยกให้\n"
    if plan.beneficiaries:
        for b in plan.beneficiaries:
            desc = b.asset_description or "TBD"
            out += f"- {b.name} ({b.relationship}): {desc}\n"
    else:
        out += "- TBD — list each beneficiary and the asset(s) bequeathed to them.\n"
    out += "\n"
    out += (
        "## Execution / การลงนาม\n"
        "Signed by the testator, dated at the time of making, before at least two "
        "witnesses present at the same time, who also sign to certify the testator's "
        "signature.\n"
        "ผู้ทำพินัยกรรมลงลายมือชื่อ ลงวันที่ในขณะทำพินัยกรรม ต่อหน้าพยานอย่างน้อย 2 คนซึ่งอยู่พร้อมกัน "
        "และพยานลงลายมือชื่อรับรองลายมือชื่อของผู้ทำพินัยกรรม\n\n"
        f"Testator signature / ลายมือชื่อผู้ทำพินัยกรรม: ____________________   "
        "Date / วันที่: __________\n\n"
    )
    out += _witness_block(plan)
    return out


def render_living_will(plan: EstatePlan) -> str:
    out = _header(
        "Living Will / Advance Directive (National Health Act B.E. 2550, Section 12)",
        "หนังสือแสดงเจตนาล่วงหน้า (มาตรา 12 พ.ร.บ.สุขภาพแห่งชาติ พ.ศ. 2550)",
    )
    out += (
        f"I, **{plan.full_name}** (Passport/ID {plan.passport_or_id_number}), being of "
        "sound mind, declare that if I am in a terminal stage of illness or condition "
        "and treatment would only prolong the dying process or cause unnecessary "
        "suffering, I wish to refuse or withdraw treatment that serves only to prolong "
        "such condition. This directive concerns medical treatment only and has no "
        "effect on the disposition of my property.\n\n"
        f"ข้าพเจ้า **{plan.full_name}** (เลขที่หนังสือเดินทาง/บัตรประชาชน {plan.passport_or_id_number}) "
        "ในขณะมีสติสัมปชัญญะสมบูรณ์ ขอแสดงเจตนาว่าหากข้าพเจ้าอยู่ในระยะสุดท้ายของชีวิตและการรักษาเป็นเพียงการยืดการตาย "
        "หรือทำให้ทุกข์ทรมานโดยไม่จำเป็น ข้าพเจ้าขอปฏิเสธหรือถอนการรักษาที่มีผลเพียงยืดสภาวะดังกล่าวออกไป "
        "หนังสือฉบับนี้เกี่ยวกับการรักษาพยาบาลเท่านั้น ไม่เกี่ยวข้องกับการจัดการทรัพย์สิน\n\n"
        "This directive permits withholding/withdrawing treatment (passive) only. It "
        "does not authorize active euthanasia, which remains illegal in Thailand.\n"
        "หนังสือฉบับนี้อนุญาตเฉพาะการปฏิเสธ/ถอนการรักษา (passive) เท่านั้น ไม่ใช่การกระทำให้ถึงแก่ความตาย "
        "(active euthanasia) ซึ่งยังผิดกฎหมายในประเทศไทย\n\n"
    )
    out += (
        "Please give a copy of this document to your hospital, healthcare proxy, and "
        "family. / กรุณามอบสำเนาเอกสารนี้แก่โรงพยาบาล ผู้รับมอบอำนาจด้านสุขภาพ และครอบครัว\n\n"
        f"Signature / ลายมือชื่อ: ____________________   Date / วันที่: __________\n\n"
    )
    out += _witness_block(plan)
    return out


def render_medical_poa(plan: EstatePlan) -> str:
    out = _header(
        "Medical Power of Attorney", "หนังสือมอบอำนาจด้านสุขภาพ"
    )
    out += (
        f"I, **{plan.full_name}** (Passport/ID {plan.passport_or_id_number}), appoint "
        f"**{plan.healthcare_proxy_name}** as my healthcare proxy (ผู้รับมอบอำนาจด้านสุขภาพ) "
        "to make real-time medical decisions on my behalf if I become incapacitated and "
        "unable to communicate my own wishes.\n\n"
        f"ข้าพเจ้า **{plan.full_name}** (เลขที่หนังสือเดินทาง/บัตรประชาชน {plan.passport_or_id_number}) "
        f"แต่งตั้งให้ **{plan.healthcare_proxy_name}** เป็นผู้รับมอบอำนาจด้านสุขภาพ "
        "เพื่อตัดสินใจด้านการรักษาพยาบาลแทนข้าพเจ้าในกรณีที่ข้าพเจ้าไม่สามารถสื่อสารเจตนาของตนเองได้\n\n"
        "This appointment should be read together with my Living Will / Advance "
        "Directive. Copies should be given to the hospital, proxy, and family.\n"
        "การแต่งตั้งนี้ควรอ่านประกอบกับหนังสือแสดงเจตนาล่วงหน้าของข้าพเจ้า และควรมอบสำเนาแก่โรงพยาบาล "
        "ผู้รับมอบอำนาจ และครอบครัว\n\n"
        f"Signature / ลายมือชื่อ: ____________________   Date / วันที่: __________\n\n"
    )
    out += _witness_block(plan)
    return out


def render_asset_inventory(plan: EstatePlan) -> str:
    out = _header("Asset Inventory", "บัญชีทรัพย์สิน")
    out += f"Owner / เจ้าของ: {plan.full_name}\n\n"

    def line(label_en, label_th, present):
        mark = "☑" if present else "☐"
        return f"{mark} {label_en} / {label_th}"

    out += "## Real estate / ที่ดินและสิ่งปลูกสร้าง\n"
    out += line("Land (title deed / Chanote)", "ที่ดิน (โฉนดที่ดิน)", plan.owns_land) + "\n"
    out += line("Condominium unit", "ห้องชุด", plan.owns_condo) + "\n"
    if plan.owns_land and plan.status != "thai_national":
        out += (
            "  ⚠️ Foreign heir needs Ministry of Interior permission to retain land "
            "(Land Code Section 87 area cap).\n"
        )
    if plan.owns_condo and plan.status != "thai_national":
        out += (
            "  ⚠️ Foreign heir must qualify under the Condominium Act's foreign quota "
            "or dispose of the unit within ~1 year.\n"
        )
    out += "\n## Vehicles / ยานพาหนะ\nRegistration book (ทะเบียนรถ): _______________\n\n"
    out += (
        "## Business / ธุรกิจ\nCompany affidavit / shareholder register / Foreign "
        "Business License (if applicable): _______________\n\n"
    )
    out += "## Leases / สัญญาเช่า\n"
    out += line("Has a lease", "มีสัญญาเช่า", plan.has_lease) + "\n"
    if plan.has_lease and plan.has_lease_with_succession_clause is False:
        out += "  ⚠️ Lease terminates on death — no succession clause on file.\n"
    out += (
        "\n## Financial accounts / บัญชีการเงิน\nThai bank accounts / foreign accounts / "
        "insurance policies / safe deposit box: _______________\n\n"
        "## Digital assets / สินทรัพย์ดิจิทัล\nCrypto wallets / domains / online "
        "businesses: _______________\n\n"
        "## Identity & registration documents / เอกสารประจำตัวและทะเบียน\n"
        f"Passport/ID / หนังสือเดินทาง/บัตรประชาชน: {plan.passport_or_id_number}\n"
    )
    if plan.married_to_thai:
        registered = (
            "registered at the Amphur"
            if plan.marriage_registered_at_amphur
            else "⚠️ NOT confirmed as registered at the Amphur — confirm registration"
        )
        out += f"Marriage certificate ({plan.spouse_name}): {registered}\n"
    return out


DOCUMENT_RENDERERS = {
    "last_will": ("Last Will", render_last_will),
    "living_will": ("Living Will", render_living_will),
    "medical_poa": ("Medical Power of Attorney", render_medical_poa),
    "asset_inventory": ("Asset Inventory", render_asset_inventory),
}
