// ============ CONFIG & STATE ============
// Par défaut, on utilise la même origine que la page (le front est servi par FastAPI).
// Si la page est ouverte en file://, on retombe sur localhost:8080.
const DEFAULT_API = (location.protocol === 'http:' || location.protocol === 'https:')
  ? location.origin
  : 'http://localhost:8080';
let API_BASE = localStorage.getItem('gtp_api') || DEFAULT_API;
document.getElementById('apiUrl').textContent = API_BASE;

document.getElementById('apiUrl').addEventListener('click', () => {
  const v = prompt('URL de l\'API FastAPI', API_BASE);
  if (v) {
    API_BASE = v.replace(/\/$/, '');
    localStorage.setItem('gtp_api', API_BASE);
    document.getElementById('apiUrl').textContent = API_BASE;
    checkApi();
    loadAll();
  }
});

// ============ TOASTS ============
function toast(msg, type='ok') {
  const t = document.createElement('div');
  t.className = 'toast ' + (type === 'err' ? 'err' : 'ok');
  t.textContent = msg;
  document.getElementById('toasts').appendChild(t);
  setTimeout(() => { t.style.opacity = '0'; t.style.transform = 'translateX(20px)'; t.style.transition = 'all 0.25s'; }, 3000);
  setTimeout(() => t.remove(), 3300);
}

// ============ API HELPER ============
async function api(path, opts = {}) {
  const url = API_BASE + path;
  const cfg = { headers: { 'Content-Type': 'application/json' }, ...opts };
  if (cfg.body && typeof cfg.body !== 'string') cfg.body = JSON.stringify(cfg.body);
  try {
    const r = await fetch(url, cfg);
    const text = await r.text();
    let data;
    try { data = text ? JSON.parse(text) : null; } catch { data = text; }
    if (!r.ok) {
      const detail = (data && data.detail) ? (Array.isArray(data.detail) ? data.detail.map(d => d.msg || JSON.stringify(d)).join(', ') : data.detail) : ('Erreur ' + r.status);
      throw new Error(detail);
    }
    return data;
  } catch (e) {
    if (e.message.includes('Failed to fetch')) throw new Error('API injoignable. Vérifier que FastAPI tourne sur ' + API_BASE);
    throw e;
  }
}

// ============ NAV ============
document.querySelectorAll('#nav button').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('#nav button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('main > section').forEach(s => s.classList.add('hidden'));
    const view = document.getElementById('view-' + btn.dataset.view);
    view.classList.remove('hidden');
    // Re-trigger animation
    view.style.animation = 'none'; void view.offsetWidth; view.style.animation = '';
    // Refresh data for the view
    const handlers = { dashboard: loadDashboard, utilisateurs: loadUsers, voyages: loadTrips, destinations: loadDestSelect, budget: loadBudgetSelect, relations: loadRelSelectors };
    handlers[btn.dataset.view]?.();
  });
});

// ============ HEALTH CHECK ============
async function checkApi() {
  const status = document.getElementById('apiStatus');
  try {
    await api('/api');
    status.classList.add('up'); status.classList.remove('down');
    status.querySelector('div').innerHTML = '<span class="dot"></span> API connectée';
  } catch {
    status.classList.add('down'); status.classList.remove('up');
    status.querySelector('div').innerHTML = '<span class="dot"></span> API hors ligne';
  }
}

// ============ DASHBOARD ============
async function loadDashboard() {
  try {
    const [users, trips, rels] = await Promise.all([
      api('/utilisateurs').catch(() => []),
      api('/voyages').catch(() => []),
      api('/relations').catch(() => [])
    ]);
    document.getElementById('statUsers').textContent = users.length;
    document.getElementById('statTrips').textContent = trips.length;
    document.getElementById('statRel').textContent = rels.length;
    document.getElementById('statDone').textContent = trips.filter(t => t.voyage_fini).length;

    const tbody = document.getElementById('dashTrips');
    const last = trips.slice(-5).reverse();
    tbody.innerHTML = last.length ? last.map(t => `
      <tr>
        <td><span class="id-pill">#${t.voyage_id}</span></td>
        <td><strong>${esc(t.lieu)}</strong></td>
        <td>${formatDate(t)}</td>
        <td>${formatPrice(t.prix)}</td>
        <td><span class="badge ${t.voyage_fini ? 'badge-fini' : 'badge-encours'}">${t.voyage_fini ? 'terminé' : 'à venir'}</span></td>
      </tr>`).join('') : '<tr><td colspan="5" class="empty">Aucun voyage. Créez-en un !</td></tr>';
  } catch (e) { toast(e.message, 'err'); }
}

