// The deck and the output plate, drawn for the Check page (app.js) and the Execute page (execute.js).
// deckView(view): every carrier on its rails and the labware in its sites, seen from the front (the rear-most site at
// the top). Red: a potential problem with it. Yellow: a drafting assumption is about it. Hover for a photo of that
// kind of labware, what it holds and why it is marked; click to keep the card open (for its links).
// outputView(outputs, series): what the protocol's output plate or tubes end up holding, well by well.
// el, fmt and info come from common.js. All text goes through textContent.

const ROLE_LABEL = { output: "Output", source: "Source", intermediate: "Intermediate", tips: "Tips", waste: "Waste" };
const STATUS_LABEL = { issue: "Potential problem", assumption: "Assumption", used: "Used by the protocol", idle: "Not used" };

const hover = { card: null, pinned: null };

function hoverCard() {
  if (!hover.card) {
    hover.card = el("div", { class: "hovercard", role: "dialog", "aria-live": "polite", hidden: "" });
    document.body.append(hover.card);
    document.addEventListener("click", (e) => {
      if (hover.pinned && !hover.card.contains(e.target) && !e.target.closest(".dv-item")) unpin();
    });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") unpin(); });
  }
  return hover.card;
}

function unpin() {
  if (hover.pinned) hover.pinned.classList.remove("pinned");
  hover.pinned = null;
  if (hover.card) hover.card.hidden = true;
}

function place(card, target) {
  const r = target.getBoundingClientRect();
  card.hidden = false;
  const w = card.offsetWidth, h = card.offsetHeight;
  let x = r.right + 10, y = r.top;
  if (x + w > window.innerWidth - 8) x = Math.max(8, r.left - w - 10);
  if (y + h > window.innerHeight - 8) y = Math.max(8, window.innerHeight - h - 8);
  card.style.left = `${x}px`;
  card.style.top = `${y}px`;
}

function photoBlock(image) {
  if (!image) return null;
  const box = el("figure", { class: "hc-photo" });
  if (image.src) {
    const img = el("img", { src: image.src, alt: image.caption || image.name || "", loading: "lazy", referrerpolicy: "no-referrer" });
    img.addEventListener("error", () => img.replaceWith(el("div", { class: "hc-nophoto", text: "Photo unavailable offline" })));
    box.append(img);
  }
  const cap = el("figcaption", {});
  if (image.caption) cap.append(el("span", { text: `${image.caption} (a photo of this kind of labware). ` }));
  if (image.page) cap.append(el("a", { href: image.page, target: "_blank", rel: "noopener", text: `${image.credit || "Source"}, ${image.license || ""}` }));
  if (image.product_page) cap.append(" · ", el("a", { href: image.product_page, target: "_blank", rel: "noopener", text: "Product page" }));
  box.append(cap);
  return box;
}

function list(cls, title, items) {
  if (!items || !items.length) return null;
  return el("div", { class: `hc-list ${cls}` }, el("strong", { text: title }), el("ul", {}, ...items.map((t) => el("li", { text: t }))));
}

function itemCard(kind, data, carrier) {
  const card = hoverCard();
  const rows = [];
  const kv = (k, v) => { if (v != null && v !== "") rows.push(el("div", { class: "hc-kv" }, el("span", { class: "muted", text: k }), el("span", { text: String(v) }))); };
  let title, sub;
  if (kind === "carrier") {
    title = data.type;
    sub = (data.image && data.image.name) || "Carrier";
    kv("On the deck as", data.name);
    kv("Rails", data.width > 1 ? `${data.rails}–${data.rails + data.width - 1}` : data.rails);
    kv("Positions", data.sites);
    if (data.added) kv("Before the run", "Add this carrier to the deck");
  } else {
    title = data.id;
    sub = `${data.type || "tip waste"}${data.image && data.image.name ? ` · ${data.image.name}` : ""}`;
    kv("Role", ROLE_LABEL[data.role] || (data.used ? "Used" : "Not used by this protocol"));
    kv("Where", carrier ? `${carrier.type}, rail ${carrier.rails}, position ${data.position} of ${carrier.sites}` : "");
    kv("Holds", data.holds);
    if (data.loaded_ul != null) kv("Load before the run", `${fmt(data.loaded_ul)} µL`);
    if (data.capacity_ul) kv("Capacity", data.kind === "plate" ? `${fmt(data.capacity_ul)} µL per well` : `${fmt(data.capacity_ul)} µL`);
    if (data.final) kv("At the end", `${data.final.wells > 1 ? `${data.final.wells} wells, ` : ""}${fmt(data.final.total_ul)} µL in all${data.final.leaves_deck ? ", then taken off the deck" : ""}`);
    if (data.added) kv("Before the run", "Place it on the deck");
  }
  const issues = kind === "carrier" ? [...data.issues, ...data.labware.flatMap((l) => l.issues.map((i) => `${l.id}: ${i}`))] : data.issues;
  const assumptions = kind === "carrier" ? data.labware.flatMap((l) => l.assumptions) : data.assumptions;
  card.replaceChildren(
    el("div", { class: "hc-head" }, el("strong", { text: title }), el("span", { class: "muted", text: sub })),
    ...[photoBlock(data.image), el("div", { class: "hc-body" }, ...rows),
      list("bad", "Potential problems", issues), list("warn", "Assumptions about it", [...new Set(assumptions)])].filter(Boolean),
  );
  return card;
}

