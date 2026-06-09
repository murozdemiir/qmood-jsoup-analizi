"""
run_all.py
----------
Tum pipeline'i sirayla calistirir:
  1) fetch_versions  -> surumleri indir
  2) analyze         -> metrik cikar + CSV uret
  3) visualize       -> grafikler uret
  4) llm_prompts     -> LLM promptlarini uret
"""
import runpy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

STEPS = ["fetch_versions", "analyze", "visualize", "llm_prompts"]


def main():
    for step in STEPS:
        print("\n" + "#" * 70)
        print(f"# ADIM: {step}")
        print("#" * 70)
        runpy.run_module(step, run_name="__main__")
    print("\n[TAMAM] Tum pipeline calisti.")


if __name__ == "__main__":
    main()
