#!/usr/bin/env python
"""
 Overview
 --------
 This script processes a given input file representing a crystal structure 
 and manipulates it to produce various domain wall structures based on 
 different space group symmetries. 

 The script uses `ase` and `pymatgen` libraries to manipulate atomic structures,
 determine symmetry properties, and generate domain wall configurations. It allows
 the user to choose from a range of predefined space groups and domain wall angles.
 
 The main features include:
 - Automatic space group identification and lattice type determination using `pymatgen`.
 - User input for selecting predefined systems and domain wall angles.
 - Creation of various domain wall structures (109°, 71°, 180°) and supercells.
 - Calculations of lattice strain between different domains.
 - Warnings about potential domain wall artifacts that may arise during the 
   process, advising manual adjustment.
 
 Usage:
 - Ensure required libraries (`ase`, `pymatgen`, `numpy`, and `colorama`) are 
   installed.
 - Run the script and follow prompts for user input.
 - The script generates domain wall structures and supercells in the respective 
   directories for the specified system and angle selections.

 Dependencies:
 - ase
 - pymatgen
 - numpy
 - colorama

 For detailed usage instructions, refer to the prompts in the script.
"""

import os
import sys
import ase
import ase.io
from ase.build import cut, rotate, stack
import numpy as np
from colorama import init, Fore, Style
from numpy.linalg import norm
from colorama import Fore, Style
from pymatgen.core.structure import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

# Find the path of the current directory
current_path = os.getcwd()

filename = input("Enter the input file name (with extension): ")
D1 = ase.io.read(filename)

struct = Structure.from_file(filename)
sym = SpacegroupAnalyzer(struct)
data = sym.get_symmetry_dataset()

print("Space group number: {}".format(data["number"]))
print("International symbol: {}".format(data["international"]))
print(f"Lattice type: {sym.get_lattice_type()}")

# Conditionally select the system based on international symbol
if data["international"] == "R3c":
    system_selection = 1
elif data["international"] == "R3m":
    system_selection = 2
elif data["international"] == "P4mm":
    system_selection = 3
elif data["international"] == "P6_3cm":
    system_selection = 4
elif data["international"] == "Pnma":
    system_selection = 5
elif data["international"] == "Pmc2_1":
    system_selection = 6

else:
    print("Warning: The international symbol does not match any pre-defined systems.")
    print("Please manually select the system.")
    system_selection = 7

# Prompt the user to select the system if not automatically selected
if system_selection == 7:
    print("Select the system:")
    print("1 - R3c")
    print("2 - R3m")
    print("3 - P4mm")
    print("4 - P6_3cm")
    print("5 - Pnma")
    print("6 - Pmc2_1")

    print("7 - Manual Orientation relationships")


    system_selection = int(input())

# BFO system 
# Reference: Wang Y, Nelson C, Melville A, Winchester B, Shang S, Liu ZK, Schlom DG, Pan X, Chen LQ. BiFeO 3 domain wall energies and structures: a combined experimental and density functional theory+ U study. Physical review letters. 2013 Jun 24;110(26):267601.

