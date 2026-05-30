from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# Color Palette
GREEN_DARK   = RGBColor(0x1B, 0x5E, 0x20)   # 深綠
GREEN_MID    = RGBColor(0x2E, 0x7D, 0x32)   # 中綠
GREEN_LIGHT  = RGBColor(0x66, 0xBB, 0x6A)   # 淺綠
AMBER        = RGBColor(0xF5, 0x7F, 0x17)   # 橙黃
WHITE        = RGBColor(0xFF, 0xFF, 0xFF)
GRAY_DARK    = RGBColor(0x21, 0x21, 0x21)
GRAY_MID     = RGBColor(0x42, 0x42, 0x42)
GRAY_LIGHT   = RGBColor(0xF5, 0xF5, 0xF5)
CREAM        = RGBColor(0xF9, 0xFB, 0xE7)
RED_WARN     = RGBColor(0xC6, 0x28, 0x28)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

BLANK = prs.slide_layouts[6]  # completely blank

# ─────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────
def add_rect(slide, l, t, w, h, fill=None, line_color=None, line_width=Pt(0)):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.line.fill.background()
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = line_width
    else:
        shape.line.fill.background()
    return shape

def add_text(slide, text, l, t, w, h,
             font_size=14, bold=False, color=GRAY_DARK,
             align=PP_ALIGN.LEFT, italic=False, wrap=True):
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txb.word_wrap = wrap
    tf = txb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txb

def add_para(tf, text, font_size=13, bold=False, color=GRAY_DARK,
             align=PP_ALIGN.LEFT, space_before=Pt(4)):
    p = tf.add_paragraph()
    p.alignment = align
    p.space_before = space_before
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    return p