// ============ UTILISATEURS ============
async function loadUsers() {
  try {
    const users = await api('/utilisateurs');
    const tbody = document.getElementById('usersBody');
    tbody.innerHTML = users.length ? users.map(u => `
      <tr>
        <td><span class="id-pill">#${u.utilisateur_id}</span></td>
        <td><code style="font-family:'JetBrains Mono',monospace;font-size:12px">${esc(u.email)}</code></td>
        <td>${esc(u.prenom)}</td>
        <td>${esc(u.nom)}</td>
        <td>${u.age}</td>
        <td><div class="row-actions">
          <button class="btn btn-ghost btn-sm" onclick="editUser('${esc(u.email)}')">Éditer</button>
          <button class="btn btn-danger" onclick="deleteUser('${esc(u.email)}')">Suppr</button>
        </div></td>
      </tr>`).join('') : '<tr><td colspan="6" class="empty">Aucun utilisateur enregistré.</td></tr>';
  } catch (e) { toast(e.message, 'err'); }
}
async function createUser() {
  try {
    const body = {
      email: gv('u_email'), prenom: gv('u_prenom'), nom: gv('u_nom'),
      age: parseInt(gv('u_age')), mdp: gv('u_mdp')
    };
    await api('/utilisateurs', { method: 'POST', body });
    toast('Utilisateur créé');
    clearUserForm(); loadUsers();
  } catch (e) { toast(e.message, 'err'); }
}
async function deleteUser(email) {
  if (!confirm(`Supprimer ${email} ?`)) return;
  try { await api('/utilisateurs/' + encodeURIComponent(email), { method: 'DELETE' }); toast('Supprimé'); loadUsers(); }
  catch (e) { toast(e.message, 'err'); }
}
async function editUser(email) {
  const champ = prompt('Quel champ modifier ? (email, prenom, nom, age, mdp)', 'prenom');
  if (!champ) return;
  const valeur = prompt(`Nouvelle valeur pour "${champ}"`);
  if (valeur === null) return;
  const body = {}; body[champ] = champ === 'age' ? parseInt(valeur) : valeur;
  try { await api('/utilisateurs/' + encodeURIComponent(email), { method: 'PUT', body }); toast('Modifié'); loadUsers(); }
  catch (e) { toast(e.message, 'err'); }
}
function clearUserForm() { ['u_email','u_prenom','u_nom','u_age','u_mdp'].forEach(id => document.getElementById(id).value = ''); }

