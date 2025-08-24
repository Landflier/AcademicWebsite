---
title: "Gilbert Cell Mixer Design"
subtitle: "RF Analog Circuit Design using GF180MCU Technology"
technologies: ["Xschem", "Magic-VLSI", "CACE", "GLayout", "GF180MCU PDK", "Python", "RF Design"]
team_members: [
  {name: "Shaikh Shoeb Dawood", github: "https://github.com/shoebNTU"},
  {name: "Vasil Yordanov", github: "https://github.com/Landflier"}
]
image: "/images/projects/gilbert_cell/Gilbert_cell_icon.svg"
description: "Design and implementation of a Gilbert cell mixer for RF applications using the GF180MCU process, including full layout, verification, and performance characterization."
github: "https://github.com/Landflier/Chipathon_2025_gLayout"
presentation: "https://github.com/Landflier/Chipathon_2025_gLayout/blob/main/doc/TimeTranscenders_Proposal.pdf"
type: "projects"
---


## Introduction and Project Overview

This project involves the design and implementation of a Gilbert cell mixer for RF applications as part of the 2025 Chipathon organized by the IEEE Solid-State Circuits Society (SSCS). The work encompasses RF circuit design, layout implementation, verification, and comprehensive performance characterization using the GF180MCU process technology.

### Theory 
The Gilbert cell is a type of mixer, utilizing three differential pairs. The mathematical operation of a mixer is to multiply the two input signals (RF and LO). Supposing that the two signals are sine waves with the following shape:

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
&= \frac{A(t) A_{LO}}{2}\left[\cos \phi(t)\left(\cos \left(\omega_{LO}+\omega_{RF}\right) t+\cos \left(\omega_{LO}-\omega_{RF}\right) t\right) - \right. \nonumber \newline
& \left.\quad \phantom{=\frac{A(t) A_{L}}{2}} \sin \phi(t)\left(\sin \left(\omega_{LO}+\omega_{RF}\right) t+\sin \left(\omega_{LO}-\omega_{RF}\right) t\right)\right] \nonumber \newline
&= \frac{A(t) A_{LO}}{2} \left[\cos \left(\left(\omega_{LO}+\omega_{RF}\right) t+\phi(t)\right) + \right. \nonumber \newline
& \left.\quad \phantom{=\frac{A(t) A_{L}}{2}} \cos \left(\left(\omega_{LO}-\omega_{RF}\right) t+\phi(t)\right)\right] \tag{2}
\end{align}
$$

In this derivation we have ignored the non-linearity of the mixer, thus omitting the higher order harmonics. These harmonics will become important when we discuss the linearity of the mixer. 

As can be seen from equation (1), the mixer produces two sine waves, at the frequencies $\omega_{IF}=\omega_{LO} \pm \omega_{RF}$. This property of the mixer can also be seen from a Fourier perspective, using the fact that the Fourier transform of a product of two functions is the convolution of their Fourier transforms. But we will try to keep the math to a minimum here...

### Target specifications

In the table below we have given the metrics we aim to achieve in this project. The simulation and future measurement values are included for easy comparison.
| Metric | Target | Simulation | Measured |
|--------|:------:|:----------:|:--------:|
| RF frequency | $89.3\text{MHz}$ | $89.3\text{MHz}$ | - |
| LO frequency | $100\text{MHz}$ | $100\text{MHz}$ | - |
| IF frequency | $10.7\text{MHz}$ | $10.7\text{MHz}$ | - |
| Conversion gain | $\geq 12\text{dB}$ | $11.55\text{dB}$ | - |
| Input P1dB | $-8\text{dBm}$ | - | - |
| IIP3 | $\leq +2\text{dBm}$ | - | - |
| Noise figure | $\leq 9\text{dB}$ | - | - |

#### References
[1] RF Cafe, "Mixer Characteristics and Performance," WJ Tech Notes. [Online]. Available: https://www.rfcafe.com/references/articles/wj-tech-notes/mixers-characteristics-performance-p1.pdf

## Circuit Design
In our workflow we used Xschem for creating the schematics, and a python notebook for gm/ID transistor sizing.