if system_selection == 1:

    # Cut and rotate the structure to obtain a pseudo-cubic structure
    pseudo_cubic = cut(D1, a=[1.0, 1.0, -1], b=[-1, 1, 1], c=[1, -1, 1])
    rotate(pseudo_cubic, pseudo_cubic.cell[0], (0,1,0), pseudo_cubic.cell[1], (1,0,0))

    # Write the pseudo-cubic structure to a VASP file
    pseudo_cubic.write('Pseudo_cubic_BFO.vasp', sort=True, vasp5=True)

    # Read the pseudo-cubic structure
    BFO = ase.io.read('Pseudo_cubic_BFO.vasp')

    # Prompt the user to select the domain wall angle
    print("Select the domain wall angle:")
    print("1 - 109 degrees")
    print("2 - 71 degrees")
    print("3 - 180 degrees")
    print("4 - All angles")
    angle_selection = int(input())

    # Prompt the user to enter the domain wall size
    domain_size = int(input("Enter the domain wall size (in number of unit cells): "))

    # Cut and rotate the slabs based on the selected domain wall angle(s)
    if angle_selection == 1 or angle_selection == 4:
        slab1 = cut(BFO, a=[0.0, 1, 0], b=[1, 0, 0], c=[0, 0, domain_size])
        rotate(slab1, slab1.cell[0], (0,1,0), slab1.cell[1], (1,0,0))
        slab2 = cut(BFO, a=[0.0, -1, 0], b=[-1, 0, 0], c=[0, 0, domain_size])
        rotate(slab2, slab2.cell[0], (0,1,0), slab2.cell[1], (1,0,0))
        slab109 = stack(slab1, slab2, axis=2, maxstrain=None)
        os.makedirs('BFO_109')
        slab109.write('BFO_109/109_DW.vasp', sort=True, vasp5=True)
        slab1.write('BFO_109/109_domain1.vasp', sort=True, vasp5=True)
        slab2.write('BFO_109/109_domain2.vasp', sort=True, vasp5=True)
        print("Domain 1 Orientation (109 DW): a = [0, 1, 0), b = [1, 0, 0], c = (0, 0, 1)")
        print("Domain 2 Orientation (109 DW): a = [0, -1, 0), b = [-1, 0, 0], c = (0, 0, 1)")
        print("\033[1;31;40mWarning: This code might create domain wall artifacts, like missing or duplicate atoms, at the domain wall. Therefore, manual adjustment may be needed.\033[0m")
        
        #Calculatue lattice strain
        a1, b1, c1 = slab1.cell
        a2, b2, c2 = slab2.cell

        print ('strain along a (%):', (norm(a1) - norm(a2)) / norm(a2) * 100.)
        print ('strain along b (%):', (norm(b1) - norm(b2)) / norm(b2) * 100.)
        print ('strain along c (%):', (norm(c1) - norm(c2)) / norm(c2) * 100.)

    if angle_selection == 2 or angle_selection == 4:
        slab1 = cut(BFO, a=[1, -1, 0], b=[0, 0, 1], c=[domain_size, domain_size, 0])
        rotate(slab1, slab1.cell[0], (0,1,0), slab1.cell[1], (1,0,0))
        slab2 = cut(BFO, a=[-1, 1, 0], b=[0, 0, -1], c=[domain_size, domain_size, 0])
        rotate(slab2, slab2.cell[0], (0,1,0), slab2.cell[1], (1,0,0))
        slab71 = stack(slab1, slab2, axis=2, maxstrain=None)
        os.makedirs(os.path.join(current_path, 'BFO_71'))
        slab71.write(os.path.join(current_path, 'BFO_71', '71_DW.vasp'), sort=True, vasp5=True)
        slab1.write(os.path.join(current_path, 'BFO_71', '71_domain1.vasp'), sort=True, vasp5=True)
        slab2.write(os.path.join(current_path, 'BFO_71', '71_domain2.vasp'), sort=True, vasp5=True)
        print("Domain 1 Orientation (71 DW): a = [1, -1, 0), b = [0, 0, 1], c = (1, 1, 0)")
        print("Domain 2 Orientation (71 DW): a = [-1, 1, 0), b = [0, 0, -1], c = (1, 1, 0)")
        print("\033[1;31;40mWarning: This code might create domain wall artifacts, like missing or duplicate atoms, at the domain wall. Therefore, manual adjustment may be needed.\033[0m")
       
        #Calculatue lattice strain
        a1, b1, c1 = slab1.cell
        a2, b2, c2 = slab2.cell

        print ('strain along a (%):', (norm(a1) - norm(a2)) / norm(a2) * 100.)
        print ('strain along b (%):', (norm(b1) - norm(b2)) / norm(b2) * 100.)
        print ('strain along c (%):', (norm(c1) - norm(c2)) / norm(c2) * 100.)


    if angle_selection == 3 or angle_selection == 4:
        slab1 = cut(BFO, a=[1, 1, 0], b=[0, 0, -1], c=[-domain_size, domain_size, 0])
        rotate(slab1, slab1.cell[0], (0,1,0), slab1.cell[1], (1,0,0))
        slab2 = cut(BFO, a=[-1, -1, 0], b=[0, 0, 1], c=[-domain_size, domain_size, 0])
        rotate(slab2, slab2.cell[0], (0,1,0), slab2.cell[1], (1,0,0))
        slab180 = stack(slab1, slab2, axis=2, maxstrain=None)
        os.makedirs(os.path.join(current_path, 'BFO_180'))    
        slab180.write(os.path.join(current_path,'BFO_180', '180_DW.vasp'), sort=True, vasp5=True)
        slab1.write(os.path.join(current_path,'BFO_180', '180_domain1.vasp'), sort=True, vasp5=True)
        slab2.write(os.path.join(current_path,'BFO_180', '180_domain2.vasp'), sort=True, vasp5=True)
        print("Domain 1 Orientation (180 DW): a = [1, 1, 0), b = [0, 0, -1], c = (-1, 1, 0)")
        print("Domain2 Orientation (180 DW): a = [-1, -1, 0), b = [0, 0, -1], c = (-1, 1, 0)")
        print("\033[1;31;40mWarning: This code might create domain wall artifacts, like missing or duplicate atoms, at the domain wall. Therefore, manual adjustment may be needed.\033[0m")

         #Calculatue lattice strain
        a1, b1, c1 = slab1.cell
        a2, b2, c2 = slab2.cell

        print ('strain along a (%):', (norm(a1) - norm(a2)) / norm(a2) * 100.)
        print ('strain along b (%):', (norm(b1) - norm(b2)) / norm(b2) * 100.)
        print ('strain along c (%):', (norm(c1) - norm(c2)) / norm(c2) * 100.)

        
        # Create supercells of the domain walls

    supercell_size = int(input("Enter size of supercell (in number of unit cells): "))
    if angle_selection == 1 or angle_selection == 4:
        slab109_supercell = slab109.repeat([supercell_size, supercell_size, 1])
        slab109_supercell.write(os.path.join(current_path,'BFO_109', '109_supercell.vasp'), sort=True, vasp5=True)

    if angle_selection == 2 or angle_selection == 4:
        slab71_supercell = slab71.repeat([supercell_size, supercell_size, 1])
        slab71_supercell.write(os.path.join(current_path, 'BFO_71', '71_supercell.vasp'), sort=True, vasp5=True)

    if angle_selection == 3 or angle_selection == 4:
        slab180_supercell = slab180.repeat([supercell_size, supercell_size, 1])
        slab180_supercell.write(os.path.join(current_path, 'BFO_180', '180_supercell.vasp'), sort=True, vasp5=True)


    #Print confirmation message to user

print("Domain wall structures and supercells created successfully!")

 # BaTiO3 system
# Ref: Taherinejad M, Vanderbilt D, Marton P, Stepkova V, Hlinka J. Bloch-type domain walls in rhombohedral BaTiO 3. Physical Review B. 2012 Oct 22;86(15):155138.

