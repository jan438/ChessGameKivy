from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.properties import *
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.lang.builder import Builder
from kivy.utils import get_hex_from_color, get_color_from_hex

Width, Height = 800, 800
Window.size = (Width, Height)

class ChessPiece(ButtonBehavior, Image):

    grid_x = NumericProperty()
    grid_y = NumericProperty()
    id = StringProperty()
    def available_moves(self, pieces):
        pass

class Pawn(ChessPiece):

    First_use = BooleanProperty()
    def callback(instance, value):
        print("Value of First_use changed", value)

    def available_moves(self, pieces):
        if self.id[:5] == "White":
            available_moves = {"available_moves":(), "pieces_to_capture":[]}
            if self.grid_y > 7:
                return available_moves
            if self.First_use:
                available_moves["available_moves"] = ((self.grid_x, self.grid_y+1), (self.grid_x, self.grid_y+2))
            else:
                available_moves["available_moves"] = ((self.grid_x, self.grid_y+1),)
            for piece in pieces:
                if piece.grid_y == self.grid_y + 1 and piece.grid_x == self.grid_x:
                    available_moves["available_moves"] = ()
                if self.First_use and piece.grid_y == self.grid_y + 2 and piece.grid_x == self.grid_x:
                    available_moves["available_moves"] = ()
                if piece.id[:5] == "Black" and piece.grid_x == self.grid_x + 1 and piece.grid_y == self.grid_y + 1:
                    available_moves["pieces_to_capture"].append((self.grid_x + 1,self.grid_y + 1))
                if piece.id[:5] == "Black" and piece.grid_x == self.grid_x - 1 and piece.grid_y == self.grid_y + 1:
                    available_moves["pieces_to_capture"].append((self.grid_x - 1,self.grid_y + 1))
            return available_moves
        if self.id[:5] == "Black":
            available_moves = {"available_moves":(), "pieces_to_capture":[]}
            if self.First_use:
                available_moves["available_moves"] = ((self.grid_x, self.grid_y-1), (self.grid_x,self.grid_y-2))
            else:
                available_moves["available_moves"] = ((self.grid_x, self.grid_y-1),)
            for piece in pieces:
                if piece.grid_y == self.grid_y - 1 and piece.grid_x == self.grid_x:
                    available_moves["available_moves"] = ()
                if self.First_use and piece.grid_y == self.grid_y - 2 and piece.grid_x == self.grid_x:
                    available_moves["available_moves"] = ()
                if piece.id[:5] == "White" and piece.grid_x == self.grid_x + 1 and piece.grid_y == self.grid_y - 1:
                    available_moves["pieces_to_capture"].append((self.grid_x + 1,self.grid_y - 1))
                if piece.id[:5] == "White" and piece.grid_x == self.grid_x - 1 and piece.grid_y == self.grid_y - 1:
                    available_moves["pieces_to_capture"].append((self.grid_x - 1,self.grid_y - 1))
            return available_moves

class Rook(ChessPiece):

    First_use = BooleanProperty()
    def available_moves(self, pieces):
        available_moves = {"available_moves":[], "pieces_to_capture":[]}
        rows = 8
        cols = 8
        for x in range(int(self.grid_x) + 1, cols):
            found = False
            for piece in pieces:
                if piece.grid_x == x and piece.grid_y == self.grid_y:
                    found = True
                    if piece.id[:5] != self.id[:5]:
                        available_moves["pieces_to_capture"].append((piece.grid_x, piece.grid_y))
                    break
            if found:
                break
            available_moves["available_moves"].append((x, self.grid_y))
        for y in range(int(self.grid_y) + 1, rows):
            found = False
            for piece in pieces:
                if piece.grid_x == self.grid_x and piece.grid_y == y:
                    found = True
                    if piece.id[:5] != self.id[:5]:
                        available_moves["pieces_to_capture"].append((piece.grid_x, piece.grid_y))
                    break
            if found:
                break
            available_moves["available_moves"].append((self.grid_x, y))
        for x in range(int(self.grid_x) - 1, -1, -1):
            found = False
            for piece in pieces:
                if piece.grid_x == x and piece.grid_y == self.grid_y:
                    found = True
                    if piece.id[:5] != self.id[:5]:
                        available_moves["pieces_to_capture"].append((piece.grid_x, piece.grid_y))
                    break
            if found:
                break
            available_moves["available_moves"].append((x, self.grid_y))
        for y in range(int(self.grid_y) - 1, -1, -1):
            found = False
            for piece in pieces:
                if piece.grid_x == self.grid_x and piece.grid_y == y:
                    found = True
                    if piece.id[:5] != self.id[:5]:
                        available_moves["pieces_to_capture"].append((piece.grid_x, piece.grid_y))
                    break
            if found:
                break
            available_moves["available_moves"].append((self.grid_x, y))
        return available_moves

