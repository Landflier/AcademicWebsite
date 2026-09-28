--- 
title : "My plotting setup for gnuplot" 
date : "2026-09-28" 
tags : ["resesarch", "design", "visualization"] 
author : "Vasil R Yordanov" 
type : "blog" 
draft: "false"
---

# Why I chose gnuplot 

With so many options for plotting - Python libraries such
as matplotlib and seaborn; R; Julia; and the must-not-be-named bloatware
point-and-click programs, why did I choose gnuplot, a seemingly old-timer
plotting program? My answer is simple - gnuplot adheres to the DOTADIW principle
- do one thing, and do it well. Gnuplot also gets yearly updates and continues
to have reasonable community support. 

# Templates for gnuplot

Because I have to present results constantly in slide format,
I made several templates that I use to generate different sized figures for
presentation slides. I have four sizes - a figure that takes up an entire slide,
and figures for ÷2, ÷4, ÷8 slide sizes. The templates help me keep text
readable and consistent, regardless of the size of the figures I have in
a presentation. I also use the templates to regenerate figures from papers
I read, to have a homogenous figure style througout a presentation (I use
engauge to extract data from research figures). 

For fonts, I chose STIX Two and STIX Two Math, because the font's focus on
scientific and engineering publishing. 

I decided on the the Okabe-Ito color-palette, due to the palette's accessibility for
color-blind people. I also like the colors.

The setup relies on multiple template files connected through macros. The top-level file is
`~/.gnuplot`, defining all the different macros. 

```gnuplot
# ~/.gnuplot
# Main gnuplot startup file.
# It loads shared definitions once and defines aliases for the output profiles.

set macros

# Location of the split configuration files.
# Override this before loading ~/.gnuplot if you keep the files somewhere else.
if (!exists("GP_CONFIG_DIR")) GP_CONFIG_DIR = system("printf %s \"$HOME/.config/gnuplot\"")

load GP_CONFIG_DIR . "/common.gp"

# -----------------------------------------------------------------------------
# Profile aliases
# -----------------------------------------------------------------------------
# Usage examples:
#   @TYPST
#   set output "figure.svg"
#   plot "data.csv" u 1:2 w lp ls 1 title "data"
#
#   @PAPER
#   set output "figure.eps"
#   plot ...
#
#   @PPT
#   set output "figure.png"
#   plot ...

TYPST = "load '" . GP_CONFIG_DIR . "/typst.gp'"
PAPER_PDF = "load '" . GP_CONFIG_DIR . "/paper_pdf.gp'"

# PowerPoint profiles: default is half-slide. Quarter and full-HD variants are
# implemented through PPT_FIGSIZE and the same presentation profile file.
PPT = "PPT_FIGSIZE='half'; load '" . GP_CONFIG_DIR . "/presentation_svg.gp'"
PPT_HALF = PPT
PPT_QUARTER = "PPT_FIGSIZE='quarter'; load '" . GP_CONFIG_DIR . "/presentation_svg.gp'"
PPT_ONE_EIGHT = "PPT_FIGSIZE='one_eight'; load '" . GP_CONFIG_DIR . "/presentation_svg.gp'"
PPT_FULLHD = "PPT_FIGSIZE='fullhd'; load '" . GP_CONFIG_DIR . "/presentation_svg.gp'"
PPT_WITH_TITLE = "PPT_FIGSIZE='ppt_with_title'; load '" . GP_CONFIG_DIR . "/presentation_svg.gp'"


# Default interactive profile. Change this if you want gnuplot startup to default
# to @PAPER or @PPT instead.
@TYPST
```

Besides the .gnuplot file, there is a file that defines settings shared by all
templates. That file is:

