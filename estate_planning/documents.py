"""Draft document generators in English, Thai, or dual language.

All output is a DRAFT for review by a licensed Thai probate/estate lawyer before
signing or witnessing. Nothing produced here is legal advice.
"""

from .asset_schema import ASSET_FIELD_SCHEMA, SPECIAL_KEYS, field_label
from .bequests import asset_label, summarize
from .models import ASSET_CATEGORIES, EstatePlan


def _cell(value):
    """Escape a value for a Markdown table cell."""
    return str(value).replace("|", r"\|").replace("\n", " ").strip()


def _asset_detail_text(asset, mode):
    """Notes cell text: category-specific detail fields plus the user's notes."""
    schema = ASSET_FIELD_SCHEMA.get(asset.category)
    parts = []
    if schema:
        skip = {schema["primary"], schema["reference"]} | SPECIAL_KEYS
        for key, value in asset.details.items():
            if key in skip:
                continue
            parts.append(f"{field_label(asset.category, key, mode)}: {value}")
    extra = "; ".join(parts)
    if extra and asset.notes:
        return f"{extra}; {asset.notes}"
    return extra or asset.notes

MODE_EN = "en"
MODE_TH = "th"
MODE_DUAL = "dual"
LANGUAGE_MODES = (MODE_EN, MODE_TH, MODE_DUAL)
LANGUAGE_LABELS = {
    MODE_EN: "English",
    MODE_TH: "Thai / ไทย",
    MODE_DUAL: "Dual (English + Thai)",
}

DISCLAIMER_EN = (
    "DRAFT ONLY — not legal advice. Verify with a licensed Thai probate/estate "
    "lawyer and confirm current law before signing or witnessing this document."
)
DISCLAIMER_TH = (
    "ร่างเอกสารเท่านั้น — ไม่ใช่คำแนะนำทางกฎหมาย กรุณาตรวจสอบกับทนายความด้านมรดกที่มีใบอนุญาต "
    "และยืนยันกฎหมายปัจจุบันก่อนลงนามหรือให้พยานลงนามในเอกสารนี้"
)


def _t(mode, en, th):
    """Block text: English, Thai, or both on separate lines."""
    if mode == MODE_EN:
        return en
    if mode == MODE_TH:
        return th
    return f"{en}\n{th}"


def _lbl(mode, en, th):
    """Inline label pair: 'English', 'ไทย', or 'English / ไทย'."""
    if mode == MODE_EN:
        return en
    if mode == MODE_TH:
        return th
    return f"{en} / {th}"


def _header(mode, title_en, title_th):
    if mode == MODE_EN:
        title = f"# {title_en}\n\n"
        disclaimer = f"*{DISCLAIMER_EN}*\n\n"
    elif mode == MODE_TH:
        title = f"# {title_th}\n\n"
        disclaimer = f"*{DISCLAIMER_TH}*\n\n"
    else:
        title = f"# {title_en}\n# {title_th}\n\n"
        disclaimer = f"*{DISCLAIMER_EN}*\n*{DISCLAIMER_TH}*\n\n"
    return title + disclaimer + "---\n\n"


def _witness_block(mode, plan):
    out = f"## {_lbl(mode, 'Witnesses', 'พยาน')}\n"
    name_lbl = _lbl(mode, "Name", "ชื่อ")
    id_lbl = _lbl(mode, "ID/Passport", "บัตรประชาชน/หนังสือเดินทาง")
    sig_lbl = _lbl(mode, "Signature", "ลายมือชื่อ")
    date_lbl = _lbl(mode, "Date", "วันที่")
    witnesses = plan.witnesses or []
    for i in range(max(2, len(witnesses))):
        w = witnesses[i] if i < len(witnesses) else None
        name = w.name if w else "____________________"
        id_no = w.id_or_passport if w else "____________________"
        out += (
            f"{i + 1}. {name_lbl}: {name}   {id_lbl}: {id_no}   "
            f"{sig_lbl}: ____________________   {date_lbl}: __________\n"
        )
    return out


