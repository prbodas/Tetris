from graphics import *
from random import *

############################################################
# BLOCK CLASS
############################################################

class Block(Rectangle):
    ''' Block class:
        Implement a block for a tetris piece
        Attributes: x - type: int
                    y - type: int
        specify the position on the tetris board
        in terms of the square grid
    '''

    BLOCK_SIZE = 30
    OUTLINE_WIDTH = 3

    def __init__(self, pos, color):
        self.x = pos.x
        self.y = pos.y
        
        p1 = Point(pos.x*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH,
                   pos.y*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH)
        p2 = Point(p1.x + Block.BLOCK_SIZE, p1.y + Block.BLOCK_SIZE)

        Rectangle.__init__(self, p1, p2)
        self.setWidth(Block.OUTLINE_WIDTH)
        self.setFill(color)

    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            checks if the block can move dx squares in the x direction
            and dy squares in the y direction
            Returns True if it can, and False otherwise
            HINT: use the can_move method on the Board object
        '''

        DIRECTION_DOWN = dx == 0 and dy == 1

        OUT_OF_BOUNDS = (self.x + dx) > board.width or (self.x + dx) < 0 or (self.y + dy) > board.height - 1 or (self.y + dy) < 0
        if OUT_OF_BOUNDS or not board.can_move(self.x + dx, self.y + dy):
            return False
        else:
            return True
    
    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int
                        
            moves the block dx squares in the x direction
            and dy squares in the y direction
        '''

        self.x += dx
        self.y += dy

        Rectangle.move(self, dx*Block.BLOCK_SIZE, dy*Block.BLOCK_SIZE)

############################################################
# SHAPE CLASS
############################################################

class Shape():
    ''' Shape class:
        Base class for all the tetris shapes
        Attributes: blocks - type: list - the list of blocks making up the shape
                    rotation_dir - type: int - the current rotation direction of the shape
                    shift_rotation_dir - type: Boolean - whether or not the shape rotates
    '''

    def __init__(self, coords, color):
        self.blocks = []
        self.rotation_dir = 1
        ### A boolean to indicate if a shape shifts rotation direction or not.
        ### Defaults to false since only 3 shapes shift rotation directions (I, S and Z)
        self.shift_rotation_dir = False
        
        for pos in coords:
            self.blocks.append(Block(pos, color))



    def get_blocks(self):
        '''returns the list of blocks
        '''
        #YOUR CODE HERE
        return self.blocks

    def draw(self, win):
        ''' Parameter: win - type: CanvasFrame

            Draws the shape:
            i.e. draws each block
        ''' 
        for block in self.blocks:
            block.draw(win)

    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            moves the shape dx squares in the x direction
            and dy squares in the y direction, i.e.
            moves each of the blocks
        '''
        for block in self.blocks:
            block.move(dx, dy)

    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            checks if the shape can move dx squares in the x direction
            and dy squares in the y direction, i.e.
            check if each of the blocks can move
            Returns True if all of them can, and False otherwise
           
        '''
        
        #YOUR CODE HERE
        for block in self.blocks:
            if not block.can_move(board,dx,dy):
                return False

        return True
    
    def get_rotation_dir(self):
        ''' Return value: type: int
        
            returns the current rotation direction
        '''
        return self.rotation_dir

    def get_rotate_positions(self, board):

        direction = self.get_rotation_dir() # -1 is counterclockwise, 1 is clockwise
        new_blocks = [] #will hold new blocks
        temp_blocks = list(self.blocks) #a temporary copy of self.blocks, excluding the center piece at index 1

        center_point = temp_blocks.pop(1)

         #(x,y) is the center of revolution
        x = center_point.x
        y = center_point.y

        #grid of eight points surrounding a center block, starting from the top left and going clockwise
        moving_grid = [Point(x,y),
                       Point(x-1, y-1),
                       Point(x, y-1),
                       Point(x+1, y-1),
                       Point(x+1, y),
                       Point(x+1, y+1),
                       Point(x, y+1),
                       Point(x-1, y+1),
                       Point(x-1, y)]

        
        for point in temp_blocks:
            for index in range(1, len(moving_grid)):
                newind = None
                #find point in grid that corresponds to point in blocks, excludes index 0 (center of grid)
                if point.x == moving_grid[index].getX() and point.y == moving_grid[index].getY():
                    if direction == -1: #counterclockwise
                        newind = index - 2 #two spots up or down, depending on direction, in the matrix
                    else: #presumably clockwise, assuming so in any case
                        newind = index + 2

                #wraps newind
                if newind == -1:
                    newind = len(moving_grid) - 2
                elif newind == 0:
                    newind = len(moving_grid) - 1
                elif newind == len(moving_grid):
                    newind = 1
                elif newind == len(moving_grid) + 1:
                    newind = 2


                if not newind == None:
                    new_blocks.append(moving_grid[newind])
                    break

        new_blocks.insert(1,moving_grid[0])

        return new_blocks


    def can_rotate(self, board):
        ''' Parameters: board - type: Board object
            Return value: type : bool
            
            Checks if the shape can be rotated.
            
            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation and check if
            the new position is valid
            3. If any of the blocks cannot be moved to their new position,
            return False
                        
            otherwise all is good, return True
        '''
        
        #YOUR CODE HERE
        
        new_blocks = self.get_rotate_positions(board) #this is in points

        for block in new_blocks:
            #check if spot trying to move to is occupied by the same shape
            #if not, then try the board canmove method
            if not board.can_move(block.getX(), block.getY()):

                IS_OCCUPIED = False

                for est in self.blocks:
                    if block.getX() == est.x and block.getY() == est.y:
                        IS_OCCUPIED = True

                if not IS_OCCUPIED: # if not occupied already by the same shape and still cannot move there
                    return False

        return True




    def rotate(self, board):
        ''' Parameters: board - type: Board object

            rotates the shape:
            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation
            3. Move the block to the new position
            
        '''    

        ####  YOUR CODE HERE #####
        rotated_blocks = self.get_rotate_positions(board)

        for index in range(0, len(rotated_blocks)):
            x = self.blocks[index].x
            y = self.blocks[index].y  #old positions x and y, find in board and change
            xnew = rotated_blocks[index].getX()
            ynew = rotated_blocks[index].getY()

            self.blocks[index].move(xnew-x, ynew-y)


        ### This should be at the END of your rotate code. 
        ### DO NOT touch it. Default behavior is that a piece will only shift
        ### rotation direciton after a successful rotation. This ensures that 
        ### pieces which switch rotations definitely remain within their 
        ### accepted rotation positions.
        if self.shift_rotation_dir:
            self.rotation_dir *= -1

        

