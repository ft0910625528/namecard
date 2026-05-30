"""
影音合成：espeak-ng TTS + 投影片圖片 → MP4
"""
import os, subprocess, textwrap
from pathlib import Path
import static_ffmpeg
static_ffmpeg.add_paths()

BASE      = Path("/home/user/namecard")
SLIDE_DIR = BASE / "video_tmp" / "slides"
AUDIO_DIR = BASE / "video_tmp" / "audio"
SEG_DIR   = BASE / "video_tmp" / "segments"
AUDIO_DIR.mkdir(exist_ok=True)
SEG_DIR.mkdir(exist_ok=True)

# ── 旁白文案 ─────────────────────────────────────────────────────────
NARRATIONS = [
    # 01 封面
    "各位好，這份報告針對桃園市平鎮區平德路二七一號一樓，規劃複合市集升級方案的可行性評估。本方案將傳統蔬果店升級為一樓八個攤位特約出租制，加上二樓複合功能空間，包含快剪、精品、讀書室或老人會館。以下逐頁說明評估內容。",
    # 02 商業模式
    "首先說明商業模式的升級邏輯。原方案為單一自營蔬果店，每月需達五十三萬到六十五萬才能損益平衡，競爭壓力大。升級方案導入攤位出租制，由租金收入分擔固定成本，再加入二樓多元業態共同引流。這樣能實現四大核心價值：風險分散、人流共享、社區定錨，以及坪效提升。",
    # 03 一樓規劃
    "一樓五十坪的配置方式如下。全區規劃八個攤位，每攤三坪，合計二十四坪，業態涵蓋蔬菜、水果、豆腐蛋品、海鮮、熟食便當、滷味小菜、有機乾貨，以及一個彈性業態攤位。其餘二十六坪分配給冷藏倉儲、結帳服務台，以及走道通行空間。攤位合約建議六到十二個月，月租金八千到一萬二千元，含水電分攤。",
    # 04 租金試算
    "攤位出租的財務效益相當顯著。七個出租攤位，每月租金收入合計約七萬八千元。以押金制收取兩個月租金，初期即可入帳十五萬六千元。最關鍵的是，租金收入可抵銷每月固定成本的百分之四十五，使自營主攤的損益平衡門檻，從原本的五十三萬，大幅降低到只需三十一萬。這是升級方案最核心的財務優勢。",
    # 05 二樓業態
    "二樓共評估四種業態。第一，快剪髮廊，每月一到兩次消費頻率，導流效果最強，月租約兩萬元，裝潢成本低，強烈推薦。第二，精品飾品，客群與主婦族高度重疊，月租一萬二到兩萬。第三，讀書室，採訂閱制，三十席月費制，每月可收三萬到五萬，現金流穩定。第四，老人會館，長輩族群每日買菜需求強烈，且可申請桃園市長照社造補助。",
    # 06 最佳組合
    "綜合評估後，推薦三種組合方案。方案A，快剪加讀書室，月租合計五萬五千元，兩者互補性最強，導流加穩定客流，為最推薦組合。方案B，老人會館加快剪，月租約兩萬三千元，強化社區形象，長輩購買蔬果連動效益高。方案C，精品加讀書室加快剪，全客層覆蓋，適合空間六十坪以上的二樓。",
    # 07 財務模型
    "整合財務模型試算如下。收入面，一樓七攤租金七萬八千元、快剪兩萬元、讀書室三萬五千元，加上自營蔬果主攤毛利九萬六千元，月總可用收入約二十二萬九千元。支出面，整棟租金十二萬、人事八萬、水電兩萬二、管理與行銷一萬六千元，合計二十三萬八千元。自營主攤只需達到月營收三十一萬，即可整體損益平衡，比純自營方案降低百分之四十二的門檻。",
    # 08 SWOT
    "升級方案的策略評估：優勢方面，租金收入分散風險，多業態共同引流，社區據點黏著度高。劣勢方面，二樓裝潢增加八十到一百五十萬啟動成本，多攤主管理複雜度提升。機會方面，台鐵平鎮站預計二零二六年五月啟用，周邊人流將顯著增加，複合市集模式在台灣也有成功案例支撐。威脅方面，需注意攤主招租風險與租賃合約糾紛管理。",
    # 09 招商管理
    "招商策略與管理規範方面。目標攤主鎖定在地小農、食品微型創業者，透過桃園市農會、在地社群與傳單進行招募。面試優先選擇有機認證、產地直送、有故事性的攤主，並設計兩個月試攤期，雙方互相評估。管理規約涵蓋業態獨家性、統一開關店時間、環境衛生標準，以及共用POS系統。法務方面，需簽訂特約加盟協議書，攤主需自行辦理食品業者登錄。",
    # 10 三方案比較
    "三大方案的綜合比較一目了然。純自營方案得分六十五分，損益門檻最高，風險集中。攤位制方案得分七十八分，月被動收入增加七萬八千元。複合市集加二樓方案得分八十八分，損益門檻最低，收益來源最多元，為最推薦選擇。預估回本期二十四到三十六個月，略長於純自營，但風險分散程度與長期獲利能力明顯更優。",
    # 11 執行路線圖
    "執行路線圖分四個階段。籌備期，負六到負四個月，確認二樓空間、設計攤位平面、啟動招商。建設期，負三到負一個月，施工裝潢、完成攤主簽約、系統建置。開幕期，第一到三個月，盛大開幕、農夫到場活動、每日SOP執行。成長期，第四到十二個月，引入VIP會員、各業態效益確認、年底財務審查。核心KPI為出租率百分之八十五以上，月自營達三十萬，綜合月損益轉正。",
    # 12 總結建議
    "總結與決策建議。本次評估結論，複合市集升級方案可行性高，綜合評分八十八分，強烈建議採用。在行動前，需確認四件事：第一，二樓空間是否可取得；第二，預算是否可支應三百八十到六百萬的啟動資金；第三，業主是否有管理多租戶的時間與能力；第四，法律合規事項是否就緒。建議的第一步，委請設計師出攤位加樓層平面規劃圖，預算兩到三萬，作為後續決策的具體依據。",
    # 13 結語
    "感謝您的聆聽。本報告針對桃園市平鎮區平德路二七一號複合市集升級方案，進行了完整的可行性評估。攤位出租制可使損益門檻降低百分之四十二，搭配二樓快剪與讀書室，每月可增加被動收入十三萬三千元。若有任何疑問或需要進一步分析，歡迎隨時諮詢。祝您創業順利，生意興隆。",
]

