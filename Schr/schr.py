#!/usr/bin/python

import numpy as np
from numpy import *
from gi.repository import Gtk

import compy as cp

class Schr():
    def __init__(self, builder):
        self.builder = builder
        
        self.pot_e = self.builder.get_object("potential_entry")
        self.from_s = self.builder.get_object("from_spin")
        self.to_s = self.builder.get_object("to_spin")
        self.points_s = self.builder.get_object("points_spin")

    def on_solve(self, button):
        pot_txt = self.pot_e.get_text()

        fro = self.from_s.get_value()
        to = self.to_s.get_value()
        num_points = int(self.points_s.get_value())

        D = cp.Domain(fro, to, num_points)
        V = [eval(pot_txt) for x in D.generator()]
        ev, ef = cp.schrodinger.solve_numerov(D, V, 1, 1, eigen_num=5)
        
        print(ev)

    def on_window_delete(self, *args):
        Gtk.main_quit(*args)

builder = Gtk.Builder()
builder.add_from_file("glade/gui.glade")
builder.connect_signals(Schr(builder))

window = builder.get_object("SchrWin")
window.show_all()

Gtk.main()