class Knight(ChessPiece):

    def available_moves(self, pieces):
        available_moves = {"available_moves":self.create_moves(), "pieces_to_capture":[]}
        for piece in pieces:
            if self.id[:5] == "White":
                if piece.id[:5] == "White" and (piece.grid_x, piece.grid_y) in available_moves["available_moves"]:
                    available_moves["available_moves"].remove((piece.grid_x, piece.grid_y))
                if piece.id[:5] == "Black" and (piece.grid_x, piece.grid_y) in available_moves["available_moves"]:
                    available_moves["available_moves"].remove((piece.grid_x, piece.grid_y))
                    available_moves["pieces_to_capture"].append((piece.grid_x, piece.grid_y))
            if self.id[:5] == "Black":
                if piece.id[:5] == "Black" and (piece.grid_x, piece.grid_y) in available_moves["available_moves"]:
                    available_moves["available_moves"].remove((piece.grid_x, piece.grid_y))
                if piece.id[:5] == "White" and (piece.grid_x, piece.grid_y) in available_moves["available_moves"]:
                    available_moves["available_moves"].remove((piece.grid_x, piece.grid_y))
                    available_moves["pieces_to_capture"].append((piece.grid_x, piece.grid_y))
        return available_moves

    def create_moves(self):
        moves = [
            (self.grid_x + 2, self.grid_y + 1),
            (self.grid_x + 1, self.grid_y + 2),
            (self.grid_x - 2, self.grid_y + 1),
            (self.grid_x - 1, self.grid_y + 2),

            (self.grid_x + 1, self.grid_y - 2),
            (self.grid_x + 2, self.grid_y - 1),
            (self.grid_x - 2, self.grid_y - 1),
            (self.grid_x - 1, self.grid_y - 2),
        ]
        good_moves = []
        for move in moves:
            if move[0] <= 7 and move[1] <= 7 and move[0] >= 0 and move[1] >= 0:
                good_moves.append((move))

        return good_moves

class Bishop(ChessPiece):

    def available_moves(self, pieces):
        available_moves = {"available_moves":[], "pieces_to_capture":[]}
        rows = 8
        cols = 8
        for i in range(1, rows):
            if self.grid_x + i >= rows or self.grid_y + i >= cols:
                break
            found = False
            for piece in pieces:
                if piece.grid_x == self.grid_x + i and piece.grid_y == self.grid_y + i:
                    found = True
                    if piece.id[:5] != self.id[:5]:
                        available_moves["pieces_to_capture"].append((self.grid_x + i, self.grid_y + i))
                    break
            if found:
                break
            available_moves["available_moves"].append((self.grid_x + i, self.grid_y + i))
        for i in range(1, rows):
            if self.grid_x - i < 0 or self.grid_y + i >= rows:
                break
            found = False
            for piece in pieces:
                if piece.grid_x == self.grid_x - i and piece.grid_y == self.grid_y + i:
                    found = True
                    if piece.id[:5] != self.id[:5]:
                        available_moves["pieces_to_capture"].append((self.grid_x - i, self.grid_y + i))
                    break
            if found:
                break
            available_moves["available_moves"].append((self.grid_x - i, self.grid_y + i))
        for i in range(1, rows):
            if self.grid_x - i < 0 or self.grid_y - i < 0:
                break
            found = False
            for piece in pieces:
                if piece.grid_x == self.grid_x - i and piece.grid_y == self.grid_y - i:
                    found = True
                    if piece.id[:5] != self.id[:5]:
                        available_moves["pieces_to_capture"].append((self.grid_x - i, self.grid_y - i))
                    break
            if found:
                break
            available_moves["available_moves"].append((self.grid_x - i, self.grid_y - i))
        for i in range(1, rows):
            if self.grid_x + i >= rows or self.grid_y - i < 0:
                break
            found = False
            for piece in pieces:
                if piece.grid_x == self.grid_x + i and piece.grid_y == self.grid_y - i:
                    found = True
                    if piece.id[:5] != self.id[:5]:
                        available_moves["pieces_to_capture"].append((self.grid_x + i, self.grid_y - i))
                    break
            if found:
                break
            available_moves["available_moves"].append((self.grid_x + i, self.grid_y - i))
        return available_moves

