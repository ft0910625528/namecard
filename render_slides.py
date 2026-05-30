"""
直接用 Pillow 渲染投影片為 PNG，不依賴 LibreOffice
"""
from PIL import Image, ImageDraw, ImageFont
import os, textwrap

W, H   = 1920, 1080
OUT    = "/home/user/namecard/video_tmp/slides"
os.makedirs(OUT, exist_ok=True)

# ── Fonts ─────────────────────────────────────────
FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

def F(size): return ImageFont.truetype(FONT_PATH, size)

# ── Colors ────────────────────────────────────────
C = {
    "GD":  (0x1B, 0x5E, 0x20),  # green dark
    "GM":  (0x2E, 0x7D, 0x32),  # green mid
    "GL":  (0x66, 0xBB, 0x6A),  # green light
    "AM":  (0xF5, 0x7F, 0x17),  # amber
    "AL":  (0xFF, 0xE0, 0x82),  # amber light
    "W":   (0xFF, 0xFF, 0xFF),
    "GrD": (0x21, 0x21, 0x21),  # gray dark
    "GrM": (0x42, 0x42, 0x42),  # gray mid
    "GrL": (0xF5, 0xF5, 0xF5),  # gray light
    "CR":  (0xF9, 0xFB, 0xE7),  # cream
    "RD":  (0xC6, 0x28, 0x28),  # red
    "BL":  (0x15, 0x65, 0xC0),  # blue
    "BD":  (0x0D, 0x47, 0xA1),  # blue dark
    "TL":  (0x00, 0x69, 0x64),  # teal
    "PU":  (0x6A, 0x1B, 0x9A),  # purple
}

def new_slide(bg=C["GrL"]):
    img = Image.new("RGB", (W, H), bg)
    return img, ImageDraw.Draw(img)

def box(d, x, y, w, h, fill=None, outline=None, lw=2):
    if fill:   d.rectangle([x, y, x+w, y+h], fill=fill)
    if outline: d.rectangle([x, y, x+w, y+h], outline=outline, width=lw)

def txt(d, text, x, y, fs=20, color=C["GrD"], anchor="la", wrap=None, line_spacing=1.35, italic=False):
    font = F(fs)
    # Split multiline text manually (anchor not supported for multiline)
    raw_lines = text.split("\n")
    all_lines = []
    for para in raw_lines:
        if wrap and para.strip():
            all_lines += textwrap.wrap(para, width=wrap)
        else:
            all_lines.append(para)
    if len(all_lines) == 1 and "\n" not in text:
        # single line — use anchor
        d.text((x, y), all_lines[0], font=font, fill=color, anchor=anchor)
    else:
        # multiline — anchor not supported, offset manually for "mt"
        total_h = len(all_lines) * int(fs * line_spacing)
        start_y = y - total_h // 2 if anchor == "mt" else y
        for i, line in enumerate(all_lines):
            d.text((x, start_y + i * int(fs * line_spacing)), line, font=font, fill=color)

def header(img, d, title, sub=""):
    box(d, 0, 0, W, 110, fill=C["GD"])
    box(d, 0, H-25, W, 25, fill=C["GM"])
    txt(d, title, 45, 15, fs=42, color=C["W"])
    if sub:
        txt(d, sub, 45, 70, fs=22, color=C["GL"])

def sec_hdr(d, label, x, y, w, h, hc=C["GM"], bg=C["CR"]):
    box(d, x, y, w, 42, fill=hc)
    txt(d, label, x+12, y+6, fs=20, color=C["W"])
    box(d, x, y+42, w, h-42, fill=bg, outline=C["GL"], lw=2)

def bullet_list(d, items, x, y, fs=18, color=C["GrM"], spacing=1.5, icon="▶"):
    for i, item in enumerate(items):
        lines = textwrap.wrap(item, 55)
        for j, line in enumerate(lines):
            prefix = f"{icon} " if j == 0 else "   "
            d.text((x, y + (i * 2.5 + j) * int(fs * spacing / 2)),
                   prefix + line, font=F(fs), fill=color)

