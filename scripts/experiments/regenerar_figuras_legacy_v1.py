#!/usr/bin/env python3
"""regenerar_figuras_legacy_v1.py — rehace las dos figuras heredadas sin generador.

POR QUE EXISTE
--------------
La auditoria de figuras del 2026-08-26 encontro que seis figuras de la memoria estaban a
160-170 dpi frente a los 300 del resto, y con una paleta distinta. Cuatro las producia
`final_report_audit_artifacts_v1.py` (corregido alli). Las otras dos —la curva de latencia
y la fraccion de sesiones agitadas por periodo— no tenian generador en ningun script ni
cuaderno: se habian producido de forma manual y no eran reproducibles.

Este script las devuelve al ciclo reproducible. Los valores NO se re-derivan de los datos
crudos: se toman de las tablas ya publicadas y verificadas de la memoria, que es lo que la
figura debe ilustrar. Cada uno lleva anotada su procedencia para que la correspondencia sea
comprobable de un vistazo.

Estilo: identico al del resto del documento (300 dpi, paleta azul/tierra/gris, sin marco
superior ni derecho, rejilla tenue), de modo que las figuras parezcan del mismo trabajo.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
FIGS = RAIZ / "reports/memoria/figures"

AZUL, TIERRA, GRIS, TINTA = "#2E5E8C", "#B5651D", "#8A8F98", "#1A1A1A"

# Fuente: Tabla «Rendimiento en el test terminal bajo distintas latencias»
# (reports/memoria/mainmatter/chapter3.tex, tab:latencia)
LATENCIA = [(0, 64, 92.2, +6.79), (2, 63, 39.7, -1.48),
            (4, 66, 45.5, -0.74), (8, 66, 43.9, -0.30)]

# Fuente: chapter4.tex — «la fraccion de sesiones de alta volatilidad aumento hasta
# aproximadamente el 58 %, frente al 18-22 % de los periodos historicos»
REGIMEN = [("Entrenamiento\n(may)", 18.0), ("Validación\n(may)", 22.0),
           ("Bloque fuera\nde muestra (jun)", 58.0)]


def estilo():
    plt.rcParams.update({
        "figure.dpi": 300, "savefig.dpi": 300, "font.size": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "axes.axisbelow": True, "grid.alpha": 0.25,
        "axes.edgecolor": GRIS, "text.color": TINTA,
        "axes.labelcolor": TINTA, "xtick.color": TINTA, "ytick.color": TINTA,
    })


def fig_latencia():
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    x = [f"{s} s" for s, _, _, _ in LATENCIA]
    y = [n for _, _, _, n in LATENCIA]
    col = [AZUL if v > 0 else TIERRA for v in y]
    barras = ax.bar(x, y, color=col, width=0.58)
    ax.axhline(0, color=TINTA, lw=0.9)
    for b, (_, n, ac, v) in zip(barras, LATENCIA):
        va = "bottom" if v > 0 else "top"
        off = 0.25 if v > 0 else -0.25
        ax.text(b.get_x() + b.get_width() / 2, v + off, f"{v:+.2f}",
                ha="center", va=va, fontsize=9, color=TINTA)
        ax.text(b.get_x() + b.get_width() / 2, -7.4, f"n={n}\n{ac:.1f} %",
                ha="center", va="bottom", fontsize=7.5, color=GRIS)
    ax.set_ylim(-8.2, 8.4)
    ax.set_ylabel("Neto medio (ticks)")
    ax.set_xlabel("Latencia de entrada")
    ax.set_title("La ventaja no sobrevive al primer escalón medible", pad=10)
    ax.text(0.015, 0.955,
            "acierto direccional del 92 % a latencia cero;\nel resultado economico ya es negativo a 2 s",
            transform=ax.transAxes, fontsize=8, color=GRIS, va="top")
    fig.tight_layout()
    p = FIGS / "fig_latencia.png"
    fig.savefig(p, bbox_inches="tight")
    plt.close(fig)
    return p


def fig_regimen():
    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    et = [e for e, _ in REGIMEN]
    v = [x for _, x in REGIMEN]
    col = [GRIS, GRIS, TIERRA]
    barras = ax.bar(et, v, color=col, width=0.55)
    for b, x in zip(barras, v):
        ax.text(b.get_x() + b.get_width() / 2, x + 1.5, f"{x:.0f} %",
                ha="center", fontsize=9.5, color=TINTA)
    ax.set_ylim(0, 70)
    ax.set_ylabel("Sesiones de alta volatilidad")
    ax.set_title("El bloque de test cayó en otro régimen de mercado", pad=10)
    ax.text(0.015, 0.95,
            "el filtro se propone DESPUÉS de ver este salto:\npor eso es diagnóstico, no validación",
            transform=ax.transAxes, fontsize=8, color=GRIS, va="top")
    fig.tight_layout()
    p = FIGS / "fig_regimen.png"
    fig.savefig(p, bbox_inches="tight")
    plt.close(fig)
    return p


if __name__ == "__main__":
    estilo()
    for f in (fig_latencia, fig_regimen):
        p = f()
        print(f"escrita {p.relative_to(RAIZ)}")
