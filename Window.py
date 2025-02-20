import chess
import chess.pgn
import io
import sys
import os
from datetime import datetime
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.properties import *
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.lang.builder import Builder
from kivy.utils import get_hex_from_color, get_color_from_hex
from kivy.uix.popup import Popup
from kivy.uix.label import Label 
import random

Width, Height = 800, 800
Window.size = (Width, Height)
wep = [False,False,False,False,False,False,False,False]
bep = [False,False,False,False,False,False,False,False]

def play_sound(sorf):
    if sorf:
        sound = SoundLoader.load('WAV/success.wav')
    else:
        sound = SoundLoader.load('WAV/failure.wav')
    if sound: 
        sound.play()

def letter_to_xpos(letter):
    if letter == 'a':
        return 0
    if letter == 'b':
        return 1
    if letter == 'c':
        return 2
    if letter == 'd':
        return 3
    if letter == 'e':
        return 4
    if letter == 'f':
        return 5
    if letter == 'g':
        return 6
    if letter == 'h':
        return 7
    raise ValueError("Invalid letter.")

def letter_to_ypos(letter):
    if letter == '1':
        return 0
    if letter == '2':
        return 1
    if letter == '3':
        return 2
    if letter == '4':
        return 3
    if letter == '5':
        return 4
    if letter == '6':
        return 5
    if letter == '7':
        return 6
    if letter == '8':
        return 7
    raise ValueError("Invalid letter")
    
def xpos_to_letter(digit):
    if digit >= 0 and digit <= 7:
        str = "abcdefgh"
        letter = str[digit]
        return letter
    raise ValueError("Invalid digit")
     
