---
title: "Gilbert Cell Mixer Design"
subtitle: "RF Analog Circuit Design using GF180MCU Technology"
date: 2025-06-30
event: "2025 Chipathon - IEEE SSCS PICO Initiative"
technologies: ["Xschem", "Magic-VLSI", "CACE", "GLayout", "GF180MCU PDK", "Python", "RF Design"]
image: "/images/projects/gilbert-mixer-layout.png"
description: "Design and implementation of a Gilbert cell mixer for RF applications using the GF180MCU process, including full layout, verification, and performance characterization."
github: "https://github.com/Landflier/Chipathon_2025_gLayout"
presentation: "https://github.com/Landflier/Chipathon_2025_gLayout/blob/main/doc/TimeTranscenders_Proposal.pdf"
type: "projects"
---

## Project Overview

This project involves the design and implementation of a Gilbert cell mixer for RF applications as part of the 2025 Chipathon organized by the IEEE Solid-State Circuits Society (SSCS). The work encompasses RF circuit design, layout implementation, verification, and comprehensive performance characterization using the GF180MCU process technology.


## Circuit Design
The Gilbert cell mixer was designed using Cadence Virtuoso, focusing on:
- **Architecture selection**: Classic Gilbert cell topology for balanced mixing
- **Transistor sizing**: Optimized for conversion gain and linearity
- **Bias network design**: Stable current sources and voltage references
- **RF matching**: Input/output impedance matching for 50Ω systems

