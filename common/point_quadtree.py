import sys
from random import seed, randrange
 
# ==========================================================================
#		Recursive quadtree data structure
# ==========================================================================
 
def quadtree(points,topleft,botright):
    if len(points) > 1:
#        print >>sys.stderr,"splitting",len(points),topleft,botright
        mid = [(topleft[i]+botright[i])*0.5 for i in range(2)]
        svgLine((mid[0],topleft[1]),(mid[0],botright[1]))
        svgLine((topleft[0],mid[1]),(botright[0],mid[1]))
        quadtree([p for p in points if p[0]<mid[0] and p[1]<mid[1]],
                 topleft,mid)
        quadtree([p for p in points if p[0]<mid[0] and p[1]>=mid[1]],
                 (topleft[0],mid[1]),(mid[0],botright[1]))
        quadtree([p for p in points if p[0]>=mid[0] and p[1]<mid[1]],
                 (mid[0],topleft[1]),(botright[0],mid[1]))
        quadtree([p for p in points if p[0]>=mid[0] and p[1]>=mid[1]],
                 mid,botright)
 
 
# ==========================================================================
#		SVG output utility routines
# ==========================================================================
 
nestingLevel = None
 
def svgTag(s, deltaIndentation = 0):
	"""Send a single XML tag to the SVG file.
	First argument is the tag with all its attributes appended.
	Second arg is +1, -1, or 0 if tag is open, close, or both respectively.
	"""
 
	global nestingLevel
	if deltaIndentation < 0:
		nestingLevel -= 1
	if nestingLevel:
		sys.stdout.write('\t' * nestingLevel)
	sys.stdout.write('<')
	if deltaIndentation < 0:
		sys.stdout.write('/')
	sys.stdout.write(s)
	if not deltaIndentation:
		sys.stdout.write(' /')
	sys.stdout.write('>\n')
	if deltaIndentation > 0:
		nestingLevel += 1
 
 
def svgHeader(maxX, maxY):
	"""Start producing an SVG object.
	The output bounding box runs from (0,0) to (maxX,maxY).
	Must be followed by svg content and a call to svgTrailer().
	"""
	global nestingLevel
	if nestingLevel is None:
		sys.stdout.write('''<?xml version="1.0" encoding="iso-8859-1"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
 "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
''')
		nestingLevel = 0
	svgTag('svg xmlns="http://www.w3.org/2000/svg" version="1.1" '
		   'width="%dpt" height="%dpt" viewBox="0 0 %d %d"'
			% (maxX, maxY, maxX, maxY), 1)
 
def svgTrailer():
	"""End of SVG object."""
	svgTag('svg', -1)
 
def svgStyle(style):
	"""Start a group of svg items with the given style.
	Argument is a string in the form of a list of svg item attributes.
	Must be followed by svg content and a call to svgEndStyle().
	"""
	svgTag('g ' + style, 1)
 
def svgEdgeStyle(index):
	"""Look up edge style and call svgStyle with it."""
	svgStyle(globals()['edgeStyle' + str(index)])
 
def svgEndStyle():
	"""Finish group of styled svg items."""
	svgTag('g', -1)
 
def svgLine(start, end):
	"""Output line segment from start to end coordinates.
	Must be called within an svgStyle()/svgEndStyle() call pair.
	"""
	svgTag('line x1="%d" y1="%d" x2="%d" y2="%d"' % (start+end) )
 
def svgCircle(center, radius):
	"""Output circle with given center and radius coordinates.
	Must be called within an svgStyle()/svgEndStyle() call pair.
	"""
	svgTag('circle cx="%d" cy="%d" r="%s"' % (center+(radius,)) )
 
 
 
# ==========================================================================
#		Test code driver
# ==========================================================================
 
seed(27)
 
svgRadius = 2
svgBound = 400
margin = 4
 
def clusteredCoordinate(clusteringExponent,fractalExponent):
    x = long(randrange(1000)**clusteringExponent)
    y = 0
    p = 1
    while x:
        if x & 1:
            y += p
        p *= fractalExponent
        x >>= 1
    return y
 
def clusteredPoint():
    return clusteredCoordinate(2,2.5),clusteredCoordinate(1.5,3.2)
 
points = [clusteredPoint() for i in range(250)]
maxX = max(x for x,y in points)
maxY = max(y for x,y in points)

scaleX = 1.0*(svgBound-2*margin)/maxX
scaleY = 1.0*(svgBound-2*margin)/maxY

points = [(x*scaleX+margin,y*scaleY+margin) for x,y in points]
 
svgHeader(svgBound,svgBound)
 
svgStyle('fill="none" stroke="blue"')
svgLine((1,1),(1,svgBound-1))
svgLine((1,svgBound-1),(svgBound-1,svgBound-1))
svgLine((svgBound-1,svgBound-1),(svgBound-1,1))
svgLine((svgBound-1,1),(1,1))
quadtree(points,(1,1),(svgBound-1,svgBound-1))
svgEndStyle()
 
svgStyle('fill="white" stroke="black"')
for p in points:
    svgCircle(p,svgRadius)
svgEndStyle()
 
svgTrailer()