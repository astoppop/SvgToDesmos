from svg.path import parse_path
from svg.path.path import Line, CubicBezier
from xml.dom import minidom

# read the SVG file
doc = minidom.parse('./boat.svg')
path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
doc.unlink()

equations = []

def appendLine(x0, y0, x1, y1):
    if (x1 - x0) == 0:
        equations.append(f'x = {x0} \left\{{{min(y0, y1)} < y < {max(y0, y1)}\\right\}}')
        return
    m = (y1 - y0) / (x1 - x0)
    b = y1 - (x1 * m)

    # equations.append(f'y = {m}x + {b} \left\{{{min(x0, x1)} < x < {max(x0, x1)}\\right\}}')
    #  r sin(q) = m r cos q + b 
    equations.append(f'r \\sin\\theta = {m}r \\cos\\theta + {b} \left\{{{min(x0, x1)} < r \\cos\\theta < {max(x0, x1)}\\right\}}')

def p(t, a, b, c, d):
    return (pow(1 - t, 3) * a) + (3 * pow(1 - t, 2) * t * b) + (3 * (1 - t) * pow(t, 2) * c) + (pow(t, 3) * d)

# print the line draw commands
for path_string in path_strings:
    path = parse_path(path_string)
    for e in path:
        print(e)
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
            print(e)

            pastX, pastY = x0, y0
            for i in range(0, 5):
                t = i / 5
                newX, newY = p(t, x0, x1, x2, x3), p(t, y0, y1, y2, y3)
                appendLine(pastX, pastY, newX, newY)
                pastX, pastY = newX, newY

print('\n'.join(equations))