class Queen(Rook, Bishop):
    def available_moves(self, pieces):
        available_moves1 = Rook.available_moves(self,pieces)
        available_moves2 = Bishop.available_moves(self,pieces)
        available_moves = {key: val + available_moves2[key] for key, val in available_moves1.items()}
        return available_moves

class King(ChessPiece):
    First_use = BooleanProperty()
    def available_moves(self, pieces):
        available_moves = self.create_moves()
        rows, cols = 8,8
        good_available_moves = []
        for move in available_moves["available_moves"]:
            if move[0] <= cols and move[1] <= rows and move[1] >= 0 and move[0] >= 0:
                good_available_moves.append(move)
        available_moves["available_moves"] = good_available_moves
        for piece in pieces:
            if (piece.grid_x, piece.grid_y) in available_moves["available_moves"]:
                if piece.id[:5] != self.id[:5]:
                    available_moves["available_moves"].remove((piece.grid_x, piece.grid_y))
                    available_moves["pieces_to_capture"].append((piece.grid_x, piece.grid_y))
                available_moves["available_moves"].remove((piece.grid_x, piece.grid_y))
        if self.First_use:
            #print("Available King:",self.id,self.castling(pieces))
            available_moves["castling"] = self.castling(pieces)
        return available_moves

    def create_moves(self):
        available_moves = {"available_moves":[], "pieces_to_capture":[]}
        available_moves["available_moves"].append((self.grid_x, self.grid_y+1))
        available_moves["available_moves"].append((self.grid_x-1, self.grid_y+1))
        available_moves["available_moves"].append((self.grid_x+1, self.grid_y+1))
        available_moves["available_moves"].append((self.grid_x-1, self.grid_y))
        available_moves["available_moves"].append((self.grid_x-1, self.grid_y-1))
        available_moves["available_moves"].append((self.grid_x+1, self.grid_y))
        available_moves["available_moves"].append((self.grid_x+1, self.grid_y-1))
        available_moves["available_moves"].append((self.grid_x, self.grid_y-1))
        return available_moves

    def castling(self, pieces):
        if self.First_use:
            no_piece_left = True
            no_piece_right = True
            for piece in pieces:
                #print("Castling def1",piece.id,piece.grid_x,piece.grid_y)
                if piece.grid_y == self.grid_y and piece.grid_x > self.grid_x and (piece.id[5:9] != "Rook" or self.id[:5] != piece.id[:5]):
                    no_piece_right = False

                elif piece.grid_y == self.grid_y and piece.grid_x < self.grid_x and (piece.id[5:9] != "Rook" or self.id[:5] != piece.id[:5]):
                    no_piece_left = False
            if no_piece_right and no_piece_left:
                #print("Castling def2 no leftt no right:",self.grid_x-2,self.grid_y,self.id,self.grid_x+2,self.grid_y)
                return [(self.grid_x-2, self.grid_y),(self.grid_x+2, self.grid_y)]
            if no_piece_right:
                #print("Castling def2 no right:",self.grid_x+2,self.grid_y,self.id)
                return [(self.grid_x+2, self.grid_y)]
            if no_piece_left:
                #print("Castling def2 no left:",self.grid_x-2,self.grid_y,self.id)
                return [(self.grid_x-2, self.grid_y)]
        return []