```
# ~/.config/gnuplot/common.gp
# Shared gnuplot defaults for all figure styles.
# Loaded by ~/.gnuplot at startup.

# Enable string-macro expansion, so commands like @TYPST and @LINESET_OKABE work.
set macros

# -----------------------------------------------------------------------------
# Fonts
# -----------------------------------------------------------------------------
# For cairo/png/svg terminals, these are resolved through fontconfig / Pango.
# In WSL, make sure the fonts are installed and visible to fontconfig.
FONT_TEXT = "STIX Two Text"
FONT_MATH = "STIX Two Math"

# -----------------------------------------------------------------------------
# Shared colors
# -----------------------------------------------------------------------------
# Catppuccin Latte-like document background and foreground colors.
C_LATTE_BG      = "#eff1f5"
C_LATTE_FG      = "#4c4f69"
C_LATTE_GRID    = "#acb0be"
C_WHITE         = "#ffffff"
C_BLACK         = "#000000"

# Named Okabe-Ito colors (first 4)
okabe_blue   = "#0072B2"
okabe_orange = "#D55E00"
okabe_green  = "#009E73"
okabe_pink   = "#CC79A7"

# -----------------------------------------------------------------------------
# Shared categorical line styles
# -----------------------------------------------------------------------------
# Default choice: Okabe-Ito. It is compact, high-contrast, and color-vision-
# deficiency friendly, so it is a safe default for papers, Typst documents,
# and presentation slides.
# Use in plotting commands with: plot ... ls 1, ... ls 2, etc.
LINESET_OKABE = "\
set linetype 1 lc rgb '#0072B2' lw 2 pt 7  ps 1.4; \
set linetype 2 lc rgb '#D55E00' lw 2 pt 13 ps 1.4; \
set linetype 3 lc rgb '#009E73' lw 2 pt 9  ps 1.4; \
set linetype 4 lc rgb '#CC79A7' lw 2 pt 11 ps 1.4; \
set linetype 5 lc rgb '#E69F00' lw 2 pt 5  ps 1.4; \
set linetype 6 lc rgb '#56B4E9' lw 2 pt 3  ps 1.4; \
set linetype 7 lc rgb '#F0E442' lw 2 pt 1  ps 1.4; \
set linetype 8 lc rgb '#000000' lw 2 pt 2  ps 1.4"

# Paul Tol's Bright qualitative scheme – the author's recommended default for
# line plots. Colour-blind safe, print-friendly, distinct on screen and paper.
# Recommended cycling order: blue, red, green, yellow, cyan, purple, grey.
# Reference: https://sronpersonalpages.nl/~pault/
LINESET_TOL_BRIGHT = "\
set linetype 1 lc rgb '#4477AA' lw 2 pt 7  ps 1.4; \
set linetype 2 lc rgb '#EE6677' lw 2 pt 5  ps 1.4; \
set linetype 3 lc rgb '#228833' lw 2 pt 9  ps 1.4; \
set linetype 4 lc rgb '#CCBB44' lw 2 pt 13 ps 1.4; \
set linetype 5 lc rgb '#66CCEE' lw 2 pt 11 ps 1.4; \
set linetype 6 lc rgb '#AA3377' lw 2 pt 3  ps 1.4; \
set linetype 7 lc rgb '#BBBBBB' lw 2 pt 1  ps 1.4; \
set linetype 8 lc rgb '#000000' lw 2 pt 2  ps 1.4"

# -----------------------------------------------------------------------------
# Catppuccin palette – accent colors only (no neutrals/grayscale)
# https://catppuccin.com/palette/
# Usage: plot sin(x) lc rgb cattpuccin_mocha_blue
# -----------------------------------------------------------------------------

# Latte
cattpuccin_latte_rosewater  = "#dc8a78"
cattpuccin_latte_flamingo   = "#dd7878"
cattpuccin_latte_pink       = "#ea76cb"
cattpuccin_latte_mauve      = "#8839ef"
cattpuccin_latte_red        = "#d20f39"
cattpuccin_latte_maroon     = "#e64553"
cattpuccin_latte_peach      = "#fe640b"
cattpuccin_latte_yellow     = "#df8e1d"
cattpuccin_latte_green      = "#40a02b"
cattpuccin_latte_teal       = "#179299"
cattpuccin_latte_sky        = "#04a5e5"
cattpuccin_latte_sapphire   = "#209fb5"
cattpuccin_latte_blue       = "#1e66f5"
cattpuccin_latte_lavender   = "#7287fd"

# Frappé
cattpuccin_frappe_rosewater = "#f2d5cf"
cattpuccin_frappe_flamingo  = "#eebebe"
cattpuccin_frappe_pink      = "#f4b8e4"
cattpuccin_frappe_mauve     = "#ca9ee6"
cattpuccin_frappe_red       = "#e78284"
cattpuccin_frappe_maroon    = "#ea999c"
cattpuccin_frappe_peach     = "#ef9f76"
cattpuccin_frappe_yellow    = "#e5c890"
cattpuccin_frappe_green     = "#a6d189"
cattpuccin_frappe_teal      = "#81c8be"
cattpuccin_frappe_sky       = "#99d1db"
cattpuccin_frappe_sapphire  = "#85c1dc"
cattpuccin_frappe_blue      = "#8caaee"
cattpuccin_frappe_lavender  = "#babbf1"

# Macchiato
cattpuccin_macchiato_rosewater = "#f4dbd6"
cattpuccin_macchiato_flamingo  = "#f0c6c6"
cattpuccin_macchiato_pink      = "#f5bde6"
cattpuccin_macchiato_mauve     = "#c6a0f6"
cattpuccin_macchiato_red       = "#ed8796"
cattpuccin_macchiato_maroon    = "#ee99a0"
cattpuccin_macchiato_peach     = "#f5a97f"
cattpuccin_macchiato_yellow    = "#eed49f"
cattpuccin_macchiato_green     = "#a6da95"
cattpuccin_macchiato_teal      = "#8bd5ca"
cattpuccin_macchiato_sky       = "#91d7e3"
cattpuccin_macchiato_sapphire  = "#7dc4e4"
cattpuccin_macchiato_blue      = "#8aadf4"
cattpuccin_macchiato_lavender  = "#b7bdf8"

# Mocha
cattpuccin_mocha_rosewater = "#f5e0dc"
cattpuccin_mocha_flamingo  = "#f2cdcd"
cattpuccin_mocha_pink      = "#f5c2e7"
cattpuccin_mocha_mauve     = "#cba6f7"
cattpuccin_mocha_red       = "#f38ba8"
cattpuccin_mocha_maroon    = "#eba0ac"
cattpuccin_mocha_peach     = "#fab387"
cattpuccin_mocha_yellow    = "#f9e2af"
cattpuccin_mocha_green     = "#a6e3a1"
cattpuccin_mocha_teal      = "#94e2d5"
cattpuccin_mocha_sky       = "#89dceb"
cattpuccin_mocha_sapphire  = "#74c7ec"
cattpuccin_mocha_blue      = "#89b4fa"
cattpuccin_mocha_lavender  = "#b4befe"

# Select the shared categorical set used by all profiles.
DEFAULT_LINESET = LINESET_OKABE
@DEFAULT_LINESET

# Shared continuous palette for maps/images.
# set palette cubehelix start 0.5 cycles -1.5 saturation 1

# -----------------------------------------------------------------------------
# Shared data/parsing defaults
# -----------------------------------------------------------------------------
set decimalsign '.'
# set datafile separator ','

# -----------------------------------------------------------------------------
# Axes styles
# -----------------------------------------------------------------------------
set ytics nomirror
set xtics nomirror

# -----------------------------------------------------------------------------
# Legend style
# -----------------------------------------------------------------------------
set key right top spacing 0.9

# -----------------------------------------------------------------------------
# Small convenience aliases
# -----------------------------------------------------------------------------
st = "set title"
sx = "set xlabel"
sy = "set ylabel"

# Optional: quick output alias, e.g. @so "figure.svg" is not valid gnuplot syntax,
# so use it as: eval so." 'figure.svg'" if you like; otherwise ignore.
so = "set output"
```

