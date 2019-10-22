# -*- coding: utf-8 -*-
"""
Network Visualization Module
============

Module for rendering the network, using [sigma.js](http://sigmajs.org/) or [d3.js](https://d3js.org/) frameworks.

"""
from mesa.visualization.ModularVisualization import VisualizationElement


class LeafletModule(VisualizationElement):
    """A MapModule for Leaflet maps."""

    package_includes = []
    local_includes = ["LeafletVisualization/leaflet.js", "LeafletVisualization/LeafletMap.js"]
    # local_includes = ["LeafletVisualization/LeafletMap.js"]

    def __init__(
        self, portrayal_method, view=[0, 0], zoom=10, map_height=500, map_width=500
    ):
        self.portrayal_method = portrayal_method
        self.map_height = map_height
        self.map_width = map_width
        self.view = view
        new_element = "new LeafletModule({}, {}, {}, {})"
        new_element = new_element.format(view, zoom, map_width, map_height)
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        return self.portrayal_method(model.G)['nodes']
