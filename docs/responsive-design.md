# Responsive Architecture

## Approach
Mobile-first. Base styles target 320px; `responsive.css` adds `min-width` media queries only.

| Breakpoint | Name    | Layout |
|-----------:|---------|--------|
| 320px      | Mobile  | 1-column cards, off-canvas sidebar, header with menu button |
| 768px      | Tablet  | 2-column cards, 2-column forms, off-canvas sidebar |
| 1024px     | Laptop  | Permanent sidebar (grid column), 3-column cards |
| 1440px     | Desktop | 4-column cards, wider container |

## Grid vs Flexbox
- **Grid:** page shell (`.app-shell` with named areas), card grids, stats grid (`auto-fit`), form grids.
- **Flexbox:** header, nav list, buttons, form fields, page header, modal actions.

## No horizontal overflow (root causes, not `overflow-x: hidden`)
- Grid tracks use `minmax(0, 1fr)` and children have `min-width: 0`, so long content can't stretch tracks.
- Cards use `overflow-wrap: anywhere` for long unbroken text/emails.
- Images/SVG/video: `max-width: 100%`.
- Tables scroll inside `.table-wrap` (keyboard-focusable region), never the page.
- Modal: `width: min(32rem, calc(100vw - 2rem))`.
- Sidebar is `position: fixed` + `translateX(-100%)` off-canvas below 1024px.

## Themes
Light tokens live in `tokens.css`. `themes.css` overrides them under `:root[data-theme="dark"]`, and under `prefers-color-scheme: dark` when no choice is saved. `js/theme.js` toggles `data-theme`, saves it to `localStorage` key `theme`, and updates the button's `aria-label`/`aria-pressed`. Load it in `<head>` (no `defer`) to avoid a flash.

## Accessibility
Skip link, visible `:focus-visible` rings, 44px touch targets, `aria-expanded`/`aria-controls` on the menu button, Esc closes nav and modal, native `<dialog>` (focus trap), `prefers-reduced-motion`, forced-colors support.

## CSS load order
tokens → reset → base → layout → components → responsive → themes → accessibility