############################################################
# ALL SHAPE CLASSES
############################################################

 
class I_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 2, center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y)]
        Shape.__init__(self, coords, 'blue')
        self.shift_rotation_dir = True
        self.center_block = self.blocks[2]

    def get_rotate_positions(self, board):
        #Overriding get_rotate positions because the I_shape doesn't work with the 9-grid scheme

        direction = self.get_rotation_dir() # -1 is counterclockwise, 1 is clockwise
        new_blocks = [] #will hold new blocks
        temp_blocks = list(self.blocks) #a temporary copy of self.blocks, excluding the center piece at index 1

        center_point = temp_blocks.pop(1)

         #(x,y) is the center of revolution
        x = center_point.x
        y = center_point.y

        
        for point in temp_blocks:
            if point.y == y: #y is equal to the center
                dx = (point.x - x)*direction
                new_blocks.append(Point(x, y + dx))
            elif point.x == x: #x is equal to center
                dy = (point.y - y)*direction #accounts for clockwise or counterclockwise
                new_blocks.append(Point(x + dy, y))

        new_blocks.insert(1,Point(x,y))

        return new_blocks


class J_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'orange')        
        self.center_block = self.blocks[1]

class L_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'cyan')        
        self.center_block = self.blocks[1]


class O_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x   , center.y + 1),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'red')
        self.center_block = self.blocks[0]

    def rotate(self, board):
        # Override Shape's rotate method since O_Shape does not rotate
        return 

class S_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'green')
        self.center_block = self.blocks[0]
        self.shift_rotation_dir = True
        self.rotation_dir = -1


class T_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x    , center.y + 1)]
        Shape.__init__(self, coords, 'yellow')
        self.center_block = self.blocks[1]


class Z_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y), 
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'magenta')
        self.center_block = self.blocks[1]
        self.shift_rotation_dir = True
        self.rotation_dir = -1      



############################################################
# BOARD CLASS
############################################################

