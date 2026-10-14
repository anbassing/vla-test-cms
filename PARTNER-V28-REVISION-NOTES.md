# Visit Locals Partner — V28 Revision Notes

Base: **V25** (`VISIT-LOCALS-v25-partner-popup-form-alignment-fix.zip`)

## Requested changes implemented

### 1. Spectrum of Collaboration — Bring Your Local Knowledge to Life
- Kept all six requested collaboration cards and their exact descriptions/icons.
- Added hover animation to the main Spectrum content grid.
- Added stronger independent hover animation to all six inner collaboration cards:
  - Immersive Cultural Journeys
  - Private Sanctuary Access
  - Cross-Border Business Introductions
  - Regional Industry Dossiers
  - Sustainable Sourcing & Export
  - Community & Adat Stewardship
- Hover uses lift, scale, shadow, and subtle background transition.

### 2. Partner Registration — Let’s Work Together
- Desktop layout is explicitly split into 12 columns.
- Left side: registration heading, description, and the three reassurance boxes.
- Right side: the complete filling form, beginning with **Full Name**.
- The three reassurance boxes alone receive hover animation:
  - Confidentiality Assured
  - Direct WhatsApp Response
  - Zero Listing Fees
- The form itself remains stationary.

## Technical correction
V25 contained malformed nested `<style>` tags around the Partner enhancement CSS. V28 consolidates the Partner CSS into one valid style block so the modal, hover animations, and registration grid rules reliably apply in the browser.

The existing Partner popup behavior from V25 is retained and its card selector is corrected to support the actual `h4` headings used by the Local Knowledge / Who We Work With cards.