if system_selection == 2:
    # Prompt the user to enter the input file name

    # Prompt the user to select the domain wall angle
    print("Select the domain wall angle:")
    print("1 - R180 degrees")
    print("2 - R71 degrees")
    print("3 - R109 degrees")
    print("4 - All angles")
    angle_selection = int(input())

    # Prompt the user to enter the lattice vector sizes
    print("Note: R109 and  R71 domain walls lie along the a-direction and R180 along c-direction")

    # Prompt the user to enter the lattice vector sizes
    domain_size = int(input("Enter the domain wall size (in number of unit cells): "))

    # Cut and rotate the slabs based on the selected domain wall angle(s)
    if angle_selection == 1 or angle_selection == 4:
        slab1 = cut(D1, a=[1, 1, 0], b=[0, 0, 1], c=[domain_size, -domain_size, 0])
        rotate(slab1, slab1.cell[0], (0,1,0), slab1.cell[1], (1,0,0))
        slab2 = cut(D1, a=[-1, -1, 0], b=[0, 0, -1], c=[domain_size, -domain_size, 0])
        rotate(slab2, slab2.cell[0], (0,1,0), slab2.cell[1], (1,0,0))
        slab180 = stack(slab1, slab2, axis=2, maxstrain=None)
        os.makedirs(os.path.join(current_path, 'R180'))
        slab180.write(os.path.join(current_path, 'R180', 'R180_DW.vasp'), sort=True, vasp5=True)
        slab1.write(os.path.join(current_path, 'R180', 'R180_domain1.vasp'), sort=True, vasp5=True)
        slab2.write(os.path.join(current_path, 'R180', 'R180_domain2.vasp'), sort=True, vasp5=True)
        print("Domain 1 Orientation (R180 DW): a = [1, 1, 0), b = [0, 0, 1], c = (1, -1, 0)")
        print("Domain 2 Orientation (R180 DW): a = [-1, -1, 0), b = [0, 0, -1], c = (1, -1, 0)")
        print("\033[1;31;40mWarning: This code might create domain wall artifacts, like missing or duplicate atoms, at the domain wall. Therefore, manual adjustment may be needed.\033[0m")

        #Calculatue lattice strain
        a1, b1, c1 = slab1.cell
        a2, b2, c2 = slab2.cell

        print ('strain along a (%):', (norm(a1) - norm(a2)) / norm(a2) * 100.)
        print ('strain along b (%):', (norm(b1) - norm(b2)) / norm(b2) * 100.)
        print ('strain along c (%):', (norm(c1) - norm(c2)) / norm(c2) * 100.)

    if angle_selection == 2 or angle_selection == 4:
        slab1 = cut(D1, a=[domain_size, domain_size, 0], b=[0, 0, 1], c=[1, -1, 0])
        rotate(slab1, slab1.cell[0], (0,1,0), slab1.cell[1], (1,0,0))
        slab2 = cut(D1, a=[domain_size, domain_size, 0], b=[0, 0, -1], c=[-1, 1, 0])
        rotate(slab2, slab2.cell[0], (0,1,0), slab2.cell[1], (1,0,0))
        slab71 = stack(slab1, slab2, axis=0, maxstrain=None)
        os.makedirs(os.path.join(current_path, 'R71'))
        slab71.write(os.path.join(current_path, 'R71', 'R71_DW.vasp'), sort=True, vasp5=True)
        slab1.write(os.path.join(current_path, 'R71', 'R71_domain1.vasp'), sort=True, vasp5=True)
        slab2.write(os.path.join(current_path, 'R71', 'R71_domain2.vasp'), sort=True, vasp5=True)
        print("Domain 1 Orientation (R71 DW): a = (1, 1, 0), b = [0, 0, 1], c = [1, -1, 0]")
        print("Domain 2 Orientation (R71 DW): a = (1, 1, 0), b = [0, 0, -1], c = [-1, 1, 0]")
        print("\033[1;31;40mWarning: This code might create domain wall artifacts, like missing or duplicate atoms, at the domain wall. Therefore, manual adjustment may be needed.\033[0m")

        #Calculatue lattice strain
        a1, b1, c1 = slab1.cell
        a2, b2, c2 = slab2.cell

        print ('strain along a (%):', (norm(a1) - norm(a2)) / norm(a2) * 100.)
        print ('strain along b (%):', (norm(b1) - norm(b2)) / norm(b2) * 100.)
        print ('strain along c (%):', (norm(c1) - norm(c2)) / norm(c2) * 100.)


    if angle_selection == 3 or angle_selection == 4:
        slab1 = cut(D1, a=[domain_size, 0.0, 0], b=[0, 1, 0], c=[0, 0, 1])
        rotate(slab1, slab1.cell[0], (0,1,0), slab1.cell[1], (1,0,0))
        slab2 = cut(D1, a=[domain_size, 0.0, 0], b=[0, -1, 0], c=[0, 0, -1])
        rotate(slab2, slab2.cell[0], (0,1,0), slab2.cell[1], (1,0,0))
        slab109 = stack(slab1, slab2, axis=0, maxstrain=None)
        os.makedirs(os.path.join(current_path, 'R109'))
        slab109.write(os.path.join(current_path, 'R109', 'R109_DW.vasp'), sort=True, vasp5=True)
        slab1.write(os.path.join(current_path, 'R109', 'R109_domain1.vasp'), sort=True, vasp5=True)
        slab2.write(os.path.join(current_path, 'R109', 'R109_domain2.vasp'), sort=True, vasp5=True)
        print("Domain 1 Orientation (R109 DW): a = (1, 0, 0), b = [0, 1, 0], c = [0, 0, 1]")
        print("Domain 2 Orientation (R109 DW): a = (1, 0, 0), b = [0, -1, 0], c = [0, 0, -1]")
        print("\033[1;31;40mWarning: This code might create domain wall artifacts, like missing or duplicate atoms, at the domain wall. Therefore, manual adjustment may be needed.\033[0m")

        #Calculatue lattice strain
        a1, b1, c1 = slab1.cell
        a2, b2, c2 = slab2.cell

        print ('strain along a (%):', (norm(a1) - norm(a2)) / norm(a2) * 100.)
        print ('strain along b (%):', (norm(b1) - norm(b2)) / norm(b2) * 100.)
        print ('strain along c (%):', (norm(c1) - norm(c2)) / norm(c2) * 100.)


    # Create supercells of the domain walls

    supercell_size = int(input("Enter size of supercell (in number of unit cells): "))
    if angle_selection == 1 or angle_selection == 4:
        slab180_supercell = slab180.repeat([supercell_size, supercell_size, 1])
        slab180_supercell.write(os.path.join(current_path, 'R180', 'R180_supercell.vasp'), sort=True, vasp5=True)

    if angle_selection == 2 or angle_selection == 4:
        slab71_supercell = slab71.repeat([1, supercell_size, supercell_size])
        slab71_supercell.write(os.path.join(current_path, 'R71', 'R71_supercell.vasp'), sort=True, vasp5=True)

    if angle_selection == 3 or angle_selection == 4:
        slab109_supercell = slab109.repeat([1, supercell_size, supercell_size])
        slab109_supercell.write(os.path.join(current_path, 'R109', 'R109_supercell.vasp'), sort=True, vasp5=True)

    #Print confirmation message to user

    print("Domain wall structures and supercells created successfully!")



 # PTO system 
