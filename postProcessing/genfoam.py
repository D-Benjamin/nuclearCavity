#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 22:39:40 2018

@author: rodrigo
"""

class genfoamData(object):
    
    def __init__(self, fluxGroups, precursorsGroups):
        
        self.flux = {'label': [],
                     'title': [],
                     'unit': ' ($ \mathrm{m}^{-2} \cdot \mathrm{s}^{-1} $)',
                     'rank': 0}
        for i in range(fluxGroups):
            self.flux['label'].append('flux{}'.format(i))
            self.flux['title'].append('Flux{}'.format(i))
        
        self.prec = {'label': [],
                     'title': [],
                     'unit': ' ($ \mathrm{m}^{-3} $)',
                     'rank': 0}
        for i in range(precursorsGroups):
            self.prec['label'].append('prec{}'.format(i))
            self.prec['title'].append('Precursors{}'.format(i))
        
        self.oneGroupFlux = {'label': ['oneGroupFlux'],
                             'title': ['Integral flux'],
                             'unit': ' ($ \mathrm{m}^{-2} \cdot \mathrm{s}^{-1} $)',
                             'rank': 0}
        
        self.rhoCoolNeutro = {'label': ['rhoCoolNeutro'],
                              'title': ['Coolant density@neutronics'],
                              'unit': ' ($ \mathrm{kg} \cdot \mathrm{m}^{-3} $)',
                              'rank': 0}
        
        self.T = {'label': ['T'],
                  'title': ['Temperature'],
                  'unit': ' ($ \mathrm{K} $)',
                  'rank': 0}

        self.p = {'label': ['p'],
                  'title': ['Pressure'],
                  'unit': ' ($ \mathrm{Pa} $)',
                  'rank': 0}
        
        self.U = {'label': ['U'],
                  'title': ['Velocity'],
                  'unit': ' ($ \mathrm{m} \cdot \mathrm{s}^{-1} $)',
                  'rank': 1}
