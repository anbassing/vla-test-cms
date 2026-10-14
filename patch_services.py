from pathlib import Path
import re, shutil, zipfile, os

root=Path('/mnt/data/vlwork')

services=[
('01','Market Entry','Market Entry & Feasibility','Understand where, how, and with what vehicle to enter Indonesia. We clarify complex BKPM investment regulations, competitive positioning, and consumer segmentation.',
 ['Competitive Landscape & Pricing Audits','Regulatory Roadmaps & OSS/BKPM Structuring','Addressable Market Sizing Across Provinces'],'Explore Market Entry','query_stats','market-entry'),
('02','Partnering','Business & Partner Matching','Locate the right counterparties to drive your commercial goals without reliance on cold introductions or unvetted commercial intermediaries.',
 ['Distributor & Wholesaler Screening (Java/Sumatra)','Joint-Venture & Concession Alignment','Curated C-Suite Executive Introductions'],'Find Local Partners','hub','partnering'),
('03','Verification','Due Diligence & Verification','Know who you are dealing with before committing capital. We conduct legal checks and on-site physical audits of Indonesian companies.',
 ['Ministry of Law (AHU) Corporate Records','On-Site Physical Asset & Inventory Audits','Reputation, Litigation, and Sanction Checks'],'Request Due Diligence','verified_user','verification'),
('04','Procurement','Sourcing & Procurement','Direct connection to Indonesia’s raw materials, textiles, master timber craft, botanical ingredients, and contract manufacturing facilities.',
 ['Tier-1 & Tier-2 Producer Identification','Sampling Quality Control & Lab Verification','Export Readiness & Certification Clearance'],'Find Suppliers','inventory_2','procurement'),
('05','Operations','Local Operations Support','Your extended ground team. Dedicated in-country project managers who represent your brand across administrative, legal, and operational meetings.',
 ['Bilingual Negotiation & Meeting Interpretation','Production Monitoring & Milestone Sign-offs','Business Travel Concierge & Industrial Escorts'],'Get Local Support','support_agent','operations'),
('06','Intelligence','Bespoke Business Intelligence','Actionable, discreet briefings on changing policies, trade tariff movements, upcoming tenders, and local market trends before they reach public wires.',
 ['Quarterly Sectoral & Policy Briefings','Domestic Supply Chain Bottleneck Early Warnings','Proprietary Local Market Sentiment Indexes'],'Request Intelligence','query_stats','intelligence'),
]

