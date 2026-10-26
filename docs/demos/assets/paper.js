/* pokerbots · paper-style helpers (theme, figures, footnote-style math panels) */
(function(){
  var d=document,root=d.documentElement;
  window.LAB={cv:function(n){return getComputedStyle(root).getPropertyValue(n).trim()}};
  try{var s=localStorage.getItem('lab-theme');if(s)root.dataset.theme=s}catch(e){}
  var dark=function(){return root.dataset.theme?root.dataset.theme==='dark':matchMedia('(prefers-color-scheme:dark)').matches};
  var SUN='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
      MOON='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
  d.addEventListener('DOMContentLoaded',function(){
    var fig=0;
    d.querySelectorAll('main > section').forEach(function(sec){
      var h=sec.querySelector('h2'),m=h&&h.textContent.match(/^\s*(\d+)\.\s*(.*)$/),title=h?h.textContent:'';
      if(m){h.innerHTML='<span class="num">Experiment '+m[1]+'</span><span></span>';h.lastChild.textContent=m[2];title=m[2]}
      if(h&&/^Break it/i.test(h.textContent))sec.classList.add('break');
      /* wrap everything after the prediction up to the math note into one inline figure */
      var pr=sec.querySelector(':scope > .prompt');
      if(pr){var f=d.createElement('figure');f.className='fig';f.style.margin='1.8rem 0';var n=pr.nextElementSibling;pr.after(f);
        while(n&&!(n.tagName==='P'&&n.classList.contains('math'))){var nx=n.nextElementSibling;f.appendChild(n);n=nx}
        fig++;var c=d.createElement('figcaption');c.innerHTML='<b>Figure '+fig+'.</b> ';c.appendChild(d.createTextNode(title+'. Change a control and the numbers and plot update immediately.'));f.appendChild(c)}
    });
    d.querySelectorAll('main .math').forEach(function(p){var det=d.createElement('details');det.className='math-panel';det.innerHTML='<summary>Show the math</summary>';p.parentNode.insertBefore(det,p);det.appendChild(p)});
    var main=d.querySelector('main'),top=d.querySelector('.top'),btn=top.querySelector('.theme');
    var paint=function(){btn.innerHTML=dark()?SUN:MOON};paint();
    btn.onclick=function(){var x=dark()?'light':'dark';root.dataset.theme=x;try{localStorage.setItem('lab-theme',x)}catch(e){}paint();window.dispatchEvent(new Event('labtheme'))};
    if(d.body.dataset.prov){var ft=d.createElement('footer');ft.className='foot';ft.innerHTML='<b>Where these numbers come from.</b> ';ft.appendChild(d.createTextNode(d.body.dataset.prov));main.appendChild(ft)}
  });
})();
