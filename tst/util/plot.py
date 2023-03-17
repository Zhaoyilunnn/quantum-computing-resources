from util.plot import *


class TestUtilPlot:

    def test_plot_bar(self):
        data = [1, 2, 3, 4, 5]
        labels = ['A', 'B', 'C', 'D', 'E']
        plot_bar(data, labels, figname="test_plot_bar.png")
