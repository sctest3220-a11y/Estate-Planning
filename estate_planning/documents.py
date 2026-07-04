"""Draft document generators in English, Thai, or dual language.

All output is a DRAFT for review by a licensed Thai probate/estate lawyer before
signing or witnessing. Nothing produced here is legal advice.
"""

from .models import ASSET_CATEGORIES, EstatePlan

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
    if plan.beneficiaries:
        for b in plan.beneficiaries:
            desc = b.asset_description or "____________________"
            out += f"- {b.name} ({b.relationship}): {desc}\n"
    else:
        out += (
            "- "
            + _t(
                mode,
                "List each beneficiary and the asset(s) bequeathed to them.",
                "ระบุผู้รับพินัยกรรมแต่ละคนและทรัพย์สินที่ยกให้",
            )
            + "\n"
        )
    out += "\n"
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

    # Itemized asset sheet (from online entry or an uploaded CSV).
    if plan.assets:
        out += f"## {_lbl(mode, 'Itemized assets', 'รายการทรัพย์สิน')}\n\n"
        headers = [
            _lbl(mode, "Category", "หมวดหมู่"),
            _lbl(mode, "Description", "รายละเอียด"),
            _lbl(mode, "Value (THB)", "มูลค่า (บาท)"),
            _lbl(mode, "Location / Reference", "ที่ตั้ง / เอกสารอ้างอิง"),
            _lbl(mode, "Notes", "หมายเหตุ"),
        ]
        out += "| " + " | ".join(headers) + " |\n"
        out += "|" + "|".join(["---"] * len(headers)) + "|\n"
        total = 0.0
        for a in plan.assets:
            total += a.value_thb or 0.0
            cat = ASSET_CATEGORIES.get(a.category, a.category)
            value = f"{a.value_thb:,.0f}" if a.value_thb else ""
            out += (
                f"| {cat} | {a.description} | {value} | {a.location} | {a.notes} |\n"
            )
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