# Ref: 
if system_selection == 3:
    # Prompt the user to enter the input file name
    
    # Prompt the user to select the domain wall angle
    print("Select the domain wall angle:")
    print("1 - T180 degrees")
    print("2 - T90 degrees")
    print("3 - All angles")
    angle_selection = int(input())
    # Prompt the user to enter the lattice vector sizes
    domain_size = int(input("Enter the domain wall size (in number of unit cells): "))

    # Cut and rotate the slabs based on the selected domain wall angle(s)
    if angle_selection == 1 or angle_selection == 3:
        slab1 = cut(D1, a=[1.01, 0, 0], b=[0, domain_size, 0], c=[0, 0, 1.01])
        rotate(slab1, slab1.cell[0], (0,1,0), slab1.cell[1], (1,0,0))
        slab2 = cut(D1, a=[-1.01, 0, 0], b=[0, domain_size, 0], c=[0, 0, -1.01])
        rotate(slab2, slab2.cell[0], (0,1,0), slab2.cell[1], (1,0,0))
        slab180 = stack(slab1, slab2, axis=1, maxstrain=None)
        os.makedirs(os.path.join(current_path, 'T180'))
        slab180.write(os.path.join(current_path, 'T180', 'T180_DW.vasp'), sort=True, vasp5=True)
        slab1.write(os.path.join(current_path, 'T180', 'T180_domain1.vasp'), sort=True, vasp5=True)
        slab2.write(os.path.join(current_path, 'T180', 'T180_domain2.vasp'), sort=True, vasp5=True)
        print("Domain 1 Orientation (T180 DW): a = [1, 0, 0], b = (0, 1, 0), c = [0, 0, 1]")
        print("Domain 2 Orientation (T180 DW): a = [-1, 0, 0], b = (0, 1, 0), c = [0, 0, -1]")
        print("\033[1;31;40mWarning: This code might create domain wall artifacts, like missing or duplicate atoms, at the domain wall. Therefore, manual adjustment may be needed.\033[0m")

         #Calculatue lattice strain
        a1, b1, c1 = slab1.cell
        a2, b2, c2 = slab2.cell

        print ('strain along a (%):', (norm(a1) - norm(a2)) / norm(a2) * 100.)
        print ('strain along b (%):', (norm(b1) - norm(b2)) / norm(b2) * 100.)
        print ('strain along c (%):', (norm(c1) - norm(c2)) / norm(c2) * 100.)
   
    if angle_selection == 2 or angle_selection == 3:
        slab1 = cut(D1, a=[0, 1, 0], b=[-1, 0, 1], c=[domain_size, 0, domain_size])
        rotate(slab1, slab1.cell[0], (0,1,0), slab1.cell[1], (1,0,0))
        slab2 = cut(D1, a=[0, -1, 0], b=[1, 0, -1], c=[domain_size, 0, domain_size])
        rotate(slab2, slab2.cell[0], (0,1,0), slab2.cell[1], (1,0,0))
        slab90 = stack(slab1, slab2, axis=2, maxstrain=None)
        os.makedirs(os.path.join(current_path, 'T90'))
        slab90.write(os.path.join(current_path, 'T90', 'T90_DW.vasp'), sort=True, vasp5=True)
        slab1.write(os.path.join(current_path, 'T90', 'T90_domain1.vasp'), sort=True, vasp5=True)
        slab2.write(os.path.join(current_path, 'T90', 'T90_domain2.vasp'), sort=True, vasp5=True)
        print("Domain 1 Orientation (T90 DW): a = [0, 1, 0], b = [-1, 0, 1], c = (1, 0, 1)")
        print("Domain 2 Orientation (T90 DW): a = [0, -1, 0], b = [1, 0, -1], c = (1, 0, 1)")
        print("\033[1;31;40mWarning: This code might create domain wall artifacts, like missing or duplicate atoms, at the domain wall. Therefore, manual adjustment may be needed.\033[0m")

        #Calculatue lattice strain
        a1, b1, c1 = slab1.cell
        a2, b2, c2 = slab2.cell

        print ('strain along a (%):', (norm(a1) - norm(a2)) / norm(a2) * 100.)
        print ('strain along b (%):', (norm(b1) - norm(b2)) / norm(b2) * 100.)
        print ('strain along c (%):', (norm(c1) - norm(c2)) / norm(c2) * 100.)

    # Create supercells of the domain walls

    supercell_size = int(input("Enter size of supercell (in number of unit cells): "))
    if angle_selection == 1 or angle_selection == 3:
        slab180_supercell = slab180.repeat([supercell_size, 1, supercell_size])
        slab180_supercell.write(os.path.join(current_path, 'T180', 'T180_supercell.vasp'), sort=True, vasp5=True)

    if angle_selection == 2 or angle_selection == 3:
        slab90_supercell = slab90.repeat([supercell_size, supercell_size, 1])
        slab90_supercell.write(os.path.join(current_path, 'T90', 'T90_supercell.vasp'), sort=True, vasp5=True)

    #Print confirmation message to user

    print("Domain wall structures and supercells created successfully!")



    
    
