import matplotlib
import matplotlib.pyplot as plt
from typing import *
from os import PathLike

from .tools import *
from .math import Vector2, Vector3
import pandas as pd

import numpy as np
import enum


class GraphStyle(enum.Enum):
    DEFAULT = 'default'
    CLASSIC = 'classic'
    GRAYSCALE = 'grayscale'
    GGPLOT = 'ggplot'
    SEABORN = 'seaborn-v0_8'
    FAST = 'fast'
    BMH = 'bmh'
    SOLARIZED_LIGHT = 'Solarize_Light2'
    SEABORN_NOTEBOOK = 'seaborn-v0_8-notebook'


class ColorMap(enum.Enum):
    ACCENT = "Accent"
    BLUES = "Blues"
    BRBG = "BrBG"
    BUGN = "BuGN"
    BUPU = "BuPu"
    CMRMAP = "CMRmap"
    DARK2 = "Dark_2"
    GNBU = "GnBu"
    GRAYS = "Grays"
    GREENS = "Greens"
    GREYS = "Greys"
    ORRD = "OrRd"
    ORANGES = "Oranges"
    PRGN = "PRGn"
    PAIRED = "Paired"
    PASTEL1 = "Pastel1"
    PASTEL2 = "Pastel2"
    PIYG = "PiYG"
    PUBU = "PuBu"
    PUBUGN = "PuBuGn"
    PUOR = "PuOr"
    PURD = "PuRd"
    PURPLES = "Purples"
    RDBU = "RdBu"
    RDGY = "RdGy"
    RDPU = "RdPu"
    RDYLBU = "RdYlBu"
    RDYLGN = "RdYlGn"
    REDS = "Reds"
    SET1 = "Set1"
    SET2 = "Set2"
    SET3 = "Set3"
    SPECTRAL = "Spectral"
    WISTIA = "Wistia"
    YLGN = "YlGn"
    YLGNBU = "YlGnBu"
    YLORBT = "YlOrBt"
    YLORRD = "YlOrRd"
    AFMHOT = "afmhot"
    AUTUMN = "autumn"
    BINARY = "binary"
    BONE = "bone"
    BRG = "brg"
    BWR = "bwr"
    CIVIDIS = "cividis"
    COOL = "cool"
    COOLWARM = "coolwarm"
    COPPER = "copper"
    CUBEHELIX = "cubehelix"
    FLAG = "flag"
    GIST_EARTH = "gist_earth"
    GIST_GRAY = "gist_gray"
    GIST_HEAT = "gist_heat"
    GIST_NCAR = "gist_ncar"
    GIST_RAINBOW = "gist_rainbow"
    GIST_STERN = "gist_stern"
    GIST_YARG = "gist_yarg"
    GIST_YERG = "gist_yerg"
    GNUPLOT = "gnuplot"
    GNUPLOT2 = "gnuplot_2"
    GRAY = "gray"
    GREY = "grey"
    HOT = "hot"
    HSV = "hsv"
    INFERNO = "inferno"
    JET = "jet"
    MAGMA = "magma"
    NIPY_SPECTRAL = "nipy_spectral"
    OCEAN = "ocean"
    PINK = "pink"
    PLASMA = "plasma"
    PRISM = "prism"
    RAINBOW = "rainbow"
    SEISMIC = "seismic"
    SPRING = "spring"
    SUMMER = "summer"
    TAB10 = "tab_10"
    TAB20 = "tab_20"
    TAB20B = "tab_20_b"
    TAB20C = "tab_20_c"
    TERRAIN = "terrain"
    TRUBO = "trubo"
    TWILIGHT = "twilight"
    TWILIGHT_SHIFTED = "twilight_shifted"
    VIRIDIS = "viridis"
    WINTER = "winter"


