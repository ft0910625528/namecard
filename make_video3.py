"""
最終影音報告：女聲模擬 + 繁體中文字幕 + 生動主播文案
"""
import os, subprocess, textwrap, json
from pathlib import Path
import static_ffmpeg
static_ffmpeg.add_paths()

BASE      = Path("/home/user/namecard")
SLIDE_DIR = BASE / "video_tmp" / "slides"
AUDIO_DIR = BASE / "video_tmp" / "audio_v2"
SEG_DIR   = BASE / "video_tmp" / "segments_v2"
SUB_DIR   = BASE / "video_tmp" / "subtitles"
AUDIO_DIR.mkdir(exist_ok=True)
SEG_DIR.mkdir(exist_ok=True)
SUB_DIR.mkdir(exist_ok=True)

# ── 生動主播風格旁白（更新版）────────────────────────────────────────
NARRATIONS = [
    # 01 封面
    "嗨，大家好！今天要為您帶來一份精彩的商業評估報告。"
    "地點是桃園市平鎮區平德路二七一號一樓，"
    "我們將一起探討——如何把一間傳統蔬果店，"
    "升級成充滿活力的複合市集！"
    "包含一樓八個攤位特約出租，加上二樓的快剪、讀書室或老人會館。"
    "讓我們開始吧！",

    # 02 商業模式
    "首先，我們來看看為什麼要升級？"
    "傳統單一自營蔬果店，每個月至少要賣到五十三萬才能打平，"
    "壓力真的不小！"
    "升級方案的核心邏輯是這樣的——"
    "透過攤位出租，讓租金幫你分擔固定成本；"
    "再引入二樓多元業態，讓各種客群自然匯聚。"
    "一句話總結：風險分散、坪效翻倍、社區深根！",

    # 03 一樓規劃
    "接下來看一樓五十坪的聰明配置。"
    "我們把它規劃成八個精緻攤位，每攤剛好三坪，"
    "業態涵蓋蔬菜、水果、豆腐蛋品、海鮮、熟食便當、"
    "滷味小菜、有機乾貨，還有一個彈性業態攤位。"
    "剩下的二十六坪，留給冷藏倉儲、結帳服務台和走道空間。"
    "攤位月租金八千到一萬二，合約六到十二個月，"
    "讓好的攤主安心紮根！",

    # 04 租金試算
    "來看最讓人興奮的數字！"
    "七個出租攤位，每個月穩穩進帳七萬八千元。"
    "一開始還可以收十五萬六千元的押金，"
    "直接改善初期現金流！"
    "最關鍵的是，租金收入可以抵銷將近一半的固定成本，"
    "讓您的損益平衡門檻，從五十三萬直接降到三十一萬！"
    "這就是攤位出租制最強大的財務魔力。",

    # 05 二樓業態
    "二樓要放什麼？我們評估了四個超有潛力的業態！"
    "第一，快剪髮廊——客人等剪髮的空檔，直接下樓買菜，導流效果無敵強！"
    "第二，精品飾品——主婦族群高度重疊，假日人流顯著提升。"
    "第三，讀書室——採月費訂閱制，三十個座位每月穩定進帳三萬到五萬，"
    "現金流超可預期！"
    "第四，老人會館——長輩每天都要買菜，而且還可以申請桃園市的長照補助！",

    # 06 最佳組合
    "好，那二樓到底要怎麼組合最划算？"
    "強力推薦方案A——快剪加讀書室，"
    "月租合計五萬五千元，導流加訂閱雙引擎，互補性超強！"
    "如果您更看重社區形象，選方案B，老人會館加快剪，"
    "長輩每天報到，蔬果業績自然跟著來。"
    "若是空間夠大，方案C三業態全上，"
    "學生、主婦、長輩一次通吃，客層最完整！",

    # 07 財務模型
    "整合財務模型來了，請看這個數字！"
    "收入面：一樓七攤租金七萬八、快剪兩萬、讀書室三萬五，"
    "加上自營主攤毛利九萬六，月總可用收入高達二十二萬九千元！"
    "支出面：整棟租金十二萬、人事八萬、水電兩萬二、管理行銷一萬六，"
    "合計二十三萬八千元。"
    "結論是，自營主攤只要做到三十一萬，整體就能損益平衡，"
    "比純自營省了整整四成二的壓力！",

    # 08 SWOT
    "用SWOT來全面檢視這個方案。"
    "優勢：租金收入分散風險、多業態引流、社區黏著度高。"
    "劣勢：二樓裝潢多花八十到一百五十萬，管理複雜度也會提升。"
    "機會來了——台鐵平鎮站預計二零二六年五月啟用，人流即將大增！"
    "複合市集在台灣也有很多成功案例可以參考。"
    "威脅方面，攤主招租和合約管理要做好，這是關鍵！",

    # 09 招商管理
    "成功的複合市集，攤主選對很重要！"
    "我們的目標攤主是——在地小農、食品微型創業者，"
    "那種有品牌意識、有故事可說的好攤主。"
    "招募管道包括桃園市農會、在地臉書社群、傳單發放。"
    "設計兩個月試攤期，大家互相了解再決定。"
    "管理上，業態獨家、衛生標準、共用POS一定要寫清楚，"
    "用特約合作協議書保護雙方權益！",

    # 10 三方案比較
    "三大方案大PK，讓數字說話！"
    "純自營方案，六十五分，損益門檻高、風險全自擔。"
    "攤位制方案，七十八分，每月多了七萬八千元的穩定收入。"
    "複合市集加二樓方案，八十八分，損益門檻最低、收益來源最多元，"
    "毫無疑問是最推薦的選擇！"
    "回本期雖然稍長，大約二十四到三十六個月，"
    "但長期獲利能力完全不同等級！",

    # 11 執行路線圖
    "行動計畫分四個清晰階段！"
    "籌備期，提前六到四個月，確認二樓空間、設計平面圖、啟動招商。"
    "建設期，提前三到一個月，裝潢施工、完成攤主簽約、系統建置。"
    "開幕期，第一到三個月，盛大開幕、農夫到場互動、即期品SOP每日執行。"
    "成長期，第四到十二個月，培育VIP會員、各業態效益確認、年底財務審查。"
    "核心目標：出租率百分之八十五以上，月自營三十萬，損益轉正！",

    # 12 總結
    "最後來到總結建議！"
    "結論非常明確——複合市集升級方案，綜合評分八十八分，強烈建議！"
    "不過在行動之前，有四件事一定要先確認好："
    "第一，二樓空間是否可取得？"
    "第二，三百八十到六百萬的啟動資金準備好了嗎？"
    "第三，業主有時間和能力管理多個租戶嗎？"
    "第四，法律合規和證照都就緒了嗎？"
    "建議第一步就是，花兩到三萬委請設計師出平面圖，具體的規劃是一切的開始！",

    # 13 結語
    "好的，以上就是今天的完整評估報告！"
    "攤位出租制讓損益門檻降低四成二，"
    "搭配二樓快剪與讀書室，每月被動收入可增加超過十三萬！"
    "平鎮區人口持續成長，台鐵站即將啟用，時機非常成熟。"
    "感謝您的聆聽，希望這份報告對您的創業決策有所幫助。"
    "祝您開業順利，財源廣進，生意興隆！",
]

