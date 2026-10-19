/* Language control behaviour. The menu is a <details> of real links, so it works without this file; this adds
   Escape / outside click / arrow keys, remembers the choice, keeps the #hash and sets the footer year. */
(function () {
  var KEY = 'lumoxia.lang';
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  var menu = document.querySelector('[data-lang-menu]');
  if (!menu) return;
  var button = menu.querySelector('summary');
  var links = Array.prototype.slice.call(menu.querySelectorAll('a[data-lang]'));

  function close(refocus) {
    menu.removeAttribute('open');
    if (refocus) button.focus();
  }

  document.addEventListener('click', function (e) {
    if (menu.hasAttribute('open') && !menu.contains(e.target)) close(false);
  });
  menu.addEventListener('focusout', function (e) {
    if (menu.hasAttribute('open') && e.relatedTarget && !menu.contains(e.relatedTarget)) close(false);
  });
  menu.addEventListener('toggle', function () {
    if (menu.hasAttribute('open') && links.length) {
      var current = menu.querySelector('[aria-current]') || links[0];
      current.focus();
    }
  });
  menu.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && menu.hasAttribute('open')) {
      e.preventDefault();
      close(true);
      return;
    }
    var i = links.indexOf(document.activeElement);
    var next = null;
    if (e.key === 'ArrowDown') next = links[(i + 1) % links.length];
    else if (e.key === 'ArrowUp') next = links[(i - 1 + links.length) % links.length];
    else if (e.key === 'Home' && i > -1) next = links[0];
    else if (e.key === 'End' && i > -1) next = links[links.length - 1];
    if (next && menu.hasAttribute('open')) {
      e.preventDefault();
      next.focus();
    }
  });

  links.forEach(function (a) {
    a.addEventListener('click', function () {
      try { localStorage.setItem(KEY, a.getAttribute('data-lang')); } catch (e) { /* storage blocked: the link still works */ }
      if (location.hash && a.href.indexOf('#') < 0) a.href += location.hash;
    });
  });
})();
