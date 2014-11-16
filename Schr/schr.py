# -*- encoding:utf-8 -*-
#!/usr/bin/python

import numpy as np
from numpy import *
import matplotlib.pyplot as plt
from gi.repository import Gtk

import compy as cp

class Schr():
    def __init__(self, builder):
        self.builder = builder
        
        self.pot_e = self.builder.get_object("potential_entry")
        self.from_s = self.builder.get_object("from_spin")
        self.to_s = self.builder.get_object("to_spin")
        self.points_s = self.builder.get_object("points_spin")
        self.bs_s = self.builder.get_object("bs_spin") # boundary start
        self.be_s = self.builder.get_object("be_spin") # boundary end
        self.rn_r = self.builder.get_object("range_num_radio")
        self.emin_s = self.builder.get_object("emin_spin")
        self.emax_s = self.builder.get_object("emax_spin")
        self.enum_s = self.builder.get_object("enum_spin")
        self.einc_s = self.builder.get_object("einc_spin")
        self.pre_s = self.builder.get_object("precision_spin")
        self.mass_e = self.builder.get_object("mass_entry")
        self.plank_e = self.builder.get_object("plank_entry")
        self.norm_c = self.builder.get_object("norm_check")
        self.prob_c = self.builder.get_object("probability_check")

    def on_solve(self, button):
        pot_txt = self.pot_e.get_text()

        fro = self.from_s.get_value()
        to = self.to_s.get_value()
        num_points = int(self.points_s.get_value())

        D = cp.Domain(fro, to, num_points)
        V = [eval(pot_txt) for x in D.generator()]
        
        boundary_start = self.bs_s.get_value()
        boundary_end = self.be_s.get_value()
        
        erange = self.rn_r.get_active()
        
        dE = self.einc_s.get_value()
        precision = self.pre_s.get_value()
        
        try:
            mass = float(self.mass_e.get_text())
        except:
            print("Mass must be a number. Assuming mass = 1.")
            mass = 1
        
        try:
            h = float(self.mass_e.get_text())
        except:
            print("Plank's constant must be a number. Assuming Plank's constant = 1.")
            h = 1
            
        norm = self.norm_c.get_active()
        prob = self.prob_c.get_active()
        
        if erange:
            E_min = self.emin_s.get_value()
            E_max = self.emax_s.get_value()
            
            ev, ef = cp.schrodinger.solve_numerov(D, V, boundary_start, boundary_end, E_min=E_min, E_max=E_max,
                dE=dE, precision=precision, h=h, m=mass, normalized=norm)
        else:
            eigen_num = int(self.enum_s.get_value())
            ev, ef = cp.schrodinger.solve_numerov(D, V, boundary_start, boundary_end, eigen_num=eigen_num,
                dE=dE, precision=precision, h=h, m=mass, normalized=norm)
        
        if prob:
            ps = [cp.schrodinger.square_modulus(psi) for psi in ef]
            self.plot(D, ev, ps)
        else:
            self.plot(D, ev, ef)
    
    def plot(self, D, ev, ef):
        f = plt.figure()
        ax = f.add_subplot()
        
        for v, psi in zip(ev, ef):
            plt.plot(D.as_array(), psi, label=v)
        
        plt.xlabel("x")
        plt.ylabel(u"Ψ")
        plt.grid(True)
        plt.legend()
        
        plt.show()

    def on_window_delete(self, *args):
        Gtk.main_quit(*args)

builder = Gtk.Builder()
builder.add_from_file("glade/gui.glade")
builder.connect_signals(Schr(builder))

window = builder.get_object("SchrWin")
window.show_all()

Gtk.main()
