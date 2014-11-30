# -*- encoding:utf-8 -*-
#!/usr/bin/python

from multiprocessing import Process, Queue
import time
import locale, gettext
import os

from gi.repository import Gtk
from gi.repository import GLib
import numpy as np # stupid!!!
from numpy import *
import matplotlib.pyplot as plt

import compy as cp

APP = "schr"
TRANSLATION_DIR = ".\translations"
VERSION = "0.1~alpha"

# Localization
if os.getenv('LANG') is not None:
    locale.setlocale(locale.LC_ALL, '')
    locale.bindtextdomain(APP, TRANSLATION_DIR)
    gettext.bindtextdomain(APP, TRANSLATION_DIR)
    gettext.textdomain(APP)
    lang = gettext.translation(APP, TRANSLATION_DIR, lang)
    _ = lang.gettext 
    gettext.install(APP, TRANSLATION_DIR)

# Theta function, useful for step potentials and wells
def theta(x):
    if x <= 0:
        return 0
    else:
        return 1

def call_schr(q, tn, *args, **kwargs):
    def callback(fraction):
        q.put({"type": "fraction", "fraction": fraction})
    
    ev, ef = cp.schrodinger.solve_numerov(callback=callback, *args, **kwargs)
    
    q.put({"type": "result", "result": (ev, ef, args[1], tn)})

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
        self.ene_e = self.builder.get_object("energy_entry")
        self.pre_s = self.builder.get_object("precision_spin")
        self.mass_e = self.builder.get_object("mass_entry")
        self.plank_e = self.builder.get_object("plank_entry")
        self.norm_c = self.builder.get_object("norm_check")
        self.prob_c = self.builder.get_object("probability_check")
        self.pot_c = self.builder.get_object("potential_check")
        
        self.min_l = self.builder.get_object("min_label")
        self.max_l = self.builder.get_object("max_label")
        self.n_l = self.builder.get_object("n_label")
        self.ene_l = self.builder.get_object("energy_label")
        self.inc_l = self.builder.get_object("increment_label")
        self.pre_l = self.builder.get_object("precision_label")

        self.times = {}

    def on_solve(self, button):
        pot_txt = self.pot_e.get_text()

        fro = self.from_s.get_value()
        to = self.to_s.get_value()
        num_points = int(self.points_s.get_value())

        D = cp.Domain(fro, to, num_points)
        try:
            V = [eval(pot_txt) for x in D.generator()]
        except:
            print("Please insert a valid potential funcion.")
            return 0
        
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
            h = float(self.plank_e.get_text())
        except:
            print("Plank's constant must be a number. Assuming Plank's constant = 1.")
            h = 1
        
        try:
            E = float(self.ene_e.get_text())
        except:
            print("Energy must be a number. Assuming Energy = 1.")
            E = 1
            
        norm = self.norm_c.get_active()
        prob = self.prob_c.get_active()
        
        q = Queue()
        if erange:
            E_min = self.emin_s.get_value()
            E_max = self.emax_s.get_value()
            
            p = Process(target=call_schr, args=[q, len(self.times), D, V, boundary_start, boundary_end],
                kwargs={"E_min": E_min, "E_max": E_max, "dE": dE, "precision": precision, "h": h,
                "m": mass, "normalized": norm})
        else:
            eigen_num = int(self.enum_s.get_value())
           
            p = Process(target=call_schr, args=[q, len(self.times), D, V, boundary_start, boundary_end],
                kwargs={"eigen_num": eigen_num, "dE": dE, "precision": precision, "h": h,
                "m": mass, "normalized": norm})
        
        self.times[len(self.times)] = time.time()
        p.start()
        
        GLib.timeout_add(100, self.update, p, q, prob, D)
    
    def update(self, p, q, prob, D):
        while True:
            try:
                elem = q.get()
            except Queue.Empty:
                return True

            if elem["type"] == "result":
                ev, ef, V, tn = elem["result"]

                end_time = time.time()
                start_time = self.times[tn]
                elapsed_time = end_time - start_time

                p = Process(target=self.display, args=(prob, D, ev, ef, V))
                p.start()

                self.show_results(elapsed_time)
                
                return False
            elif elem["type"] == "fraction":
                self.progress(elem["fraction"])

    def show_results(self, elapsed_time):
        # Open results window
        builder = Gtk.Builder()
        builder.add_from_file("glade/results.glade")

        window = builder.get_object("results_win")
        window.show_all()

        time_l = builder.get_object("time_label")

        time_l.set_text("{:.3} s".format(elapsed_time))
    
    def display(self, prob, D, ev, ef, V):
        if prob:
            ps = [cp.schrodinger.square_modulus(psi) for psi in ef]
            self.plot(D, ev, ps, V)
        else:
            self.plot(D, ev, ef, V)
    
    def progress(self, fraction):
        self.pot_e.set_progress_fraction(fraction)
        while Gtk.events_pending():
            Gtk.main_iteration()
    
    def plot(self, D, ev, ef, V):
        prob = self.prob_c.get_active()
        show_potential = self.pot_c.get_active()

        if show_potential:
            f = plt.figure(figsize=(8, 10))
            ax = f.add_subplot(211)
        else:
            f = plt.figure()
            ax = f.add_subplot()
        
        for v, psi in zip(ev, ef):
            plt.plot(D.as_array(), psi, label=v)

        plt.title("Solutions")
        plt.xlabel("x")
        if prob:
            plt.ylabel(u"|Ψ|²")
        else:
            plt.ylabel(u"Ψ")
        plt.grid(True)
        plt.legend()

        if show_potential:
            ax2 = f.add_subplot(212)
            plt.plot(D.as_array(), V, label="Potential")
        
            ymin = np.min(V)
            ymax = np.max(V)

            if ymin < 0:
                ymin *= 1.1
            elif ymin == 0:
                ymin = -ymax*0.1
            else:
                ymin *= 0.9

            if ymax < 0:
                ymax *= 0.9
            elif ymax == 0:
                ymax = -ymin*0.1
            else:
                ymax *= 1.1

            print(ymin, ymax)
            plt.ylim((ymin, ymax))

            plt.xlabel("x")
            plt.ylabel(u"V")
            plt.grid(True)
            plt.legend()
            f.subplots_adjust(bottom=0.08, top=0.92)
        
        plt.show()

    def set_energy_sensitive(self, *args):
        widgets = [self.emin_s, self.emax_s, self.enum_s,
            self.ene_e, self.einc_s, self.pre_s]
        labels = [self.min_l, self.max_l, self.n_l,
            self.ene_l, self.inc_l, self.pre_l]

        for b, w, l in zip(args, widgets, labels):
            w.set_sensitive(b)
            l.set_sensitive(b)
        
    def on_set_range(self, radio):
        self.set_energy_sensitive(True, True, False, False, True, True)
        
    def on_set_enum(self, radio):
        self.set_energy_sensitive(False, False, True, False, True, True)
        
    def on_set_energy(self, radio):
        self.set_energy_sensitive(False, False, False, True, False, False)

    def on_normalized_toggled(self, check):
        if self.norm_c.get_active():
            self.prob_c.set_sensitive(True)
        else:
            self.prob_c.set_sensitive(False)

    def on_window_delete(self, *args):
        Gtk.main_quit(*args)


if __name__ == '__main__':
    builder = Gtk.Builder()
    builder.set_translation_domain(APP)
    builder.add_from_file("glade/gui.glade")
    builder.connect_signals(Schr(builder))

    window = builder.get_object("SchrWin")
    window.show_all()

    Gtk.main()
