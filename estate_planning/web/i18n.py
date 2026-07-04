"""Interface (chrome) translations for the web app: English and Thai.

This is separate from the *document output* language chosen in the questionnaire.
Here we translate the UI itself — buttons, labels, headings, flash messages.
"""

UI_LANGS = ("en", "th")
DEFAULT_UI_LANG = "en"

TRANSLATIONS = {
    # Chrome
    "brand": {"en": "Estate Planning · Thailand", "th": "การวางแผนมรดก · ประเทศไทย"},
    "nav_questionnaire": {"en": "Questionnaire", "th": "แบบสอบถาม"},
    "nav_preview": {"en": "Preview", "th": "ดูตัวอย่าง"},
    "nav_logout": {"en": "Log out", "th": "ออกจากระบบ"},
    "banner": {
        "en": "Not legal advice · Not yet reviewed by a lawyer · Drafts only — verify with a licensed Thai probate/estate lawyer before signing.",
        "th": "ไม่ใช่คำแนะนำทางกฎหมาย · ยังไม่ผ่านการตรวจโดยทนายความ · เป็นเพียงร่างเอกสาร — โปรดตรวจสอบกับทนายความด้านมรดกที่มีใบอนุญาตก่อนลงนาม",
    },
    "footer": {
        "en": "Informational tool encoding publicly available Thai statutory rules. No attorney–client relationship is created. Use at your own discretion.",
        "th": "เครื่องมือให้ข้อมูลที่อ้างอิงกฎหมายไทยที่เผยแพร่ทั่วไป ไม่ก่อให้เกิดความสัมพันธ์ระหว่างทนายความกับลูกความ ใช้งานตามดุลยพินิจของท่านเอง",
    },
    "theme_toggle": {"en": "Dark mode", "th": "โหมดมืด"},

    # Login / register
    "login_title": {"en": "Log in", "th": "เข้าสู่ระบบ"},
    "google_signin": {"en": "Sign in with Google", "th": "เข้าสู่ระบบด้วย Google"},
    "or": {"en": "or", "th": "หรือ"},
    "username": {"en": "Username", "th": "ชื่อผู้ใช้"},
    "password": {"en": "Password", "th": "รหัสผ่าน"},
    "password_hint": {"en": "(at least 8 characters)", "th": "(อย่างน้อย 8 ตัวอักษร)"},
    "login_btn": {"en": "Log in", "th": "เข้าสู่ระบบ"},
    "no_account": {"en": "No account?", "th": "ยังไม่มีบัญชี?"},
    "create_one": {"en": "Create one", "th": "สร้างบัญชี"},
    "register_title": {"en": "Create account", "th": "สร้างบัญชี"},
    "create_account_btn": {"en": "Create account", "th": "สร้างบัญชี"},
    "have_account": {"en": "Already have an account?", "th": "มีบัญชีอยู่แล้ว?"},

    # Terms
    "terms_title": {"en": "Before you continue", "th": "ก่อนดำเนินการต่อ"},
    "terms_lead": {
        "en": "This tool is not legal advice and has not been reviewed by a lawyer. It is an informational tool that encodes publicly available Thai statutory rules (Civil and Commercial Code, National Health Act B.E. 2550) to help you organize your estate planning and produce draft documents.",
        "th": "เครื่องมือนี้ไม่ใช่คำแนะนำทางกฎหมายและยังไม่ผ่านการตรวจโดยทนายความ เป็นเพียงเครื่องมือให้ข้อมูลที่อ้างอิงกฎหมายไทยที่เผยแพร่ทั่วไป (ประมวลกฎหมายแพ่งและพาณิชย์ และพระราชบัญญัติสุขภาพแห่งชาติ พ.ศ. 2550) เพื่อช่วยจัดระเบียบการวางแผนมรดกและจัดทำร่างเอกสาร",
    },
    "terms_point_1": {
        "en": "Using this tool does not create an attorney–client relationship.",
        "th": "การใช้เครื่องมือนี้ไม่ก่อให้เกิดความสัมพันธ์ระหว่างทนายความกับลูกความ",
    },
    "terms_point_2": {
        "en": "Every document it generates is a draft. Do not sign or have anyone witness a document until a licensed Thai probate/estate lawyer has reviewed it.",
        "th": "เอกสารทุกฉบับที่สร้างขึ้นเป็นเพียงร่าง อย่าลงนามหรือให้ผู้ใดเป็นพยานจนกว่าทนายความด้านมรดกที่มีใบอนุญาตจะตรวจสอบแล้ว",
    },
    "terms_point_3": {
        "en": "Laws and tax thresholds change. Figures and rules here may be out of date; you are responsible for verifying current law.",
        "th": "กฎหมายและเกณฑ์ภาษีเปลี่ยนแปลงได้ ตัวเลขและกฎเกณฑ์ในที่นี้อาจล้าสมัย ท่านมีหน้าที่ตรวจสอบกฎหมายปัจจุบัน",
    },
    "terms_point_4": {
        "en": "The advice is generated from the answers you provide and cannot account for the full facts of your situation.",
        "th": "คำแนะนำสร้างจากคำตอบที่ท่านให้ และไม่สามารถครอบคลุมข้อเท็จจริงทั้งหมดในสถานการณ์ของท่าน",
    },
    "terms_point_5": {
        "en": "You use this tool at your own discretion and risk.",
        "th": "ท่านใช้เครื่องมือนี้ตามดุลยพินิจและความเสี่ยงของท่านเอง",
    },
    "terms_checkbox": {
        "en": "I understand this is not legal advice, has not been reviewed by a lawyer, and that all output is a draft I must verify with a licensed Thai lawyer.",
        "th": "ข้าพเจ้าเข้าใจว่านี่ไม่ใช่คำแนะนำทางกฎหมาย ยังไม่ผ่านการตรวจโดยทนายความ และผลลัพธ์ทั้งหมดเป็นเพียงร่างที่ข้าพเจ้าต้องตรวจสอบกับทนายความไทยที่มีใบอนุญาต",
    },
    "terms_btn": {"en": "I acknowledge — continue", "th": "ข้าพเจ้ารับทราบ — ดำเนินการต่อ"},
    "terms_must_ack": {
        "en": "You must acknowledge the terms to continue.",
        "th": "ท่านต้องยอมรับเงื่อนไขเพื่อดำเนินการต่อ",
    },

    # Flash messages
    "flash_account_created": {
        "en": "Account created. Please log in.",
        "th": "สร้างบัญชีแล้ว กรุณาเข้าสู่ระบบ",
    },
    "flash_invalid_login": {
        "en": "Invalid username or password.",
        "th": "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง",
    },
    "flash_google_not_configured": {
        "en": "Google sign-in is not configured on this server.",
        "th": "ยังไม่ได้ตั้งค่าการเข้าสู่ระบบด้วย Google บนเซิร์ฟเวอร์นี้",
    },
    "flash_google_failed": {
        "en": "Google sign-in failed. Please try again.",
        "th": "การเข้าสู่ระบบด้วย Google ล้มเหลว กรุณาลองใหม่",
    },
    "flash_google_email": {
        "en": "Could not verify your Google email.",
        "th": "ไม่สามารถยืนยันอีเมล Google ของท่านได้",
    },
    "flash_csv_failed": {
        "en": "Could not read the uploaded asset sheet. Check it is a CSV file.",
        "th": "ไม่สามารถอ่านไฟล์บัญชีทรัพย์สินที่อัปโหลดได้ โปรดตรวจสอบว่าเป็นไฟล์ CSV",
    },

    # Assets section
    "q_assets_sheet_legend": {"en": "Asset sheet", "th": "บัญชีทรัพย์สิน"},
    "q_assets_sheet_hint": {
        "en": "List your assets below, or download the template to fill in offline and upload it.",
        "th": "ระบุทรัพย์สินด้านล่าง หรือดาวน์โหลดแม่แบบเพื่อกรอกออฟไลน์แล้วอัปโหลด",
    },
    "q_download_template": {"en": "⬇ Download CSV template", "th": "⬇ ดาวน์โหลดแม่แบบ CSV"},
    "q_upload_csv": {"en": "⬆ Upload filled sheet (CSV)", "th": "⬆ อัปโหลดไฟล์ที่กรอกแล้ว (CSV)"},
    "q_upload_hint": {
        "en": "The uploaded sheet is imported when you submit this form (the button at the bottom). You can also type assets directly below.",
        "th": "ไฟล์ที่อัปโหลดจะถูกนำเข้าเมื่อท่านส่งแบบฟอร์มนี้ (ปุ่มด้านล่าง) หรือจะพิมพ์ทรัพย์สินด้านล่างโดยตรงก็ได้",
    },
    "q_upload_chosen": {"en": "Selected file:", "th": "ไฟล์ที่เลือก:"},
    "q_add_asset": {"en": "+ Add asset", "th": "+ เพิ่มทรัพย์สิน"},
    "q_asset_category": {"en": "Category", "th": "หมวดหมู่"},
    "q_asset_description": {"en": "Description", "th": "รายละเอียด"},
    "q_asset_value": {"en": "Value (THB)", "th": "มูลค่า (บาท)"},
    "q_asset_location": {"en": "Location / reference", "th": "ที่ตั้ง / เอกสารอ้างอิง"},
    "q_asset_notes": {"en": "Notes", "th": "หมายเหตุ"},

    # Tax planning
    "r_taxplan_title": {"en": "Inheritance tax planning", "th": "การวางแผนภาษีมรดก"},
    "r_taxplan_total_estate": {"en": "Total listed estate", "th": "มูลค่ากองมรดกที่ระบุรวม"},
    "r_taxplan_total_tax": {"en": "Estimated inheritance tax", "th": "ประมาณการภาษีมรดก"},
    "r_taxplan_tips": {"en": "Planning suggestions", "th": "ข้อเสนอแนะการวางแผน"},
    "r_taxplan_none": {
        "en": "Add beneficiaries with values to see a tax estimate.",
        "th": "เพิ่มผู้รับพร้อมมูลค่าเพื่อดูประมาณการภาษี",
    },
    "r_tips_title": {"en": "Tips & reminders", "th": "เคล็ดลับและข้อควรจำ"},

    # Questionnaire
    "q_title": {"en": "Estate planning questionnaire", "th": "แบบสอบถามการวางแผนมรดก"},
    "q_preview_link": {"en": "Preview blank templates →", "th": "ดูตัวอย่างเอกสารเปล่า →"},
    "q_intro": {
        "en": "Only fields marked * are required. Everything else is optional — leave a blank to fill it in by hand on the printed draft. Nothing you enter is saved on the server.",
        "th": "เฉพาะช่องที่มีเครื่องหมาย * เท่านั้นที่จำเป็น ช่องอื่นเป็นทางเลือก — เว้นว่างไว้เพื่อเติมด้วยลายมือบนร่างที่พิมพ์ออกมา ข้อมูลที่ท่านกรอกจะไม่ถูกบันทึกบนเซิร์ฟเวอร์",
    },
    "q_docs_legend": {"en": "Documents to create", "th": "เอกสารที่ต้องการสร้าง"},
    "q_docs_hint": {
        "en": "Choose which documents to generate. Only the questions relevant to your selection are shown.",
        "th": "เลือกเอกสารที่ต้องการสร้าง จะแสดงเฉพาะคำถามที่เกี่ยวข้องกับการเลือกของท่าน",
    },
    "q_doclang_legend": {"en": "Document language", "th": "ภาษาของเอกสาร"},
    "q_about_legend": {"en": "About you", "th": "เกี่ยวกับท่าน"},
    "q_full_name": {"en": "Full legal name", "th": "ชื่อ-นามสกุลตามกฎหมาย"},
    "q_nationality": {"en": "Nationality", "th": "สัญชาติ"},
    "q_passport": {"en": "Passport / ID number", "th": "หมายเลขหนังสือเดินทาง / บัตรประชาชน"},
    "q_dob": {"en": "Date of birth", "th": "วันเกิด"},
    "q_address": {"en": "Address in Thailand", "th": "ที่อยู่ในประเทศไทย"},
    "q_status": {"en": "Which status applies to you?", "th": "สถานะใดที่ตรงกับท่าน?"},
    "q_status_choose": {"en": "— choose —", "th": "— เลือก —"},
    "q_status_thai": {"en": "Thai national", "th": "คนไทย"},
    "q_status_foreign": {
        "en": "Foreign resident / property owner / married to a Thai national",
        "th": "ชาวต่างชาติที่พำนัก / เจ้าของทรัพย์สิน / สมรสกับคนไทย",
    },
    "q_status_visitor": {
        "en": "Occasional visitor, no Thai assets",
        "th": "ผู้มาเยือนเป็นครั้งคราว ไม่มีทรัพย์สินในไทย",
    },
    "q_existing_legend": {"en": "Existing documents", "th": "เอกสารที่มีอยู่"},
    "q_has_thai_will": {"en": "I already have a Thai will", "th": "ข้าพเจ้ามีพินัยกรรมไทยอยู่แล้ว"},
    "q_has_foreign_will": {
        "en": "I already have a foreign (home-country) will",
        "th": "ข้าพเจ้ามีพินัยกรรมต่างประเทศ (ประเทศบ้านเกิด) อยู่แล้ว",
    },
    "q_assets_legend": {"en": "Assets & family", "th": "ทรัพย์สินและครอบครัว"},
    "q_owns_land": {"en": "I own land in Thailand", "th": "ข้าพเจ้าเป็นเจ้าของที่ดินในประเทศไทย"},
    "q_owns_condo": {
        "en": "I own a condominium unit in Thailand",
        "th": "ข้าพเจ้าเป็นเจ้าของห้องชุดในประเทศไทย",
    },
    "q_has_lease": {"en": "I hold a lease in Thailand", "th": "ข้าพเจ้ามีสัญญาเช่าในประเทศไทย"},
    "q_lease_succession": {
        "en": "Does the lease include a succession clause?",
        "th": "สัญญาเช่ามีข้อกำหนดการสืบทอดหรือไม่?",
    },
    "q_married": {"en": "I am married to a Thai national", "th": "ข้าพเจ้าสมรสกับคนไทย"},
    "q_spouse_name": {"en": "Spouse's full name", "th": "ชื่อ-นามสกุลของคู่สมรส"},
    "q_marriage_registered": {
        "en": "Is the marriage registered at the Amphur (Section 1457)?",
        "th": "การสมรสจดทะเบียนที่อำเภอหรือไม่ (มาตรา 1457)?",
    },
    "q_people_legend": {"en": "People to designate", "th": "บุคคลที่ต้องแต่งตั้ง"},
    "q_executor_name": {"en": "Executor's full name", "th": "ชื่อ-นามสกุลผู้จัดการมรดก"},
    "q_executor_in_th": {
        "en": "Is the executor based in Thailand?",
        "th": "ผู้จัดการมรดกอยู่ในประเทศไทยหรือไม่?",
    },
    "q_proxy_name": {"en": "Healthcare proxy's full name", "th": "ชื่อ-นามสกุลผู้รับมอบอำนาจด้านสุขภาพ"},
    "q_livingwill_legend": {"en": "Living will directives", "th": "คำสั่งในหนังสือแสดงเจตนา"},
    "q_livingwill_hint": {
        "en": "Choose the specific instructions to include in your living will. These apply only in a terminal stage where treatment would merely prolong dying. Thai law (Section 12) permits refusing life-prolonging treatment (passive) but not active euthanasia. Acceptance of specific directives can vary — confirm each with your hospital and a Thai lawyer before relying on it.",
        "th": "เลือกคำสั่งเฉพาะที่จะรวมไว้ในหนังสือแสดงเจตนาของท่าน คำสั่งเหล่านี้ใช้เฉพาะในภาวะระยะสุดท้ายที่การรักษาเป็นเพียงการยืดการตาย กฎหมายไทย (มาตรา 12) อนุญาตให้ปฏิเสธการรักษาเพื่อยืดชีวิต (passive) แต่ไม่อนุญาตการทำให้ถึงแก่ความตาย โปรดยืนยันแต่ละข้อกับโรงพยาบาลและทนายความไทยก่อนนำไปใช้",
    },
    "q_livingwill_other": {"en": "Additional wishes (free text)", "th": "ความประสงค์เพิ่มเติม (ข้อความอิสระ)"},
    "q_witnesses_legend": {"en": "Witnesses", "th": "พยาน"},
    "q_witnesses_hint": {
        "en": "at least 2 recommended for a will",
        "th": "แนะนำอย่างน้อย 2 คนสำหรับพินัยกรรม",
    },
    "q_add_witness": {"en": "+ Add witness", "th": "+ เพิ่มพยาน"},
    "q_beneficiaries_legend": {"en": "Beneficiaries", "th": "ผู้รับพินัยกรรม"},
    "q_add_beneficiary": {"en": "+ Add beneficiary", "th": "+ เพิ่มผู้รับพินัยกรรม"},
    "q_submit": {"en": "Get advice & draft documents", "th": "รับคำแนะนำและร่างเอกสาร"},
    "q_optional": {"en": "optional", "th": "ไม่บังคับ"},
    "q_skip_visitor": {
        "en": "optional — skip if occasional visitor",
        "th": "ไม่บังคับ — ข้ามได้หากเป็นผู้มาเยือนชั่วคราว",
    },

    # Preview
    "pv_title": {"en": "Preview blank templates", "th": "ดูตัวอย่างเอกสารเปล่า"},
    "pv_fill_link": {"en": "Fill in my details →", "th": "กรอกข้อมูลของฉัน →"},
    "pv_intro": {
        "en": "These are the document templates with [placeholders] where your details would go. No information is required to view them.",
        "th": "นี่คือแม่แบบเอกสารพร้อม [ช่องว่าง] สำหรับใส่ข้อมูลของท่าน ไม่ต้องกรอกข้อมูลใด ๆ เพื่อดู",
    },
    "pv_documents": {"en": "Documents", "th": "เอกสาร"},
    "pv_language": {"en": "Language", "th": "ภาษา"},
    "pv_update": {"en": "Update preview", "th": "อัปเดตตัวอย่าง"},

    # Results
    "r_advice_title": {"en": "Your advice", "th": "คำแนะนำสำหรับท่าน"},
    "r_recommendations": {"en": "Recommendations", "th": "ข้อแนะนำ"},
    "r_warnings": {"en": "Warnings", "th": "ข้อควรระวัง"},
    "r_tax": {
        "en": "Estimated inheritance tax by beneficiary",
        "th": "ประมาณการภาษีมรดกแยกตามผู้รับ",
    },
    "r_docs_title": {"en": "Draft documents", "th": "ร่างเอกสาร"},
    "r_download": {"en": "Download all as ZIP", "th": "ดาวน์โหลดทั้งหมดเป็น ZIP"},
    "r_draft_note": {
        "en": "These are drafts. Have a licensed Thai lawyer review each one before signing or witnessing.",
        "th": "เอกสารเหล่านี้เป็นร่าง โปรดให้ทนายความไทยที่มีใบอนุญาตตรวจสอบแต่ละฉบับก่อนลงนามหรือเป็นพยาน",
    },
    "r_start_over": {"en": "← Start over", "th": "← เริ่มใหม่"},
}


def t(key, lang):
    entry = TRANSLATIONS.get(key)
    if not entry:
        return key
    return entry.get(lang) or entry.get(DEFAULT_UI_LANG) or key