class Board():
    ''' Board class: it represents the Tetris board

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:CanvasFrame - where the pieces will be drawn
                    grid - type:Dictionary - keeps track of the current state of
                    the board; stores the blocks for a given position
    '''
    
    def __init__(self, win, width, height):
        self.width = width
        self.height = height

        # create a canvas to draw the tetris shapes on
        self.canvas = CanvasFrame(win, self.width * Block.BLOCK_SIZE,
                                        self.height * Block.BLOCK_SIZE)
        self.canvas.setBackground('light gray')

        # create an empty dictionary
        # currently we have no shapes on the board
        self.grid = {}

    def draw_shape(self, shape):
        ''' Parameters: shape - type: Shape
            Return value: type: bool

            draws the shape on the board if there is space for it
            and returns True, otherwise it returns False
        '''
        if shape.can_move(self, 0, 0):
            shape.draw(self.canvas)
            return True
        return False

    def can_move(self, x, y):
        ''' Parameters: x - type:int
                        y - type:int
            Return value: type: bool

            1. check if it is ok to move to square x,y
            if the position is outside of the board boundaries, can't move there
            return False

            2. if there is already a block at that postion, can't move there
            return False

            3. otherwise return True
            
        '''

        # false if out of bounds or already a block at that key 
        OUT_OF_BOUNDS = x < 0 or x > self.width-1 or y < 0 or y > self.height-1   
        if OUT_OF_BOUNDS or self.grid.has_key((x,y)):
            return False

        return True

    def add_shape(self, shape):
        ''' Parameter: shape - type:Shape
            
            add a shape to the grid, i.e.
            add each block to the grid using its
            (x, y) coordinates as a dictionary key

            Hint: use the get_blocks method on Shape to
            get the list of blocks
            
        '''
        
        blocks = shape.get_blocks()
        for block in blocks:
            self.grid[(block.x,block.y)] = block        


    def delete_row(self, y):
        ''' Parameters: y - type:int

            remove all the blocks in row y
            to remove a block you must remove it from the grid
            and erase it from the screen.
            If you dont remember how to erase a graphics object
            from the screen, take a look at the Graphics Library
            handout
            
        '''
        
        #YOUR CODE HERE
        for x in range(0,self.width):
            if self.grid.has_key((x,y)):
                self.grid[(x,y)].undraw()
                self.grid.pop((x,y))
    
    def is_row_complete(self, y):        
        ''' Parameter: y - type: int
            Return value: type: bool

            for each block in row y
            check if there is a block in the grid (use the in operator) 
            if there is one square that is not occupied, return False
            otherwise return True
            
        '''
        
        #YOUR CODE HERE
        for x in range(0, self.width):
            if not self.grid.has_key((x,y)): #if doesn't have that key, there is no block there
                return False
        return True
    
    def move_down_rows(self, y_start):
        ''' Parameters: y_start - type:int                        

            for each row from y_start to the top
                for each column
                    check if there is a block in the grid
                    if there is, remove it from the grid
                    and move the block object down on the screen
                    and then place it back in the grid in the new position

        '''
        #print "y_start is ", y_start
        #print "height is ", self.height
        #print "k range is ", range(1,y_start)
        for k in range(0, y_start):
            y = y_start - k
            for x in range(0, self.width):
                if self.grid.has_key((x,y)):
                    #print "(x,y) is", (x,y)
                    block = self.grid.pop((x,y)) #removed and saved
                    block.move(0, 1)
                    self.grid[(x,y+1)] = block
                    #print "(x,y+1) is", (x,y+1)
        
        
    
    def remove_complete_rows(self):
        ''' removes all the complete rows
            1. for each row, y, 
            2. check if the row is complete
                if it is,
                    delete the row
                    move all rows down starting at row y - 1

        '''

        r = 1
        while r < self.height:
            y = self.height - r
            if self.is_row_complete(y):
                #print "row is complete for row ", y
                self.delete_row(y)
                #print "moving down rows"
                self.move_down_rows(y-1)
                r = r - 1
            r = r + 1

    def game_over(self):
        ''' display "Game Over !!!" message in the center of the board
            HINT: use the Text class from the graphics library
        '''
        
        #YOUR CODE HERE
        print "Game Over"        


############################################################
# TETRIS CLASS
############################################################

