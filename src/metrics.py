"""
metrics.py
----------
Java kaynak kodundan SINIF DUZEYINDE nesne yonelimli metrikleri cikarir.
Parser olarak `javalang` (saf Python) kullanilir; hicbir hazir metrik araci
kullanilmaz (yonerge: "hazir analiz sonuclarinin dogrudan kullanilmasi yasaktir").

Hesaplanan sinif duzeyi metrikler
=================================
CK metrik takimi:
  WMC   Weighted Methods per Class   -> metotlarin McCabe karmasikliklari toplami
  DIT   Depth of Inheritance Tree    -> proje ici kalitim agacinda koke uzaklik
  NOC   Number of Children           -> dogrudan alt sinif sayisi (proje ici)
  CBO   Coupling Between Objects      -> baglantili farkli proje sinifi sayisi
  RFC   Response For a Class          -> tanimli metot + cagrilan farkli metot
  LCOM  Lack of Cohesion of Methods  -> Chidamber-Kemerer LCOM
  NOM   Number of Methods            -> tanimli metot sayisi
  NOA   Number of Attributes         -> alan (field) sayisi
  MPC   Message Passing Coupling     -> disa yapilan metot cagrisi sayisi
  DAC   Data Abstraction Coupling    -> tipi proje sinifi olan alan sayisi

QMOOD tasarim metrikleri icin ek sinif duzeyi olculer:
  pub_methods   -> public metot sayisi (CIS icin)
  priv_prot_attr-> private+protected alan sayisi (DAM icin)
  inherited_methods / accessible_methods (MFA icin)
  poly_methods  -> soyut/override/overridable metot sayisi (NOP icin)
  cam           -> Cohesion Among Methods (parametre tipi ortakligi)
  ancestors     -> proje ici ata sayisi (ANA icin)

Sistem duzeyi (QMOOD) toplamlar qmood.py icinde hesaplanir.
"""
import os
import javalang
from collections import defaultdict


# ----------------------------- yardimcilar -----------------------------------

PRIMITIVES = {
    "byte", "short", "int", "long", "float", "double", "boolean", "char",
    "void", "String", "Object", "Integer", "Long", "Double", "Boolean",
    "Float", "Character", "Byte", "Short", "Number", "CharSequence",
}


def iter_java_files(root):
    for dirpath, _, files in os.walk(root):
        for fn in files:
            if fn.endswith(".java"):
                yield os.path.join(dirpath, fn)


def type_name(t):
    """javalang tip dugumunden temel tip adini cikarir (jenerikleri soyar)."""
    if t is None:
        return None
    name = getattr(t, "name", None)
    if name is None:
        return None
    return name


def count_cyclomatic(method):
    """Metot govdesindeki karar noktalarini sayarak McCabe karmasikligi (+1)."""
    complexity = 1
    decision = (
        javalang.tree.IfStatement,
        javalang.tree.ForStatement,
        javalang.tree.WhileStatement,
        javalang.tree.DoStatement,
        javalang.tree.SwitchStatementCase,
        javalang.tree.CatchClause,
        javalang.tree.TernaryExpression,
    )
    try:
        for _, node in method:
            if isinstance(node, decision):
                complexity += 1
            elif isinstance(node, javalang.tree.BinaryOperation) and node.operator in ("&&", "||"):
                complexity += 1
    except Exception:
        pass
    return complexity


# --------------------------- ana cozumleyici ---------------------------------

class ClassInfo:
    """Tek bir sinif/arayuz icin toplanan ham bilgi ve metrikler."""

    def __init__(self, name, kind):
        self.name = name              # basit ad (paketsiz)
        self.kind = kind              # 'class' | 'interface' | 'enum'
        self.extends = None           # ust sinif basit adi
        self.implements = []          # arayuz basit adlari
        self.is_abstract = False
        self.attributes = []          # (ad, tip_adi, gorunurluk)
        self.methods = []             # dict: name, params(list of type), visibility,
                                      #       complexity, is_abstract, is_override,
                                      #       is_final, is_static, called_methods(set),
                                      #       used_types(set), accessed_fields(set)
        # turetilmis metrikler (hesaplanir):
        self.metrics = {}

    # --- kolaylik ---
    @property
    def nom(self):
        return len(self.methods)

    @property
    def noa(self):
        return len(self.attributes)


