// Tiny progressive enhancement: mobile menu + story search. No cookies, no tracking, no external requests.
(function () {
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
  var q = document.getElementById('q'), grid = document.getElementById('grid'), nores = document.getElementById('nores');
  if (q && grid) {
    var norm = function (s) { return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, ''); };
    var cards = Array.prototype.slice.call(grid.querySelectorAll('.card'));
    q.addEventListener('input', function () {
      var v = norm(q.value.trim()), shown = 0;
      cards.forEach(function (c) {
        var hit = !v || norm(c.getAttribute('data-search') || '').indexOf(v) !== -1;
        c.hidden = !hit; if (hit) shown++;
      });
      if (nores) nores.hidden = shown !== 0;
    });
  }
})();
