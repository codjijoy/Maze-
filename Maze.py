# Maze.py
# Yejin Hwang & Codi Elliott
# Lab8: User walks through a maze.
# Maze code provided by JORourke

from random import shuffle, randrange
from graphics import *
win = GraphWin( 'Maze', 500, 500 )


#================================================================
def MakeStringMaze(w = 12, h = 8):
    ''' https://rosettacode.org/wiki/Maze_generation#Python
        (Author unknown, but based on
        https://en.wikipedia.org/wiki/Maze_generation_algorithm.)
        Default w,h=12,8. Returns a string.
    '''
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+--"] * w + ['+'] for _ in range(h + 1)]
 
    def walk(x, y):
        vis[y][x] = 1
 
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "+  "
            if yy == y: ver[y][max(x, xx)] = "   "
            walk(xx, yy)
 
    walk(randrange(w), randrange(h))

    # Create a string representation of the maze:
    s = ''
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    return s

def DrawMaze( s, win, w ):
    '''Convert string-maze s to graphics-maze.
       Assumes default w,h=12,8, and win coords +/-100.
       Author: JORourke
    '''
    # Break up s into rows:
    slist = s.split( '\n' )

    dx,dy = 5,10 # Mimic char aspect ratio, about 1::2
    Lgobjs=[] # List of graphics objects
    # i : controls x coord
    # j : controls y coord
    for j in range( len( slist ) ):
        row = slist[j]
        y = -j * dy + w - 2*dy
        for i in range( len(row) ):
            x = i * dx - w + 2*dx
            c = row[i] # c: single character
            if c=='|':
                Lgobjs.append( Line(Point(x,y+dy),Point(x,y-dy)) )
            elif c=='-':
                Lgobjs.append( Line(Point(x-dx,y),Point(x+dx,y)) )

    # Now draw all the graphic objects                              
    for gobj in Lgobjs:
        gobj.setWidth( 2 )
        gobj.setFill( 'LightGreen' )
        gobj.draw( win )

    # Begin & End circs
    def BeginEnd( x, y ):
        print( 'Corner:', x, y)
        p = Point( x, y )
        circ = Circle( p, dx )
        circ.setFill( 'Pink' )
        circ.draw( win )

    BeginEnd( x, y+2*dy )
    BeginEnd( -w + dy, w - 2*dy )
#================================================================
def Moving(token, direction):
    '''Move token in the direction it went and call DrawPath'''
    # Extract the circle data:
    pcent = token.getCenter( )
    xc,yc = pcent.getX(), pcent.getY()

    # Compute displacement based on direction
    diff = 10
    if direction == 'Right':
        dx = diff
        dy = 0
    if direction == 'Left':
        dx = -diff
        dy = 0
    if direction == 'Up':
        dx = 0
        dy = diff
    if direction == 'Down':
        dx = 0
        dy = -diff
    token.move( dx, dy )
    DrawPath(token, dx, dy)
    return Point(xc+dx, yc+dy)
    
    
def DrawPath(token, dx, dy):
    '''Trace path token went by drawing line'''
    pcent = token.getCenter( )
    xc,yc = pcent.getX(), pcent.getY()
    oldx = xc-dx
    oldy = yc-dy
    nPoint = Point(xc,yc)
    oPoint = Point(oldx, oldy)

    path = Line(nPoint, oPoint)
    path.draw(win)
    
def PtInCirc( p, circ ):
    '''Is point p in the circle?
    '''
    # Extract the pt coords:
    xp,yp = p.getX(),p.getY()

    # Extract the circle data:
    pcent = circ.getCenter( )
    xc,yc = pcent.getX(), pcent.getY()
    r = circ.getRadius( )

    # Avoid sqrts by working with squares:
    r2 = r**2 
    d2 = (xc-xp)**2 + (yc-yp)**2
    #print( r2, '::', d2 )
    
    if d2 <= r2:
        return True
    else:
        return False


def main( ):
    '''Maze Game: move token to win'''
    win.setBackground( 'DarkGreen' )
    w = 100
    win.setCoords( -w, -w, w, w)

    # Create a maze as a string:
    s = MakeStringMaze( )
    print( s )
    # Convert string maze to graphics maze:
    DrawMaze( s, win, w )


    #Create Token
    p1 = Point(90,-80)
    r = 5
    token = Circle(p1, r)
    token.setFill('#508658')
    token.draw(win)

    #Create End
    p2 = Point(-90,80)
    r2 = 8
    end = Circle(p2, r2)
    end.setFill('#EEC718')
    end.draw(win)

    #Create congrats message
    message = Text(Point(0,4), "You Won!\nClick to close window.")
    box = Rectangle(Point(-25,-5), Point(25,15))
    box.setFill('Light Pink')
    #-----------------------------------------------------------
    newCenterPoint = Point(10000,-10000)
    win.getMouse()
    print('Now: checkKey () [focus in window]...')
    while True:
        k = win.checkKey()
        if k== 'period': break
        if PtInCirc(newCenterPoint, end):
            print('Congrats')
            box.draw(win)
            message.draw(win)
            break
        if (k != ''):
            print( 'Key=', k)
            newCenterPoint = Moving(token, k)            
    #-----------------------------------------------------------
        
    print( 'Click in window to close' )
    win.getMouse( )
    win.close( )

main( )

