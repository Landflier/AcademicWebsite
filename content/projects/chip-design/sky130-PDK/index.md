---
title: "Sky130nm Op-Amp Design"
date: 2023-07-13
draft: true
---

# Two-Stage Operational Amplifier in Sky130nm PDK

## Project Overview

This project involves the design and implementation of a two-stage operational amplifier using the open-source Sky130nm Process Design Kit (PDK). The Sky130 PDK is a collaboration between Google and SkyWater Technology Foundry, providing an open-source 130nm manufacturing process.

## Design Specifications

- **Process Technology**: Sky130nm CMOS
- **Supply Voltage**: 1.8V
- **DC Gain**: > 60dB
- **Unity Gain Bandwidth**: > 10MHz
- **Phase Margin**: > 60 degrees
- **CMRR**: > 60dB
- **PSRR**: > 50dB
- **Output Swing**: Rail-to-rail
- **Power Consumption**: < 500µW

## Circuit Architecture

The operational amplifier employs a classic two-stage architecture:
1. **First Stage**: Differential input pair with active load
2. **Second Stage**: Common source amplifier for additional gain
3. **Miller Compensation**: For stability across a wide range of loads

![Op-Amp Schematic](/images/sky130-opamp-schematic.png)

## Simulation Results

The design has been verified through several simulation corners:
- Process variations (TT, SS, FF, SF, FS)
- Temperature ranges (-40°C to 125°C)
- Supply voltage variations (±10%)

### AC Response
- DC Gain: 68dB
- Unity Gain Bandwidth: 15MHz
- Phase Margin: 65 degrees

### Transient Response
- Settling Time (0.1%): 200ns
- Slew Rate: 10V/µs

## Layout Considerations

The layout employs common-centroid techniques for the input differential pair and careful matching for current mirrors to minimize offset. Guard rings are used to isolate sensitive analog components from substrate noise.

## Future Work

- Integration with a bandgap reference circuit
- Adding power-down functionality
- Exploring rail-to-rail input capabilities

## Tools Used

- **Schematic Capture**: Xschem
- **Simulation**: ngspice
- **Layout**: Magic
- **Verification**: Netgen 