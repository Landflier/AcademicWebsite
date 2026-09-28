--- 
title : "My plotting setup for gnuplot" 
date : "2026-09-28" 
tags : ["resesarch", "design", "visualization"] 
author : "Vasil R Yordanov" 
type : "blog" draft: "false" ---

# Why I chose gnuplot 

With so many options for plotting - Python libraries such
as matplotlib, seaborn; R; Julia; and the must-not-be-named bloatware
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




##

## References

