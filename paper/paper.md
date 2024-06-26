---
title: 'DWBuilder: A code to generate ferroelectric/ferroelastic domain walls and multi-material atomic interface structures'
tags:
  - Python
  - domain walls
  - crystallography
  - multi-material inrerfaces
  - atomistic simulations (VASP, LAMMPS)
authors:
  - name: M.Z.Khalid
    orcid: 0000-0002-7866-3870
    affiliation: 1
  - name: S.M.Selbach
    affiliation: 1
affiliations:
 - name: Department of Materials Science and Engineering, Norwegian University of Science and Technology, Trondheim, Norway
   index: 1
date: 22 April 2024
bibliography: paper.bib
---

# Summary

In ferroelectric materials, the order parameter polarization can be switched by an external electric field. Regions within ferroelectric materials with uniform polarization are called domain, and the boundaries between  domains with differently aligned polarization vectors are called domain walls (DWs). These domain walls, which are only a few nanometers wide, possess unique properties with potential technological applications. DWs show promise for nanoscale electronic circuit elements and enable innovative design concepts because they can be created, erased and moved using applied electric fields [@meier2022ferroelectric; @catalan2012domain; @meier2015functional; @bednyakov2018physics]. DWs can also replicate the functionality of key electronic components such as diodes [@whyte2015diode], transistors [@mundy2017functional], and random access memories (RAM) [@sharma2017nonvolatile] .

Due to the nanoscale sizes and promising properties of DWs, there has been significant interest in studying how to control and manipulate them using atomistic simulations [@schultheiss2020intrinsic; @smaabraaten2020domain; @smaabraaten2018charged]. However, developing atomic DW structures is challenging and requires knowledge of the order parameter and DW types in ferroelectric materials. DWs can be ferroelectric, antiferroelectric, and/or ferroelastic, and they can vary depending on the allowed symmetry of the ferroelectric material. For instance, ferroelectric BiFeO$_3$ exists at room temperature as a rhombohedrally distorted perovskite with space group R3c and spontaneous polarization oriented along the [111]$_P$ axis[@ederer2005effect; @wang2003epitaxial]. The symmetry constraints of having the ferroelectric polarization in BiFeO$_3$ along <111> directions gives four types of DWs across which the polarization direction changes by 71°, 109°, or 180°[@wang2003epitaxial]. Similarly, other domain wall types have been identified in other ferroelectric materials such as BaTiO$_3$[@taherinejad2012bloch], PbTiO$_3$[@meyer2002ab] and YMnO$_3$[@smaabraaten2018charged], and in ferroelastics like CaTiO$_3$[@barone2014improper].

The ``DWBuilder`` code is designed as a command-line tool to create DWs and interface structures from specific input unit cell geometries, as described in detail in the README file of the repository. The code comprises two main components: (i) a domain wall builder for similar materials and (ii) a heterogeneous interface builder for multi-material atomic interfaces. Figure 1 explains the structure and workflow of the ``DWBuilder`` package. 

The first part, handled by the scripts ``dwbuilder.py`` and ``dbuilder.py``,  produces domain walls by first analyzing the input unit cell geometry and determining the space group of the structure. The space group is identified using the open-source Python library Pymatgen. If the space group matches the specified type, the script offers a range of possible domain wall types and ultimately creates the DW structures. If the space group of the input structure does not match, the script allows you to choose a desired space group type or manually define the domains by specifying lattice vectors. To generate different domains separately, you can use ``dbuilder.py`` to develop distinct domains, which can be useful for bulk and surface calculations.
  
 The second part of the code involves creating a heterogeneous interface structure of multi-material compounds, which is handled by the script ``hibuilder.py``. This script requires two input structures, named ``bulk1`` and ``bulk2``. To develop compatible interfaces, you must define the orientation relationship (OR) between the two bulk phases. This definition is necessary to address any lattice and angular mismatches that arise from differences in space groups and/or atomic structures of the two phases. 

Currently, the script cannot predict the ORs that would result in a low lattice mismatch between the two bulk phases. However, theoretical studies and methods such as edge-to-edge [@zhang2005edge] and face-to-face [@khalid2020atomistic] matching techniques can help predict low lattice misfit for interface construction. This script assumes that the user is already familiar with the appropriate ORs to construct the interface structure. For instance, the ORs of interfaces reported in referenced papers  [@khalid2020ab; @khalid2021imc; @khalid2021first; @mzkhalid2019first] can be replicated using this script. Additionally, the script can generate atomic interfaces if you know the OR from experiments, and it can predict the atomic interface structure and lattice mismatch between the two bulk phases.

 ![Structure of the `DWBuilder` package.\label{fig:scheme}](dwbuilder.png){width="100%"}

# Statement of need:
``DWBuilder`` is an interactive toolbox for developing atomic-scale domain walls and interface structures of homogeneous and heterogeneous material compounds, making it suitable for high-throughput calculations. Its target audience includes students and scientists in materials science and physics at any level of expertise. ``DWBuilder`` utilizes the NumPy library extensively, which speeds up execution, particularly when working with large structures. Users are guided through the process of identifying and creating the desired domain walls in a step-by-step manner. The code is designed to be user-friendly and educational, with a focus on plane orientation and electric polarization switching.

The ``DWBuilder`` code is designed to automate the creation of atomic interfaces and domain wall structures, allowing researchers to focus on optimizing and studying material behavior and properties. The structures generated by this code are compatible with both first-principles and second-principles calculations. The code provides ample functionality to support practical research tasks while remaining lightweight and well-documented. This allows junior researchers with minimal or no assistance to easily install, use, and understand the code.


# Acknowledgements

Funding from the Norwegian research counsil  (Grant agreement No. 90544501) is gratefully acknowledged.

# References



