"""
補充報告：可行性評估 / 行銷模式規劃 / VIP定義 / 即期商品銷售評定
追加至主報告，單獨輸出為 PPTX
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ── Palette ──────────────────────────────────────
GREEN_DARK  = RGBColor(0x1B, 0x5E, 0x20)
GREEN_MID   = RGBColor(0x2E, 0x7D, 0x32)
GREEN_LIGHT = RGBColor(0x66, 0xBB, 0x6A)
AMBER       = RGBColor(0xF5, 0x7F, 0x17)
AMBER_LIGHT = RGBColor(0xFF, 0xE0, 0x82)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
GRAY_DARK   = RGBColor(0x21, 0x21, 0x21)
GRAY_MID    = RGBColor(0x42, 0x42, 0x42)
GRAY_LIGHT  = RGBColor(0xF5, 0xF5, 0xF5)
CREAM       = RGBColor(0xF9, 0xFB, 0xE7)
RED_WARN    = RGBColor(0xC6, 0x28, 0x28)
BLUE_MID    = RGBColor(0x15, 0x65, 0xC0)
PURPLE      = RGBColor(0x6A, 0x1B, 0x9A)
GOLD        = RGBColor(0xF9, 0xA8, 0x25)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

# ── Helpers ──────────────────────────────────────
def rect(slide, l, t, w, h, fill=None, lc=None, lw=Pt(0)):
    s = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    s.line.fill.background()
    if fill:
        s.fill.solid(); s.fill.fore_color.rgb = fill
    else:
        s.fill.background()
    if lc:
        s.line.color.rgb = lc; s.line.width = lw
    else:
        s.line.fill.background()
    return s

def txt(slide, text, l, t, w, h, fs=13, bold=False, color=GRAY_DARK,
        align=PP_ALIGN.LEFT, italic=False):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tb.word_wrap = True
    tf = tb.text_frame; tf.word_wrap = True
    p  = tf.paragraphs[0]; p.alignment = align
    r  = p.add_run(); r.text = text
    r.font.size = Pt(fs); r.font.bold = bold
    r.font.italic = italic; r.font.color.rgb = color
    return tb

def header(slide, title, sub=""):
    rect(slide, 0, 0, 13.33, 1.1, fill=GREEN_DARK)
    txt(slide, title, 0.35, 0.1, 11, 0.65, fs=26, bold=True, color=WHITE)
    if sub:
        txt(slide, sub, 0.35, 0.72, 11, 0.35, fs=13, color=GREEN_LIGHT)
    rect(slide, 0, 7.25, 13.33, 0.25, fill=GREEN_MID)

def sec(slide, label, l, t, w, h, bg=CREAM, hc=GREEN_MID):
    rect(slide, l, t, w, 0.38, fill=hc)
    txt(slide, label, l+0.12, t+0.03, w-0.2, 0.35, fs=13, bold=True, color=WHITE)
    rect(slide, l, t+0.38, w, h-0.38, fill=bg, lc=GREEN_LIGHT, lw=Pt(1))
    return (l+0.15, t+0.5, w-0.3, h-0.55)

def bullets(slide, label, items, l, t, w, h, icon="●", hc=GREEN_MID, fs=12):
    ix, iy, iw, ih = sec(slide, label, l, t, w, h, hc=hc)
    tb = slide.shapes.add_textbox(Inches(ix), Inches(iy), Inches(iw), Inches(ih))
    tb.word_wrap = True; tf = tb.text_frame; tf.word_wrap = True
    first = True
    for item in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False; p.alignment = PP_ALIGN.LEFT; p.space_before = Pt(5)
        r = p.add_run(); r.text = f"{icon} {item}"
        r.font.size = Pt(fs); r.font.color.rgb = GRAY_MID

def kpi(slide, label, value, unit, l, t, w=2.5, h=1.3, vc=GREEN_DARK, bg=WHITE):
    rect(slide, l, t, w, h, fill=bg, lc=GREEN_LIGHT, lw=Pt(1.5))
    rect(slide, l, t, w, 0.06, fill=GREEN_MID)
    txt(slide, label, l+0.1, t+0.08, w-0.2, 0.35, fs=11, color=GRAY_MID, align=PP_ALIGN.CENTER)
    txt(slide, value, l+0.1, t+0.35, w-0.2, 0.55, fs=22, bold=True, color=vc, align=PP_ALIGN.CENTER)
    if unit:
        txt(slide, unit, l+0.1, t+0.88, w-0.2, 0.3, fs=10, color=GRAY_MID, align=PP_ALIGN.CENTER)

def mtxt(tf, text, fs=12, bold=False, color=GRAY_DARK, align=PP_ALIGN.LEFT, sp=Pt(5)):
    p = tf.add_paragraph(); p.alignment = align; p.space_before = sp
    r = p.add_run(); r.text = text
    r.font.size = Pt(fs); r.font.bold = bold; r.font.color.rgb = color

# ═══════════════════════════════════════════════════════════════════
# SLIDE 1 — 封面
# ═══════════════════════════════════════════════════════════════════
s0 = prs.slides.add_slide(BLANK)
rect(s0, 0, 0, 13.33, 7.5, fill=GREEN_DARK)
rect(s0, 0, 5.5, 13.33, 2.0, fill=GREEN_MID)
rect(s0, 0, 6.85, 13.33, 0.65, fill=AMBER)
txt(s0, "複合式蔬果店 — 經營策略補充報告", 0.8, 0.7, 11.73, 1.1,
    fs=36, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s0, "桃園市平鎮區平德路 271 號 1 樓｜店面約 50 坪", 0.8, 1.85, 11.73, 0.6,
    fs=16, color=GREEN_LIGHT, align=PP_ALIGN.CENTER)
rect(s0, 3.8, 2.6, 5.73, 0.06, fill=AMBER)
topics = ["A  可行性評估", "B  行銷模式規劃", "C  VIP 定義與制度", "D  即期商品銷售評定"]
for i, tp in enumerate(topics):
    lx = 0.6 + (i % 2) * 6.2
    ly = 2.8 + (i // 2) * 1.0
    rect(s0, lx, ly, 5.8, 0.78, fill=GREEN_MID)
    txt(s0, tp, lx+0.18, ly+0.15, 5.5, 0.5, fs=17, bold=True, color=WHITE)
txt(s0, "評估日期：2026年5月", 0.8, 4.9, 11.73, 0.45,
    fs=12, color=RGBColor(0xC8,0xE6,0xC9), align=PP_ALIGN.CENTER)
txt(s0, "CONFIDENTIAL  ·  僅供內部決策使用", 0, 6.9, 13.33, 0.4,
    fs=11, color=WHITE, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════════════════════════
# SLIDE 2 — 可行性評估（一）：評估框架
# ═══════════════════════════════════════════════════════════════════
s2 = prs.slides.add_slide(BLANK)
header(s2, "A｜可行性評估（一）：五力評估框架", "全面檢視本案開店的可行條件")

# 5 dimension bars
dims = [
    ("市場需求可行性", 88, "平鎮區人口22.8萬、住宅密集，生鮮蔬果日常剛性需求高，市場基礎穩固", GREEN_MID),
    ("財務可行性",    62, "啟動資金249-401萬，需月營收53-65萬達損益平衡，風險中等，需嚴格財務管控", AMBER),
    ("競爭可行性",    55, "全聯、家樂福等強勢競爭，差異化複合業態為突破口，競爭壓力偏高", AMBER),
    ("營運可行性",    75, "50坪空間可完整分區，複合業態可行，關鍵在供應鏈與庫存管理", GREEN_MID),
    ("地點可行性",    70, "1樓臨路、住宅密集，台鐵站2026年啟用利多，但全聯覆蓋率高需差異化", GREEN_MID),
]
for i, (dim, score, desc, bc) in enumerate(dims):
    ty = 1.28 + i * 1.12
    rect(s2, 0.3, ty, 3.0, 0.88, fill=GRAY_LIGHT, lc=GREEN_LIGHT, lw=Pt(1))
    txt(s2, dim, 0.42, ty+0.18, 2.8, 0.5, fs=12, bold=True, color=GREEN_DARK)
    # score bar background
    rect(s2, 3.4, ty+0.22, 5.5, 0.42, fill=RGBColor(0xE0,0xE0,0xE0))
    bar_w = 5.5 * score / 100
    rect(s2, 3.4, ty+0.22, bar_w, 0.42, fill=bc)
    txt(s2, f"{score}分", 9.05, ty+0.22, 0.8, 0.42, fs=14, bold=True,
        color=bc, align=PP_ALIGN.CENTER)
    txt(s2, desc, 3.4, ty+0.68, 9.55, 0.38, fs=10, color=GRAY_MID)

# overall verdict
rect(s2, 0.3, 6.95, 12.6, 0.48, fill=GREEN_DARK)
txt(s2, "綜合可行性評分：70 / 100｜結論：條件成立，建議在強化差異化策略後進行，風險可控",
    0.5, 6.98, 12.2, 0.4, fs=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════════════════════════
# SLIDE 3 — 可行性評估（二）：財務敏感度
# ═══════════════════════════════════════════════════════════════════
s3 = prs.slides.add_slide(BLANK)
header(s3, "A｜可行性評估（二）：財務敏感度分析", "不同情境下的月損益預測")

# Scenario table
rect(s3, 0.3, 1.2, 12.6, 0.48, fill=GREEN_DARK)
for hdr, lx, wd in [("指標", 0.35, 2.3), ("悲觀情境", 2.7, 2.5),
                     ("基準情境", 5.25, 2.5), ("樂觀情境", 7.8, 2.5),
                     ("達標條件", 10.35, 2.45)]:
    txt(s3, hdr, lx, 1.25, wd, 0.38, fs=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

rows_data = [
    ("月營收", "NT$35萬", "NT$55萬", "NT$75萬", "日客60人×$350"),
    ("毛利率", "25%", "32%", "38%", "熟食佔比>30%"),
    ("毛利額", "NT$8.75萬", "NT$17.6萬", "NT$28.5萬", "—"),
    ("固定成本", "NT$17.2萬", "NT$17.2萬", "NT$17.2萬", "租金+人事+水電"),
    ("月損益", "▼ -8.45萬", "▲ +0.4萬", "▲ +11.3萬", "—"),
    ("年化損益", "▼ -101萬", "▲ +4.8萬", "▲ +135萬", "—"),
    ("回本預估", "無法回本", "約30個月", "約18個月", "基準以上可行"),
]
bg_cycle = [GRAY_LIGHT, WHITE]
val_colors = [RED_WARN, AMBER, GREEN_MID]
for r_i, row in enumerate(rows_data):
    ry = 1.72 + r_i * 0.72
    bg = bg_cycle[r_i % 2]
    rect(s3, 0.3, ry, 12.6, 0.7, fill=bg)
    txt(s3, row[0], 0.38, ry+0.14, 2.25, 0.44, fs=12, bold=True, color=GREEN_DARK)
    for ci, (val, vc) in enumerate(zip(row[1:4], val_colors)):
        bld = "▲" in val or "▼" in val
        fc = RED_WARN if "▼" in val else (GREEN_MID if "▲" in val and ci==2 else GRAY_DARK)
        txt(s3, val, 2.72+ci*2.55, ry+0.14, 2.42, 0.44, fs=12, bold=bld,
            color=fc, align=PP_ALIGN.CENTER)
    txt(s3, row[4], 10.37, ry+0.14, 2.38, 0.44, fs=11, color=GRAY_MID,
        align=PP_ALIGN.CENTER)

txt(s3, "※ 固定成本：租金5.5萬+人事8萬+水電1.8萬+雜支1.9萬=17.2萬；回本期以開店總成本300萬計算",
    0.3, 7.05, 12.5, 0.3, fs=10, italic=True, color=GRAY_MID)

# ═══════════════════════════════════════════════════════════════════
# SLIDE 4 — 可行性評估（三）：成功關鍵條件
# ═══════════════════════════════════════════════════════════════════
s4 = prs.slides.add_slide(BLANK)
header(s4, "A｜可行性評估（三）：成功關鍵條件 (KSF)", "本案能否成功的決定性因素")

ksfs = [
    ("KSF 1", "差異化商品力", GREEN_DARK,
     ["熟食現做（便當/沙拉/滷味）佔業績30%以上",
      "在地農夫直供、季節蔬果、有機專區",
      "獨家選品（台灣在地品種、無農藥認證）",
      "每週推出特色蔬果組合包（150-200元）"]),
    ("KSF 2", "社區深耕能力", GREEN_MID,
     ["建立LINE社群，定期推播當日菜價與特價",
      "與附近里辦公室、學校合作團購",
      "老主顧識別服務（認臉打招呼、記住偏好）",
      "節慶禮盒、年菜預購深化情感連結"]),
    ("KSF 3", "財務紀律管控", AMBER,
     ["進貨量控制在日銷售預測95%以內，降低耗損",
      "前6個月設月目標里程碑，低於標準立即調整",
      "熟食轉換即期品，不浪費不折損",
      "帳款每週結算，現金流透明管理"]),
    ("KSF 4", "營運效率", BLUE_MID,
     ["2名員工分工：生鮮備料+熟食製作",
      "POS庫存系統追蹤動銷率，精準採購",
      "開店前2小時完成蔬果陳列補貨",
      "供應商關係：3家以上分散風險"]),
]
for ci, (num, title, hc, pts) in enumerate(ksfs):
    lx = 0.3 + ci * 3.22
    rect(s4, lx, 1.2, 3.05, 0.48, fill=hc)
    txt(s4, f"{num}", lx+0.1, 1.23, 0.7, 0.4, fs=14, bold=True, color=AMBER if hc==GREEN_DARK else WHITE)
    txt(s4, title, lx+0.7, 1.23, 2.25, 0.4, fs=14, bold=True, color=WHITE)
    rect(s4, lx, 1.68, 3.05, 5.2, fill=CREAM, lc=hc, lw=Pt(1.5))
    tb = s4.shapes.add_textbox(Inches(lx+0.15), Inches(1.82), Inches(2.75), Inches(4.9))
    tb.word_wrap = True; tf = tb.text_frame; tf.word_wrap = True
    first = True
    for pt in pts:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False; p.space_before = Pt(9)
        r = p.add_run(); r.text = f"▶ {pt}"
        r.font.size = Pt(11.5); r.font.color.rgb = GRAY_DARK

# ═══════════════════════════════════════════════════════════════════
# SLIDE 5 — 行銷模式規劃（一）：整體策略
# ═══════════════════════════════════════════════════════════════════
s5 = prs.slides.add_slide(BLANK)
header(s5, "B｜行銷模式規劃（一）：整體行銷策略", "4P + 社區行銷 + 數位整合")

# Product
bullets(s5, "🥦 Product — 商品策略", [
    "核心品類：每日新鮮蔬果（60%）、熟食便當（20%）、乾雜有機（20%）",
    "週特選：3-5款主打蔬果，搭配食譜卡陳列，提升客單價",
    "季節限定組合包：年節禮盒、補充包、蔬菜箱訂閱制",
    "自有品牌：簡易醃漬品/調味包貼牌，提升毛利與識別度",
], 0.3, 1.2, 6.15, 3.0, hc=GREEN_DARK)

bullets(s5, "💰 Price — 定價策略", [
    "蔬果定價比全聯高5-10%，但強調新鮮度與在地性",
    "熟食便當：NT$70-120（平鎮工薪族可負擔帶走區間）",
    "會員優惠：VIP折扣5%、積點換贈品",
    "即期蔬果：下架前以5-7折出售，減少耗損",
], 6.55, 1.2, 6.5, 3.0, hc=GREEN_DARK)

bullets(s5, "📍 Place — 通路策略", [
    "實體店為核心：1樓臨路，主動製造香氣吸客（熟食區靠近門口）",
    "LINE官方帳號：每日菜單、特價推播，支援預購自取",
    "Uber Eats / foodpanda 外送上架（熟食便當）",
    "社區宅配：半徑500m 內，滿NT$500免費送達",
], 0.3, 4.35, 6.15, 2.95, hc=GREEN_MID)

bullets(s5, "📣 Promotion — 促銷策略", [
    "開幕期（1-3月）：買NT$500送50元折扣券，首購禮",
    "每週二「週中特惠日」：特定蔬果85折吸引平日回流",
    "每月「農夫日」：邀請供應農夫到場互動、試吃",
    "與學校/辦公室合作：午餐便當團購、蔬菜箱訂閱",
], 6.55, 4.35, 6.5, 2.95, hc=GREEN_MID)

# ═══════════════════════════════════════════════════════════════════
# SLIDE 6 — 行銷模式規劃（二）：社群與數位行銷
# ═══════════════════════════════════════════════════════════════════
s6 = prs.slides.add_slide(BLANK)
header(s6, "B｜行銷模式規劃（二）：社群與數位行銷", "低成本高觸及的在地數位行銷計畫")

# Channel cards
channels = [
    ("LINE 官方帳號", GREEN_DARK, [
        "每日早7點推播：今日特價蔬果+便當菜單",
        "「菜市場直播」：每週一次10分鐘直播開箱",
        "預購功能：熟食便當前一天訂，省等待時間",
        "會員折扣碼發送、生日優惠自動推播",
        "目標：開業3個月內累積300位好友",
    ]),
    ("Facebook 粉絲頁", GREEN_MID, [
        "在地社團加入曝光（平鎮生活社群、桃園媽媽團）",
        "每週發布「產地故事」貼文，建立品牌溫度",
        "顧客打卡贈小禮（一週一次抽獎活動）",
        "投放社區定向廣告：半徑1.5km、預算NT$500/週",
        "目標：開業6個月內累積500粉絲",
    ]),
    ("Google 商家", BLUE_MID, [
        "立即登錄Google商家，設定完整營業資訊",
        "蒐集5星評價：開幕首月鼓勵顧客留評",
        "定期上傳商品照、活動照，提升搜尋排名",
        "回覆每一則評論，展現服務溫度",
        "目標：3個月內累積50則好評",
    ]),
    ("外送平台整合", AMBER, [
        "Uber Eats / foodpanda 上架熟食便當品項",
        "設定午餐尖峰（11-13點）外送接單優先",
        "外送專屬組合：便當+蔬果沙拉套餐優惠",
        "外送收入可彌補店面閒時，提升坪效",
        "目標：開業2個月內上架並達月外送50單",
    ]),
]
for ci, (title, hc, pts) in enumerate(channels):
    lx = 0.3 + ci * 3.22
    rect(s6, lx, 1.2, 3.05, 0.45, fill=hc)
    txt(s6, title, lx+0.12, 1.22, 2.85, 0.4, fs=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    rect(s6, lx, 1.65, 3.05, 4.75, fill=CREAM, lc=hc, lw=Pt(1.5))
    tb = s6.shapes.add_textbox(Inches(lx+0.15), Inches(1.78), Inches(2.75), Inches(4.5))
    tb.word_wrap = True; tf = tb.text_frame; tf.word_wrap = True
    first = True
    for pt in pts:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False; p.space_before = Pt(9)
        r = p.add_run(); r.text = f"▶ {pt}"
        r.font.size = Pt(11); r.font.color.rgb = GRAY_DARK

rect(s6, 0.3, 6.52, 12.6, 0.65, fill=GREEN_DARK)
txt(s6, "行銷預算建議：開幕期 NT$8,000-12,000/月（含廣告+活動）；穩定期縮減至 NT$4,000-6,000/月",
    0.5, 6.57, 12.2, 0.52, fs=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════════════════════════
# SLIDE 7 — 行銷模式規劃（三）：年度行銷日曆
# ═══════════════════════════════════════════════════════════════════
s7 = prs.slides.add_slide(BLANK)
header(s7, "B｜行銷模式規劃（三）：年度行銷活動日曆", "12個月主題行銷節點規劃")

months = [
    ("1月", "農曆年節\n預購禮盒"),
    ("2月", "情人節\n有機蔬果禮"),
    ("3月", "春季\n在地蔬果節"),
    ("4月", "清明\n春耕採買"),
    ("5月", "母親節\n蔬果禮盒"),
    ("6月", "夏至\n冷食沙拉季"),
    ("7月", "夏季\n補充元氣週"),
    ("8月", "中元\n感恩回饋日"),
    ("9月", "中秋\n蔬果禮組合"),
    ("10月", "秋季\n根莖類特賣"),
    ("11月", "感恩\n社區日活動"),
    ("12月", "歲末\n年菜預購"),
]
mc = [GREEN_DARK, GREEN_MID, GREEN_MID, AMBER, AMBER, BLUE_MID,
      BLUE_MID, GREEN_MID, GREEN_DARK, AMBER, GREEN_MID, RED_WARN]
for i, ((mo, act), c) in enumerate(zip(months, mc)):
    col = i % 6; row = i // 6
    lx = 0.3 + col * 2.13; ty = 1.2 + row * 2.65
    rect(s7, lx, ty, 2.0, 0.45, fill=c)
    txt(s7, mo, lx+0.05, ty+0.05, 1.9, 0.35, fs=14, bold=True,
        color=WHITE, align=PP_ALIGN.CENTER)
    rect(s7, lx, ty+0.45, 2.0, 2.1, fill=CREAM, lc=c, lw=Pt(1))
    txt(s7, act, lx+0.1, ty+0.6, 1.8, 1.85, fs=12, bold=True,
        color=GRAY_DARK, align=PP_ALIGN.CENTER)

rect(s7, 0.3, 6.62, 12.6, 0.6, fill=GREEN_DARK)
txt(s7, "每月固定活動：★ 每週二特惠日  ★ 每月農夫到場日  ★ 每季新品發表  ★ 每季VIP積點兌換",
    0.5, 6.67, 12.2, 0.48, fs=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════════════════════════
# SLIDE 8 — VIP 定義（一）：制度架構
# ═══════════════════════════════════════════════════════════════════
s8 = prs.slides.add_slide(BLANK)
header(s8, "C｜VIP 定義（一）：會員制度架構", "三級會員制度設計與升等條件")

# Tier cards
tiers = [
    ("🌱 綠葉會員", "一般會員", GREEN_MID,
     "入會門檻", "免費加入（消費滿NT$200首次）",
     "每消費NT$100 → 1點（1點=1元折抵）",
     ["生日當月兌換禮物（蔬果組合包）",
      "每週特價短訊/LINE通知優先收到",
      "購物滿NT$800免費贈送1項蔬菜",
      "會員專屬小農直購價（部分品項）"]),
    ("🌿 金葉會員", "進階會員", AMBER,
     "升等條件", "單季累積消費滿 NT$3,000",
     "每消費NT$100 → 1.5點，有效期12個月",
     ["全品項享9.5折優惠",
      "每月一次「金葉專屬」新品優先試吃",
      "生日禮升級（熟食便當+蔬果禮盒）",
      "優先接受節慶禮盒預購限量名額"]),
    ("👑 白金會員", "頂級VIP", PURPLE,
     "升等條件", "單年累積消費滿 NT$15,000",
     "每消費NT$100 → 2點，永久有效",
     ["全品項享9折，含熟食便當",
      "每週免費配送蔬果箱（半徑500m內）",
      "專屬客服專線/LINE一對一服務",
      "農場參訪邀請、私廚體驗活動優先報名",
      "年終回饋：依消費總額給予5%購物金"]),
]
for ci, (name, sub, hc, lbl1, v1, v2, perks) in enumerate(tiers):
    lx = 0.3 + ci * 4.3
    rect(s8, lx, 1.2, 4.1, 0.58, fill=hc)
    txt(s8, name, lx+0.12, 1.22, 3.9, 0.35, fs=16, bold=True,
        color=WHITE, align=PP_ALIGN.CENTER)
    txt(s8, sub, lx+0.12, 1.55, 3.9, 0.22, fs=11, color=AMBER_LIGHT if hc==PURPLE else GREEN_LIGHT,
        align=PP_ALIGN.CENTER)
    rect(s8, lx, 1.78, 4.1, 5.35, fill=CREAM, lc=hc, lw=Pt(2))
    txt(s8, lbl1, lx+0.15, 1.88, 1.6, 0.3, fs=11, bold=True, color=hc)
    txt(s8, v1, lx+0.15, 2.15, 3.8, 0.5, fs=11, color=GRAY_DARK)
    txt(s8, "累積優惠", lx+0.15, 2.65, 1.6, 0.3, fs=11, bold=True, color=hc)
    txt(s8, v2, lx+0.15, 2.92, 3.8, 0.5, fs=11, color=GRAY_DARK)
    rect(s8, lx+0.12, 3.45, 3.85, 0.3, fill=hc)
    txt(s8, "✦ 專屬福利", lx+0.2, 3.47, 3.65, 0.26, fs=11, bold=True, color=WHITE)
    tb = s8.shapes.add_textbox(Inches(lx+0.15), Inches(3.8), Inches(3.8), Inches(3.15))
    tb.word_wrap = True; tf = tb.text_frame; tf.word_wrap = True
    first = True
    for pk in perks:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False; p.space_before = Pt(8)
        r = p.add_run(); r.text = f"◆ {pk}"
        r.font.size = Pt(11); r.font.color.rgb = GRAY_DARK

# ═══════════════════════════════════════════════════════════════════
# SLIDE 9 — VIP 定義（二）：積點與升降等規則
# ═══════════════════════════════════════════════════════════════════
s9 = prs.slides.add_slide(BLANK)
header(s9, "C｜VIP 定義（二）：積點兌換與升降等規則", "積點制度明細與會員管理機制")

bullets(s9, "🎯 積點規則", [
    "基礎積點：每消費NT$100 = 1點（綠葉）/ 1.5點（金葉）/ 2點（白金）",
    "點數有效期：綠葉6個月、金葉12個月、白金永久",
    "加碼積點：週二特惠日雙倍點、生日月三倍點、農夫日活動加1點",
    "點數不得轉讓，不可折現，不與其他折扣同時使用",
    "每次最少可兌換100點（NT$100折抵），無上限",
], 0.3, 1.2, 6.15, 3.8, hc=GREEN_DARK)

bullets(s9, "⬆ 升等條件（滾動計算）", [
    "綠葉→金葉：任一季度（3個月）累計消費滿 NT$3,000",
    "金葉→白金：任一年度（12個月）累計消費滿 NT$15,000",
    "升等即時生效，當日起享新等級福利",
    "升等後下一週期重新起算消費額，不影響已累積點數",
    "季度：以自然季度計算（1-3月、4-6月、7-9月、10-12月）",
], 6.55, 1.2, 6.5, 3.8, hc=AMBER)

bullets(s9, "⬇ 降等與維持條件", [
    "金葉維持：每半年消費滿 NT$1,500（未達→退回綠葉）",
    "白金維持：每年消費滿 NT$10,000（未達→退回金葉）",
    "降等前30天LINE通知提醒，給予補消費機會",
    "休眠帳號（12個月未消費）：點數清零但等級保留6個月",
], 0.3, 5.15, 6.15, 2.2, hc=RED_WARN)

bullets(s9, "📊 會員KPI目標", [
    "開業6個月：綠葉200人、金葉30人",
    "開業12個月：綠葉500人、金葉80人、白金10人",
    "VIP顧客貢獻度目標：占總業績40%以上",
    "每月一次會員回顧：分析消費行為、動態調整福利",
], 6.55, 5.15, 6.5, 2.2, hc=PURPLE)

# ═══════════════════════════════════════════════════════════════════
# SLIDE 10 — 即期商品銷售評定（一）：定義與分級
# ═══════════════════════════════════════════════════════════════════
s10 = prs.slides.add_slide(BLANK)
header(s10, "D｜即期商品銷售評定（一）：定義與分級機制", "蔬果即期品的科學管理與分級處置標準")

# Definition
rect(s10, 0.3, 1.2, 12.6, 0.72, fill=GREEN_DARK)
txt(s10, "【定義】即期商品：預估在24-72小時內將影響外觀品質或食用安全，但目前仍可安全食用的蔬果生鮮品項",
    0.5, 1.28, 12.2, 0.56, fs=13, bold=True, color=WHITE)

# Grading table
rect(s10, 0.3, 2.02, 12.6, 0.45, fill=GREEN_MID)
for hdr, lx, wd in [("等級", 0.35, 1.2), ("品相狀態", 1.6, 2.2),
                     ("剩餘時效", 3.85, 1.5), ("處置方式", 5.4, 4.2),
                     ("折扣幅度", 9.65, 3.1)]:
    txt(s10, hdr, lx, 2.06, wd, 0.35, fs=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

grade_rows = [
    ("A 級\n尚鮮", "外觀完整，輕微色澤變化，\n無明顯軟化", "48-72h",
     "即期特賣區獨立陳列，明顯標示\n「今日嚴選特惠」，保持整齊", "85折 (約-15%)", GREEN_MID),
    ("B 級\n近效", "輕微脫水、部分葉片軟化，\n仍可食用", "24-48h",
     "熟食加工轉換（炒菜料理包、\n醃漬品）或低價清倉袋裝販售", "65-75折 (約-30%)", AMBER),
    ("C 級\n待處理", "明顯軟化、部分腐爛，\n但可切除可食部位", "< 24h",
     "當日熟食烹調使用（員工餐或\n外賣便當配菜）；不可對外銷售", "不對外售", RED_WARN),
    ("D 級\n淘汰", "腐爛、發霉、有異味，\n不可食用", "已超期",
     "立即下架隔離，登記耗損紀錄，\n環保分類廚餘處理", "報廢", RGBColor(0x61, 0x61, 0x61)),
]
for ri, (grade, cond, time, action, disc, hc) in enumerate(grade_rows):
    ry = 2.5 + ri * 1.1
    bg = CREAM if ri % 2 == 0 else WHITE
    rect(s10, 0.3, ry, 12.6, 1.05, fill=bg)
    rect(s10, 0.3, ry, 1.25, 1.05, fill=hc)
    txt(s10, grade, 0.33, ry+0.18, 1.15, 0.7, fs=12, bold=True,
        color=WHITE, align=PP_ALIGN.CENTER)
    txt(s10, cond,  1.63, ry+0.1, 2.15, 0.88, fs=11, color=GRAY_DARK)
    txt(s10, time,  3.87, ry+0.28, 1.45, 0.5, fs=12, bold=True,
        color=hc, align=PP_ALIGN.CENTER)
    txt(s10, action, 5.42, ry+0.08, 4.15, 0.9, fs=11, color=GRAY_DARK)
    txt(s10, disc,  9.67, ry+0.25, 3.0, 0.55, fs=13, bold=True,
        color=hc, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════════════════════════
# SLIDE 11 — 即期商品銷售評定（二）：操作流程與財務影響
# ═══════════════════════════════════════════════════════════════════
s11 = prs.slides.add_slide(BLANK)
header(s11, "D｜即期商品銷售評定（二）：操作流程與財務效益", "標準化即期品管理流程與損耗控制目標")

bullets(s11, "⏰ 日常即期品檢查流程（SOP）", [
    "開店前（7:30）：全面檢查昨日未售出蔬果，依A/B/C/D分級",
    "A級品：移至「今日特惠區」，換上特價標籤，社群推播",
    "B級品：立即轉入熟食備料（醃漬/炒料包），當日完成轉換",
    "C/D級：填寫「耗損記錄表」，當日結算損失金額",
    "收店後（20:00）：明日預估動銷量，調整次日進貨量",
    "每週彙整：耗損率超過10%需提交改善方案",
], 0.3, 1.2, 6.15, 4.2, hc=GREEN_DARK, fs=11)

bullets(s11, "💡 即期品轉換創意方案", [
    "「今日小農嚴選袋」：即期蔬果混搭，NT$99/袋",
    "「養生湯品材料包」：根莖類即期品組合，NT$129/包",
    "「炒菜料理包」：切好洗淨的即期菜，熟食轉換",
    "員工福利包：C級品分給員工帶回，提升人心",
    "與鄰近里老人共餐合作：B/C級品公益捐贈，塑造品牌形象",
    "「明日蔬菜箱」預購：隔日現採但需當天完售，零耗損",
], 6.55, 1.2, 6.5, 4.2, hc=AMBER, fs=11)

# Financial impact KPIs
rect(s11, 0.3, 5.52, 12.6, 0.42, fill=GREEN_MID)
txt(s11, "📊 即期品管理財務目標", 0.5, 5.55, 12.0, 0.35, fs=13, bold=True, color=WHITE)

kpi_data = [
    ("目標耗損率", "≤ 8%", "業界標準10-15%"),
    ("A級轉售率", "≥ 90%", "即期品仍可創收"),
    ("B級轉換率", "≥ 80%", "熟食彌補損失"),
    ("月耗損金額", "≤ NT$8,000", "占進貨成本4%"),
]
for i, (lbl, val, note) in enumerate(kpi_data):
    kpi(s11, lbl, val, note, 0.35 + i*3.12, 6.02, w=2.95, h=1.32,
        vc=GREEN_DARK, bg=CREAM)

# ═══════════════════════════════════════════════════════════════════
# SLIDE 12 — 綜合行動計畫
# ═══════════════════════════════════════════════════════════════════
s12 = prs.slides.add_slide(BLANK)
header(s12, "總結｜綜合行動計畫與時程表", "四大主題整合推進時程")

phases = [
    ("籌備期\n（-3 → 0 月）", GREEN_DARK, [
        "完成50坪裝潢與設備採購",
        "建立供應商合作（3家以上）",
        "申請LINE官方帳號、Google商家",
        "設定POS系統與庫存管理",
        "制訂VIP制度、點數系統上線",
        "即期品SOP文件制定完成",
    ]),
    ("開幕期\n（1 → 3 月）", AMBER, [
        "開幕優惠：買千送百、免費加入會員",
        "LINE社群開放，目標300位好友",
        "每週農夫到場日活動啟動",
        "即期品每日SOP執行並記錄耗損率",
        "Uber Eats熟食便當上架",
        "每月評估財務達成率（KPI追蹤）",
    ]),
    ("成長期\n（4 → 12 月）", GREEN_MID, [
        "金葉VIP升等首批名單，辦升等禮",
        "推出「蔬菜箱訂閱制」穩定現金流",
        "有機/溯源專區獨立陳列上架",
        "社區辦公室、學校便當合作洽談",
        "即期轉換率達80%以上為目標",
        "半年財務審查，決策是否擴充熟食區",
    ]),
    ("深化期\n（13 → 24 月）", BLUE_MID, [
        "白金VIP首批認定，舉辦農場體驗",
        "評估第二店址（台鐵平鎮站附近）",
        "品牌自有醃漬/調味品上市",
        "OMO整合：APP或LINE訂購全流程",
        "年度損益達月淨利10%以上",
        "申請在地優良商店或有機認證",
    ]),
]
for ci, (phase, hc, items) in enumerate(phases):
    lx = 0.3 + ci * 3.22
    rect(s12, lx, 1.2, 3.05, 0.65, fill=hc)
    txt(s12, phase, lx+0.1, 1.22, 2.88, 0.6, fs=13, bold=True,
        color=WHITE, align=PP_ALIGN.CENTER)
    rect(s12, lx, 1.85, 3.05, 5.15, fill=CREAM, lc=hc, lw=Pt(1.5))
    tb = s12.shapes.add_textbox(Inches(lx+0.15), Inches(1.98), Inches(2.75), Inches(4.9))
    tb.word_wrap = True; tf = tb.text_frame; tf.word_wrap = True
    first = True
    for it in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False; p.space_before = Pt(8)
        r = p.add_run(); r.text = f"▶ {it}"
        r.font.size = Pt(11); r.font.color.rgb = GRAY_DARK

rect(s12, 0.3, 7.1, 12.6, 0.3, fill=GREEN_MID)
txt(s12, "每季檢核：財務達成率 / VIP人數成長 / 耗損率 / 社群觸及 — 未達標即啟動應對措施",
    0.5, 7.12, 12.2, 0.25, fs=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════════════════════════
# SLIDE 13 — 結語
# ═══════════════════════════════════════════════════════════════════
s13 = prs.slides.add_slide(BLANK)
rect(s13, 0, 0, 13.33, 7.5, fill=GREEN_DARK)
rect(s13, 0, 5.5, 13.33, 2.0, fill=GREEN_MID)
rect(s13, 0, 6.95, 13.33, 0.55, fill=AMBER)
txt(s13, "感謝閱覽", 1, 0.9, 11.33, 1.1,
    fs=44, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s13, "複合式蔬果店經營策略補充報告", 1, 2.05, 11.33, 0.65,
    fs=20, color=GREEN_LIGHT, align=PP_ALIGN.CENTER)
rect(s13, 4.2, 2.85, 4.93, 0.07, fill=AMBER)
summaries = [
    "✅ 可行性評估：綜合評分70/100，財務敏感度明確，KSF清晰",
    "✅ 行銷策略：4P + 社群數位整合，低成本高觸及在地行銷",
    "✅ VIP制度：三級會員、積點兌換、升降等機制完整",
    "✅ 即期商品：ABCD分級SOP，目標耗損率≤8%，轉換創收",
]
for i, s in enumerate(summaries):
    txt(s13, s, 2.0, 3.1 + i * 0.55, 9.33, 0.5, fs=13, color=WHITE)
txt(s13, "本報告資料截至 2026年5月｜數據來源：桃園市政府、財政部、業界公開資訊",
    1, 5.65, 11.33, 0.5, fs=11, italic=True,
    color=RGBColor(0xC8,0xE6,0xC9), align=PP_ALIGN.CENTER)
txt(s13, "CONFIDENTIAL  ·  僅供內部決策使用", 0, 7.0, 13.33, 0.42,
    fs=11, color=WHITE, align=PP_ALIGN.CENTER)

# ── Save ─────────────────────────────────────────
out = "/home/user/namecard/平鎮平德路_複合式蔬果店_經營策略補充報告.pptx"
prs.save(out)
print(f"✅ Saved: {out}")