class ChessBoard(RelativeLayout):
    piece_pressed = False
    id_piece_ = None
    available_moves = {"available_moves":(), "pieces_to_capture":[]}
    turn_ = "White"
    piece_index = None
    check = BooleanProperty(defaultvalue=False)
    
    def listpieces(self):
        for child in self.children:
            print("Human board",child.id,child.grid_x,child.grid_y)           
    
    def findpiece(self,id):
        for child in self.children:
            #print("find====",child.id)
            if child.id == id:
                return child
                
    def trace(self,id,nr):
        piece = self.findpiece(id)
        print("trace====",id,"nr:",nr,"piece.id:",piece.id,"piece.grid_y",piece.grid_y)

    def on_touch_down(self, touch):
        print("Len:",len(self.children))
        traceid = "WhitePawn_3"
        self.trace(traceid,1)
        rows, cols = 8,8
        grid_x = int(touch.pos[0] / self.width * rows)
        grid_y = int(touch.pos[1] / self.height * cols)
        print("On toch", grid_x, grid_y)
        for id, child in enumerate(self.children):
            if grid_x == child.grid_x and grid_y == child.grid_y:
                print(child.id,child.grid_x,grid_y)
        for id, child in enumerate(self.children):
            old_x, old_y = child.grid_x, child.grid_y
            if not ChessBoard.piece_pressed:
                if grid_x == child.grid_x and grid_y == child.grid_y and child.id[:5] == ChessBoard.turn_:
                    ChessBoard.piece_pressed = True
                    ChessBoard.piece_index = id
                    ChessBoard.available_moves = child.available_moves(self.children)
                    print(ChessBoard.available_moves)
                    self.draw_moves()
                    ChessBoard.id_piece_ = child.id
                    break
            elif ChessBoard.piece_pressed and grid_x == child.grid_x and grid_y == child.grid_y and ChessBoard.id_piece_[:5] == child.id[:5]:
                ChessBoard.available_moves = child.available_moves(self.children)
                self.draw_moves()
                ChessBoard.id_piece_ = child.id
                ChessBoard.piece_index = id
                break
            elif ChessBoard.piece_pressed and child.id == ChessBoard.id_piece_:
                if (grid_x, grid_y) in ChessBoard.available_moves["available_moves"]:
                    ########### optie 1 grid_x and grid_y updaten
                    anim = Animation(grid_x=grid_x, grid_y=grid_y, t='in_quad', duration=0.5)
                    anim.start(self.children[id])
                    ChessBoard.piece_pressed = False
                    ChessBoard.available_moves = {"available_moves":(), "pieces_to_capture":[]}
                    if (child.id[5:9] == "Pawn" or child.id[5:9] == "Rook" or child.id[5:9] == "King") and child.First_use:
                        child.First_use = False
                    self.draw_moves()
                    if self.check_check():
                        anim = Animation(grid_x=old_x, grid_y=old_y, t='in_quad', duration=0.5)
                        anim.start(self.children[id])
                        break
                    else:
                        print("3b")
                        self.trace(traceid,2)
                        self.turn()
                        break
                elif (grid_x, grid_y) in ChessBoard.available_moves["pieces_to_capture"]:
                    for enemy in self.children:
                        if enemy.grid_x == grid_x and enemy.grid_y == grid_y:
                            anim = Animation(grid_x=grid_x, grid_y=grid_y, t='in_out_expo', duration=0.5)
                            anim.start(self.children[id])
                            self.remove_widget(enemy)
                            ChessBoard.piece_pressed = False
                            ChessBoard.available_moves = {"available_moves":(), "pieces_to_capture":[]}
                            if (child.id[5:9] == "Pawn" or child.id[5:9] == "Rook" or child.id[5:9] == "King") and child.First_use:
                                child.First_use = False
                            self.draw_moves()
                            if self.check_check():
                                anim = Animation(grid_x=old_x, grid_y=old_y, t='in_quad', duration=0.5)
                                anim.start(self.children[id])
                                break
                            else:
                                self.turn()
                                break
            elif ChessBoard.piece_pressed and ChessBoard.id_piece_[5:] == "King" and (grid_x, grid_y) in ChessBoard.available_moves["castling"]:
                print("Castling uitvoeren")
                if grid_x == 2 and grid_y == 0:
                    piece = self.findpiece("WhiteRook_0")
                    anim = Animation(grid_x=grid_x+1, grid_y=grid_y, t='in_out_expo', duration=0.5)
                    anim.start(piece)
                if grid_x == 2 and grid_y == 7:
                    piece = self.findpiece("BlackRook_0")
                    anim = Animation(grid_x=grid_x+1, grid_y=grid_y, t='in_out_expo', duration=0.5)
                    anim.start(piece)
                if grid_x == 6 and grid_y == 0:
                    piece = self.findpiece("WhiteRook_1")
                    anim = Animation(grid_x=grid_x-1, grid_y=grid_y, t='in_out_expo', duration=0.5)
                    anim.start(piece)
                if grid_x == 6 and grid_y == 7:
                    piece = self.findpiece("BlackRook_1")
                    anim = Animation(grid_x=grid_x-1, grid_y=grid_y, t='in_out_expo', duration=0.5)
                    anim.start(piece)
                anim = Animation(grid_x=grid_x, grid_y=grid_y, t='in_out_expo', duration=0.5)
                anim.start(self.children[ChessBoard.piece_index])
                ChessBoard.piece_pressed = False
                self.children[ChessBoard.piece_index].First_use = False
                ChessBoard.available_moves = {"available_moves":(), "pieces_to_capture":[]}
                if self.check_check():
                    anim = Animation(grid_x=old_x, grid_y=old_y, t='in_quad', duration=0.5)
                    anim.start(self.children[id])
                    if ChessBoard.id_piece_ == "White":
                        anim = Animation(grid_x=4, grid_y=0, t='in_quad', duration=0.5)
                        anim.start(self.children[ChessBoard.piece_index])
                    self.children[ChessBoard.piece_index].First_use = True
                    break
                else:
                    self.turn()
                    self.draw_moves()
                    break
                self.turn()
                self.draw_moves()

    def turn(self):
        if ChessBoard.turn_ == "White":
            ChessBoard.turn_ = "Black"
        else:
            ChessBoard.turn_ = "White"
        #self.listpieces()

    def check_check(self):
        King = None
        for piece_ in self.children:
            if piece_.id[:5] == ChessBoard.turn_ and piece_.id[5:] == "King":
                King = piece_
                break
        for piece in self.children:
            if piece.id[:5] != ChessBoard.turn_:
                piece_available_moves = piece.available_moves(self.children)
                if (King.grid_x, King.grid_y) in piece_available_moves["available_moves"] or (King.grid_x, King.grid_y) in piece_available_moves["pieces_to_capture"]:
                    return True
        return False

    def checkmate(self):
        if self.check_check():
            still_check = True
            for child in self.children:
                if child.id[:5] == ChessBoard.turn_:
                    every_move = []
                    for type_of_moves in child.available_moves(self.children).values():
                        every_move.extend(type_of_moves)
                    for move in every_move:
                        if child.id[5:9] == "Pawn":
                            self.add_widget(Pawn(id=child.id[:5]+"InvPawn",source=None,grid_x=move[0], grid_y=move[1]))
                        elif child.id[5:9] == "Rook":
                            self.add_widget(Rook(id=child.id[:5]+"InvRook",source=None,grid_x=move[0], grid_y=move[1]))
                        elif child.id[5:11] == "Knight":
                            self.add_widget(Knight(id=child.id[:5]+"InvKnight",source=None,grid_x=move[0], grid_y=move[1]))
                        elif child.id[5:11] == "Bishop":
                            self.add_widget(Bishop(id=child.id[:5]+"InvBishop",source=None,grid_x=move[0], grid_y=move[1]))
                        elif child.id[5:10] == "Queen":
                            self.add_widget(Queen(id=child.id[:5]+"InvQueen",source=None,grid_x=move[0], grid_y=move[1]))
                        elif child.id[5:9] == "King":
                            self.add_widget(King(id=child.id[:5]+"InvKing",source=None,grid_x=move[0], grid_y=move[1]))
                        if not self.check_check():
                            still_check = False
                        for child2 in self.children:
                            if "Inv" in child2.id:
                                self.remove_widget(child2)
                        if not still_check:
                            return False
        return True

    def draw_moves(self):
        grid_size_x = self.width / 8
        grid_size_y = self.height / 8
        Blue = (0, 0, 1)
        Green = (0, 1, 0)
        with self.canvas:
            self.canvas.remove_group("moves")
            size = (0.2*grid_size_x, 0.2*grid_size_y)
            for idx, moves in enumerate(ChessBoard.available_moves.values()):
                if idx == 0:
                    Color(rgb=Blue)
                    for move in moves:
                        Ellipse(pos=(grid_size_x * move[0]+grid_size_x/2 - size[0]/2, grid_size_y * move[1] + grid_size_y/2 - size[1]/2), size=size, group="moves")
                elif idx == 1:
                    Color(rgb=Green)
                    for move in moves:
                        Ellipse(pos=(grid_size_x * move[0]+grid_size_x/2 - size[0]/2, grid_size_y * move[1] + grid_size_y/2 - size[1]/2), size=size, group="moves")

    def on_size(self, *_):
        self.draw_board()
        self.draw_moves()

    def update(self):
        pass

    def on_pos(self, *_):
        self.draw_board()
        self.draw_moves()

    def draw_board(self):
        is_white = False
        grid_size_x = self.width / 8
        grid_size_y = self.height / 8
        with self.canvas.before:
            for y in range(8):
                for x in range(8):
                    if is_white:
                        Color(rgb=get_color_from_hex('#ECDFCB'))
                    else:
                        Color(rgb=get_color_from_hex('#A18E6E'))
                    Rectangle(pos=(grid_size_x * x, grid_size_y * y), size=(grid_size_x, grid_size_y))
                    is_white = not is_white
                is_white = not is_white

