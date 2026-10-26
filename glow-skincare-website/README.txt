========================================================================
GLOW & CARE - CLEAN & KIND SKINCARE E-COMMERCE WEBSITE
========================================================================

Inspired by Simple Skincare (simpleskincare.in), Glow & Care delivers pure,
gentle, and dermatologist-tested skincare formulated for sensitive skin.

------------------------------------------------------------------------
1. PROJECT SPECIFICATIONS & TECH STACK
------------------------------------------------------------------------
- Core Technologies: HTML5 & CSS3 only.
- Strict Constraints:
  * NO JavaScript used anywhere.
  * NO frameworks (No React, Vue, Bootstrap, Tailwind, Node.js).
  * 100% pure HTML & CSS styling and interactivity.
- Brand Name: Glow & Care
- Visual Identity & Color Palette:
  * Base White: #FFFFFF & Soft Off-White: #FAFAF7
  * Soft Mint Green: #E8F5E9 / #D8F3DC / #C2E7D9
  * Deep Forest Green: #1B4332 / #2D6A4F
  * Warm Light Beige: #F9F6F0 / #F3EDE2
  * Gentle Accents: #40916C / #52B788
- Typography:
  * Google Fonts: 'Plus Jakarta Sans' (Body & Clean UI) and 'Playfair Display' (Editorial Headings)

------------------------------------------------------------------------
2. DIRECTORY STRUCTURE
------------------------------------------------------------------------
glow-skincare-website/
│
├── index.html                  --> Homepage (Hero, USPs, Bestsellers, Routine, Reviews, Newsletter)
├── README.txt                  --> Project documentation & guide
│
├── pages/
│   ├── shop.html               --> Full product catalog with filter bar, grid & FAQs
│   ├── face-wash.html          --> Face Wash & Cleansers collection page
│   ├── moisturizers.html       --> Daily Hydrators & Moisturizers collection page
│   ├── serums.html             --> Targeted Serums & Treatments collection page
│   ├── about.html              --> Brand mission, 0% harsh chemical pledge, science & values
│   └── contact.html            --> Pure CSS contact form, support channels & location info
│
├── css/
│   ├── style.css               --> Global theme, CSS custom properties, header, nav, footer, cards
│   ├── shop.css                --> Shop catalog, category headers, filter badges & product grids
│   └── pages.css               --> About & Contact styling, ingredient tables, contact form UI
│
└── images/                     --> Local images directory (Unsplash high-res links used for products)

------------------------------------------------------------------------
3. PURE CSS & ACCESSIBILITY HIGHLIGHTS
------------------------------------------------------------------------
- Pure CSS Mobile Navigation:
  Utilizes the hidden checkbox trick (<input type="checkbox" id="nav-toggle">)
  with CSS sibling selectors (+ and ~) to deliver a responsive slide-out drawer
  on mobile and tablet devices with ZERO JavaScript.
- Pure CSS Form Enhancements:
  Interactive focus states, validation indicators (:valid, :invalid, :focus),
  and tactile submit button animations.
- Pure CSS Accordion:
  Semantic <details> and <summary> tags styled cleanly for FAQs.
- Pure CSS Card Hover Transitions:
  Subtle image elevation, zoom effects, and button transitions.
- Semantic HTML5 Architecture:
  Built using <header>, <nav>, <main>, <section>, <article>, <aside>,
  and <footer> with ARIA-friendly attributes and descriptive alt tags.
- Relative Path Consistency:
  All subpages in 'pages/' link back to root and CSS assets using '../'
  so the entire website functions cleanly when opened locally in any browser.

========================================================================
Developed with care for Glow & Care Skincare.
========================================================================