# Slide template

The template for slide figures is the following:

```gnuplot
# ~/.config/gnuplot/gnuplot_presentation_svg.gp
# PowerPoint / slide figure profile.
# Intended output: transparent SVG, 16:9 aspect ratio.

# Size selector. The main ~/.gnuplot aliases set PPT_FIGSIZE before loading this.
# Available values: "half", "quarter", "one_eight", "fullhd", "ppt_with_title".
if (!exists("PPT_FIGSIZE")) PPT_FIGSIZE = "half"

# --- Font-size conversion note -------------------------------------------
# A PowerPoint widescreen slide is 960 pt × 540 pt (13.33" × 7.5" at 72 pt/in).
# A fullhd SVG (1920×1080) is scaled by 0.5 when it fills the slide, so:
#   PPT visible pt = gnuplot font size × 0.5   (for fullhd variants)
# Example: gnuplot 36  →  18 pt visible in PowerPoint.
# For the half/quarter/one_eight figures the scale depends on how much of
# the slide they occupy, but they are typically used at lower magnification
# so smaller gnuplot values are appropriate.
# -------------------------------------------------------------------------


if (PPT_FIGSIZE eq "one_eight") {
    set terminal svg enhanced size 480,270 font "STIX Two Text,14" background rgb "white"
    PPT_KEY_FONT = '"STIX Two Text,13"'
} else {
if (PPT_FIGSIZE eq "quarter") {
    set terminal svg enhanced size 640,360 font "STIX Two Text,16" background rgb "white"
    PPT_KEY_FONT = '"STIX Two Text,15"'
} else {
    if (PPT_FIGSIZE eq "fullhd") {
        # 1920×1080 fills slide → scale 0.5 → gnuplot 36 ≈ 18 pt in PPT
        set terminal svg enhanced size 1920,1080 font "STIX Two Text,36" background rgb "white"
        PPT_KEY_FONT = '"STIX Two Text,34"'
    } else {
    if (PPT_FIGSIZE eq "ppt_with_title") {
        # 1920×900: leaves ~90 pt of slide height for a two-line 28 pt heading.
        # Same font calibration as fullhd (scale 0.5).
        set terminal svg enhanced size 1920,900 font "STIX Two Text,36" background rgb "white"
        PPT_KEY_FONT = '"STIX Two Text,34"'
    } else {
        set terminal svg enhanced size 960,540 font "STIX Two Text,20" background rgb "white"
        PPT_KEY_FONT = '"STIX Two Text,17"'
    }
    }
}
}


@DEFAULT_LINESET

set pointsize 1.4
# set grid back lw 1.4 lc rgb "#b8b8b8" dt 3
set border linewidth 1.8 lc rgb "black"
set tics out scale 0.9 textcolor rgb "black"
set key top right opaque box lw 1.2 spacing 1.25 width 2 samplen 1.8 \
    font @PPT_KEY_FONT textcolor rgb "black"

# Presentation notes:
# - pngcairo supports transparent PNG output via the 'transparent' terminal option.
# - If your slide background is dark, switch text/border colors to white and use
#   brighter gridlines.
# - For quarter-slide plots, use @PPT_QUARTER instead of @PPT.
```
# Paper template

