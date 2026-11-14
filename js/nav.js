/* nav.js — collapsible sidebar for screens below 1024px (keyboard accessible) */
document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector("[data-nav-toggle]");
  var sidebar = document.getElementById("sidebar");
  var overlay = document.querySelector(".sidebar-overlay");
  if (!toggle || !sidebar) return;

  var mq = window.matchMedia("(min-width: 1024px)");

  function setOpen(open) {
    sidebar.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    if (overlay) overlay.hidden = !open;
    if (open) {
      var first = sidebar.querySelector("a, button");
      if (first) first.focus();
    }
  }

  toggle.addEventListener("click", function () {
    setOpen(toggle.getAttribute("aria-expanded") !== "true");
  });
  if (overlay) overlay.addEventListener("click", function () { setOpen(false); toggle.focus(); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && sidebar.classList.contains("is-open") && !mq.matches) {
      setOpen(false); toggle.focus();
    }
  });
  var onChange = function () { if (mq.matches) { sidebar.classList.remove("is-open"); toggle.setAttribute("aria-expanded", "false"); if (overlay) overlay.hidden = true; } };
  if (mq.addEventListener) mq.addEventListener("change", onChange); else mq.addListener(onChange);
});