class ChessBoardScreen(Screen):
    def __init__(self, **kwargs):
        super(ChessBoardScreen, self).__init__(**kwargs)
        self.game = ChessGame()
        self.add_widget(self.game)

class ChessApp(App):
    def build(self):
        board = ChessBoard()
        for col in range(8):
            board.add_widget(Pawn(id="WhitePawn_"+str(col),source="Assets/PNG/WhitePawn.png",grid_x=col, grid_y=1))
            board.add_widget(Pawn(id="BlackPawn_"+str(col),source="Assets/PNG/BlackPawn.png",grid_x=col, grid_y=6))
        board.add_widget(Rook(id="WhiteRook_"+str(0),source="Assets/PNG/WhiteRook.png",grid_x=0, grid_y=0))
        board.add_widget(Rook(id="WhiteRook_"+str(1),source="Assets/PNG/WhiteRook.png",grid_x=7, grid_y=0))
        board.add_widget(Knight(id="WhiteKnight_"+str(0),source="Assets/PNG/WhiteKnight.png",grid_x=1, grid_y=0))
        board.add_widget(Knight(id="WhiteKnight_"+str(1),source="Assets/PNG/WhiteKnight.png",grid_x=6, grid_y=0))
        board.add_widget(Bishop(id="WhiteBishop_"+str(0),source="Assets/PNG/WhiteBishop.png",grid_x=2, grid_y=0))
        board.add_widget(Bishop(id="WhiteBishop_"+str(1),source="Assets/PNG/WhiteBishop.png",grid_x=5, grid_y=0))
        board.add_widget(Queen(id="WhiteQueen",source="Assets/PNG/WhiteQueen.png",grid_x=3, grid_y=0))
        board.add_widget(King(id="WhiteKing",source="Assets/PNG/WhiteKing.png",grid_x=4, grid_y=0))
        board.add_widget(Rook(id="BlackRook_"+str(0),source="Assets/PNG/BlackRook.png",grid_x=0, grid_y=7))
        board.add_widget(Rook(id="BlackRook_"+str(1),source="Assets/PNG/BlackRook.png",grid_x=7, grid_y=7))
        board.add_widget(Knight(id="BlackKnight_"+str(0),source="Assets/PNG/BlackKnight.png",grid_x=1, grid_y=7))
        board.add_widget(Knight(id="BlackKnight_"+str(1),source="Assets/PNG/BlackKnight.png",grid_x=6, grid_y=7))
        board.add_widget(Bishop(id="BlackBishop_"+str(0),source="Assets/PNG/BlackBishop.png",grid_x=2, grid_y=7))
        board.add_widget(Bishop(id="BlackBishop_"+str(1),source="Assets/PNG/BlackBishop.png",grid_x=5, grid_y=7))
        board.add_widget(Queen(id="BlackQueen",source="Assets/PNG/BlackQueen.png",grid_x=3, grid_y=7))
        board.add_widget(King(id="BlackKing",source="Assets/PNG/BlackKing.png",grid_x=4, grid_y=7))
        return board

if __name__ == '__main__':
    ChessApp().run()