Besides templates for slides, I have a template for paper figures.

```gnuplot
# ~/.config/gnuplot/paper_pdf.gp
# Academic paper figure profile.
# Intended output: PDF, single-column width.

# Matches paper_eps.gp: approximately 3.35 in wide. Adjust height if needed.
# PDF is an ISO-standard, open vector format and preserves searchable text and
# vector paths for typical publisher submission workflows.
set terminal pdfcairo enhanced color size 3.35in,2.35in font "STIX Two Text,9" \
    linewidth 1.0 background rgb "white"

@DEFAULT_LINESET

set pointsize 1.1
set grid back lw 0.7 lc rgb "#c9c9c9" dt 3
set border linewidth 1.0 lc rgb "black"
set tics out scale 0.55 textcolor rgb "black"
set key top right opaque box lw 0.7 spacing 1.05 width 1 samplen 1.4 \
    font "STIX Two Text,8" textcolor rgb "black"

# Paper notes:
# - Check the target journal's author instructions: use EPS only when it is
#   explicitly required, and use the required PDF version when one is stated.
# - If journal requires a different column width, change the terminal size.
```

# Typst template

Fascinated by typst, and excited to try it out, I also built a template for
typst documents.

```gnuplot
# ~/.config/gnuplot/typst.gp
# Typst figure profile.
# Intended output: SVG, included in Typst documents compiled with --font-path.

# SVG keeps text as text and names the font; Typst/browser rendering must be able
# to find the font.
set terminal svg enhanced size 1000,700 font "STIX Two Text,16" background rgb "#eff1f5"

# Re-apply shared categorical colors after changing terminal/profile.
@DEFAULT_LINESET

set pointsize 2.1
set grid back lw 1.0 lc rgb "#acb0be"
set border linewidth 1.4 lc rgb "#4c4f69"
set tics out scale 0.8 textcolor rgb "#4c4f69"
set key top right opaque box lw 1.0 spacing 1.25 width 2 samplen 1.6 \
    font "STIX Two Text,14" textcolor rgb "#4c4f69"

# Typst/SVG notes:
# - Use enhanced text syntax for simple super/subscripts, e.g. x^{2}, a_{0}.
# - This is not real Typst/LaTeX math rendering; for that, create labels in Typst
#   or use a LaTeX-oriented terminal in a separate workflow.
# - You can try STIX Two Math in selected labels if the SVG renderer resolves it,
#   e.g. set xlabel "{/STIX Two Math:Italic k}"
```

