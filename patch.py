from pathlib import Path
import re
root=Path('/mnt/data/vlwork')
pages=['index.html','explore/index.html','business/index.html','experience/index.html','insight/index.html','partner/index.html']
# Stable header based on Insight, with neutral active states; JS sets active page.
header='''<header class="fixed top-0 w-full z-50 bg-surface/90 backdrop-blur-md shadow-[0_1px_8px_rgba(0,0,0,0.04)]"><div class="h-20 max-w-7xl mx-auto px-margin md:px-margin-md lg:px-margin-lg flex items-center justify-between"><a class="flex flex-col group" data-path="home" href="/"><span class="font-display-lg text-[22px] tracking-wide text-primary leading-tight font-medium">VISIT LOCALS</span><span class="font-label-md text-[10px] tracking-widest uppercase text-tertiary font-semibold">Gateway to Indonesia</span></a><nav class="hidden xl:flex items-center gap-space-md" data-active-classes="bg-primary-container text-on-primary font-bold rounded-lg px-space-xs py-1"><a class="font-label-md text-label-md uppercase tracking-wider text-on-surface-variant hover:text-on-surface transition-colors py-1" data-path="home" href="/">Home</a><a class="font-label-md text-label-md uppercase tracking-wider text-on-surface-variant hover:text-on-surface transition-colors py-1" data-path="explore" href="/explore/">Explore</a><a class="font-label-md text-label-md uppercase tracking-wider text-on-surface-variant hover:text-on-surface transition-colors py-1" data-path="business" href="/business/">Business</a><a class="font-label-md text-label-md uppercase tracking-wider text-on-surface-variant hover:text-on-surface transition-colors py-1" data-path="experience" href="/experience/">Experience</a><a class="font-label-md text-label-md uppercase tracking-wider text-on-surface-variant hover:text-on-surface transition-colors py-1" data-path="insight" href="/insight/">Insight</a><a class="font-label-md text-label-md uppercase tracking-wider text-on-surface-variant hover:text-on-surface transition-colors py-1" data-path="partner-with-us" href="/partner/">Partner with Us</a></nav><button aria-controls="vl-mobile-menu" aria-expanded="false" aria-label="Open menu" class="vl-mobile-menu-button" type="button"><span aria-hidden="true"></span></button><div class="flex items-center gap-space-sm"><button aria-label="Search Archive" class="p-space-xs text-on-surface-variant hover:text-primary transition-colors flex items-center justify-center" type="button"><span class="material-symbols-outlined text-xl">search</span></button><div class="relative flex items-center group vl-language"><button aria-expanded="false" aria-haspopup="true" class="vl-language-button flex items-center gap-1 font-label-md text-label-md text-on-surface-variant hover:text-primary px-space-xs py-1 transition-colors uppercase" type="button"><span class="vl-current-language">EN</span><span class="material-symbols-outlined text-base">expand_more</span></button><div aria-label="Language" class="vl-language-menu" role="menu"><button aria-current="true" class="vl-language-option" data-lang="EN" role="menuitem" type="button">EN — English</button><button class="vl-language-option" data-lang="AR" role="menuitem" type="button">AR — العربية</button><button class="vl-language-option" data-lang="TUR" role="menuitem" type="button">TUR — Türkçe</button><button class="vl-language-option" data-lang="FR" role="menuitem" type="button">FR — Français</button><button class="vl-language-option" data-lang="JP" role="menuitem" type="button">JP — 日本語</button></div></div></div></div></header>'''
# Mobile menu is outside header and shared in current build. Keep it.
for rel in pages:
    p=root/rel; s=p.read_text()
    a=s.index('<header'); b=s.index('</header>')+len('</header>')
    s=s[:a]+header+s[b:]
    if rel=='experience/index.html':
        banner=re.compile(r'<div class="bg-surface-container-high/80 text-on-surface-variant font-label-md text-label-md">.*?</div></div>', re.S)
        s=banner.sub('',s,count=1)
        s=s.replace('<main class="w-full pt-28 bg-surface">','<main class="w-full pt-20 bg-surface">',1)
    p.write_text(s)