# YMO system
if system_selection == 4:
    # Prompt the user to enter the input file name
    filename2 = input("Enter the input domain2 file name (with extension): ")

    # Read the input file
    YMO1 = ase.io.read(filename1)
    YMO2 = ase.io.read(filename2)


    # Prompt the user to select the domain wall angle
    print("Select the domain wall angle:")
    print("1 - Neutral domain wall")
    print("2 - Charged domain wall")
    print("3 - both")
    angle_selection = int(input())

    # Find the path of the current directory
    current_path = os.getcwd()



    domain_size = float(input("Enter the domain wall size (in number of unit cells): "))

    # Cut and rotate the slabs based on the selected domain wall angle(s)
    if angle_selection == 1 or angle_selection == 3:
        slab1 = cut(YMO1, a=[-domain_size, domain_size, 0], b=[0.0, 0.0, 1.01], c=[-1.0, -1.0, 0])
        rotate(slab1, slab1.cell[0], (0,1,0), slab1.cell[1], (1,0,0))
        slab2 = cut(YMO2, a=[-domain_size, domain_size, 0], b=[0.0, 0.0, 1.01], c=[-1.0, -1.0, 0])
        rotate(slab2, slab2.cell[0], (0,1,0), slab2.cell[1], (1,0,0))
        slab_NDW = stack(slab1, slab2, axis=0, maxstrain=None)
        os.makedirs(os.path.join(current_path, 'NDW'))
        slab_NDW.write(os.path.join(current_path, 'NDW', 'NDW.vasp'), sort=True, vasp5=True)
        slab1.write(os.path.join(current_path, 'NDW', 'domain1.vasp'), sort=True, vasp5=True)
        slab2.write(os.path.join(current_path, 'NDW', 'domain2.vasp'), sort=True, vasp5=True)
        print("\033[1;31;40mWarning: This code might create domain wall artifacts, like missing or duplicate atoms, at the domain wall. Therefore, manual adjustment may be needed.\033[0m")
        print("NDW Orientation: a = (-1, 1, 0), b = [0, 0, 1], c = [-1, -1, 0]")
       
        #Calculatue lattice strain
        a1, b1, c1 = slab1.cell
        a2, b2, c2 = slab2.cell

        print ('strain along a (%):', (norm(a1) - norm(a2)) / norm(a2) * 100.)
        print ('strain along b (%):', (norm(b1) - norm(b2)) / norm(b2) * 100.)
        print ('strain along c (%):', (norm(c1) - norm(c2)) / norm(c2) * 100.)

    if angle_selection == 2 or angle_selection == 3:
        slab1 = cut(YMO1, a=[-1, 1, 0], b=[0.0, 0.0, domain_size+0.01], c=[-1.0, -1.0, 0])
        rotate(slab1, slab1.cell[0], (0,1,0), slab1.cell[1], (1,0,0))
        slab2 = cut(YMO2, a=[-1, 1, 0], b=[0.0, 0.0, domain_size+0.01], c=[-1.0, -1.0, 0])
        rotate(slab2, slab2.cell[0], (0,1,0), slab2.cell[1], (1,0,0))
        slab_CDW = stack(slab1, slab2, axis=1, maxstrain=None)
        os.makedirs(os.path.join(current_path, 'CDW'))
        slab_CDW.write(os.path.join(current_path, 'CDW', 'CDW.vasp'), sort=True, vasp5=True)
        slab1.write(os.path.join(current_path, 'CDW', 'CDW_domain1.vasp'), sort=True, vasp5=True)
        slab2.write(os.path.join(current_path, 'CDW', 'CDW_domain2.vasp'), sort=True, vasp5=True)
        print("CDW Orientation: a = [-1, 1, 0], b = (0, 0, 1), c = [-1, -1, 0]")

        print("\033[1;31;40mWarning: This code might create domain wall artifacts, like missing or duplicate atoms, at the domain wall. Therefore, manual adjustment may be needed.\033[0m")
   
        #Calculatue lattice strain
        a1, b1, c1 = slab1.cell
        a2, b2, c2 = slab2.cell

        print ('strain along a (%):', (norm(a1) - norm(a2)) / norm(a2) * 100.)
        print ('strain along b (%):', (norm(b1) - norm(b2)) / norm(b2) * 100.)
        print ('strain along c (%):', (norm(c1) - norm(c2)) / norm(c2) * 100.)

    # Create supercells of the domain walls

    supercell_size = int(input("Enter size of supercell (in number of unit cells): "))
    if angle_selection == 1 or angle_selection == 3:
        slab_NDW_supercell = slab_NDW.repeat([1, supercell_size, supercell_size])
        slab_NDW_supercell.write(os.path.join(current_path, 'NDW', 'NDW_supercell.vasp'), sort=True, vasp5=True)

    if angle_selection == 2 or angle_selection == 3:
        slab_CDW_supercell = slab_CDW.repeat([supercell_size, 1, supercell_size])
        slab_CDW_supercell.write(os.path.join(current_path, 'CDW', 'CDW_supercell.vasp'), sort=True, vasp5=True)

    #Print confirmation message to user

    print("Domain wall structures and supercells created successfully!")


 # CTO system
