/* -------------------------------------------------------------------
   The Beauty Cast — front-end JavaScript

   Deliberately minimal. The site works fine with JavaScript disabled;
   this only adds small conveniences.
   ------------------------------------------------------------------- */

(function () {
  "use strict";

  /* If someone clicked a package on the landing page, preselect it on
     the brand form. Reads ?package=Launch+Pack from the URL. */
  var params = new URLSearchParams(window.location.search);
  var chosen = params.get("package");
  var select = document.getElementById("package");

  if (chosen && select) {
    for (var i = 0; i < select.options.length; i++) {
      if (select.options[i].value === chosen) {
        select.selectedIndex = i;
        break;
      }
    }
  }

  /* Stop double submissions on slow connections. */
  document.querySelectorAll("form").forEach(function (form) {
    form.addEventListener("submit", function () {
      var button = form.querySelector('button[type="submit"]');
      if (button) {
        button.disabled = true;
        button.textContent = "Sending…";
      }
    });
  });
})();
