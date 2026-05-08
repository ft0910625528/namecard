/* ═══════════════════════════════
   app.js — 主控制器
═══════════════════════════════ */
const App = (() => {

  // ── 狀態 ───────────────────────────────────────────
  let state = {
    cards: [],
    currentId: null,
    editMode: 'new',    // 'new' | 'edit'
    pendingImage: null, // base64
    qrStream: null,
    qrAnimId: null,
  };

  // ── DOM 快取 ────────────────────────────────────────
  const $ = id => document.getElementById(id);
  const views = {
    list:   $('view-list'),
    add:    $('view-add'),
    qr:     $('view-qr'),
    ocr:    $('view-ocr'),
    edit:   $('view-edit'),
    detail: $('view-detail'),
  };

  // ── View 切換 ───────────────────────────────────────
  function showView(name) {
    Object.entries(views).forEach(([k, el]) => {
      if (k === 'list') {
        el.classList.toggle('active', k === name);
      } else if (k === 'add') {
        el.classList.toggle('hidden', k !== name);
      } else {
        el.classList.toggle('hidden', k !== name);
      }
    });
  }

  function showSheet() {
    views.add.classList.remove('hidden');
    requestAnimationFrame(() => {
      views.add.querySelector('.sheet-backdrop').style.opacity = '1';
      views.add.querySelector('.sheet-content').style.transform = 'translateY(0)';
    });
  }

  function hideSheet() {
    views.add.querySelector('.sheet-backdrop').style.opacity = '0';
    views.add.querySelector('.sheet-content').style.transform = 'translateY(100%)';
    setTimeout(() => views.add.classList.add('hidden'), 350);
  }

  // ── Toast ───────────────────────────────────────────
  let toastTimer;
  function toast(msg, dur = 2500) {
    const el = $('toast');
    el.textContent = msg;
    el.classList.remove('hidden');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.add('hidden'), dur);
  }

  // ── Avatar ─────────────────────────────────────────
  function avatarLetter(card) {
    const n = card.name || card.company || '?';
    return n.charAt(0).toUpperCase();
  }

  function avatarColor(card) {
    const n = (card.name || card.company || '');
    let hash = 0;
    for (const c of n) hash = (hash * 31 + c.charCodeAt(0)) & 0xffffffff;
    return 'ac' + (Math.abs(hash) % 8);
  }

  // ── 名片列表 ────────────────────────────────────────
  async function loadList(filter = '') {
    state.cards = await DB.all();
    const list = $('card-list');
    const empty = $('empty-state');
    const query = filter.toLowerCase();

    const filtered = state.cards.filter(c => {
      if (!query) return true;
      return [c.name, c.company, c.phone, c.mobile, c.email, c.jobtitle]
        .some(v => v && v.toLowerCase().includes(query));
    });

    // 清除舊內容（保留 empty-state）
    [...list.children].forEach(el => { if (el !== empty) el.remove(); });

    if (!filtered.length) {
      empty.classList.remove('hidden');
      return;
    }
    empty.classList.add('hidden');

    filtered.forEach(card => {
      const div = document.createElement('div');
      div.className = 'card-item';
      div.innerHTML = `
        <div class="card-avatar ${avatarColor(card)}">${avatarLetter(card)}</div>
        <div class="card-info">
          <div class="card-name">${esc(card.name || '（無姓名）')}</div>
          <div class="card-sub">${esc([card.jobtitle, card.company].filter(Boolean).join('・') || card.phone || card.mobile || '')}</div>
        </div>
        <div class="card-chevron"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg></div>
      `;
      div.addEventListener('click', () => openDetail(card.id));
      list.appendChild(div);
    });
  }

  // ── 詳細頁 ──────────────────────────────────────────
  async function openDetail(id) {
    const card = await DB.get(id);
    if (!card) return;
    state.currentId = id;

    $('d-avatar').textContent = avatarLetter(card);
    $('d-avatar').className = `detail-avatar ${avatarColor(card)}`;
    $('d-name').textContent = card.name || '（無姓名）';
    $('d-subtitle').textContent = [card.jobtitle, card.company].filter(Boolean).join('・');

    if (card.photo) {
      $('d-photo').src = card.photo;
      $('d-photo-wrap').classList.remove('hidden');
    } else {
      $('d-photo-wrap').classList.add('hidden');
    }

    const fields = $('d-fields');
    fields.innerHTML = '';

    const addField = (icon, label, value, href) => {
      if (!value) return;
      const div = document.createElement('div');
      div.className = 'detail-field' + (href ? '' : ' non-tap');
      div.innerHTML = `
        <div class="field-icon" style="background:var(--gray1)">${icon}</div>
        <div class="field-content">
          <div class="field-label">${label}</div>
          <div class="field-value${href ? ' link' : ''}">${esc(value)}</div>
        </div>
        ${href ? '<div class="field-action"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg></div>' : ''}
      `;
      if (href) div.addEventListener('click', () => window.location.href = href);
      fields.appendChild(div);
    };

    addField('📞', '電話',   card.phone,   card.phone   ? `tel:${card.phone}`   : null);
    addField('📱', '手機',   card.mobile,  card.mobile  ? `tel:${card.mobile}`  : null);
    addField('📠', '傳真',   card.fax,     null);
    addField('✉️',  'Email',  card.email,   card.email   ? `mailto:${card.email}` : null);
    addField('🌐', '網站',   card.website, card.website);
    addField('📍', '地址',   card.address, card.address ? `maps:?q=${encodeURIComponent(card.address)}` : null);
    addField('📝', '備註',   card.notes,   null);

    showView('detail');
  }

  // ── 編輯頁 ──────────────────────────────────────────
  function openEdit(card = {}) {
    state.editMode = card.id ? 'edit' : 'new';
    state.currentId = card.id || null;
    $('edit-nav-title').textContent = card.id ? '編輯名片' : '新增名片';

    $('f-name').value     = card.name     || '';
    $('f-jobtitle').value = card.jobtitle || '';
    $('f-company').value  = card.company  || '';
    $('f-phone').value    = card.phone    || '';
    $('f-mobile').value   = card.mobile   || '';
    $('f-fax').value      = card.fax      || '';
    $('f-email').value    = card.email    || '';
    $('f-website').value  = card.website  || '';
    $('f-address').value  = card.address  || '';
    $('f-notes').value    = card.notes    || '';

    const photo = card.photo || state.pendingImage;
    if (photo) {
      $('edit-photo-img').src = photo;
      $('edit-photo-section').classList.remove('hidden');
    } else {
      $('edit-photo-section').classList.add('hidden');
    }

    if (card.raw) {
      $('f-raw').value = card.raw;
      $('raw-section').style.display = '';
    } else {
      $('raw-section').style.display = 'none';
    }

    showView('edit');
  }

  async function saveCard() {
    const card = {
      id:       state.currentId,
      name:     $('f-name').value.trim(),
      jobtitle: $('f-jobtitle').value.trim(),
      company:  $('f-company').value.trim(),
      phone:    $('f-phone').value.trim(),
      mobile:   $('f-mobile').value.trim(),
      fax:      $('f-fax').value.trim(),
      email:    $('f-email').value.trim(),
      website:  $('f-website').value.trim(),
      address:  $('f-address').value.trim(),
      notes:    $('f-notes').value.trim(),
      raw:      $('f-raw').value.trim(),
      photo:    state.pendingImage || null,
    };

    if (!card.name && !card.company && !card.phone && !card.mobile) {
      toast('請至少填寫姓名或電話');
      return;
    }

    // 如果是 edit 模式，保留原本的 photo
    if (card.id && !state.pendingImage) {
      const orig = await DB.get(card.id);
      if (orig) card.photo = orig.photo;
    }

    try {
      const isNew = !card.id;
      await DB.save(card);
      state.pendingImage = null;
      toast(isNew ? '名片已儲存 ✓' : '名片已更新 ✓');
      await loadList();
      showView('list');
    } catch (err) {
      console.error('saveCard error:', err);
      toast('儲存失敗，請重試');
    }
  }

  // ── 刪除 ────────────────────────────────────────────
  async function deleteCard(id) {
    if (!confirm('確定要刪除這張名片嗎？')) return;
    await DB.remove(id);
    toast('名片已刪除');
    await loadList();
    showView('list');
  }

  // ── 匯出 vCard ──────────────────────────────────────
  async function exportVCF(id) {
    const card = await DB.get(id);
    if (!card) return;
    const vcf  = Parser.toVCF(card);
    const blob = new Blob([vcf], { type: 'text/vcard;charset=utf-8' });
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href     = url;
    a.download = `${card.name || 'contact'}.vcf`;
    a.click();
    URL.revokeObjectURL(url);
    toast('已下載 .vcf，請點擊檔案加入聯絡人');
  }

  // ── 圖片轉 base64 ───────────────────────────────────
  function fileToBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload  = e => resolve(e.target.result);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  // ── 影像前處理（提升 OCR 準確度）───────────────────
  function preprocessForOCR(base64) {
    return new Promise(resolve => {
      const img = new Image();
      img.onload = () => {
        let w = img.width, h = img.height;

        // 1. 放大：確保最長邊至少 2000px（Tesseract 在高解析度下更準確）
        const MIN_PX = 2000, MAX_PX = 3000;
        const longest = Math.max(w, h);
        if (longest < MIN_PX) {
          const s = MIN_PX / longest;
          w = Math.round(w * s); h = Math.round(h * s);
        } else if (longest > MAX_PX) {
          const s = MAX_PX / longest;
          w = Math.round(w * s); h = Math.round(h * s);
        }

        // 2. 畫到 canvas，套用 CSS filter 提升對比與亮度
        const cv = document.createElement('canvas');
        cv.width = w; cv.height = h;
        const ctx = cv.getContext('2d');
        ctx.filter = 'grayscale(1) contrast(1.6) brightness(1.08)';
        ctx.drawImage(img, 0, 0, w, h);
        ctx.filter = 'none';

        // 3. 取出像素，做直方圖延伸（讓暗字更黑、背景更白）
        const imgData = ctx.getImageData(0, 0, w, h);
        const d = imgData.data;
        const samples = [];
        for (let i = 0; i < d.length; i += 16) samples.push(d[i]); // 每 4 px 取樣
        samples.sort((a, b) => a - b);
        const lo  = samples[Math.floor(samples.length * 0.05)];
        const hi  = samples[Math.floor(samples.length * 0.95)];
        const rng = hi - lo || 1;

        for (let i = 0; i < d.length; i += 4) {
          const v = Math.min(255, Math.max(0, Math.round((d[i] - lo) / rng * 255)));
          d[i] = d[i + 1] = d[i + 2] = v;
        }
        ctx.putImageData(imgData, 0, 0);

        // 4. 輸出 PNG（無損，OCR 效果比 JPEG 好）
        resolve(cv.toDataURL('image/png'));
      };
      img.src = base64;
    });
  }

  // 儲存用壓縮（顯示用，較小檔案）
  function compressImage(base64, maxPx = 1600) {
    return new Promise(resolve => {
      const img = new Image();
      img.onload = () => {
        let { width: w, height: h } = img;
        if (w > maxPx || h > maxPx) {
          if (w > h) { h = Math.round(h * maxPx / w); w = maxPx; }
          else       { w = Math.round(w * maxPx / h); h = maxPx; }
        }
        const cv = document.createElement('canvas');
        cv.width = w; cv.height = h;
        cv.getContext('2d').drawImage(img, 0, 0, w, h);
        resolve(cv.toDataURL('image/jpeg', 0.82));
      };
      img.src = base64;
    });
  }

  // ── OCR 辨識 ────────────────────────────────────────
  async function runOCR(base64) {
    showView('ocr');
    $('ocr-img').src = base64;
    $('ocr-status-text').textContent = '影像前處理中…';

    // 前處理：強化對比給 Tesseract 用，原圖保留做預覽和儲存
    const processed = await preprocessForOCR(base64);
    $('ocr-status-text').textContent = '正在辨識文字，請稍候…';

    try {
      const worker = await Tesseract.createWorker(['chi_tra', 'chi_sim', 'eng'], 1, {
        logger: m => {
          if (m.status === 'recognizing text') {
            $('ocr-status-text').textContent = `辨識中 ${Math.round(m.progress * 100)}%…`;
          }
        }
      });

      // PSM 6：單一均勻文字區塊（最適合名片版面）
      await worker.setParameters({
        tessedit_pageseg_mode: '6',
        preserve_interword_spaces: '1',
      });

      const { data } = await worker.recognize(processed);
      await worker.terminate();

      const text = data.text.trim();
      if (!text) {
        toast('無法辨識文字，請手動輸入');
        openEdit({ photo: base64 });
        return;
      }

      const card = Parser.parseOCR(text);
      card.photo = base64;
      state.pendingImage = base64;
      openEdit(card);
    } catch (err) {
      console.error(err);
      toast('辨識失敗，請手動輸入');
      state.pendingImage = base64;
      openEdit({ photo: base64 });
    }
  }

  // ── QR Code 掃描 ────────────────────────────────────
  async function startQR() {
    showView('qr');
    const video  = $('qr-video');
    const canvas = $('qr-canvas');
    const ctx    = canvas.getContext('2d');

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } }
      });
      state.qrStream = stream;
      video.srcObject = stream;
      await video.play();

      const scan = () => {
        if (!state.qrStream) return;
        if (video.readyState === video.HAVE_ENOUGH_DATA) {
          canvas.width  = video.videoWidth;
          canvas.height = video.videoHeight;
          ctx.drawImage(video, 0, 0);
          const img  = ctx.getImageData(0, 0, canvas.width, canvas.height);
          const code = jsQR(img.data, img.width, img.height, { inversionAttempts: 'dontInvert' });
          if (code) {
            stopQR();
            handleQRData(code.data);
            return;
          }
        }
        state.qrAnimId = requestAnimationFrame(scan);
      };
      state.qrAnimId = requestAnimationFrame(scan);
    } catch {
      toast('無法開啟相機，請確認相機權限');
      showView('list');
    }
  }

  function stopQR() {
    if (state.qrAnimId) { cancelAnimationFrame(state.qrAnimId); state.qrAnimId = null; }
    if (state.qrStream) {
      state.qrStream.getTracks().forEach(t => t.stop());
      state.qrStream = null;
    }
  }

  function handleQRData(text) {
    let card;
    if (Parser.isVCard(text)) {
      card = Parser.parseVCard(text);
    } else if (/^(http|https):\/\//i.test(text)) {
      card = { website: text, name: '', raw: text };
    } else if (RE_EMAIL.test(text)) {
      card = { email: text, raw: text };
    } else if (/^[0-9+\-\s()]{7,}$/.test(text)) {
      card = { phone: text, raw: text };
    } else {
      card = Parser.parseOCR(text);
    }
    state.pendingImage = null;
    openEdit(card);
  }

  const RE_EMAIL = /^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$/;

  // ── HTML 轉義 ───────────────────────────────────────
  function esc(s) {
    return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  // ── 事件綁定 ────────────────────────────────────────
  function bindEvents() {
    // 新增按鈕
    $('btn-add').addEventListener('click', showSheet);
    $('btn-add-cancel').addEventListener('click', hideSheet);
    $('sheet-backdrop').addEventListener('click', hideSheet);

    // 拍照
    $('btn-take-photo').addEventListener('click', () => {
      hideSheet();
      setTimeout(() => $('camera-input').click(), 350);
    });

    $('camera-input').addEventListener('change', async e => {
      const file = e.target.files[0];
      e.target.value = '';
      if (!file) return;
      const b64 = await fileToBase64(file);
      // 原圖壓縮後儲存（保留顯示用），前處理版本給 OCR 用
      const compressed = await compressImage(b64);
      state.pendingImage = compressed;
      await runOCR(compressed);
    });

    // 相簿
    $('btn-pick-photo').addEventListener('click', () => {
      hideSheet();
      setTimeout(() => $('album-input').click(), 350);
    });

    $('album-input').addEventListener('change', async e => {
      const file = e.target.files[0];
      e.target.value = '';
      if (!file) return;
      const b64 = await fileToBase64(file);
      const compressed = await compressImage(b64);
      state.pendingImage = compressed;
      await runOCR(compressed);
    });

    // QR Code
    $('btn-scan-qr').addEventListener('click', () => {
      hideSheet();
      setTimeout(startQR, 350);
    });

    $('btn-qr-cancel').addEventListener('click', () => {
      stopQR();
      showView('list');
    });

    // 手動輸入
    $('btn-manual').addEventListener('click', () => {
      hideSheet();
      state.pendingImage = null;
      setTimeout(() => openEdit({}), 350);
    });

    // OCR 取消
    $('btn-ocr-cancel').addEventListener('click', () => {
      state.pendingImage = null;
      showView('list');
    });

    // 編輯儲存 / 取消
    $('btn-edit-save').addEventListener('click', saveCard);
    $('btn-edit-cancel').addEventListener('click', () => {
      state.pendingImage = null;
      if (state.editMode === 'edit') openDetail(state.currentId);
      else showView('list');
    });

    // 詳細頁
    $('btn-detail-back').addEventListener('click', () => showView('list'));
    $('btn-detail-edit').addEventListener('click', async () => {
      const card = await DB.get(state.currentId);
      state.pendingImage = null;
      openEdit(card);
    });
    $('btn-save-contact').addEventListener('click', () => exportVCF(state.currentId));
    $('btn-delete-card').addEventListener('click', () => deleteCard(state.currentId));

    // 搜尋
    $('search-input').addEventListener('input', e => loadList(e.target.value));
  }

  // ── 初始化 ──────────────────────────────────────────
  async function init() {
    bindEvents();
    await loadList();
    showView('list');
  }

  return { init };
})();

document.addEventListener('DOMContentLoaded', () => App.init());