// ============ VOYAGES ============
async function loadTrips() {
  try {
    const trips = await api('/voyages');
    const tbody = document.getElementById('tripsBody');
    tbody.innerHTML = trips.length ? trips.map(t => `
      <tr>
        <td><span class="id-pill">#${t.voyage_id}</span></td>
        <td><strong>${esc(t.lieu)}</strong></td>
        <td>${formatDate(t)}</td>
        <td>${formatPrice(t.prix)}</td>
        <td><span class="badge ${t.voyage_fini ? 'badge-fini' : 'badge-encours'}">${t.voyage_fini ? 'terminé' : 'à venir'}</span></td>
        <td><div class="row-actions">
          <button class="btn btn-ghost btn-sm" onclick="toggleTripStatus(${t.voyage_id}, ${!t.voyage_fini})">${t.voyage_fini ? '↩ Rouvrir' : '✓ Marquer fini'}</button>
          <button class="btn btn-ghost btn-sm" onclick="editTrip(${t.voyage_id})">Éditer</button>
          <button class="btn btn-danger" onclick="deleteTrip(${t.voyage_id})">Suppr</button>
        </div></td>
      </tr>`).join('') : '<tr><td colspan="6" class="empty">Aucun voyage. Lancez l\'aventure !</td></tr>';
  } catch (e) { toast(e.message, 'err'); }
}
async function createTrip() {
  try {
    const body = {
      jour: parseInt(gv('v_jour')), mois: parseInt(gv('v_mois')),
      annee: parseInt(gv('v_annee')), lieu: gv('v_lieu'),
      prix: parseFloat(gv('v_prix'))
    };
    await api('/voyages', { method: 'POST', body });
    toast('Voyage créé'); clearTripForm(); loadTrips();
  } catch (e) { toast(e.message, 'err'); }
}
async function deleteTrip(id) {
  if (!confirm('Supprimer ce voyage ? Cela supprimera aussi ses destinations.')) return;
  try { await api('/voyages/' + id, { method: 'DELETE' }); toast('Supprimé'); loadTrips(); }
  catch (e) { toast(e.message, 'err'); }
}
async function toggleTripStatus(id, newStatus) {
  try { await api('/voyages/' + id, { method: 'PUT', body: { voyage_fini: newStatus } }); toast('Statut mis à jour'); loadTrips(); }
  catch (e) { toast(e.message, 'err'); }
}
async function editTrip(id) {
  const champ = prompt('Quel champ modifier ? (lieu, prix, voyage_fini)', 'lieu');
  if (!champ) return;
  let valeur = prompt(`Nouvelle valeur pour "${champ}"`);
  if (valeur === null) return;
  if (champ === 'prix') valeur = parseFloat(valeur);
  if (champ === 'voyage_fini') valeur = (valeur === 'true' || valeur === '1');
  try { await api('/voyages/' + id, { method: 'PUT', body: { [champ]: valeur } }); toast('Modifié'); loadTrips(); }
  catch (e) { toast(e.message, 'err'); }
}
function clearTripForm() { ['v_jour','v_mois','v_annee','v_lieu','v_prix'].forEach(id => document.getElementById(id).value = ''); }

// ============ DESTINATIONS ============
async function loadDestSelect() {
  try {
    const trips = await api('/voyages');
    const sel = document.getElementById('d_voyage_select');
    const cur = sel.value;
    sel.innerHTML = trips.length
      ? trips.map(t => `<option value="${t.voyage_id}">#${t.voyage_id} — ${esc(t.lieu)} (${formatDate(t)})</option>`).join('')
      : '<option value="">Aucun voyage. Créez-en d\'abord un.</option>';
    if (cur) sel.value = cur;
    loadDestinations();
  } catch (e) { toast(e.message, 'err'); }
}
async function loadDestinations() {
  const vid = document.getElementById('d_voyage_select').value;
  if (!vid) { document.getElementById('destBody').innerHTML = ''; return; }
  try {
    const dests = await api(`/voyages/${vid}/destinations/`);
    const tbody = document.getElementById('destBody');
    tbody.innerHTML = dests.length ? dests.map(d => `
      <tr>
        <td><span class="id-pill">${d.ordre ?? '—'}</span></td>
        <td><strong>${esc(d.nom)}</strong></td>
        <td>${d.categorie ? `<span class="badge badge-${d.categorie}">${d.categorie}</span>` : '—'}</td>
        <td>${esc(d.localisation || '—')}</td>
        <td style="max-width:240px;font-size:13px;color:var(--muted)">${esc(d.notes || '')}</td>
        <td><div class="row-actions">
          <button class="btn btn-ghost btn-sm" onclick="editDest(${d.destination_id})">Éditer</button>
          <button class="btn btn-danger" onclick="deleteDest(${d.destination_id})">Suppr</button>
        </div></td>
      </tr>`).join('') : '<tr><td colspan="6" class="empty">Aucune étape. Ajoutez-en une.</td></tr>';
  } catch (e) { toast(e.message, 'err'); }
}
async function createDestination() {
  const vid = document.getElementById('d_voyage_select').value;
  if (!vid) return toast('Sélectionner un voyage', 'err');
  const body = { nom: gv('d_nom') };
  if (gv('d_loc')) body.localisation = gv('d_loc');
  if (gv('d_cat')) body.categorie = gv('d_cat');
  if (gv('d_notes')) body.notes = gv('d_notes');
  if (gv('d_ordre')) body.ordre = parseInt(gv('d_ordre'));
  try {
    await api(`/voyages/${vid}/destinations/`, { method: 'POST', body });
    toast('Étape ajoutée');
    ['d_nom','d_loc','d_cat','d_notes','d_ordre'].forEach(id => document.getElementById(id).value = '');
    loadDestinations();
  } catch (e) { toast(e.message, 'err'); }
}
async function deleteDest(id) {
  if (!confirm('Supprimer cette étape ?')) return;
  try { await api('/destinations/' + id, { method: 'DELETE' }); toast('Supprimée'); loadDestinations(); }
  catch (e) { toast(e.message, 'err'); }
}
async function editDest(id) {
  const champ = prompt('Champ à modifier ? (nom, localisation, categorie, notes, ordre)', 'notes');
  if (!champ) return;
  let valeur = prompt(`Nouvelle valeur`);
  if (valeur === null) return;
  if (champ === 'ordre') valeur = parseInt(valeur);
  try { await api('/destinations/' + id, { method: 'PUT', body: { [champ]: valeur } }); toast('Modifiée'); loadDestinations(); }
  catch (e) { toast(e.message, 'err'); }
}

