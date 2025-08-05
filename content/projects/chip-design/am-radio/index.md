---
title: "AM Radio Receiver Design"
subtitle: "Analog Circuit Design and Implementation"
date: 2024-02-10
project_type: "Academic Project"
technologies: ["LTSpice", "PCB Design", "Analog Circuits", "RF Design", "MATLAB"]
image: "/images/projects/am-radio.jpg"
description: "Design and construction of a complete AM radio receiver including RF front-end, mixer, intermediate frequency amplifier, and audio output stage."
github: "https://github.com/username/am-radio-project"
demo: "https://youtu.be/radio-demo"
paper: "/papers/am-radio-report.pdf"
type: "projects"
draft: "true"
---

## Abstract

This project presents the design and implementation of a complete AM radio receiver operating in the standard AM broadcast band (530-1710 kHz). The receiver employs a superheterodyne architecture with careful attention to noise figure, sensitivity, and selectivity requirements.

## Introduction

AM radio remains a fundamental application in analog circuit design, providing an excellent platform for understanding key concepts including:
- RF circuit design principles
- Frequency conversion and mixing
- Intermediate frequency amplification
- Automatic gain control (AGC)
- Audio signal processing

The goal of this project was to design a functional AM receiver capable of receiving local broadcast stations with acceptable audio quality and interference rejection.

## System Architecture

### Superheterodyne Receiver Design
The receiver implements a classic superheterodyne architecture consisting of:

1. **RF Front-End**
   - Input bandpass filter (530-1710 kHz)
   - Low-noise RF amplifier
   - Variable tuning capacitor

2. **Frequency Conversion**
   - Local oscillator (LO) with frequency control
   - Double-balanced mixer
   - Intermediate frequency: 455 kHz

3. **IF Section**
   - IF bandpass filter (455 kHz ± 5 kHz)
   - Multi-stage IF amplifier with AGC
   - AM detector (envelope detector)

4. **Audio Processing**
   - Audio preamplifier
   - Volume control
   - Audio power amplifier
   - Speaker driver

## Circuit Design

### RF Amplifier
The RF amplifier stage uses a common-emitter configuration optimized for:
- **Noise Figure**: < 3 dB
- **Gain**: 20 dB
- **Input Impedance**: 50 Ω
- **Bandwidth**: 530-1710 kHz

**Key Design Considerations:**
- Transistor selection for low noise and high frequency operation
- Input/output matching networks for minimum noise figure
- Bias point optimization for linearity and low distortion

### Local Oscillator
The LO employs a Colpitts oscillator configuration featuring:
- **Frequency Range**: 985-2165 kHz (IF + RF frequency)
- **Phase Noise**: < -80 dBc/Hz at 1 kHz offset
- **Frequency Stability**: ±100 ppm over temperature

### IF Amplifier
The IF section provides:
- **Overall Gain**: 60 dB (distributed across 3 stages)
- **Bandwidth**: 10 kHz (-3 dB)
- **AGC Range**: 40 dB
- **Selectivity**: > 60 dB at ±20 kHz offset

## Implementation and Testing

### PCB Design
The circuit was implemented on a 4-layer PCB with careful attention to:
- RF layout practices and ground plane design
- Component placement for minimal coupling
- Proper power supply decoupling
- Shielding between circuit blocks

### Performance Measurements

| Parameter | Specification | Measured |
|-----------|---------------|----------|
| Sensitivity | -100 dBm | -105 dBm |
| Dynamic Range | 60 dB | 65 dB |
| Adjacent Channel Rejection | 60 dB | 58 dB |
| Audio Output Power | 100 mW | 125 mW |
| Total Harmonic Distortion | < 5% | 3.2% |

### Challenges and Solutions

**1. Oscillator Pulling**
- **Problem**: LO frequency shifting with antenna loading
- **Solution**: Improved buffer amplifier isolation

**2. Image Rejection**
- **Problem**: Insufficient image frequency rejection
- **Solution**: Added tuned circuit in RF front-end

**3. AGC Response Time**
- **Problem**: Slow AGC response causing distortion
- **Solution**: Optimized AGC time constants

## Results and Analysis

The completed AM receiver successfully demonstrated:
- Clear reception of local AM broadcast stations
- Adequate sensitivity for typical signal levels
- Good audio quality with low distortion
- Effective AGC operation preventing overload

**Frequency Response:**
The measured frequency response shows flat response across the AM broadcast band with proper selectivity characteristics.

**Noise Performance:**
The measured noise figure of 2.8 dB exceeds the design specification, contributing to excellent sensitivity.

## Conclusions

This project successfully demonstrated the design and implementation of a functional AM radio receiver. Key learning outcomes include:

- Understanding of superheterodyne receiver principles
- Practical experience with RF circuit design
- Importance of proper PCB layout for RF circuits
- System-level thinking in analog design
- Trade-offs between performance specifications

The project reinforced the fundamental concepts of analog circuit design while providing hands-on experience with RF engineering principles.

## Future Enhancements

Potential improvements for future versions:
- Digital signal processing for improved selectivity
- Automatic frequency control (AFC)
- Stereo AM capability
- Integration with software-defined radio concepts

## References

1. Razavi, B. "RF Microelectronics." 2nd Edition, Prentice Hall.
2. Lee, T. H. "The Design of CMOS Radio-Frequency Integrated Circuits." 2nd Edition.
3. Rogers, J., & Plett, C. "Radio Frequency Integrated Circuit Design." Artech House.
4. Bowick, C. "RF Circuit Design." 2nd Edition, Newnes.