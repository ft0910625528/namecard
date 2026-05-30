"""
最終影音報告生成器
流程：PPTX → 圖片 → 旁白TTS → 整合MP4
"""
import os, subprocess, tempfile, textwrap, time
from pathlib import Path
from gtts import gTTS
from PIL import Image
import static_ffmpeg
static_ffmpeg.add_paths()

BASE   = Path("/home/user/namecard")
OUTDIR = BASE / "video_tmp"
OUTDIR.mkdir(exist_ok=True)

# ── 1. 旁白文案（每頁對應） ─────────────────────────────────────────
NARRATIONS = [
    # 封面
    """
    各位好，這份報告針對桃園市平鎮區平德路二百七十一號一樓，
    規劃複合市集升級方案的可行性評估。
    本方案將傳統蔬果店升級為——
    一樓八個攤位特約出租制，加上二樓複合功能空間，
    包含快剪、精品、讀書室或老人會館。
    以下逐頁說明評估內容。
    """,
    # 商業模式升級概念
    """
    首先說明商業模式的升級邏輯。
    原方案為單一自營蔬果店，每月需達五十三到六十五萬才能損益平衡，
    競爭壓力大。
    升級方案導入攤位出租制，由租金收入分擔固定成本，
    再加入二樓多元業態共同引流。
    這樣能實現四大核心價值：
    風險分散、人流共享、社區定錨，以及坪效提升。
    """,
    # 一樓空間規劃
    """
    一樓五十坪的配置方式如下。
    全區規劃八個攤位，每攤三坪，合計二十四坪。
    業態涵蓋蔬菜、水果、豆腐蛋品、海鮮、熟食便當、滷味小菜、有機乾貨，
    以及一個彈性業態攤位。
    其餘二十六坪分配給冷藏倉儲、結帳服務台，以及走道通行空間。
    攤位合約建議六到十二個月，月租金八千到一萬二千元，含水電分攤。
    """,
    # 攤位租金財務試算
    """
    攤位出租的財務效益相當顯著。
    七個出租攤位，每月租金收入合計約七萬八千元。
    以押金制收取兩個月租金，初期即可入帳十五萬六千元。
    最關鍵的是：租金收入可抵銷每月固定成本的百分之四十五，
    使自營主攤的損益平衡門檻，從原本的五十三萬，
    大幅降低到只需三十一萬。
    這是升級方案最核心的財務優勢。
    """,
    # 二樓業態規劃
    """
    二樓共評估四種業態。
    第一，快剪髮廊：每月一到兩次消費頻率，導流效果最強，
    月租約兩萬元，裝潢成本低，強烈推薦。
    第二，精品飾品：客群與主婦族高度重疊，月租一萬二到兩萬。
    第三，讀書室：採訂閱制，三十席月費制，
    每月可收三萬到五萬，現金流穩定。
    第四，老人會館：長輩族群每日買菜需求強烈，
    且可申請桃園市長照社造補助。
    """,
    # 二樓最佳組合
    """
    綜合評估後，推薦三種組合方案。
    方案A：快剪加讀書室，月租合計五萬五千元，
    兩者互補性最強，導流加穩定客流，為最推薦組合。
    方案B：老人會館加快剪，月租約兩萬三千元，
    強化社區形象，長輩購買蔬果連動效益高。
    方案C：精品加讀書室加快剪，全客層覆蓋，
    適合空間六十坪以上的二樓。
    """,
    # 整合財務模型
    """
    整合財務模型試算如下。
    收入面：一樓七攤租金七萬八千元、快剪兩萬元、
    讀書室三萬五千元，加上自營蔬果主攤毛利九萬六千元，
    月總可用收入約二十二萬九千元。
    支出面：整棟租金十二萬、人事八萬、水電兩萬二、
    管理與行銷一萬六千元，合計二十三萬八千元。
    自營主攤只需達到月營收三十一萬，即可整體損益平衡，
    比純自營方案降低百分之四十二的門檻。
    """,
    # SWOT
    """
    升級方案的 SWOT 分析：
    優勢方面，租金收入分散風險，多業態共同引流，
    社區據點黏著度高。
    劣勢方面，二樓裝潢增加八十到一百五十萬啟動成本，
    多攤主管理複雜度提升。
    機會方面，台鐵平鎮站預計二零二六年五月啟用，
    周邊人流將顯著增加，複合市集模式在台灣也有成功案例支撐。
    威脅方面，需注意攤主招租風險與租賃合約糾紛管理。
    """,
    # 攤位招商管理
    """
    招商策略與管理規範方面。
    目標攤主鎖定在地小農、食品微型創業者，
    透過桃園市農會、在地社群與傳單進行招募。
    管理規約涵蓋業態獨家性、統一開關店時間、
    環境衛生標準、共用POS系統，以及攤主委員會機制。
    法務方面，需簽訂特約加盟協議書，
    攤主需自行辦理食品業者登錄，二樓業態依法規申請相應執照。
    """,
    # 三方案比較
    """
    三大方案的綜合比較一目了然。
    純自營方案得分六十五分，損益門檻最高，風險集中。
    攤位制方案得分七十八分，月被動收入增加七萬八千元。
    複合市集加二樓方案得分八十八分，
    損益門檻最低，收益來源最多元，為最推薦選擇。
    預估回本期二十四到三十六個月，略長於純自營，
    但風險分散程度與長期獲利能力明顯更優。
    """,
    # 執行路線圖
    """
    執行路線圖分四個階段。
    籌備期，負六到負四個月：確認二樓空間、設計攤位平面、啟動招商。
    建設期，負三到負一個月：施工裝潢、完成攤主簽約、系統建置。
    開幕期，第一到三個月：盛大開幕、農夫到場活動、每日SOP執行。
    成長期，第四到十二個月：引入VIP會員、各業態效益確認、年底財務審查。
    核心KPI為出租率百分之八十五以上，月自營達三十萬，
    綜合月損益轉正。
    """,
    # 總結建議
    """
    總結與決策建議。
    本次評估結論：複合市集升級方案可行性高，綜合評分八十八分，
    強烈建議採用。
    在行動前，需確認四件事：
    第一，二樓空間是否可取得；
    第二，預算是否可支應三百八十到六百萬的啟動資金；
    第三，業主是否有管理多租戶的時間與能力；
    第四，法律合規事項是否就緒。
    建議的第一步：委請設計師出攤位加樓層平面規劃圖，預算兩到三萬，
    作為後續決策的具體依據。
    """,
    # 結語
    """
    感謝您的聆聽。
    本報告針對桃園市平鎮區平德路二百七十一號複合市集升級方案，
    進行了完整的可行性評估。
    若有任何疑問或需要進一步的數據分析，歡迎隨時諮詢。
    祝您創業順利，生意興隆。
    """,
]

