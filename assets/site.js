// Concept-site form handler: nothing is sent anywhere.
(function () {
  var f = document.getElementById('quote');
  if (!f) return;
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var name = f.elements.name, phone = f.elements.phone;
    if (!name.value.trim()) { name.focus(); return; }
    if (!phone.value.trim()) { phone.focus(); return; }
    document.getElementById('form-msg').classList.add('show');
    f.reset();
  });
})();
