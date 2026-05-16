#!/usr/bin/env python3
"""Extrakce obrázků/diagramů z PDF přednášek BI-OSY do wiki/skripta/img/.

Pipeline pro každé PDF:
  1. pdfimages -list  -> tabulka objektů (page, num, type, width, height)
  2. pdfimages -png   -> každý objekt jako <prefix>-NNN.png (NNN == sloupec num)
  3. ke každému `image` se spáruje jeho `smask` (alfa maska), pokud existuje
  4. image + smask se složí a podloží bílou (jinak má diagram černé pozadí)
  5. zahodí se malé / téměř prázdné / duplicitní obrázky a titulní strany
  6. uloží se jako <kod>-sXX-N.png a zapíše se manifest.json

Použití:  ./venv/bin/python extract_images.py
"""
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent
PDF_DIR = ROOT / "prednasky"
OUT_DIR = ROOT / "wiki" / "skripta" / "img"

# kód přednášky -> soubor PDF (12 hlavních přednášek; p01 bez duplicitního "01_" prefixu)
LECTURES = {
    "p01": "bi-osy-p01-Introduction_01.pdf",
    "p02": "bi-osy-p02-Threads_01.pdf",
    "p03": "bi-osy-p03-IPC_tools-01.pdf",
    "p04": "bi-osy-p04-IPC_problems_01.pdf",
    "p05": "bi-osy-p05-Deadlock-01.pdf",
    "p06": "bi-osy-p06-Scheduling-01.pdf",
    "p07": "bi-osy-p07-Memory_Introduction-01.pdf",
    "p08": "bi-osy-p08-Memory_VM-01.pdf",
    "p09": "bi-osy-p09-Memory_PRA-01.pdf",
    "p10": "biosy-p10-Data_storage-01.pdf",
    "p11": "biosy-p11-FS_Disk-01.pdf",
    "p12": "biosy-p12-FS_OS-01.pdf",
}

# Filtrační prahy
MIN_W, MIN_H = 250, 150          # menší objekty = ikony, odrážky, loga
MIN_AREA = 80_000                # plocha v px
MIN_INK = 1500                   # min. počet ne-bílých pixelů (jinak prázdný objekt)
SKIP_PAGES = {1, 2}              # titulní strana + obsah


def list_objects(pdf: Path):
    """Vrátí seznam objektů z `pdfimages -list` jako dict(page, num, type, w, h)."""
    out = subprocess.run(
        ["pdfimages", "-list", str(pdf)], capture_output=True, text=True
    ).stdout
    rows = []
    for line in out.splitlines()[2:]:
        p = line.split()
        if len(p) < 5 or not p[0].isdigit():
            continue
        rows.append(
            {"page": int(p[0]), "num": int(p[1]), "type": p[2],
             "w": int(p[3]), "h": int(p[4])}
        )
    return rows


def composite(img_path: Path, mask_path: Path | None) -> Image.Image:
    """Složí image + smask a podloží bílou; vrátí RGB obrázek."""
    img = Image.open(img_path).convert("RGB")
    if mask_path and mask_path.exists():
        mask = Image.open(mask_path).convert("L")
        if mask.size != img.size:
            mask = mask.resize(img.size)
        bg = Image.new("RGB", img.size, "white")
        bg.paste(img, mask=mask)
        return bg
    return img


def ink_pixels(img: Image.Image) -> int:
    """Počet ne-bílých (tmavších) pixelů — odhad, zda obrázek něco obsahuje."""
    hist = img.convert("L").histogram()
    return sum(hist[:248])


def main():
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)

    manifest: dict[str, list] = {}
    seen_hashes: dict[str, str] = {}   # hash -> první soubor (deduplikace)
    total_kept = 0

    for code, pdf_name in LECTURES.items():
        pdf = PDF_DIR / pdf_name
        if not pdf.exists():
            print(f"  ! chybí {pdf_name}")
            continue

        rows = list_objects(pdf)
        by_num = {r["num"]: r for r in rows}

        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                ["pdfimages", "-png", str(pdf), f"{tmp}/x"],
                capture_output=True,
            )
            kept = []
            for r in rows:
                if r["type"] != "image":
                    continue
                # spárování se smask: následující objekt téže strany
                nxt = by_num.get(r["num"] + 1)
                mask_path = None
                if nxt and nxt["type"] in ("smask", "stencil") and nxt["page"] == r["page"]:
                    mask_path = Path(tmp) / f"x-{nxt['num']:03d}.png"

                if r["page"] in SKIP_PAGES:
                    continue
                if r["w"] < MIN_W or r["h"] < MIN_H or r["w"] * r["h"] < MIN_AREA:
                    continue

                img_path = Path(tmp) / f"x-{r['num']:03d}.png"
                if not img_path.exists():
                    continue
                final = composite(img_path, mask_path)
                if ink_pixels(final) < MIN_INK:
                    continue

                digest = hashlib.md5(final.tobytes()).hexdigest()
                if digest in seen_hashes:
                    continue
                seen_hashes[digest] = code

                idx = len([k for k in kept if k["page"] == r["page"]]) + 1
                fname = f"{code}-s{r['page']:02d}-{idx}.png"
                final.save(OUT_DIR / fname, optimize=True)
                kept.append({"file": fname, "page": r["page"],
                             "w": final.width, "h": final.height})

            manifest[code] = kept
            total_kept += len(kept)
            print(f"  {code}: {len(kept):2d} obrázků  ({pdf_name})")

    (OUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nCelkem {total_kept} obrázků -> {OUT_DIR}")


if __name__ == "__main__":
    main()