# Cleanup narrations
NARRATIONS = [textwrap.dedent(n).strip() for n in NARRATIONS]

print(f"✅ 旁白文案共 {len(NARRATIONS)} 頁")

# ── 2. 將最終PPTX轉換為圖片 ────────────────────────────────────────
PPTX_FILE = BASE / "平鎮平德路_複合市集升級方案評估報告.pptx"
IMG_DIR   = OUTDIR / "slides"
IMG_DIR.mkdir(exist_ok=True)

print("🔄 轉換 PPTX → PNG 圖片...")
result = subprocess.run([
    "libreoffice", "--headless", "--convert-to", "png",
    "--outdir", str(IMG_DIR),
    str(PPTX_FILE)
], capture_output=True, text=True, timeout=120)
print(result.stdout[-300:] if result.stdout else "")
if result.returncode != 0:
    print("STDERR:", result.stderr[-300:])

# Sorted slide images
slide_imgs = sorted(IMG_DIR.glob("*.png"))
print(f"✅ 取得 {len(slide_imgs)} 張投影片圖片")

# ── 3. 生成TTS旁白音訊 ───────────────────────────────────────────────
AUDIO_DIR = OUTDIR / "audio"
AUDIO_DIR.mkdir(exist_ok=True)

print("🎙️  生成旁白音訊（TTS）...")
audio_files = []
for i, narration in enumerate(NARRATIONS):
    audio_path = AUDIO_DIR / f"slide_{i:02d}.mp3"
    if not audio_path.exists():
        tts = gTTS(text=narration, lang="zh-TW", slow=False)
        tts.save(str(audio_path))
        time.sleep(0.3)  # avoid rate limit
    audio_files.append(audio_path)
    print(f"  ✔ 頁{i+1:02d} 音訊完成")