print(f"✅ 旁白文案：{len(NARRATIONS)} 頁")

# ── TTS：espeak-ng 女聲模擬（高音調 + 適中語速）──────────────────────
print("🎙️  生成女聲旁白（espeak-ng 高音調）...")
audio_files = []
for i, narration in enumerate(NARRATIONS):
    wav = AUDIO_DIR / f"slide_{i:02d}.wav"
    if not wav.exists():
        r = subprocess.run([
            "espeak-ng", "-v", "cmn",
            "-s", "130",   # 語速（預設175，130較自然）
            "-p", "74",    # 音調（預設50，74模擬女聲）
            "-a", "175",   # 音量
            "-g", "6",     # 字詞間距（增加韻律感）
            "-w", str(wav), narration
        ], capture_output=True, text=True)
    audio_files.append(wav)
    print(f"  ✔ 頁{i+1:02d}")

print("✅ 音訊完成")

# ── 取得音訊時長 ─────────────────────────────────────────────────────
def dur(path):
    r = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path)
    ], capture_output=True, text=True)
    return float(r.stdout.strip())

durations = [dur(a) for a in audio_files]
total_sec = sum(durations)
print(f"📊 總時長：{total_sec:.1f}s ({total_sec/60:.1f} 分鐘)")

# ── 建立 ASS 字幕（繁體中文，主播風格）────────────────────────────────
def make_ass_subtitle(slide_idx, narration, audio_dur):
    """為每頁生成 ASS 字幕檔"""
    # 將旁白切成字幕行（每行15-20字）
    # 簡單策略：按標點切句，每句一行
    import re
    sentences = re.split(r'([，。！？、；])', narration)
    lines = []
    current = ""
    for part in sentences:
        current += part
        if part in "。！？" and len(current.strip()) > 0:
            lines.append(current.strip())
            current = ""
    if current.strip():
        lines.append(current.strip())
    # 過濾空行
    lines = [l for l in lines if l.strip()]
    if not lines:
        lines = [narration]

    # 每行分配時間
    n = len(lines)
    time_per_line = audio_dur / n if n > 0 else audio_dur

    def sec_to_ass(s):
        h  = int(s // 3600)
        m  = int((s % 3600) // 60)
        sc = s % 60
        return f"{h}:{m:02d}:{sc:05.2f}"

    ass_events = []
    for j, line in enumerate(lines):
        t_start = j * time_per_line
        t_end   = min((j + 1) * time_per_line, audio_dur)
        ass_events.append(
            f"Dialogue: 0,{sec_to_ass(t_start)},{sec_to_ass(t_end)},"
            f"Default,,0,0,0,,{line}"
        )

    return "\n".join(ass_events)

# ASS 樣式頭
ASS_HEADER = """\
[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,WenQuanYi Zen Hei,52,&H00FFFFFF,&H000000FF,&H00000000,&H99000000,-1,0,0,0,100,100,2,0,1,3,2,2,80,80,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

# ── 合成每頁影片（圖片+音訊+字幕）────────────────────────────────────
slide_imgs = sorted(SLIDE_DIR.glob("slide_*.png"))
n = min(len(slide_imgs), len(NARRATIONS), len(audio_files))
print(f"\n🎬 合成 {n} 頁影片片段（含字幕）...")

segments = []
all_durs = []
for i in range(n):
    seg   = SEG_DIR / f"seg_{i:02d}.mp4"
    img   = slide_imgs[i]
    audio = audio_files[i]
    d_sec = durations[i] + 1.0  # 1秒停頓
    all_durs.append(d_sec)

    # 建立字幕檔
    ass_path = SUB_DIR / f"slide_{i:02d}.ass"
    events   = make_ass_subtitle(i, NARRATIONS[i], durations[i])
    ass_path.write_text(ASS_HEADER + events, encoding="utf-8")

    if not seg.exists():
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-framerate", "1",
            "-i", str(img),
            "-i", str(audio),
            "-vf", (
                "scale=1920:1080:force_original_aspect_ratio=decrease,"
                "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,"
                f"ass={ass_path}"
            ),
            "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            "-t", str(d_sec),
            str(seg)
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  ❌ 頁{i+1} 失敗:\n{r.stderr[-300:]}")
        else:
            print(f"  ✔ 頁{i+1:02d}/{n}  ({d_sec:.1f}s)")
    else:
        print(f"  ✔ 頁{i+1:02d}/{n}  (cached {d_sec:.1f}s)")
    segments.append(seg)

# ── 串接最終影片 ─────────────────────────────────────────────────────
print("\n🔗 串接最終影片...")
concat = BASE / "video_tmp" / "concat_v2.txt"
with open(concat, "w") as f:
    for s in segments:
        f.write(f"file '{s}'\n")

FINAL = BASE / "平鎮平德路_複合市集_影音報告_字幕版.mp4"
r = subprocess.run([
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", str(concat),
    "-c:v", "libx264", "-crf", "21", "-preset", "medium",
    "-c:a", "aac", "-b:a", "128k",
    "-movflags", "+faststart",
    str(FINAL)
], capture_output=True, text=True)

if r.returncode != 0:
    print(f"❌ 串接失敗:\n{r.stderr[-500:]}")
else:
    mb  = FINAL.stat().st_size / 1024 / 1024
    tot = sum(all_durs)
    print(f"\n{'='*55}")
    print(f"✅  影音報告（字幕版）生成完成！")
    print(f"   📁 {FINAL.name}")
    print(f"   📦 大小：{mb:.1f} MB")
    print(f"   ⏱  時長：{tot/60:.1f} 分鐘（{tot:.0f} 秒）")
    print(f"   🎞  解析度：1920×1080  Full HD")
    print(f"   🔤 字幕：繁體中文 ASS 燒錄")
    print(f"   🎙  語音：女聲模擬（高音調 cmn）")
    print(f"{'='*55}")

# ── 同時輸出 SRT 字幕檔（備用）────────────────────────────────────────
print("\n📄 輸出合併 SRT 字幕檔...")
import re

def sec_to_srt(s):
    h  = int(s // 3600)
    m  = int((s % 3600) // 60)
    sc = s % 60
    ms = int((sc % 1) * 1000)
    return f"{h:02d}:{m:02d}:{int(sc):02d},{ms:03d}"

srt_lines = []
idx = 1
offset = 0.0
for i, (narration, d_sec) in enumerate(zip(NARRATIONS, durations)):
    sentences = re.split(r'([。！？])', narration)
    lines = []
    current = ""
    for part in sentences:
        current += part
        if part in "。！？" and current.strip():
            lines.append(current.strip()); current = ""
    if current.strip(): lines.append(current.strip())
    lines = [l for l in lines if l.strip()] or [narration]

    n_lines = len(lines)
    tpl = d_sec / n_lines
    for j, line in enumerate(lines):
        ts = offset + j * tpl
        te = offset + min((j+1)*tpl, d_sec)
        srt_lines += [str(idx), f"{sec_to_srt(ts)} --> {sec_to_srt(te)}", line, ""]
        idx += 1
    offset += d_sec + 1.0

SRT_PATH = BASE / "平鎮平德路_複合市集_影音報告.srt"
SRT_PATH.write_text("\n".join(srt_lines), encoding="utf-8")
print(f"✅ SRT 字幕檔：{SRT_PATH.name}  ({idx-1} 行)")