def _asset_line(asset, mode):
    val = f" — {asset.value_thb:,.0f} THB" if asset.value_thb else ""
    return f"  - {asset_label(asset)}{val}\n"


def _render_bequests(plan, mode):
    """Who-gets-what: each beneficiary with their mapped assets, plus any
    unassigned assets or assets named to someone not in the beneficiary list."""
    summary = summarize(plan)
    out = ""
    has_content = (
        summary["beneficiaries"] or summary["unknown"] or summary["unassigned"]
    )
    if not has_content:
        return (
            "- "
            + _t(
                mode,
                "List each beneficiary and the asset(s) bequeathed to them.",
                "ระบุผู้รับพินัยกรรมแต่ละคนและทรัพย์สินที่ยกให้",
            )
            + "\n"
        )

    for row in summary["beneficiaries"]:
        out += f"- **{row['name']}** ({row['relationship']})\n"
        if row["bequest_text"]:
            out += f"  - {row['bequest_text']}\n"
        for a in row["assets"]:
            out += _asset_line(a, mode)
        if row["mapped_total"]:
            out += (
                f"  - {_lbl(mode, 'Subtotal', 'ยอดรวม')}: "
                f"{row['mapped_total']:,.0f} THB\n"
            )
        if not row["bequest_text"] and not row["assets"]:
            out += (
                "  - "
                + _t(
                    mode,
                    "(no specific assets assigned yet)",
                    "(ยังไม่ได้ระบุทรัพย์สิน)",
                )
                + "\n"
            )

    for u in summary["unknown"]:
        warn = _t(
            mode,
            f'Assets assigned to "{u["name"]}", who is not in the beneficiary '
            "list — add them as a beneficiary.",
            f'ทรัพย์สินที่มอบให้ "{u["name"]}" ซึ่งไม่อยู่ในรายชื่อผู้รับ — โปรดเพิ่มเป็นผู้รับ',
        )
        out += f"- ⚠ {warn}\n"
        for a in u["assets"]:
            out += _asset_line(a, mode)

    if summary["unassigned"]:
        out += (
            "- "
            + _t(
                mode,
                "Unassigned assets (no beneficiary named):",
                "ทรัพย์สินที่ยังไม่ได้ระบุผู้รับ:",
            )
            + "\n"
        )
        for a in summary["unassigned"]:
            out += _asset_line(a, mode)

    return out


