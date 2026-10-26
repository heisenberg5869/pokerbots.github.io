/* pokerbots labs · shared enhancements. Loaded in <head>; every lab still works without it. */
(function(){
  var d=document,root=d.documentElement;
  window.LAB={cv:function(n){return getComputedStyle(root).getPropertyValue(n).trim()}};
  root.classList.add('js');
  try{if(self!==top)root.classList.add('embedded')}catch(e){root.classList.add('embedded')}
  try{var s=localStorage.getItem('lab-theme');if(s)root.dataset.theme=s}catch(e){}
  var dark=function(){return root.dataset.theme?root.dataset.theme==='dark':matchMedia('(prefers-color-scheme:dark)').matches};
  var SUN='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
      MOON='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';

  d.addEventListener('DOMContentLoaded',function(){
    var main=d.querySelector('main'),secs=[].slice.call(d.querySelectorAll('main > section'));

    /* numbered step badges, "Break it" styling, "Show the math" panels */
    secs.forEach(function(sec,i){
      var h=sec.querySelector('h2');if(!h)return;
      if(!sec.id)sec.id='s'+(i+1);
      var m=h.textContent.match(/^\s*(\d+)\.\s*(.*)$/);
      if(m){h.innerHTML='<span class="step" aria-hidden="true">'+m[1]+'</span><span></span>';h.lastChild.textContent=m[2];h.setAttribute('aria-label',m[1]+'. '+m[2]);sec.dataset.short=m[1]+' · '+m[2]}
      else{sec.dataset.short=h.textContent;if(/self-check/i.test(h.textContent)){h.innerHTML='<span class="step" aria-hidden="true">✓</span><span>Quick self-check</span>'}if(/^Break it/i.test(h.textContent)){sec.classList.add('break');h.innerHTML='<span class="step" aria-hidden="true">!</span><span>Break it</span>'}}
    });
    d.querySelectorAll('main .math').forEach(function(p){
      var det=d.createElement('details');det.className='math-panel';
      det.innerHTML='<summary>Show the math</summary>';p.parentNode.insertBefore(det,p);det.appendChild(p)
    });

    /* top bar: brand, section pills, theme toggle */
    var bar=d.createElement('nav');bar.className='topbar';bar.setAttribute('aria-label','Lab navigation');
    bar.innerHTML='<a class="brand" href="../"><i></i><span>pokerbots</span></a><div class="pills"></div><button class="theme" type="button" aria-label="Switch between light and dark theme"></button>';
    d.body.insertBefore(bar,d.body.firstChild);
    var pills=bar.querySelector('.pills'),btn=bar.querySelector('.theme');
    secs.forEach(function(sec){var a=d.createElement('a');a.href='#'+sec.id;var t=sec.dataset.short||'';if(t.length>24){t=t.slice(0,24).replace(/\s+\S*$/,'')+'…'}a.textContent=t;pills.appendChild(a)});
    var paint=function(){btn.innerHTML=dark()?SUN:MOON};paint();
    btn.onclick=function(){var next=dark()?'light':'dark';root.dataset.theme=next;try{localStorage.setItem('lab-theme',next)}catch(e){}paint();window.dispatchEvent(new Event('labtheme'))};
    matchMedia('(prefers-color-scheme:dark)').addEventListener&&matchMedia('(prefers-color-scheme:dark)').addEventListener('change',function(){paint();window.dispatchEvent(new Event('labtheme'))});

    /* provenance footer */
    if(d.body.dataset.prov&&main){var f=d.createElement('footer');f.className='foot';f.innerHTML='<b>Where these numbers come from.</b> ';f.appendChild(d.createTextNode(d.body.dataset.prov));main.appendChild(f)}

    /* reveal on scroll + scroll-spy */
    if('IntersectionObserver' in window){
      var rev=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');rev.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
      secs.forEach(function(s){s.classList.add('reveal');rev.observe(s)});
      var spy=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)[].forEach.call(pills.children,function(a){a.setAttribute('aria-current',a.getAttribute('href')==='#'+e.target.id)})})},{rootMargin:'-35% 0px -60% 0px'});
      secs.forEach(function(s){spy.observe(s)})
    }
  });
})();
