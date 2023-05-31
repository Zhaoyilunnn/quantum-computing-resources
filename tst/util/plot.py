from util.plot import *


class TestUtilPlot:
    def test_plot_single_bar(self):
        data = [1, 2, 3, 4, 5]
        labels = ["A", "B", "C", "D", "E"]
        plot_bar(data, labels, figname="test_plot_bar.png")

    def test_plot_multi_bars(self):
        data0 = [1, 2, 3, 4, 5]
        data1 = [3, 2, 1, 5, 4]
        labels = ["A", "B", "C", "D", "E"]
        data_labels = ["M", "N"]
        plot_bar(
            [data0, data1],
            labels,
            data_labels=data_labels,
            figname="test_plot_multi_bars.png",
        )