def render_last_will(plan: EstatePlan, mode: str = MODE_DUAL) -> str:
    out = _header(
        mode,
        "Last Will and Testament (Ordinary Written Will)",
        "พินัยกรรมแบบธรรมดา",
    )
    out += f"{_lbl(mode, 'Testator', 'ผู้ทำพินัยกรรม')}: **{plan.full_name}**\n"
    out += f"{_lbl(mode, 'Nationality', 'สัญชาติ')}: {plan.nationality}\n"
    out += (
        f"{_lbl(mode, 'Passport/ID No.', 'เลขที่หนังสือเดินทาง/บัตรประชาชน')}: "
        f"{plan.passport_or_id_number}\n"
    )
    out += f"{_lbl(mode, 'Date of birth', 'วันเกิด')}: {plan.date_of_birth}\n"
    out += (
        f"{_lbl(mode, 'Address in Thailand', 'ที่อยู่ในประเทศไทย')}: "
        f"{plan.thai_address}\n\n"
    )
    out += (
        _t(
            mode,
            "Made under Civil and Commercial Code Section 1656 (Ordinary Written "
            "Will). This will disposes of my Thai-situated assets only.",
            "ทำขึ้นตามประมวลกฎหมายแพ่งและพาณิชย์ มาตรา 1656 พินัยกรรมฉบับนี้จัดการเฉพาะทรัพย์สินในประเทศไทยเท่านั้น",
        )
        + "\n\n"
    )
    if plan.has_foreign_will:
        out += (
            f"**{_lbl(mode, 'Carve-out clause', 'ข้อกำหนดไม่เพิกถอนพินัยกรรมอื่น')}:** "
            + _t(
                mode,
                "This will does not revoke, and is not revoked by, any will executed "
                "in another jurisdiction disposing of assets located outside Thailand.",
                "พินัยกรรมฉบับนี้ไม่เพิกถอนและไม่ถูกเพิกถอนโดยพินัยกรรมฉบับอื่นที่ทำขึ้นในต่างประเทศซึ่งจัดการทรัพย์สินนอกประเทศไทย",
            )
            + "\n\n"
        )
    else:
        out += (
            _t(
                mode,
                "**Note:** No foreign will is currently on file. If you hold assets "
                "outside Thailand, consider executing a home-country will with a "
                "matching carve-out clause.",
                "**หมายเหตุ:** ยังไม่มีพินัยกรรมต่างประเทศ หากท่านมีทรัพย์สินนอกประเทศไทย "
                "ควรทำพินัยกรรมในประเทศนั้นพร้อมข้อกำหนดไม่เพิกถอนซึ่งกันและกัน",
            )
            + "\n\n"
        )

    out += f"## {_lbl(mode, 'Executor', 'ผู้จัดการมรดก')}\n"
    out += f"{_lbl(mode, 'Name', 'ชื่อ')}: {plan.executor_name}\n"
    if plan.executor_based_in_thailand is False:
        out += (
            "⚠️ "
            + _t(
                mode,
                "Executor is based outside Thailand and must appear in person before "
                "the Thai probate court. Consider naming a Thai-based executor.",
                "ผู้จัดการมรดกอยู่ต่างประเทศและต้องมาปรากฏตัวต่อศาลด้วยตนเอง ควรพิจารณาแต่งตั้งผู้จัดการมรดกที่อยู่ในประเทศไทย",
            )
            + "\n"
        )
    out += (
        f"\n## {_lbl(mode, 'Beneficiaries and Bequests', 'ผู้รับพินัยกรรมและทรัพย์สินที่ยกให้')}\n"
    )
    out += _render_bequests(plan, mode)
    out += "\n"
    if plan.assets:
        out += (
            "> "
            + _t(
                mode,
                "A detailed inventory of these assets (account numbers, locations) is "
                "kept separately for the executor's use. That inventory is an "
                "administrative aid, not part of this will. To make a detailed "
                "schedule of assets legally binding it must be signed and witnessed "
                "with the same formalities as this will — confirm with a Thai lawyer.",
                "รายการทรัพย์สินโดยละเอียด (เลขที่บัญชี ที่ตั้ง) จัดเก็บแยกต่างหากเพื่อใช้โดยผู้จัดการมรดก "
                "บัญชีดังกล่าวเป็นเพียงเอกสารประกอบการบริหารจัดการ ไม่ใช่ส่วนหนึ่งของพินัยกรรมฉบับนี้ "
                "หากต้องการให้บัญชีทรัพย์สินโดยละเอียดมีผลผูกพันตามกฎหมาย ต้องลงนามและมีพยานตามแบบพิธีเดียวกับพินัยกรรมนี้ "
                "โปรดตรวจสอบกับทนายความไทย",
            )
            + "\n\n"
        )
    out += f"## {_lbl(mode, 'Execution', 'การลงนาม')}\n"
    out += (
        _t(
            mode,
            "Signed by the testator, dated at the time of making, before at least two "
            "witnesses present at the same time, who also sign to certify the "
            "testator's signature.",
            "ผู้ทำพินัยกรรมลงลายมือชื่อ ลงวันที่ในขณะทำพินัยกรรม ต่อหน้าพยานอย่างน้อย 2 คนซึ่งอยู่พร้อมกัน "
            "และพยานลงลายมือชื่อรับรองลายมือชื่อของผู้ทำพินัยกรรม",
        )
        + "\n\n"
    )
    out += (
        f"{_lbl(mode, 'Testator signature', 'ลายมือชื่อผู้ทำพินัยกรรม')}: "
        f"____________________   {_lbl(mode, 'Date', 'วันที่')}: __________\n\n"
    )
    out += _witness_block(mode, plan)
    return out


