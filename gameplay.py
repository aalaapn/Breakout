# gameplay.py
# Drew Samuels (drs354) and Aalaap Narasipura (agn27)
# December 7, 2014
#Header for _getCollidingObject copied from course website
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Gameplay represent a single game.  If you want to restart a new game,
you are expected to make a new instance of Gameplay.

The subcontroller Gameplay manages the paddle, ball, and bricks.  These are model
objects.  The ball and the bricks are represented by classes stored in models.py.
The paddle does not need a new class (unless you want one), as it is an instance
of GRectangle provided by game2d.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Gameplay can only access attributes in models.py via getters/setters
# Gameplay is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Gameplay(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It
    animates the ball, removing any bricks as necessary.  When the game is
    won, it stops animating.  You should create a NEW instance of 
    Gameplay (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.
    
    INSTANCE ATTRIBUTES:
        _wall   [BrickWall]:  the bricks still remaining 
        _paddle [GRectangle]: the paddle to play with 
        _ball [Ball, or None if waiting for a serve]: 
            the ball to animate
        _last [GPoint, or None if mouse button is not pressed]:  
            last mouse position (if Button pressed)
        _tries  [int >= 0]:   the number of tries left
        _lastTouch
    
    As you can see, all of these attributes are hidden.  You may find that you
    want to access an attribute in call Breakout. It is okay if you do, but
    you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter and/or
    setter for any attribute that you need to access in Breakout.  Only add
    the getters and setters that you need for Breakout.
    
    You may change any of the attributes above as you see fit. For example, you
    might want to make a Paddle class for your paddle.  If you make changes,
    please change the invariants above.  Also, if you add more attributes,
    put them and their invariants below.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _bounceSound [pygame.mixer.Sound]
            sound to play when ball hits paddle
    _brickSounds [list ofpygame.mixer.Sound]
            sounds to play when ball hits a brick
    _soundState [bool]
            Determines whether sounds are on (True) or off (False)
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getBallBottom(self):
        """Returns True if self._ball is at or below the bottom of the view
        
        Returns False otherwise"""
        return self._ball.getBottom()
    
    
    def getNumberBricks(self):
        """Returns the number of bricks in self._wall"""
        wall = self._wall.getBricks()
        return len(wall)
    

    def getSoundState(self):
        """Returns True if sounds are on and False if sounds are off"""
        return self._soundState
    
    
    def setSoundState(self, state):
        """Sets the soundState to state to turn sounds off or on
        
        Precondition: state must be a bool"""
        assert isinstance(state,bool), 'state must be a boolean'
        self._soundState = state

    
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):
        """Creates an instance of the class Gameplay"""
        self._wall = BrickWall()
        self._paddle = GRectangle(x= GAME_WIDTH/2,y=PADDLE_OFFSET,
        width=PADDLE_WIDTH,height=PADDLE_HEIGHT,fillcolor=colormodel.RGB(236, 240, 241))
        self._last = None
        self._ball = None
        self._bounceSound = Sound('bounce.wav')
        self._brickSounds = [Sound('saucer1.wav'),Sound('saucer2.wav'),
                    Sound('cup1.wav'),Sound('plate1.wav'),Sound('plate2.wav')]
        self._soundState = True

    
    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def draw(self,view):
        """Draws all objects in self to the view.
        
        Precondition: view is an instance of class GView."""
        assert isinstance(view,GView), 'view must be an instance of GView'
        self._wall.draw(view)
        self._paddle.draw(view)
        if self._ball != None :
            self._ball.draw(view)

    
    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    def updatePaddle(self, touch):
        """Updates position of paddle based on touch
        
        In response to a user clicking and dragging across the screen, changes
        the x position of the paddle so that the distance along the x-axis
        between the paddle and the touch does not change unless the paddle
        reaches the edge of the view.
        Ensures the paddle remains completely on the view.
        Precondition: touch is an instance of GPoint or is None and is an
            attribute of a GView object"""
        assert isinstance(touch,GPoint) or touch==None, 'touch must be a GPoint\
        or None'
        if touch != None and self._last != None:
            dist = touch.x - self._last.x
            self._paddle.center_x += dist
        if self._paddle.x + PADDLE_WIDTH >= GAME_WIDTH:
            self._paddle.x = GAME_WIDTH - PADDLE_WIDTH
        if self._paddle.x < 0:
            self._paddle.x = 0
        self._last = touch
    
    
    def serveBall(self):
        """Creates a ball object in the center of the view
        
        Ball moves downward in a random x direction"""
        self._ball = Ball()
    
    
    def updateBall(self,state):
        """Changes position of ball based on velocity and contact with other objects"""
        self._ball.moveBall(state)
        if self._getCollidingObject() == self._paddle and self._ball.getVy()<0:
            self._ball.setVy(-1*(self._ball.getVy()))
            if self._soundState:
                self._bounceSound.play() 
        if self._getCollidingObject() in self._wall.getBricks():
            self._ball.setVy(-1*(self._ball.getVy()))
            self._wall.getBricks().remove(self._getCollidingObject())
            if self._soundState:
                index = random.randint(0,len(self._brickSounds)-1)
                self._brickSounds[index].play()
        if self.getNumberBricks() < BRICKS_IN_ROW*BRICK_ROWS*.9:
            if self._ball.getVy() <0:
                self._ball.setVy(-5)
            if self._ball.getVy() >0:
                self._ball.setVy(5)
        if self.getNumberBricks() < BRICKS_IN_ROW*BRICK_ROWS*.7:
            if self._ball.getVy() <0:
                self._ball.setVy(-7)
            if self._ball.getVy() >0:
                self._ball.setVy(7)
        if self.getNumberBricks() < BRICKS_IN_ROW*BRICK_ROWS*.5:
            if self._ball.getVy() <0:
                self._ball.setVy(-9)
            if self._ball.getVy() >0:
                self._ball.setVy(9)
        if self.getNumberBricks() < BRICKS_IN_ROW*BRICK_ROWS*.3:
            if self._ball.getVy() <0:
                self._ball.setVy(-11)
            if self._ball.getVy() >0:
                self._ball.setVy(11)
        if self.getNumberBricks() < BRICKS_IN_ROW*BRICK_ROWS*.1:
            if self._ball.getVy() <0:
                self._ball.setVy(-13)
            if self._ball.getVy() >0:
                self._ball.setVy(13)


    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    
    #Header and specification copied from course website,
    #http://www.cs.cornell.edu/Courses/cs1110/2014fa/assignments/assignment7/index.php
    def _getCollidingObject(self):
        """Returns: GObject that has collided with the ball
        
        This method checks the four corners of the ball, one at a 
        time. If one of these points collides with either the paddle 
        or a brick, it stops the checking immediately and returns the 
        object involved in the collision. If no collision occured, returns None"""
        #End copied code
        #Check lower left corner
        x = self._ball.x
        y = self._ball.y
        collision = self._getCollision(x,y)
        if collision != None:
            return collision
        #Check upper left corner
        y = self._ball.top
        collision = self._getCollision(x,y)
        if collision != None:
            return collision
        #Check upper right corner
        x = self._ball.right
        collision = self._getCollision(x,y)
        if collision != None:
            return collision
        #Check lower right corner
        y = self._ball.y
        collision = self._getCollision(x,y)
        if collision != None:
            return collision
        return None
    
    
    def _getCollision(self,x,y):
        """Returns: GObject (not including the ball) at position (x,y)
        
        Returns None if there is no GObject at this position
        Precondition: x an y are floats"""
        assert isinstance(x,float) and isinstance(y,float), \
            'x and y must be floats'
        for i in self._wall.getBricks():
            if i.contains(x,y):
                return i
        if self._paddle.contains(x,y):
            return self._paddle
        return None
    
    
    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE
    
    
    def deleteBall(self):
        """Resets the object _ball to None"""
        self._ball = None
    