However, the template is not entirely polished, and a bit bare-bones.
I also had to add the STIX fonts to Typst, but I haven't tested if it renders
the gnuplot svg text correctly.

# Vim template

To streamline the creation of new gnuplots, I created a small template.gp file
that lives in ~/.vim/templates:

```vim
@PPT_ONE_EIGHT
unset grid

set output 'figures/{{FILENAME}}.svg'

# -------------------------- #
#          Data              #
# -------------------------- #

data_file = ""
# set datafile separator ","
# set datafile commentschars "#"

# -------------------------- #
#          Labels            #
# -------------------------- #

set title ''
@sx ''  offset 0,0.5
@sy '' offset 2,0

# -------------------------- #
#          Legend            #
# -------------------------- #

set key right top spacing 0.9 box width -2

# -------------------------- #
#           Plot             #
# -------------------------- #

plot \
    data_file using 1:2 with lines lw 2 dt 1 title "Curve 1" , \
```

# Installation
The installation on a Linux system requires the files to be placed in the
correct places. This is described in the README:
```markdown
mkdir -p ~/.config/gnuplot
ln -sf "$PWD/gnuplot_common.gp" ~/.config/gnuplot/common.gp
ln -sf "$PWD/gnuplot_typst.gp" ~/.config/gnuplot/typst.gp
ln -sf "$PWD/gnuplot_paper_eps.gp" ~/.config/gnuplot/paper_eps.gp
ln -sf "$PWD/gnuplot_paper_pdf.gp" ~/.config/gnuplot/paper_pdf.gp
ln -sf "$PWD/gnuplot_presentation_svg.gp" ~/.config/gnuplot/presentation_svg.gp
ln -s  "$PWD/dot_gnuplot" ~/.gnuplot
ln -sf "$PWD/template.gp" ~/.vim/templates/
```
## References