# Selectable living-will directives. Each is phrased within the Section 12
# framework: passive refusal of life-prolonging treatment in the terminal stage
# only (active euthanasia/assisted dying is illegal in Thailand). Acceptance of
# any specific directive can vary — confirm with the hospital and a Thai lawyer.
# key -> {label_en, label_th, clause_en, clause_th, kind: "refuse"|"request"}
LIVING_WILL_OPTIONS = {
    "dnr": {
        "label_en": "Do not attempt resuscitation (DNR / no CPR)",
        "label_th": "ไม่ต้องการการช่วยฟื้นคืนชีพ (DNR / งดการปั๊มหัวใจ)",
        "clause_en": "I do not wish to receive cardiopulmonary resuscitation (CPR) if my heart or breathing stops in that terminal condition.",
        "clause_th": "ข้าพเจ้าไม่ประสงค์จะได้รับการช่วยฟื้นคืนชีพ (CPR) หากหัวใจหรือการหายใจหยุดในภาวะระยะสุดท้ายดังกล่าว",
        "kind": "refuse",
    },
    "ventilator": {
        "label_en": "No mechanical ventilation to prolong dying",
        "label_th": "ไม่ใช้เครื่องช่วยหายใจเพื่อยืดการตาย",
        "clause_en": "I do not wish to be placed on, or kept on, a mechanical ventilator solely to prolong my dying.",
        "clause_th": "ข้าพเจ้าไม่ประสงค์จะถูกใส่หรือคงไว้ซึ่งเครื่องช่วยหายใจเพียงเพื่อยืดการตายของข้าพเจ้า",
        "kind": "refuse",
    },
    "feeding_tube": {
        "label_en": "No artificial nutrition/hydration by tube to prolong dying",
        "label_th": "ไม่ให้อาหารหรือน้ำทางสายยางเพื่อยืดการตาย",
        "clause_en": "I do not wish to receive artificial nutrition or hydration by tube where it serves only to prolong my dying.",
        "clause_th": "ข้าพเจ้าไม่ประสงค์จะได้รับอาหารหรือน้ำทางสายยางในกรณีที่เป็นเพียงการยืดการตาย",
        "kind": "refuse",
    },
    "dialysis": {
        "label_en": "No dialysis to prolong dying",
        "label_th": "ไม่ฟอกไตเพื่อยืดการตาย",
        "clause_en": "I do not wish to receive dialysis where it serves only to prolong my dying.",
        "clause_th": "ข้าพเจ้าไม่ประสงค์จะได้รับการฟอกไตในกรณีที่เป็นเพียงการยืดการตาย",
        "kind": "refuse",
    },
    "comfort_care": {
        "label_en": "Provide palliative / comfort care and pain relief",
        "label_th": "ให้การดูแลแบบประคับประคองและบรรเทาความเจ็บปวด",
        "clause_en": "I wish to receive palliative and comfort care, including adequate relief of pain and distress.",
        "clause_th": "ข้าพเจ้าประสงค์จะได้รับการดูแลแบบประคับประคองและการบรรเทาความเจ็บปวดและความทุกข์ทรมานอย่างเพียงพอ",
        "kind": "request",
    },
    "place_of_death": {
        "label_en": "Prefer to spend final days at home / in a peaceful setting",
        "label_th": "ประสงค์จะใช้ช่วงสุดท้ายของชีวิตที่บ้านหรือในที่ที่สงบ",
        "clause_en": "Where medically appropriate, I wish to spend my final days at home or in a peaceful setting rather than receiving further life-prolonging treatment in hospital.",
        "clause_th": "หากเหมาะสมทางการแพทย์ ข้าพเจ้าประสงค์จะใช้ช่วงสุดท้ายของชีวิตที่บ้านหรือในสถานที่ที่สงบ แทนการรับการรักษาเพื่อยืดชีวิตต่อไปในโรงพยาบาล",
        "kind": "request",
    },
    "spiritual_care": {
        "label_en": "Receive spiritual / religious care per my beliefs",
        "label_th": "ได้รับการดูแลด้านจิตวิญญาณ/ศาสนาตามความเชื่อของข้าพเจ้า",
        "clause_en": "I wish to receive spiritual or religious care in accordance with my beliefs.",
        "clause_th": "ข้าพเจ้าประสงค์จะได้รับการดูแลด้านจิตวิญญาณหรือศาสนาตามความเชื่อของข้าพเจ้า",
        "kind": "request",
    },
}