// ============ BUDGET ============
async function loadBudgetSelect() {
  try {
    const trips = await api('/voyages');
    const sel = document.getElementById('b_voyage_select');
    const cur = sel.value;
    sel.innerHTML = trips.length
      ? trips.map(t => `<option value="${t.voyage_id}">#${t.voyage_id} — ${esc(t.lieu)}</option>`).join('')
      : '<option value="">Aucun voyage.</option>';
    if (cur) sel.value = cur;
    loadBudget();
  } catch (e) { toast(e.message, 'err'); }
}
async function loadBudget() {
  const vid = document.getElementById('b_voyage_select').value;
  if (!vid) return;
  try {
    const b = await api(`/voyages/${vid}/budget`);
    document.getElementById('b_total').value = b.total_amount;
    document.getElementById('b_spent').value = b.spent_amount;
    renderProgress(b.total_amount, b.spent_amount);
  } catch (e) {
    document.getElementById('b_total').value = '';
    document.getElementById('b_spent').value = '';
    document.getElementById('b_progress').innerHTML = `<div style="color:var(--muted);font-style:italic;font-family:'Fraunces',serif">Aucun budget pour ce voyage. Créez-en un.</div>`;
  }
}
function renderProgress(total, spent) {
  const pct = total > 0 ? Math.min(100, (spent / total) * 100) : 0;
  const remaining = total - spent;
  const over = spent > total;
  document.getElementById('b_progress').innerHTML = `
    <div style="display:flex;justify-content:space-between;margin-bottom:6px;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.1em;text-transform:uppercase;color:var(--muted)">
      <span>Dépensé · ${formatPrice(spent)}</span>
      <span>${pct.toFixed(0)}%</span>
      <span>Restant · ${formatPrice(remaining)}</span>
    </div>
    <div style="background:var(--cream-2);height:10px;border-radius:5px;overflow:hidden;border:1px solid var(--line)">
      <div style="width:${pct}%;height:100%;background:${over ? 'var(--rust)' : 'var(--moss)'};transition:width 0.4s"></div>
    </div>
    ${over ? '<div style="color:var(--rust);margin-top:6px;font-size:12px">⚠ Budget dépassé</div>' : ''}
  `;
}
async function createBudget() {
  const vid = document.getElementById('b_voyage_select').value;
  if (!vid) return toast('Sélectionner un voyage', 'err');
  const body = {
    total_amount: parseFloat(gv('b_total')) || 0,
    spent_amount: parseFloat(gv('b_spent')) || 0
  };
  try { await api(`/voyages/${vid}/budget`, { method: 'POST', body }); toast('Budget créé'); loadBudget(); }
  catch (e) { toast(e.message, 'err'); }
}
async function updateBudget() {
  const vid = document.getElementById('b_voyage_select').value;
  if (!vid) return;
  const body = {
    total_amount: parseFloat(gv('b_total')),
    spent_amount: parseFloat(gv('b_spent'))
  };
  try { await api(`/voyages/${vid}/budget`, { method: 'PUT', body }); toast('Budget mis à jour'); loadBudget(); }
  catch (e) { toast(e.message, 'err'); }
}

