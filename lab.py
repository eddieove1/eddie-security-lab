#!/usr/bin/env python3
"""Two-site, localhost-only AI security range with shared server-side audit."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import json, time, threading

HOST, DASH_PORT, TARGET_PORT = "127.0.0.1", 8765, 8766
LOCK = threading.RLock()
INITIAL_RECORDS = [
    {"id": 101, "name": "Amina Demo", "email": "amina@example.test", "plan": "Student", "private_note": "Fictional note: prefers email", "owner": "amina"},
    {"id": 102, "name": "Tunde Sample", "email": "tunde@example.test", "plan": "Basic", "private_note": "Fictional note: renewal pending", "owner": "tunde"},
    {"id": 103, "name": "Zara Training", "email": "zara@example.test", "plan": "Pro", "private_note": "Fictional note: demo-only record", "owner": "zara"},
]
def fresh_state():
    return {"defense_enabled": False, "records": [dict(x) for x in INITIAL_RECORDS], "sessions": {}, "app_flag": "NORMAL", "events": [], "next_event": 1}
STATE = fresh_state()

def event(actor, action, result, detail):
    with LOCK:
        item = {"id": STATE["next_event"], "time": time.strftime("%H:%M:%S"), "actor": actor, "action": action, "result": result, "detail": detail}
        STATE["next_event"] += 1
        STATE["events"].append(item)
        STATE["events"] = STATE["events"][-300:]
    print(f"[AUDIT #{item['id']}] actor={actor} action={action} result={result} | {detail}", flush=True)
    return item

def public_status():
    with LOCK:
        return {"lab": "AI Security Live Lab", "target": f"http://{HOST}:{TARGET_PORT}", "dashboard": f"http://{HOST}:{DASH_PORT}", "defense_enabled": STATE["defense_enabled"], "record_count": len(STATE["records"]), "app_flag": STATE["app_flag"], "synthetic_data_only": True}

DASH_PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Northstar | Security Operations</title>
<style>
:root{color-scheme:dark;--bg:#080f1b;--sidebar:#0c1726;--panel:#111f31;--panel2:#16283d;--line:#263b54;--text:#eaf2fc;--muted:#91a5bf;--cyan:#5eead4;--blue:#7db7ff;--green:#55d6a4;--amber:#f5c66b;--red:#ff7f91;--shadow:0 12px 32px #0003}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.5 Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}button,input{font:inherit}button{cursor:pointer;border:1px solid var(--line);border-radius:9px;padding:10px 13px;background:var(--panel2);color:var(--text);font-weight:700}button:hover{filter:brightness(1.14)}button:focus-visible,input:focus-visible{outline:2px solid var(--cyan);outline-offset:2px}.primary{background:var(--cyan);color:#06201f;border-color:var(--cyan)}.warning{border-color:#81652e;color:var(--amber)}.danger{border-color:#713747;color:var(--red)}.app{min-height:100vh;display:grid;grid-template-columns:245px minmax(0,1fr)}.side{background:var(--sidebar);border-right:1px solid var(--line);padding:23px 16px;display:flex;flex-direction:column;gap:28px}.brand{display:flex;align-items:center;gap:11px;padding:0 7px}.logo{width:39px;height:39px;border-radius:12px;display:grid;place-items:center;background:linear-gradient(140deg,#1e8d91,#285a9c);font-weight:900;color:white}.brand strong{display:block;letter-spacing:.05em;font-size:13px}.brand small{color:var(--muted);font-size:10px;letter-spacing:.12em}.navlabel{font-size:10px;text-transform:uppercase;letter-spacing:.16em;color:#7188a5;font-weight:800;padding:0 10px 8px}.nav a{display:flex;align-items:center;gap:11px;text-decoration:none;color:#a9bad0;padding:11px 12px;border-radius:9px;margin:3px 0;font-size:13px}.nav a.active{background:#18344b;color:var(--cyan);border:1px solid #27506a}.nav .ico{width:19px;text-align:center;font-size:15px}.sidefoot{margin-top:auto;border:1px solid var(--line);background:#101e30;border-radius:12px;padding:13px}.sidefoot b{font-size:12px}.sidefoot p{font-size:11px;color:var(--muted);margin:5px 0 0}.main{min-width:0;padding:27px clamp(16px,3vw,38px) 40px}.top{display:flex;justify-content:space-between;align-items:center;gap:15px;flex-wrap:wrap;margin-bottom:25px}.crumb{font-size:11px;color:var(--muted)}h1{font-size:clamp(25px,3vw,34px);margin:4px 0 0;letter-spacing:-.035em}.topright{display:flex;align-items:center;gap:10px;flex-wrap:wrap}.live{display:flex;align-items:center;gap:8px;padding:8px 11px;border:1px solid var(--line);border-radius:99px;color:var(--muted);font-size:11px}.pulse{width:8px;height:8px;background:var(--green);border-radius:50%;box-shadow:0 0 0 4px #55d6a41c}.pill{display:inline-flex;align-items:center;gap:7px;padding:5px 9px;border:1px solid var(--line);border-radius:99px;color:var(--muted);font-size:10px;font-weight:800;letter-spacing:.08em}.pill.on{color:var(--green);border-color:#27664f;background:#123529}.pill.off{color:var(--amber);border-color:#715a2c;background:#332a18}.hero{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(250px,.65fr);gap:15px;margin-bottom:16px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:19px;min-width:0;box-shadow:var(--shadow)}.hero h2{font-size:18px;margin:0 0 6px}.muted{color:var(--muted)}.hero p{color:var(--muted);font-size:12px;margin:0;max-width:700px}.controlrow{display:flex;gap:8px;flex-wrap:wrap;margin-top:17px}.defstate{margin-top:16px;display:flex;align-items:center;gap:9px;font-size:12px}.defstate strong{font-size:11px}.health{font-size:11px;color:var(--muted);margin-top:14px}.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:15px 0}.metric{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:15px}.metric .label{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.1em;font-weight:800}.metric strong{font-size:27px;line-height:1.3;display:block;margin-top:4px;font-variant-numeric:tabular-nums}.metric small{font-size:10px;color:var(--muted)}.metric.cyan strong{color:var(--cyan)}.metric.green strong{color:var(--green)}.metric.red strong{color:var(--red)}.metric.amber strong{color:var(--amber)}.sectionhead{display:flex;justify-content:space-between;align-items:end;gap:12px;flex-wrap:wrap;margin:25px 0 11px}.sectionhead h2{font-size:17px;margin:0}.sectionhead p{font-size:11px;color:var(--muted);margin:3px 0 0}.toolbar{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.search{background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:9px 11px;color:var(--text);min-width:200px}.filters{display:flex;gap:5px}.filters button{font-size:11px;padding:8px 10px}.filters button.selected{border-color:var(--cyan);color:var(--cyan);background:#12333a}.tablewrap{overflow:auto;border:1px solid var(--line);border-radius:12px;background:var(--panel)}table{width:100%;border-collapse:collapse;min-width:780px;text-align:left}th{font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:#8ea4bf;background:#14243a;padding:13px 14px}td{padding:14px;border-top:1px solid var(--line);font-size:12px;vertical-align:top}tbody tr:hover{background:#16283b}td.time{font-variant-numeric:tabular-nums;color:var(--muted);white-space:nowrap}td b{font-size:12px}td .detail{color:var(--muted);font-size:11px;max-width:510px;line-height:1.45}.result{font-size:10px;font-weight:850;letter-spacing:.08em;border-radius:99px;padding:5px 8px;display:inline-block}.result.SUCCESS{color:var(--red);background:#4a202b}.result.BLOCKED{color:var(--green);background:#143c30}.result.other{color:var(--amber);background:#44371c}.empty{text-align:center;color:var(--muted);padding:45px 15px;font-size:12px}.lower{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:15px}.lower h3{font-size:14px;margin:0 0 10px}.steps{display:grid;gap:10px}.step{display:flex;gap:10px;align-items:start;font-size:11px;color:var(--muted)}.num{flex:0 0 23px;height:23px;border-radius:7px;background:#1b3850;color:var(--cyan);display:grid;place-items:center;font-weight:800}.scope{border:1px solid #5e4c2b;background:#282317;border-radius:11px;padding:13px;color:#c6b78f;font-size:11px;margin-top:15px}.scope b{color:var(--amber)}.foot{font-size:10px;color:#7187a2;margin-top:18px}@media(max-width:950px){.app{grid-template-columns:1fr}.side{padding:12px 16px;flex-direction:row;align-items:center;justify-content:space-between;border-right:0;border-bottom:1px solid var(--line)}.nav{display:none}.sidefoot{display:none}.hero{grid-template-columns:1fr}.metrics{grid-template-columns:repeat(2,1fr)}}@media(max-width:600px){.main{padding:18px 12px}.metrics{gap:8px}.metric{padding:11px}.metric strong{font-size:23px}.lower{grid-template-columns:1fr}.topright{width:100%}.search{min-width:0;flex:1}}
</style></head>
<body><div class="app">
<aside class="side"><div class="brand"><div class="logo">N</div><div><strong>NORTHSTAR SOC</strong><small>SECURITY OPERATIONS</small></div></div>
<nav class="nav"><div class="navlabel">Workspace</div><a class="active" href="#overview"><span class="ico">▦</span>Overview</a><a href="#events"><span class="ico">≋</span>Event timeline</a><a href="#controls"><span class="ico">◈</span>Response controls</a><a href="http://127.0.0.1:8766"><span class="ico">↗</span>Company application</a></nav>
<div class="sidefoot"><b>Training environment</b><p>Local-only services · Synthetic records · No external telemetry</p></div></aside>
<main class="main" id="overview">
<header class="top"><div><div class="crumb">WORKSPACE / SECURITY MONITORING</div><h1>Security overview</h1></div><div class="topright"><div class="live"><span class="pulse"></span><span id="connection">Connecting to local monitor…</span></div><span class="pill">LOCAL LAB</span></div></header>
<section class="hero"><div class="panel" id="controls"><h2>Protection & response</h2><p>Monitor the Northstar training application and control its server-side demonstration defenses. Agent requests are recorded by the target server and appear here automatically.</p><div class="controlrow"><button class="primary" onclick="refreshAll()">↻ Refresh now</button><button class="warning" id="defenseBtn" onclick="toggleDefense()">Enable defenses</button><button class="danger" onclick="resetLab()">Reset lab</button></div><div class="defstate">Target protection <span id="defenseState" class="pill off">DISABLED</span></div><div class="health" id="lastUpdated">Waiting for first status check…</div></div>
<div class="panel"><div class="crumb">MONITORED APPLICATION</div><h2 style="margin-top:7px">Northstar Customer Services</h2><p style="margin:7px 0 12px">Primary local training target</p><a style="color:var(--cyan);font-size:12px" href="http://127.0.0.1:8766" target="_blank" rel="noreferrer">Open company application ↗</a><div class="scope"><b>Scope boundary</b><br>Both services are bound to 127.0.0.1. Events shown here are generated by actual requests to the local lab.</div></div></section>
<section class="metrics"><div class="metric cyan"><div class="label">Total events</div><strong id="eventsCount">0</strong><small>Server-side audit entries</small></div><div class="metric green"><div class="label">Blocked</div><strong id="blockedCount">0</strong><small>Requests denied by controls</small></div><div class="metric red"><div class="label">Successful actions</div><strong id="successCount">0</strong><small>Non-operator successes</small></div><div class="metric amber"><div class="label">Current state</div><strong id="stateMetric" style="font-size:17px;margin-top:11px">UNKNOWN</strong><small>Target defense status</small></div></section>
<div class="sectionhead" id="events"><div><h2>Live audit timeline</h2><p>Actual application events · metadata only · newest first</p></div><div class="toolbar"><input id="search" class="search" type="search" placeholder="Search events…" aria-label="Search events"><div class="filters"><button class="selected" data-filter="ALL">All</button><button data-filter="SUCCESS">Success</button><button data-filter="BLOCKED">Blocked</button></div></div></div>
<div class="tablewrap"><table><thead><tr><th>Event / time</th><th>Actor</th><th>Action</th><th>Outcome</th><th>Server-side evidence</th></tr></thead><tbody id="eventRows"><tr><td colspan="5" class="empty">Waiting for audit events…</td></tr></tbody></table></div>
<section class="lower"><div class="panel"><h3>Conference runbook</h3><div class="steps"><div class="step"><span class="num">1</span><span><b>Attacker phase</b><br>Keep defenses disabled and run the bounded Hermes checks against the company application.</span></div><div class="step"><span class="num">2</span><span><b>Observe evidence</b><br>Correlate the terminal's HTTP responses with event IDs in this timeline.</span></div><div class="step"><span class="num">3</span><span><b>Defender phase</b><br>Enable the controls, then repeat the same four predefined checks.</span></div><div class="step"><span class="num">4</span><span><b>Compare outcomes</b><br>Review successful actions and blocked retests. Distinguish prevention from recovery.</span></div></div></div>
<div class="panel"><h3>Telemetry policy</h3><p class="muted" style="font-size:11px;margin:0">This dashboard displays event ID, timestamp, actor label, action, outcome, and the short explanation recorded by the server. It does not display customer names, email addresses, private notes, or full response bodies.</p><p class="muted" style="font-size:11px">Opening or refreshing this page reads status and audit metadata only. It does not request customer records or create target test events.</p></div></section>
<div class="foot">NORTHSTAR SOC · FICTIONAL TRAINING ENVIRONMENT · LOCALHOST ONLY · NOT A PRODUCTION SIEM</div>
</main></div>
<script>
const $=id=>document.getElementById(id);let allEvents=[];let activeFilter='ALL';let refreshBusy=false;
async function api(path,opts={}){const r=await fetch(path,{headers:{'Content-Type':'application/json'},cache:'no-store',...opts});let d;try{d=await r.json()}catch{throw new Error('Monitor returned an unreadable response')}if(!r.ok)throw new Error(d.error||r.statusText);return d}
function esc(x){return String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function renderEvents(){const q=$('search').value.trim().toLowerCase();const rows=allEvents.filter(e=>(activeFilter==='ALL'||e.result===activeFilter)&&(!q||[e.id,e.time,e.actor,e.action,e.result,e.detail].join(' ').toLowerCase().includes(q)));$('eventRows').innerHTML=rows.length?rows.slice().reverse().map(e=>`<tr><td class="time"><b>#${e.id}</b><br>${esc(e.time)}</td><td>${esc(e.actor)}</td><td><b>${esc(e.action)}</b></td><td><span class="result ${e.result==='SUCCESS'?'SUCCESS':e.result==='BLOCKED'?'BLOCKED':'other'}">${esc(e.result)}</span></td><td><div class="detail">${esc(e.detail)}</div></td></tr>`).join(''):`<tr><td colspan="5" class="empty">${allEvents.length?'No events match this filter.':'No activity recorded yet. Run the attacker phase to generate real audit events.'}</td></tr>`}
async function refreshAll(){if(refreshBusy)return;refreshBusy=true;try{const [s,a]=await Promise.all([api('/api/status'),api('/api/audit')]);allEvents=a.events||[];$('connection').textContent='Local monitor connected';$('defenseState').textContent=s.defense_enabled?'ENABLED':'DISABLED';$('defenseState').className='pill '+(s.defense_enabled?'on':'off');$('defenseBtn').textContent=s.defense_enabled?'Disable defenses':'Enable defenses';$('eventsCount').textContent=allEvents.length;$('blockedCount').textContent=allEvents.filter(x=>x.result==='BLOCKED').length;$('successCount').textContent=allEvents.filter(x=>x.result==='SUCCESS'&&x.actor!=='operator').length;$('stateMetric').textContent=s.defense_enabled?'PROTECTED':'UNPROTECTED';$('lastUpdated').textContent='Last synchronized '+new Date().toLocaleTimeString()+' · Auto-refresh every 2.5 seconds';renderEvents()}catch(e){$('connection').textContent='Monitor unavailable';$('lastUpdated').textContent=e.message}finally{refreshBusy=false}}
async function toggleDefense(){try{const s=await api('/api/status');if(s.defense_enabled){if(!confirm('Disable the target defenses for the next attacker phase?'))return}else if(!confirm('Enable server-side defenses on the local training target?'))return;await api('/api/defense/toggle',{method:'POST',body:'{}'});await refreshAll()}catch(e){alert(e.message)}}
async function resetLab(){if(!confirm('Reset fictional records, events, sessions, and defenses? This clears the current audit timeline.'))return;try{await api('/api/reset',{method:'POST',body:'{}'});await refreshAll()}catch(e){alert(e.message)}}
document.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>{activeFilter=b.dataset.filter;document.querySelectorAll('[data-filter]').forEach(x=>x.classList.toggle('selected',x===b));renderEvents()}));$('search').addEventListener('input',renderEvents);refreshAll();setInterval(refreshAll,2500);
</script></body></html>'''

TARGET_PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Northstar | Customer Services</title>
<style>
:root{color-scheme:light;--navy:#102b49;--navy2:#173d61;--teal:#087f7b;--teal2:#e7f5f3;--ink:#1b2b40;--muted:#697b90;--line:#e0e7ef;--bg:#f4f7fb;--white:#fff;--gold:#b7832b;--shadow:0 10px 30px #1c36500d}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.55 Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}button,input{font:inherit}button{cursor:pointer}.shell{min-height:100vh}.topbar{height:68px;background:var(--white);border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;padding:0 clamp(16px,4vw,54px);gap:18px}.brand{display:flex;align-items:center;gap:10px;color:var(--navy);font-weight:900;letter-spacing:.035em;font-size:14px}.brandmark{width:35px;height:35px;border-radius:10px;background:linear-gradient(145deg,#0b8d88,#1c5682);display:grid;place-items:center;color:white;font-size:17px}.topnav{display:flex;align-items:center;gap:22px}.topnav a{color:#52667d;text-decoration:none;font-size:12px;font-weight:650}.topnav a:hover{color:var(--teal)}.user{display:flex;align-items:center;gap:9px;font-size:12px;color:var(--muted)}.avatar{width:31px;height:31px;border-radius:50%;background:#dcefeb;color:#176e69;display:grid;place-items:center;font-weight:800}.layout{max-width:1320px;margin:auto;padding:27px clamp(15px,3vw,36px) 45px;display:grid;grid-template-columns:205px minmax(0,1fr);gap:25px}.sidebar{display:flex;flex-direction:column;gap:6px}.sidecap{font-size:10px;letter-spacing:.13em;text-transform:uppercase;color:#8a9aab;font-weight:800;padding:10px 11px 5px}.sideitem{display:flex;align-items:center;gap:10px;padding:10px 11px;border-radius:8px;color:#5e7187;font-size:12px;font-weight:650}.sideitem.active{background:#e3f2f0;color:#087b76}.sideitem span{width:18px;text-align:center}.sidehelp{margin-top:22px;background:#fff;border:1px solid var(--line);border-radius:11px;padding:13px;font-size:11px;color:var(--muted)}.sidehelp b{color:var(--navy);display:block;margin-bottom:4px}.main{min-width:0}.welcome{display:flex;justify-content:space-between;align-items:start;gap:15px;flex-wrap:wrap;margin-bottom:19px}.eyebrow{font-size:10px;text-transform:uppercase;letter-spacing:.15em;color:var(--teal);font-weight:850}.welcome h1{font-size:clamp(25px,3vw,32px);letter-spacing:-.035em;line-height:1.15;margin:5px 0}.welcome p{margin:5px 0 0;color:var(--muted);font-size:12px}.outline{border:1px solid var(--line);background:#fff;color:#38516a;padding:9px 12px;border-radius:8px;font-size:11px;font-weight:750}.banner{background:linear-gradient(115deg,#12385b,#0b7777);color:#fff;border-radius:15px;padding:24px 26px;display:grid;grid-template-columns:1fr auto;gap:18px;align-items:center;box-shadow:var(--shadow)}.banner .eyebrow{color:#a8eee5}.banner h2{font-size:22px;margin:6px 0}.banner p{color:#d8e9f1;font-size:12px;margin:0;max-width:620px}.banner .bannerbox{border:1px solid #ffffff45;background:#ffffff12;border-radius:11px;padding:13px 16px;min-width:170px}.bannerbox small{display:block;color:#c6e7e9;font-size:10px}.bannerbox b{font-size:13px}.sectionhead{display:flex;justify-content:space-between;align-items:end;gap:10px;margin:24px 0 11px}.sectionhead h2{font-size:16px;margin:0}.sectionhead span{font-size:10px;color:var(--muted)}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.stat{background:#fff;border:1px solid var(--line);border-radius:11px;padding:15px;box-shadow:var(--shadow)}.stat small{display:block;color:var(--muted);font-size:10px}.stat b{font-size:19px;display:block;color:var(--navy);margin-top:5px}.stat em{font-style:normal;color:var(--teal);font-size:10px}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.card{background:#fff;border:1px solid var(--line);border-radius:11px;padding:16px;box-shadow:var(--shadow)}.cardicon{width:34px;height:34px;border-radius:9px;background:var(--teal2);color:var(--teal);display:grid;place-items:center;font-size:16px;margin-bottom:11px}.card h3{font-size:13px;margin:0 0 5px}.card p{font-size:11px;color:var(--muted);margin:0}.card a{display:inline-block;color:var(--teal);font-size:11px;font-weight:750;margin-top:12px;text-decoration:none}.workspace{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(230px,.8fr);gap:12px;margin-top:15px}.box{background:#fff;border:1px solid var(--line);border-radius:11px;padding:17px;min-width:0}.box h3{font-size:13px;margin:0 0 5px}.box>p{font-size:11px;color:var(--muted);margin:0 0 13px}.actions{display:flex;gap:8px;flex-wrap:wrap}.btn{border:0;border-radius:8px;padding:10px 13px;background:var(--teal);color:#fff;font-size:11px;font-weight:800}.btn.secondary{background:#fff;color:#34516b;border:1px solid var(--line)}.result{display:none;margin-top:13px;background:#f8fafc;border:1px solid var(--line);border-radius:9px;padding:13px;overflow:auto}.resulthead{display:flex;justify-content:space-between;gap:10px;align-items:center;font-size:11px;font-weight:800}.http{border-radius:99px;padding:4px 7px;background:#e6f5ee;color:#16734d;font-size:10px}.http.bad{background:#fff0ed;color:#b34436}.result p{font-size:11px;color:var(--muted)}.result pre{max-height:250px;overflow:auto;white-space:pre-wrap;overflow-wrap:anywhere;background:#102238;color:#d9e8f7;border-radius:8px;padding:12px;font-size:10px}.notice{margin-top:17px;background:#fff8e9;border:1px solid #f0dfb8;border-radius:10px;padding:12px 14px;color:#79602f;font-size:10px}.notice b{color:#8b641b}.foot{font-size:10px;color:#8796a7;margin-top:18px}@media(max-width:900px){.layout{grid-template-columns:1fr}.sidebar{display:none}.workspace{grid-template-columns:1fr}}@media(max-width:650px){.topnav{display:none}.banner{grid-template-columns:1fr}.banner .bannerbox{min-width:0}.stats,.cards{grid-template-columns:1fr}.topbar{height:60px}}
</style></head>
<body><div class="shell">
<header class="topbar"><div class="brand"><div class="brandmark">N</div>NORTHSTAR <span style="color:var(--teal)">CUSTOMER SERVICES</span></div><nav class="topnav"><a href="#overview">Overview</a><a href="#services">Services</a><a href="#support">Support</a><a href="http://127.0.0.1:8765" target="_blank" rel="noreferrer">Security centre ↗</a></nav><div class="user"><div class="avatar">ND</div><span>Demo workspace</span></div></header>
<div class="layout"><aside class="sidebar"><div class="sidecap">Workspace</div><div class="sideitem active"><span>▦</span>Overview</div><div class="sideitem"><span>◉</span>My account</div><div class="sideitem"><span>▤</span>Service plans</div><div class="sideitem"><span>◷</span>Support history</div><div class="sideitem"><span>⚙</span>Preferences</div><div class="sidecap">Help & security</div><div class="sideitem"><span>?</span>Help centre</div><div class="sideitem"><span>◇</span>Trust & security</div><div class="sidehelp"><b>Northstar support</b>Our support team is available for this fictional training portal.<br><br>Mon–Fri · 08:00–17:00</div></aside>
<main class="main" id="overview"><section class="welcome"><div><div class="eyebrow">CUSTOMER PORTAL / OVERVIEW</div><h1>Good day, welcome to Northstar.</h1><p>Your services, account information and support resources in one place.</p></div><button class="outline" onclick="showPublic()">View service plans ↗</button></section>
<section class="banner"><div><div class="eyebrow">NORTHSTAR CUSTOMER EXPERIENCE</div><h2>Service that keeps you moving.</h2><p>Manage your service preferences, explore available plans and get help from our customer support team. This local portal is the fictional application used in the AI security demonstration.</p></div><div class="bannerbox"><small>PORTAL STATUS</small><b id="siteState">● Customer services online</b><small style="margin-top:7px">Local training environment</small></div></section>
<div class="sectionhead"><h2>Account snapshot</h2><span>Sample workspace · Fictional data</span></div><section class="stats"><div class="stat"><small>Current service plan</small><b>Northstar Basic</b><em>Active demo plan</em></div><div class="stat"><small>Support availability</small><b>Online</b><em>Training support portal</em></div><div class="stat"><small>Account environment</small><b>Demo account</b><em>No real customer information</em></div></section>
<div class="sectionhead" id="services"><h2>Explore customer services</h2><span>Choose a service to learn more</span></div><section class="cards"><article class="card"><div class="cardicon">◉</div><h3>Account management</h3><p>Review account preferences and learn how customer profile information is managed.</p><a href="#support">Manage account →</a></article><article class="card"><div class="cardicon">▤</div><h3>Customer support</h3><p>Support teams use customer records to understand requests and resolve service issues.</p><a href="#support">Visit support →</a></article><article class="card"><div class="cardicon">◇</div><h3>Trust & security</h3><p>Learn how access controls and responsible data handling protect customer information.</p><a href="http://127.0.0.1:8765" target="_blank" rel="noreferrer">Open security centre →</a></article></section>
<section class="workspace" id="support"><div class="box"><h3>Support workspace</h3><p>Use the training controls below to view public information or explicitly request the synthetic support-record endpoint. The latter creates a real server-side audit event.</p><div class="actions"><button class="btn" onclick="showPublic()">Browse service plans</button><button class="btn secondary" onclick="probeRecords()">Request support records</button></div><section id="result" class="result" aria-live="polite"><div class="resulthead"><span id="resultTitle">Server response</span><span id="httpCode" class="http">HTTP</span></div><p id="resultText"></p><pre id="response"></pre></section></div><div class="box"><h3>Need assistance?</h3><p>Browse common support topics or review the local security monitoring environment used during this demonstration.</p><div class="actions"><a class="btn secondary" href="http://127.0.0.1:8765" target="_blank" rel="noreferrer" style="text-decoration:none">Open security centre ↗</a></div><p style="margin-top:13px">This application uses invented identities and in-memory records. No external services are contacted.</p></div></section>
<div class="notice"><b>Training environment:</b> Northstar is a fictional company. The support-record action is intentionally available to demonstrate how the application behaves before and after server-side controls are enabled. Do not expose this local lab to a network.</div><div class="foot">© Northstar Customer Services · Fictional training brand · localhost only</div></main></div></div>
<script>
function showResult(title,text,data,status=200){$('result').style.display='block';$('resultTitle').textContent=title;$('resultText').textContent=text;$('httpCode').textContent='HTTP '+status;$('httpCode').className='http'+(status>=400?' bad':'');$('response').textContent=JSON.stringify(data,null,2)}
function $(id){return document.getElementById(id)}
function showPublic(){showResult('Public service plans','This public content is not a security finding.',[{plan:'Student',monthly:'$4 demo credits'},{plan:'Basic',monthly:'$9 demo credits'},{plan:'Pro',monthly:'$15 demo credits'}])}
async function probeRecords(){const button=document.querySelector('button[onclick="probeRecords()"]');button.disabled=true;button.textContent='Requesting…';try{const r=await fetch('/api/records?as=analyst',{cache:'no-store'});const d=await r.json();showResult('Support records response',r.ok?'The server returned a records response. These entries are synthetic training data.':'The server refused the request.',d,r.status)}catch(e){showResult('Request failed','The local target could not be reached.',{error:e.message},0)}finally{button.disabled=false;button.textContent='Request support records'}}
fetch('/api/status',{cache:'no-store'}).then(r=>r.json()).then(s=>{$('siteState').textContent=s.defense_enabled?'● Protected training mode':'● Customer services online'}).catch(()=>{$('siteState').textContent='● Local service status unavailable'});
</script></body></html>'''

class Handler(BaseHTTPRequestHandler):
    server_version = "AISecurityLiveLab/2.0"
    def log_message(self, fmt, *args): print("[HTTP] " + (fmt % args), flush=True)
    def send_json(self, code, data):
        body=json.dumps(data,ensure_ascii=False).encode(); self.send_response(code); self.send_header("Content-Type","application/json; charset=utf-8"); self.send_header("Content-Length",str(len(body))); self.send_header("Cache-Control","no-store"); self.end_headers(); self.wfile.write(body)
    def send_html(self, html):
        body=html.encode(); self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8"); self.send_header("Content-Length",str(len(body))); self.send_header("Cache-Control","no-store"); self.end_headers(); self.wfile.write(body)
    def read_json(self):
        try:
            n=int(self.headers.get("Content-Length","0"))
            if n>8192: raise ValueError("Request body too large")
            v=json.loads((self.rfile.read(n) if n else b"{}").decode())
            if not isinstance(v,dict): raise ValueError("JSON object required")
            return v
        except Exception as e: raise ValueError("Invalid JSON body: "+str(e))
    def do_GET(self):
        u=urlparse(self.path); q=parse_qs(u.query); port=self.server.server_port
        if port==DASH_PORT:
            if u.path=="/": return self.send_html(DASH_PAGE)
            if u.path=="/api/status": return self.send_json(200,public_status())
            if u.path=="/api/audit":
                with LOCK: return self.send_json(200,{"events":list(STATE["events"])})
            return self.send_json(404,{"error":"Not found on monitor"})
        if u.path=="/": return self.send_html(TARGET_PAGE)
        if u.path=="/api/status": return self.send_json(200,public_status())
        if u.path=="/api/records":
            role=q.get("as",["guest"])[0][:40]
            with LOCK:
                protected=STATE["defense_enabled"]
                if protected and role not in ("admin","auditor"):
                    event(role,"records.read","BLOCKED","Authorization control denied private record access.")
                    return self.send_json(403,{"ok":False,"error":"Forbidden: private records require admin or auditor role","records":[]})
                rows=[dict(r) for r in STATE["records"]]
                event(role,"records.read","SUCCESS",f"Vulnerable mode returned {len(rows)} synthetic records including private notes." if not protected else f"Authorized role {role} read {len(rows)} synthetic records.")
                return self.send_json(200,{"ok":True,"records":rows,"defense_enabled":protected})
        return self.send_json(404,{"error":"Not found"})
    def do_POST(self):
        u=urlparse(self.path); port=self.server.server_port
        try: data=self.read_json()
        except ValueError as e: return self.send_json(400,{"error":str(e)})
        if port==DASH_PORT:
            if u.path=="/api/defense/toggle":
                with LOCK: STATE["defense_enabled"]=not STATE["defense_enabled"]; enabled=STATE["defense_enabled"]
                event("operator","defense.toggle","SUCCESS",f"Target server-side defenses {'enabled' if enabled else 'disabled'} by local operator.")
                return self.send_json(200,{"ok":True,"defense_enabled":enabled})
            if u.path=="/api/reset":
                with LOCK: STATE.clear(); STATE.update(fresh_state())
                print("[AUDIT] Lab state reset by operator; audit log cleared.",flush=True)
                return self.send_json(200,{"ok":True,"message":"Lab reset"})
            return self.send_json(404,{"error":"Not found on monitor"})
        if u.path=="/api/profile/update":
            actor=str(data.get("actor","guest"))[:40]; rid=data.get("record_id"); note=str(data.get("private_note",""))[:160]
            with LOCK:
                row=next((x for x in STATE["records"] if x["id"]==rid),None)
                if row is None: return self.send_json(404,{"ok":False,"error":"Synthetic record not found"})
                if STATE["defense_enabled"] and actor!=row["owner"] and actor!="admin":
                    event(actor,"profile.update","BLOCKED",f"Ownership check blocked update to record {rid}.")
                    return self.send_json(403,{"ok":False,"error":"Forbidden: record ownership required"})
                row["private_note"]=note; event(actor,"profile.update","SUCCESS",f"Synthetic record {rid} updated; owner={row['owner']}; defense={STATE['defense_enabled']}.")
                return self.send_json(200,{"ok":True,"record":dict(row),"message":"Synthetic record updated"})
        if u.path=="/api/login":
            actor=str(data.get("username","guest"))[:40]; token=str(data.get("demo_token",""))[:80]
            with LOCK:
                if STATE["defense_enabled"]:
                    if data.get("password")=="LabOnly-2026!":
                        session="lab-session-"+actor; STATE["sessions"][session]={"username":actor,"role":"admin" if actor=="admin" else "user"}; event(actor,"login","SUCCESS","Training credentials accepted; synthetic session issued.")
                        return self.send_json(200,{"ok":True,"session":session,"role":STATE["sessions"][session]["role"]})
                    event(actor,"login","BLOCKED","Defended demo login rejected client-supplied identity claim or invalid training credentials.")
                    return self.send_json(401,{"ok":False,"error":"Invalid training credentials"})
                if token=="admin-demo-token" or data.get("password")=="LabOnly-2026!":
                    session="lab-session-"+actor; STATE["sessions"][session]={"username":actor,"role":"admin" if token=="admin-demo-token" or actor=="admin" else "user"}; event(actor,"login","SUCCESS","Vulnerable demo accepted a client-supplied identity claim; synthetic session issued.")
                    return self.send_json(200,{"ok":True,"session":session,"role":STATE["sessions"][session]["role"],"warning":"Vulnerable demo behavior"})
                event(actor,"login","BLOCKED","Login rejected invalid training credentials."); return self.send_json(401,{"ok":False,"error":"Invalid training credentials"})
        if u.path=="/api/admin/action":
            actor=str(data.get("actor","guest"))[:40]; action=str(data.get("action",""))[:80]
            with LOCK:
                if STATE["defense_enabled"] and actor!="admin":
                    event(actor,"admin.action","BLOCKED",f"Role check denied restricted action '{action}'."); return self.send_json(403,{"ok":False,"error":"Forbidden: administrator role required"})
                STATE["app_flag"]="CHANGED_BY_"+(actor.upper().replace(" ","_")[:24] or "GUEST"); event(actor,"admin.action","SUCCESS",f"Synthetic restricted action '{action}' accepted; app flag changed.")
                return self.send_json(200,{"ok":True,"app_flag":STATE["app_flag"],"message":"Synthetic application flag changed"})
        return self.send_json(404,{"error":"Not found"})

def main():
    print("\nAI Security Live Lab — two-site version",flush=True)
    print(f"COMPANY TARGET : http://{HOST}:{TARGET_PORT}",flush=True)
    print(f"SOC DASHBOARD  : http://{HOST}:{DASH_PORT}",flush=True)
    print("Idle startup: no records are read and no audit events are generated by opening either page.",flush=True)
    print("Only explicit target API requests create audit events. Ctrl+C stops both sites.\n",flush=True)
    servers=[ThreadingHTTPServer((HOST,DASH_PORT),Handler),ThreadingHTTPServer((HOST,TARGET_PORT),Handler)]
    threads=[]
    for server in servers:
        t=threading.Thread(target=server.serve_forever,daemon=True); t.start(); threads.append(t)
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping both local sites...",flush=True)
        for server in servers: server.shutdown(); server.server_close()
if __name__=="__main__": main()