def render_living_will(plan: EstatePlan, mode: str = MODE_DUAL) -> str:
    out = _header(
        mode,
        "Living Will / Advance Directive (National Health Act B.E. 2550, Section 12)",
        "หนังสือแสดงเจตนาล่วงหน้า (มาตรา 12 พ.ร.บ.สุขภาพแห่งชาติ พ.ศ. 2550)",
    )
    out += (
        _t(
            mode,
            f"I, **{plan.full_name}** (Passport/ID {plan.passport_or_id_number}), being "
            "of sound mind, declare that if I am in a terminal stage of illness or "
            "condition and treatment would only prolong the dying process or cause "
            "unnecessary suffering, I wish to refuse or withdraw treatment that serves "
            "only to prolong such condition. This directive concerns medical treatment "
            "only and has no effect on the disposition of my property.",
            f"ข้าพเจ้า **{plan.full_name}** (เลขที่หนังสือเดินทาง/บัตรประชาชน "
            f"{plan.passport_or_id_number}) ในขณะมีสติสัมปชัญญะสมบูรณ์ "
            "ขอแสดงเจตนาว่าหากข้าพเจ้าอยู่ในระยะสุดท้ายของชีวิตและการรักษาเป็นเพียงการยืดการตาย "
            "หรือทำให้ทุกข์ทรมานโดยไม่จำเป็น ข้าพเจ้าขอปฏิเสธหรือถอนการรักษาที่มีผลเพียงยืดสภาวะดังกล่าวออกไป "
            "หนังสือฉบับนี้เกี่ยวกับการรักษาพยาบาลเท่านั้น ไม่เกี่ยวข้องกับการจัดการทรัพย์สิน",
        )
        + "\n\n"
    )
    out += (
        _t(
            mode,
            "This directive permits withholding/withdrawing treatment (passive) only. "
            "It does not authorize active euthanasia, which remains illegal in Thailand.",
            "หนังสือฉบับนี้อนุญาตเฉพาะการปฏิเสธ/ถอนการรักษา (passive) เท่านั้น ไม่ใช่การกระทำให้ถึงแก่ความตาย "
            "(active euthanasia) ซึ่งยังผิดกฎหมายในประเทศไทย",
        )
        + "\n\n"
    )

    # Selected specific directives.
    selected = [k for k in (plan.living_will_options or []) if k in LIVING_WILL_OPTIONS]
    if selected or plan.living_will_other:
        out += (
            f"## {_lbl(mode, 'Specific instructions', 'คำสั่งเฉพาะ')}\n"
            + _t(
                mode,
                "In that terminal situation, the following apply. (Confirm each with "
                "your hospital and a Thai lawyer, as acceptance of specific directives "
                "can vary.)",
                "ในภาวะระยะสุดท้ายดังกล่าว ให้เป็นไปตามข้อกำหนดต่อไปนี้ (โปรดยืนยันแต่ละข้อกับโรงพยาบาลและทนายความไทย "
                "เนื่องจากการยอมรับคำสั่งเฉพาะอาจแตกต่างกัน)",
            )
            + "\n\n"
        )
        for key in selected:
            opt = LIVING_WILL_OPTIONS[key]
            out += "- " + _t(mode, opt["clause_en"], opt["clause_th"]) + "\n"
        if plan.living_will_other:
            out += (
                f"- {_lbl(mode, 'Additional wishes', 'ความประสงค์เพิ่มเติม')}: "
                f"{plan.living_will_other}\n"
            )
        out += "\n"

    out += (
        _t(
            mode,
            "Please give a copy of this document to your hospital, healthcare proxy, "
            "and family.",
            "กรุณามอบสำเนาเอกสารนี้แก่โรงพยาบาล ผู้รับมอบอำนาจด้านสุขภาพ และครอบครัว",
        )
        + "\n\n"
    )
    out += (
        f"{_lbl(mode, 'Signature', 'ลายมือชื่อ')}: ____________________   "
        f"{_lbl(mode, 'Date', 'วันที่')}: __________\n\n"
    )
    out += _witness_block(mode, plan)
    return out