print(f"✅ 音訊生成完成：{len(audio_files)} 個")

# ── 4. 取得每個音訊的時長 ────────────────────────────────────────────
def get_duration(audio_path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)],
        capture_output=True, text=True
    )
    return float(r.stdout.strip())

durations = [get_duration(a) for a in audio_files]
print(f"✅ 音訊總時長：{sum(durations):.1f} 秒 ({sum(durations)/60:.1f} 分鐘)")

# ── 5. 為每頁生成影片片段 ────────────────────────────────────────────
SEGMENT_DIR = OUTDIR / "segments"
SEGMENT_DIR.mkdir(exist_ok=True)

n_slides = min(len(slide_imgs), len(NARRATIONS), len(audio_files))
print(f"🎬 合成 {n_slides} 個影片片段...")

segments = []
for i in range(n_slides):
    seg_path = SEGMENT_DIR / f"seg_{i:02d}.mp4"
    if not seg_path.exists():
        img   = slide_imgs[i]
        audio = audio_files[i]
        dur   = durations[i] + 0.5  # 0.5s pause after narration

        # Resize image to 1920×1080
        pil_img = Image.open(img)
        bg = Image.new("RGB", (1920, 1080), (0, 0, 0))
        ratio = min(1920/pil_img.width, 1080/pil_img.height)
        new_w  = int(pil_img.width  * ratio)
        new_h  = int(pil_img.height * ratio)
        resized = pil_img.resize((new_w, new_h), Image.LANCZOS)
        bg.paste(resized, ((1920-new_w)//2, (1080-new_h)//2))
        tmp_img = OUTDIR / f"tmp_slide_{i:02d}.png"
        bg.save(str(tmp_img))

        # ffmpeg: image + audio → video segment
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(tmp_img),
            "-i", str(audio),
            "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            "-t", str(dur),
            "-vf", "scale=1920:1080",
            str(seg_path)
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  ❌ 片段{i+1} 失敗: {r.stderr[-200:]}")
        else:
            print(f"  ✔ 片段 {i+1:02d}/{n_slides} 完成 ({dur:.1f}s)")

    segments.append(seg_path)

# ── 6. 串接所有片段 ──────────────────────────────────────────────────
print("🔗 串接所有片段為最終 MP4...")
concat_list = OUTDIR / "concat.txt"
with open(concat_list, "w") as f:
    for seg in segments:
        f.write(f"file '{seg}'\n")

FINAL_OUT = BASE / "平鎮平德路_複合市集升級方案_影音報告.mp4"
cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", str(concat_list),
    "-c:v", "libx264", "-crf", "23", "-preset", "fast",
    "-c:a", "aac", "-b:a", "128k",
    str(FINAL_OUT)
]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print(f"❌ 串接失敗: {r.stderr[-400:]}")
else:
    size_mb = FINAL_OUT.stat().st_size / 1024 / 1024
    print(f"✅ 影音報告生成完成！")
    print(f"   檔案：{FINAL_OUT.name}")
    print(f"   大小：{size_mb:.1f} MB")
    print(f"   總時長：{sum(durations)/60:.1f} 分鐘")
