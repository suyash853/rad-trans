# -*- coding: utf-8 -*-
"""run_RADEX_pythonradex.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sWQSJ_HAQDiMSbeqQduc28Iy0JTEcXGg
"""

import os
import time
import numpy as np
from pythonradex import nebula,helpers
from scipy import constants
import matplotlib.pyplot as plt

def write_radex_inp(inpfilename="test.inp",molfile="hco+.dat",outfilename="hco+.rdx",freqrange=(0,0),tkin=20, part1dens=10000,
                    part1name='H2', part2name=None, part2dens=None, tbk=2.73, ntot=1e12, line=2.0):
    """writes a .inp file in working directory with information to call radex upon. 
  
  Inputs:
  inpfilename: name of file to be created/over-written. (use .inp at the end)
  outfilename: name of file to write the results of the radex program to. 
  molfile: molecular data file of the molecule whose transitions are to be investigated
  freqrange: output frequency range (GHz; 0 0 means unlimited)
  tkin: kinetic temperature (K)
  part1name: string of name of first collision partner. Default 'H2'. Possible- H2, p-H2, o-H2, electrons, H (atoms), He, and H+.
  part1dens: density of first collision partner ( in cm-3)
  part2name: string of name of second collision partner. Default None, leads to no second collision partner being considered.
  part2dens: density of second collision partner ( in cm-3), if any. Default 'None'. (Warning: don't assign value if part2name=None, may lead to error)
  tbk: temperature of background radiation (K)
  ntot: molecular column density (in cm-2)
  line: line width (km/s)     
  """ 
    
    inp=open(inpfilename,'w')
    
    inp.write(molfile+" \n")
    inp.write(outfilename+" \n")
    
    for i in freqrange:
          inp.write(str(i)+" ")
    inp.write(" \n")
    
    inp.write("{:g} \n".format(tkin))
    
    if part2name!=None:
        inp.write("2 \n")
        inp.write(part1name+" \n")
        inp.write("{:g} \n".format(part1dens))
        inp.write(part2name+" \n")
        inp.write("{:g} \n".format(part2dens))
    else: 
        inp.write("1 \n")
        inp.write(part1name+" \n")
        inp.write("{:g} \n".format(part1dens))
   
    inp.write("{:g} \n".format(tbk))
    inp.write("{:g} \n".format(ntot))
    inp.write("{:g} \n".format(line))
    
    inp.write("0 \n")

def run_RADEX(inpfilename="test.inp",molfile="hco+.dat",outfilename="hco+.rdx",freqrange=(0,0),tkin=20, part1dens=10000, part1name='H2',
              part2name=None, part2dens=None, tbk=2.73, ntot=1e12, line=2.0):
    """runs RADEX for given input parameters and writes the output to outfilename.

    Inputs:
  inpfilename: name of file to be created/over-written. (use .inp at the end)
  outfilename: name of file to write the results of the radex program to. 
  molfile: molecular data file of the molecule whose transitions are to be investigated
  freqrange: output frequency range (GHz; 0 0 means unlimited)
  tkin: kinetic temperature (K)
  part1name: string of name of first collision partner. Default 'H2'. Possible- H2, p-H2, o-H2, electrons, H (atoms), He, and H+.
  part1dens: density of first collision partner ( in cm-3)
  part2name: string of name of second collision partner. Default None, leads to no second collision partner being considered.
  part2dens: density of second collision partner ( in cm-3), if any. Default 'None'. (Warning: don't assign value if part2name=None, may lead to error)
  tbk: temperature of background radiation (K)
  ntot: molecular column density (in cm-2)
  line: line width (km/s)     
    """
    start= time.time()
    
    write_radex_inp(inpfilename=inpfilename,molfile=molfile,outfilename=outfilename,freqrange=freqrange,tkin=tkin,part1dens=part1dens,
                part1name=part1name, part2name=part2name, part2dens=part2dens, tbk=tbk,ntot=ntot,line=line)
    
    path= '/home/suyash/Desktop/Intern/Radex/bin'
    os.environ["PATH"] += os.pathsep + path
    os.system("radex < "+inpfilename)
    
    fin=time.time()
    print("\n Time taken:"+str(fin-start))

