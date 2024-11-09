#!/usr/bin/env python

# Haldane model from Phys. Rev. Lett. 61, 2015 (1988)

from pythtb import * 
import numpy as np

from pybott import bott

def haldane_model(n_side=6, t1=1, t2=0.2j, delta=0, pbc=True):
    t2c = t2.conjugate()

    lat=[[1.0,0.0],[0.5,np.sqrt(3.0)/2.0]]
    orb=[[1./3.,1./3.],[2./3.,2./3.]]

    my_model=tb_model(2,2,lat,orb)

    my_model.set_onsite([-delta,delta])

    my_model.set_hop(t1, 0, 1, [ 0, 0])
    my_model.set_hop(t1, 1, 0, [ 1, 0])
    my_model.set_hop(t1, 1, 0, [ 0, 1])

    my_model.set_hop(t2 , 0, 0, [ 1, 0])
    my_model.set_hop(t2 , 1, 1, [ 1,-1])
    my_model.set_hop(t2 , 1, 1, [ 0, 1])
    my_model.set_hop(t2c, 1, 1, [ 1, 0])
    my_model.set_hop(t2c, 0, 0, [ 1,-1])
    my_model.set_hop(t2c, 0, 0, [ 0, 1])

    # cutout finite model first along direction x
    tmp_model=my_model.cut_piece(n_side,0,glue_edgs=pbc)
    # cutout also along y direction 
    fin_model=tmp_model.cut_piece(n_side,1,glue_edgs=pbc)
    
    (evals,evecs)=fin_model.solve_all(eig_vectors=True)
    
    return fin_model.get_orb(), evals, evecs.T

def haldane_ham(n_side=6, t1=1, t2=0.2j, delta=0, pbc=True):
    t2c = t2.conjugate()

    lat=[[1.0,0.0],[0.5,np.sqrt(3.0)/2.0]]
    orb=[[1./3.,1./3.],[2./3.,2./3.]]

    my_model=tb_model(2,2,lat,orb)

    my_model.set_onsite([-delta,delta])

    my_model.set_hop(t1, 0, 1, [ 0, 0])
    my_model.set_hop(t1, 1, 0, [ 1, 0])
    my_model.set_hop(t1, 1, 0, [ 0, 1])

    my_model.set_hop(t2 , 0, 0, [ 1, 0])
    my_model.set_hop(t2 , 1, 1, [ 1,-1])
    my_model.set_hop(t2 , 1, 1, [ 0, 1])
    my_model.set_hop(t2c, 1, 1, [ 1, 0])
    my_model.set_hop(t2c, 0, 0, [ 1,-1])
    my_model.set_hop(t2c, 0, 0, [ 0, 1])

    # cutout finite model first along direction x
    tmp_model=my_model.cut_piece(n_side,0,glue_edgs=pbc)
    # cutout also along y direction 
    fin_model=tmp_model.cut_piece(n_side,1,glue_edgs=pbc)
    
    (evals,evecs)=fin_model.solve_all(eig_vectors=True)
    
    return fin_model.get_orb(), fin_model._gen_ham()

            