function attachHover(node, kind, data, carrier) {
  node.tabIndex = 0;
  const show = () => { if (!hover.pinned) place(itemCard(kind, data, carrier), node); };
  node.addEventListener("mouseenter", show);
  node.addEventListener("focus", show);
  node.addEventListener("mouseleave", () => { if (!hover.pinned) hoverCard().hidden = true; });
  node.addEventListener("blur", () => { if (!hover.pinned) hoverCard().hidden = true; });
  node.addEventListener("click", (e) => {
    e.stopPropagation();
    if (hover.pinned === node) { unpin(); return; }
    unpin();
    place(itemCard(kind, data, carrier), node);
    hover.pinned = node;
    node.classList.add("pinned");
  });
}

function shortName(id) {
  return id.length > 16 ? `${id.slice(0, 15)}…` : id;
}

function deckView(view, { usedOnly = false } = {}) {
  const wrap = el("div", { class: "deckview" });
  const rails = view.num_rails || 30;
  const deck = el("div", { class: "dv-deck", role: "group", "aria-label": "Deck layout, seen from the front" });
  deck.append(el("div", { class: "dv-back muted", text: "Back" }));
  for (let r = 1; r <= rails; r++) {
    if (r === 1 || r % 5 === 0) deck.append(el("span", { class: "dv-rail muted", style: `left:${((r - 0.5) / rails) * 100}%`, text: String(r) }));
  }
  for (const c of view.carriers) {
    const shown = usedOnly ? c.labware.filter((l) => l.used) : c.labware;
    if (usedOnly && !shown.length) continue;
    const narrow = c.width <= 2;
    const node = el("div", {
      class: `dv-carrier s-${c.status}${c.added ? " added" : ""}${narrow ? " narrow" : ""}`,
      style: `left:${((c.rails - 1) / rails) * 100}%;width:calc(${(c.width / rails) * 100}% - 3px)`,
    });
    const sites = el("div", { class: "dv-sites" });
    for (const l of c.labware) {
      const pos = l.position || 1;
      const item = el("div", {
        class: `dv-item s-${l.status} r-${l.role || "none"}${l.used ? "" : " unused"}${l.added ? " added" : ""}${l.status === "issue" && l.assumptions.length ? " also-assumption" : ""}`,
        style: `top:${((pos - 1) / c.sites) * 100}%;height:calc(${100 / c.sites}% - 3px)`,
        "aria-label": `${l.id}: ${STATUS_LABEL[l.status]}${l.role ? `, ${ROLE_LABEL[l.role] || l.role}` : ""}`,
      });
      if (c.sites <= 8) {
        item.append(el("span", { class: "dv-label", text: narrow ? shortName(l.id) : l.id }));
        if (!narrow && l.type) item.append(el("span", { class: "dv-type", text: l.type }));
      }
      if (l.role === "output") item.append(el("span", { class: "dv-badge", text: "OUT" }));
      attachHover(item, "labware", l, c);
      sites.append(item);
    }
    const foot = el("div", { class: "dv-foot", title: c.type }, el("span", { text: narrow ? c.type.replace(/_A00.*$/, "") : c.type }));
    attachHover(foot, "carrier", c);
    node.append(sites, foot);
    deck.append(node);
  }
  deck.append(el("div", { class: "dv-front muted", text: "Front (operator side)" }));
  const legend = el("div", { class: "dv-legend" },
    el("span", {}, el("i", { class: "sw s-issue" }), "Potential problem"),
    el("span", {}, el("i", { class: "sw s-assumption" }), "Assumption"),
    el("span", {}, el("i", { class: "sw s-used" }), "Used"),
    el("span", {}, el("i", { class: "sw s-idle" }), "Not used"),
    el("span", {}, el("i", { class: "sw added" }), "Place before the run"),
    el("span", {}, el("b", { class: "dv-badge inline", text: "OUT" }), "The protocol's output"),
    el("span", { class: "muted", text: "Hover for a photo and details; click to keep it open." }));
  wrap.append(deck, legend);
  if (view.general_assumptions && view.general_assumptions.length) {
    wrap.append(el("div", { class: "dv-notes warn" }, el("strong", { text: "Assumptions about the whole protocol" }),
      el("ul", {}, ...view.general_assumptions.map((a) => el("li", { text: a })))));
  }
  if (view.unplaced_issues && view.unplaced_issues.length) {
    wrap.append(el("div", { class: "dv-notes bad" }, el("strong", { text: "Other potential problems" }),
      el("ul", {}, ...view.unplaced_issues.map((a) => el("li", { text: a })))));
  }
  return wrap;
}