def read_rdx(outfilename='hco+.rdx'):
    """reads given RADEX output file and returns an array of the computed line fluxes in K km/s for each transition
    
    Inputs:
    outfilename: name of file to be read.
     """
    result=[]
    outfile= open(outfilename)
    
    lines= outfile.readlines()
    
    for i in range(len(lines)):
        w= lines[i].split()
        if w[-1]=='(erg/cm2/s)':
            ind=i
            break
        
    for line in lines[ind+1:]:
        w= line.split()
        result.append(float(w[-2]))
    
    return np.array(result)

def run_pythonradex(molfile="./lamda_file/hco+.dat",tkin=20,ntot=1e12/constants.centi**2,width_v=2*constants.kilo,
                    part1dens=1e4/constants.centi**3,part1name='H2', part2name=None, part2dens=None,
                    ext_background=helpers.CMB_background):
   """runs pythonradex for given input parameters and returns an array of the computed line fluxes in K km/s for each transition 

    Inputs:
  molfile: molecular data file of the molecule whose transitions are to be investigated
  tkin: kinetic temperature (K)
  part1name: string of name of first collision partner. Default 'H2'. Possible- H2, p-H2, o-H2, electrons, H (atoms), He, and H+.
  part1dens: density of first collision partner in m-3
  part2name: string of name of second collision partner. Default None, leads to no second collision partner being considered.
  part2dens: density of second collision partner in m-3, if any. Default 'None'. (Warning: don't assign value if part2name=None, may lead to error)
  ntot: molecular column density in m-2
  width_v: line width in m/s     
    """
    
    coll_partner_densities={part1name:part1dens}
    if part2name!=None:
        coll_partner_densities[part2name]=part2dens
        
    example_nebula = nebula.Nebula(data_filepath=molfile,geometry='uniform sphere',ext_background=ext_background,
                                   Tkin=tkin, coll_partner_densities=coll_partner_densities, Ntot=ntot,line_profile='square',
                                   width_v=width_v)
    example_nebula.solve_radiative_transfer()
    
    Int_I=[]
    for i,line in enumerate(example_nebula.emitting_molecule.rad_transitions):
        meas_nu= (helpers.B_nu(line.nu0,example_nebula.Tex[i])-ext_background(line.nu0))*(1.0-np.exp(-example_nebula.tau_nu0[i]))
        Ta_nu= (constants.c**2)*meas_nu/(2*constants.k*(line.nu0**2))
        kkms= Ta_nu*1.0645*width_v*1e-3
        Int_I.append(kkms)
        
    return np.array(Int_I)

def comparison(molfile='hco+.dat',tkin=20,ntot=1e12,line=2, part1dens=10000,part1name='H2', part2name=None, part2dens=None,
               tbk=2.73):
   """runs RADEX and pythonradex for given input parameters, plots the results obtained by each together for comparison and returns tuple of numpy arrays containing the data.

    Inputs:
    
  molfile: molecular data file of the molecule whose transitions are to be investigated
  tkin: kinetic temperature (K)
  part1name: string of name of first collision partner. Default 'H2'. Possible- H2, p-H2, o-H2, electrons, H (atoms), He, and H+.
  part1dens: density of first collision partner ( in cm-3)
  part2name: string of name of second collision partner. Default None, leads to no second collision partner being considered.
  part2dens: density of second collision partner ( in cm-3), if any. Default 'None'. (Warning: don't assign value if part2name=None, may lead to error)
  tbk: temperature of background radiation (K)
  ntot: molecular column density (in cm-2)
  line: line width (km/s)     
    """
    
    run_RADEX(molfile=molfile,tkin=tkin,ntot=ntot,part1dens=part1dens,part1name=part1name,part2dens=part2dens,
                 part2name=part2name,tbk=tbk, line=line)
    x=read_rdx()
    
    if tbk==2.73:
        ext_background=helpers.CMB_background
    if part2dens!=None:
        part2dens= part2dens/constants.centi**3
    molfile_p='./lamda_file/'+molfile    
    y=run_pythonradex(molfile=molfile_p,tkin=tkin,ntot=ntot/constants.centi**2,part1dens=part1dens/constants.centi**3,
                      part1name=part1name,part2dens=part2dens,part2name=part2name,
                      width_v=line*constants.kilo, ext_background=ext_background)
    
    plt.figure()
    plt.plot(range(len(x)),x)
    plt.plot(range(len(y)),y)

    return (x,y)