def ypos_to_digit(digit):
    if digit >= 0 and digit <= 7:
        letter = chr(ord('0') + digit + 1)
        return letter
    raise ValueError("Invalid digit")
     
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
            available_moves = {"available_moves":[], "pieces_to_capture":[]}
            if self.First_use:
                available_moves["available_moves"] = {(self.grid_x, self.grid_y+1), (self.grid_x, self.grid_y+2)}
            else:
                available_moves["available_moves"] = {(self.grid_x, self.grid_y+1)}
            for piece in pieces:
                if piece.grid_y == self.grid_y + 1 and piece.grid_x == self.grid_x:
                    available_moves["available_moves"] = ()
                if self.First_use and piece.grid_y == self.grid_y + 2 and piece.grid_x == self.grid_x:
                    if len(available_moves) == 2:
                        available_moves["available_moves"].remove((piece.grid_x, piece.grid_y))
                if piece.id[:9] == "BlackPawn" and piece.grid_x == self.grid_x + 1 and piece.grid_y == self.grid_y and self.grid_y == 4 and bep[round(piece.grid_x)]:
                    available_moves["pieces_to_capture"].append((self.grid_x + 1,self.grid_y + 1))
                if piece.id[:9] == "BlackPawn" and piece.grid_x == self.grid_x - 1 and piece.grid_y == self.grid_y and self.grid_y == 4 and bep[round(piece.grid_x)]:
                    available_moves["pieces_to_capture"].append((self.grid_x - 1,self.grid_y + 1))
                if piece.id[:5] == "Black" and piece.grid_x == self.grid_x + 1 and piece.grid_y == self.grid_y + 1:
                    available_moves["pieces_to_capture"].append((self.grid_x + 1,self.grid_y + 1))
                if piece.id[:5] == "Black" and piece.grid_x == self.grid_x - 1 and piece.grid_y == self.grid_y + 1:
                    available_moves["pieces_to_capture"].append((self.grid_x - 1,self.grid_y + 1))
            return available_moves
        if self.id[:5] == "Black":
            available_moves = {"available_moves":(), "pieces_to_capture":[]}
            if self.First_use:
                available_moves["available_moves"] = {(self.grid_x, self.grid_y-1), (self.grid_x, self.grid_y-2)}
            else:
                available_moves["available_moves"] = {(self.grid_x, self.grid_y-1)}
            for piece in pieces:
                if piece.grid_y == self.grid_y - 1 and piece.grid_x == self.grid_x:
                    available_moves["available_moves"] = ()
                if self.First_use and piece.grid_y == self.grid_y - 2 and piece.grid_x == self.grid_x:
                    if len(available_moves) == 2:
                        available_moves["available_moves"].remove((piece.grid_x, piece.grid_y))
                if piece.id[:9] == "WhitePawn" and piece.grid_x == self.grid_x + 1 and piece.grid_y == self.grid_y and self.grid_y == 3 and wep[round(piece.grid_x)]:
                    available_moves["pieces_to_capture"].append((self.grid_x + 1,self.grid_y - 1))          
                if piece.id[:9] == "WhitePawn" and piece.grid_x == self.grid_x - 1 and piece.grid_y == self.grid_y and self.grid_y == 3 and wep[round(piece.grid_x)]:
                    available_moves["pieces_to_capture"].append((self.grid_x - 1,self.grid_y - 1))
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
        no_attack_left = True
        no_attack_right = True
        if self.First_use:
            no_piece_left = True
            no_piece_right = True
            for piece in pieces:
                if piece.grid_y == self.grid_y and piece.grid_x > self.grid_x and (piece.id[5:9] != "Rook" or self.id[:5] != piece.id[:5]):
                    no_piece_right = False
                elif piece.grid_y == self.grid_y and piece.grid_x < self.grid_x and (piece.id[5:9] != "Rook" or self.id[:5] != piece.id[:5]):
                    no_piece_left = False
            if no_piece_left and no_piece_right and self.id == "WhiteKing":
                no_attack_left = self.safe_left(pieces)
                no_attack_right = self.safe_right(pieces)
                if no_attack_left and no_attack_right:
                    return [(self.grid_x-2, 0),(self.grid_x+2, 0)]      
                if no_attack_left:
                    return [(self.grid_x-2, 0)]
                if no_attack_right:  
                    return [(self.grid_x+2, 0)]       
            elif no_piece_left and self.id == "WhiteKing":
                no_attack_left = self.safe_left(pieces) 
                if no_attack_left:
                    return [(self.grid_x-2, 0)]                      
            elif no_piece_right and self.id == "WhiteKing":
                 no_attack_right = self.safe_right(pieces)
                 if no_attack_right:
                     return [(self.grid_x+2, 0)]               
            elif no_piece_left and no_piece_right and self.id == "BlackKing":
                 no_attack_left = self.safe_left(pieces) 
                 no_attack_right = self.safe_right(pieces) 
                 if no_attack_left and no_attack_right:
                     return [(self.grid_x-2, 7),(self.grid_x+2, 7)]     
                 if no_attack_left:
                     return [(self.grid_x-2, 7)]
                 if no_attack_right:
                     return [(self.grid_x+2, 7)]      
            elif no_piece_left and self.id == "BlackKing":
                 no_attack_left = self.safe_left(pieces)  
                 if no_attack_left:
                     return [(self.grid_x-2, 7)]               
            elif no_piece_right and self.id == "BlackKing":
                 no_attack_right = self.safe_right(pieces) 
                 if no_attack_right:
                     return [(self.grid_x+2, 7)]        
            return []
    
    def safe_left(self, pieces):
        if self.id == "WhiteKing":
            places = [[4,0],[3,0],[2,0],[1,0]]
            for plc in places:
                if not self.safe_place(plc, pieces):
                    return False
        if self.id == "BlackKing":
            places = [[4,7],[3,7],[2,7],[1,7]]
            for plc in places:
                if not self.safe_place(plc, pieces):
                    return False
        return True
        
    def safe_right(self, pieces):
        if self.id == "WhiteKing":
            places = [[4,0],[5,0],[6,0]]
            for plc in places:
                if not self.safe_place(plc, pieces):
                    return False
        if self.id == "BlackKing":
            places = [[4,7],[5,7],[6,7]]
            for plc in places:
                if not self.safe_place(plc, pieces):
                    return False
        return True
        
    def safe_place(self, plc, pieces):
        for piece in pieces:
            if (plc[1] == 0 and piece.id[:5] == "Black") or (plc[1] == 7 and piece.id[:5] == "White"):
                if self.attacked(plc, piece):
                    return False
        return True
        
    def attacked(self, plc, piece):
        piecekind = piece.id[5:9]
        if piecekind == "Knig":
            if (piece.grid_x + 2, piece.grid_y + 1) == (plc[0],plc[1]) or (piece.grid_x + 1, piece.grid_y + 2) == (plc[0],plc[1]) or (piece.grid_x - 2, piece.grid_y + 1) == (plc[0],plc[1]) or  (piece.grid_x - 1, piece.grid_y + 2) == (plc[0],plc[1]) or (piece.grid_x + 1, piece.grid_y - 2) == (plc[0],plc[1]) or (piece.grid_x + 2, piece.grid_y - 1) == (plc[0],plc[1]) or  (piece.grid_x - 2, piece.grid_y - 1) == (plc[0],plc[1]) or (piece.grid_x - 1, piece.grid_y - 2) == (plc[0],plc[1]):
               return True
        if piecekind == "Bish":
            if self.diagonal(plc, piece):
                return True
        if piecekind == "Rook":
            if self.straight(plc, piece):
                return True
        if piecekind == "Quee":
            if self.diagonal(plc, piece) or self.straight(plc, piece):
                return True
        if piecekind == "Pawn":
            if (piece.grid_x + 1, piece.grid_y + 1) == (plc[0],plc[1]) or (piece.grid_x - 1, piece.grid_y + 1) == (plc[0],plc[1]) or (piece.grid_x + 1, piece.grid_y - 1) == (plc[0],plc[1]) or (piece.grid_x - 1, piece.grid_y - 1) == (plc[0],plc[1]):
                return True
        return False
        
    def diagonal(self, plc, piece):
        deltax = abs(round(piece.grid_x) - plc[0])
        deltay = abs(round(piece.grid_y) - plc[1])
        if deltax == deltay:
            if piece.grid_x < self.grid_x:
               stepx = +1
            else:
                stepx = -1
            if piece.grid_y < self.grid_y:
                stepy = +1
            else:
                stepy = -1
            for i in range(deltax):
                pgnposx = round(piece.grid_x) + i * stepx + stepx
                pgnposy = round(piece.grid_y) + i * stepy + stepy
                pieceindex = pgnposy * 8 + pgnposx
                pgnpiece = ChessBoard.pgnboard.piece_at(pieceindex)
                if pgnpiece != None:
                    break
            endindex =  plc[1] * 8 + plc[0]
            endpiece = ChessBoard.pgnboard.piece_at(endindex)
            if pgnposy == plc[1] and (endpiece == None or endpiece == 'K' or endpiece == 'k'):
                return True
        return False
    
    def straight(self, plc, piece):
        deltax = abs(round(piece.grid_x) - plc[0])
        deltay = abs(round(piece.grid_y) - plc[1])
        if deltax == 0 or deltay == 0:
            if deltay == 0:
                pgnposy = plc[1]
                if piece.grid_x < self.grid_x:
                    stepx = +1
                if piece.grid_x > self.grid_x:
                    stepx = -1
                for i in range(deltax):
                    pgnposx = round(piece.grid_x) + i * stepx + stepx
                    pieceindex = pgnposy * 8 + pgnposx
                    pgnpiece = ChessBoard.pgnboard.piece_at(pieceindex)
                    if pgnpiece != None:
                        break
                endindex =  plc[1] * 8 + plc[0]
                endpiece = ChessBoard.pgnboard.piece_at(endindex)
                if pgnposx == plc[0] and (endpiece == None or endpiece == 'K' or endpiece == 'k'):
                    return True
            if deltax == 0:
                pgnposx = plc[0]
                if piece.grid_y < self.grid_y:
                    stepy = +1
                if piece.grid_y > self.grid_y:
                    stepy = -1
                for i in range(deltay):
                    pgnposy = round(piece.grid_y) + i * stepy + stepy
                    pieceindex = pgnposy * 8 + pgnposx
                    pgnpiece = ChessBoard.pgnboard.piece_at(pieceindex)
                    if pgnpiece != None:
                        break
                endindex =  plc[1] * 8 + plc[0]
                endpiece = ChessBoard.pgnboard.piece_at(endindex)
                if pgnposy == plc[1] and (endpiece == None or endpiece == 'K' or endpiece == 'k'):
                    return True
        return False              