def esc(s):
    return (s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;'))

def home_cards():
    cards=[]
    for n,tag,title,desc,bullets,cta,icon,key in services:
        li=''.join(f'''<li class="flex items-start gap-2.5"><span class="material-symbols-outlined notranslate text-secondary text-base shrink-0 mt-0.5" translate="no">check_circle</span><span><strong>{esc(b.split(' ')[0])}</strong>{(' ' + ' '.join(b.split(' ')[1:])) if False else ''}</span></li>''' for b in [])
        # For home cards, preserve supplied bullet wording exactly (without inventing a bold split).
        li=''.join(f'''<li class="flex items-start gap-2.5"><span class="material-symbols-outlined notranslate text-secondary text-base shrink-0 mt-0.5" translate="no">check_circle</span><span>{esc(b)}</span></li>''' for b in bullets)
        cards.append(f'''<div class="business-service-card bg-surface-container-high text-primary rounded-xl p-8 space-y-6 shadow-lg cursor-pointer hover:shadow-xl hover:-translate-y-0.5 transition-all duration-300" role="button" tabindex="0" onclick="openBusinessServiceModal('{key}')" onkeydown="if(event.key==='Enter'||event.key===' '){{event.preventDefault();openBusinessServiceModal('{key}')}}">
<div class="flex items-center justify-between"><span class="font-label-sm text-label-sm uppercase tracking-widest text-secondary font-bold">Cluster {n}</span><span class="material-symbols-outlined notranslate text-secondary text-2xl" translate="no">{icon}</span></div>
<div><span class="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant">{tag}</span><h3 class="font-headline-md text-headline-md font-semibold mt-1">{esc(title)}</h3></div>
<p class="font-body-md text-body-md text-on-surface-variant leading-relaxed">{esc(desc)}</p>
<ul class="space-y-3 font-body-md text-body-md text-on-surface">{li}</ul>
<div class="pt-2"><button type="button" onclick="event.stopPropagation();openBusinessServiceModal('{key}')" class="inline-flex items-center gap-2 font-label-md text-label-md text-primary font-bold uppercase tracking-wider hover:text-secondary transition-colors"><span>{esc(cta)}</span><span class="material-symbols-outlined notranslate text-base" translate="no">arrow_forward</span></button></div>
</div>''')
    return '\n'.join(cards)

modal='''
<!-- Business Advisory Service Detail Modal -->
<div id="business-service-modal" class="fixed inset-0 z-[10000] hidden items-center justify-center bg-primary/70 backdrop-blur-sm p-4 overflow-y-auto" aria-hidden="true">
  <div class="relative w-full max-w-2xl my-6 rounded-2xl bg-surface shadow-2xl overflow-hidden" style="background-color:#FAF6F0;border:1px solid #E0D4C3;">
    <button type="button" onclick="closeBusinessServiceModal()" aria-label="Close" style="position:absolute;top:14px;right:14px;z-index:20;width:42px;height:42px;border-radius:9999px;display:flex;align-items:center;justify-content:center;background:#fff;color:#050040;border:1px solid #E0D4C3;box-shadow:0 4px 12px rgba(0,0,0,.12);cursor:pointer;font-size:28px;line-height:1;">×</button>
    <div class="p-7 md:p-9 space-y-6 max-h-[85vh] overflow-y-auto">
      <div class="space-y-2 pr-12">
        <div class="flex items-center gap-3"><span id="business-service-number" class="font-display-lg text-2xl text-tertiary"></span><span id="business-service-category" class="px-2.5 py-1 rounded-full bg-surface-container-high text-[11px] font-label-md text-primary uppercase"></span></div>
        <h3 id="business-service-title" class="font-display-lg text-3xl md:text-4xl text-primary"></h3>
        <p id="business-service-description" class="text-sm md:text-base text-on-surface-variant leading-relaxed"></p>
      </div>
      <div class="rounded-2xl p-5 md:p-6" style="background:#F3EDE4;border:1px solid #E0D4C3;">
        <h4 class="font-label-md text-label-md uppercase tracking-wider text-primary font-bold mb-4">What this service covers</h4>
        <ul id="business-service-bullets" class="space-y-3 text-sm text-on-surface"></ul>
      </div>
      <div class="rounded-xl p-4" style="background:#F8F4EC;border:1px solid #E5DCCE;">
        <p class="text-sm text-on-surface-variant leading-relaxed"><strong class="text-primary">How to proceed:</strong> Tell us what you need, and the Visit Locals advisory team can continue through the confidential inquiry form or directly through WhatsApp.</p>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
        <button id="business-service-form-cta" type="button" class="inline-flex items-center justify-center gap-2 bg-primary hover:bg-primary-container text-on-primary font-label-md text-label-md uppercase tracking-wider px-5 py-3.5 rounded-lg shadow-md transition-all" onclick="continueBusinessServiceToForm()"><span>Request via Form</span><span class="material-symbols-outlined notranslate text-base" translate="no">arrow_forward</span></button>
        <button id="business-service-wa-cta" type="button" class="inline-flex items-center justify-center gap-2 bg-secondary hover:bg-secondary-container text-on-secondary font-label-md text-label-md uppercase tracking-wider px-5 py-3.5 rounded-lg transition-all" onclick="openBusinessServiceWhatsApp('Wafi')"><span class="material-symbols-outlined notranslate text-base" translate="no">chat</span><span>WhatsApp Wafi</span></button>
      </div>
      <button type="button" class="w-full text-xs uppercase tracking-wider text-on-surface-variant hover:text-primary py-1" onclick="openBusinessServiceWhatsApp('Safirah')">Prefer tourism / local coordination? WhatsApp Safirah →</button>
    </div>
  </div>
</div>
'''

js='''
<script id="vl-business-service-modal-script">
(function(){
  const SERVICES = {
    'market-entry': {number:'01', category:'Market Entry', title:'Market Entry & Feasibility', description:'Understand where, how, and with what vehicle to enter Indonesia. We clarify complex BKPM investment regulations, competitive positioning, and consumer segmentation.', bullets:['Competitive Landscape & Pricing Audits','Regulatory Roadmaps & OSS/BKPM Structuring','Addressable Market Sizing Across Provinces']},
    'partnering': {number:'02', category:'Partnering', title:'Business & Partner Matching', description:'Locate the right counterparties to drive your commercial goals without reliance on cold introductions or unvetted commercial intermediaries.', bullets:['Distributor & Wholesaler Screening (Java/Sumatra)','Joint-Venture & Concession Alignment','Curated C-Suite Executive Introductions']},
    'verification': {number:'03', category:'Verification', title:'Due Diligence & Verification', description:'Know who you are dealing with before committing capital. We conduct legal checks and on-site physical audits of Indonesian companies.', bullets:['Ministry of Law (AHU) Corporate Records','On-Site Physical Asset & Inventory Audits','Reputation, Litigation, and Sanction Checks']},
    'procurement': {number:'04', category:'Procurement', title:'Sourcing & Procurement', description:'Direct connection to Indonesia’s raw materials, textiles, master timber craft, botanical ingredients, and contract manufacturing facilities.', bullets:['Tier-1 & Tier-2 Producer Identification','Sampling Quality Control & Lab Verification','Export Readiness & Certification Clearance']},
    'operations': {number:'05', category:'Operations', title:'Local Operations Support', description:'Your extended ground team. Dedicated in-country project managers who represent your brand across administrative, legal, and operational meetings.', bullets:['Bilingual Negotiation & Meeting Interpretation','Production Monitoring & Milestone Sign-offs','Business Travel Concierge & Industrial Escorts']},
    'intelligence': {number:'06', category:'Intelligence', title:'Bespoke Business Intelligence', description:'Actionable, discreet briefings on changing policies, trade tariff movements, upcoming tenders, and local market trends before they reach public wires.', bullets:['Quarterly Sectoral & Policy Briefings','Domestic Supply Chain Bottleneck Early Warnings','Proprietary Local Market Sentiment Indexes']}
  };
  let activeKey='market-entry';
  window.openBusinessServiceModal=function(key){
    const data=SERVICES[key]; if(!data) return; activeKey=key;
    document.getElementById('business-service-number').textContent=data.number;
    document.getElementById('business-service-category').textContent=data.category;
    document.getElementById('business-service-title').textContent=data.title;
    document.getElementById('business-service-description').textContent=data.description;
    document.getElementById('business-service-bullets').innerHTML=data.bullets.map(b=>'<li class="flex items-start gap-2.5"><span class="material-symbols-outlined notranslate text-secondary text-base mt-0.5" translate="no">check_circle</span><span>'+b+'</span></li>').join('');
    const m=document.getElementById('business-service-modal');
    m.classList.remove('hidden'); m.classList.add('flex'); m.setAttribute('aria-hidden','false'); document.body.classList.add('overflow-hidden');
  };
  window.closeBusinessServiceModal=function(){const m=document.getElementById('business-service-modal'); if(!m)return; m.classList.add('hidden');m.classList.remove('flex');m.setAttribute('aria-hidden','true');document.body.classList.remove('overflow-hidden');};
  window.continueBusinessServiceToForm=function(){
    const data=SERVICES[activeKey];
    closeBusinessServiceModal();
    setTimeout(function(){
      const formTarget=document.getElementById('consultation-inquiry') || document.getElementById('inquiry');
      if(document.getElementById('mode-business-btn')) { try{setInquiryMode('business');}catch(e){} }
      const select=document.getElementById('business-primary-need');
      const map={'market-entry':'market-entry','partnering':'partner-matching','verification':'due-diligence','procurement':'sourcing','operations':'business-trip','intelligence':'general-advisory'};
      if(select && map[activeKey]) select.value=map[activeKey];
      const ta=document.querySelector('#inquiry-form textarea, #businessInquiryForm textarea');
      if(ta && !ta.value.trim()) ta.value='Service requested: '+data.title+'\\n\\n';
      if(formTarget) formTarget.scrollIntoView({behavior:'smooth',block:'start'});
      else { const f=document.getElementById('businessInquiryForm'); if(f) f.scrollIntoView({behavior:'smooth'}); }
    },80);
  };
  window.openBusinessServiceWhatsApp=function(consultant){
    const data=SERVICES[activeKey];
    const number=consultant==='Safirah'?'38671776409':'6285285469417';
    const message='Hello '+consultant+', I found this service on Visit Locals and would like to discuss '+data.title+'. Please share the next steps and what information you need from me.';
    window.open('https://wa.me/'+number+'?text='+encodeURIComponent(message),'_blank','noopener,noreferrer');
  };
  document.addEventListener('click',function(e){const m=document.getElementById('business-service-modal'); if(m && e.target===m) closeBusinessServiceModal();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape') closeBusinessServiceModal();});
})();
</script>
'''

# HOME
p=root/'index.html'; s=p.read_text(errors='ignore')
start=s.find('<div class="grid grid-cols-1 md:grid-cols-2 gap-gutter">', s.find('Service Clusters'))
end=s.find('</div>\n</div>\n</section>', start)
if start<0 or end<0: raise RuntimeError('home cluster bounds not found')
end += len('</div>\n</div>\n</section>')
s=s[:start]+'<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-gutter">\n'+home_cards()+'\n</div>\n</div>\n</section>'+s[end:]
# insert modal before client-side interactive behaviors script, after existing quote modal markup
marker='<!-- Client-side Interactive Behaviors -->'
pos=s.find(marker)
if pos<0: raise RuntimeError('home script marker not found')
s=s[:pos]+modal+'\n'+js+'\n'+s[pos:]
p.write_text(s)

# BUSINESS
p=root/'business/index.html'; s=p.read_text(errors='ignore')
# add click handlers to six service card opening divs, based on service title nearby
for key,title in [(x[7],x[2]) for x in services]:
    pattern=r'(<div class="group bg-surface-container-low hover:bg-surface-container rounded-2xl p-8 transition-all duration-300 flex flex-col justify-between shadow-sm hover:shadow-md border border-surface-container-high/60">)'
    m=re.search(pattern,s)
    if not m: raise RuntimeError('service card not found '+key)
    # choose the first remaining card and replace sequentially by locating title after m
    idx=m.start()
    titlepos=s.find('<h3',idx)
    if titlepos<0 or s.find(title,titlepos,titlepos+500)<0:
        # find card containing title by searching all occurrences and selecting nearest preceding card
        titlepos=s.find(title)
        if titlepos<0: raise RuntimeError('title not found '+title)
        card_start=s.rfind('<div class="group bg-surface-container-low',0,titlepos)
        if card_start<0: raise RuntimeError('card start not found '+key)
        idx=card_start
    else: idx=m.start()
    # exact card opening at idx
    old='<div class="group bg-surface-container-low hover:bg-surface-container rounded-2xl p-8 transition-all duration-300 flex flex-col justify-between shadow-sm hover:shadow-md border border-surface-container-high/60">'
    new=old.replace('cursor-pointer','')[:-1]+' cursor-pointer" role="button" tabindex="0" onclick="openBusinessServiceModal(\''+key+'\')" onkeydown="if(event.key===\'Enter\'||event.key===\' \'){event.preventDefault();openBusinessServiceModal(\''+key+'\')}">'
    if s[idx:idx+len(old)]!=old:
        raise RuntimeError('unexpected card opening for '+key)
    s=s[:idx]+new+s[idx+len(old):]
    # change the card CTA's first href within this card to modal action, avoiding global replacement
    card_end=s.find('</div> <!-- Service',idx+len(new))
    if card_end<0: card_end=s.find('<!-- Service',idx+len(new))
    if card_end<0: card_end=min(len(s),idx+5000)
    segment=s[idx:card_end]
    # CTA anchor with href consultation-inquiry
    segment=segment.replace('href="#consultation-inquiry"','href="#" onclick="event.stopPropagation();openBusinessServiceModal(\''+key+'\');return false;"',1)
    s=s[:idx]+segment+s[card_end:]
# add id to primary need select
s=s.replace('<select class="w-full px-4 py-3 rounded-lg bg-surface-container-low border border-surface-container-high focus:outline-none focus:border-primary text-sm text-on-surface">\n<option value="market-entry">Market Entry &amp; Strategy</option>', '<select id="business-primary-need" class="w-full px-4 py-3 rounded-lg bg-surface-container-low border border-surface-container-high focus:outline-none focus:border-primary text-sm text-on-surface">\n<option value="market-entry">Market Entry &amp; Strategy</option>',1)
# insert modal + js before closing main/footer after existing form success modal block, before footer
marker='</main><footer'
pos=s.find(marker)
if pos<0: raise RuntimeError('business footer marker not found')
s=s[:pos]+modal+'\n'+js+'\n'+s[pos:]
p.write_text(s)
print('patched')
