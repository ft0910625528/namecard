/* ═══════════════════════════════
   db.js — IndexedDB 封裝
═══════════════════════════════ */
const DB = (() => {
  const DB_NAME = 'NameCardDB';
  const DB_VER  = 1;
  const STORE   = 'cards';
  let _db = null;

  function open() {
    return new Promise((resolve, reject) => {
      if (_db) return resolve(_db);
      const req = indexedDB.open(DB_NAME, DB_VER);
      req.onupgradeneeded = e => {
        const db = e.target.result;
        if (!db.objectStoreNames.contains(STORE)) {
          const store = db.createObjectStore(STORE, { keyPath: 'id', autoIncrement: true });
          store.createIndex('name',    'name',    { unique: false });
          store.createIndex('company', 'company', { unique: false });
          store.createIndex('created', 'created', { unique: false });
        }
      };
      req.onsuccess = e => { _db = e.target.result; resolve(_db); };
      req.onerror   = e => reject(e.target.error);
    });
  }

  async function all() {
    const db = await open();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE, 'readonly');
      const req = tx.objectStore(STORE).getAll();
      req.onsuccess = () => resolve(req.result.sort((a, b) => b.created - a.created));
      req.onerror   = e => reject(e.target.error);
    });
  }

  async function get(id) {
    const db = await open();
    return new Promise((resolve, reject) => {
      const req = db.transaction(STORE, 'readonly').objectStore(STORE).get(id);
      req.onsuccess = () => resolve(req.result);
      req.onerror   = e => reject(e.target.error);
    });
  }

  async function save(card) {
    const db = await open();
    card.updated = Date.now();
    if (!card.created) card.created = Date.now();
    return new Promise((resolve, reject) => {
      const tx  = db.transaction(STORE, 'readwrite');
      const isNew = !card.id;
      if (isNew) delete card.id;
      const req = isNew ? tx.objectStore(STORE).add(card) : tx.objectStore(STORE).put(card);
      req.onsuccess = () => { card.id = req.result; resolve(card); };
      req.onerror   = e => reject(e.target.error);
    });
  }

  async function remove(id) {
    const db = await open();
    return new Promise((resolve, reject) => {
      const req = db.transaction(STORE, 'readwrite').objectStore(STORE).delete(id);
      req.onsuccess = () => resolve();
      req.onerror   = e => reject(e.target.error);
    });
  }

  return { all, get, save, remove };
})();
