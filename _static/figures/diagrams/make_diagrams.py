#!/usr/bin/env python3
"""Solver-coupling diagrams of the online documentation.

    python3 make_diagrams.py        # writes <name>.svg and <name>.png here

framework_overview  dsmcFoamAblation, its regions and models, inputs, external
                    codes used for verification, planned blocks
coupling_window     one DSMC step and the gas-solid coupling window
impact_path         the path of one gas-surface impact and the per-step and
                    per-update surface processes

The content follows dsmcFoamAblation.C (time loop), dsmcCloud::evolve() and
conjugateRegionsCoupling.H; update it when those change.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Nimbus Roman", "Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "svg.fonttype": "path",
})

INK = "#222222"
STYLE = {
    "input":    dict(fc="#e8f3ea", ec="#2e7d32", ls="-"),
    "gas":      dict(fc="#e6eef8", ec="#1f4e8c", ls="-"),
    "surface":  dict(fc="#fdf0e2", ec="#b35900", ls="-"),
    "sub":      dict(fc="#fffaf3", ec="#b35900", ls="-"),
    "solid":    dict(fc="#efe9e4", ec="#6d4c41", ls="-"),
    "mesh":     dict(fc="#f2f2f2", ec="#555555", ls="-"),
    "frame":    dict(fc="none",    ec="#333333", ls="-"),
    "external": dict(fc="#ffffff", ec="#777777", ls="--"),
    "planned":  dict(fc="#fafafa", ec="#9e9e9e", ls=":"),
    "output":   dict(fc="#f7f7f7", ec="#555555", ls="-"),
    "plain":    dict(fc="#ffffff", ec="#444444", ls="-"),
}
TITLE_SIZE = 10.5
TEXT_SIZE = 8.8


def new(w, h):
    fig = plt.figure(figsize=(w/10, h/10))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def box(ax, x0, y0, x1, y1, title, lines=(), kind="plain", lw=1.2,
        title_top=True, align="center", grey=False):
    s = STYLE[kind]
    ax.add_patch(FancyBboxPatch(
        (x0, y0), x1 - x0, y1 - y0,
        boxstyle="round,pad=0,rounding_size=1.2",
        fc=s["fc"], ec=s["ec"], ls=s["ls"], lw=lw, zorder=1))
    col = "#777777" if grey else INK
    xc = (x0 + x1)/2 if align == "center" else x0 + 1.4
    ha = "center" if align == "center" else "left"
    y = y1 - 1.9
    if title:
        ax.text(xc, y, title, ha=ha, va="top", fontsize=TITLE_SIZE,
                fontweight="bold", color=s["ec"] if not grey else col,
                zorder=3)
        y -= 3.0
    for ln in lines:
        ax.text(xc, y, ln, ha=ha, va="top", fontsize=TEXT_SIZE, color=col,
                style="italic" if grey else "normal", zorder=3)
        y -= 2.45
    return (x0, y0, x1, y1)


def arrow(ax, p0, p1, label=None, at=None, rad=0.0, ls="-", color=INK,
          both=False, lw=1.3, size=TEXT_SIZE, ha="center", va="center"):
    a = FancyArrowPatch(p0, p1, arrowstyle="<|-|>" if both else "-|>",
                        mutation_scale=11, lw=lw, color=color, ls=ls,
                        connectionstyle=f"arc3,rad={rad}", zorder=2,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    if label:
        x, y = at if at else ((p0[0] + p1[0])/2, (p0[1] + p1[1])/2)
        ax.text(x, y, label, ha=ha, va=va, fontsize=size, color=color,
                zorder=4, bbox=dict(fc="white", ec="none", pad=0.6))


def save(fig, name):
    for ext in ("svg", "png"):
        fig.savefig(os.path.join(HERE, f"{name}.{ext}"), dpi=170,
                    facecolor="white")
    plt.close(fig)


# --------------------------------------------------------------------------
def framework_overview():
    W, H = 132, 92
    fig, ax = new(W, H)

    # inputs
    box(ax, 2, 76, 42, 90, "Frozen species database",
        ["NIST WebBook spectroscopy, ATcT $D_0$",
         "Gosma and Pfeiffer transport data",
         r"$\rightarrow$ rovibronic levels $(n, v, J)$"], "input")
    box(ax, 46, 76, 86, 90, "Surface chemistry input",
        ["finite-rate GS and PS steps, site sets",
         "ACA and SGC18 mechanisms",
         "SPARTA mechanism import"], "input")
    box(ax, 90, 76, 130, 90, "Solid properties",
        [r"$\rho$, $k(T)$, $c_p(T)$, emissivity",
         r"$T_\mathrm{melt}$, latent heat $L$",
         "melt film and droplet options"], "input")

    # the executable (title in the bottom-right band, clear of the arrows)
    box(ax, 2, 10, 101, 70, "", kind="frame", lw=1.8)
    ax.text(99.5, 14.6, "dsmcFoamAblation", ha="right", va="center",
            fontsize=TITLE_SIZE + 0.5, fontweight="bold", color="#333333")
    ax.text(99.5, 11.9, "one executable, one Time, parallel (-allRegions)",
            ha="right", va="center", fontsize=TEXT_SIZE - 0.6,
            color="#333333")

    box(ax, 4, 32, 31, 64, "Gas region (DSMC)",
        ["parcels carry $(n, v, J)$",
         "VSS collisions (pair data)",
         "Larsen-Borgnakke relaxation",
         "QK dissociation,",
         r"SR-$\mu$TST exchange,",
         "recombination by",
         "detailed balance"], "gas")

    box(ax, 37, 22, 67, 64, "Gas-surface interaction", kind="surface")
    box(ax, 38.5, 42, 65.5, 59.5, "Body-fitted walls",
        ["diffuse, CLL, TD, impulsive, adiabatic",
         r"exact $O(1)$ internal-state sampler",
         "per-face wall temperature $T_w$",
         "finite-rate engine: coverages,",
         "GS impacts, PS kinetics"], "sub", lw=1.0)
    box(ax, 38.5, 25.5, 65.5, 40.5, "Immersed surfaces",
        ["implicit (level set) or explicit (STL)",
         "probability or mechanism chemistry",
         "recession; explicit hands over",
         "to implicit when degraded"], "sub", lw=1.0)
    ax.text(52, 23.0, "reaction heat and removal ledger", ha="center",
            va="center", fontsize=TEXT_SIZE - 0.6, color="#b35900",
            style="italic")

    box(ax, 73, 32, 99, 64, "Solid regions",
        ["enthalpy-form conduction",
         r"with $k(T)$, $c_p(T)$",
         r"re-radiation $\varepsilon\sigma T^4$",
         "Stefan melting,",
         "melt film, droplets",
         "recession on the moving",
         "solid mesh; several",
         "couplings, parallel"], "solid")

    box(ax, 37, 12, 67, 19.5, "Gas mesh motion",
        ["dynamicFvMesh; parcels relocated"], "mesh")

    # arrows inside the executable
    arrow(ax, (31, 50), (37, 50), both=True)
    ax.text(34, 53.2, "impacts,\nproducts", ha="center", va="bottom",
            fontsize=TEXT_SIZE - 0.8)
    arrow(ax, (67, 55), (73, 55))
    ax.text(70, 57.0, r"$q$, $\dot m$, $F$", ha="center", va="bottom",
            fontsize=TEXT_SIZE - 0.4)
    arrow(ax, (73, 47), (67, 47))
    ax.text(70, 45.0, "$T_w$", ha="center", va="top",
            fontsize=TEXT_SIZE - 0.2)
    ax.text(70, 40.6, "window,\nAMI", ha="center", va="top",
            fontsize=TEXT_SIZE - 1.4, color="#555555")
    arrow(ax, (86, 32), (67, 16.5), rad=-0.15)
    ax.text(84.5, 24.5, "wall\ndisplacement", ha="left", va="center",
            fontsize=TEXT_SIZE - 0.6)
    arrow(ax, (37, 16), (17.5, 32), rad=-0.15)
    ax.text(14.5, 22.0, "moved gas\nmesh", ha="center", va="center",
            fontsize=TEXT_SIZE - 0.6)

    # inputs into the regions
    arrow(ax, (22, 76), (18, 64))
    arrow(ax, (66, 76), (55, 64))
    arrow(ax, (110, 76), (88, 64))

    # outputs
    box(ax, 2, 1, 101, 7.5, "", kind="output", lw=1.0)
    ax.text(51.5, 4.25, "Outputs: gas fields, wall and surface data, "
            "conjugate window records, restart of every region",
            ha="center", va="center", fontsize=TEXT_SIZE)
    arrow(ax, (51.5, 10), (51.5, 7.5))

    # external codes (verification) and planned blocks
    box(ax, 105, 36, 130, 70, "External references",
        ["SPARTA: twins for walls,",
         "immersed surfaces,",
         "recession",
         "PICLas: catalysis and",
         "ablation cross-checks",
         "Python oracles: QK rates,",
         "$K_{eq}$, surface mechanisms",
         "PATO: file hand-shake",
         "(frozen)"], "external")
    arrow(ax, (105, 53), (101, 53), ls="--", color="#777777")
    ax.text(103, 55.5, "verification", ha="center", va="bottom",
            fontsize=TEXT_SIZE - 1.4, color="#777777", rotation=90)
    box(ax, 105, 10, 130, 32, "Planned",
        ["QK gas-surface chemistry",
         "(B11)",
         "composite surfaces (B7)",
         "solid under the immersed",
         "surface (B9)"], "planned", grey=True)

    save(fig, "framework_overview")


# --------------------------------------------------------------------------
def coupling_window():
    W, H = 132, 56
    fig, ax = new(W, H)

    # gas time line
    y_g = 32
    arrow(ax, (4, y_g), (128, y_g), lw=1.4)
    ax.text(128, y_g + 1.6, r"gas time $t$", ha="right", va="bottom",
            fontsize=TEXT_SIZE)
    for k in range(10):
        x = 8 + 6*k
        ax.plot([x, x], [y_g - 0.9, y_g + 0.9], color=INK, lw=1.0)
    ax.plot([68, 68], [y_g - 2.2, y_g + 2.2], color="#b35900", lw=2.0)
    for k in range(1, 9):
        x = 68 + 6*k
        ax.plot([x, x], [y_g - 0.9, y_g + 0.9], color=INK, lw=1.0)
    ax.text(38, y_g - 2.2, r"window $k$: $N$ DSMC steps of $\Delta t$",
            ha="center", va="top", fontsize=TEXT_SIZE)
    ax.text(92, y_g + 1.6, r"window $k+1$", ha="center", va="bottom",
            fontsize=TEXT_SIZE)

    box(ax, 6, 36.5, 66, 54, "Each DSMC step (dsmcCloud::evolve)",
        ["1  move parcels; wall and immersed-surface interactions",
         "2  collisions, Larsen-Borgnakke relaxation, QK chemistry",
         "3  surface kinetics (PS steps) on every surface element",
         "4  sampling; walls add $q$, $\\dot m$, $F$ per face to the",
         r"    window sums ($O(1)$ per impact, no face loop)"],
        "gas", align="left")
    arrow(ax, (36, 36.5), (36, y_g + 1.2), lw=1.0)

    # solid time line
    y_s = 13
    arrow(ax, (68, y_s), (128, y_s), lw=1.4, color="#6d4c41")
    ax.text(128, y_s - 1.6, r"solid time $t_s$", ha="right", va="top",
            fontsize=TEXT_SIZE, color="#6d4c41")
    for k in range(9):
        x = 70 + 6*k
        ax.plot([x, x], [y_s - 0.9, y_s + 0.9], color="#6d4c41", lw=1.0)
    ax.text(94, y_s - 1.6, r"$M$ solid steps of $\Delta t_s$",
            ha="center", va="top", fontsize=TEXT_SIZE, color="#6d4c41")
    box(ax, 4, 1, 60, 11.5, "Each solid step",
        [r"conduction ($k(T)$, $c_p(T)$), re-radiation, Stefan melting,",
         "melt film and droplets, recession of the solid mesh (ALE)"],
        "solid", align="left")
    arrow(ax, (60, 6), (69.5, y_s - 1.0), lw=1.0, color="#6d4c41")

    # exchanges at the window end
    arrow(ax, (68, y_g - 2.4), (68, y_s + 1.2), color="#b35900", lw=1.6)
    ax.text(66.5, 22.5, "AMI gas $\\rightarrow$ solid:\nwindow-averaged\n"
            r"$q$, $\dot m$, $F$ per face", ha="right", va="center",
            fontsize=TEXT_SIZE, color="#b35900")
    arrow(ax, (119, y_s + 1.2), (71.5, y_g - 1.2), color="#6d4c41", lw=1.6)
    ax.text(104, 26.5, "AMI solid $\\rightarrow$ gas:\n$T_w$ per face;\n"
            "wall displacement $\\rightarrow$\ngas mesh update",
            ha="left", va="center", fontsize=TEXT_SIZE, color="#6d4c41")

    ax.text(2, 21.5, "The solid clock may run ahead\nof the gas clock "
            r"($M\Delta t_s \geq N\Delta t$)" "\nwhen the flow is "
            "quasi-steady.", ha="left", va="center", fontsize=TEXT_SIZE,
            color="#444444", style="italic")

    save(fig, "coupling_window")


# --------------------------------------------------------------------------
def impact_path():
    W, H = 120, 86
    fig, ax = new(W, H)

    box(ax, 30, 77, 90, 85, "One gas-surface impact",
        ["a parcel reaches a wall face or an immersed-surface element"],
        "gas")
    box(ax, 38, 64, 82, 72, "Surface model of that surface",
        ["selected in boundariesDict or for the immersed surface"],
        "plain")
    arrow(ax, (60, 77), (60, 72))

    cols = [
        (2, 38, "Kernel wall",
         ["diffuse, CLL, TD, impulsive or",
          "adiabatic kernel at $T_w$",
          "internal state $(n, v, J)$ from",
          r"the exact $O(1)$ sampler",
          r"$\rightarrow$ re-emitted parcel"]),
        (42, 78, "Probability chemistry",
         [r"reaction draw with $\beta(T_w)$",
          "or a fixed probability;",
          "products emitted, bulk atoms",
          "booked; otherwise the kernel",
          r"$\rightarrow$ products or re-emission"]),
        (82, 118, "Finite-rate mechanism",
         ["site drawn from the coverages;",
          "GS step: adsorb, react with the",
          "adsorbate or the bulk, or scatter;",
          "coverages and bulk updated",
          r"$\rightarrow$ products or re-emission"]),
    ]
    for x0, x1, title, lines in cols:
        box(ax, x0, 38, x1, 58, title, lines, "surface")
        arrow(ax, (60, 64), ((x0 + x1)/2, 58), rad=0.0)

    box(ax, 10, 24, 110, 32, "Energy and mass ledgers",
        ["reaction heat from 0 K formation enthalpies; removed bulk atoms; "
         r"window sums $q$, $\dot m$, $F$ per face"], "solid")
    for x0, x1, _, _ in cols:
        arrow(ax, ((x0 + x1)/2, 38), ((x0 + x1)/2, 32))

    box(ax, 2, 1, 58, 17, "Between impacts, every DSMC step",
        ["PS kinetics on each surface element",
         "(desorption, Langmuir-Hinshelwood):",
         "exponential, SPARTA time counter",
         "or exact stochastic integration"], "sub")
    box(ax, 62, 1, 118, 17, "Every recession update",
        [r"body-fitted wall $\rightarrow$ point displacement",
         r"implicit surface $\rightarrow$ level-set rise with",
         "swept volume = removed volume",
         r"explicit surface $\rightarrow$ vertex motion"], "sub")
    arrow(ax, (90, 24), (90, 17))
    ax.text(91.2, 20.5, "removed atoms", ha="left", va="center",
            fontsize=TEXT_SIZE - 0.6)

    save(fig, "impact_path")


if __name__ == "__main__":
    framework_overview()
    coupling_window()
    impact_path()
