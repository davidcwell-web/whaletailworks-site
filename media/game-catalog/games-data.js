/* Add a game here to create its catalog row, popup and availability count.
 * Prices are USD. Set status to 'available' only when its store listing is live.
 * Artwork is promotional; screenshots below are actual game captures.
 */
window.WTW_GAME_CATALOG = [
  {
    id: 'xenodex', title: 'XENODEX', genre: 'Sci-fi strategy', status: 'available',
    accent: '#87cdeb', price: '$2.99', priceNote: 'One-time purchase · No ads',
    summary: 'Defend Earth, uncover alien species, and discover who is running the count.',
    cover: 'img/xeno_hero.jpg', coverAlt: 'XENODEX — a lone observer beneath an alien craft',
    store: 'https://play.google.com/store/apps/details?id=net.whaletailworks.xenodex',
    paragraphs: [
      'Earth is being counted. Command A.E.G.I.S. field agents, catalogue 18 alien species across 13 worlds, defend your base, and uncover who — or what — is running the count.'
    ],
    features: [
      '18 species, each with a dossier, a fleet commander and a craft of its own.',
      '26 field operations — chases, sieges, stakeouts, deductions and first contact.',
      'Not every species is an enemy: some you answer, some you trade with.',
      'Craft lighting built from real first-hand encounter reports.',
      'Premium: $2.99 USD once — no ads, ever.'
    ],
    screenshots: [
      {src:'img/xeno_shot_globe.jpg',caption:'Orbital command'},
      {src:'img/xeno_shot_hull.jpg',caption:'Hull Run'},
      {src:'img/xeno_shot_trench.jpg',caption:'Crossfire Alley'},
      {src:'img/xeno_shot_stalker.jpg',caption:'Dead Still'},
      {src:'img/xeno_shot_lattice.jpg',caption:'Common Ground'},
      {src:'img/xeno_shot_dex.jpg',caption:'The dossier'},
      {src:'img/xeno_shot_file.jpg',caption:'Species file'}
    ],
    videos: [
      {id:'CyElBPor1bs',title:'Gameplay trailer',poster:'img/xeno_shot_hull.jpg'},
      {id:'8JpWppoVjAU',title:'Hull Run',poster:'media/game-catalog/xenodex-hull-run-short.jpg',short:true},
      {id:'aYksZG8_XV4',title:'Base Defense',poster:'media/game-catalog/xenodex-base-defense-short.jpg',short:true}
    ],
    preview: {src:'media/gameplay-loop.mp4',poster:'img/xeno_shot_hull.jpg'},
    privacy: 'privacy.html'
  },
  {
    id: 'greenwood', title: 'The Greenwood Way', genre: 'Story & strategy', status: 'available',
    accent: '#b7d9a4', price: '$3.99', priceNote: 'One-time purchase · No ads',
    summary: 'Eight unlikely heroes. A forest worth saving. An adventure with a little mischief.',
    cover: 'media/game-catalog/greenwood-cover.webp', containCover: true,
    coverAlt: 'The Greenwood Way — its carved emerald banner among forest, sea and mountains',
    store: 'https://play.google.com/store/apps/details?id=net.whaletailworks.greenwood',
    paragraphs: [
      'Eight unlikely heroes, one dying forest, and a very opinionated toad. Isometric battles with real verticality, telegraphed enemies, campfire banter — and a villain who only wanted to be remembered.',
      'Three acts across wildland, drowned sea and frozen peaks · a storm that buries the board while you fight · mercy you can choose, and an ending that remembers every time you did.',
      'Guardians join the company as you meet them on the road, each arriving in an animated scene of their own. A 21-mission campaign, played in six languages.'
    ],
    features: ['Plays fully offline.','No ads, ever.','No in-app purchases.','Collects no data.'],
    heroes: [
      {src:'img/gw_reg.png',name:'Sir Reginald'},{src:'img/gw_elowen.png',name:'Elowen'},
      {src:'img/gw_barnaby.png',name:'Barnaby'},{src:'img/gw_mabs.png',name:'Mabs'},
      {src:'img/gw_sylvai.png',name:'Sylvai'},{src:'img/gw_gruni.png',name:'Gruni'},
      {src:'img/gw_torvald.png',name:'Torvald'},{src:'img/gw_pip.png',name:'Pip'}
    ],
    screenshots: [
      {src:'media/greenwood-trailer.jpg',caption:'Choose your next move'},
      {src:'img/gw_shot_camp.jpg',caption:'Camp in the Emberdeep'},
      {src:'img/gw_shot_cut.jpg',caption:'The company before Nocturne'},
      {src:'img/gw_shot_sea.jpg',caption:'The Sundered Sea'},
      {src:'img/gw_shot_wyrm.jpg',caption:"The Old Wyrm’s terraces"}
    ],
    videos: [
      {id:'CvNTH8N5w3M',title:'Gameplay trailer',poster:'media/greenwood-trailer.jpg'},
      {id:'FMc9mh3uJ_U',title:'Battles',poster:'media/greenwood-battles.jpg',short:true}
    ],
    privacy: 'greenwood-privacy.html'
  },
  {
    id: 'reef-currents', title: 'Reef Currents', genre: 'Cozy underwater puzzle', status: 'coming-soon',
    accent: '#99e0e8', price: 'Free at launch',
    priceNote: 'Optional $1.99: remove ads + play offline',
    summary: 'Turn the stones, guide the water, and bring a quiet corner of the ocean to life.',
    cover: 'media/game-catalog/reef-cover.webp',
    coverAlt: 'Reef Currents — a manta ray gliding over a sunlit coral garden',
    paragraphs: [
      'Turn the channel stones, guide a fresh current from the inlet to every anemone, then release it and watch the reef come alive. No timer, no lives, no move limit. Hints and undo are always free.',
      'Thirty hand-set boards across six reef gardens, then an endless reef that keeps growing. Meet shells, crabs, kelp and small fish, with a shark, an octopus or a whale’s fin passing the edge now and then. A journal fills as you meet them.',
      'Classical music rendered for the game — Bach, Pachelbel and an original pavane — and a turn sound that climbs a little scale as you play.'
    ],
    features: [
      'Planned for launch: free play needs a connection; offline play comes with the purchase.',
      'Ads between boards, never during one.',
      'Non-personalised ads, suitable for children.',
      'One $1.99 purchase removes ads for good and unlocks offline play.'
    ],
    screenshots: [
      {src:'img/reef_shot_board.jpg',caption:'Guide the current'},
      {src:'img/reef_shot_complete.jpg',caption:'A little life returns'},
      {src:'img/reef_shot_map.jpg',caption:'Your little reef'}
    ],
    privacy: 'reef-currents-privacy.html'
  }
];
