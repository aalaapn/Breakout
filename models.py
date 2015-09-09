# models.py
# Drew Samuels (drs354) and Aalaap Narasipura (agn27)
# December 7, 2014
#Two lines of code copied from A7 instructions on course website,
#http://www.cs.cornell.edu/Courses/cs1110/2014fa/assignments/assignment7/index.php
#Part of the specification for _brickRow copied from API
"""Models module for Breakout

This module contains the model classes for the Breakout game. Anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, both paddle
and individual bricks can just be instances of GRectangle.  There is no need for a
new class in the case of these objects.

We only need a new class when we have to add extra features to our objects.  That
is why we have classes for Ball and BrickWall.  Ball is usually a subclass of GEllipse,
but it needs extra methods for movement and bouncing.  Similarly, BrickWall needs
methods for accessing and removing individual bricks.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *


# PRIMARY RULE: Models are not allowed to access anything in any module other than
# constants.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Gameplay should pass it as a argument when it
# calls the method.


class BrickWall(object):
    """An instance represents the layer of bricks in the game.  When the wall is
    empty, the game is over and the player has won. This model class keeps track of
    all of the bricks in the game, allowing them to be added or removed.
    
    INSTANCE ATTRIBUTES:
        _bricks [list of GRectangle, can be empty]:
            This is the list of currently active bricks in the game.  When a brick
            is destroyed, it is removed from the list.
    
    As you can see, this attribute is hidden.  You may find that you want to access 
    a brick from class Gameplay. It is okay if you do that,  but you MAY NOT 
    ACCESS THE ATTRIBUTE DIRECTLY. You must use a getter and/or setter for any 
    attribute that you need to access in GameController.  Only add the getters and 
    setters that you need.
    
    We highly recommend a getter called getBrickAt(x,y).  This method returns the first
    brick it finds for which the point (x,y) is INSIDE the brick.  This is useful for
    collision detection (e.g. it is a helper for _getCollidingObject).
    
    You will probably want a draw method too.  Otherwise, you need getters in Gameplay
    to draw the individual bricks.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getBricks(self):
        """Returns: list of bricks in Brickwall
        
        Changes to the list will change the object"""
        return self._bricks
    
    
    # INITIALIZER TO LAYOUT BRICKS ON THE SCREEN
    def __init__(self):
        """Creates an instance of class BrickWall"""
        self._bricks = []
        y = GAME_HEIGHT - BRICK_Y_OFFSET
        color = colormodel.RED
        for i in range(BRICK_ROWS):
            color = self._brickColor(i)
            self._bricks = self._bricks + self._brickRow(color,y)
            y = y - BRICK_SEP_V - BRICK_HEIGHT
        
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def draw(self,view):
        """Draws all bricks in self to the view
        Invariant: view is an instance of class GView"""
        assert isinstance(view,GView), 'view must be an instance of GView'
        for brick in self._bricks:
            brick.draw(view)
        
    
    def _brickRow(self,color,y):
        """Returns: a row of bricks of color color and height y as a list
        
        Precondition: color 'must be a 4-element list of float between 0 and 1.
        If you assign it a RGB or HSV object from module colormodel, it will
        convert the color for your automatically.'
            Source: http://www.cs.cornell.edu/Courses/cs1110/2014fa/assignments/assignment7/api/gobject.html#gobject-label
        y must be a number (int or float) between 0 and GAME_HEIGHT"""
        assert (isinstance(color,list) and len(color)==4) or \
            isinstance(color,colormodel.RGB) or isinstance(color,colormodel.HSV) \
            , 'color must be a valid list, RGB, or HSV representation of color'
        assert isinstance(y,int) or isinstance(y,float), 'y must be a number'
        assert y>0 and y<GAME_HEIGHT, 'invalid height, y must be in the view'
        bricks = []
        x = BRICK_SEP_H/2
        for i in range(BRICKS_IN_ROW):
            bricks.append(GRectangle(x=x,y=y,width=BRICK_WIDTH,
            height=BRICK_HEIGHT,fillcolor=color, linecolor = color))
            x = x + BRICK_SEP_H + BRICK_WIDTH
        return bricks

    
    def _brickColor(self,n):
        """Returns: color of the bricks in row n
        
        Precondition: n is an int between 0 and BRICK_ROWS"""
        assert isinstance(n,int) and n>=0 and n<=BRICK_ROWS \
            , 'n must be an int between 0 and BRICK_ROWS'
        n = n % 10
        if n == 0 or n==1:
            return colormodel.RGB(22, 160, 133)
        elif n==2 or n==3:
            return colormodel.RGB(46, 204, 113)
        elif n==4 or n==5:
            return colormodel.RGB(241, 196, 15)
        elif n==6 or n==7:
            return colormodel.RGB(231, 76, 60)
        elif n==8 or n==9:
            return colormodel.RGB(155, 89, 182)
    


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Gameplay will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    In addition you must add the following methods in this class: an __init__
    method to set the starting velocity and a method to "move" the ball.  The
    __init__ method will need to use the __init__ from GEllipse as a helper.
    The move method should adjust the ball position according to  the velocity.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _atBottom [bool]: True if ball is at the bottom, False otherwise
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    def getVx(self):
        """Returns: x-velocity of the ball"""
        return self._vx
    
    def getVy(self):
        """Returns: y-velocity of the ball"""
        return self._vy
    
    
    def setVx(self,x):
        """Sets x-velocity to x
        
        Precondition: x must be a number (int or float)"""
        self._vx = x


    def setVy(self,y):
        """Sets y-velocity to y
        
        Precondition: y must be a number (int or float)"""
        self._vy = y
    
    
    def getBottom(self):
        """Returns: self._atBottom"""
        return self._atBottom
    
    # INITIALIZER TO SET RANDOM VELOCITY
    def __init__(self):
        """Creates a Ball object with _vy of -5.0 and random _vx."""
        GEllipse.__init__(self,center_x=GAME_WIDTH/2, center_y = GAME_HEIGHT/2,
                 width = BALL_DIAMETER, height = BALL_DIAMETER,
                 fillcolor = colormodel.RGB(189, 195, 199), linecolor = colormodel.RGB(236, 240, 241),)
        #code below copied from http://www.cs.cornell.edu/Courses/cs1110/2014fa/assignments/assignment7/index.php
        self._vx = random.uniform(1.0,5.0)
        self._vx = self._vx * random.choice([-1, 1])
        #end of code from course website
        self._vy = -3.0
        self.x = NUMBER_TURNS
        self._atBottom = False
    
    
    # METHODS TO MOVE AND/OR BOUNCE THE BALL
    def moveBall(self,state):
        """Changes ball position
        
        Increments x-coordinate of the Ball's by amount _vx and y-coordinate by
        amount _vy.  Changes velocity based on equal approach and recession
        angles when the ball hits the edge of the view."""
        if self.top >= GAME_HEIGHT:
            self._vy = -1*self._vy
        if self.bottom <= 0:
            self._atBottom = True
        if self.right >= GAME_WIDTH or self.left <= 0:
            self._vx = -1*self._vx
        self.center_x += self._vx
        self.center_y += self._vy
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE