// Table test for assets/lang-detect.js. Run: node scripts/test_detect.js
const detect = require('../assets/lang-detect.js');
const assert = require('assert');
const codes = ['en', 'fr', 'es', 'de', 'ar', 'zh', 'it', 'hi', 'tl'];
const t = (saved, search, prefs) => detect(saved, search, prefs, codes);
const cases = [
  [[null, '', ['fr-CA']], { target: 'fr', save: null }],
  [[null, '', ['zh-TW']], { target: 'zh', save: null }],
  [[null, '', ['fil']], { target: 'tl', save: null }],
  [[null, '', ['tl']], { target: 'tl', save: null }],
  [[null, '', ['pt-BR']], { target: null, save: null }],
  [[null, '', ['pt', 'de']], { target: 'de', save: null }],
  [['es', '', ['fr']], { target: 'es', save: null }],
  [['en', '', ['fr']], { target: 'en', save: null }],
  [[null, '?lang=en', ['fr']], { target: 'en', save: 'en' }],
  [['de', '?lang=fr', ['it']], { target: 'fr', save: 'fr' }],
  [['xx', '', ['it']], { target: 'it', save: null }],
  [[null, '?lang=xx', []], { target: null, save: null }],
  [[null, '', []], { target: null, save: null }],
  [[null, '', undefined], { target: null, save: null }],
];
cases.forEach(([args, want]) => assert.deepStrictEqual(t(...args), want, JSON.stringify(args)));
console.log('lang-detect ok (' + cases.length + ' cases)');
