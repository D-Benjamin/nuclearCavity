#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 16:31:06 2019

@author: deoliveira_r
"""

conf = {'1.25': {'thres': 0.9,
                 'min_dist': 200},
        '2.5': {'thres': 0.5,
                'min_dist': 100},
        '5':  {'thres': 0.5,
               'min_dist': 100},
        '10':  {'thres': 0.7,
                'min_dist': 100},
        '20':  {'thres': 0.9,
                'min_dist': 200},
        '40': {'thres': 0.9,
               'min_dist': 2000},
        '80': {'thres': 0.9,
               'min_dist': 2000} }

end_time = 520

# peakutils options
pthresh = 0.9
pmin_dist = 2000
