import json, sys, re

SETS = {
    "CER": "media taza=80;1 taza=160;1 plato=250",
    "VEG": "media taza=75;1 taza=150",
    "BEB": "vaso=250;lata=354;botella 500 ml=500",
    "VASO": "vaso chico=200;vaso=250;vaso grande=350",
    "TAZA": "pocillo=70;taza=200;taza grande=300",
    "CARNE": "porción chica=100;porción=150;porción grande=200",
    "FETA": "1 feta=20;2 fetas=40;4 fetas=80",
    "CDA": "cucharadita=5;cucharada=15",
    "PLATO": "medio plato=150;1 plato=300",
    "PORC": "porción chica=100;porción=150;porción grande=200",
}

src = sys.argv[1]
out = sys.argv[2]
foods = []
names = set()
warn = []
cat = ""
for ln, line in enumerate(open(src, encoding="utf-8"), 1):
    line = line.strip()
    if not line:
        continue
    if line.startswith("#"):
        m = re.match(r"#\s*-+\s*(.+?)\s*-+\s*$", line)
        if m:
            cat = m.group(1)
        continue
    parts = line.split("|")
    if len(parts) < 7:
        sys.exit(f"line {ln}: faltan campos: {line}")
    n, u, k, p, c, g, por = parts[:7]
    alias = parts[7] if len(parts) > 7 else ""
    if n in names:
        sys.exit(f"line {ln}: nombre repetido {n}")
    names.add(n)
    if u not in ("g", "ml"):
        sys.exit(f"line {ln}: unidad {u}")
    k, p, c, g = float(k), float(p), float(c), float(g)
    por = SETS.get(por, por)
    pors = []
    for item in por.split(";"):
        lab, grams = item.rsplit("=", 1)
        pors.append([lab.strip(), float(grams)])
    est = 4 * p + 4 * c + 9 * g
    if k > 30 and abs(est - k) > 0.3 * k:
        warn.append(f"{n}: kcal {k} vs macros {est:.0f}")
    f = {"n": n, "u": u, "k": k, "p": p, "c": c, "g": g, "por": [[l, int(x) if x == int(x) else x] for l, x in pors], "cat": cat}
    if alias:
        f["a"] = alias
    foods.append(f)

js = "const FOODS=" + json.dumps(foods, ensure_ascii=False, separators=(",", ":")) + ";\n"
open(out, "w", encoding="utf-8").write(js)
print(f"{len(foods)} alimentos, {len(js)/1024:.1f} KB")
for w in warn:
    print("  revisar:", w)
