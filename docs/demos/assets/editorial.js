/* pokerbots · editorial-style helpers: two-column experiments, theme toggle, math notes */
(function(){
  var d=document,root=d.documentElement;
  window.LAB={cv:function(n){return getComputedStyle(root).getPropertyValue(n).trim()}};
  try{var s=localStorage.getItem('lab-theme');if(s)root.dataset.theme=s}catch(e){}
  var dark=function(){return root.dataset.theme?root.dataset.theme==='dark':matchMedia('(prefers-color-scheme:dark)').matches};
  var SUN='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
      MOON='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
  d.addEventListener('DOMContentLoaded',function(){
    d.querySelectorAll('main > section').forEach(function(sec){
      var h=sec.querySelector(':scope > h2');if(!h)return;
      var m=h.textContent.match(/^\s*(\d+)\.\s*(.*)$/),label;
      if(m){label='Experiment 0'+m[1];h.textContent=m[2]}
      else if(/self-check/i.test(h.textContent))label='Check yourself';
      else{label='Stress test';sec.classList.add('break')}
      var eb=d.createElement('p');eb.className='eyebrow';eb.textContent=label;
      var side=d.createElement('div'),inner=d.createElement('div'),work=d.createElement('div');
      side.className='side';inner.className='side-in';work.className='work';
      inner.append(eb,h);
      var hasPrompt=!!sec.querySelector(':scope > .prompt'),first=true,math=null;
      [].slice.call(sec.children).forEach(function(c){
        if(c===side||c===work||c===h)return;
        if(c.classList&&c.classList.contains('prompt'))inner.appendChild(c);
        else if(c.classList&&c.classList.contains('math')){var det=d.createElement('details');det.className='math-panel';det.innerHTML='<summary>Show the math</summary>';det.appendChild(c);math=det}
        else if(!hasPrompt&&first&&c.tagName==='P'&&!sec.classList.contains('break')){inner.appendChild(c)}
        else work.appendChild(c);
        first=false
      });
      if(math)inner.appendChild(math);
      side.appendChild(inner);sec.classList.add('exp');sec.append(side,work)
    });
    var main=d.querySelector('main'),btn=d.querySelector('.theme');
    var paint=function(){btn.innerHTML=dark()?SUN:MOON};paint();
    btn.onclick=function(){var x=dark()?'light':'dark';root.dataset.theme=x;try{localStorage.setItem('lab-theme',x)}catch(e){}paint();window.dispatchEvent(new Event('labtheme'))};
    if(d.body.dataset.prov){var ft=d.createElement('footer');ft.className='foot';ft.innerHTML='<b>Where these numbers come from.</b> ';ft.appendChild(d.createTextNode(d.body.dataset.prov));main.appendChild(ft)}
  });
})();
