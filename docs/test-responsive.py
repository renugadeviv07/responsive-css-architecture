"""Real-browser check: horizontal overflow, theme persistence, nav, modal. Saves screenshots."""
import pathlib, json
from playwright.sync_api import sync_playwright
root = pathlib.Path(__file__).resolve().parent.parent
url = (root / "demo.html").as_uri()
shots = root / "docs" / "screenshots"; shots.mkdir(parents=True, exist_ok=True)
JS_OVER = "()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,off:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>document.documentElement.clientWidth+1 && !e.closest('.table-wrap') && getComputedStyle(e).position!=='fixed' && !e.classList.contains('skip-link')}).map(e=>e.tagName+'.'+e.className).slice(0,5)})"
res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in [(320,700),(375,800),(768,1024),(1024,768),(1440,900)]:
        ctx = b.new_context(viewport={"width":w,"height":h}, color_scheme="light")
        pg = ctx.new_page(); pg.goto(url); pg.wait_for_timeout(300)
        r = pg.evaluate(JS_OVER)
        res[w] = {"scrollWidth":r["sw"],"clientWidth":r["cw"],"horizontal_overflow":r["sw"]>r["cw"],"offenders":r["off"]}
        names = {320:"01-mobile-320",768:"02-tablet-768",1024:"03-laptop-1024",1440:"04-desktop-1440"}
        if w in names: pg.screenshot(path=str(shots/f"{names[w]}.png"), full_page=True)
        ctx.close()
    # theme + persistence
    ctx = b.new_context(viewport={"width":1440,"height":900}, color_scheme="light")
    pg = ctx.new_page(); pg.goto(url)
    pg.screenshot(path=str(shots/"05-light-theme.png"), full_page=True)
    pg.click("[data-theme-toggle]"); pg.wait_for_timeout(600)
    t1 = pg.evaluate("document.documentElement.dataset.theme")
    label = pg.get_attribute("[data-theme-toggle]","aria-label")
    pg.screenshot(path=str(shots/"06-dark-theme.png"), full_page=True)
    pg.reload()
    t2 = pg.evaluate("document.documentElement.dataset.theme")
    res["theme"] = {"after_click":t1,"after_reload":t2,"aria_label_after_click":label}
    ctx.close()
    # mobile nav + modal + keyboard
    ctx = b.new_context(viewport={"width":375,"height":800}); pg = ctx.new_page(); pg.goto(url)
    vis0 = pg.evaluate("getComputedStyle(document.getElementById('sidebar')).visibility")
    pg.click("[data-nav-toggle]")
    exp = pg.get_attribute("[data-nav-toggle]","aria-expanded")
    vis1 = pg.evaluate("getComputedStyle(document.getElementById('sidebar')).visibility")
    pg.screenshot(path=str(shots/"07-mobile-nav-open-375.png"))
    pg.keyboard.press("Escape")
    exp2 = pg.get_attribute("[data-nav-toggle]","aria-expanded")
    pg.click("[data-modal-open]")
    modal_open = pg.evaluate("document.getElementById('add-dialog').open")
    mr = pg.evaluate("(()=>{const r=document.getElementById('add-dialog').getBoundingClientRect();return [r.left,r.right]})()")
    pg.screenshot(path=str(shots/"08-mobile-modal-375.png"))
    pg.keyboard.press("Escape")
    modal_closed = not pg.evaluate("document.getElementById('add-dialog').open")
    res["mobile_nav_modal"] = {"sidebar_visibility_closed":vis0,"aria_expanded_open":exp,"sidebar_visibility_open":vis1,"aria_expanded_after_esc":exp2,"modal_opened":modal_open,"modal_left_right_px":mr,"modal_closed_with_esc":modal_closed}
    # keyboard: tab order starts at skip link
    pg.goto(url); pg.keyboard.press("Tab")
    res["first_tab_focus"] = pg.evaluate("document.activeElement.className")
    b.close()
print(json.dumps(res, indent=2))