def render_medical_poa(plan: EstatePlan, mode: str = MODE_DUAL) -> str:
    out = _header(mode, "Medical Power of Attorney", "หนังสือมอบอำนาจด้านสุขภาพ")
    out += (
        _t(
            mode,
            f"I, **{plan.full_name}** (Passport/ID {plan.passport_or_id_number}), "
            f"appoint **{plan.healthcare_proxy_name}** as my healthcare proxy to make "
            "real-time medical decisions on my behalf if I become incapacitated and "
            "unable to communicate my own wishes.",
            f"ข้าพเจ้า **{plan.full_name}** (เลขที่หนังสือเดินทาง/บัตรประชาชน "
            f"{plan.passport_or_id_number}) แต่งตั้งให้ **{plan.healthcare_proxy_name}** "
            "เป็นผู้รับมอบอำนาจด้านสุขภาพ เพื่อตัดสินใจด้านการรักษาพยาบาลแทนข้าพเจ้าในกรณีที่ข้าพเจ้าไม่สามารถสื่อสารเจตนาของตนเองได้",
        )
        + "\n\n"
    )
    out += (
        _t(
            mode,
            "This appointment should be read together with my Living Will / Advance "
            "Directive. Copies should be given to the hospital, proxy, and family.",
            "การแต่งตั้งนี้ควรอ่านประกอบกับหนังสือแสดงเจตนาล่วงหน้าของข้าพเจ้า และควรมอบสำเนาแก่โรงพยาบาล "
            "ผู้รับมอบอำนาจ และครอบครัว",
        )
        + "\n\n"
    )
    out += (
        f"{_lbl(mode, 'Signature', 'ลายมือชื่อ')}: ____________________   "
        f"{_lbl(mode, 'Date', 'วันที่')}: __________\n\n"
    )
    out += _witness_block(mode, plan)
    return out