// ============ RELATIONS ============
async function loadRelSelectors() {
  try {
    const [users, trips] = await Promise.all([api('/utilisateurs'), api('/voyages')]);
    document.getElementById('r_user').innerHTML = users.map(u => `<option value="${u.utilisateur_id}">#${u.utilisateur_id} — ${esc(u.prenom)} ${esc(u.nom)}</option>`).join('') || '<option value="">Aucun utilisateur</option>';
    document.getElementById('r_trip').innerHTML = trips.map(t => `<option value="${t.voyage_id}">#${t.voyage_id} — ${esc(t.lieu)}</option>`).join('') || '<option value="">Aucun voyage</option>';
    loadRelations();
  } catch (e) { toast(e.message, 'err'); }
}
async function loadRelations() {
  try {
    const [rels, users, trips] = await Promise.all([
      api('/relations').catch(() => []),
      api('/utilisateurs').catch(() => []),
      api('/voyages').catch(() => [])
    ]);
    const userMap = Object.fromEntries(users.map(u => [u.utilisateur_id, `${u.prenom} ${u.nom}`]));
    const tripMap = Object.fromEntries(trips.map(t => [t.voyage_id, t.lieu]));
    const tbody = document.getElementById('relBody');
    tbody.innerHTML = rels.length ? rels.map(r => `
      <tr>
        <td><span class="id-pill">#${r.utilisateur_id}</span> ${esc(userMap[r.utilisateur_id] || '?')}</td>
        <td><span class="id-pill">#${r.voyage_id}</span> ${esc(tripMap[r.voyage_id] || '?')}</td>
        <td><button class="btn btn-danger" onclick="deleteRel(${r.utilisateur_id}, ${r.voyage_id})">Délier</button></td>
      </tr>`).join('') : '<tr><td colspan="3" class="empty">Aucune relation.</td></tr>';
  } catch (e) { toast(e.message, 'err'); }
}
async function createRelation() {
  const utilisateur_id = parseInt(document.getElementById('r_user').value);
  const voyage_id = parseInt(document.getElementById('r_trip').value);
  if (!utilisateur_id || !voyage_id) return toast('Sélectionner les deux', 'err');
  try { await api('/relations', { method: 'POST', body: { utilisateur_id, voyage_id } }); toast('Lié'); loadRelations(); }
  catch (e) { toast(e.message, 'err'); }
}
async function deleteRel(utilisateur_id, voyage_id) {
  if (!confirm('Délier cet utilisateur de ce voyage ?')) return;
  try { await api('/relations', { method: 'DELETE', body: { utilisateur_id, voyage_id } }); toast('Délié'); loadRelations(); }
  catch (e) { toast(e.message, 'err'); }
}

// ============ HELPERS ============
function gv(id) { return document.getElementById(id).value.trim(); }
function esc(s) { return String(s ?? '').replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m])); }
function formatDate(t) {
  if (t.jour && t.mois && t.annee) {
    return `${String(t.jour).padStart(2,'0')}/${String(t.mois).padStart(2,'0')}/${t.annee}`;
  }
  if (t.date) return t.date;
  return '—';
}
function formatPrice(p) {
  if (p == null) return '—';
  return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(p);
}

function loadAll() { loadDashboard(); }

// ============ INIT ============
checkApi();
loadDashboard();
setInterval(checkApi, 30000);
