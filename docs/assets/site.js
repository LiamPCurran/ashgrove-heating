// Concept-site form handler: nothing is sent anywhere.
(function () {
  document.querySelectorAll('form.lead-form').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = f.elements.name, phone = f.elements.phone;
      if (!name.value.trim()) { name.focus(); return; }
      if (!phone.value.trim()) { phone.focus(); return; }
      f.querySelector('.form-msg').classList.add('show');
      f.reset();
    });
  });
})();
