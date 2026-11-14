/* modal.js — open/close native <dialog> modals (focus trap + Esc handled by the browser) */
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("[data-modal-open]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var dlg = document.getElementById(btn.getAttribute("data-modal-open"));
      if (dlg && dlg.showModal) dlg.showModal();
    });
  });
  document.querySelectorAll("[data-modal-close]").forEach(function (btn) {
    btn.addEventListener("click", function () { btn.closest("dialog").close(); });
  });
});