// ---------- the output ----------

function contentsText(contents, total, series) {
  return Object.entries(contents).map(([name, ul]) => {
    const n = name.length > 40 ? `${name.slice(0, 39)}…` : name;
    const ratio = series && ul > 0 && total / ul >= 2 ? ` (1:${Number((total / ul).toPrecision(3)).toLocaleString()})` : "";
    return `${n} ${fmt(ul)} µL${ratio}`;
  }).join(" + ");
}

function groupWells(wells) {
  // wells holding the same thing, so "A1–H1: 100 µL TE" reads as one line
  const groups = new Map();
  for (const w of wells) {
    const key = JSON.stringify([w.ul, w.contents]);
    if (!groups.has(key)) groups.set(key, { ul: w.ul, contents: w.contents, wells: [] });
    groups.get(key).wells.push(w.well);
  }
  return [...groups.values()];
}

function wellRange(names) {
  if (names.length <= 3) return names.join(", ");
  return `${names[0]}–${names[names.length - 1]} (${names.length} wells)`;
}

function plateMap(o, series) {
  const rows = o.rows || 8, cols = o.columns || 12;
  const byWell = new Map(o.wells.map((w) => [w.well, w]));
  const max = Math.max(...o.wells.map((w) => w.ul), 1);
  const grid = el("div", { class: "pm-grid", style: `grid-template-columns: 1.4em repeat(${cols}, 1fr)` });
  grid.append(el("span", {}));
  for (let c = 1; c <= cols; c++) grid.append(el("span", { class: "pm-h muted", text: String(c) }));
  for (let r = 0; r < rows; r++) {
    const row = "ABCDEFGHIJKLMNOP"[r];
    grid.append(el("span", { class: "pm-h muted", text: row }));
    for (let c = 1; c <= cols; c++) {
      const w = byWell.get(`${row}${c}`);
      const cell = el("span", { class: `pm-well${w ? " full" : ""}` });
      if (w) {
        cell.style.setProperty("--fill", String(0.25 + 0.75 * (w.ul / max)));
        cell.title = `${w.well}: ${fmt(w.ul)} µL = ${contentsText(w.contents, w.ul, series)}`;
        cell.setAttribute("aria-label", cell.title);
      }
      grid.append(cell);
    }
  }
  return grid;
}

function outputView(outputs, series) {
  const box = el("div", { class: "outputs" });
  if (!outputs || !outputs.length) {
    box.append(el("p", { class: "muted", text: "No labware holds liquid the protocol put there at the end." }));
    return box;
  }
  const plates = outputs.filter((o) => o.kind === "plate");
  const tubes = outputs.filter((o) => o.kind !== "plate");
  for (const o of plates) {
    const groups = groupWells(o.wells);
    box.append(el("div", { class: "out-plate" },
      el("div", { class: "out-head" }, el("strong", { text: o.labware }),
        el("span", { class: "muted", text: ` ${o.wells.length} well${o.wells.length === 1 ? "" : "s"} filled, ${fmt(o.total_ul)} µL in all${o.named_by_protocol ? " · named as the output by the protocol" : ""}` })),
      plateMap(o, series),
      el("ul", { class: "out-groups" }, ...groups.map((g) => el("li", {},
        el("span", { class: "mono", text: wellRange(g.wells) }), el("span", { text: `  ${fmt(g.ul)} µL = ${contentsText(g.contents, g.ul, series)}` })))),
      o.leaves_deck ? el("p", { class: "note", text: `Then off the deck: ${o.leaves_deck}` }) : null));
  }
  if (tubes.length) {
    const max = Math.max(...tubes.map((t) => t.total_ul), 1);
    box.append(el("div", { class: "out-tubes" }, ...tubes.map((t) => {
      const w = t.wells[0] || { ul: 0, contents: {} };
      return el("div", { class: "out-tube", title: contentsText(w.contents, w.ul, series) },
        el("div", { class: "tube-glass" }, el("div", { class: "tube-fill", style: `height:${Math.max(6, (t.total_ul / max) * 100)}%` })),
        el("strong", { text: t.labware }), el("span", { class: "muted", text: `${fmt(t.total_ul)} µL` }),
        el("small", { text: contentsText(w.contents, w.ul, series) }),
        t.leaves_deck ? el("small", { class: "note", text: `Then: ${t.leaves_deck}` }) : null);
    })));
  }
  return box;
}
