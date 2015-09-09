# breakout.py
# Drew Samuels (drs354), Aalaap Narasipura (agn27)
# December 7, 2014
"""Primary module for Breakout application

This module contains the App controller class for the Breakout application.
There should not be any need for additional classes in this module.
If you need more classes, 99% of the time they belong in either the gameplay
module or the models module. If you are ensure about where a new class should go, 
post a question on Piazza."""
from constants import *
from gameplay import *
from game2d import *


# PRIMARY RULE: Breakout can only access attributes in gameplay.py via getters/setters
# Breakout is NOT allowed to access anything in models.py

class Breakout(GameApp):
    """Instance is a Breakout App
    
    This class extends GameApp and implements the various methods necessary 
    for processing the player inputs and starting/running a game.
    
        Method init starts up the game.
        
        Method update either changes the state or updates the Gameplay object
        
        Method draw displays the Gameplay object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the init method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Gameplay.
    Gameplay should have a minimum of two methods: updatePaddle(touch) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView, it is inherited from GameApp]:
            the game view, used in drawing (see examples from class)
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE]:
            the current state of the game represented a value from constants.py
        _last   [GPoint, or None if mouse button is not pressed]:
            the last mouse position (if Button was pressed)
        _game   [Gameplay, or None if there is no game currently active]: 
            the game controller, which manages the paddle, ball, and bricks
    
    ADDITIONAL INVARIANTS: Attribute _game is only None if _state is STATE_INACTIVE.
    
    You may have more attributes if you wish (you might need an attribute to store
    any text messages you display on the screen). If you add new attributes, they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _message [Glabel if state is STATE_INACTIVE, None otherwise]
            Message to display before the game starts
    _countdownframes [int]
            Accumulator variable for countdown
    _pausedframes [int]
            Accumulator variable for paused state
    _countdownmessage [GLabel]
            Message to display during countdown
    _endgamemessage [GLabel]
            Message to display in the event of a loss
    _pausemessage [GLabel]
            Message to display at state paused
    _completemessage [GLabel]
            Message to display when the game is won
    _turns [int]
            The number of turns left.
    _score [GLabel]
            Message to display the score, which is
            the number of bricks destroyed
    _soundmessage [GLabel]
            Message to tell whether sounds are off or on
    """
    
    
    # DO NOT MAKE A NEW INITIALIZER!
                                                                                        
    # GAMEAPP METHODS
    def init(self):
        """Initialize the game state.
        
        This method is distinct from the built-in initializer __init__.
        This method is called once the game is running. You should use
        it to initialize any game specific attributes.
        
        This method should initialize any state attributes as necessary 
        to statisfy invariants. When done, set the _state to STATE_INACTIVE
        and create a message (in attribute _message) saying that the user should 
        press to play a game.""" 
        self._state = STATE_INACTIVE
        self._last = None
        self._game = None
        self._countdownframes = 0
        self._pausedframes = 0
        self._turns = NUMBER_TURNS
        #messages
        self._countdownmessage = None

        self._score = GLabel(x=(GAME_WIDTH/2),y=(GAME_HEIGHT-20),
        right=GAME_WIDTH,top=GAME_HEIGHT,text='Score:'+ str(0),
        font_size=27, halign='center',valign='middle',font_name='Fix.ttf')

        self._message = GLabel(x=(GAME_WIDTH/2),y=(GAME_HEIGHT/2),
        right=GAME_WIDTH,top=GAME_HEIGHT,text='Click to Play!',font_size=40,
        halign='center',valign='middle',font_name='Fix.ttf')
        
        self._endgamemessage = GLabel(x=(GAME_WIDTH/2),y=(GAME_HEIGHT/2),
        right=GAME_WIDTH,top=GAME_HEIGHT,text='Game Over! \nClick to Replay',
        font_size=40,halign='center',valign='middle',font_name='Fix.ttf')
        
        self._completemessage = GLabel(x=(GAME_WIDTH/2),y=(GAME_HEIGHT/2),
        right=GAME_WIDTH,top=GAME_HEIGHT,text='You win! \nClick to Replay',
        font_size=40,halign='center',valign='middle',font_name='Fix.ttf')
        
        self._soundmessage = GLabel(x=(GAME_WIDTH),y=(GAME_HEIGHT),
        right=GAME_WIDTH,top=GAME_HEIGHT,text='Sounds: On',
        font_size=15,halign='right',valign='top',font_name='Fix.ttf')


    def update(self,dt):
        """Animate a single frame in the game.
        
        It is the method that does most of the work. Of course, it should
        rely on helper methods in order to keep the method short and easy
        to read.  Some of the helper methods belong in this class, but most
        of the others belong in class Gameplay.
        
        The first thing this method should do is to check the state of the
        game. We recommend that you have a helper method for every single
        state: STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE.
        The game does different things in each state.
        
        In STATE_INACTIVE, the method checks to see if the player clicks
        the mouse (_last is None, but view.touch is not None). If so, it 
        (re)starts the game and switches to STATE_COUNTDOWN.
        
        STATE_PAUSED is similar to STATE_INACTIVE. However, instead of 
        restarting the game, it simply switches to STATE_COUNTDOWN.
        
        In STATE_COUNTDOWN, the game counts down until the ball is served.
        The player is allowed to move the paddle, but there is no ball.
        Paddle movement should be handled by class Gameplay (NOT in this class).
        This state should delay at least one second.
        
        In STATE_ACTIVE, the game plays normally.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Gameplay (NOT in this class).
        Gameplay should have methods named updatePaddle and updateBall.
        
        While in STATE_ACTIVE, if the ball goes off the screen and there
        are tries left, it switches to STATE_PAUSED.  If the ball is lost 
        with no tries left, or there are no bricks left on the screen, the
        game is over and it switches to STATE_INACTIVE.  All of these checks
        should be in Gameplay, NOT in this class.
        
        You are allowed to add more states if you wish. Should you do so,
        you should describe them here.
        
        Precondition: dt is the time since last update (a float).  This
        parameter can be safely ignored. It is only relevant for debugging
        if your game is running really slowly. If dt > 0.5, you have a 
        framerate problem because you are trying to do something too complex."""
        if self._state == STATE_INACTIVE:
            self._inactive()
        if self._state == STATE_COUNTDOWN:
            self._countdown()
        if self._state == STATE_ACTIVE:
            self._active()
        if self._state == STATE_PAUSED:
            self._paused()
        if self._state == STATE_END_GAME:
            self._endgame()
        if self._state == STATE_COMPLETE:
            self._endgame()
        self._last = self.view.touch

    
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject. 
        To draw a GObject g, simply use the method g.draw(view).  It is 
        that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are
        attributes in Gameplay. In order to draw them, you either need to
        add getters for these attributes or you need to add a draw method
        to class Gameplay.  We suggest the latter.  See the example 
        subcontroller.py from class."""
        #below is the backgrond color
        GRectangle(x=0,y=0,width=GAME_WIDTH,
        height=GAME_HEIGHT,fillcolor=colormodel.RGB(52, 73, 94), 
        linecolor = colormodel.RGB(52, 73, 94)).draw(self.view)
        #end background color code
        if self._state == STATE_INACTIVE:
            self._message.draw(self.view)
        if self._state == STATE_COUNTDOWN and self._countdownmessage != None:
            self._countdownmessage.draw(self.view)
            self._game.draw(self.view)
            self._score.draw(self.view)
            self._soundmessage.draw(self.view)
        if self._state == STATE_ACTIVE:
            self._game.draw(self.view)
            self._score.draw(self.view)
            self._soundmessage.draw(self.view)
        if self._state == STATE_PAUSED:
            self._pausemessage.draw(self.view)
            self._score.draw(self.view)
        if self._state == STATE_END_GAME:
            self._score.draw(self.view)
            self._endgamemessage.draw(self.view)
        if self._state == STATE_COMPLETE:
            self._completemessage.draw(self.view)


    # HELPER METHODS FOR THE STATES GO HERE
    
    
    def _inactive(self):
        """Changes _state from STATE_INACTIVE to STATE_COUNTDOWN
        in response to a click by the user
        
        Dismisses the welcome screen when the player clicks the mouse
        or touches the screen. Sets _message to None and loads _game """
        
        if isinstance(self.view.touch,GPoint) and self._last == None:
            self._state = STATE_COUNTDOWN
            self._message = None
            self._game = Gameplay()
    
    
    def _countdown(self):
        """Used to update game during STATE_COUNTDOWN
        
        Ensures paddle can move with input from user
        Dispalys a sequence counting down from 3
        Changes state to STATE_ACTIVE and serves ball at end of countdown"""
        self._game.updatePaddle(self.view.touch)
        self._score = GLabel(x=(GAME_WIDTH/2),y=(GAME_HEIGHT-20),
        right=GAME_WIDTH,top=GAME_HEIGHT,text='Score:'+ str(100-self._game.getNumberBricks()),
        font_size=27, halign='center',valign='middle',font_name='Fix.ttf')
        if isinstance(self.view.touch,GPoint) and self._last == None:
            self._soundControl()
        if self._countdownframes < FPS:
            self._countdownmessage = GLabel(text='3',
                font_size=50,halign='center',valign='middle',
                x=GAME_WIDTH/2,y=GAME_HEIGHT/2, font_name='Fix.ttf')
        elif self._countdownframes < 2*FPS:
            self._countdownmessage = GLabel(text='2',
                        font_size=50,halign='center',valign='middle',
                        x=GAME_WIDTH/2,y=GAME_HEIGHT/2, font_name='Fix.ttf')
        elif self._countdownframes < 3*FPS:
            self._countdownmessage = GLabel(text='1',
                        font_size=50,halign='center',valign='middle',
                        x=GAME_WIDTH/2,y=GAME_HEIGHT/2, font_name='Fix.ttf')
        elif self._countdownframes < 4*FPS:
            self._countdownmessage = GLabel(text='Go!',
                        font_size=50,halign='center',valign='middle',
                        x=GAME_WIDTH/2,y=GAME_HEIGHT/2, font_name='Fix.ttf')
        else:
            self._countdownmessage = None
            self._state = STATE_ACTIVE
            self._game.serveBall()
        self._countdownframes += 1


    def _paused(self):
        """Used to update game during STATE_PAUSED"""
        self._score = GLabel(x=(GAME_WIDTH/2),y=(GAME_HEIGHT-20),
        right=GAME_WIDTH,top=GAME_HEIGHT,text='Score:'+ str(100-self._game.getNumberBricks()),
        font_size=27, halign='center',valign='middle',font_name='Fix.ttf')
        self._pausemessage = GLabel(x=(GAME_WIDTH/2),y=(GAME_HEIGHT/2),
        right=GAME_WIDTH,top=GAME_HEIGHT,text='lives left: ' + str(self._turns),font_size=40,
        halign='center',valign='middle',font_name='Fix.ttf')
        if self._turns == 0:
            self._state = STATE_END_GAME
        self._countdownframes = 0
        if self._pausedframes == 2*FPS:
            self._state = STATE_COUNTDOWN
        self._pausedframes += 1
    
    
    def _active(self):
        """Used to update game during STATE_ACTIVE
        
        Ensures paddle responds to user input and updates the position of the
        ball"""
        self._score = GLabel(x=(GAME_WIDTH/2),y=(GAME_HEIGHT-20),
        right=GAME_WIDTH,top=GAME_HEIGHT,text='Score:'+ str(100-self._game.getNumberBricks()),
        font_size=27, halign='center',valign='middle',font_name='Fix.ttf')
        if isinstance(self.view.touch,GPoint) and self._last == None:
            self._soundControl()
        self._game.updateBall(self._state)
        self._game.updatePaddle(self.view.touch)
        if self._game.getBallBottom():
            self._pausedframes = 0
            self._turns -= 1
            self._game.deleteBall()
            self._state = STATE_PAUSED
        if self._game.getNumberBricks() == 0:
            self._state = STATE_COMPLETE
    
    
    def _endgame(self):
        """Initializes a new game when the current game is complete
        
        Waits for a click/touch, then initializes a new game"""
        if isinstance(self.view.touch,GPoint) and self._last == None:
            self.init()

    def _soundControl(self):
        """Toggles sounds on/off when the user clicks on the sound GLabel"""
        soundState = self._game.getSoundState()
        click = self.view.touch
        if self._soundmessage.contains(click.x,click.y):
            self._game.setSoundState(not soundState)
        if soundState:
            soundText = 'Sounds: On'
        else:
            soundText = 'Sounds: Off'
        self._soundmessage = GLabel(x=(GAME_WIDTH),y=(GAME_HEIGHT),
        right=GAME_WIDTH,top=GAME_HEIGHT,text=soundText,
        font_size=15,halign='right',valign='top',font_name='Fix.ttf')
    