# Ref: Barone P, Di Sante D, Picozzi S. Improper origin of polar displacements at CaTiO 3 and CaMnO 3 twin walls. Physical Review B. 2014 Apr 8;89(14):144104.
if system_selection == 5:
    # Prompt the user to enter the input file name


    # Prompt the user to enter the lattice vector sizes
    print("Pnma space group has ferroelastic domain walls")

    # Prompt the user to enter the lattice vector sizes
    domain_size = int(input("Enter the domain wall size (in number of unit cells): "))

    # Cut and rotate the slabs based on the selected domain wall angle(s)
    slab1 = cut(D1, a=[1, 1, 0], b=[0.0, 0.0, 1], c=[domain_size, -domain_size, 0])
    rotate(slab1, slab1.cell[0], (0,1,0), slab1.cell[1], (1,0,0))
    slab2 = cut(D1, a=[-1, 1, 0], b=[0.0, 0.0, 1], c=[domain_size, domain_size, 0])
    rotate(slab2, slab2.cell[0], (0,1,0), slab2.cell[1], (1,0,0))
    slab180 = stack(slab1, slab2, axis=2, maxstrain=None)
    os.makedirs(os.path.join(current_path, 'Pnma'))
    slab180.write(os.path.join(current_path, 'Pnma', 'FE_DW.vasp'), sort=True, vasp5=True)
    slab1.write(os.path.join(current_path, 'Pnma', 'D1.vasp'), sort=True, vasp5=True)
    slab2.write(os.path.join(current_path, 'Pnma', 'D2.vasp'), sort=True, vasp5=True)
    print("Domain 1 Orientation (R180 DW): a = [1, 1, 0), b = [0, 0, 1], c = (1, -1, 0)")
    print("Domain 2 Orientation (R180 DW): a = [-1, 1, 0), b = [0, 0, 1], c = (1, 1, 0)")
    print("\033[1;31;40mWarning: This code might create domain wall artifacts, like missing or duplicate atoms, at the domain wall. Therefore, manual adjustment may be needed.\033[0m")

    #Calculatue lattice strain
    a1, b1, c1 = slab1.cell
    a2, b2, c2 = slab2.cell

    print ('strain along a (%):', (norm(a1) - norm(a2)) / norm(a2) * 100.)
    print ('strain along b (%):', (norm(b1) - norm(b2)) / norm(b2) * 100.)
    print ('strain along c (%):', (norm(c1) - norm(c2)) / norm(c2) * 100.)
    
    # Create supercells of the domain walls

    supercell_size = int(input("Enter size of supercell (in number of unit cells): "))
    if angle_selection == 5:
        slab180_supercell = slab180.repeat([supercell_size, supercell_size, 1])
        slab180_supercell.write(os.path.join(current_path, 'Pnma', 'T180_supercell.vasp'), sort=True, vasp5=True)

    #Print confirmation message to user

    print("Domain wall structures and supercells created successfully!")

     # Orthorhombic system

