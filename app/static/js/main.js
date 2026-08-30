/* ===================================================================
   THE BEAUTY CAST — front-end JavaScript

   Four small features, no libraries:
     1. Theme toggle (light / dark, remembered between visits)
     2. Pointer parallax on the signal rings
     3. Scroll reveal
     4. 3D tilt on cards

   Everything degrades gracefully: with JavaScript off, the site is
   still fully readable and every form still works.
   =================================================================== */

(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------------------------------------------------------
     1. THEME TOGGLE
     The theme is applied in <head> before paint (see base.html) so
     there is no white flash for dark-mode visitors. This only wires
     up the button.
     --------------------------------------------------------------- */
  var toggle = document.querySelector("[data-theme-toggle]");

  if (toggle) {
    toggle.addEventListener("click", function () {
      var current = document.documentElement.getAttribute("data-theme");
      var next = current === "dark" ? "light" : "dark";

      document.documentElement.setAttribute("data-theme", next);
      toggle.setAttribute("aria-label", next === "dark" ? "Switch to light mode" : "Switch to dark mode");

      try {
        localStorage.setItem("bc-theme", next);
      } catch (e) {
        /* Private browsing blocks storage. The toggle still works,
           it just will not be remembered. */
      }
    });
  }

  /* ---------------------------------------------------------------
     2. POINTER PARALLAX
     Each ring layer has data-depth. Higher depth = moves further,
     which reads as closer to the viewer.
     --------------------------------------------------------------- */
  var ringFields = document.querySelectorAll(".rings");

  if (ringFields.length && !reduceMotion && window.matchMedia("(hover: hover)").matches) {
    var pointerX = 0, pointerY = 0, currentX = 0, currentY = 0, ticking = false;

    window.addEventListener("mousemove", function (event) {
      pointerX = (event.clientX / window.innerWidth - 0.5) * 2;   // -1 to 1
      pointerY = (event.clientY / window.innerHeight - 0.5) * 2;

      if (!ticking) {
        ticking = true;
        requestAnimationFrame(step);
      }
    });

    function step() {
      // Ease toward the pointer instead of snapping to it.
      currentX += (pointerX - currentX) * 0.06;
      currentY += (pointerY - currentY) * 0.06;

      ringFields.forEach(function (field) {
        field.querySelectorAll("[data-depth]").forEach(function (layer) {
          var depth = parseFloat(layer.getAttribute("data-depth")) || 0;
          var x = currentX * depth * 26;
          var y = currentY * depth * 26;
          layer.style.transform = "translate3d(" + x + "px," + y + "px,0)";
        });
      });

      if (Math.abs(pointerX - currentX) > 0.001 || Math.abs(pointerY - currentY) > 0.001) {
        requestAnimationFrame(step);
      } else {
        ticking = false;
      }
    }
  }

  /* ---------------------------------------------------------------
     3. SCROLL REVEAL
     --------------------------------------------------------------- */
  var revealables = document.querySelectorAll(".reveal");

  if (revealables.length) {
    if (reduceMotion || !("IntersectionObserver" in window)) {
      revealables.forEach(function (el) { el.classList.add("is-visible"); });
    } else {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);   // reveal once, then stop watching
          }
        });
      }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });

      revealables.forEach(function (el) { observer.observe(el); });
    }
  }

  /* ---------------------------------------------------------------
     4. 3D TILT ON CARDS
     Mouse only. Touch devices skip this entirely.
     --------------------------------------------------------------- */
  if (!reduceMotion && window.matchMedia("(hover: hover)").matches) {
    document.querySelectorAll(".tilt").forEach(function (card) {
      card.addEventListener("mousemove", function (event) {
        var box = card.getBoundingClientRect();
        var x = (event.clientX - box.left) / box.width - 0.5;
        var y = (event.clientY - box.top) / box.height - 0.5;

        card.style.transform =
          "perspective(900px) rotateX(" + (-y * 5).toFixed(2) + "deg) " +
          "rotateY(" + (x * 5).toFixed(2) + "deg) translateY(-4px)";
      });

      card.addEventListener("mouseleave", function () {
        card.style.transform = "";
      });
    });
  }

  /* ---------------------------------------------------------------
     5. FORM HELPERS
     Preselect a package if the visitor clicked one, and stop double
     submissions on slow connections.
     --------------------------------------------------------------- */
  var chosen = new URLSearchParams(window.location.search).get("package");
  var packageSelect = document.getElementById("package");

  if (chosen && packageSelect) {
    Array.prototype.forEach.call(packageSelect.options, function (option, index) {
      if (option.value === chosen) { packageSelect.selectedIndex = index; }
    });
  }

  document.querySelectorAll("form").forEach(function (form) {
    form.addEventListener("submit", function () {
      var button = form.querySelector('button[type="submit"]');
      if (button) {
        button.disabled = true;
        button.textContent = "Sending\u2026";
      }
    });
  });
})();