print(f"✅ 旁白文案共 {len(NARRATIONS)} 頁")

# ── TTS 生成（使用 espeak-ng cmn 中文普通話）─────────────────────────
print("🎙️  生成旁白音訊（espeak-ng）...")
audio_files = []
for i, narration in enumerate(NARRATIONS):
    wav_path = AUDIO_DIR / f"slide_{i:02d}.wav"
    mp3_path = AUDIO_DIR / f"slide_{i:02d}.mp3"
    if not wav_path.exists():
        # Generate WAV via espeak-ng (keep as WAV — ffmpeg handles it fine)
        r = subprocess.run(
            ["espeak-ng", "-v", "cmn", "-s", "145", "-p", "55",
             "-w", str(wav_path), narration],
            capture_output=True, text=True
        )
        if r.returncode != 0 or not wav_path.exists():
            print(f"  ❌ 頁{i+1} TTS 失敗: {r.stderr}")
            audio_files.append(None); continue
    audio_files.append(wav_path)
    print(f"  ✔ 頁{i+1:02d} 音訊完成 ({audio_files[-1].suffix})")

print(f"✅ 音訊生成完成")

# ── 取得音訊時長 ─────────────────────────────────────────────────────
def get_dur(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True)
    return float(r.stdout.strip())

durations = [get_dur(a) for a in audio_files if a]
print(f"📊 音訊總時長：{sum(durations):.1f} 秒 ({sum(durations)/60:.1f} 分鐘)")

# ── 合成每頁影片片段 ──────────────────────────────────────────────────
slide_imgs  = sorted(SLIDE_DIR.glob("slide_*.png"))
n = min(len(slide_imgs), len(NARRATIONS), len(audio_files))
print(f"🎬 合成 {n} 個影片片段...")

segments = []
all_durations = []
for i in range(n):
    seg = SEG_DIR / f"seg_{i:02d}.mp4"
    dur = get_dur(audio_files[i]) + 0.8  # 0.8s pause
    all_durations.append(dur)
    if not seg.exists():
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-framerate", "1",
            "-i", str(slide_imgs[i]),
            "-i", str(audio_files[i]),
            "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            "-t", str(dur),
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
            str(seg)
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  ❌ 片段{i+1} 失敗: {r.stderr[-200:]}")
        else:
            print(f"  ✔ 片段 {i+1:02d}/{n}  ({dur:.1f}s)")
    else:
        print(f"  ✔ 片段 {i+1:02d}/{n}  (cached)")
    segments.append(seg)

# ── 串接所有片段 ─────────────────────────────────────────────────────
print("🔗 串接所有片段...")
concat = BASE / "video_tmp" / "concat.txt"
with open(concat, "w") as f:
    for seg in segments:
        f.write(f"file '{seg}'\n")

FINAL = BASE / "平鎮平德路_複合市集升級方案_影音報告.mp4"
r = subprocess.run([
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", str(concat),
    "-c:v", "libx264", "-crf", "22", "-preset", "medium",
    "-c:a", "aac", "-b:a", "128k",
    "-movflags", "+faststart",
    str(FINAL)
], capture_output=True, text=True)

if r.returncode != 0:
    print(f"❌ 串接失敗:\n{r.stderr[-500:]}")
else:
    mb = FINAL.stat().st_size / 1024 / 1024
    total_min = sum(all_durations) / 60
    print(f"\n{'='*50}")
    print(f"✅  影音報告生成完成！")
    print(f"   📁 檔案：{FINAL.name}")
    print(f"   📦 大小：{mb:.1f} MB")
    print(f"   ⏱  總時長：{total_min:.1f} 分鐘 ({sum(all_durations):.0f} 秒)")
    print(f"   🎞  解析度：1920×1080 (Full HD)")
    print(f"{'='*50}")
