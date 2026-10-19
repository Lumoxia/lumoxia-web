/* Which language should an English entry page show? Pure function, inlined into the head of the English pages by
   scripts/build.py (before first paint, so no English flash) and unit tested under Node.
   Returns {target, save}: `target` is a language code to show (or null), `save` a code to remember (or null). */
function lumoxiaDetect(saved, search, prefs, codes) {
  var q = /[?&]lang=([a-z]{2})(?:&|$)/.exec(search || '');
  if (q && codes.indexOf(q[1]) > -1) return { target: q[1], save: q[1] };
  if (saved && codes.indexOf(saved) > -1) return { target: saved, save: null };
  for (var i = 0; i < (prefs || []).length; i++) {
    var p = String(prefs[i]).toLowerCase().split('-')[0];
    if (p === 'fil') p = 'tl';
    if (codes.indexOf(p) > -1) return { target: p, save: null };
  }
  return { target: null, save: null };
}
if (typeof module !== 'undefined') module.exports = lumoxiaDetect;