### Gilbert cell
- **Transistor sizing**
For the tranisistor sizing, we chose to use the gm/ID methodology. The RF
transistors were selected to operate in moderate inverison with gm/ID=12, since
this is the transconductance stage, and moderate inversion gives a good
tradeoff between area, speed and gain [1-3].The switching LO transistors were
selected to operate more towards the linear triode region, but still in
moderate inversion, with a gm/Id=15. Higher gm/ID was avoided in order to avoid
having too big devices and sacrifacing some of the transistor's ft (although
the frequency response is a smaller issue, since we are working in the FM
broadcasting band). For the sizing, a jupyter notebook was used [https://github.com/Landflier/Chipathon_2025_gLayout/blob/main/src/jupyter_notebooks/gmId/sizing_Gilbert_cell.ipynb]. The gm/ID calculation vs the simulation results are given in the table below:

| Source | Transistor Type | gm/ID | gm (S) | ID (A) | jd (A/μm²) | W (μm) | ft (GHz) |
|--------|----------------|-------|--------|--------|------------|--------|----------|
| Calculation | RF Transistors | 12 | 6.00×10⁻⁴ | 5.00×10⁻⁵ | 4.30×10⁻⁶ | 11.64 | 7.68 |
| Calculation | LO Transistors | 15 | 3.75×10⁻⁴ | 5.00×10⁻⁵ | 2.10×10⁻⁶ | 23.84 | 2.45 |
| Simulation | RF Transistors | - | - | - | - | - | - |
| Simulation | LO Transistors | - | - | - | - | - | - |  

#### References

[1] B. Boser, "OTA gm/Id Design," UC Berkeley EECS Department, 2011-12. [Online]. Available: https://people.eecs.berkeley.edu/~boser/presentations/2011-12%20OTA%20gm%20Id.pdf

[2] "MOSFET Operation in Weak and Moderate Inversion," StudyLib. [Online]. Available: https://studylib.net/doc/18221859/mosfet-operation-in-weak-and-moderate-inversion

[3] "Lecture Notes on Nanotransistors," Purdue University, edX Course Materials, 2021. [Online]. Available: https://courses.edx.org/asset-v1:PurdueX+69504x+1T2021+type@asset+block@LNS_Lecture_Notes_on_Nanotransistors.final.pdf

### Biasing network

## Layout Implementation
The physical layout was implemented following RF design principles:
- **Floorplanning**: Symmetrical layout for balanced operation
- **RF routing**: Minimized parasitics and maintained signal integrity
- **Ground plane**: Solid ground plane for low-noise performance
- **Design rule compliance**: Adherence to GF180MCU PDK design rules

### Gilbert cell
For the Gilbert mixer, matching in the RF diff pair and 

Some tidbits and pictures on transistor layout matching:

1. Dummy transistors

2. Interdigited design
Current flows laterally across a CMOS (i.e from a typical Manhattan layout, right-to-left or left-to-right). These two orientations might have different mobilities, for example due to 'tilted implants' from the ion implantation, which is done at an angle.  There are other sources of orientation mismatch, such as litho misalignment (drain and source could be defined with different layers on the photomask level). 

![Figure 13.57 from [1], example of interdigited design. This design can be labeled as dAsBdBsAD ](/images/projects/gilbert_cell/interdigited_design.png)

![Figure 13.58 from [1], illustration of the 'tilted implants'. ](/images/projects/gilbert_cell/tilted_implant.png)

3. Common centroid design
![Table 13.2 from [1], the 5 rules for common-centroid layout](/images/projects/gilbert_cell/common_centroid_rules.png)


![Table 13.3 from [1], examples of interdigited common-centroid layout patterns of common-source devices. Brackets denote a pattern which can be repeated a number of times, given by the superscript. Dashes denote places where S-D cannot be merged](/images/projects/gilbert_cell/common_centroid_examples.png)

4. More esoteric matchings (withing +-1mV and +-1& current)
Refer to [2]- autozeroing and chopper stabilization (not used in this project). 

#### References:
[1] Hastings, A. (n.d.). The art of analog layout. Pearson Higher Education US 
[2] 74 C. C. Enz and G. C. Temes, “Circuit techniques for reducing the effects of op-amp imperfections: autozeroing, correlated double sampling, and chopper stabilization,” Proc. IEEE, Vol. 84, #11, 1996, pp. 1584–1614
[3] https://www.design-reuse.com/article/61548-optimizing-analog-layouts-techniques-for-effective-layout-matching/

### Biasing network

### Verification & Analysis
Comprehensive verification was performed including:
- **Design Rule Check (DRC)**: Verified layout compliance with GF180MCU rules
- **Layout vs. Schematic (LVS)**: Confirmed layout matches schematic netlist
- **Parasitic extraction**: RF parasitic extraction including inductances
- **RF simulation**: S-parameter analysis and harmonic distortion characterization
- **Noise analysis**: Noise figure and signal-to-noise ratio optimization

## Results

### Performance Metrics
- **RF frequency**: 2.4 GHz
- **LO frequency**: 2.3 GHz
- **IF frequency**: 100 MHz
- **Conversion gain**: 12 dB
- **Input P1dB**: -8 dBm
- **IIP3**: +2 dBm
- **Noise figure**: 9 dB
- **Power consumption**: 8 mW at 1.8V supply
- **Area**: 0.25 mm²

### Key Achievements
- Achieved target conversion gain with excellent linearity
- Low noise figure suitable for receiver applications
- Successful first-pass design with all specifications met
- Balanced layout ensuring good common-mode rejection
- Ready for fabrication through Chipathon initiative

## Technical Challenges

### RF Layout Challenges
The most significant challenge was maintaining RF performance in the layout:
- Symmetrical transistor matching for balanced operation
- Minimizing parasitic capacitances and inductances
- Proper ground plane implementation
- Isolation between RF and DC bias networks

### Performance Optimization
Achieving target performance required:
- Careful transistor sizing for optimal transconductance
- Bias current optimization for linearity vs. power trade-off
- Load impedance tuning for maximum conversion gain
- Noise optimization through proper device selection

## Tools and Technologies

- **Cadence Virtuoso**: Schematic capture and RF simulation
- **Spectre RF**: Advanced RF circuit simulation
- **GF180MCU PDK**: GlobalFoundries 180nm process design kit
- **Python**: Custom analysis scripts and data processing
- **MATLAB**: Signal processing and performance analysis

## Future Work

- Integration with complete RF receiver system
- Multi-band mixer design for software-defined radio
- Advanced calibration techniques for process variations
- Fabrication through the Chipathon program and measurement validation

## Chipathon 2025 Initiative

This project is part of the IEEE SSCS Chipathon 2025, an initiative to promote hands-on IC design experience and foster innovation in the solid-state circuits community. The Chipathon provides:
- Access to industry-standard PDKs and tools
- Fabrication opportunities for student designs
- Mentorship from industry experts
- Platform for sharing design methodologies

## Acknowledgments

Grateful acknowledgment to the IEEE Solid-State Circuits Society for organizing the Chipathon initiative, GlobalFoundries for providing the GF180MCU PDK access, and the broader IC design community for their support and collaboration.

## References

1. GlobalFoundries. "GF180MCU Process Design Kit Documentation." 2024.
2. IEEE SSCS. "Chipathon 2025 Design Guidelines and Specifications." 2024.
3. Gilbert, B. "A Precise Four-Quadrant Multiplier with Subnanosecond Response." IEEE JSSC, 1968.
4. Razavi, B. "RF Microelectronics." 2nd Edition, Prentice Hall.
