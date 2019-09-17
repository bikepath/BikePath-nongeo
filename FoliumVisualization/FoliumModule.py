from mesa.visualization.ModularVisualization import VisualizationElement
import osmnx as ox


class FoliumModule(VisualizationElement):
    local_includes = ["FoliumVisualization/folium_module.js"]
    canvas_height = 500
    canvas_width = 500

    def __init__(self, height=500, width=500):
        '''
        Instantiate a new FoliumModule
        '''
        self.height = height
        self.width = width
        new_element = ("new Folium_Module({}, {})".
                       format(self.width, self.height))
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        folium_map = ox.plot_graph_folium(model.G)
        return folium_map