def parse_file(path):
    """Bir .java dosyasini cozumleyip ClassInfo listesi dondurur."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        src = f.read()
    try:
        tree = javalang.parse.parse(src)
    except Exception:
        return []  # cozumlenemeyen dosyayi atla

    infos = []
    for _, node in tree.filter(javalang.tree.TypeDeclaration):
        if isinstance(node, javalang.tree.ClassDeclaration):
            kind = "class"
        elif isinstance(node, javalang.tree.InterfaceDeclaration):
            kind = "interface"
        elif isinstance(node, javalang.tree.EnumDeclaration):
            kind = "enum"
        else:
            continue

        ci = ClassInfo(node.name, kind)
        mods = set(getattr(node, "modifiers", []) or [])
        ci.is_abstract = "abstract" in mods or kind == "interface"

        if getattr(node, "extends", None):
            ext = node.extends
            if isinstance(ext, list):  # interface birden fazla extends edebilir
                ci.extends = type_name(ext[0]) if ext else None
                for e in ext[1:]:
                    ci.implements.append(type_name(e))
            else:
                ci.extends = type_name(ext)
        for impl in (getattr(node, "implements", None) or []):
            ci.implements.append(type_name(impl))

        # --- alanlar (fields) ---
        for field in node.fields if hasattr(node, "fields") else []:
            fmods = set(field.modifiers or [])
            vis = _visibility(fmods)
            tname = type_name(field.type)
            for decl in field.declarators:
                ci.attributes.append((decl.name, tname, vis))

        # --- metotlar ---
        for m in (getattr(node, "methods", None) or []):
            mmods = set(m.modifiers or [])
            minfo = {
                "name": m.name,
                "params": [type_name(p.type) for p in (m.parameters or [])],
                "visibility": _visibility(mmods),
                "is_abstract": ("abstract" in mmods) or kind == "interface",
                "is_static": "static" in mmods,
                "is_final": "final" in mmods,
                "complexity": count_cyclomatic(m),
                "called_methods": set(),
                "used_types": set(),
                "accessed_fields": set(),
                "annotations": {a.name for a in (m.annotations or [])},
            }
            _collect_method_body(m, minfo, ci)
            ci.methods.append(minfo)

        # yapilandiricilar da metot govdesi gibi cagri/kullanim icerir
        for c in (getattr(node, "constructors", None) or []):
            cinfo = {
                "name": "<init>",
                "params": [type_name(p.type) for p in (c.parameters or [])],
                "visibility": _visibility(set(c.modifiers or [])),
                "is_abstract": False, "is_static": False, "is_final": False,
                "complexity": count_cyclomatic(c),
                "called_methods": set(), "used_types": set(),
                "accessed_fields": set(), "annotations": set(),
            }
            _collect_method_body(c, cinfo, ci)
            ci.methods.append(cinfo)

        infos.append(ci)
    return infos


def _visibility(mods):
    if "private" in mods:
        return "private"
    if "protected" in mods:
        return "protected"
    if "public" in mods:
        return "public"
    return "package"


def _collect_method_body(method, minfo, ci):
    """Metot govdesinden cagrilan metotlari, kullanilan tipleri, erisilen alanlari toplar."""
    try:
        for _, node in method:
            if isinstance(node, javalang.tree.MethodInvocation):
                minfo["called_methods"].add(node.member)
                if node.qualifier:
                    minfo["used_types"].add(node.qualifier)
            elif isinstance(node, javalang.tree.ClassCreator):
                tn = type_name(node.type)
                if tn:
                    minfo["used_types"].add(tn)
            elif isinstance(node, javalang.tree.MemberReference):
                if node.member:
                    minfo["accessed_fields"].add(node.member)
            elif isinstance(node, (javalang.tree.LocalVariableDeclaration,)):
                tn = type_name(node.type)
                if tn:
                    minfo["used_types"].add(tn)
    except Exception:
        pass
    # parametre ve donus tipleri de kullanilan tip sayilir
    for p in minfo["params"]:
        if p:
            minfo["used_types"].add(p)


# --------------------- proje genelinde metrik hesaplama ----------------------

def build_project(version_dir):
    """Bir surum dizinindeki tum siniflari cozumler ve metrikleri hesaplar.

    Donus: {sinif_adi: ClassInfo} sozlugu (metrics doldurulmus).
    """
    classes = {}
    for path in iter_java_files(version_dir):
        for ci in parse_file(path):
            # ayni basit ad birden fazla olabilir (ic siniflar); ilkini tut
            if ci.name not in classes:
                classes[ci.name] = ci

    names = set(classes.keys())

    # kalitim iliskileri: cocuk sayilari ve ata zincirleri
    children = defaultdict(list)
    for ci in classes.values():
        if ci.extends and ci.extends in names:
            children[ci.extends].append(ci.name)
        for impl in ci.implements:
            if impl in names:
                children[impl].append(ci.name)

    def ancestors(name, seen=None):
        if seen is None:
            seen = set()
        ci = classes.get(name)
        if not ci:
            return []
        chain = []
        parent = ci.extends
        while parent and parent in classes and parent not in seen:
            seen.add(parent)
            chain.append(parent)
            parent = classes[parent].extends
        return chain

    # her sinif icin metrikleri hesapla
    for name, ci in classes.items():
        anc = ancestors(name)
        dit = len(anc)
        noc = len(children.get(name, []))

        # CBO / DCC: baglantili farkli proje siniflari
        coupled = set()
        # alan tipleri
        for (_, tname, _) in ci.attributes:
            if tname in names and tname != name:
                coupled.add(tname)
        # metot parametre/donus/kullanim tipleri + extends/implements
        for m in ci.methods:
            for t in m["used_types"]:
                if t in names and t != name:
                    coupled.add(t)
        if ci.extends in names:
            coupled.add(ci.extends)
        for impl in ci.implements:
            if impl in names:
                coupled.add(impl)
        cbo = len(coupled)

        # RFC: tanimli metotlar + cagrilan farkli metotlar
        called = set()
        for m in ci.methods:
            called |= m["called_methods"]
        rfc = ci.nom + len(called)

        # MPC: toplam disa metot cagrisi (tekrarli sayim, mesaj trafigi)
        mpc = sum(len(m["called_methods"]) for m in ci.methods)

        # DAC / MOA: tipi proje sinifi olan alan sayisi
        dac = sum(1 for (_, tname, _) in ci.attributes
                  if tname in names and tname != name)

        # WMC: metot karmasikliklari toplami
        wmc = sum(m["complexity"] for m in ci.methods)

        # LCOM (Chidamber-Kemerer): alan paylasimina gore metot ciftleri
        lcom = _lcom_ck(ci)

        # --- QMOOD ek olculeri ---
        pub_methods = sum(1 for m in ci.methods if m["visibility"] == "public")
        priv_prot_attr = sum(1 for (_, _, v) in ci.attributes
                             if v in ("private", "protected"))
        dam = (priv_prot_attr / ci.noa) if ci.noa else 1.0  # kapsulleme orani
        # MFA: kalitilan metot / erisilebilir metot
        inherited = 0
        for a in anc:
            inherited += classes[a].nom if a in classes else 0
        accessible = inherited + ci.nom
        mfa = (inherited / accessible) if accessible else 0.0
        # NOP: polimorfik metotlar (soyut, override veya overridable=public/protected non-final non-static)
        poly = 0
        for m in ci.methods:
            if m["is_abstract"] or "Override" in m["annotations"]:
                poly += 1
            elif (not m["is_static"] and not m["is_final"]
                  and m["visibility"] in ("public", "protected")
                  and m["name"] != "<init>"):
                poly += 1
        cam = _cam(ci)

        ci.metrics = {
            "kind": ci.kind,
            "is_abstract": int(ci.is_abstract),
            "DIT": dit, "NOC": noc, "WMC": wmc, "CBO": cbo, "RFC": rfc,
            "LCOM": lcom, "NOM": ci.nom, "NOA": ci.noa, "MPC": mpc, "DAC": dac,
            # QMOOD ek olculeri:
            "ancestors": dit, "CIS": pub_methods, "DAM": round(dam, 4),
            "MFA": round(mfa, 4), "NOP": poly, "MOA": dac, "CAM": round(cam, 4),
            "DCC": cbo,
        }

    return classes


def _lcom_ck(ci):
    """Chidamber-Kemerer LCOM: alan paylasmayan metot cifti sayisi - paylasan.

    LCOM = max(0, |P| - |Q|),  P: ortak alani olmayan ciftler, Q: olan ciftler.
    """
    methods = [m for m in ci.methods if m["name"] != "<init>"]
    field_names = {a[0] for a in ci.attributes}
    sets = []
    for m in methods:
        used = m["accessed_fields"] & field_names
        sets.append(used)
    n = len(sets)
    if n < 2:
        return 0
    P = Q = 0
    for i in range(n):
        for j in range(i + 1, n):
            if sets[i] & sets[j]:
                Q += 1
            else:
                P += 1
    return max(0, P - Q)


def _cam(ci):
    """Cohesion Among Methods: metot parametre tiplerinin tum tip kumesine orani.

    CAM = (her metodun parametre tipleri kesisimi) / (toplam tip * metot sayisi).
    Bansiya-Davis tanimina yakin basitlestirilmis bicim.
    """
    methods = [m for m in ci.methods if m["name"] != "<init>"]
    if not methods:
        return 0.0
    all_types = set()
    per_method = []
    for m in methods:
        ts = {t for t in m["params"] if t}
        per_method.append(ts)
        all_types |= ts
    if not all_types:
        return 0.0
    total = 0.0
    for ts in per_method:
        total += len(ts) / len(all_types)
    return total / len(methods)
