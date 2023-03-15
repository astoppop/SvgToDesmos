from svg.path import parse_path
from svg.path.path import Line, CubicBezier
from xml.dom import minidom
import clipboard

# read the SVG file
doc = minidom.parse('./igloo.svg')
path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
doc.unlink()

equations = []
flip = True

def appendLine(x0, y0, x1, y1):
    if (x1 - x0) == 0:
        # equations.append(f'x = {x0} \left\{{{min(y0, y1)} < y < {max(y0, y1)}\\right\}}')
        equations.append(f'r = {x0}\\csc\\theta \left\{{{min(y0, y1)} < y < {max(y0, y1)}\\right\}}')
        return
    m = (y1 - y0) / (x1 - x0)
    b = y1 - (x1 * m)
    if flip:
        m *= -1
        b *= -1

    # equations.append(f'y = {m}x + {b} \left\{{{min(x0, x1)} < x < {max(x0, x1)}\\right\}}')
    #  r sin(q) = m r cos q + b 
    equations.append(f'r \\sin\\theta = {m}r \\cos\\theta + {b} \left\{{{min(x0, x1)} < r \\cos\\theta < {max(x0, x1)}\\right\}}')

def p(t, a, b, c, d):
    return (pow(1 - t, 3) * a) + (3 * pow(1 - t, 2) * t * b) + (3 * (1 - t) * pow(t, 2) * c) + (pow(t, 3) * d)

# print the line draw commands
for path_string in path_strings:
    path = parse_path(path_string)
    for e in path:
        if isinstance(e, Line):
            x0, y0 = e.start.real, e.start.imag
            x1, y1 = e.end.real, e.end.imag
            # print("(%.2f, %.2f) - (%.2f, %.2f)" % (x0, y0, x1, y1))
            appendLine(x0, y0, x1, y1)
        elif isinstance(e, CubicBezier):
            x0, y0 = e.start.real, e.start.imag
            x1, y1 = e.control1.real, e.control1.imag
            x2, y2 = e.control2.real, e.control2.imag
            x3, y3 = e.end.real, e.end.imag

            pastX, pastY = x0, y0
            for i in range(1, 4):
                t = i / 3
                newX, newY = p(t, x0, x1, x2, x3), p(t, y0, y1, y2, y3)
                appendLine(pastX, pastY, newX, newY)
                pastX, pastY = newX, newY
        # else: print(e)

# print('\n'.join(equations))
# clipboard.copy('\n'.join(equations))

f = open("text.txt", "w")
f.writelines('\n'.join(equations))
f.close()