class ColorFunction(enum.Enum):
    MAGNITUDE = lambda u, v, z: np.sqrt(u ** 2 + v ** 2)
    SUM = lambda u, v, z: abs(u) + abs(v)
    DIFFERENCE = lambda u, v, z: abs(u) - abs(v)
    PRODUCT = lambda u, v, z: u * v

    @staticmethod
    def LINEAR(axis: str = "x"):
        if axis == "x":
            return lambda u, v, z: u
        elif axis == "y":
            return lambda u, v, z: v
        elif axis == "z":
            return lambda u, v, z: z
        else:
            raise ValueError("Invalid Axis")

    @staticmethod
    def QUADRATIC(axis: str = "x"):
        if axis == "x":
            return lambda u, v, z: u * u
        elif axis == "y":
            return lambda u, v, z: v * v
        elif axis == "z":
            return lambda u, v, z: z * z
        else:
            raise ValueError("Invalid Axis")


class Graph2D:
    def __init__(self, name: str = "Graph 2D", style: GraphStyle = GraphStyle.DEFAULT):
        plt.style.use(style.value)
        self.fig = plt.figure(figsize=(16, 9))
        self.name = name
        self.subplots = 0

    def addAxes(self):
        self.ax = plt.subplot()
        self.ax.set_title(self.name)

    def addSubplot(self, row: int, col: int, title: str = None):
        if title is None:
            title = f"{self.subplots}"
        self.subplots += 1
        self.ax = self.fig.add_subplot(row, col, self.subplots)
        self.ax.set_title(title)

    def setTitle(self, title: str):
        self.ax.set_title(title)

    def setXlim(self, lim: tuple[float | int, float | int]):
        self.ax.set_xlim(lim)

    def setYlim(self, lim: tuple[float | int, float | int]):
        self.ax.set_ylim(lim)

    def setXLabel(self, label: str):
        self.ax.set_xlabel(label)

    def setYLabel(self, label: str):
        self.ax.set_ylabel(label)

    def save(self, name: str):
        self.fig.savefig(name)

    def plotPoint(self, point: Vector2, **kwargs):
        return self.ax.scatter(point.x, point.y, **kwargs)

    def plotPoints(self, *points: Vector2, **kwargs):
        return self.ax.scatter([i.x for i in points], [j.y for j in points], **kwargs)

    def drawLine(self, start: Vector2, end: Vector2, **kwargs):
        line = self.ax.plot([start.x, end.x], [start.y, end.y], **kwargs)
        return line

    def linePlot(self, xVals: Sequence, yVals: Sequence, **kwargs):
        if len(xVals) == len(yVals):
            return self.ax.plot(xVals, yVals, **kwargs)
        else:
            raise ValueError(f"Length of both arrays should be same. Lengths - X: {len(xVals)}, Y: {len(yVals)}")

    def scatterPlot(self, xVals: Sequence, yVals: Sequence, **kwargs):
        if len(xVals) == len(yVals):
            sctr = self.ax.scatter(xVals, yVals, **kwargs)
        else:
            raise ValueError(f"Length of both arrays should be same. Lengths - X: {len(xVals)}, Y: {len(yVals)}")
        return sctr

    def scatterPlotCF(self, xVals: Sequence, yVals: Sequence,
                      cfunction: Callable | ColorFunction = (lambda x, y, z: x + y), cmap: ColorMap = ColorMap.VIRIDIS,
                      colorBar: bool = False, **kwargs):
        c = [cfunction(item1, item2, 0) for item1, item2 in zip(xVals, yVals)]
        if len(xVals) == len(yVals):
            sctr = self.ax.scatter(xVals, yVals, cmap=cmap.value, c=c, **kwargs)
            if colorBar:
                plt.colorbar(sctr)
        else:
            raise ValueError(f"Length of both arrays should be same. Lengths - X: {len(xVals)}, Y: {len(yVals)}")

    def plotCSV(self, csvFilePath: Union[str, PathLike], xHeader: str, yHeader: str, color: str = 'blue',
                dots: bool = False, setAxisLabels: bool = True, label: str = None):
        data = pd.read_csv(csvFilePath)
        x = data[xHeader]
        y = data[yHeader]

        if setAxisLabels:
            self.setXLabel(xHeader)
            self.setXLabel(yHeader)

        if dots:
            self.ax.plot(x, y, color, marker="o")
        else:
            self.ax.plot(x, y, color)

    def annotate(self, text: str, xy: tuple[float, float]):
        self.ax.annotate(text, xy)

    @staticmethod
    def showGrid():
        plt.grid()

    @staticmethod
    def legend(*args, **kwargs):
        plt.legend(*args, **kwargs)

    @staticmethod
    def show():
        plt.show()


