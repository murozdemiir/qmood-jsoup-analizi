"""
qmood.py
--------
Sinif duzeyi metrikleri (metrics.py) sistem duzeyi QMOOD TASARIM OZELLIKLERINE
toplar ve QMOOD KALITE NITELIKLERINI (Bansiya & Davis, 2002) hesaplar.

QMOOD tasarim metrikleri (sistem duzeyi)
========================================
  DSC  Design Size in Classes     -> toplam sinif sayisi
  NOH  Number of Hierarchies      -> cocugu olan kok sinif sayisi
  ANA  Average Number of Ancestors-> ortalama ata sayisi
  DAM  Data Access Metric         -> ort. (private+protected alan / toplam alan)
  DCC  Direct Class Coupling      -> ortalama sinif baglanti sayisi (CBO)
  CAM  Cohesion Among Methods     -> ortalama metot uyumu
  MOA  Measure of Aggregation     -> ortalama ADT (proje sinifi) tipli alan sayisi
  MFA  Measure of Functional Abst.-> ortalama kalitilan metot orani
  NOP  Number of Polymorphic Meth.-> ortalama polimorfik metot sayisi
  CIS  Class Interface Size       -> ortalama public metot sayisi
  NOM  Number of Methods          -> ortalama metot sayisi (karmasiklik gostergesi)

QMOOD kalite nitelik denklemleri
================================
  Reusability      = -0.25*DCC + 0.25*CAM + 0.50*CIS + 0.50*DSC
  Flexibility      =  0.25*DAM - 0.25*DCC + 0.50*MOA + 0.50*NOP
  Understandability= -0.33*ANA + 0.33*DAM - 0.33*DCC + 0.33*CAM
                     -0.33*NOP - 0.33*NOM - 0.33*DSC
  Functionality    =  0.12*CAM + 0.22*NOP + 0.22*CIS + 0.22*DSC + 0.22*NOH
  Extendibility    =  0.50*ANA - 0.50*DCC + 0.50*MFA + 0.50*NOP
  Effectiveness    =  0.20*ANA + 0.20*DAM + 0.20*MOA + 0.20*MFA + 0.20*NOP

NOT: DSC mutlak deger olarak cok buyuktur ve denklemleri ezer. QMOOD
karsilastirmali calismalarinda standart yaklasim, her tasarim metrigini bir
REFERANS surume (ilk surum) gore NORMALIZE etmektir. Boylece her metrik ~1.0
civarinda indeks olur ve surumler arasi kalite degisimi yorumlanabilir.
Bu modul hem HAM hem NORMALIZE QMOOD tasarim metriklerini ve her iki temelde
kalite niteliklerini uretir.
"""
import numpy as np


DESIGN_PROPERTIES = [
    "DSC", "NOH", "ANA", "DAM", "DCC", "CAM", "MOA", "MFA", "NOP", "CIS", "NOM"
]


def aggregate_design_metrics(classes):
    """metrics.build_project ciktisindan sistem duzeyi QMOOD tasarim metriklerini uretir."""
    infos = list(classes.values())
    n = len(infos)
    if n == 0:
        return {k: 0.0 for k in DESIGN_PROPERTIES}

    def avg(key):
        return float(np.mean([ci.metrics[key] for ci in infos]))

    # DSC: toplam sinif sayisi
    dsc = n

    # NOH: hiyerarsi (kok) sayisi -> cocugu olan (NOC>0) ve kendisi proje ici
    # bir ust sinifa ait OLMAYAN siniflar kok hiyerarsi sayilir.
    names = set(classes.keys())
    roots = 0
    for ci in infos:
        has_children = ci.metrics["NOC"] > 0
        extends_project = ci.extends in names
        implements_project = any(i in names for i in ci.implements)
        is_root = not extends_project and not implements_project
        if has_children and is_root:
            roots += 1
    roots = max(roots, 1)

    return {
        "DSC": float(dsc),
        "NOH": float(roots),
        "ANA": avg("ancestors"),
        "DAM": avg("DAM"),
        "DCC": avg("DCC"),
        "CAM": avg("CAM"),
        "MOA": avg("MOA"),
        "MFA": avg("MFA"),
        "NOP": avg("NOP"),
        "CIS": avg("CIS"),
        "NOM": avg("NOM"),
    }


def quality_attributes(dm):
    """QMOOD kalite niteliklerini verilen tasarim metrigi sozlugunden hesaplar."""
    R = (-0.25 * dm["DCC"] + 0.25 * dm["CAM"] + 0.50 * dm["CIS"] + 0.50 * dm["DSC"])
    F = (0.25 * dm["DAM"] - 0.25 * dm["DCC"] + 0.50 * dm["MOA"] + 0.50 * dm["NOP"])
    U = (-0.33 * dm["ANA"] + 0.33 * dm["DAM"] - 0.33 * dm["DCC"] + 0.33 * dm["CAM"]
         - 0.33 * dm["NOP"] - 0.33 * dm["NOM"] - 0.33 * dm["DSC"])
    Fu = (0.12 * dm["CAM"] + 0.22 * dm["NOP"] + 0.22 * dm["CIS"]
          + 0.22 * dm["DSC"] + 0.22 * dm["NOH"])
    E = (0.50 * dm["ANA"] - 0.50 * dm["DCC"] + 0.50 * dm["MFA"] + 0.50 * dm["NOP"])
    Ef = (0.20 * dm["ANA"] + 0.20 * dm["DAM"] + 0.20 * dm["MOA"]
          + 0.20 * dm["MFA"] + 0.20 * dm["NOP"])
    return {
        "Reusability": R,
        "Flexibility": F,
        "Understandability": U,
        "Functionality": Fu,
        "Extendibility": E,
        "Effectiveness": Ef,
    }


def normalize(dm, baseline):
    """Tasarim metriklerini referans (baseline) surume gore normalize eder."""
    out = {}
    for k in DESIGN_PROPERTIES:
        b = baseline.get(k, 0.0)
        out[k] = (dm[k] / b) if b else 0.0
    return out