def slide_header(slide, title, subtitle=""):
    # top bar
    add_rect(slide, 0, 0, 13.33, 1.1, fill=GREEN_DARK)
    add_text(slide, title, 0.35, 0.1, 11, 0.65,
             font_size=26, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
    if subtitle:
        add_text(slide, subtitle, 0.35, 0.72, 11, 0.35,
                 font_size=13, bold=False, color=GREEN_LIGHT, align=PP_ALIGN.LEFT)
    # bottom accent bar
    add_rect(slide, 0, 7.25, 13.33, 0.25, fill=GREEN_MID)

def section_box(slide, label, l, t, w, h):
    add_rect(slide, l, t, w, 0.38, fill=GREEN_MID)
    add_text(slide, label, l+0.12, t+0.03, w-0.2, 0.35,
             font_size=13, bold=True, color=WHITE)
    add_rect(slide, l, t+0.38, w, h-0.38, fill=CREAM,
             line_color=GREEN_LIGHT, line_width=Pt(1))
    return (l+0.15, t+0.5, w-0.3, h-0.55)  # inner text area coords

def bullet_box(slide, label, bullets, l, t, w, h, icon="●"):
    ix, iy, iw, ih = section_box(slide, label, l, t, w, h)
    txb = slide.shapes.add_textbox(Inches(ix), Inches(iy), Inches(iw), Inches(ih))
    txb.word_wrap = True
    tf = txb.text_frame
    tf.word_wrap = True
    first = True
    for b in bullets:
        if first:
            p = tf.paragraphs[0]; first = False
        else:
            p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_before = Pt(5)
        run = p.add_run()
        run.text = f"{icon} {b}"
        run.font.size = Pt(12)
        run.font.color.rgb = GRAY_MID

def kpi_card(slide, label, value, unit, l, t, w=2.5, h=1.3,
             val_color=GREEN_DARK):
    add_rect(slide, l, t, w, h, fill=WHITE,
             line_color=GREEN_LIGHT, line_width=Pt(1.5))
    add_rect(slide, l, t, w, 0.06, fill=GREEN_MID)
    add_text(slide, label, l+0.1, t+0.08, w-0.2, 0.35,
             font_size=11, bold=False, color=GRAY_MID, align=PP_ALIGN.CENTER)
    add_text(slide, value, l+0.1, t+0.35, w-0.2, 0.55,
             font_size=22, bold=True, color=val_color, align=PP_ALIGN.CENTER)
    if unit:
        add_text(slide, unit, l+0.1, t+0.88, w-0.2, 0.3,
                 font_size=10, color=GRAY_MID, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════════════
# SLIDE 1 — 封面
# ═══════════════════════════════════════════════════════
s1 = prs.slides.add_slide(BLANK)
add_rect(s1, 0, 0, 13.33, 7.5, fill=GREEN_DARK)
add_rect(s1, 0, 0, 13.33, 7.5, fill=RGBColor(0x1B, 0x5E, 0x20))

# decorative shapes
add_rect(s1, 0, 5.5, 13.33, 2.0, fill=GREEN_MID)
add_rect(s1, 0, 6.8, 13.33, 0.7, fill=AMBER)

add_text(s1, "複合式蔬果店", 1.2, 0.8, 11, 1.2,
         font_size=42, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s1, "選址市場評估報告", 1.2, 1.9, 11, 0.9,
         font_size=34, bold=True, color=GREEN_LIGHT, align=PP_ALIGN.CENTER)

add_rect(s1, 3.5, 2.95, 6.3, 0.05, fill=AMBER)

add_text(s1, "📍 桃園市平鎮區平德路 271 號 1 樓｜店面約 50 坪",
         1.0, 3.2, 11.3, 0.6,
         font_size=16, bold=False, color=WHITE, align=PP_ALIGN.CENTER)

add_text(s1, "評估日期：2026年5月", 1.0, 4.0, 11.3, 0.5,
         font_size=13, color=GREEN_LIGHT, align=PP_ALIGN.CENTER)

add_text(s1, "包含：商圈分析 ｜ 競爭態勢 ｜ 消費潛力 ｜ 財務試算 ｜ SWOT ｜ 開店建議",
         0.8, 4.55, 11.7, 0.5,
         font_size=12, italic=True, color=RGBColor(0xC8, 0xE6, 0xC9),
         align=PP_ALIGN.CENTER)

add_text(s1, "CONFIDENTIAL  ·  僅供內部決策使用", 0, 6.85, 13.33, 0.45,
         font_size=11, color=WHITE, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════════════
# SLIDE 2 — 報告目錄
# ═══════════════════════════════════════════════════════
s2 = prs.slides.add_slide(BLANK)
slide_header(s2, "報告目錄", "市場評估報告架構")

items = [
    ("01", "地點概況與商圈環境"),
    ("02", "區域人口與消費力分析"),
    ("03", "競爭對手調查"),
    ("04", "台灣複合式蔬果店市場趨勢"),
    ("05", "財務估算與損益試算"),
    ("06", "SWOT 分析"),
    ("07", "風險評估"),
    ("08", "總結建議與開店策略"),
]

cols = [(0.4, 1.2), (6.8, 1.2)]
for i, (num, title) in enumerate(items):
    col_idx = i // 4
    row_idx = i % 4
    lx = cols[col_idx][0]
    ty = cols[col_idx][1] + row_idx * 1.45

    add_rect(s2, lx, ty, 5.9, 1.25, fill=WHITE,
             line_color=GREEN_LIGHT, line_width=Pt(1))
    add_rect(s2, lx, ty, 0.85, 1.25, fill=GREEN_MID)
    add_text(s2, num, lx+0.05, ty+0.28, 0.75, 0.65,
             font_size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s2, title, lx+1.0, ty+0.3, 4.7, 0.65,
             font_size=15, bold=True, color=GREEN_DARK, align=PP_ALIGN.LEFT)

# ═══════════════════════════════════════════════════════
# SLIDE 3 — 地點概況與商圈環境
# ═══════════════════════════════════════════════════════
s3 = prs.slides.add_slide(BLANK)
slide_header(s3, "01｜地點概況與商圈環境", "桃園市平鎮區平德路 271 號 1 樓")

# Left panel
bullet_box(s3, "📌 地點基本資訊", [
    "地址：桃園市平鎮區平德路 271 號 1 樓",
    "店面坪數：約 50 坪（約 165 m²）",
    "行政區：平鎮區（平德里附近）",
    "道路性質：平德路為平鎮區主要生活道路",
    "樓層：1 樓臨路店面，能見度佳",
    "業種定位：複合式蔬果店（生鮮+加工+熟食）",
], 0.35, 1.25, 5.9, 3.5)

bullet_box(s3, "🏘️ 周邊環境概況", [
    "半徑 500m 內：密集住宅社區、公寓大樓群",
    "鄰近平鎮區主要生活幹道，交通流量穩定",
    "周邊有學校、里民活動中心等公共設施",
    "商業型態以傳統零售、便利商店為主",
    "步行購物需求高，騎機車族為主要客群",
    "平鎮區總面積 47.75 km²，商業集中於北部",
], 6.45, 1.25, 6.5, 3.5)

# bottom KPI strip
add_rect(s3, 0.35, 4.9, 12.6, 2.1, fill=CREAM,
         line_color=GREEN_LIGHT, line_width=Pt(1))
add_rect(s3, 0.35, 4.9, 12.6, 0.38, fill=GREEN_MID)
add_text(s3, "🌟 地點優勢亮點", 0.5, 4.93, 8, 0.32,
         font_size=13, bold=True, color=WHITE)

pts = [
    "✔ 1樓臨路，購物動線自然",
    "✔ 平德路為住宅區幹道，來客流量穩定",
    "✔ 50坪空間可完整陳列生鮮+複合商品",
    "✔ 鄰近住宅密集，回購率高",
]
for i, pt in enumerate(pts):
    add_text(s3, pt, 0.5 + i * 3.15, 5.38, 3.0, 1.4,
             font_size=12, color=GREEN_DARK)

# ═══════════════════════════════════════════════════════
# SLIDE 4 — 區域人口與消費力分析
# ═══════════════════════════════════════════════════════
s4 = prs.slides.add_slide(BLANK)
slide_header(s4, "02｜區域人口與消費力分析", "平鎮區人口結構與消費潛力")

# KPI row
kpis = [
    ("平鎮區總人口", "22.8萬", "2025年估計（桃園市第三大區）"),
    ("總戶數",       "約9萬戶", "平均每戶2.5人"),
    ("人口密度",    "4,787人", "每平方公里（2020年）"),
    ("近十年成長",  "+8.4%",   "高於全國平均成長率"),
    ("房價所得比",  "8.65倍",  "桃園市（相對台北市15.4倍低）"),
]
for i, (lbl, val, unit) in enumerate(kpis):
    kpi_card(s4, lbl, val, unit, 0.3 + i*2.55, 1.2, w=2.4, h=1.4)

bullet_box(s4, "👨‍👩‍👧 人口結構特色", [
    "以青壯年（25-45歲）家庭為主體，對日用生鮮需求量大",
    "雙薪家庭比例高，追求便利、一站購足購物體驗",
    "外來移入人口持續增加，新住民比例高於全市平均",
    "中低收入家庭為主，對價格敏感，CP值導向消費",
    "人口仍在成長，社區型零售市場具擴大潛力",
], 0.3, 2.75, 6.2, 3.5)

bullet_box(s4, "💰 消費力與購買行為", [
    "台灣2024年基本月薪 NT$27,470；薪資中位數約NT$36,000",
    "桃園市房價所得比 8.65 倍，生活支出壓力低於北市",
    "蔬果蛋奶為家庭每月必要支出，需求穩定、低彈性",
    "平鎮居民習慣週末集中採購，週間補購模式",
    "有機、在地、溯源意識漸強，願意為品質溢價",
    "複合購物偏好：蔬果+乾貨+熟食一次完成",
], 6.7, 2.75, 6.2, 3.5)

# ═══════════════════════════════════════════════════════
# SLIDE 5 — 競爭對手調查
# ═══════════════════════════════════════════════════════
s5 = prs.slides.add_slide(BLANK)
slide_header(s5, "03｜競爭對手調查", "平鎮區生鮮通路競爭態勢分析")

# Table header
headers = ["競爭者", "距離", "業態", "規模", "主要優勢", "威脅程度"]
col_ws  = [2.0, 0.85, 1.5, 0.9, 3.6, 1.3]
col_x   = [0.25]
for w in col_ws[:-1]:
    col_x.append(col_x[-1] + w)

ty = 1.2
add_rect(s5, 0.25, ty, 12.8, 0.42, fill=GREEN_DARK)
for i, h in enumerate(headers):
    add_text(s5, h, col_x[i]+0.05, ty+0.05, col_ws[i]-0.1, 0.35,
             font_size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

rows = [
    ["全聯福利中心\n（平鎮環南店）", "~1.2km", "連鎖超市", "大型", "品牌信任、低價策略、\n完整商品線（含蔬果）", "⚠ 高"],
    ["全聯福利中心\n（平鎮育達店）", "~1.5km", "連鎖超市", "大型", "價格低廉、\n行銷資源豐富", "⚠ 高"],
    ["家樂福平鎮店", "~2.0km", "大型量販", "超大型", "一站購足、停車便利、\n量販價格", "⚠ 中高"],
    ["傳統攤販\n（早市/夜市）", "~0.3km", "傳統零售", "小型", "現撈現採、在地感、\n議價空間", "⚠ 中"],
    ["7-11 / 全家\n便利商店", "周邊密布", "便利商店", "小型", "24小時、便利性高、\n沙拉/即食蔬果", "⚠ 低中"],
    ["本計畫\n複合式蔬果店", "—", "特色零售", "中型50坪", "在地特色、複合服務、\n現切/熟食差異化", "自身定位"],
]
row_colors = [GRAY_LIGHT, WHITE, GRAY_LIGHT, WHITE, GRAY_LIGHT, CREAM]
warn_colors = [RED_WARN, RED_WARN, AMBER, AMBER, GREEN_MID, GREEN_DARK]

for r_idx, row in enumerate(rows):
    ry = ty + 0.42 + r_idx * 0.9
    add_rect(s5, 0.25, ry, 12.8, 0.88, fill=row_colors[r_idx])
    for c_idx, cell in enumerate(row):
        fsize = 11 if c_idx == 4 else 12
        fc = warn_colors[r_idx] if c_idx == 5 else GRAY_DARK
        bold = c_idx == 5
        add_text(s5, cell, col_x[c_idx]+0.05, ry+0.08, col_ws[c_idx]-0.1, 0.75,
                 font_size=fsize, bold=bold, color=fc, align=PP_ALIGN.CENTER)

add_text(s5, "※ 距離為概估值；複合式差異化是本案突破關鍵",
         0.3, 7.05, 12, 0.3, font_size=10, italic=True, color=GRAY_MID)

# ═══════════════════════════════════════════════════════
# SLIDE 6 — 台灣複合式蔬果店市場趨勢
# ═══════════════════════════════════════════════════════
s6 = prs.slides.add_slide(BLANK)
slide_header(s6, "04｜台灣複合式蔬果店市場趨勢", "產業環境與商機洞察")

bullet_box(s6, "📈 市場規模與成長", [
    "2024年台灣量販超市業合計營收突破 5,082 億元（年增 5.4%）",
    "生鮮蔬果為超市主要客流引擎，每週到訪率達 60% 以上",
    "有機蔬果市場年均成長 8-10%，消費主力為 30-50 歲家庭",
    "2025年食品市場趨勢：健康、在地、溯源、便利一站購足",
    "日系超市 LOPIA 進台灣不到2年，單月營收破億，熟食+生鮮雙引擎",
], 0.3, 1.2, 6.1, 4.5)

bullet_box(s6, "🛒 複合式業態優勢", [
    "「複合式」=生鮮蔬果＋熟食便當＋有機專區＋乾貨雜糧",
    "一次滿足「買菜＋帶便當」需求，提升客單價與回購率",
    "熟食區毛利率高（約 55-65%），可彌補生鮮低毛利",
    "差異化選品（在地農夫直供、季節限定）建立品牌忠誠",
    "50坪空間足夠分區陳列，體驗感優於傳統菜攤",
    "OMO 整合（LINE 訂購+自取）可延伸服務圈至 1.5km",
], 6.6, 1.2, 6.1, 4.5)

# Trend pills at bottom
add_rect(s6, 0.3, 5.85, 12.6, 1.35, fill=GREEN_DARK)
add_text(s6, "2025-2026 關鍵消費趨勢", 0.5, 5.9, 5, 0.4,
         font_size=13, bold=True, color=GREEN_LIGHT)
trends = ["🌱 減碳飲食", "🥗 蔬食增加", "📦 產地直送", "💊 機能性蔬果",
          "📱 行動訂購", "♻ 低塑包裝", "🍱 即食熟食"]
for i, tr in enumerate(trends):
    lx = 0.45 + (i % 4) * 3.1
    ly = 6.35 if i < 4 else 6.75
    add_rect(s6, lx, ly, 2.85, 0.35, fill=GREEN_MID)
    add_text(s6, tr, lx+0.08, ly+0.03, 2.7, 0.3,
             font_size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════════════
# SLIDE 7 — 財務估算（開店成本）
# ═══════════════════════════════════════════════════════
s7 = prs.slides.add_slide(BLANK)
slide_header(s7, "05｜財務估算（一）：開店成本試算", "50坪複合式蔬果店啟動資金需求")

# Cost table
add_rect(s7, 0.3, 1.2, 7.8, 0.45, fill=GREEN_DARK)
for hdr, lx, wd in [("成本項目", 0.35, 3.5), ("說明", 3.9, 2.3), ("估算金額（萬元）", 6.25, 1.8)]:
    add_text(s7, hdr, lx, 1.25, wd, 0.35, font_size=13, bold=True,
             color=WHITE, align=PP_ALIGN.CENTER)

cost_rows = [
    ("裝潢工程費", "牆面、地板、冷藏設備空間設計", "80 – 120"),
    ("冷藏冷凍設備", "生鮮冷藏櫃、冷凍庫、蔬果保鮮冰台", "60 – 90"),
    ("熟食設備", "加熱台、便當保溫設備、排油煙系統", "20 – 35"),
    ("貨架/陳列器具", "蔬果斜面架、乾貨貨架、結帳台", "15 – 25"),
    ("POS系統/設備", "收銀系統、電子秤、條碼掃描器", "5 – 10"),
    ("首批進貨備料", "蔬果、乾貨、熟食食材首批庫存", "10 – 15"),
    ("保證金（押金）", "通常 3-6 個月租金", "24 – 48"),
    ("行政/開業費用", "執照申請、保險、開幕行銷", "5 – 8"),
    ("周轉預備金", "前3個月虧損緩衝（建議）", "30 – 50"),
]
for r, (item, desc, amt) in enumerate(cost_rows):
    ry = 1.65 + r * 0.58
    bg = GRAY_LIGHT if r % 2 == 0 else WHITE
    add_rect(s7, 0.3, ry, 7.8, 0.56, fill=bg)
    add_text(s7, item, 0.38, ry+0.1, 3.4, 0.4, font_size=12, bold=True, color=GREEN_DARK)
    add_text(s7, desc, 3.85, ry+0.1, 2.3, 0.4, font_size=11, color=GRAY_MID)
    add_text(s7, amt, 6.22, ry+0.1, 1.8, 0.4, font_size=12, bold=True,
             color=AMBER, align=PP_ALIGN.CENTER)

# Total
add_rect(s7, 0.3, 6.87, 7.8, 0.46, fill=GREEN_DARK)
add_text(s7, "合計估算", 0.38, 6.9, 3.5, 0.4, font_size=14, bold=True, color=WHITE)
add_text(s7, "NT$ 249 – 401 萬元", 4.5, 6.9, 3.5, 0.4,
         font_size=16, bold=True, color=AMBER, align=PP_ALIGN.CENTER)

# Right side note box
bullet_box(s7, "💡 資金規劃建議", [
    "建議自備資金至少 200 萬元，其餘搭配青創貸款",
    "中小企業處青年創業貸款：最高 400 萬，優惠利率",
    "裝潢優先考慮中古設備節省成本",
    "冷藏設備為核心投資，不建議妥協品質",
    "保留 30-50 萬周轉金，避免初期現金流斷鏈",
    "平鎮區 50 坪店面月租約 NT$4-8 萬（依路段）",
], 8.3, 1.2, 4.7, 5.8)

# ═══════════════════════════════════════════════════════
# SLIDE 8 — 財務估算（損益試算）
# ═══════════════════════════════════════════════════════
s8 = prs.slides.add_slide(BLANK)
slide_header(s8, "05｜財務估算（二）：月度損益試算", "達到損益平衡所需條件分析")

# Left: Monthly P&L
add_rect(s8, 0.3, 1.2, 6.1, 0.42, fill=GREEN_MID)
add_text(s8, "📊 月固定成本估算", 0.45, 1.23, 5.8, 0.35,
         font_size=13, bold=True, color=WHITE)

cost_items = [
    ("租金（50坪平鎮路面）", "55,000"),
    ("人事（老闆+2員工）", "80,000"),
    ("水電費（含冷藏）", "18,000"),
    ("進貨成本（月營收60%）", "（變動）"),
    ("包裝耗材", "6,000"),
    ("行銷/維護費用", "5,000"),
    ("雜支/折舊", "8,000"),
    ("固定成本小計", "172,000"),
]
for i, (item, val) in enumerate(cost_items):
    ry = 1.65 + i * 0.55
    bg = CREAM if i == len(cost_items)-1 else (GRAY_LIGHT if i%2==0 else WHITE)
    bld = i == len(cost_items)-1
    vc = GREEN_DARK if bld else GRAY_MID
    add_rect(s8, 0.3, ry, 6.1, 0.53, fill=bg)
    add_text(s8, item, 0.4, ry+0.1, 4.0, 0.36, font_size=12, bold=bld, color=GRAY_DARK)
    add_text(s8, val, 4.5, ry+0.1, 1.8, 0.36, font_size=12, bold=bld,
             color=vc, align=PP_ALIGN.RIGHT)

# Right: BEP analysis
add_rect(s8, 6.65, 1.2, 6.3, 0.42, fill=GREEN_MID)
add_text(s8, "🎯 損益平衡分析", 6.8, 1.23, 6.0, 0.35,
         font_size=13, bold=True, color=WHITE)

add_rect(s8, 6.65, 1.65, 6.3, 5.45, fill=CREAM,
         line_color=GREEN_LIGHT, line_width=Pt(1))

bep_lines = [
    ("蔬果生鮮毛利率（財政部標準）", "約 15–25%"),
    ("熟食/加工品毛利率", "約 50–65%"),
    ("綜合平均毛利率（估）", "約 30–35%"),
    ("", ""),
    ("損益平衡公式", "固定成本 ÷ 毛利率"),
    ("損益平衡月營收", "NT$172,000 ÷ 32% ≈ 537,500"),
    ("", ""),
    ("每日目標營收", "537,500 ÷ 25天 ≈ NT$21,500"),
    ("假設客單價 NT$250", "需日來客約 86 人"),
    ("假設客單價 NT$350", "需日來客約 61 人"),
]
for i, (k, v) in enumerate(bep_lines):
    ry = 1.75 + i * 0.52
    if k == "":
        continue
    bld = "損益平衡月營收" in k or "損益平衡公式" in k
    vc = GREEN_DARK if bld else GRAY_DARK
    add_text(s8, k, 6.78, ry, 3.8, 0.45, font_size=11, bold=False, color=GRAY_MID)
    add_text(s8, v, 10.2, ry, 2.6, 0.45, font_size=12, bold=bld,
             color=vc, align=PP_ALIGN.RIGHT)

# Highlight BEP box
add_rect(s8, 6.85, 4.15, 5.9, 1.15, fill=GREEN_DARK)
add_text(s8, "🎯 月營收目標：NT$ 53 – 65 萬", 7.0, 4.2, 5.6, 0.5,
         font_size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s8, "約 50 坪生鮮店的合理業績門檻（含熟食複合）",
         7.0, 4.65, 5.6, 0.5, font_size=12, color=GREEN_LIGHT, align=PP_ALIGN.CENTER)

add_text(s8, "※ 毛利率依據財政部113年度同業利潤標準；實際數字需依進貨議價調整",
         0.3, 7.05, 12.5, 0.3, font_size=10, italic=True, color=GRAY_MID)

# ═══════════════════════════════════════════════════════
# SLIDE 9 — SWOT 分析
# ═══════════════════════════════════════════════════════
s9 = prs.slides.add_slide(BLANK)
slide_header(s9, "06｜SWOT 分析", "本址開設複合式蔬果店之策略環境評估")

# 4 quadrants
quads = [
    (GREEN_DARK,  "S 優勢 Strengths",   0.3,  1.15, [
        "1樓臨路，購物動線自然、可見度高",
        "50坪空間充裕，可完整分區陳列",
        "複合式業態（生鮮+熟食）差異化明顯",
        "住宅密集區，高頻回購客群穩定",
        "在地直供可降低進貨成本",
    ]),
    (AMBER,       "W 劣勢 Weaknesses",  6.85, 1.15, [
        "全聯、家樂福等大型通路競爭激烈",
        "新品牌缺乏知名度，需時間建立信任",
        "冷藏設備投資與電費成本高",
        "生鮮品耗損率高（損耗約 8-15%）",
        "初期客流不穩定，資金壓力大",
    ]),
    (GREEN_MID,   "O 機會 Opportunities", 0.3, 4.35, [
        "台鐵平鎮站預計2026年5月啟用，人流增加",
        "桃園捷運橘線規劃中，未來區域升值",
        "平鎮人口持續成長（近十年+8.4%）",
        "健康飲食風潮，有機蔬果年均成長 8-10%",
        "電商整合（LINE訂購）可擴大服務範圍",
    ]),
    (RED_WARN,    "T 威脅 Threats",     6.85, 4.35, [
        "全聯福利中心持續拓點、強化生鮮陳列",
        "通貨膨脹推高食材與租金成本",
        "傳統菜市場仍是在地消費習慣核心",
        "外送平台壓縮實體店客流",
        "蔬果產地氣候風險影響供應穩定性",
    ]),
]
for color, title, lx, ty, pts in quads:
    add_rect(s9, lx, ty, 6.3, 0.42, fill=color)
    add_text(s9, title, lx+0.12, ty+0.05, 6.0, 0.35,
             font_size=14, bold=True, color=WHITE)
    add_rect(s9, lx, ty+0.42, 6.3, 2.65, fill=WHITE,
             line_color=color, line_width=Pt(1.5))
    txb = s9.shapes.add_textbox(Inches(lx+0.15), Inches(ty+0.55),
                                Inches(6.0), Inches(2.4))
    txb.word_wrap = True
    tf = txb.text_frame; tf.word_wrap = True
    first = True
    for pt in pts:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_before = Pt(6)
        r = p.add_run(); r.text = f"◆ {pt}"
        r.font.size = Pt(12); r.font.color.rgb = GRAY_DARK

# ═══════════════════════════════════════════════════════
# SLIDE 10 — 風險評估
# ═══════════════════════════════════════════════════════
s10 = prs.slides.add_slide(BLANK)
slide_header(s10, "07｜風險評估", "主要風險因子與對應緩解策略")

add_rect(s10, 0.25, 1.2, 12.8, 0.42, fill=GREEN_DARK)
for hdr, lx, wd in [("風險類別", 0.3, 1.7), ("風險描述", 2.05, 3.5),
                     ("等級", 5.6, 0.9), ("緩解策略", 6.55, 6.4)]:
    add_text(s10, hdr, lx, 1.25, wd, 0.35, font_size=13, bold=True,
             color=WHITE, align=PP_ALIGN.CENTER)

risks = [
    ("競爭風險", "全聯、家樂福強力競爭，\n蠶食生鮮客群", "高",
     "差異化：熟食現做、在地農夫直供、有機專區；\n主打社區情感連結與個人化服務"),
    ("財務風險", "初期客流不穩定，\n現金流壓力大", "高",
     "保留50萬以上緩衝資金；\n前6個月設定損益評估里程碑"),
    ("耗損風險", "蔬果日耗損率8-15%，\n增加固定損失", "中",
     "精準採購（小量多次）、熟食轉換耗損品、\n導入庫存管理系統"),
    ("租金風險", "租金上漲影響固定成本", "中",
     "爭取3-5年租約鎖定租金；\n增加複合品類提高坪效"),
    ("供應鏈風險", "氣候、颱風影響\n蔬果供應與價格", "中",
     "建立多元供應商；季節預備乾貨\n暨加工品彌補缺貨期"),
    ("人力風險", "員工流動率高，\n熟食技術人員難覓", "低中",
     "提供市場薪資＋業績獎金；\n簡化熟食製程（半成品加工）"),
]
rc = [GRAY_LIGHT, WHITE, GRAY_LIGHT, WHITE, GRAY_LIGHT, WHITE]
lv_c = {"高": RED_WARN, "中": AMBER, "低中": GREEN_MID}
for i, (cat, desc, lv, mit) in enumerate(risks):
    ry = 1.65 + i * 0.88
    add_rect(s10, 0.25, ry, 12.8, 0.86, fill=rc[i])
    add_text(s10, cat, 0.32, ry+0.1, 1.65, 0.65, font_size=12, bold=True, color=GREEN_DARK)
    add_text(s10, desc, 2.05, ry+0.06, 3.45, 0.75, font_size=11, color=GRAY_MID)
    add_rect(s10, 5.62, ry+0.18, 0.85, 0.48, fill=lv_c[lv])
    add_text(s10, lv, 5.62, ry+0.2, 0.85, 0.42, font_size=13, bold=True,
             color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s10, mit, 6.58, ry+0.06, 6.3, 0.75, font_size=11, color=GRAY_DARK)

# ═══════════════════════════════════════════════════════
# SLIDE 11 — 總結建議與開店策略
# ═══════════════════════════════════════════════════════
s11 = prs.slides.add_slide(BLANK)
slide_header(s11, "08｜總結建議與開店策略", "評估結論與行動計畫")

# Verdict banner
add_rect(s11, 0.3, 1.2, 12.6, 1.05, fill=GREEN_DARK)
add_text(s11, "✅  整體評估：地點條件中等偏好，建議審慎評估後進行",
         0.6, 1.28, 12.0, 0.45, font_size=18, bold=True, color=WHITE)
add_text(s11, "平鎮區人口穩定成長、消費需求明確，本址具備基礎條件，關鍵在差異化策略與財務紀律",
         0.6, 1.7, 12.0, 0.4, font_size=13, color=GREEN_LIGHT)

# 3 strategy columns
strats = [
    ("🚀 短期 (0–6個月)\n開幕建立期", [
        "以「平德路在地好菜」為品牌定位",
        "開幕前1個月社群預熱（LINE社群/FB）",
        "提供開幕優惠（買千送百、蔬果試吃）",
        "建立社區會員制，儲值送蔬果禮盒",
        "每日現場直播蔬果開箱、農場溯源",
    ]),
    ("📈 中期 (7–18個月)\n穩定獲利期", [
        "擴充熟食便當區（提升毛利至35%以上）",
        "引入有機/在地農夫直供專區",
        "推動LINE訂購+自取外送服務",
        "申請農產品有機認證資格",
        "達月營收60萬、淨利10%為里程碑",
    ]),
    ("🏆 長期 (19個月以上)\n品牌深化期", [
        "配合台鐵平鎮站啟用擴大商圈影響",
        "考慮設置二店（鄰近社區）或加盟模式",
        "建立季節預購訂閱盒（蔬菜箱）",
        "深化社區關係（與里辦公室合作）",
        "評估取得健康食品/有機店認證提升形象",
    ]),
]
for ci, (title, pts) in enumerate(strats):
    lx = 0.3 + ci * 4.3
    add_rect(s11, lx, 2.4, 4.1, 0.52, fill=GREEN_MID)
    add_text(s11, title, lx+0.1, 2.42, 3.9, 0.48,
             font_size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_rect(s11, lx, 2.95, 4.1, 3.6, fill=CREAM,
             line_color=GREEN_LIGHT, line_width=Pt(1))
    txb = s11.shapes.add_textbox(Inches(lx+0.15), Inches(3.08),
                                 Inches(3.8), Inches(3.35))
    txb.word_wrap = True
    tf = txb.text_frame; tf.word_wrap = True
    first = True
    for pt in pts:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_before = Pt(7)
        r = p.add_run(); r.text = f"▶ {pt}"
        r.font.size = Pt(11.5); r.font.color.rgb = GRAY_DARK

# Bottom key metrics
add_rect(s11, 0.3, 6.65, 12.6, 0.7, fill=GREEN_DARK)
kms = [
    "啟動資金：約 250–400 萬",
    "損益平衡月營收：NT$53–65 萬",
    "建議日來客：60–90 人",
    "預估回本期：18–30 個月",
]
for i, km in enumerate(kms):
    add_text(s11, km, 0.5 + i*3.15, 6.68, 3.0, 0.6,
             font_size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════════════
# SLIDE 12 — 結語
# ═══════════════════════════════════════════════════════
s12 = prs.slides.add_slide(BLANK)
add_rect(s12, 0, 0, 13.33, 7.5, fill=GREEN_DARK)
add_rect(s12, 0, 5.8, 13.33, 1.7, fill=GREEN_MID)
add_rect(s12, 0, 7.0, 13.33, 0.5, fill=AMBER)

add_text(s12, "感謝閱覽", 1, 1.2, 11.33, 1.2,
         font_size=44, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s12, "桃園市平鎮區平德路 271 號 複合式蔬果店 選址評估報告",
         1, 2.4, 11.33, 0.7, font_size=18, color=GREEN_LIGHT, align=PP_ALIGN.CENTER)

add_rect(s12, 4.0, 3.25, 5.33, 0.05, fill=AMBER)

closing_pts = [
    "✅ 地點條件：中等偏好（住宅密集、交通便利）",
    "✅ 市場需求：生鮮蔬果日常需求穩定、複合業態具差異化優勢",
    "⚠  主要挑戰：全聯等連鎖超市競爭激烈，需明確差異化",
    "💡 核心建議：在地品牌＋熟食複合＋社區深耕為成功關鍵",
]
for i, pt in enumerate(closing_pts):
    add_text(s12, pt, 2.0, 3.6 + i*0.52, 9.33, 0.48,
             font_size=13, color=WHITE, align=PP_ALIGN.LEFT)

add_text(s12, "本報告資料截至 2026年5月｜數據來源：桃園市政府、財政部、業界公開資訊",
         1, 5.95, 11.33, 0.5, font_size=11, italic=True,
         color=RGBColor(0xC8, 0xE6, 0xC9), align=PP_ALIGN.CENTER)

out_path = "/home/user/namecard/平鎮平德路_複合式蔬果店_市場評估報告.pptx"
prs.save(out_path)
print(f"✅ PPT saved: {out_path}")