# Replace interaction script in every page.
script=re.compile(r'<script id="vl-header-interactions">.*?</script>', re.S)
new='''<script id="vl-header-interactions">
(function () {
  const LANGS = { EN: 'en', AR: 'ar', TUR: 'tr', FR: 'fr', JP: 'ja' };
  const ROUTES = [
    ['Home','/'], ['Explore','/explore/'], ['Business','/business/'],
    ['Experience','/experience/'], ['Insight','/insight/'], ['Partner With Us','/partner/']
  ];
  function esc(s){ return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
  function init() {
    /* Match the stable Insight header active-state styling on every page. */
    const path = location.pathname.replace(/\\/+$/, '') || '/';
    document.querySelectorAll('header nav a[data-path]').forEach(a => {
      const href = new URL(a.getAttribute('href'), location.origin).pathname.replace(/\\/+$/, '') || '/';
      const active = href === path;
      a.classList.remove('bg-primary-container','text-on-primary','font-bold','rounded-lg','px-space-xs','py-1');
      if (active) {
        a.classList.add('bg-primary-container','text-on-primary','font-bold','rounded-lg','px-space-xs','py-1');
        a.setAttribute('aria-current','page');
      } else a.removeAttribute('aria-current');
    });

    /* Search: index the whole static site, not only the current page. */
    const searchButton=document.querySelector('header button[aria-label="Search Archive"]');
    const overlay=document.getElementById('vl-search-overlay');
    const input=document.getElementById('vl-search-input');
    const results=document.getElementById('vl-search-results');
    const close=document.getElementById('vl-search-close');
    let siteItems=[];
    async function buildIndex(){
      const all=[];
      for(const [label,url] of ROUTES){
        try{
          const r=await fetch(url,{credentials:'same-origin'}); if(!r.ok) continue;
          const html=await r.text();
          const doc=new DOMParser().parseFromString(html,'text/html');
          doc.querySelectorAll('main h1, main h2, main h3, main h4, main a').forEach(el=>{
            const text=(el.textContent||'').replace(/\\s+/g,' ').trim();
            if(text.length>2 && !/^(Home|Explore|Business|Experience|Insight|Partner With Us)$/i.test(text)){
              all.push({text,href:el.tagName==='A'?(el.getAttribute('href')||url):url, page:label});
            }
          });
        }catch(e){}
      }
      const seen=new Set(); siteItems=all.filter(x=>{const k=x.text+'|'+x.href;if(seen.has(k))return false;seen.add(k);return true;}).slice(0,600);
    }
    function render(q){
      const query=q.trim().toLowerCase();
      if(!query){results.innerHTML='<div class="vl-search-empty">Search destinations, experiences, businesses, insights, or topics across Visit Locals.</div>';return;}
      const matches=siteItems.filter(x=>x.text.toLowerCase().includes(query)).slice(0,30);
      results.innerHTML=matches.length?matches.map(x=>'<a class="vl-search-result" href="'+esc(x.href)+'"><strong>'+esc(x.text)+'</strong><small>'+esc(x.page)+'</small></a>').join(''):'<div class="vl-search-empty">No matching results found.</div>';
    }
    if(searchButton&&overlay&&input&&results&&close){
      const open=async()=>{overlay.classList.add('open');overlay.setAttribute('aria-hidden','false');document.body.style.overflow='hidden';input.value='';render('');input.focus();if(!siteItems.length)await buildIndex();};
      const shut=()=>{overlay.classList.remove('open');overlay.setAttribute('aria-hidden','true');document.body.style.overflow='';};
      searchButton.addEventListener('click',open); close.addEventListener('click',shut); overlay.addEventListener('click',e=>{if(e.target===overlay)shut();}); input.addEventListener('input',()=>render(input.value)); document.addEventListener('keydown',e=>{if(e.key==='Escape'&&overlay.classList.contains('open'))shut();});
    }

    /* Language: real automatic translation using Google Translate, persisted across pages. */
    const lw=document.querySelector('.vl-language'), lb=lw&&lw.querySelector('.vl-language-button'), lm=lw&&lw.querySelector('.vl-language-menu');
    if(lw&&lb&&lm){
      const opts=lw.querySelectorAll('.vl-language-option');
      const saved=localStorage.getItem('vl-language')||'EN';
      lb.querySelector('.vl-current-language').textContent=saved;
      opts.forEach(o=>o.setAttribute('aria-current',String(o.dataset.lang===saved)));
      lb.addEventListener('click',e=>{e.stopPropagation();const open=lm.classList.toggle('open');lb.setAttribute('aria-expanded',String(open));});
      document.addEventListener('click',()=>{lm.classList.remove('open');lb.setAttribute('aria-expanded','false');});
      opts.forEach(o=>o.addEventListener('click',e=>{e.stopPropagation();const lang=o.dataset.lang||'EN';localStorage.setItem('vl-language',lang);lb.querySelector('.vl-current-language').textContent=lang;opts.forEach(x=>x.setAttribute('aria-current',String(x===o)));lm.classList.remove('open');lb.setAttribute('aria-expanded','false');
        const target=LANGS[lang]||'en';
        document.cookie='googtrans=/en/'+target+';path=/';
        if(lang==='EN') document.cookie='googtrans=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';
        location.reload();
      }));
    }
    window.googleTranslateElementInit=function(){
      if(window.google&&google.translate&&google.translate.TranslateElement){
        new google.translate.TranslateElement({pageLanguage:'en',autoDisplay:false,multilanguagePage:true},'google_translate_element');
      }
    };
    if(!document.getElementById('google_translate_element')){const d=document.createElement('div');d.id='google_translate_element';d.style.cssText='position:fixed;left:-9999px;top:-9999px;width:1px;height:1px;overflow:hidden;';document.body.appendChild(d);}
    if(!document.getElementById('vl-google-translate-script')){const sc=document.createElement('script');sc.id='vl-google-translate-script';sc.src='https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';document.body.appendChild(sc);}
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
</script>'''
for rel in pages:
    p=root/rel; s=p.read_text(); s=script.sub(lambda m: new,s); p.write_text(s)