### Gilbert cell
![Schematic of the Gilbert cell mixer, implemented in Xschem](/images/projects/gilbert_cell/Gilbert_cell_no_hierarchy_editted.svg)

#### Transistor sizing
For the transistor sizing, we chose to use the gm/ID methodology. The RF
transistors were selected to operate in moderate inversion with gm/ID=12, since
this is the trans-conductance stage, and moderate inversion gives a good
trade-off between area, speed and gain [1-3].The switching LO transistors were
selected to operate more towards the linear triode region, but still in
moderate inversion, with a gm/Id=15. Higher gm/ID was avoided in order to avoid
having too big devices and sacrificing some of the transistor's ft (although
the frequency response is a smaller issue, since we are working in the FM
broadcasting band). For the sizing, a [Jupyter notebook for gm/ID transistor sizing](https://github.com/Landflier/Chipathon_2025_gLayout/blob/main/src/jupyter_notebooks/gmId/sizing_Gilbert_cell.ipynb) was used. The gm/ID calculation vs the simulation results are given in the table below:

| Source | Transistor | gm/ID | gm(mS) | ID(uA) |  W(μm) | ft(GHz) | VGS(V) | VDS(V) |
|------|-------|:------:|:-------:|:--------:|:------:|:-------:|:-----:|:-----:|
| Calculation (nf=1) | RF | 12 | 0.600 | 50 | 11.64 | 7.68 | 0.69 | 1.65 |
| Calculation (nf=6) | RF | 12 | 0.600 | 50 | 10.38 | 14.34* | 0.67 | 1.65 |
| Calculation (nf=1) | LO | 15 | 0.375 | 25 | 23.84 | 2.45 | 0.64 | 1.65 |
| Calculation (nf=6) | LO | 15 | 0.375 | 25 | 20.57 | 5.28* | 0.62 | 1.65 |
| Simulation | RF | 11 | 0.55 | 50 | 10 (nf=5) | - | 0.83 | 0.39 |
| Simulation | LO | 16 | 0.42 | 25 | 20 (nf=5) | - | 0.82 | 2.23 |  


Note the calculation results depend on the 'nf' that was used in the simulations of the single device .mat files. The models which are to be used for these simulations are a bit different from the ones provided by the foundry - the correct ones are provided by B Murman on this github repo: [https://github.com/bmurmann/Chipathon2025/tree/main/models_updated_2025.07.19/ngspice].

* These values shouldn't be trusted, since 'cgso' and 'cgdo' .op values were zero in the simulation. This means the capacitancesacitances of the G,D and S terminals are off.

\* These fT values (14.34 GHz and 5.28 GHz) shouldn't be trusted, since 'cgso' and 'cgdo' .op values were zero in the simulation. This means the capacitance of the G,D and S terminals are off.

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
For the biasing network, we decided to pass in ~100uA current into a one of the chip pins, and copy that current to the mixer biasing branches and the impedance matching network using simple current mirrors. This approach was attractive for its simplicity and straightforward implementation.

![Schematic of the biasing network, implemented in Xschem](/images/projects/gilbert_cell/interdigited_design.png)

To bias the 5T-OTA buffer connected to the output of the Gilbert mixer's IF port, we decided to use a Wilson current mirror. The main reason was improving the CMRR of the OTA. [2]

#### References

[1] Analog Devices, "Chapter 14," University Courses - Electronics. [Online]. Available: https://wiki.analog.com/university/courses/electronics/text/chapter-14

[2] Sedra and Smith, Microelectronic Circuits, International Sixth Edition, eq 7.148

### Impedance matching stage

![Schematic of the input matching network, implemented in Xschem](/images/projects/gilbert_cell/5T-OTA-buffer_no_hierarchy.svg)
In order to test our circuit, we will need to attach a probe (oscilloscope, VNA) to the IF output pin of our chip. This probe will load the mixer, which has a low impedance output $R_{load} \parallel $. Therefore, to make testing possible, avoiding loading and reflecting signals, we need to design an impedance matching network, to serve as a buffer between the mixer and the testing probe. 
We decided to use a 5T-OTA, for its simplicity, high output impedance (current source) and differential to single ended output. A nice review/introduction for OpAmps vs OTAs, see [1] in this section's references.
The probe model we used in our test benches for the OTA setup, taken from a standard supplier's documentation: 

![Schematic of the input matching network, implemented in Xschem](/images/projects/gilbert_cell/Osciloscope_probe.svg)

#### References
https://people.engr.tamu.edu/spalermo/ecen474/lecture11_ee474_simple_ota.pdf

![Operational Amplifier vs Operational Trans-amplifier as an impedance matching stage. Image taken from [1]](/images/projects/gilbert_cell/Op_Amp_vs_OTA.svg)
## Layout Implementation
In RF and analog layout, device matching is paramount for the correct operation of the circuits. Below, we have included some tidbits and pictures on transistor layout matching:

1. Dummy transistors

To ensure the same operation point for devices across the physical area of the chip, dummy structures are placed to homogenize the local environment of the devices. In [3] (which is taken from a more formal source [1]), various dummy techniques are shown for resistors, capacitors and transistors.

2. Interdigited design

Current flows laterally across a CMOS (i.e from a typical Manhattan layout, right-to-left or left-to-right). These two orientations might have different mobilities, for example due to 'tilted implants' from the ion implantation, which is done at an angle.  There are other sources of orientation mismatch, such as litho misalignment (drain and source could be defined with different layers on the photo-mask level). 

![Figure 13.57 from [1], example of interdigited design. This design can be labeled as dAsBdBsAD ](/images/projects/gilbert_cell/interdigited_design.png)

![Figure 13.58 from [1], illustration of the 'tilted implants'. ](/images/projects/gilbert_cell/tilted_implant.png)

3. Common centroid design

The main consideration when doing a common centroid design are:

   **COINCIDENCE**: The centroids of the matched MOS transistors should coincide at least approximately. Ideally, the centroids should exactly coincide.

   **SYMMETRY**: The array should be symmetric around both the horizontal and vertical axes.

   **DISPERSION**: When possible, a large array should be subdivided into as many smaller arrays as possible that each satisfy the rules of coincidence and symmetry. If this can be achieved, then the larger array need not satisfy these rules; only the sub-arrays that comprise it need do so.

   **COMPACTNESS**: The array (or each of its sub-arrays) should be as compact as possible.

   **ORIENTATION**: Matched MOS transistors should possess equal orientations.

   Some examples of common-centroid interdigited designs. Brackets denote a pattern which can be repeated a number of times, given by the superscript. Dashes denote places where S-D cannot be merged

   **A**: $\left({ }_D A_S B_D B_S A\right)^i{ }_D$

   **B**: $\left({ }_S A_D A\right)^i\left({ }_S B_D B\right)^j\left({ }_S A_D A\right)^i{ }_S$

   **C**: $\left({ }_S A_D A_S B_D B_S A_D A\right)^i{ }_S$

   **D**: $\left({ }_S A_D A_S B_D-{}_S A_D A_S-{}_D B_S A_D A\right)^i{ }_S$

   **E**: $\left({ }_S A_D A_S B_D B_S C_D C\right)^i{ }_S\left(C_D C_S B_D B_S A_D A_S\right)^i$

4. More esoteric matching (withing +-1mV and +-1& current)
Refer to [2]- auto-zeroing and chopper stabilization (not used in this project). 

### Gilbert cell
As a start, we provide an estimate of the area of the project. The layout was generated and measured using Magic VLSI.


![Area estimation of the Gilbert cell, plus supporting circuitry. The length estimation was done using Magic VLSI.](/images/projects/gilbert_cell/Gilbert_area_estimation.svg)

We note that this layout does not include dummy devices, no interdigitation is implemented (which would reduce the area), and no biasing network are included. Thus, we estimate the actual design to be around $80\textit{ um}x80\textit{ um}$, for a total area of $6400 um^2$.


#### References:

[1] A. Hastings, *The Art of Analog Layout*, 2nd ed. Upper Saddle River, NJ: Prentice Hall, 2006.

[2] C. C. Enz and G. C. Temes, "Circuit techniques for reducing the effects of op-amp imperfections: autozeroing, correlated double sampling, and chopper stabilization," *Proc. IEEE*, vol. 84, no. 11, pp. 1584-1614, Nov. 1996.

[3] "Optimizing Analog Layouts: Techniques for Effective Layout Matching," Design & Reuse. [Online]. Available: https://www.design-reuse.com/article/61548-optimizing-analog-layouts-techniques-for-effective-layout-matching/

### Biasing network
For the biasing network, we have decided to pass 100uA of current through the bondbands and then, using current mirrors, to distribute 50uA to each of branches of the RF differential pair.

## Verification & Analysis
### Gilbert cell
Below are given waveforms for the output of the Gilbert mixer, in both the time and frequency domain. The circuit biasing is with ideal current sources, and both the RF and LO signals each contain a single frequency

![Time-domain simulation of the mixer, t=300ns](/images/projects/gilbert_cell/Time-series_editted.svg)
![Frequency spectrum of the mixer, with $f_{LO}=100MHz$ and $f_{RF}=89.3MHz$.](/images/projects/gilbert_cell/FFT_editted.svg)
### Impedence matching (5T-OTA)
### Biasing network
### Top level

## Testing results
The following testing equipment will be used to measure the mixer performance:
- Vector Network Analyzer (VNA) : Measures insertion loss, return loss, and isolation.
- Spectrum Analyzer : Analyzes frequency response and spurious signals.
- Signal Generators : Provides RF, LO, and IF signals for testing.
- Power Meter : Measures power levels at different ports.
- Noise Figure Analyzer : Evaluates noise characteristics of the mixer.

The test setups for the different measurements are schematically shown in the figures below.

![Conversion loss measurement setup. DBM stands for Double Balanced Mixer, the terminations are $10dB=50Ohm$. Figure from \[3\]](/images/projects/gilbert_cell/Application_Note_AN009-Mini-Circuits-004.svg)
![Two-tone third order distortion (IIP3). Figure from \[3\]](/images/projects/gilbert_cell/Application_Note_AN009-Mini-Circuits-003.svg)
![VSWR measurement setup. Figure from \[3\].](/images/projects/gilbert_cell/Application_Note_AN009-Mini-Circuits-002.svg)
![Isolation measurement setup. Figure from \[3\].](/images/projects/gilbert_cell/Application_Note_AN009-Mini-Circuits-001.svg)

For our chip, we used the following pin-out:
![Pin-out of the Gilbert cell mixer on a GF180MCU padframe](/images/projects/gilbert_cell/Pinout.svg)

#### References
[1] Test & Measurement World, "RF Mixer Testing." [Online]. Available: https://www.test-and-measurement-world.com/measurements/rf/rf-mixer-testing

[2] Mini-Circuits, "Application Notes." [Online]. Available: https://www.minicircuits.com/applications/application_notes.html

[3] Mini-Circuits, "Application Note AN00-009." [Online]. Available: https://www.minicircuits.com/appdoc/AN00-009.html

## Further tools reference websites:
[1] H. Pretl, "Magic VLSI Keybind Cheatsheet," IIC-OSIC. [Online]. Available: https://raw.githubusercontent.com/hpretl/iic-osic/main/magic-cheatsheet/magic_cheatsheet.pdf

## Notes about tool specificities, caveats
The open-source design tools are constantly evolving, and thus there were some aha's and caveats I encountered during the design. I have listed these here to remind myself in the future.

1. For a MOSFET device in the PDK, 'nf' in MagicVLSI and 'nf' in Xschem are completely different. Example: a device with W=2um, nf=2 in Magic will have width=W\*nf=4um; the same device will have width=W=2um in xschem, with per-finger length of W/nf=1um. Steffan Schippers (the maintainer of Xschem), has even included devices which specify W as the per-finger width:
Open Source Silicon Community, "In Xschem, when using such a symbol, the nf one and then havin," Forum Discussion. [Online]. Available: https://web.open-source-silicon.dev/t/16920148/in-xschem-when-using-such-a-symbol-the-nf-one-and-then-havin.
After a short discussion on the FOSSi Element chat, Tim Edwards has changed the Magic-VLSI generators to conform to the BSIM4 convention, that W is the total width, nf is the number of fingers, and thus each finger has a length W/nf. 
I have also pushed a pull request to the gLayout github repository to conform to this convention too, since the generators in gLayout were not adhering to it.


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
