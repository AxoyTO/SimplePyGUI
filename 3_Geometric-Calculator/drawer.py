import matplotlib
from matplotlib.patches import Polygon, Rectangle as Rect
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
matplotlib.use('Qt5Agg')


class DrawFigures(FigureCanvasQTAgg):
    def __init__(self, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(DrawFigures, self).__init__(self.fig)


class DrawCircle(DrawFigures):
    def __init__(self, radius, perimeter):
        DrawFigures.__init__(self)
        theta = np.linspace(0, 2*np.pi, 100)
        a = radius*np.cos(theta)
        b = radius*np.sin(theta)
        rad1 = [0, 0]
        rad2 = [radius, 0]
        self.axes.plot(a, b, rad1, rad2)
        self.axes.set_title('Circle')
        self.axes.set_aspect(1)


class DrawRectangle(DrawFigures):
    def __init__(self, title, side_a, side_b):
        DrawFigures.__init__(self)
        self.axes.add_patch(Rect((0, 0), side_a, side_b, edgecolor='blue',
                                 facecolor='none', linewidth=2))

        if side_b > side_a:
            self.axes.plot(side_a*4, side_b*2)
        elif side_b < side_a:
            self.axes.plot(side_a*2, side_b*4)
        else:
            self.axes.plot(side_a*2, side_b*2)
        self.axes.set_title(title)


class DrawCube(DrawFigures):
    def __init__(self, side_a):
        DrawFigures.__init__(self)
        self.axes.remove()
        self.axes = [side_a]*3
        data = np.ones(self.axes, dtype=np.bool)
        alpha = 0.4
        colors = np.empty(self.axes + [4], dtype=np.float32)
        colors[:] = [0, 1, 1, alpha]
        self.axes = self.fig.add_subplot(111, projection='3d')
        self.axes.voxels(data, facecolors='cyan', alpha=.25)
        self.draw()


class DrawTriangle(DrawFigures):
    def __init__(self, side_a, height):
        DrawFigures.__init__(self)
        pts = np.array(
            [[-side_a/2, side_a/2], [0, height], [side_a/2, side_a/2]])
        p = Polygon(pts, closed=False)
        self.axes.add_patch(p)
        self.axes.plot(side_a/2, side_a/2)


class DrawPyramid(DrawFigures):
    def __init__(self, side_a, height):
        DrawFigures.__init__(self)
        self.axes.remove()

        self.axes = self.fig.add_subplot(111, projection='3d')

        v = np.array([[-side_a/2, -side_a/2, 0], [side_a/2, -side_a/2, 0],
                     [side_a/2, side_a/2, 0],  [-side_a/2, side_a/2, 0], [0, 0, height]])
        self.axes.scatter3D(v[:, 0], v[:, 1], v[:, 2])

        vertices = [[v[0], v[1], v[4]], [v[0], v[3], v[4]],
                    [v[2], v[1], v[4]], [v[2], v[3], v[4]], [v[0], v[1], v[2], v[3]]]

        self.axes.add_collection3d(
            Poly3DCollection(
                vertices,
                facecolors='cyan',
                linewidths=1,
                edgecolors='black',
                alpha=.25
            )
        )

        self.draw()


class DrawSphere(DrawFigures):
    def __init__(self, radius):
        DrawFigures.__init__(self)
        self.axes.remove()
        self.axes = self.fig.add_subplot(111, projection='3d')

        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = radius * np.outer(np.cos(u), np.sin(v))
        y = radius * np.outer(np.sin(u), np.sin(v))
        z = radius * np.outer(np.ones(np.size(u)), np.cos(v))

        self.axes.plot_surface(x, y, z, color='cyan')

        plt.show()


class DrawTrapezoid(DrawFigures):
    def __init__(self, side_a, side_b, height):
        DrawFigures.__init__(self)
        x = [-side_a/2, side_a/2, side_b/2, -side_b/2]
        y = [-height/2, -height/2, height/2, height/2]
        self.axes.plot(side_a, height)
        self.axes.add_patch(Polygon(xy=list(zip(x, y)), fill=False))


class DrawRhombus(DrawFigures):
    def __init__(self, diagonal_p, diagonal_q):
        DrawFigures.__init__(self)
        x = [0, -diagonal_q/2, 0, diagonal_q/2]
        y = [-diagonal_p/2, 0, diagonal_p/2, 0]
        self.axes.plot(diagonal_p, diagonal_q)
        self.axes.add_patch(Polygon(xy=list(zip(x, y)), fill=False))


class DrawParallelepiped(DrawFigures):
    def __init__(self, side_a, side_b, side_c):
        DrawFigures.__init__(self)
        self.axes.remove()

        points = np.array([[-side_a/2, -side_b/2, -side_c/2],
                           [side_a/2, -side_b/2, -side_c/2],
                           [side_a/2, side_b/2, -side_c/2],
                           [-side_a/2, side_b/2, -side_c/2],
                           [-side_a/2, -side_b/2, side_c/2],
                           [side_a/2, -side_b/2, side_c/2],
                           [side_a/2, side_b/2, side_c/2],
                           [-side_a/2, side_b/2, side_c/2]])

        P = [[2.06498904e-01, -6.30755443e-07,  1.07477548e-03],
             [1.61535574e-06,  1.18897198e-01,  7.85307721e-06],
             [7.08353661e-02,  4.48415767e-06,  2.05395893e-01]]

        Z = np.zeros((8, 3))
        for i in range(8):
            Z[i, :] = np.dot(points[i, :], P)
        Z = 10.0*Z

        self.axes = self.fig.add_subplot(111, projection='3d')

        r = [-1, 1]

        X, Y = np.meshgrid(r, r)

        self.axes.scatter3D(Z[:, 0], Z[:, 1], Z[:, 2])

        vertices = [[Z[0], Z[1], Z[2], Z[3]],
                    [Z[4], Z[5], Z[6], Z[7]],
                    [Z[0], Z[1], Z[5], Z[4]],
                    [Z[2], Z[3], Z[7], Z[6]],
                    [Z[1], Z[2], Z[6], Z[5]],
                    [Z[4], Z[7], Z[3], Z[0]]]

        self.axes.add_collection3d(
            Poly3DCollection(
                vertices,
                facecolors='cyan',
                linewidths=1,
                edgecolors='black',
                alpha=.25
            )
        )

        self.draw()


class DrawCylinder(DrawFigures):
    def __init__(self, radius, height):
        DrawFigures.__init__(self)
        self.axes.remove()
        self.axes = self.fig.add_subplot(111, projection='3d')

        z = np.linspace(0, height, 50)
        theta = np.linspace(0, 2*np.pi, 50)
        theta_grid, z_grid = np.meshgrid(theta, z)
        x_grid = radius*np.cos(theta_grid) + 0.2
        y_grid = radius*np.sin(theta_grid) + 0.2
        Xc, Yc, Zc = x_grid, y_grid, z_grid
        self.axes.plot_surface(Xc, Yc, Zc, alpha=.4)

        self.draw()


class DrawCone(DrawFigures):
    def __init__(self, radius, height):
        DrawFigures.__init__(self)

        self.axes.remove()
        self.axes = self.fig.add_subplot(111, projection='3d')

        z = np.arange(0, height, 0.01)
        theta = np.arange(0, radius * np.pi + np.pi / 50, np.pi / 50)

        for z_value in z:
            x = z_value * np.array([np.cos(q) for q in theta])
            y = z_value * np.array([np.sin(q) for q in theta])
            self.axes.plot(x, y, -z_value, 'c', alpha=.4)

        self.draw()
