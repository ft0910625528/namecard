/* ═══════════════════════════════
   parser.js — OCR 文字 → 名片欄位
═══════════════════════════════ */
const Parser = (() => {

  // ── Regex 規則 ──────────────────────────────────────
  const RE = {
    email:   /[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/,
    url:     /(?:https?:\/\/|www\.)[^\s，,、。\n]+/i,
    phone:   /(?:(?:\+?886|0)[-\s]?)?(?:\d[\d\s\-().]{6,14}\d)/,
    mobile:  /09\d{2}[-\s]?\d{3}[-\s]?\d{3}/,
    fax:     /(?:傳真|fax|f\.?)[:\s：]*([\d\s\-().+]+)/i,
    tel:     /(?:電話|tel|t\.?|phone)[:\s：]*([\d\s\-().+]+)/i,
    zipTW:   /\d{3,6}/,
    addrTW:  /[台臺][灣北中南東高基新苗竹嘉彰投南屏宜花東澎金連]|[縣市區鄉鎮村里]|[路街道巷弄號樓]|[0-9０-９]+[號樓]/,
    name:    /^[一-鿿]{2,4}$|^[A-Z][a-zA-Z]+([\s][A-Z][a-zA-Z]+)+$/,
    title:   /總裁|董事長?|執行長|總經理|副總|協理|經理|主任|主管|工程師|設計師|顧問|業務|行銷|專員|助理|祕書|秘書|技術長|財務長|人資|CEO|COO|CFO|CTO|CMO|VP|Director|Manager|Engineer|Designer|Consultant|Analyst|Associate|Assistant|Specialist|Developer|Coordinator/i,
    company: /公司|企業|集團|機構|組織|事務所|工廠|股份|有限|Ltd|LLC|Inc|Corp|Co\.|&\s*Co/i,
  };

  // ── vCard 解析 ─────────────────────────────────────
  function parseVCard(text) {
    const card = {};
    const get = (key) => {
      const m = text.match(new RegExp(`${key}[^:]*:(.+)`, 'im'));
      return m ? m[1].trim() : '';
    };

    card.name    = get('FN') || get('N').replace(/;/g, ' ').trim();
    card.company = get('ORG');
    card.jobtitle= get('TITLE');
    card.email   = get('EMAIL');
    card.website = get('URL');

    const phones = [...text.matchAll(/TEL[^:]*:(.+)/gim)].map(m => m[1].trim());
    card.mobile  = phones.find(p => p.startsWith('09') || p.includes('09')) || '';
    card.phone   = phones.find(p => p !== card.mobile) || phones[0] || '';

    const adr = get('ADR').replace(/;/g, ' ').trim();
    card.address = adr;
    card.raw = text;
    return card;
  }

  // ── OCR 純文字解析 ──────────────────────────────────
  function parseOCR(rawText) {
    const card = { raw: rawText };
    const lines = rawText.split(/\n+/).map(l => l.trim()).filter(l => l.length > 0);
    const used = new Set();

    // Email
    for (let i = 0; i < lines.length; i++) {
      const m = lines[i].match(RE.email);
      if (m && !card.email) { card.email = m[0]; used.add(i); }
    }

    // Website
    for (let i = 0; i < lines.length; i++) {
      const m = lines[i].match(RE.url);
      if (m && !card.website) {
        let url = m[0];
        if (!url.startsWith('http')) url = 'https://' + url;
        card.website = url;
        used.add(i);
      }
    }

    // Mobile (手機 09xx)
    for (let i = 0; i < lines.length; i++) {
      const m = lines[i].match(RE.mobile);
      if (m && !card.mobile) { card.mobile = m[0].replace(/[\s]/g, ''); used.add(i); }
    }

    // 傳真
    for (let i = 0; i < lines.length; i++) {
      const m = lines[i].match(RE.fax);
      if (m && !card.fax) { card.fax = m[1].trim(); used.add(i); }
    }

    // 電話 (帶 tel: 標籤)
    for (let i = 0; i < lines.length; i++) {
      const m = lines[i].match(RE.tel);
      if (m && !card.phone) { card.phone = m[1].trim(); used.add(i); }
    }

    // 電話（數字判斷）
    for (let i = 0; i < lines.length; i++) {
      if (used.has(i)) continue;
      const m = lines[i].match(/^[\d\s\-().+]{7,20}$/);
      if (m) {
        const num = lines[i].replace(/[\s]/g, '');
        if (num.startsWith('09') && !card.mobile) { card.mobile = num; used.add(i); }
        else if (!card.phone) { card.phone = num; used.add(i); }
      }
    }

    // 地址（含中文地址關鍵字）
    const addrLines = [];
    for (let i = 0; i < lines.length; i++) {
      if (used.has(i)) continue;
      if (RE.addrTW.test(lines[i])) { addrLines.push(lines[i]); used.add(i); }
    }
    if (addrLines.length) card.address = addrLines.join(' ');

    // 公司
    for (let i = 0; i < lines.length; i++) {
      if (used.has(i)) continue;
      if (RE.company.test(lines[i]) && !card.company) { card.company = lines[i]; used.add(i); }
    }

    // 職稱
    for (let i = 0; i < lines.length; i++) {
      if (used.has(i)) continue;
      if (RE.title.test(lines[i]) && !card.jobtitle) { card.jobtitle = lines[i]; used.add(i); }
    }

    // 姓名（剩餘短行，優先純中文 2-4 字 或 英文 Full Name）
    const candidates = lines.filter((l, i) => !used.has(i) && l.length >= 2 && l.length <= 30);
    for (const c of candidates) {
      if (RE.name.test(c) && !card.name) { card.name = c; break; }
    }
    // 如果還是沒有姓名，取第一個未使用的短行
    if (!card.name && candidates.length) {
      card.name = candidates[0];
    }

    return card;
  }

  // ── vCard 匯出 ──────────────────────────────────────
  function toVCF(card) {
    const esc = s => (s || '').replace(/[,;\\]/g, c => '\\' + c).replace(/\n/g, '\\n');
    let vcf = 'BEGIN:VCARD\r\nVERSION:3.0\r\n';
    if (card.name)     vcf += `FN:${esc(card.name)}\r\nN:${esc(card.name)};;;;\r\n`;
    if (card.company)  vcf += `ORG:${esc(card.company)}\r\n`;
    if (card.jobtitle) vcf += `TITLE:${esc(card.jobtitle)}\r\n`;
    if (card.phone)    vcf += `TEL;TYPE=WORK,VOICE:${esc(card.phone)}\r\n`;
    if (card.mobile)   vcf += `TEL;TYPE=CELL:${esc(card.mobile)}\r\n`;
    if (card.fax)      vcf += `TEL;TYPE=FAX:${esc(card.fax)}\r\n`;
    if (card.email)    vcf += `EMAIL;TYPE=INTERNET:${esc(card.email)}\r\n`;
    if (card.website)  vcf += `URL:${esc(card.website)}\r\n`;
    if (card.address)  vcf += `ADR;TYPE=WORK:;;${esc(card.address)};;;;\r\n`;
    if (card.notes)    vcf += `NOTE:${esc(card.notes)}\r\n`;
    vcf += 'END:VCARD\r\n';
    return vcf;
  }

  function isVCard(text) {
    return text.trim().toUpperCase().startsWith('BEGIN:VCARD');
  }

  return { parseOCR, parseVCard, toVCF, isVCard };
})();
