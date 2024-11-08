# Compressible_flow
Functions for working with compressible inviscid flow of gases.

## Description
This package provide a class for the most common function used in calculations of supersonic flow of an ideal gas, including adiabatic flow properties, normal shock wave properties, theta-beta-Mach relation, and Prandtl-Meyer function. 

## Installation
`pip install -i compressible-flow`

## Usage
Create an Ideal_Gas using the adiabatic ratio $\gamma$ and the effective gas constant $R_{specific}=R/M$ as parameters
```python
import compressible_flow as cf
air = cf.Ideal_Gas(R=287, gamma=1.4)
```
Calculate the total temperature to temperature ratio T_0/T as a function of the Mach number
```python
air.T0T(M=1.5)
```

## Repository
https://gitlab.com/itorre/compressible_flow

## License
This project is released under the MIT license.