"""
analyze.py
----------
Tum surumler icin metrik cikarimini calistirir ve sonuc tablolarini uretir.

Ciktilar (data/ altinda):
  class_metrics.csv   -> her surum x her sinif icin tum sinif duzeyi metrikler
  design_metrics.csv  -> her surum icin sistem duzeyi QMOOD tasarim metrikleri
                         (ham + baseline'a gore normalize)
  quality_raw.csv     -> ham tasarim metriklerinden kalite nitelikleri
  quality_norm.csv    -> normalize tasarim metriklerinden kalite nitelikleri
  ck_summary.csv      -> surum basina CK metrik ortalamalari (genel egilim)
"""
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import metrics as M
import qmood as Q
from fetch_versions import SELECTED, VERSIONS_DIR

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

CK_METRICS = ["DIT", "NOC", "WMC", "CBO", "RFC", "LCOM", "NOM", "NOA", "MPC", "DAC"]


def analyze_version(version):
    vdir = os.path.join(VERSIONS_DIR, version)
    classes = M.build_project(vdir)
    return classes


def main():
    class_rows = []
    design_rows = []
    ck_rows = []
    design_by_version = {}

    versions = [v for v in SELECTED
                if os.path.isdir(os.path.join(VERSIONS_DIR, v))]
    print(f"[i] {len(versions)} surum analiz edilecek: {versions}")

    for v in versions:
        print(f"[+] Analiz: {v}")
        classes = analyze_version(v)
        print(f"    {len(classes)} sinif cozumlendi")

        # sinif duzeyi satirlar
        for name, ci in classes.items():
            row = {"version": v, "class": name}
            row.update({k: ci.metrics[k] for k in
                        CK_METRICS + ["CIS", "DAM", "MFA", "NOP", "MOA", "CAM",
                                      "DCC", "kind", "is_abstract"]})
            class_rows.append(row)

        # CK ortalamalari
        df_v = pd.DataFrame(
            [{k: ci.metrics[k] for k in CK_METRICS} for ci in classes.values()])
        ck_avg = {"version": v, "num_classes": len(classes)}
        ck_avg.update({f"{k}_mean": round(df_v[k].mean(), 4) for k in CK_METRICS})
        ck_avg.update({f"{k}_max": int(df_v[k].max()) for k in CK_METRICS})
        ck_rows.append(ck_avg)

        # QMOOD tasarim metrikleri
        dm = Q.aggregate_design_metrics(classes)
        design_by_version[v] = dm

    # baseline = ilk surum
    baseline = design_by_version[versions[0]]

    quality_raw_rows = []
    quality_norm_rows = []
    for v in versions:
        dm = design_by_version[v]
        ndm = Q.normalize(dm, baseline)

        drow = {"version": v}
        drow.update({k: round(dm[k], 4) for k in Q.DESIGN_PROPERTIES})
        drow.update({f"{k}_norm": round(ndm[k], 4) for k in Q.DESIGN_PROPERTIES})
        design_rows.append(drow)

        qr = Q.quality_attributes(dm)
        qn = Q.quality_attributes(ndm)
        qrr = {"version": v}
        qrr.update({k: round(val, 4) for k, val in qr.items()})
        quality_raw_rows.append(qrr)
        qnr = {"version": v}
        qnr.update({k: round(val, 4) for k, val in qn.items()})
        quality_norm_rows.append(qnr)

    # yaz
    pd.DataFrame(class_rows).to_csv(
        os.path.join(DATA, "class_metrics.csv"), index=False)
    pd.DataFrame(design_rows).to_csv(
        os.path.join(DATA, "design_metrics.csv"), index=False)
    pd.DataFrame(ck_rows).to_csv(
        os.path.join(DATA, "ck_summary.csv"), index=False)
    pd.DataFrame(quality_raw_rows).to_csv(
        os.path.join(DATA, "quality_raw.csv"), index=False)
    pd.DataFrame(quality_norm_rows).to_csv(
        os.path.join(DATA, "quality_norm.csv"), index=False)

    print("\n[OK] CSV ciktilari yazildi: data/")
    print("\n=== QMOOD Kalite Nitelikleri (normalize, baseline=" + versions[0] + ") ===")
    print(pd.DataFrame(quality_norm_rows).to_string(index=False))


if __name__ == "__main__":
    main()