# ─────────────────────────────────────────────────────
# SLIDE 01 — 封面
# ─────────────────────────────────────────────────────
def slide01():
    img, d = new_slide(C["GD"])
    box(d, 0, 550, W, 310, fill=C["GM"])
    box(d, 0, 790, W, 290, fill=C["AM"])
    txt(d, "複合市集升級方案", W//2, 80, fs=72, color=C["W"], anchor="mt")
    txt(d, "攤位出租制 ＋ 二樓複合空間 可行性評估報告", W//2, 185, fs=34, color=C["GL"], anchor="mt")
    box(d, 420, 285, 1080, 6, fill=C["AM"])
    items = [("🥦 一樓8攤", "特約出租加盟"), ("✂ 快剪髮廊", "高頻導客引流"),
             ("📚 讀書室", "訂閱穩定收益"), ("🏠 老人會館", "社區深根定錨")]
    for i, (a, b) in enumerate(items):
        lx = 50 + i * 470
        box(d, lx, 310, 440, 195, fill=C["GM"])
        txt(d, a, lx+220, 345, fs=28, color=C["W"], anchor="mt")
        txt(d, b, lx+220, 395, fs=22, color=C["AL"], anchor="mt")
    txt(d, "桃園市平鎮區平德路 271 號｜2026年5月", W//2, 530, fs=22, color=(200,230,201), anchor="mt")
    txt(d, "CONFIDENTIAL  ·  僅供內部決策使用", W//2, H-55, fs=18, color=C["W"], anchor="mt")
    return img

# SLIDE 02 — 商業模式升級概念
def slide02():
    img, d = new_slide((245, 245, 245))
    header(img, d, "商業模式升級概念", "從「單店自營」升級為「複合市集+多功能樓層」")
    # Left: old model
    box(d, 30, 130, 860, 50, fill=C["GrM"])
    txt(d, "❌ 原方案：單一自營蔬果店", 50, 140, fs=24, color=C["W"])
    old_items = ["自營一家蔬果+熟食店", "全部風險自行承擔",
                 "月需達53-65萬才損益平衡", "靠自身客流，競爭壓力大"]
    for i, it in enumerate(old_items):
        box(d, 30, 185+i*70, 860, 66, fill=C["GrL"] if i%2==0 else C["W"])
        txt(d, f"● {it}", 55, 205+i*70, fs=22, color=C["GrD"])
    # Arrow
    txt(d, "⟹", 935, 330, fs=60, color=C["AM"], anchor="la")
    # Right: new model
    box(d, 1040, 130, 850, 50, fill=C["GD"])
    txt(d, "✅ 升級方案：複合市集+複合樓層", 1060, 140, fs=24, color=C["W"])
    new_items = ["一樓8攤位出租，租金分擔風險", "二樓快剪/讀書室/老人會館多元收益",
                 "多業態共同引流，提升來客頻率", "損益平衡門檻大幅降低42%"]
    for i, it in enumerate(new_items):
        box(d, 1040, 185+i*70, 850, 66, fill=C["CR"] if i%2==0 else C["W"], outline=C["GL"], lw=1)
        txt(d, f"✔ {it}", 1065, 205+i*70, fs=22, color=C["GD"])
    # Bottom 4 value cards
    box(d, 30, 480, W-60, 50, fill=C["GM"])
    txt(d, "升級方案四大核心價值", 50, 490, fs=22, color=C["W"])
    props = [("💰 風險分散", "租金收入每月約7.8萬\n降低損益壓力"),
             ("🚶 人流共享", "多業態吸引不同族群\n學生/長輩/上班族"),
             ("🏘️ 社區定錨", "讀書室+老人會館形成\n社區日常必訪據點"),
             ("📈 坪效提升", "雙層空間運用\n整體收益遠超單層")]
    for i, (t, d2) in enumerate(props):
        lx = 30 + i*475
        box(d, lx, 540, 455, 175, fill=C["W"], outline=C["GL"], lw=2)
        txt(d, t, lx+20, 560, fs=24, color=C["GD"])
        txt(d, d2, lx+20, 600, fs=19, color=C["GrM"], wrap=22)
    return img

# SLIDE 03 — 一樓空間規劃
def slide03():
    img, d = new_slide((245, 245, 245))
    header(img, d, "一樓空間規劃｜50坪攤位配置", "3坪×8攤 特約出租加盟制")
    # Stalls grid
    stalls = [
        ("① 蔬菜類", C["GM"]), ("② 水果類",  C["GM"]),
        ("③ 豆腐蛋品", C["GM"]), ("④ 海鮮生鮮", C["BL"]),
        ("⑤ 熟食便當", C["AM"]), ("⑥ 滷味/小菜", C["AM"]),
        ("⑦ 有機/乾貨", C["TL"]), ("⑧ 自由業態",  C["PU"]),
    ]
    for i, (label, color) in enumerate(stalls):
        col, row = i%4, i//4
        lx, ty = 30 + col*230, 140 + row*190
        box(d, lx, ty, 220, 175, fill=color)
        txt(d, label, lx+110, ty+55, fs=22, color=C["W"], anchor="mt")
        txt(d, "3坪", lx+110, ty+100, fs=28, color=C["AL"], anchor="mt")
    # Support areas
    box(d, 30, 530, 200, 110, fill=C["GrL"], outline=C["GrM"], lw=2)
    txt(d, "冷藏倉儲\n4坪", 130, 565, fs=20, color=C["GrD"], anchor="mt")
    box(d, 245, 530, 220, 110, fill=C["GrL"], outline=C["GrM"], lw=2)
    txt(d, "結帳/服務台\n3坪", 355, 565, fs=20, color=C["GrD"], anchor="mt")
    box(d, 480, 530, 450, 110, fill=C["GrL"], outline=C["GrM"], lw=2)
    txt(d, "走道/出入口（約19坪）", 705, 580, fs=20, color=C["GrD"], anchor="mt")
    # Right panel: specs
    box(d, 970, 130, 930, 50, fill=C["GM"])
    txt(d, "📋 攤位規格與合約條件", 990, 140, fs=24, color=C["W"])
    specs = [("攤位坪數", "每攤 3 坪（約 9.9 m²）"),
             ("攤位數量", "共 8 攤（1攤自留主攤）"),
             ("合約期",   "6–12 個月，可續約"),
             ("月租金",   "NT$8,000–12,000（含水電）"),
             ("押金",     "2 個月租金"),
             ("開關時間", "07:00–20:00 統一"),
             ("業態",     "不重複，互補為原則"),
             ("管理",     "共用POS+攤主委員會")]
    for i, (k, v) in enumerate(specs):
        box(d, 970, 183+i*57, 930, 54, fill=C["CR"] if i%2==0 else C["W"])
        txt(d, k, 990, 197+i*57, fs=20, color=C["GD"])
        txt(d, v, 1230, 197+i*57, fs=20, color=C["GrD"])
    # Bottom bar
    box(d, 30, 660, W-60, 55, fill=C["GD"])
    txt(d, "出租攤位:24坪  ●  冷藏倉儲:4坪  ●  結帳:3坪  ●  走道通行:19坪  ●  合計:50坪",
        W//2, 675, fs=20, color=C["W"], anchor="mt")
    return img

# SLIDE 04 — 租金收益試算
def slide04():
    img, d = new_slide((245, 245, 245))
    header(img, d, "攤位出租｜租金收益財務試算", "穩定租金收入大幅降低損益風險")
    # Table header
    cols = [(40,165),(200,215),(420,195),(620,185),(810,185),(1000,600),(1605,295)]
    hdrs = ["攤","業態","月租金","押金","年租金","說明","備註"]
    box(d, 30, 135, W-60, 48, fill=C["GD"])
    for (x, w), h in zip(cols, hdrs):
        txt(d, h, x+w//2, 148, fs=20, color=C["W"], anchor="mt")
    rows = [
        ("①","蔬菜","10,000","20,000","120,000","主力客流攤","★★★★★"),
        ("②","水果","10,000","20,000","120,000","主力客流攤","★★★★★"),
        ("③","豆腐蛋","8,000","16,000","96,000","輔助商品","★★★☆☆"),
        ("④","海鮮肉","12,000","24,000","144,000","高毛利業態","★★★★☆"),
        ("⑤","熟食便當","12,000","24,000","144,000","高需求業態","★★★★★"),
        ("⑥","滷味小菜","8,000","16,000","96,000","熟食配套","★★★☆☆"),
        ("⑦","有機乾貨","10,000","20,000","120,000","差異化特色","★★★★☆"),
        ("⑧","自由業態","8,000","16,000","96,000","彈性招募","★★★☆☆"),
    ]
    for ri, row in enumerate(rows):
        bg = C["CR"] if ri%2==0 else C["W"]
        box(d, 30, 186+ri*65, W-60, 62, fill=bg)
        for (x, w), val in zip(cols, row):
            color = C["GD"] if val.startswith("1") or val.startswith("8") or val.startswith("9") else C["GrD"]
            if "," in val: color = C["GD"]
            txt(d, val, x+w//2, 205+ri*65, fs=20, color=color, anchor="mt")
    # Total
    box(d, 30, 706, W-60, 58, fill=C["GD"])
    txt(d, "合計（7攤出租）", 55, 720, fs=22, color=C["W"])
    txt(d, "NT$ 78,000 / 月", W//2-100, 720, fs=24, color=C["AM"])
    txt(d, "年收 NT$936,000", W-350, 720, fs=24, color=C["AM"])
    # KPI bottom row
    kpis = [("月租金收入\n7攤合計","NT$7.8萬",C["GD"]),
            ("可抵銷固定\n成本比例","45%",C["BL"]),
            ("自營損益\n門檻降至","NT$31萬",C["AM"]),
            ("押金首收\n一次入帳","NT$15.6萬",C["TL"])]
    for i, (lbl, val, hc) in enumerate(kpis):
        lx = 30+i*475
        box(d, lx, 775, 455, 90, fill=hc)
        txt(d, lbl, lx+20, 785, fs=18, color=C["GL"])
        txt(d, val, lx+250, 790, fs=28, color=C["AM"], anchor="la")
    return img

# SLIDE 05 — 二樓業態規劃
def slide05():
    img, d = new_slide((245,245,245))
    header(img, d, "二樓複合空間｜四大業態評估", "快剪 ／ 精品 ／ 讀書室 ／ 老人會館")
    options = [
        ("✂ 快剪髮廊", C["BD"], [
            "坪數：10-15坪", "月租：NT$18,000–25,000",
            "客層：全齡，每月1-2次", "導流：★★★★★ 最強",
            "等待剪髮時順便買菜", "加盟品牌易尋，裝潢低"]),
        ("👜 精品/飾品", C["PU"], [
            "坪數：10-20坪", "月租：NT$12,000–20,000",
            "客層：25-45歲主婦", "導流：★★★ 中等",
            "客群高度重疊蔬果店", "假日人流明顯增加"]),
        ("📚 讀書室", C["TL"], [
            "坪數：20-30坪（30席）", "月租：NT$30,000–50,000",
            "訂閱月費NT$800-1,500", "導流：★★★ 固定客",
            "現金流穩定可預期", "可搭配蔬果汁服務"]),
        ("🏠 老人會館", C["GD"], [
            "坪數：30-40坪", "月租：NT$5,000+補助",
            "客層：60歲+長輩", "導流：★★★★ 每日買菜",
            "可申請桃園市長照補助", "強化社區形象口碑"]),
    ]
    for ci, (title, hc, pts) in enumerate(options):
        lx = 30 + ci*475
        box(d, lx, 135, 455, 52, fill=hc)
        txt(d, title, lx+227, 148, fs=24, color=C["W"], anchor="mt")
        box(d, lx, 187, 455, 780, fill=C["CR"], outline=hc, lw=2)
        for ri, pt in enumerate(pts):
            icon = "▶" if ri < 4 else "◆"
            col  = C["GD"] if ri < 2 else (C["AM"] if ri==3 else C["GrD"])
            txt(d, f"{icon} {pt}", lx+20, 205+ri*118, fs=20, color=col)
        # Rec star
        rec = ["⭐⭐⭐⭐⭐ 最強推薦","⭐⭐⭐⭐ 強推薦","⭐⭐⭐⭐ 強推薦","⭐⭐⭐⭐ 強推薦"][ci]
        box(d, lx, 895, 455, 70, fill=hc)
        txt(d, rec, lx+227, 915, fs=20, color=C["W"], anchor="mt")
    return img

# SLIDE 06 — 二樓最佳組合
def slide06():
    img, d = new_slide((245,245,245))
    header(img, d, "二樓最佳組合推薦", "依空間大小選擇最適業態組合")
    combos = [
        ("方案 A  ★最推薦", "快剪 ＋ 讀書室", C["GD"],
         [("快剪", "15坪", "NT$20,000"), ("讀書室", "25坪", "NT$35,000"), ("走道廁所", "10坪", "公共設施")],
         "月租合計 NT$55,000 │ 導流+穩定訂閱，雙業態互補最強"),
        ("方案 B  社區導向", "老人會館 ＋ 快剪", C["TL"],
         [("老人會館", "30坪", "NT$8,000+補助"), ("快剪", "10坪", "NT$15,000"), ("走道廁所", "10坪", "公共設施")],
         "月租合計 NT$23,000 │ 社區形象最強，長輩每日購菜連動"),
        ("方案 C  全客層", "精品+讀書室+快剪", C["PU"],
         [("精品/飾品", "15坪", "NT$15,000"), ("讀書室", "20坪", "NT$28,000"), ("快剪", "10坪", "NT$18,000")],
         "月租合計 NT$61,000 │ 學生/主婦/長輩三族群全覆蓋"),
    ]
    for ci, (name, subtitle, hc, breakdown, verdict) in enumerate(combos):
        ty = 135 + ci*295
        box(d, 30, ty, 280, 275, fill=hc)
        txt(d, name, 170, ty+60, fs=22, color=C["W"], anchor="mt")
        txt(d, subtitle, 170, ty+110, fs=20, color=C["AL"], anchor="mt")
        txt(d, "月租估算:", 170, ty+170, fs=18, color=C["GL"], anchor="mt")
        total_rent = [55000, 23000, 61000][ci]
        txt(d, f"NT${total_rent:,}", 170, ty+200, fs=26, color=C["AM"], anchor="mt")
        box(d, 320, ty, 1570, 275, fill=C["CR"] if ci%2==0 else C["W"], outline=hc, lw=2)
        # breakdown table
        box(d, 325, ty+3, 1560, 36, fill=hc)
        for hi2, (h2, x2, w2) in enumerate([("業態",330,360),("坪數",695,200),("月租金",900,280),("功能",1185,680)]):
            txt(d, h2, x2, ty+12, fs=18, color=C["W"])
        for ri2, (bt, bsz, brent) in enumerate(breakdown):
            ry2 = ty + 42 + ri2*55
            bgr = C["W"] if ri2%2==0 else C["GrL"]
            box(d, 325, ry2, 1560, 52, fill=bgr)
            txt(d, bt,   340, ry2+14, fs=19, color=C["GD"])
            txt(d, bsz,  705, ry2+14, fs=19, color=C["GrD"])
            txt(d, brent,910, ry2+14, fs=19, color=C["AM"] if "NT$" in brent else C["GrD"])
        # verdict
        box(d, 320, ty+212, 1570, 58, fill=hc)
        txt(d, f"▶ {verdict}", 340, ty+228, fs=19, color=C["W"])
    return img

# SLIDE 07 — 整合財務模型
def slide07():
    img, d = new_slide((245,245,245))
    header(img, d, "整合財務模型｜升級方案月損益", "一樓攤位租金＋二樓租金＋自營蔬果主攤")
    box(d, 30, 130, W-60, 52, fill=C["GD"])
    txt(d, "假設：7攤出租(月租NT$78,000) ＋ 二樓方案A快剪+讀書室(月租NT$55,000) ＋ 自營主攤", 50, 145, fs=20, color=C["W"])
    # Income
    box(d, 30, 193, 870, 46, fill=C["GM"])
    txt(d, "📈 月收入來源", 50, 205, fs=22, color=C["W"])
    income_rows = [("一樓攤位租金（7攤）","NT$78,000","穩定固定收入"),
                   ("二樓快剪租金","NT$20,000","穩定固定收入"),
                   ("二樓讀書室（訂閱制）","NT$35,000","30席×NT$1,200"),
                   ("自營蔬果毛利（32%）","NT$96,000","月營業額30萬估算")]
    for ri, (item, val, note) in enumerate(income_rows):
        bg = C["CR"] if ri%2==0 else C["W"]
        box(d, 30, 242+ri*75, 870, 72, fill=bg)
        txt(d, item, 50, 262+ri*75, fs=20, color=C["GrD"])
        txt(d, val,  600, 262+ri*75, fs=22, color=C["GD"])
        txt(d, note, 50,  288+ri*75, fs=16, color=C["GrM"])
    box(d, 30, 544, 870, 58, fill=C["GD"])
    txt(d, "月總可用收入（租金+毛利）", 50, 558, fs=22, color=C["W"])
    txt(d, "NT$229,000", 620, 558, fs=26, color=C["AM"])
    # Expenses
    box(d, 940, 193, 950, 46, fill=C["RD"])
    txt(d, "📉 月固定支出", 960, 205, fs=22, color=C["W"])
    exp_rows = [("整棟租金（一樓+二樓）","NT$120,000","2層合租估算"),
                ("人事費（老闆+2員工）","NT$80,000","薪資+勞健保"),
                ("水電（含冷藏/公共）","NT$22,000","夏季估算"),
                ("管理+行銷雜支","NT$16,000","清潔/廣告")]
    for ri, (item, val, note) in enumerate(exp_rows):
        bg = C["GrL"] if ri%2==0 else C["W"]
        box(d, 940, 242+ri*75, 950, 72, fill=bg)
        txt(d, item, 960, 262+ri*75, fs=20, color=C["GrD"])
        txt(d, val, 1490, 262+ri*75, fs=22, color=C["RD"])
        txt(d, note, 960, 288+ri*75, fs=16, color=C["GrM"])
    box(d, 940, 544, 950, 58, fill=C["RD"])
    txt(d, "月固定支出合計", 960, 558, fs=22, color=C["W"])
    txt(d, "NT$238,000", 1500, 558, fs=26, color=C["W"])
    # Bottom result
    box(d, 30, 620, W-60, 340, fill=C["GD"])
    txt(d, "升級方案月損益評估", 50, 638, fs=28, color=C["GL"])
    results = [("自營需達月營收","NT$31萬","（原53-65萬，降低42%）",C["AM"]),
               ("租金補貼每月","NT$13.3萬","快剪+讀書室+攤位",C["GL"]),
               ("損益平衡條件","可達成","月自營30萬即回正",C["GL"]),
               ("預估回本期","24-36月","含二樓裝潢投資",C["AL"])]
    for i, (lbl, val, note, vc) in enumerate(results):
        lx = 50 + i*475
        txt(d, lbl, lx, 685, fs=19, color=C["GL"])
        txt(d, val,  lx, 720, fs=34, color=vc)
        txt(d, note, lx, 775, fs=17, color=(200,230,201))
    return img

# SLIDE 08 — SWOT
def slide08():
    img, d = new_slide((245,245,245))
    header(img, d, "升級方案 SWOT 分析", "攤位出租制 ＋ 二樓複合空間 策略評估")
    quads = [
        (C["GD"], "S 優勢 Strengths",    30,  130, [
            "租金收入降低損益門檻，風險分散",
            "多業態共同引流，相互加乘客流",
            "讀書室/老人會館建立社區日常據點",
            "快剪高頻消費確保每日穩定人流",
            "攤位制豐富商品種類，引入優質攤主"]),
        (C["AM"], "W 劣勢 Weaknesses",   975, 130, [
            "二樓裝潢成本增加80-150萬",
            "攤位招租需時，初期可能有空攤",
            "多攤主管理複雜度提升",
            "需建立租賃合約法律機制",
            "整棟租金增加（二樓+5-7萬/月）"]),
        (C["GM"], "O 機會 Opportunities", 30,  595, [
            "台鐵平鎮站2026年5月啟用，人流大增",
            "複合市集為台灣近年成功商業顯學",
            "老人會館可申請桃園市長照補助",
            "讀書室在備考/工作族需求持續成長",
            "攤位可吸引在地新創小農微型業者"]),
        (C["RD"], "T 威脅 Threats",      975, 595, [
            "攤主租賃糾紛與欠租風險需管控",
            "空攤期損失租金收入，招租壓力",
            "二樓業態若定位不佳成閒置負擔",
            "整棟租金若調漲，成本壓力倍增",
            "多業態管理需更多業主精力投入"]),
    ]
    for color, title, lx, ty, pts in quads:
        box(d, lx, ty, 910, 50, fill=color)
        txt(d, title, lx+15, ty+10, fs=26, color=C["W"])
        box(d, lx, ty+50, 910, 390, fill=C["W"], outline=color, lw=2)
        for i, pt in enumerate(pts):
            txt(d, f"◆ {pt}", lx+18, ty+75+i*63, fs=21, color=C["GrD"])
    return img

# SLIDE 09 — 招商管理
def slide09():
    img, d = new_slide((245,245,245))
    header(img, d, "攤位招商策略與管理規範", "特約出租加盟制度設計")
    sec_hdr(d, "📣 招商策略（攤位招募）", 30, 130, 910, 430, hc=C["GD"])
    recruit = ["目標攤主：在地小農、食品微型創業者",
               "招募管道：農會/FB社團/傳單/社群",
               "面試篩選：衛生習慣、服務態度、差異性",
               "優先：有機認證、產地直送、有故事性",
               "試攤期：前2個月7折租金，雙向評估",
               "目標：開幕前完成7攤招租率≥80%"]
    for i, it in enumerate(recruit):
        txt(d, f"▶ {it}", 50, 200+i*58, fs=21, color=C["GrM"])
    sec_hdr(d, "📋 管理規約重點", 960, 130, 930, 430, hc=C["AM"])
    mgmt = ["業態獨家性：同類限1攤不重複",
            "統一時間：每日07:00–20:00",
            "環境衛生：日清攤位，違規警告制",
            "共用POS：統一收銀，費用透明",
            "商品品質：蔬果基準由主辦統一訂",
            "攤主委員會：重大問題共同決議"]
    for i, it in enumerate(mgmt):
        txt(d, f"▶ {it}", 980, 200+i*58, fs=21, color=C["GrM"])
    # Legal section
    box(d, 30, 575, W-60, 50, fill=C["GM"])
    txt(d, "⚖  法律合規重點", 50, 588, fs=22, color=C["W"])
    legal = ["需簽訂「場地租賃暨特約加盟協議書」（建議委請律師審閱）",
             "攤主需自行辦理商業登記及食品業者登錄證",
             "食品類需確認食安衛生規範；二樓讀書室需取得公共場所使用執照",
             "老人會館依長照法規申請；建議投保公共意外責任險"]
    for i, it in enumerate(legal):
        bg = C["CR"] if i%2==0 else C["W"]
        box(d, 30, 628+i*60, W-60, 57, fill=bg)
        txt(d, f"⚠  {it}", 50, 643+i*60, fs=19, color=C["GrD"])
    return img

# SLIDE 10 — 三方案比較
def slide10():
    img, d = new_slide((245,245,245))
    header(img, d, "三大方案綜合比較", "純自營 vs 攤位出租 vs 複合市集（含二樓）")
    # Table
    col_xs = [30, 330, 750, 1180, 1620]
    col_ws = [295, 415, 425, 435, 280]
    hdrs   = ["評估項目", "方案A：純自營", "方案B：攤位制", "方案C：複合市集+二樓", "推薦"]
    box(d, 30, 130, W-60, 50, fill=C["GD"])
    for x, w, h in zip(col_xs, col_ws, hdrs):
        txt(d, h, x+w//2, 143, fs=21, color=C["W"], anchor="mt")
    rows = [
        ("啟動資金",       "250–400萬",  "250–400萬",  "380–600萬",     "A=B"),
        ("月固定成本",     "NT$17.2萬",  "NT$17.2萬",  "NT$23.8萬",     "A=B"),
        ("月租金收益",     "無",         "+NT$7.8萬",  "+NT$13.3萬",    "C>B>A"),
        ("損益平衡月營收", "NT$53–65萬", "NT$31萬",    "NT$25萬",       "C>B>A"),
        ("社區黏著度",     "★★☆☆☆",     "★★★☆☆",     "★★★★★",        "C"),
        ("人流吸引力",     "★★☆☆☆",     "★★★☆☆",     "★★★★★",        "C"),
        ("管理複雜度",     "★☆☆☆☆",     "★★★☆☆",     "★★★★☆",        "A"),
        ("風險分散",       "低",         "中",         "高",            "C"),
        ("預估回本期",     "18–30月",    "15–24月",    "24–36月",       "B"),
        ("整體推薦評分",   "65 分",      "78 分",      "88 分 ★",       "C"),
    ]
    bg_cycle = [C["CR"], C["W"]]
    for ri, row in enumerate(rows):
        is_last = ri == len(rows)-1
        bg = C["GD"] if is_last else bg_cycle[ri%2]
        box(d, 30, 183+ri*62, W-60, 60, fill=bg)
        vc0 = C["W"] if is_last else C["GrD"]
        for ci, (val, x, w) in enumerate(zip(row, col_xs, col_ws)):
            if ci == 0: vc = C["W"] if is_last else C["GD"]
            elif ci == 3: vc = C["AM"] if is_last else C["GD"]
            elif ci == 4: vc = C["AM"] if is_last else C["TL"]
            else: vc = C["W"] if is_last else C["GrD"]
            fs = 24 if is_last else 20
            txt(d, val, x+w//2, 205+ri*62, fs=fs, color=vc, anchor="mt")
    txt(d, "※ 方案C需確認二樓空間可取得；若無二樓則選方案B，仍優於純自營",
        50, H-40, fs=18, color=C["GrM"])
    return img

# SLIDE 11 — 執行路線圖
def slide11():
    img, d = new_slide((245,245,245))
    header(img, d, "升級方案執行路線圖", "從規劃到開幕的關鍵里程碑")
    phases = [
        ("-6→-4月\n籌備期", C["GD"], [
            "確認二樓空間可否取得", "委請設計師出攤位平面圖",
            "制訂特約合作協議書", "開始攤主招募作業",
            "申請食品業者相關證照", "確認二樓業態組合"]),
        ("-3→-1月\n建設期", C["AM"], [
            "一樓裝潢施工（冷藏/隔間）", "二樓裝潢（依業態）",
            "完成7攤招租簽約", "POS共用系統建置",
            "LINE官方帳號開通", "申請老人會館補助"]),
        ("第1-3月\n開幕期", C["GM"], [
            "盛大開幕（里長/農夫/媒體）", "認識攤主系列活動",
            "即期品SOP每日執行", "追蹤各攤動銷率",
            "LINE群組累積300好友", "第3月財務健診"]),
        ("第4-12月\n成長期", C["BL"], [
            "引入首批VIP金葉會員", "讀書室訂閱達30席80%",
            "老人會館每週3次活動", "快剪導流效益確認",
            "年底各業態貢獻度分析", "評估是否調整業態"]),
    ]
    for ci, (phase, hc, items) in enumerate(phases):
        lx = 30 + ci*472
        box(d, lx, 135, 455, 80, fill=hc)
        txt(d, phase, lx+227, 155, fs=24, color=C["W"], anchor="mt")
        box(d, lx, 215, 455, 790, fill=C["CR"], outline=hc, lw=2)
        for i, it in enumerate(items):
            txt(d, f"▶ {it}", lx+18, 235+i*108, fs=20, color=C["GrD"])
    box(d, 30, 1020, W-60, 45, fill=C["GM"])
    txt(d, "核心KPI：出租率≥85% ／ 月自營達30萬 ／ 綜合月損益轉正 ／ VIP月增10人",
        W//2, 1030, fs=19, color=C["W"], anchor="mt")
    return img

# SLIDE 12 — 總結建議
def slide12():
    img, d = new_slide((245,245,245))
    header(img, d, "總結與決策建議", "升級方案可行性結論與行動計畫")
    box(d, 30, 130, W-60, 105, fill=C["GD"])
    txt(d, "✅ 結論：複合市集升級方案可行性高（88/100），強烈建議採用", 50, 148, fs=28, color=C["W"])
    txt(d, "    損益門檻降低42%，風險分散，長期獲利能力顯著優於純自營方案", 50, 195, fs=22, color=C["GL"])
    sec_hdr(d, "💡 行動前必確認四件事", 30, 250, 880, 400, hc=C["AM"])
    prereqs = ["空間：二樓是否可取得（自有or另租）",
               "資金：預算能否支應380-600萬啟動成本",
               "能力：業主是否有管理多租戶的時間與技能",
               "法務：協議書/食品證照/使用執照是否就緒"]
    for i, r in enumerate(prereqs):
        txt(d, f"⚠ {r}", 50, 322+i*73, fs=22, color=C["GrD"])
    sec_hdr(d, "🎯 三步驟立即行動", 930, 250, 960, 400, hc=C["GM"])
    steps = ["STEP 1：與房東確認二樓使用可行性",
             "STEP 2：委請設計師出平面規劃圖（預算2-3萬）",
             "STEP 3：試算資金缺口，申請青創貸款",
             "若有二樓 → 方案C（88分）；無二樓 → 方案B（78分）"]
    for i, s in enumerate(steps):
        txt(d, f"▶ {s}", 950, 322+i*73, fs=21, color=C["GrD"])
    # Final KPIs
    box(d, 30, 665, W-60, 50, fill=C["GM"])
    txt(d, "升級方案關鍵財務指標", 50, 678, fs=22, color=C["W"])
    kpis = [("攤位月租收入","NT$7.8萬","7攤出租穩定"),
            ("二樓月租收入","NT$5.5萬","快剪+讀書室"),
            ("損益門檻降低","－42%","只需31萬自營"),
            ("整體推薦評分","88/100","vs 純自營65分")]
    for i, (lbl, val, note) in enumerate(kpis):
        lx = 30+i*475
        box(d, lx, 724, 455, 150, fill=C["CR"], outline=C["GL"], lw=2)
        box(d, lx, 724, 455, 7, fill=C["GM"])
        txt(d, lbl,  lx+227, 742, fs=20, color=C["GrM"], anchor="mt")
        txt(d, val,  lx+227, 782, fs=32, color=C["GD"], anchor="mt")
        txt(d, note, lx+227, 840, fs=18, color=C["GrM"], anchor="mt")
    return img

# SLIDE 13 — 結語
def slide13():
    img, d = new_slide(C["GD"])
    box(d, 0, 560, W, 280, fill=C["GM"])
    box(d, 0, 780, W, 300, fill=C["AM"])
    txt(d, "感謝閱覽", W//2, 80, fs=80, color=C["W"], anchor="mt")
    txt(d, "複合市集升級方案 評估報告", W//2, 200, fs=34, color=C["GL"], anchor="mt")
    box(d, 430, 280, 1060, 7, fill=C["AM"])
    summaries = [
        "✅ 攤位出租制：7攤月租NT$7.8萬，損益門檻降低42%",
        "✅ 推薦二樓組合：快剪+讀書室，月租NT$5.5萬，導流最強",
        "✅ 複合方案整體評分 88/100，顯著優於純自營65分",
        "💡 立即行動：確認二樓可行性 → 委請設計師出規劃圖"
    ]
    for i, s in enumerate(summaries):
        txt(d, s, W//2, 310+i*65, fs=24, color=C["W"], anchor="mt")
    txt(d, "本報告資料截至2026年5月 │ 數據來源：桃園市政府、財政部、業界公開資訊",
        W//2, 590, fs=20, italic=True, color=(200,230,201), anchor="mt")
    txt(d, "CONFIDENTIAL  ·  僅供內部決策使用", W//2, H-50, fs=18, color=C["W"], anchor="mt")
    return img

# ── Render all slides ──────────────────────────────
slide_funcs = [slide01, slide02, slide03, slide04, slide05, slide06, slide07,
               slide08, slide09, slide10, slide11, slide12, slide13]

for i, func in enumerate(slide_funcs):
    img = func()
    path = f"{OUT}/slide_{i:02d}.png"
    img.save(path, "PNG")
    print(f"  ✔ Slide {i+1:02d} → {path}")

print(f"\n✅ 全部 {len(slide_funcs)} 張投影片渲染完成")
