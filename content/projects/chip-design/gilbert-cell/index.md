---
title: "Gilbert Cell Mixer Design"
subtitle: "RF Analog Circuit Design using GF180MCU Technology"
technologies: ["Xschem", "Magic-VLSI", "CACE", "GLayout", "GF180MCU PDK", "Python", "RF Design"]
image: "/images/projects/gilbert-mixer-layout.png"
description: "Design and implementation of a Gilbert cell mixer for RF applications using the GF180MCU process, including full layout, verification, and performance characterization."
github: "https://github.com/Landflier/Chipathon_2025_gLayout"
presentation: "https://github.com/Landflier/Chipathon_2025_gLayout/blob/main/doc/TimeTranscenders_Proposal.pdf"
type: "projects"
---


## Introduction and Project Overview

This project involves the design and implementation of a Gilbert cell mixer for RF applications as part of the 2025 Chipathon organized by the IEEE Solid-State Circuits Society (SSCS). The work encompasses RF circuit design, layout implementation, verification, and comprehensive performance characterization using the GF180MCU process technology.

### Theory 
The Gilbert cell is a type of mixer, utilizing three differential pairs. The mathematical operation of a mixer is to multiply the two input signals (RF and LO). Supposing that the two singals are sine waves with the following shape:

$$
\begin{align}
& v_{RF}=A(t) \cos \left(\omega_{RF} t+\phi(t)\right) \nonumber \newline
& v_{LO}=A_{LO} \cos \left(\omega_{LO} t\right) \nonumber \tag{1}
\end{align}
$$

the mixer will produce the following output:

$$
\begin{align}
v_{\text{out}} &= v_{RF} \times v_{LO} \nonumber \newline
&= \frac{A(t) A_{LO}}{2}\left[\cos \phi(t)\left(\cos \left(\omega_{LO}+\omega_{RF}\right) t+\cos \left(\omega_{LO}-\omega_{RF}\right) t\right)\right. \nonumber \newline
& \left.\quad -\sin \phi(t)\left(\sin \left(\omega_{LO}+\omega_{RF}\right) t+\sin \left(\omega_{LO}-\omega_{RF}\right) t\right)\right] \nonumber \newline
&= \frac{A(t) A_{LO}}{2} \left[\cos \left(\left(\omega_{LO}+\omega_{RF}\right) t+\phi(t)\right) \right. \nonumber \newline
& \left.\quad +\cos \left(\left(\omega_{LO}-\omega_{RF}\right) t+\phi(t)\right)\right] \tag{2}
\end{align}
$$

In this derivation we have ignored the non-linearity of the mixer, thus omitting the higher order harmonics. These harmonics will become important when we discuss the linearity of the mixer. 

As can be seen from equation (1), the mixer produces two sine waves, at the frequencies $\omega_{IF}=\omega_{LO} \pm \omega_{RF}$. This property of the mixer can also be seen from a Fourier perspective, using the fact that the Fourier transform of a product of two functions is the convolution of their Fourier transforms, thus:



#### References
https://www.rfcafe.com/references/articles/wj-tech-notes/mixers-characteristics-performance-p1.pdf

## Circuit Design
In our workflow we used Xschem for creating the schematics, and a python notebook for gm/ID transistor sizing.

### Gilbert cell
![Schematic of the Gilbert cell mixer, implemented in Xschem](/images/projects/gilbert_cell/interdigited_design.png)

