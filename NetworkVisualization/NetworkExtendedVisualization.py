# -*- coding: utf-8 -*-
"""
Network Visualization Module
============

Module for rendering the network, using [sigma.js](http://sigmajs.org/) or [d3.js](https://d3js.org/) frameworks.

"""
from mesa.visualization.ModularVisualization import VisualizationElement


class NetworkExtendedModule(VisualizationElement):
    package_includes = ["d3.min.js"]
    local_includes = ["NetworkVisualization/NetworkExtendedModule_d3.js"]

    def __init__(self, portrayal_method, canvas_height=500, canvas_width=500):
        self.portrayal_method = portrayal_method
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        new_element = ("new NetworkExtendedModule({}, {})".
                       format(self.canvas_width, self.canvas_height))
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        return self.portrayal_method(model.G)
