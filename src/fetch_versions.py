"""
fetch_versions.py
-----------------
jsoup açık kaynak projesinin seçili sürümlerinin (git tag) kaynak kodunu indirir.

Yaklaşim:
  1. jsoup deposu blob filtreli (hizli) olarak klonlanir.
  2. Her secili tag icin `git archive` ile yalnizca `src/main/java` agaci
     data/versions/<surum>/ altina cikarilir.

Cikti: data/versions/1.14.1/ , data/versions/1.15.1/ ... seklinde 11 surum.
"""
import os
import subprocess
import sys
import tarfile
import io
import shutil

REPO_URL = "https://github.com/jhy/jsoup"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
CLONE_DIR = os.path.join(DATA, "_jsoup_repo")
VERSIONS_DIR = os.path.join(DATA, "versions")

# Yazilim evrimini (1.14 -> 1.22) kapsayacak sekilde secilmis 11 surum.
# Her minor surumden en az bir temsilci alinarak buyume egrisi yakalanir.
SELECTED = [
    "1.14.1",
    "1.14.3",
    "1.15.1",
    "1.15.4",
    "1.16.2",
    "1.17.2",
    "1.18.3",
    "1.19.1",
    "1.20.1",
    "1.21.2",
    "1.22.2",
]

SRC_SUBPATH = "src/main/java"


def run(cmd, cwd=None, check=True):
    print("  $", " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd, check=check)


def ensure_clone():
    """Bos bir git deposu hazirlar (tum gecmis klonlanmaz).

    Flaky aglara dayanikli olmasi icin tum gecmisi klonlamak yerine her tag
    ayri ayri `--depth 1` ile cekilir (extract_version icinde). Burada sadece
    bos depo + remote + tolerans ayarlari kurulur.
    """
    if not os.path.isdir(os.path.join(CLONE_DIR, ".git")):
        os.makedirs(CLONE_DIR, exist_ok=True)
        print(f"[+] Bos git deposu hazirlaniyor -> {CLONE_DIR}")
        run(["git", "init", "-q"], cwd=CLONE_DIR)
        run(["git", "remote", "add", "origin", REPO_URL], cwd=CLONE_DIR, check=False)
    # kopuk baglantilara karsi tolerans ayarlari
    run(["git", "config", "http.postBuffer", "524288000"], cwd=CLONE_DIR, check=False)
    run(["git", "config", "http.lowSpeedLimit", "0"], cwd=CLONE_DIR, check=False)
    run(["git", "config", "http.lowSpeedTime", "999999"], cwd=CLONE_DIR, check=False)


def fetch_tag(git_tag, retries=4):
    """Tek bir tag'i shallow (depth 1) ceker; kopmada tekrar dener."""
    for attempt in range(1, retries + 1):
        r = run(["git", "fetch", "--depth", "1", "--no-tags", "origin",
                 f"refs/tags/{git_tag}:refs/tags/{git_tag}"],
                cwd=CLONE_DIR, check=False)
        if r.returncode == 0:
            return True
        print(f"    [!] {git_tag} cekme denemesi {attempt}/{retries} basarisiz, tekrar...")
    return False


def extract_version(tag):
    out_dir = os.path.join(VERSIONS_DIR, tag)
    if os.path.isdir(out_dir) and os.listdir(out_dir):
        print(f"[=] {tag} zaten cikarilmis, atlaniyor.")
        return
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    git_tag = f"jsoup-{tag}"
    if not fetch_tag(git_tag):
        raise RuntimeError(f"{git_tag} cekilemedi (ag hatasi)")
    print(f"[+] {git_tag} : {SRC_SUBPATH} cikariliyor -> {out_dir}")
    # git archive ile tar uretip bellek uzerinden cikartiyoruz
    proc = subprocess.run(
        ["git", "archive", "--format=tar", git_tag, SRC_SUBPATH],
        cwd=CLONE_DIR, check=True, stdout=subprocess.PIPE,
    )
    tar_bytes = io.BytesIO(proc.stdout)
    with tarfile.open(fileobj=tar_bytes, mode="r:") as tf:
        members = [m for m in tf.getmembers() if m.name.endswith(".java")]
        for m in members:
            # src/main/java/org/jsoup/... -> out_dir/org/jsoup/...
            rel = m.name[len(SRC_SUBPATH):].lstrip("/")
            target = os.path.join(out_dir, rel)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            f = tf.extractfile(m)
            if f is not None:
                with open(target, "wb") as out:
                    out.write(f.read())
    n = sum(1 for _ in iter_java(out_dir))
    print(f"    -> {n} .java dosyasi")


def iter_java(root):
    for dirpath, _, files in os.walk(root):
        for fn in files:
            if fn.endswith(".java"):
                yield os.path.join(dirpath, fn)


def main():
    ensure_clone()
    os.makedirs(VERSIONS_DIR, exist_ok=True)
    for tag in SELECTED:
        try:
            extract_version(tag)
        except subprocess.CalledProcessError as e:
            print(f"[!] {tag} cikarilamadi: {e}", file=sys.stderr)
    print("\n[OK] Tum surumler hazir:")
    for tag in SELECTED:
        d = os.path.join(VERSIONS_DIR, tag)
        if os.path.isdir(d):
            n = sum(1 for _ in iter_java(d))
            print(f"  {tag:8s}  {n:4d} java dosyasi")


if __name__ == "__main__":
    main()