def render_asset_inventory(plan: EstatePlan, mode: str = MODE_DUAL) -> str:
    out = _header(mode, "Asset Inventory", "บัญชีทรัพย์สิน")
    out += f"{_lbl(mode, 'Owner', 'เจ้าของ')}: {plan.full_name}\n\n"
    out += (
        "> "
        + _t(
            mode,
            "This inventory is an administrative record to help your executor locate "
            "your assets. It is not a will and does not, by itself, transfer anything. "
            "Any beneficiary noted here reflects your intention only — the binding "
            "gifts are those made in a properly executed will.",
            "บัญชีนี้เป็นเอกสารประกอบการบริหารจัดการเพื่อช่วยให้ผู้จัดการมรดกค้นหาทรัพย์สินของท่าน "
            "ไม่ใช่พินัยกรรมและไม่ได้โอนสิ่งใดด้วยตัวเอง ผู้รับที่ระบุไว้ที่นี่แสดงเจตนาของท่านเท่านั้น "
            "การยกให้ที่มีผลผูกพันคือการยกให้ในพินัยกรรมที่ทำขึ้นอย่างถูกต้อง",
        )
        + "\n\n"
    )

    # Itemized asset sheet (from online entry or an uploaded sheet). The
    # Beneficiary column only appears if at least one asset has been assigned —
    # assigning beneficiaries is optional (you can just track assets).
    if plan.assets:
        show_beneficiary = any(a.beneficiary for a in plan.assets)
        out += f"## {_lbl(mode, 'Itemized assets', 'รายการทรัพย์สิน')}\n\n"
        headers = [
            _lbl(mode, "Category", "หมวดหมู่"),
            _lbl(mode, "Description", "รายละเอียด"),
            _lbl(mode, "Value (THB)", "มูลค่า (บาท)"),
            _lbl(mode, "Location / Reference", "ที่ตั้ง / เอกสารอ้างอิง"),
        ]
        if show_beneficiary:
            headers.append(_lbl(mode, "Beneficiary", "ผู้รับมรดก"))
        headers.append(_lbl(mode, "Notes", "หมายเหตุ"))
        out += "| " + " | ".join(headers) + " |\n"
        out += "|" + "|".join(["---"] * len(headers)) + "|\n"
        total = 0.0
        for a in plan.assets:
            total += a.value_thb or 0.0
            cat = ASSET_CATEGORIES.get(a.category, a.category)
            value = f"{a.value_thb:,.0f}" if a.value_thb else ""
            row = [_cell(cat), _cell(a.description), value, _cell(a.location)]
            if show_beneficiary:
                row.append(_cell(a.beneficiary))
            row.append(_cell(_asset_detail_text(a, mode)))
            out += "| " + " | ".join(row) + " |\n"
        out += (
            f"\n**{_lbl(mode, 'Total listed value', 'มูลค่ารวมที่ระบุ')}: "
            f"{total:,.0f} THB**\n\n"
        )

    def line(en, th, present):
        mark = "☑" if present else "☐"
        return f"{mark} {_lbl(mode, en, th)}"

    out += f"## {_lbl(mode, 'Real estate', 'ที่ดินและสิ่งปลูกสร้าง')}\n"
    out += line("Land (title deed / Chanote)", "ที่ดิน (โฉนดที่ดิน)", plan.owns_land) + "\n"
    out += line("Condominium unit", "ห้องชุด", plan.owns_condo) + "\n"
    out += (
        "  "
        + _t(
            mode,
            "Value based on the official government appraised value (ราคาประเมินราชการ), "
            "not market price — look it up at https://assessprice.treasury.go.th",
            "มูลค่าอ้างอิงจากราคาประเมินราชการ ไม่ใช่ราคาตลาด — ตรวจสอบได้ที่ https://assessprice.treasury.go.th",
        )
        + "\n"
    )
    if plan.owns_land and plan.status != "thai_national":
        out += (
            "  ⚠️ "
            + _t(
                mode,
                "Foreign heir needs Ministry of Interior permission to retain land "
                "(Land Code Section 87 area cap).",
                "ทายาทต่างชาติต้องได้รับอนุญาตจากกระทรวงมหาดไทยเพื่อถือครองที่ดิน (จำกัดพื้นที่ตามประมวลกฎหมายที่ดิน มาตรา 87)",
            )
            + "\n"
        )
    if plan.owns_condo and plan.status != "thai_national":
        out += (
            "  ⚠️ "
            + _t(
                mode,
                "Foreign heir must qualify under the Condominium Act's foreign quota "
                "or dispose of the unit within ~1 year.",
                "ทายาทต่างชาติต้องเข้าเกณฑ์โควตาต่างชาติตามพระราชบัญญัติอาคารชุด หรือจำหน่ายห้องชุดภายในประมาณ 1 ปี",
            )
            + "\n"
        )
    out += (
        f"\n## {_lbl(mode, 'Vehicles', 'ยานพาหนะ')}\n"
        f"{_lbl(mode, 'Registration book', 'ทะเบียนรถ')}: _______________\n\n"
    )
    out += (
        f"## {_lbl(mode, 'Business', 'ธุรกิจ')}\n"
        + _t(
            mode,
            "Company affidavit / shareholder register / Foreign Business License "
            "(if applicable)",
            "หนังสือรับรองบริษัท / บัญชีผู้ถือหุ้น / ใบอนุญาตประกอบธุรกิจของคนต่างด้าว (ถ้ามี)",
        )
        + ": _______________\n\n"
    )
    out += f"## {_lbl(mode, 'Leases', 'สัญญาเช่า')}\n"
    out += line("Has a lease", "มีสัญญาเช่า", plan.has_lease) + "\n"
    if plan.has_lease and plan.has_lease_with_succession_clause is False:
        out += (
            "  ⚠️ "
            + _t(
                mode,
                "Lease terminates on death — no succession clause on file.",
                "สัญญาเช่าสิ้นสุดเมื่อผู้เช่าเสียชีวิต — ไม่มีข้อกำหนดการสืบทอด",
            )
            + "\n"
        )
    out += (
        f"\n## {_lbl(mode, 'Financial accounts', 'บัญชีการเงิน')}\n"
        + _t(
            mode,
            "Thai bank accounts / foreign accounts / insurance policies / safe "
            "deposit box",
            "บัญชีธนาคารไทย / บัญชีต่างประเทศ / กรมธรรม์ประกันภัย / ตู้นิรภัย",
        )
        + ": _______________\n\n"
    )
    out += (
        f"## {_lbl(mode, 'Digital assets', 'สินทรัพย์ดิจิทัล')}\n"
        + _t(
            mode,
            "Crypto wallets / domains / online businesses",
            "กระเป๋าคริปโต / โดเมน / ธุรกิจออนไลน์",
        )
        + ": _______________\n\n"
    )
    out += (
        f"## {_lbl(mode, 'Identity & registration documents', 'เอกสารประจำตัวและทะเบียน')}\n"
        f"{_lbl(mode, 'Passport/ID', 'หนังสือเดินทาง/บัตรประชาชน')}: "
        f"{plan.passport_or_id_number}\n"
    )
    if plan.married_to_thai:
        if plan.marriage_registered_at_amphur:
            registered = _t(
                mode, "registered at the Amphur", "จดทะเบียนที่อำเภอ"
            )
        else:
            registered = "⚠️ " + _t(
                mode,
                "NOT confirmed as registered at the Amphur — confirm registration",
                "ยังไม่ยืนยันว่าจดทะเบียนที่อำเภอ — โปรดยืนยันการจดทะเบียน",
            )
        out += (
            f"{_lbl(mode, 'Marriage certificate', 'ทะเบียนสมรส')} "
            f"({plan.spouse_name}): {registered}\n"
        )
    return out