class ChessBoard(RelativeLayout):

    piece_pressed = False
    id_piece_ = None
    available_moves = {"available_moves":(), "pieces_to_capture":[]}
    turn_ = "White"
    piece_index = None
    check = BooleanProperty(defaultvalue=False)
    pgngame = chess.pgn.Game()
    pgnboard = chess.Board()
    pgn_moves = []
    pgn_index = -1
    pgn_inputmode = False
    white_chess = False
    black_chess = False
    chessmate = False
  
    def __init__(self, **kwargs):
        super(ChessBoard, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down = self.make_pgn_move)
        
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down = self.make_pgn_move)
        self._keyboard = None
        
    def animate_pgn_move(self, index, pgn_move):
        pgnmove = str(pgn_move)
        xfrom = letter_to_xpos(pgnmove[0])
        yfrom = letter_to_ypos(pgnmove[1])
        xto = letter_to_xpos(pgnmove[2])
        yto = letter_to_ypos(pgnmove[3])
        cindex = self.pieceindex_at_board(xto, yto)
        if cindex > -1:
            child = self.children[cindex]
            self.remove_widget(child)
        pindex = self.pieceindex_at_board(xfrom, yfrom)
        if pindex > -1:
            child = self.children[pindex]
            id = child.id
            child.First_use = False
            color = child.id[:5]
            if child.id[5:9] == "Pawn":
                if abs(yto - yfrom) == 2:
                    self.mark_en_passant(color, xto)
                else:
                    self.clear_en_passant(color) 
                if color == "Black" and yto == 2 and abs(xfrom - xto) == 1 and wep[xto]:
                    pieceindex = self.pieceindex_at_board(xto, yto + 1)
                    if pieceindex > -1:
                        piece = self.children[pieceindex]
                        self.remove_widget(piece)
                    print("Enpassant black", wep)
                if color == "White" and yto == 5 and abs(xfrom - xto) == 1 and bep[xto]:
                    pieceindex = self.pieceindex_at_board(xto, yto - 1)
                    if pieceindex > -1:
                        piece = self.children[pieceindex]
                        self.remove_widget(piece)
                    print("Enpassant white", bep)
            else:
                self.clear_en_passant(color) 
            anim = Animation(grid_x = xto, grid_y = yto, t='in_out_expo', duration=0.5)
            anim.start(child)
            if id == "WhiteKing" and xto == 6 and yto == 0:
                piece = self.findpiece("WhiteRook_1")
                anim = Animation(grid_x = 5, grid_y = 0, t='in_out_expo', duration=0.5)
                piece.First_use = False
                anim.start(piece)
            if id == "WhiteKing" and xto == 2 and yto == 0:
                piece = self.findpiece("WhiteRook_0")
                anim = Animation(grid_x = 3, grid_y = 0, t='in_out_expo', duration=0.5)
                piece.First_use = False
                anim.start(piece)
            if id == "BlackKing" and xto == 6 and yto == 7:
                piece = self.findpiece("BlackRook_1")
                anim = Animation(grid_x = 5, grid_y = 7, t='in_out_expo', duration=0.5)
                piece.First_use = False
                anim.start(piece)
            if id == "BlackKing" and xto == 2 and yto == 7:
                piece = self.findpiece("BlackRook_0")
                anim = Animation(grid_x = 3, grid_y = 7, t='in_out_expo', duration=0.5)
                piece.First_use = False
                anim.start(piece)
            if id[:9] == "WhitePawn" and yto == 7:
                 self.remove_widget(child)
                 self.add_widget(Queen(id = "", source="Assets/PNG/WhiteQueen.png", grid_x = xto, grid_y = 7))
            if id[:9] == "BlackPawn" and yto == 0:
                 self.remove_widget(child)
                 self.add_widget(Queen(id = "", source="Assets/PNG/BlackQueen.png", grid_x = xto, grid_y = 0))
        #print("APM:" + str(index), pgnmove, len(pgnmove), xfrom, yfrom, xto, yto, pindex)

    def make_pgn_move(self, keyboard, keycode, text, modifiers):
        l = keycode[1]
        if l == 'q':
            pgn = open("PGN/output.pgn", "w")
            pgn.write(str(self.pgngame))
            pgn.close()
            self.close_application()
        elif l == 'm':
            self.hmmove = "    "
            self.index = 0
            self.pgn_inputmode = True
        if self.pgn_inputmode:
            if (l >= 'a' and l <= 'h') or (l >= '1' and l <= '8'):
                if self.index < 4:
                    self.hmmove = self.hmmove[:self.index] + l + self.hmmove[self.index + 1:]
                    self.index += 1
            elif l == '.':
                xfrom = letter_to_xpos(self.hmmove[0])
                yfrom = letter_to_ypos(self.hmmove[1])
                xto = letter_to_xpos(self.hmmove[2])
                yto = letter_to_ypos(self.hmmove[3])
                print(xfrom, yfrom, xto, yto)
                if ChessBoard.turn_ == "White":
                    labelcolor = [1, 1, 1, 1] 
                else:
                    labelcolor = [0, 0, 0, 1] 
                layout = BoxLayout(orientation='vertical')
                message = Label(text = "Correct? " + self.hmmove, color = labelcolor, font_size='50sp')
                layout.add_widget(message)
                button_layout = BoxLayout(size_hint_y=0.3)
                yes_button = Button(text = 'Yes')
                yes_button.bind(on_release=self.on_yes)
                button_layout.add_widget(yes_button)
                no_button = Button(text = 'No')
                no_button.bind(on_release=self.on_no)
                button_layout.add_widget(no_button)
                layout.add_widget(button_layout)
                self.pp = Popup(title = "PGN", title_size = 50, content = layout, size_hint = (0.5, 0.5), background_color = [4,.4,.2, 1])
                self.pp.open()
        elif l == 'r':
            pgn = open("PGN/input.pgn")
            self.pgngame = chess.pgn.read_game(pgn)
            self.pgnboard = self.pgngame.board()
            for move in self.pgngame.mainline_moves():
                self.pgn_moves.append(move)
            pgn.close()
            self.pgn_index = 0
        elif l == 'l':
            self.listpgn_moves()
        elif l == 'w':
            self.pgngame.headers["Event"] = "Social Chess"
            self.pgngame.headers["White"] = "Wim"
            self.pgngame.headers["Black"] = "Jan"
            current_date = datetime.today().strftime('%Y-%m-%d')
            self.pgngame.headers["Date"] = "2025.02.11"
            self.pgnboard = self.pgngame.board()
            self.pgn_moves = []
            pgn = open("PGN/begin.txt", 'r')
            for line in pgn:
                self.pgn_moves.append(line.strip())
            pgn.close()
            self.pgn_index = 0
            self.hmmove = self.pgn_moves[self.pgn_index][:4]
            node = self.pgngame.add_main_variation(chess.Move.from_uci(self.hmmove))
            node.comment = "Comment"
            self.pgn_index = 1
            while self.pgn_index < len(self.pgn_moves):
                self.hmmove = self.pgn_moves[self.pgn_index][:4]
                node = node.add_main_variation(chess.Move.from_uci(self.hmmove))
                self.pgn_index += 1
            self.pgn_index = 0
            self.pgn_moves = []
            for move in self.pgngame.mainline_moves():
                self.pgn_moves.append(move)
        elif l == 'n':
            if self.pgn_index > -1 and self.pgn_index < len(self.pgn_moves):
                self.animate_pgn_move(self.pgn_index, self.pgn_moves[self.pgn_index])
                self.pgnboard.push(self.pgn_moves[self.pgn_index])
                if self.pgn_index < len(self.pgn_moves):
                    self.pgn_index += 1
                self.turn()
        elif l == 'p':
            print(self.pgnboard, "\n")
        return True

    def close_application(self): 
        App.get_running_app().stop() 
        Window.close()      
    
    def findpiece(self,id):
        for child in self.children:
            if child.id == id:
                return child
                
    def listpgn_moves(self):
        if len(self.pgn_moves) > 0:
            for i in range(len(self.pgn_moves)):
                print(i, self.pgn_moves[i])
        else:
            print("No pgn_moves")
                                     
    def trace(self,id,nr):
        piece = self.findpiece(id)
        print("trace====", id, "nr:", nr, "piece.id:", piece.id)

    def pieceindex_at_board(self, xpos, ypos):
        index = -1
        for child in self.children:
            index += 1
            if child.grid_x == xpos and child.grid_y == ypos:
                return index
        return -1
                    
    def mark_en_passant(self, c, x):
        if c == "White":
            wep[x] = True
        elif c == "Black":
            bep[x] = True
  
    def clear_en_passant(self, c):
        if c == "White":
            wep = [False,False,False,False,False,False,False,False]
        elif c == "Black":
            bep = [False,False,False,False,False,False,False,False]
            
    def on_yes(self, instance):
        node = self.pgngame.end()
        self.pgn_index = len(self.pgn_moves)
        try:
            pgnmove = chess.Move.from_uci(self.hmmove)
            node = node.add_main_variation(pgnmove)
            self.pgn_moves.append(self.hmmove)
            self.pgnboard.push(pgnmove)
            self.animate_pgn_move(self.pgn_index, self.hmmove)
            play_sound(True)
            self.turn()
            print(self.pgnboard, "\n")
        except Exception as e:
            play_sound(False)
            print("Except", e)
        self.hmmove = "    "
        self.index = 0
        self.pgn_inputmode = False
        self.pp.dismiss()
    
    def on_no(self, instance):
        self.pp.dismiss()

    def on_touch_down(self, touch):
        rows, cols = 8,8
        grid_x = int(touch.pos[0] / self.width * rows)
        grid_y = int(touch.pos[1] / self.height * cols)
        for id, child in enumerate(self.children):
            old_x, old_y = child.grid_x, child.grid_y
            if not ChessBoard.piece_pressed:
                if grid_x == child.grid_x and grid_y == child.grid_y and child.id[:5] == ChessBoard.turn_:
                    ChessBoard.piece_pressed = True
                    ChessBoard.piece_index = id
                    ChessBoard.available_moves = child.available_moves(self.children)
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
                    touchmove = xpos_to_letter(round(old_x)) + ypos_to_digit(round(old_y)) + xpos_to_letter(round(grid_x)) + ypos_to_digit(round(grid_y))
                    node = self.pgngame.end()
                    try:
                        pgnmove = chess.Move.from_uci(touchmove)
                        node = node.add_main_variation(pgnmove)
                        self.pgn_moves.append(touchmove)
                        self.pgnboard.push(pgnmove)
                        print(self.pgnboard,"\n")
                    except Exception as e:
                        print("Except", e)
                    anim = Animation(grid_x = grid_x, grid_y = grid_y, t='in_quad', duration=0.5)
                    anim.start(self.children[id])
                    ChessBoard.piece_pressed = False
                    ChessBoard.available_moves = {"available_moves":(), "pieces_to_capture":[]}
                    if grid_y == 7 and child.id[0:9] == "WhitePawn":
                        self.remove_widget(child)
                        self.add_widget(Queen(id="WhiteQueen2",source="Assets/PNG/WhiteQueen.png", grid_x=grid_x, grid_y=grid_y))
                    if grid_y == 0 and child.id[0:9] == "BlackPawn":
                        self.remove_widget(child)
                        self.add_widget(Queen(id="BlackQueen2",source="Assets/PNG/BlackQueen.png", grid_x=grid_x, grid_y=grid_y))
                    if child.id[5:9] == "Pawn" and abs(grid_y - old_y) == 2:
                        self.mark_en_passant(child.id[:5], grid_x)
                    else:
                        self.clear_en_passant(child.id[:5]) 
                    if (child.id[5:9] == "Pawn" or child.id[5:9] == "Rook" or child.id[5:9] == "King") and child.First_use:
                        child.First_use = False
                    self.draw_moves()
                    if self.check_check():
                        anim = Animation(grid_x = old_x, grid_y = old_y, t='in_quad', duration=0.5)
                        anim.start(self.children[id])
                        break
                    else:
                        self.turn()
                        break
                elif (grid_x, grid_y) in ChessBoard.available_moves["pieces_to_capture"]:
                    enpassant = False
                    for enemy in self.children:
                        if enemy.grid_x == grid_x and enemy.grid_y == grid_y:
                            touchmove = xpos_to_letter(round(old_x)) + ypos_to_digit(round(old_y)) + xpos_to_letter(round(grid_x)) + ypos_to_digit(round(grid_y))
                            node = self.pgngame.end()
                            try:
                                pgnmove = chess.Move.from_uci(touchmove)
                                node = node.add_main_variation(pgnmove)
                                self.pgn_moves.append(touchmove)
                                self.pgnboard.push(pgnmove)
                                print(self.pgnboard,"\n")
                            except Exception as e:
                                print("Except", e)
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
                        elif child.id[5:9] == "Pawn" and enemy.id[5:9] == "Pawn" and (child.grid_x - 1 == enemy.grid_x or child.grid_x + 1 == enemy.grid_x) and child.grid_y == enemy.grid_y and child.id[:5] != enemy.id[:5]:
                            touchmove = xpos_to_letter(round(old_x)) + ypos_to_digit(round(old_y)) + xpos_to_letter(round(grid_x)) + ypos_to_digit(round(grid_y))
                            node = self.pgngame.end()
                            try:
                                pgnmove = chess.Move.from_uci(touchmove)
                                node = node.add_main_variation(pgnmove)
                                self.pgn_moves.append(touchmove)
                                self.pgnboard.push(pgnmove)
                                print(self.pgnboard,"\n")
                            except Exception as e:
                                print("Except", e)
                            anim = Animation(grid_x=grid_x, grid_y=grid_y, t='in_out_expo', duration=0.5)
                            anim.start(child)
                            if enemy.grid_x == grid_x and enemy.grid_y == grid_y - 1 and enemy.grid_y == 4 and enemy.id[:5] == "Black":
                                self.remove_widget(enemy)
                            if enemy.grid_x == grid_x and enemy.grid_y == grid_y + 1 and enemy.grid_y == 3 and enemy.id[:5] == "White":
                                self.remove_widget(enemy)
                            ChessBoard.piece_pressed = False
                            ChessBoard.available_moves = {"available_moves":[], "pieces_to_capture":[]}
                            self.draw_moves()
                            enpassant = True
                            self.turn()
                    if child.id[:5] == "White":
                        self.clear_en_passant("Black")
                    else:
                        self.clear_en_passant("White")
            elif ChessBoard.piece_pressed and ChessBoard.id_piece_[5:] == "King" and (grid_x, grid_y) in ChessBoard.available_moves["castling"]:
                touchmove = xpos_to_letter(round(self.children[ChessBoard.piece_index].grid_x)) + ypos_to_digit(round(self.children[ChessBoard.piece_index].grid_y)) + xpos_to_letter(round(grid_x)) + ypos_to_digit(round(grid_y))
                node = self.pgngame.end()
                try:
                    pgnmove = chess.Move.from_uci(touchmove)
                    node = node.add_main_variation(pgnmove)
                    self.pgn_moves.append(touchmove)
                    self.pgnboard.push(pgnmove)
                    print(self.pgnboard,"\n")
                except Exception as e:
                    print("Except", e)
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
                piece.First_use = False
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

    def animate(self, color):
        id = color + "King"
        piece = self.findpiece(id)
        pgnposx = piece.grid_x
        pgnposy = piece.grid_y
        self.remove_widget(piece)
        self.add_widget(King(id="DeadKing", source="Assets/PNG/" + color + "Dead.png", grid_x = pgnposx, grid_y = pgnposy,First_use=True))
        piece = self.findpiece("DeadKing")
        while True:
            pgnposx = random.randint(0, 7)
            pgnposy = random.randint(0, 7)
            pieceindex = pgnposy * 8 + pgnposx
            pgnpiece = self.pgnboard.piece_at(pieceindex)
            if pgnpiece == None:
                break
        anim = Animation(grid_x = pgnposx, grid_y = pgnposy, t='out_bounce', duration=5.0)
        anim += Animation(grid_x = pgnposx, grid_y = pgnposy, t='out_bounce', duration=5.0)
        anim.start(piece)

    def attack_king(self, plc, piece, row, col):
        if piece == "n" or piece == "N":
            if (col + 2, row + 1) == (plc[0], plc[1]) or (col + 1, row + 2) == (plc[0], plc[1]) or (col - 2, row + 1) == (plc[0], plc[1]) or  (col - 1, row + 2) == (plc[0], plc[1]) or (col + 1, row - 2) == (plc[0], plc[1]) or (col + 2, row - 1) == (plc[0], plc[1]) or  (col - 2, row - 1) == (plc[0], plc[1]) or (col - 1, row - 2) == (plc[0], plc[1]):
                return True
        if piece == "b" or piece == "B":
            if self.check_diagonal(plc, piece, row, col):
                return True
        if piece == "r" or piece == "R":
            if self.check_straight(plc, piece, row, col):
                return True
        if piece == "q" or piece == "Q":
            if self.check_diagonal(plc, piece, row, col) or self.check_straight(plc, piece, row, col):
                return True
        if piece == "p" or piece == "P":
            if (col + 1, row + 1) == (plc[0], plc[1]) or (col - 1, row + 1) == (plc[0], plc[1]) or (col + 1, row - 1) == (plc[0], plc[1]) or (col - 1, row - 1) == (plc[0], plc[1]):
                return True
        return False
          
    def check_diagonal(self, plc, piece, row, col):
        deltax = abs(col - plc[0])
        deltay = abs(row - plc[1])
        if deltax == deltay:
            if col < plc[0]:
               stepx = +1
            else:
                stepx = -1
            if row < plc[1]:
                stepy = +1
            else:
                stepy = -1
            for i in range(deltax):
                pgnposx = col + i * stepx + stepx
                pgnposy = row + i * stepy + stepy
                pieceindex = pgnposy * 8 + pgnposx
                pgnpiece = self.pgnboard.piece_at(pieceindex)
                if pgnpiece != None:
                    pgnpiecestr = str(pgnpiece)
                    if pgnpiecestr == 'K' or pgnpiecestr == 'k':
                        return True
                    break
        return False
        
    def check_straight(self, plc, piece, row, col):
        deltax = abs(col - plc[0])
        deltay = abs(row - plc[1])
        if deltax == 0 or deltay == 0:
            if deltax == 0:
                if row < plc[1]:
                    stepy = +1
                if row > plc[1]:
                    stepy = -1
                pgnposx = plc[0]
                for i in range(deltay):
                    pgnposy = row + i * stepy + stepy
                    pieceindex = pgnposy * 8 + pgnposx
                    pgnpiece = self.pgnboard.piece_at(pieceindex)
                    if pgnpiece != None:
                        pgnpiecestr = str(pgnpiece)
                        if pgnpiecestr == 'K' or pgnpiecestr == 'k':
                            return True
                        break
            return False
            if deltay == 0:
                if col < plc[0]:
                    stepx = +1
                if col > plc[0]:
                    stepx = -1
                pgnposy = plc[1]         
                for i in range(deltax):
                    pgnposx = col + i * stepx + stepx
                    pieceindex = pgnposy * 8 + pgnposx
                    pgnpiece = ChessBoard.pgnboard.piece_at(pieceindex)
                    if pgnpiece != None:
                        pgnpiecestr = str(pgnpiece)
                        if pgnpiecestr == 'K' or pgnpiecestr == 'k':
                            return True
                        break
            return False
        return False
          
    def check_place(self, color, plc):
        for row in range(8):
            for col in range(8):
                pieceindex = row * 8 + col
                pgnpiece = self.pgnboard.piece_at(pieceindex)
                piecestr = str(pgnpiece)
                if pgnpiece != None and color == "White" and piecestr >= 'a' and piecestr <= 'z':
                    if self.attack_king(plc, piecestr, row, col):
                        return True
                if pgnpiece != None and color == "Black" and piecestr >= 'A' and piecestr <= 'Z':
                    if self.attack_king(plc, piecestr, row, col):
                        return True
        return False

    def check_white(self):
        for row in range(8):
            for col in range(8):
                pieceindex = row * 8 + col
                pgnpiece = self.pgnboard.piece_at(pieceindex)
                if pgnpiece != None:
                    if str(pgnpiece) == "K":
                        return self.check_place("White", [col, row])
        return False
        
    def check_black(self):
        for row in range(8):
            for col in range(8):
                pieceindex = row * 8 + col
                pgnpiece = self.pgnboard.piece_at(pieceindex)
                if pgnpiece != None:
                    if str(pgnpiece) == "k":
                        return self.check_place("Black", [col, row])
        return False

    def check_check(self):
        if self.turn_ == "White":
            if self.white_chess:
                if self.check_white():
                    self.animate("White")
                    self.chessmate = True
                    return
                else:
                    self.white_chess = False
                    return
            if self.check_black():
                self.black_chess = True
                return
            if self.check_white():
                self.animate("White")
                self.chessmate = True
                return
        if self.turn_ == "Black":
            if self.black_chess:
                if self.check_black():
                    self.animate("Black")
                    self.chessmate = True
                    return
                else:
                    self.black_chess = False
                    return
            if self.check_white():
                self.white_chess = True
                return
            if self.check_black():
                self.animate("Black")
                self.chessmate = True
                return
        return self.chessmate

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
    if sys.platform[0] == 'l':
        path = '/home/jan/git/ChessGameKivy'
    if sys.platform[0] == 'w':
        path = "C:/Users/janbo/OneDrive/Documents/GitHub/ChessGameKivy"
    os.chdir(path)
    ChessApp().run()
