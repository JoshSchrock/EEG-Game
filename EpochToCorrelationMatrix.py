import mne_connectivity
import mne
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import patches
import os

class EpochsToCorrelation:
    def __init__(self, epoch_data, method='envelope', threshold=None):
        self.epoch_data = epoch_data
        self.corr_matrix = None
        self.threshold = threshold

        if method == 'envelope':
            self.envelope()
        elif method == 'pearson':
            self.pearson()

        print(np.array(self.corr_matrix))

    def envelope(self):
        corr_matrix = mne_connectivity.envelope_correlation(self.epoch_data).get_data()
        new_corr_matrix = []
        for matrix in corr_matrix:
            new_matrix = []
            for i in matrix:
                list = []
                for j in i:
                    list.append(j[0])
                new_matrix.append(list)
            new_corr_matrix.append(new_matrix)
        self.corr_matrix = new_corr_matrix

        if self.threshold is None:
            self.threshold = np.nanquantile(self.corr_matrix, 0.8)

    def pearson(self):
        self.corr_matrix = []
        for epoch in self.epoch_data:
            cur_array = np.array(epoch)
            pearson = np.corrcoef(cur_array)
            self.corr_matrix.append(pearson.tolist())

        if self.threshold is None:
            self.threshold = np.quantile(self.corr_matrix, 0.8)

    def show_figures(self, plot_matrix=True, draw_network=True):
        if plot_matrix and not draw_network:
            for index, matrix in enumerate(self.corr_matrix):
                self.plot(index, matrix)
        elif draw_network and not plot_matrix:
            for index, matrix in enumerate(self.corr_matrix):
                self.draw_network(index, matrix)
        elif draw_network and plot_matrix:
            for index, matrix in enumerate(self.corr_matrix):
                self.plot(index, matrix)
                self.draw_network(index, matrix)

    def plot(self, index, matrix):
        color_lims = np.percentile(np.array(matrix), [5, 95])
        f = plt.figure(figsize=(3, 2))
        plt.matshow(matrix, fignum=f.number, clim=color_lims)
        cb = plt.colorbar()
        cb.ax.tick_params(labelsize=14)
        plt.title(f'Covariance Correlation Matrix {str(index)}')

    def draw_network(self, index, matrix):
        # plot------------------------------
        fig, ax = plt.subplots(figsize=(8, 8))
        xy_center = [2, 2]
        radius = 2

        # left ear
        circle = patches.Ellipse(xy=[0, 2], width=0.4, height=1.0, angle=0, edgecolor="k", facecolor="w", zorder=0)
        ax.add_patch(circle)
        # right ear
        circle = patches.Ellipse(xy=[4, 2], width=0.4, height=1.0, angle=0, edgecolor="k", facecolor="w", zorder=0)
        ax.add_patch(circle)
        # nose
        xy = [[1.6, 3.6], [2, 4.3], [2.4, 3.6]]
        polygon = patches.Polygon(xy=xy, edgecolor="k", facecolor="w", zorder=0)
        ax.add_patch(polygon)
        # head
        circle = patches.Circle(xy=xy_center, radius=radius, edgecolor="k", facecolor="w", zorder=0)
        ax.add_patch(circle)

        # nodes
        G = nx.Graph()
        nodes_list = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']
        G.add_nodes_from(nodes_list)
        pos = {'AF3': [1.5, 3.8], 'F7': [0.4, 3], 'F3': [1.2, 3.3], 'FC5': [0.5, 2.5], 'T7': [0, 2], 'P7': [0.4, 1],
               'O1': [1.5, 0.4], 'O2': [2.5, 0.4], 'P8': [3.6, 1], 'T8': [4, 2], 'FC6': [3.5, 2.5], 'F4': [2.8, 3.3],
               'F8': [3.6, 3], 'AF4': [2.5, 3.8]}

        # edges
        for i in range(len(nodes_list)):
            for j in range(len(nodes_list)):
                if i < j:
                    edge = [(nodes_list[i], nodes_list[j])]
                    if matrix[i][j] > self.threshold:
                        G.add_edges_from(edge)
                        nx.draw_networkx_edges(G, pos=pos, edgelist=edge,
                                               width=(10 ** (matrix[i][j] - self.threshold)), edge_color='grey')

        # hot nodes
        color_map = []
        for node in G:
            degree = G.degree(node)
            if degree < 3:
                color_map.append('yellow')
            elif 3 <= degree <= 6:
                color_map.append('orange')
            else:
                color_map.append('r')

        nx.draw(G, pos=pos, with_labels=True, node_color=color_map, edge_color='grey')

        return plt

    def export(self, export_name):
        # make dir
        new_dir = f'{os.getcwd()}\\EEGNetExports\\{export_name}'
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
            os.makedirs(f'{new_dir}\\Chuncks')
        else:
            if not os.path.exists(f'{new_dir}\\Chuncks'):
                os.makedirs(f'{new_dir}\\Chuncks')

        for index, matrix in enumerate(self.corr_matrix):
            # print(ch_data.type)
            plt = self.draw_network(index, matrix)
            pngname = f'{new_dir}\\Chuncks\\chunck_{str(index)}.png'
            plt.savefig(pngname, format="PNG", bbox_inches='tight')

        from PIL import Image

        frames = []

        for i in range(len(self.corr_matrix)):
            file = f'{new_dir}\\Chuncks\\chunck_{str(i)}.png'
            newFrame = Image.open(file)
            frames.append(newFrame)

        # Save into a GIF file that loops forever
        saveFile = f'{new_dir}\\Net_of_{export_name}.gif'
        frames[0].save(saveFile, format='GIF', append_images=frames[1:],
                       save_all=True, duration=300, loop=0)