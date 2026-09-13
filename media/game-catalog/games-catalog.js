/* Catalog rows and native dialogs. No tracking, accounts, storage or network fetch.
   A new entry in games-data.js supplies its row, detail popup and filter counts. */
(() => {
  'use strict';
  const root=document.getElementById('games');
  const list=document.getElementById('game-catalog-list');
  const dialog=document.getElementById('game-dialog');
  const content=document.getElementById('game-dialog-content');
  const closeButton=document.getElementById('game-dialog-close');
  if(!root||!list||!dialog||!content||!closeButton)return;
  const games=Array.isArray(window.WTW_GAME_CATALOG)?window.WTW_GAME_CATALOG:[];
  const escape=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const availability=g=>g.status==='available'?'Available now':'Coming soon';
  const gameHash=g=>'#game-'+g.id;
  let opener=null,activeGame=null,locked=null,backdropDown=false,pendingBack=false,activeFilter='all',stopPreview=()=>{},pausePreview=()=>{};
  function selectedGame(){return games.find(g=>gameHash(g)===location.hash);}

  list.innerHTML=games.map(g=>`<article class="catalog-row" data-catalog-game="${escape(g.id)}" data-status="${escape(g.status)}" style="--game-accent:${escape(g.accent)}"><div class="catalog-cover ${g.containCover?'contain':''}"><img src="${escape(g.cover)}" alt="${escape(g.coverAlt)}" loading="lazy" decoding="async"><span class="catalog-status ${escape(g.status)}">${availability(g).toUpperCase()}</span></div><div class="catalog-row-body"><div class="catalog-genre">${escape(g.genre)}</div><h3>${escape(g.title)}</h3><p class="catalog-summary">${escape(g.summary)}</p><div class="catalog-row-bottom"><div><div class="catalog-price">${escape(g.price)}</div><div class="catalog-price-note">${escape(g.priceNote)}</div></div><button class="catalog-explore" type="button" data-explore-game="${escape(g.id)}" aria-label="Explore ${escape(g.title)}" aria-haspopup="dialog" aria-controls="game-dialog">Explore game <span aria-hidden="true">↗</span></button></div></div></article>`).join('');
  const matches=(g,filter)=>filter==='all'||(filter==='videos'?g.videos?.length>0:g.status===filter);
  root.querySelectorAll('[data-game-count]').forEach(el=>{
    el.textContent=String(games.filter(g=>matches(g,el.dataset.gameCount)).length);
  });
  function applyFilter(filter){
    activeFilter=filter;
    root.querySelectorAll('[data-game-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.gameFilter===filter)));
    let visible=0;
    list.querySelectorAll('[data-catalog-game]').forEach(row=>{
      row.hidden=!matches(games.find(g=>g.id===row.dataset.catalogGame),filter);
      if(!row.hidden)visible++;
    });
    document.getElementById('game-filter-announcement').textContent=`${visible} ${visible===1?'game':'games'} shown.${filter==='videos'?' Explore a game to watch its videos.':''}`;
  }
  root.querySelectorAll('[data-game-filter]').forEach(button=>button.addEventListener('click',()=>{
    if(pendingBack)return;
    const filter=button.dataset.gameFilter;
    applyFilter(filter);
    if(filter==='videos')history.replaceState(null,'',location.pathname+location.search+'#videos');
    else if(location.hash==='#videos')history.replaceState(null,'',location.pathname+location.search+'#games');
  }));
  function videoPoster(v,g){
    const url='https://www.youtube.com/watch?v='+encodeURIComponent(v.id);
    const inner=`<img src="${escape(v.poster)}" alt="" loading="lazy"><span>▶ ${v.short?'Watch Short':'Watch trailer'}</span>`;
    return location.protocol==='file:'
      ?`<a class="game-modal-trailer-link" href="${url}" target="_blank" rel="noopener" aria-label="Watch ${escape(g.title)} — ${escape(v.title)} on YouTube">${inner}</a>`
      :`<button type="button" data-game-video="${escape(v.id)}" aria-label="Play ${escape(g.title)} — ${escape(v.title)}">${inner}</button>`;
  }
  function videoSection(g){
    if(!g.videos?.length)return '';
    const preview=g.preview?`<div class="game-modal-preview"><video muted loop playsinline preload="none" poster="${escape(g.preview.poster)}" src="${escape(g.preview.src)}" aria-label="${escape(g.title)} muted gameplay preview"></video><button type="button" data-preview-toggle>Play preview</button><span>Muted gameplay preview</span></div>`:'';
    return `<div class="game-modal-videos" aria-labelledby="game-videos-heading"><h3 id="game-videos-heading" tabindex="-1">Watch ${escape(g.title)}</h3><p>Trailers and short moments from the game. Choose a video to play.</p>${preview}<div class="game-modal-video-grid">${g.videos.map(v=>`<article class="game-modal-video-card ${v.short?'is-short':'is-trailer'}"><h4>${escape(v.title)} <span>${v.short?'Short':'Trailer'}</span></h4><div class="game-modal-trailer" data-video-slot="${escape(v.id)}">${videoPoster(v,g)}</div><p class="game-modal-video-link"><a href="https://www.youtube.com/watch?v=${encodeURIComponent(v.id)}" target="_blank" rel="noopener" aria-label="Watch ${escape(g.title)} — ${escape(v.title)} on YouTube">Watch on YouTube ↗</a></p></article>`).join('')}</div></div>`;
  }
  function scrollToVideos(){
    const heading=content.querySelector('#game-videos-heading');
    if(!heading)return;
    const bar=dialog.querySelector('.game-modal-topbar').offsetHeight;
    dialog.scrollTop+=heading.getBoundingClientRect().top-dialog.getBoundingClientRect().top-bar-20;
    heading.focus({preventScroll:true});
  }
  function setupPreview(){
    const v=content.querySelector('.game-modal-preview video'),button=content.querySelector('[data-preview-toggle]');
    if(!v||!button){stopPreview=()=>{};pausePreview=()=>{};return;}
    const reduced=matchMedia('(prefers-reduced-motion:reduce)');
    let userPaused=false,visible=false,stopped=false;
    const label=()=>{button.textContent=v.paused?'Play preview':'Pause preview';button.setAttribute('aria-pressed',String(!v.paused));};
    const update=()=>{
      if(!stopped&&visible&&!document.hidden&&!userPaused&&!reduced.matches&&!navigator.connection?.saveData)v.play().catch(label);
      else v.pause();
    };
    v.addEventListener('play',label);v.addEventListener('pause',label);
    button.onclick=()=>{if(v.paused){userPaused=false;v.play().catch(label);}else{userPaused=true;v.pause();}};
    const observer=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;update();},{root:dialog,threshold:.4});
    observer.observe(v);document.addEventListener('visibilitychange',update);reduced.addEventListener('change',update);
    label();
    pausePreview=()=>{userPaused=true;v.pause();};
    stopPreview=()=>{stopped=true;v.pause();observer.disconnect();document.removeEventListener('visibilitychange',update);reduced.removeEventListener('change',update);};
  }

  function populate(g){
    const action=g.status==='available'&&g.store
      ?`<a class="game-modal-store" href="${escape(g.store)}" target="_blank" rel="noopener">Get it on Google Play ↗</a>`
      :'<span class="game-modal-soon">Coming soon to Android</span>';
    const cast=g.heroes?.length?`<h3>Meet the company</h3><div class="game-modal-cast">${g.heroes.map(h=>`<figure><img src="${escape(h.src)}" alt="${escape(h.name)}" loading="lazy"><figcaption>${escape(h.name)}</figcaption></figure>`).join('')}</div>`:'';
    content.innerHTML=`<div class="game-modal-intro"><img class="game-modal-cover ${g.containCover?'contain':''}" src="${escape(g.cover)}" alt="${escape(g.coverAlt)}"><div><div class="game-modal-status">${availability(g)} · ${escape(g.genre)}</div><h2 id="game-dialog-title">${escape(g.title)}</h2><p id="game-dialog-summary">${escape(g.summary)}</p><div class="game-modal-price">${escape(g.price)}</div><div class="game-modal-price-note">${escape(g.priceNote)}</div><div class="game-modal-actions">${action}${g.videos?.length?'<button type="button" class="game-modal-watch" data-watch-videos>Watch gameplay ↓</button>':''}<a class="game-modal-privacy" href="${escape(g.privacy)}">Privacy policy</a></div></div></div><div class="game-modal-body">${g.paragraphs.map(p=>`<p>${escape(p)}</p>`).join('')}<ul class="game-modal-features">${g.features.map(f=>`<li>${escape(f)}</li>`).join('')}</ul>${videoSection(g)}${cast}<h3>Inside the game</h3><div class="game-modal-gallery">${g.screenshots.map(s=>`<figure><img src="${escape(s.src)}" alt="${escape(s.caption)}" loading="lazy" decoding="async"><figcaption>${escape(s.caption)}</figcaption></figure>`).join('')}</div>${g.status!=='available'?`<p class="game-modal-notice">${escape(g.title)} is in development. Details shown here describe the planned release.</p>`:''}</div>`;
    setupPreview();
  }
  content.addEventListener('click',event=>{
    if(event.target.closest('[data-watch-videos]')){scrollToVideos();return;}
    const button=event.target.closest('[data-game-video]');
    if(!button)return;
    const g=games.find(g=>g.id===activeGame);
    const v=g?.videos?.find(v=>v.id===button.dataset.gameVideo);
    if(!v)return;
    pausePreview();
    content.querySelectorAll('[data-video-slot]').forEach(slot=>{
      const previous=g.videos.find(v=>v.id===slot.dataset.videoSlot);
      if(slot.querySelector('iframe'))slot.innerHTML=videoPoster(previous,g);
    });
    const frame=document.createElement('iframe');
    frame.src='https://www.youtube-nocookie.com/embed/'+encodeURIComponent(v.id)+'?autoplay=1';
    frame.title=g.title+' — '+v.title;
    frame.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';
    frame.allowFullscreen=true;
    frame.referrerPolicy='strict-origin-when-cross-origin';
    button.replaceWith(frame);
    closeButton.focus({preventScroll:true});
  });
  function lockBackground(){
    if(locked)return;
    locked={overflow:document.body.style.overflow,padding:document.body.style.paddingRight,x:scrollX,y:scrollY};
    const gutter=innerWidth-document.documentElement.clientWidth;
    if(gutter>0)document.body.style.paddingRight=(parseFloat(getComputedStyle(document.body).paddingRight)+gutter)+'px';
    document.body.style.overflow='hidden';
  }
  function openGame(g,trigger,push){
    if(!g||pendingBack)return;
    if(trigger)opener=trigger;
    if(activeGame===g.id&&dialog.open)return;
    stopPreview();populate(g);activeGame=g.id;
    lockBackground();
    if(!dialog.open)dialog.showModal();
    dialog.scrollTop=0;closeButton.focus({preventScroll:true});
    if(push&&location.hash!==gameHash(g))history.pushState({wtwGameDialog:true},'',gameHash(g));
    if(activeFilter==='videos')requestAnimationFrame(scrollToVideos);
  }
  function closeUI(){
    stopPreview();
    if(dialog.open)dialog.close();
    content.replaceChildren(); // Destroy any iframe to stop its video and audio.
    activeGame=null;
    if(locked){
      const position=locked;locked=null;
      document.body.style.overflow=position.overflow;document.body.style.paddingRight=position.padding;
      const smooth=document.documentElement.style.scrollBehavior;
      document.documentElement.style.scrollBehavior='auto';
      scrollTo(position.x,position.y);
      document.documentElement.style.scrollBehavior=smooth;
    }
    if(opener?.isConnected&&!opener.closest('[hidden]'))opener.focus({preventScroll:true});
  }
  function requestClose(){
    const hasGame=!!selectedGame();
    closeUI();
    if(hasGame&&history.state?.wtwGameDialog){pendingBack=true;history.back();}
    else if(hasGame){history.replaceState(null,'',location.pathname+location.search+'#games');}
  }
  list.addEventListener('click',event=>{
    const button=event.target.closest('[data-explore-game]');
    if(button)openGame(games.find(g=>g.id===button.dataset.exploreGame),button,true);
  });
  closeButton.addEventListener('click',requestClose);
  dialog.addEventListener('cancel',event=>{event.preventDefault();requestClose();});
  dialog.addEventListener('keydown',event=>{
    if(event.key!=='Tab')return;
    const stops=[...dialog.querySelectorAll('button:not([disabled]),a[href],iframe')].filter(el=>el.getClientRects().length);
    const first=stops[0],last=stops[stops.length-1];
    if(event.shiftKey&&document.activeElement===first){event.preventDefault();last?.focus();}
    else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first?.focus();}
  });
  function outside(event){const r=dialog.getBoundingClientRect();return event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom;}
  dialog.addEventListener('pointerdown',event=>{backdropDown=event.target===dialog&&outside(event);});
  dialog.addEventListener('pointerup',event=>{if(backdropDown&&event.target===dialog&&outside(event))requestClose();backdropDown=false;});
  dialog.addEventListener('close',()=>{if(!dialog.open&&locked)closeUI();});
  function syncLocation(){
    const returning=pendingBack||dialog.open;
    pendingBack=false;
    const game=selectedGame();
    if(game)openGame(game,null,false);
    else{
      if(dialog.open)closeUI();
      if(location.hash==='#videos')applyFilter('videos');
      else if(location.hash==='#games'&&activeFilter==='videos')applyFilter('all');
      // Fragment history restoration runs after popstate; return focus after it.
      if(returning)requestAnimationFrame(()=>{if(!dialog.open&&opener?.isConnected&&!opener.closest('[hidden]'))opener.focus({preventScroll:true});});
    }
  }
  document.querySelectorAll('nav a[href="#videos"]').forEach(a=>a.addEventListener('click',()=>applyFilter('videos')));
  document.querySelectorAll('nav a[href="#games"]').forEach(a=>a.addEventListener('click',()=>applyFilter('all')));
  addEventListener('popstate',syncLocation);
  addEventListener('hashchange',syncLocation);
  syncLocation();
})();