if system_selection == 6:
    # Prompt the user to select the domain wall angle
    print("Select the domain wall angle:")
    print("1 - O120 degrees")
    print("2 - O180 degrees")
    print("3 - O90 degrees")
    print("4 - All angles")
    angle_selection = int(input())

    # Find the path of the current directory
    current_path = os.getcwd()
    # Read the input file

    axis = input("Please select a polar axis (a, b, or c): ")

    if axis == 'a':
        slab1 = cut(D1, a=[1, 0, 0], b=[0.0, 1.0, 0], c=[0, 0, 1])
        rotate(slab1, slab1.cell[0], (0,1,0), slab1.cell[1], (1,0,0))

    elif axis == 'b':
        slab1 = cut(D1, a=[0, 1, 0], b=[0.0, 0.0, 1], c=[1, 0, 0])
        rotate(slab1, slab1.cell[0], (0,1,0), slab1.cell[1], (1,0,0))

    elif axis == 'c':
        slab1 = cut(D1, a=[0, 0, 1], b=[1.0, 0.0, 0], c=[0, 1, 0])
        rotate(slab1, slab1.cell[0], (0,1,0), slab1.cell[1], (1,0,0))

    else:
        print("Default c axis was selected")
        slab1 = cut(D1, a=[0, 0, 1], b=[1.0, 0.0, 0], c=[0, 1, 0])
        rotate(slab1, slab1.cell[0], (0,1,0), slab1.cell[1], (1,0,0))
    
    slab1.write('rot.vasp', sort=True, vasp5=True)

    Rotation = ase.io.read("rot.vasp")
    domain_size = int(input("Enter the domain wall size (in number of unit cells): "))



    if angle_selection == 1 or angle_selection == 4:
    #120 DW H-H and T-T domain walls
        slab2 = cut(Rotation, a=[-1, 2, 0], b=[-2.0*domain_size, -1.0*domain_size, 0], c=[0, 0, 1])
        rotate(slab2, slab2.cell[0], (0,1,0), slab2.cell[1], (1,0,0))


        slab3 = cut(Rotation, a=[-1, -2, 0], b=[2.0*domain_size, -1.0*domain_size, 0], c=[0, 0, 1])
        rotate(slab3, slab3.cell[0], (0,1,0), slab3.cell[1], (1,0,0))

        #OR for domain 1
        a1 = [-1, 2, 0]
        b1 = (-1, 2, 0)
        c1 = [0, 0, 1]
        print ("a b c")
        print("{} {} {}".format (a1, b1, c1))

        #OR for domain 2
        a2 = [-1, -2, 0]
        b2 = (2, -1, 0)
        c2 = [0, 0, 1]
        print ("a b c")
        print("{} {} {}".format (a2, b2, c2))
        print ("This OR create H-H and T-T domain walls")


        slab2.write('120_D1.vasp', sort=True, vasp5=True)
        slab3.write('120_D2.vasp', sort=True, vasp5=True)

        slab120hh = stack(slab3, slab2, axis=1, maxstrain=None)
        os.makedirs(os.path.join(current_path, 'O120'))
        slab120hh.write(os.path.join(current_path, 'O120', '120_HH_TT_DW.vasp'), sort=True, vasp5=True)
        slab2.write(os.path.join(current_path, 'O120', 'D1.vasp'), sort=True, vasp5=True)
        slab3.write(os.path.join(current_path, 'O120', 'D2.vasp'), sort=True, vasp5=True)

        print("\033[1;31;40mWarning: This code generates duplicate atoms at the domain wall, use VESTA to remove duplicated or closer atoms (with 0.5Å cuttoff).\033[0m")



    if angle_selection == 1 or angle_selection == 4:

        #120 DW H-T domain walls

        slab2 = cut(Rotation, a=[-1*domain_size, 2*domain_size, 0], b=[-2.0, -1.0, 0], c=[0, 0, 1])
        rotate(slab2, slab2.cell[0], (0,1,0), slab2.cell[1], (1,0,0))

        #slab2 generates (110) plane

        slab3 = cut(Rotation, a=[-1*domain_size, -2*domain_size, 0], b=[2.0, -1.0, 0], c=[0, 0, 1])
        rotate(slab3, slab3.cell[0], (0,1,0), slab3.cell[1], (1,0,0))

        #OR for domain 1
        a1 = [-1, 2, 0]
        b1 = (-2, -1, 0)
        c1 = [0, 0, 1]
        print ("a b c")
        print("{} {} {}".format (a1, b1, c1))

        #OR for domain 2
        a2 = [-1, -2, 0]
        b2 = (2, -1, 0)
        c2 = [0, 0, 1]
        print ("a b c")
        print("{} {} {}".format (a2, b2, c2))
        print ("This OR create H-T domain walls")


        slab2.write('120_D1.vasp', sort=True, vasp5=True)
        slab3.write('120_D2.vasp', sort=True, vasp5=True)

        slab120HT = stack(slab3, slab2, axis=0, maxstrain=None)
        os.makedirs(os.path.join(current_path, 'O120_HT'))
        slab120HT.write(os.path.join(current_path, 'O120_HT', '120_HT_DW.vasp'), sort=True, vasp5=True)
        slab2.write(os.path.join(current_path, 'O120_HT', 'D1_120.vasp'), sort=True, vasp5=True)
        slab3.write(os.path.join(current_path, 'O120_HT', 'D2_120.vasp'), sort=True, vasp5=True)


        print("\033[1;31;40mWarning: This code generates duplicate atoms at the domain wall, use VESTA to remove duplicated or closer atoms (with 0.5Å cuttoff).\033[0m")

        #Calculatue lattice strain
        a1, b1, c1 = slab1.cell
        a2, b2, c2 = slab2.cell

        print ('strain along a (%):', (norm(a1) - norm(a2)) / norm(a2) * 100.)
        print ('strain along b (%):', (norm(b1) - norm(b2)) / norm(b2) * 100.)
        print ('strain along c (%):', (norm(c1) - norm(c2)) / norm(c2) * 100.)


    if angle_selection == 2 or angle_selection == 4:

        #180 DW 

        slab2 = cut(Rotation, a=[1, 0, 0], b=[0, domain_size, 0], c=[0, 0, 1])
        rotate(slab2, slab2.cell[0], (0,1,0), slab2.cell[1], (1,0,0))

        #slab2 generates (110) plane

        slab3 = cut(Rotation, a=[-1, 0, 0], b=[0, -domain_size, 0], c=[0, 0, 1])
        rotate(slab3, slab3.cell[0], (0,1,0), slab3.cell[1], (1,0,0))

        #OR for 180 domain 1
        a1 = [1, 0, 0]
        b1 = (0, 1, 0)
        c1 = [0, 0, 1]
        print ("a b c")
        print("{} {} {}".format (a1, b1, c1))
    
        #OR for 180 domain 2
        a2 = [-1, 0, 0]
        b2 = (0, -1, 0)
        c2 = [0, 0, 1]
        print ("a b c")
        print("{} {} {}".format (a2, b2, c2))
        print ("This OR create 180 domain walls")


        slab2.write('180_D1.vasp', sort=True, vasp5=True)
        slab3.write('180_D2.vasp', sort=True, vasp5=True)

        slab180 = stack(slab3, slab2, axis=1, maxstrain=None)
        os.makedirs(os.path.join(current_path, 'O180'))
        slab180.write(os.path.join(current_path, 'O180', '180_DW.vasp'), sort=True, vasp5=True)
        slab2.write(os.path.join(current_path, 'O180', 'D1_180.vasp'), sort=True, vasp5=True)
        slab3.write(os.path.join(current_path, 'O180', 'D2_180.vasp'), sort=True, vasp5=True)


        print("\033[1;31;40mCaution: It is always best practice to visualize structure.\033[0m")
        
        #Calculatue lattice strain
        a1, b1, c1 = slab1.cell
        a2, b2, c2 = slab2.cell

        print ('strain along a (%):', (norm(a1) - norm(a2)) / norm(a2) * 100.)
        print ('strain along b (%):', (norm(b1) - norm(b2)) / norm(b2) * 100.)
        print ('strain along c (%):', (norm(c1) - norm(c2)) / norm(c2) * 100.)

    if angle_selection == 3 or angle_selection == 4:
    #90 DW 

        slab2 = cut(Rotation, a=[0, 1*domain_size, 0], b=[-1, 0, 0], c=[0, 0, 1])
        rotate(slab2, slab2.cell[0], (0,1,0), slab2.cell[1], (1,0,0))

        #slab2 generates (110) plane

        slab3 = cut(Rotation, a=[-1*domain_size, 0, 0], b=[0, -1, 0], c=[0, 0, 1])
        rotate(slab3, slab3.cell[0], (0,1,0), slab3.cell[1], (1,0,0))

        #OR for 90 domain 1
        a1 = [0, 1, 0]
        b1 = (-1, 0, 0)
        c1 = [0, 0, 1]
        print ("a b c")
        print("{} {} {}".format (a1, b1, c1))

        #OR for 90 domain 2
        a2 = [-1, 0, 0]
        b2 = (0, -1, 0)
        c2 = [0, 0, 1]
        print ("a b c")
        print("{} {} {}".format (a2, b2, c2))
        print ("This OR create 90 domain walls")


        slab2.write('90_D1.vasp', sort=True, vasp5=True)
        slab3.write('90_D2.vasp', sort=True, vasp5=True)

        slab90 = stack(slab3, slab2, axis=0, maxstrain=None)

        os.makedirs(os.path.join(current_path, 'O90'))
        slab90.write(os.path.join(current_path, 'O90', '90_DW.vasp'), sort=True, vasp5=True)
        slab2.write(os.path.join(current_path, 'O90', 'D1_90.vasp'), sort=True, vasp5=True)
        slab3.write(os.path.join(current_path, 'O90', 'D2_90.vasp'), sort=True, vasp5=True)

        print("\033[1;31;40mCaution: It is always best practice to visualize structure.\033[0m")
        
        #Calculatue lattice strain
        a1, b1, c1 = slab1.cell
        a2, b2, c2 = slab2.cell

        print ('strain along a (%):', (norm(a1) - norm(a2)) / norm(a2) * 100.)
        print ('strain along b (%):', (norm(b1) - norm(b2)) / norm(b2) * 100.)
        print ('strain along c (%):', (norm(c1) - norm(c2)) / norm(c2) * 100.)

        supercell_size = int(input("Enter size of supercell (in number of unit cells): "))
        if angle_selection == 1 or angle_selection == 4:
            slab120hh_supercell = slab120hh.repeat([supercell_size, 1, supercell_size])
            slab120hh_supercell.write(os.path.join(current_path, 'O120', 'O120HH_supercell.vasp'), sort=True, vasp5=True)
        if angle_selection == 1 or angle_selection == 4:
            slab120HT_supercell = slab120HT.repeat([1, supercell_size, supercell_size])
            slab120HT_supercell.write(os.path.join(current_path, 'O120_HT', 'O120HT_supercell.vasp'), sort=True, vasp5=True)
        if angle_selection == 2 or angle_selection == 4:
            slab180_supercell = slab180.repeat([supercell_size, 1, supercell_size])
            slab180_supercell.write(os.path.join(current_path, 'O180', 'O180_supercell.vasp'), sort=True, vasp5=True)
        if angle_selection == 3 or angle_selection == 4:
            slab90_supercell = slab90.repeat([1, supercell_size, supercell_size])
            slab90_supercell.write(os.path.join(current_path, 'O90', 'O180_supercell.vasp'), sort=True, vasp5=True)