# key -> (English title, Thai title, renderer)
DOCUMENT_SPECS = {
    "last_will": ("Last Will", "พินัยกรรม", render_last_will),
    "living_will": ("Living Will", "หนังสือแสดงเจตนาล่วงหน้า", render_living_will),
    "medical_poa": (
        "Medical Power of Attorney",
        "หนังสือมอบอำนาจด้านสุขภาพ",
        render_medical_poa,
    ),
    "asset_inventory": ("Asset Inventory", "บัญชีทรัพย์สิน", render_asset_inventory),
}

# Backwards-compatible mapping used by the CLI: key -> (title, renderer).
DOCUMENT_RENDERERS = {
    key: (en_title, renderer) for key, (en_title, _th, renderer) in DOCUMENT_SPECS.items()
}


def document_title(key, mode=MODE_DUAL):
    en_title, th_title, _renderer = DOCUMENT_SPECS[key]
    return _lbl(mode, en_title, th_title)


def generate(plan, keys=None, mode=MODE_DUAL):
    """Return {key: (title, content)} for the requested document keys."""
    if keys is None:
        keys = list(DOCUMENT_SPECS.keys())
    result = {}
    for key in keys:
        if key not in DOCUMENT_SPECS:
            continue
        en_title, _th_title, renderer = DOCUMENT_SPECS[key]
        result[key] = (document_title(key, mode), renderer(plan, mode))
    return result
