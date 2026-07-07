import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

points = [(1, 0), (2, 1), (3, 0), (2, -1)]
x_values = [p[0] for p in points]
y_values = [p[1] for p in points]
_, axes = plt.subplots()
axes.scatter(x_values, y_values)
rhombus = Polygon(points, closed=True, fill=False, edgecolor='red')
axes.add_patch(rhombus)
plt.show()