class Tetris():
    ''' Tetris class: Controls the game play
    Attributes:
    SHAPES - type: list (list of Shape classes)
    DIRECTION - type: dictionary - converts string direction to (dx, dy)
    BOARD_WIDTH - type:int - the width of the board
    BOARD_HEIGHT - type:int - the height of the board
    board - type:Board - the tetris board
    win - type:Window - the window for the tetris game
    delay - type:int - the speed in milliseconds for moving the shapes
    current_shapes - type: Shape - the current moving shape on the board
    '''

    SHAPES = [I_shape, J_shape, L_shape, O_shape, S_shape, T_shape, Z_shape]
    DIRECTION = {'Left':(-1, 0), 'Right':(1, 0), 'Down':(0, 1)}
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    
    def __init__(self, win):
        self.board = Board(win, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.win = win
        self.delay = 1000 #ms

        # sets up the keyboard events
        # when a key is called the method key_pressed will be called
        self.win.bind_all('<Key>', self.key_pressed)

        # set the current shape to a random new shape
        self.current_shape = self.create_new_shape()

        # Draw the current_shape oan the board (take a look at the
        # draw_shape method in the Board class)
        ####  YOUR CODE HERE ####
        self.board.draw_shape(self.current_shape)

        # For Step 9:  animate the shape!
        ####  YOUR CODE HERE ####
        self.animate_shape()


    def create_new_shape(self):
        ''' Return value: type: Shape
            
        Create a random new shape that is centered
        at y = 0 and x = int(self.BOARD_WIDTH/2)
        return the shape
        '''

        #YOUR CODE HERE
        rand = randrange(0,len(self.SHAPES)) #method inclusive on left end only
        q = self.SHAPES[rand](Point(int(self.BOARD_WIDTH/2), 0))
        #q = O_shape(Point(int(self.BOARD_WIDTH/2), 0))
        return q
    
    def animate_shape(self):
        ''' animate the shape - move down at equal intervals
            specified by the delay attribute
        '''
        
        self.do_move('Down')
        self.win.after(self.delay, self.animate_shape)
    
    def do_move(self, direction):
        ''' Parameters: direction - type: string
            Return value: type: bool

            Move the current shape in the direction specified by the parameter:
            First check if the shape can move. If it can, move it and return True
            Otherwise if the direction we tried to move was 'Down',
            1. add the current shape to the board
            2. remove the completed rows if any 
            3. create a new random shape and set current_shape attribute
            4. If the shape cannot be drawn on the board, display a
               game over message

            return False

        '''
        
        #YOUR CODE HERE

        if direction == 'Down':
            dx = self.DIRECTION[direction][0]
            dy = self.DIRECTION[direction][1]
            DOWN_ONE = self.current_shape.can_move(self.board, dx, dy)
            DOWN_TWO = self.current_shape.can_move(self.board, dx, dy*2)

            if DOWN_ONE:
                self.current_shape.move(dx,dy) #move down one

            if not DOWN_TWO or not DOWN_ONE:
                self.board.add_shape(self.current_shape) #add to board
                self.board.remove_complete_rows()
                self.current_shape = self.create_new_shape() #new shape added
                if not self.board.draw_shape(self.current_shape):
                    self.board.game_over()
                return False #can no longer move
            else:
                return True #has moved
        elif direction == 'Up':
            self.do_rotate()
        else: #direction not down or up
            dx = self.DIRECTION[direction][0]
            dy = self.DIRECTION[direction][1]
            if self.current_shape.can_move(self.board, dx, dy):
                self.current_shape.move(dx,dy)
                return True
            return False



        #     if DOWN_ONE and not DOWN_TWO: #can move down only once
        #         self.current_shape.move(dx,dy) #move down one
        #         print "adding shape"
        #         self.board.add_shape(self.current_shape) #add to board
        #         print "added shape"
        #         print "removing complete rows"
        #         self.board.remove_complete_rows()
        #         print "removed"
        #         self.current_shape = self.create_new_shape() #new shape added
        #         if not self.board.draw_shape(self.current_shape):
        #             self.game_over()
        #         return False #can no longer move
        #     elif not DOWN_ONE: #can't move down
        #         print "adding shape"
        #         self.board.add_shape(self.current_shape) #add to board
        #         print "added shape"
        #         print "removing complete rows"
        #         self.board.remove_complete_rows()
        #         print "removed"
        #         self.current_shape = self.create_new_shape() #new shape added
        #         if not self.board.draw_shape(self.current_shape):
        #             self.game_over()
        #         return False #can no longer move
        #     else: #can move like it wants
        #         self.current_shape.move(dx,dy)
        #         return True
        # else: # dir is not down



        # if self.current_shape.can_move(self.board, dx, dy):
        #     self.current_shape.move(dx,dy)
        #     return True
        # else:
        #     print "key_pressed CANNOT move"
        #     print "direction = ", direction
        #     if direction == 'Down':
        #         print "adding shape"
        #         self.board.add_shape(self.current_shape)
        #         print "added shape"
        #         print "removing complete rows"
        #         self.board.remove_complete_rows()
        #         print "removed"
        #         self.current_shape = self.create_new_shape()
        #         if not self.board.draw_shape(self.current_shape):
        #             self.game_over()

        #     return False


    def do_rotate(self):
        ''' Checks if the current_shape can be rotated and
            rotates if it can
        '''
        
        if self.current_shape.can_rotate(self.board):
            self.current_shape.rotate(self.board)
    
    def key_pressed(self, event):
        ''' this function is called when a key is pressed on the keyboard
            it currenly just prints the value of the key

            Modify the function so that if the user presses the arrow keys
            'Left', 'Right' or 'Down', the current_shape will move in
            the appropriate direction

            if the user presses the space bar 'space', the shape will move
            down until it can no longer move and is added to the board

            if the user presses the 'Up' arrow key ,
                the shape should rotate.

        '''
            
        #YOUR CODE HERE
        key = event.keysym
        #print key
        self.do_move(key)
       
################################################################
# Start the game
################################################################

win = Window("Tetris")
game = Tetris(win)
win.mainloop()