# Manually develop interfaces/DW if you have ORs
if system_selection == 7:
    def create_domain_wall(filename1, filename2, domain_size):

    # Find the path of the current directory
     current_path = os.getcwd()

    filename2 = input("Enter the input domain2 file name (with extension): ")

    # Read the input file
    D2 = ase.io.read(filename2)

    def get_too_close(atoms, cutoff):
        r = atoms.get_positions()
        d = atoms.get_all_distances()
        i, j = np.where(np.triu(d <= cutoff, k=1))
        too_close = np.unique(np.concatenate((i, j)))
        print(f"Too close atoms: {too_close}")
        return too_close


    
    # initialize colorama
    init()

    #Creating planes

    # define lattice directions for slab1
    a_input = input(Fore.GREEN + Style.BRIGHT + "Enter three comma-separated values for domain 1 lattice direction a: " + Style.RESET_ALL)
    a = [float(value.strip()) for value in a_input.split(',')]

    b_input = input(Fore.GREEN + Style.BRIGHT + "Enter three comma-separated values for domain 1 lattice direction b: " + Style.RESET_ALL)
    b = [float(value.strip()) for value in b_input.split(',')]

    c_input = input(Fore.GREEN + Style.BRIGHT + "Enter three comma-separated values for domain 1 lattice direction c: " + Style.RESET_ALL)
    c = [float(value.strip()) for value in c_input.split(',')]

    # define lattice directions for slab2
    a_input = input(Fore.BLUE + Style.BRIGHT + "Enter three comma-separated values for domain 2 lattice direction a: " + Style.RESET_ALL)
    a1 = [float(value.strip()) for value in a_input.split(',')]

    b_input = input(Fore.BLUE + Style.BRIGHT + "Enter three comma-separated values for domain 2 lattice direction b: " + Style.RESET_ALL)
    b1 = [float(value.strip()) for value in b_input.split(',')]

    c_input = input(Fore.BLUE + Style.BRIGHT + "Enter three comma-separated values for domain 2 lattice direction c: " + Style.RESET_ALL)
    c1 = [float(value.strip()) for value in c_input.split(',')]

    # create and manipulate slab1 model
    slab1 = cut(D1, a=a, b=b, c=c)
    rotate(slab1, slab1.cell[0], (0,1,0), slab1.cell[1], (1,0,0))
    os.makedirs(os.path.join(current_path, 'Misc'))
    slab1.write(os.path.join(current_path, 'Misc', 'Misc_domain1.vasp'), sort=True, vasp5=True)

    #view(slab1)

    # create and manipulate slab2 model
    slab2 = cut(D2, a=a1, b=b1, c=c1)
    rotate(slab2, slab2.cell[0], (0,1,0), slab2.cell[1], (1,0,0))
    slab2.write(os.path.join(current_path, 'Misc', 'Misc_domain2.vasp'), sort=True, vasp5=True)

    #view(slab2)

    interface_direction = int(input("Enter the stacking direction 0 for a, 1 for b and 2 for c): "))

    slab = stack(slab1, slab2, axis=interface_direction, maxstrain=None)
    slab.write(os.path.join(current_path, 'Misc', 'Misc_interface.vasp'), sort=True, vasp5=True)
    
    # Remove atoms closer than 0.5 Å in the stacked slab
    too_close_slab = get_too_close(slab, 0.6)
    slab = slab[np.setdiff1d(np.arange(len(slab)), too_close_slab)]

    slab.write('NDW.vasp', sort=True, vasp5=True)

    print("\033[1;31;40mWarning: This code might create domain wall artifacts, like missing or duplicate atoms, at the domain wall. Therefore, manual adjustment may be needed.\033[0m")

    a1, b1, c1 = slab1.cell
    a2, b2, c2 = slab2.cell

    print ('strain along a (%):', (norm(a1) - norm(a2)) / norm(a2) * 100.)
    print ('strain along b (%):', (norm(b1) - norm(b2)) / norm(b2) * 100.)
    print ('strain along c (%):', (norm(c1) - norm(c2)) / norm(c2) * 100.)
    print("\033[1;31;40mWarning: This code could generate interface/domain wall artifacts (i.e., Oxygen atoms, duplicate atoms etc,) at the interface, thus it requires manual adjustment.\033[0m")