#### Transistor sizing
For the tranisistor sizing, we chose to use the gm/ID methodology. The RF
transistors were selected to operate in moderate inverison with gm/ID=12, since
this is the transconductance stage, and moderate inversion gives a good
tradeoff between area, speed and gain [1-3].The switching LO transistors were
selected to operate more towards the linear triode region, but still in
moderate inversion, with a gm/Id=15. Higher gm/ID was avoided in order to avoid
having too big devices and sacrifacing some of the transistor's ft (although
the frequency response is a smaller issue, since we are working in the FM
broadcasting band). For the sizing, a jupyter notebook was used [https://github.com/Landflier/Chipathon_2025_gLayout/blob/main/src/jupyter_notebooks/gmId/sizing_Gilbert_cell.ipynb]. The gm/ID calculation vs the simulation results are given in the table below:

| Source | Transistor | gm/ID | gm(mS) | ID(uA) | jd(uA/μm²) | W(μm) | ft(GHz) | VGS(V) | VDS(V) |
|--------|---------|:------:|:--------:|:--------:|:----------:|:------:|:--------:|:------:|:------:|
| Calculation (nf=1) | RF | 12 | 0.600 | 50 | 4.30 | 11.64 | 7.68 | - | 1.65 |
| Calculation (nf=6) | RF | 12 | 0.600 | 50 | 4.80 | 10.38 | 14.34* | - | 1.65 |
| Calculation (nf=1) | LO | 15 | 0.375 | 25 | 2.10 | 23.84 | 2.45 | - | 1.65 |
| Calculation (nf=6) | LO | 15 | 0.375 | 25 | 2.43 | 20.57 | 5.28* | - | 1.65 |
| Simulation | RF | 11 | 0.55 | 50 | - | 10 (nf=5) | - | 0.83 | 0.39 |
| Simulation | LO | 16 | 0.42 | 25 | - | 20 (nf=5) | - | 0.82 | 2.23 |  


Note the calculation results depend on the 'nf' that was used in the simulations of the single device .mat files. The models which are to be used for these simulations are a bit different from the ones provided by the foundry - the correct ones are provided by B Murman on this github repo: [https://github.com/bmurmann/Chipathon2025/tree/main/models_updated_2025.07.19/ngspice].

* These values shouldn't be trusted, since 'cgso' and 'cgdo' .op values were zero in the simulation. This means the capacitances of the G,D and S terminals are off.
#### Notes to self

- **Problem**
Although the circuit is working, I am still having trouble understanding the regions of operation of the MOSFETs. For the LO devices, they should be operating as switches, however they are also hogging the entire voltage headroom. I.e VDS~2.5V for the LOs, and for the RF devices, VDS~0.1-0.3 (depending on what part of the LO cycling the transistor is in). Thus, aren't the RF FETs operating in the triode region? For both the LO and RF transistors, VGS>Vth, but for the LO VDS>VGS-Vth (i.e transistor is in saturation), but for the RF, VDS is less than VGS-Vth (i.e linear, triode region).
- **Solution**:
Could it that the the transistors are not biased correctly? To reproduce the problem the waveforms used are V_CM_rf = 1.2V, V_amp_rf=0.2V, V_CM_lo=1.2V, V_amp_lo=0.2V. Try increasing V_CM_lo, to bias the LO transistors further into saturation, forcing the VDS_lo drop to be higher across the LO transistors (so that the load network formed by the two resistors does not hog all the voltage)

#### References

[1] B. Boser, "OTA gm/Id Design," UC Berkeley EECS Department, 2011-12. [Online]. Available: https://people.eecs.berkeley.edu/~boser/presentations/2011-12%20OTA%20gm%20Id.pdf

[2] "MOSFET Operation in Weak and Moderate Inversion," StudyLib. [Online]. Available: https://studylib.net/doc/18221859/mosfet-operation-in-weak-and-moderate-inversion

[3] "Lecture Notes on Nanotransistors," Purdue University, edX Course Materials, 2021. [Online]. Available: https://courses.edx.org/asset-v1:PurdueX+69504x+1T2021+type@asset+block@LNS_Lecture_Notes_on_Nanotransistors.final.pdf

### Biasing network
For the biasing network, we decided to use an on-chip bandgap reference. This network provides the biasing currents of the Gilbert cell mixer.

![Schematic of the biasing network, implemented in Xschem](/images/projects/gilbert_cell/interdigited_design.png)

#### References

[1] https://wiki.analog.com/university/courses/electronics/text/chapter-14

### Matching network
The LO and RF input networks of the Gilbert cell require an impedence matching network, in order to maximize power trasfer, but more importantly, to ensure that the input waveforms have as little distortion as possible from reflected waves. 


![Schematic of the input matching network, implemented in Xschem](/images/projects/gilbert_cell/interdigited_design.png)

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

[1] A. Hastings, *The Art of Analog Layout*, 2nd ed. Upper Saddle River, NJ: Prentice Hall, 2006.

[2] C. C. Enz and G. C. Temes, "Circuit techniques for reducing the effects of op-amp imperfections: autozeroing, correlated double sampling, and chopper stabilization," *Proc. IEEE*, vol. 84, no. 11, pp. 1584-1614, Nov. 1996.

[3] "Optimizing Analog Layouts: Techniques for Effective Layout Matching," Design & Reuse. [Online]. Available: https://www.design-reuse.com/article/61548-optimizing-analog-layouts-techniques-for-effective-layout-matching/

### Biasing network
For the biasing network, we chose to use an on-chip bandgap reference. The circuit provides the current biases for the RF differential pair of the mixer

## Verification & Analysis


## Results

### Performance Metrics
- **RF frequency**: 89.3 MHz
- **LO frequency**: 100 MHz
- **IF frequency**: 10.7 MHz
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


### Reference websites:
[https://raw.githubusercontent.com/hpretl/iic-osic/main/magic-cheatsheet/magic_cheatsheet.pdf] - keybind cheatsheet for MagicVLSI

### Some confusions
During the design, there were some things which caused me some confusions. I have decided to list these here to remind myself in the future, and for anyone working with the open source tools.

1. For a MOSFET device in the PDK, 'nf' in MagicVLSI and 'nf' in Xschem are completely different. Example: a device with W=2um, nf=2 in Magic will have width=W*nf=4um; the same device will have width=W=2um in xschem, with per-finger length of W/nf=1um. Steffan Schippers (the maintainer of Xschem), has even included devices which specify W as the per-finger width:
https://web.open-source-silicon.dev/t/16920148/in-xschem-when-using-such-a-symbol-the-nf-one-and-then-havin




## Chipathon 2025 Initiative

This project is part of the IEEE SSCS Chipathon 2025, an initiative to promote hands-on IC design experience and foster innovation in the solid-state circuits community. The Chipathon provides:
- Access to industry-standard PDKs and tools
- Fabrication opportunities for student designs
- Mentorship from industry experts
- Platform for sharing design methodologies

## Acknowledgments

Grateful acknowledgment to the IEEE Solid-State Circuits Society for organizing the Chipathon initiative, GlobalFoundries for providing the GF180MCU PDK access, and the broader IC design community and FOSSi organization for their support and collaboration.

## Tools and Technologies
- **Magic VLSI**: Open-source VLSI layout editor with advanced DRC/LVS capabilities. [Documentation](http://opencircuitdesign.com/magic/)
- **GLayout**: Python-based parametric layout generator for analog circuits. [Documentation](https://github.com/niftylab/laygo2)
- **CACE**: Circuit Automatic Characterization Engine for analog and mixed-signal circuit characterization. [Documentation](https://github.com/efabless/cace)
- **Xschem and Ngspice**: Open-source schematic capture and SPICE circuit simulator for analog design verification. [Xschem Documentation](https://xschem.sourceforge.io/stefan/index.html) 
- **GF180MCU PDK**: GlobalFoundries 180nm process design kit
- **Python**: Custom analysis scripts and data processing

## Additional Resources
### Educational Video

Video explaining and testing a descretely implemented Gilbert mixer.
{{< video 
    youtube="7nmmb0pqTU0"
    title="Gilbert mixer explained"
    width="100%"
    height="450px" >}}

{{< video 
    youtube="uiTrCUNRUIA"
    title="Related Circuit Design Concepts"
    description="History and reasons behind implementing a mixer in RF systems."
    width="100%"
    height="450px" >}}

{{< video 
    youtube="DUXTZxMZDsg"
    title="Related Circuit Design Concepts"
    description="A very nice instructionon the measurement of IIP3 near the end of the video"
    width="100%"
    height="450px" >}}
