/* theme.js — light/dark theme with localStorage persistence.
   Load in <head> (no defer) so the saved theme is applied before first paint. */
(function () {
  var KEY = "theme";
  var root = document.documentElement;

  function systemTheme() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  function saved() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function current() { return root.getAttribute("data-theme") || systemTheme(); }

  var initial = saved();
  if (initial === "dark" || initial === "light") root.setAttribute("data-theme", initial);

  function updateButtons() {
    var isDark = current() === "dark";
    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      btn.setAttribute("aria-label", isDark ? "Switch to light theme" : "Switch to dark theme");
      btn.setAttribute("aria-pressed", String(isDark));
      var label = btn.querySelector("[data-theme-label]");
      if (label) label.textContent = isDark ? "Light" : "Dark";
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    updateButtons();
    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var next = current() === "dark" ? "light" : "dark";
        root.setAttribute("data-theme", next);
        try { localStorage.setItem(KEY, next); } catch (e) {}
        updateButtons();
      });
    });
  });
})();