class Graph3D:
    def __init__(self, name: str = "Graph 3D", style: GraphStyle = GraphStyle.DEFAULT):
        self.fig = plt.figure()
        plt.style.use(style.value)
        self.name = name
        self.subplots = 0

    def addAxes(self):
        self.ax = self.fig.add_subplot(projection="3d")
        plt.title(self.name)

    def addSubplot(self, row: int, col: int, title: str = None):
        if title is None:
            title = f"{self.subplots}"
        self.subplots += 1
        self.ax = self.fig.add_subplot(row, col, self.subplots, projection='3d')
        self.ax.set_title(title)

    def setTitle(self, title: str):
        self.ax.set_title(title)

    def setXlim(self, lim: tuple[float | int, float | int]):
        self.ax.set_xlim(lim)

    def setYlim(self, lim: tuple[float | int, float | int]):
        self.ax.set_ylim(lim)

    def setZlim(self, lim: tuple[float | int, float | int]):
        self.ax.set_zlim(lim)

    def setXLabel(self, label: str):
        self.ax.set_xlabel(label)

    def setYLabel(self, label: str):
        self.ax.set_ylabel(label)

    def setZLabel(self, label: str):
        self.ax.set_zlabel(label)

    def save(self, name: str):
        self.fig.savefig(name)

    def point(self, point: Vector3, **kwargs):
        return self.ax.scatter3D(point.x, point.y, point.z, **kwargs)

    def points(self, *points: Vector3, **kwargs):
        return self.ax.scatter3D([i.x for i in points], [j.y for j in points], [k.z for k in points], **kwargs)

    def linePlot(self, xVals: Sequence, yVals: Sequence, zVals: Sequence, **kwargs):
        if len(xVals) == len(yVals) == len(zVals):
            return self.ax.plot(xVals, yVals, zVals, **kwargs)
        else:
            raise ValueError(
                f"Length of arrays should be same. Lengths - X: {len(xVals)}, Y: {len(yVals)}, Z: {len(zVals)}")

    def scatterPlot(self, xVals: Sequence, yVals: Sequence, zVals: Sequence, **kwargs):
        if len(xVals) == len(yVals) == len(zVals):
            sctr = self.ax.scatter3D(xVals, yVals, zVals, **kwargs)
        else:
            raise ValueError(
                f"Length of arrays should be same. Lengths - X: {len(xVals)}, Y: {len(yVals)}, Z: {len(zVals)}")
        return sctr

    def scatterPlotCF(self, xVals: Sequence, yVals: Sequence, zVals: Sequence,
                      cfunction: Callable | ColorFunction = (lambda x, y, z: x + y), cmap: ColorMap = ColorMap.VIRIDIS,
                      colorBar: bool = False, **kwargs):
        c = [cfunction(item1, item2, item3) for item1, item2, item3 in zip(xVals, yVals, zVals)]
        if len(xVals) == len(yVals):
            sctr = self.ax.scatter3D(xVals, yVals, zVals, cmap=cmap.value, c=c, **kwargs)
            if colorBar:
                self.fig.colorbar(sctr)
        else:
            raise ValueError(f"Length of both arrays should be same. Lengths - X: {len(xVals)}, Y: {len(yVals)}")
        return sctr

    def annotate(self, text: str, xy: tuple[float, float]):
        self.ax.annotate(text, xy)

    @staticmethod
    def showGrid():
        plt.grid()

    @staticmethod
    def legend(*args, **kwargs):
        plt.legend(*args, **kwargs)

    @staticmethod
    def show():
        plt.show()

    @staticmethod
    def imshow(*args, **kwargs):
        plt.imshow(*args, **kwargs)
