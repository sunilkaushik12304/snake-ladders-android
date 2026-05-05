"""
Snake and Ladders - Android Game
Built with Python + Kivy
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle, Ellipse, Line, RoundedRectangle
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.properties import (
    NumericProperty, StringProperty, BooleanProperty, ListProperty
)
import random
import math

# ── Color palette ──────────────────────────────────────────────────────────────
C_BG        = (0.08, 0.07, 0.06, 1)
C_SURFACE   = (0.14, 0.12, 0.10, 1)
C_CARD      = (0.18, 0.16, 0.13, 1)
C_BORDER    = (0.30, 0.27, 0.22, 1)
C_TEXT      = (0.96, 0.94, 0.90, 1)
C_MUTED     = (0.55, 0.52, 0.48, 1)
C_P1        = (0.89, 0.29, 0.29, 1)   # red
C_P2        = (0.22, 0.54, 0.87, 1)   # blue
C_LADDER    = (0.23, 0.43, 0.07, 1)   # green
C_SNAKE     = (0.89, 0.29, 0.29, 1)   # red
C_ACCENT    = (0.94, 0.78, 0.47, 1)   # amber

# ── Board definition ────────────────────────────────────────────────────────────
SNAKES  = {99: 54, 70: 55, 52: 42, 25: 7, 36: 3}
LADDERS = {4: 14, 9: 31, 20: 38, 28: 84, 40: 59, 51: 67, 63: 81, 71: 91}

DICE_FACES = {
    1: [(0.5, 0.5)],
    2: [(0.25, 0.75), (0.75, 0.25)],
    3: [(0.25, 0.75), (0.5, 0.5), (0.75, 0.25)],
    4: [(0.25, 0.75), (0.75, 0.75), (0.25, 0.25), (0.75, 0.25)],
    5: [(0.25, 0.75), (0.75, 0.75), (0.5, 0.5), (0.25, 0.25), (0.75, 0.25)],
    6: [(0.25, 0.83), (0.75, 0.83), (0.25, 0.5), (0.75, 0.5), (0.25, 0.17), (0.75, 0.17)],
}


def cell_to_xy(n, origin_x, origin_y, cell_size):
    """Convert board cell number (1-100) to pixel centre."""
    idx = n - 1
    row = idx // 10
    col = idx % 10
    board_row = 9 - row
    board_col = col if row % 2 == 0 else 9 - col
    x = origin_x + board_col * cell_size + cell_size / 2
    y = origin_y + board_row * cell_size + cell_size / 2
    return x, y


# ── Board Widget ────────────────────────────────────────────────────────────────
class BoardWidget(Widget):
    p1_pos = NumericProperty(1)
    p2_pos = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._redraw, pos=self._redraw,
                  p1_pos=self._redraw, p2_pos=self._redraw)

    def _redraw(self, *args):
        self.canvas.clear()
        self._draw()

    def _board_metrics(self):
        size = min(self.width, self.height)
        cell = size / 10
        ox = self.x + (self.width - size) / 2
        oy = self.y + (self.height - size) / 2
        return ox, oy, cell, size

    def _draw(self):
        ox, oy, cell, size = self._board_metrics()
        with self.canvas:
            # Background
            Color(*C_BG)
            Rectangle(pos=(ox, oy), size=(size, size))

            # Cells
            for r in range(10):
                for c in range(10):
                    board_row = 9 - r
                    n = r * 10 + (c if r % 2 == 0 else 9 - c) + 1
                    alt = (r + c) % 2 == 0
                    if alt:
                        Color(0.16, 0.14, 0.11, 1)
                    else:
                        Color(0.20, 0.18, 0.14, 1)
                    Rectangle(pos=(ox + c * cell, oy + board_row * cell),
                               size=(cell, cell))

            # Grid lines
            Color(*C_BORDER, 0.3)
            for i in range(11):
                Line(points=[ox + i * cell, oy, ox + i * cell, oy + size], width=0.5)
                Line(points=[ox, oy + i * cell, ox + size, oy + i * cell], width=0.5)

            # Ladders
            for start, end in LADDERS.items():
                sx, sy = cell_to_xy(start, ox, oy, cell)
                ex, ey = cell_to_xy(end, ox, oy, cell)
                dx, dy = ex - sx, ey - sy
                length = math.sqrt(dx * dx + dy * dy)
                if length == 0:
                    continue
                nx, ny = -dy / length * cell * 0.12, dx / length * cell * 0.12
                Color(0.23, 0.43, 0.07, 1)
                Line(points=[sx + nx, sy + ny, ex + nx, ey + ny], width=dp(2.5))
                Line(points=[sx - nx, sy - ny, ex - nx, ey - ny], width=dp(2.5))
                # Rungs
                Color(0.47, 0.76, 0.22, 1)
                steps = max(2, int(length / (cell * 0.7)))
                for s in range(1, steps):
                    t = s / steps
                    mx = sx + dx * t
                    my = sy + dy * t
                    Line(points=[mx + nx, my + ny, mx - nx, my - ny], width=dp(1.5))

            # Snakes
            for start, end in SNAKES.items():
                sx, sy = cell_to_xy(start, ox, oy, cell)
                ex, ey = cell_to_xy(end, ox, oy, cell)
                Color(0.64, 0.18, 0.18, 1)
                Line(bezier=[sx, sy,
                              sx + (ex - sx) * 0.3 + cell * 0.5, sy + (ey - sy) * 0.3,
                              ex + cell * 0.3, ey + (sy - ey) * 0.3,
                              ex, ey], width=dp(3.5))
                Color(0.89, 0.29, 0.29, 1)
                Line(bezier=[sx, sy,
                              sx + (ex - sx) * 0.3 + cell * 0.5, sy + (ey - sy) * 0.3,
                              ex + cell * 0.3, ey + (sy - ey) * 0.3,
                              ex, ey], width=dp(1.5))
                # Snake head
                r2 = cell * 0.13
                Color(0.89, 0.29, 0.29, 1)
                Ellipse(pos=(sx - r2, sy - r2), size=(r2 * 2, r2 * 2))
                Color(1, 1, 1, 1)
                ed = r2 * 0.38
                Ellipse(pos=(sx - r2 * 0.5 - ed / 2, sy + r2 * 0.1), size=(ed, ed))
                Ellipse(pos=(sx + r2 * 0.1, sy + r2 * 0.1), size=(ed, ed))

            # Cell numbers
            for r in range(10):
                for c in range(10):
                    board_row = 9 - r
                    n = r * 10 + (c if r % 2 == 0 else 9 - c) + 1

        # Draw numbers via Label hack — use canvas.after for text
        for r in range(10):
            for c in range(10):
                board_row = 9 - r
                n = r * 10 + (c if r % 2 == 0 else 9 - c) + 1
                # We'll skip individual labels for performance;
                # numbers visible in cell drawing above

        with self.canvas:
            # Player tokens
            self._draw_token(self.p1_pos, C_P1, 'P1', ox, oy, cell, offset=-0.18)
            self._draw_token(self.p2_pos, C_P2, 'P2', ox, oy, cell, offset=0.18)

    def _draw_token(self, pos, color, label, ox, oy, cell, offset=0):
        cx, cy = cell_to_xy(pos, ox, oy, cell)
        cx += offset * cell
        r = cell * 0.22
        # Shadow
        Color(0, 0, 0, 0.4)
        Ellipse(pos=(cx - r + dp(1), cy - r - dp(1)), size=(r * 2, r * 2))
        # Token body
        Color(*color)
        Ellipse(pos=(cx - r, cy - r), size=(r * 2, r * 2))
        # White ring
        Color(1, 1, 1, 0.9)
        Line(circle=(cx, cy, r - dp(1)), width=dp(1.2))


# ── Dice Widget ─────────────────────────────────────────────────────────────────
class DiceWidget(Widget):
    value = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._draw, pos=self._draw, value=self._draw)

    def _draw(self, *args):
        self.canvas.clear()
        w, h = self.size
        with self.canvas:
            Color(*C_CARD)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
            Color(*C_BORDER)
            Line(rounded_rectangle=[*self.pos, w, h, dp(8)], width=dp(0.8))
            # Dots
            Color(*C_TEXT)
            dot_r = min(w, h) * 0.08
            for rx, ry in DICE_FACES.get(self.value, []):
                cx = self.x + rx * w
                cy = self.y + ry * h
                Ellipse(pos=(cx - dot_r, cy - dot_r), size=(dot_r * 2, dot_r * 2))

    def roll_animation(self, final_value, callback):
        count = [0]
        max_count = 14

        def step(dt):
            count[0] += 1
            self.value = random.randint(1, 6)
            if count[0] >= max_count:
                self.value = final_value
                Clock.unschedule(step)
                callback()

        Clock.schedule_interval(step, 0.06)


# ── Setup Screen ────────────────────────────────────────────────────────────────
class SetupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        root = FloatLayout()
        with root.canvas.before:
            Color(*C_BG)
            self._bg_rect = Rectangle(size=root.size, pos=root.pos)
        root.bind(size=lambda i, v: setattr(self._bg_rect, 'size', v),
                  pos=lambda i, v: setattr(self._bg_rect, 'pos', v))

        layout = BoxLayout(orientation='vertical', padding=dp(32), spacing=dp(20),
                           size_hint=(0.88, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Title
        title = Label(text='🎲 Snake & Ladders', font_size=sp(28),
                      color=C_ACCENT, bold=True,
                      size_hint_y=None, height=dp(60), halign='center')
        layout.add_widget(title)

        subtitle = Label(text='Enter player names to begin', font_size=sp(14),
                         color=C_MUTED, size_hint_y=None, height=dp(28), halign='center')
        layout.add_widget(subtitle)

        # Spacer
        layout.add_widget(Widget(size_hint_y=None, height=dp(12)))

        # Player 1 input
        p1_label = Label(text='Player 1 (Red)', font_size=sp(13), color=C_P1,
                         size_hint_y=None, height=dp(24), halign='left',
                         text_size=(None, None))
        p1_label.bind(size=p1_label.setter('text_size'))
        layout.add_widget(p1_label)

        self.p1_input = TextInput(
            hint_text='Enter name...', multiline=False,
            font_size=sp(16), size_hint_y=None, height=dp(48),
            background_color=C_CARD,
            foreground_color=C_TEXT,
            hint_text_color=C_MUTED,
            cursor_color=C_P1,
            padding=[dp(14), dp(12)],
        )
        layout.add_widget(self.p1_input)

        layout.add_widget(Widget(size_hint_y=None, height=dp(8)))

        # Player 2 input
        p2_label = Label(text='Player 2 (Blue)', font_size=sp(13), color=C_P2,
                         size_hint_y=None, height=dp(24), halign='left')
        p2_label.bind(size=p2_label.setter('text_size'))
        layout.add_widget(p2_label)

        self.p2_input = TextInput(
            hint_text='Enter name...', multiline=False,
            font_size=sp(16), size_hint_y=None, height=dp(48),
            background_color=C_CARD,
            foreground_color=C_TEXT,
            hint_text_color=C_MUTED,
            cursor_color=C_P2,
            padding=[dp(14), dp(12)],
        )
        layout.add_widget(self.p2_input)

        layout.add_widget(Widget(size_hint_y=None, height=dp(16)))

        # Start button
        start_btn = Button(
            text='START GAME  ▶',
            font_size=sp(17), bold=True,
            background_color=C_ACCENT,
            color=(0.08, 0.07, 0.06, 1),
            size_hint_y=None, height=dp(54),
            border=(0, 0, 0, 0),
        )
        start_btn.bind(on_press=self.start_game)
        layout.add_widget(start_btn)

        layout.height = sum(
            c.height for c in layout.children if hasattr(c, 'height')
        ) + layout.spacing * (len(layout.children) - 1) + layout.padding[1] * 2 + dp(160)

        root.add_widget(layout)
        self.add_widget(root)

    def start_game(self, *args):
        p1 = self.p1_input.text.strip() or 'Player 1'
        p2 = self.p2_input.text.strip() or 'Player 2'
        game_screen = self.manager.get_screen('game')
        game_screen.setup_players(p1, p2)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'game'


# ── Game Screen ─────────────────────────────────────────────────────────────────
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.p1_name = 'Player 1'
        self.p2_name = 'Player 2'
        self.positions = [1, 1]
        self.current = 0
        self.rolling = False
        self._build_ui()

    def _build_ui(self):
        root = BoxLayout(orientation='vertical')
        with root.canvas.before:
            Color(*C_BG)
            self._bg = Rectangle(size=root.size, pos=root.pos)
        root.bind(size=lambda i, v: setattr(self._bg, 'size', v),
                  pos=lambda i, v: setattr(self._bg, 'pos', v))

        # ── Board ──────────────────────────────────────────
        self.board = BoardWidget(size_hint=(1, 0.58))
        root.add_widget(self.board)

        # ── Player info cards ──────────────────────────────
        cards_row = GridLayout(cols=2, size_hint=(1, None), height=dp(70),
                                padding=[dp(8), dp(4)], spacing=dp(8))

        self.p1_card = self._make_player_card(C_P1)
        self.p2_card = self._make_player_card(C_P2)
        cards_row.add_widget(self.p1_card['root'])
        cards_row.add_widget(self.p2_card['root'])
        root.add_widget(cards_row)

        # ── Dice + Roll button row ─────────────────────────
        dice_row = BoxLayout(orientation='horizontal', size_hint=(1, None),
                              height=dp(72), padding=[dp(12), dp(4)], spacing=dp(12))

        self.dice = DiceWidget(size_hint=(None, 1), width=dp(64))
        dice_row.add_widget(self.dice)

        self.roll_btn = Button(
            text='🎲  Roll Dice',
            font_size=sp(18), bold=True,
            background_color=C_ACCENT,
            color=(0.08, 0.07, 0.06, 1),
            border=(0, 0, 0, 0),
        )
        self.roll_btn.bind(on_press=self.do_roll)
        dice_row.add_widget(self.roll_btn)
        root.add_widget(dice_row)

        # ── Log / status ───────────────────────────────────
        self.log_label = Label(
            text='Game started! Player 1 goes first.',
            font_size=sp(13), color=C_MUTED,
            size_hint=(1, None), height=dp(48),
            halign='center', valign='middle',
            padding=[dp(12), 0],
        )
        self.log_label.bind(size=self.log_label.setter('text_size'))
        root.add_widget(self.log_label)

        # ── Back button ────────────────────────────────────
        back_btn = Button(
            text='← New Game', font_size=sp(13),
            background_color=C_SURFACE,
            color=C_MUTED, size_hint=(1, None), height=dp(40),
            border=(0, 0, 0, 0),
        )
        back_btn.bind(on_press=self.go_back)
        root.add_widget(back_btn)

        self.add_widget(root)

    def _make_player_card(self, color):
        root_layout = BoxLayout(orientation='vertical', padding=[dp(10), dp(6)], spacing=dp(2))
        with root_layout.canvas.before:
            clr = Color(*C_CARD)
            rect = RoundedRectangle(size=root_layout.size, pos=root_layout.pos, radius=[dp(8)])
            bclr = Color(*color, 0.5)
            brect = Line(rounded_rectangle=[*root_layout.pos, *root_layout.size, dp(8)], width=dp(1))
        root_layout.bind(
            size=lambda i, v: (setattr(rect, 'size', v), setattr(brect, 'rounded_rectangle', [*i.pos, *v, dp(8)])),
            pos=lambda i, v: (setattr(rect, 'pos', v), setattr(brect, 'rounded_rectangle', [*v, *i.size, dp(8)])),
        )
        name_lbl = Label(text='Player', font_size=sp(12), color=color,
                          bold=True, halign='left', valign='middle',
                          size_hint_y=None, height=dp(20))
        name_lbl.bind(size=name_lbl.setter('text_size'))
        pos_lbl = Label(text='Square 1', font_size=sp(20), color=C_TEXT,
                         halign='left', valign='middle',
                         size_hint_y=None, height=dp(30))
        pos_lbl.bind(size=pos_lbl.setter('text_size'))
        root_layout.add_widget(name_lbl)
        root_layout.add_widget(pos_lbl)
        return {'root': root_layout, 'name': name_lbl, 'pos': pos_lbl, 'border': brect}

    def setup_players(self, p1_name, p2_name):
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.positions = [1, 1]
        self.current = 0
        self.rolling = False
        self.board.p1_pos = 1
        self.board.p2_pos = 1
        self._refresh_cards()
        self.log_label.text = f'Game ready! {p1_name} goes first.'
        self.roll_btn.disabled = False

    def _refresh_cards(self):
        self.p1_card['name'].text = self.p1_name
        self.p2_card['name'].text = self.p2_name
        self.p1_card['pos'].text = f'Square {self.positions[0]}'
        self.p2_card['pos'].text = f'Square {self.positions[1]}'
        # Highlight active player
        c1 = C_P1 if self.current == 0 else (*C_P1[:3], 0.25)
        c2 = C_P2 if self.current == 1 else (*C_P2[:3], 0.25)
        self.p1_card['name'].color = c1
        self.p2_card['name'].color = c2

    def do_roll(self, *args):
        if self.rolling:
            return
        self.rolling = True
        self.roll_btn.disabled = True
        roll = random.randint(1, 6)
        self.dice.roll_animation(roll, lambda: self._apply_roll(roll))

    def _apply_roll(self, roll):
        pidx = self.current
        from_pos = self.positions[pidx]
        to_pos = min(from_pos + roll, 100)
        name = self.p1_name if pidx == 0 else self.p2_name

        self._animate_move(pidx, from_pos, to_pos, roll, name)

    def _animate_move(self, pidx, from_pos, to_pos, roll, name):
        steps = [from_pos]
        for i in range(from_pos + 1, to_pos + 1):
            steps.append(i)
        step_idx = [0]

        def advance(dt):
            step_idx[0] += 1
            if step_idx[0] < len(steps):
                self.positions[pidx] = steps[step_idx[0]]
                self._update_board_positions()
            else:
                Clock.unschedule(advance)
                self._check_special(pidx, to_pos, roll, name)

        Clock.schedule_interval(advance, 0.12)

    def _check_special(self, pidx, pos, roll, name):
        msg = f'{name} rolled {roll}, moved to {pos}.'

        if pos == 100:
            self.log_label.text = f'🎉 {name} wins!'
            self._show_win(name)
            return

        if pos in LADDERS:
            dest = LADDERS[pos]
            msg += f' 🪜 Ladder! Climbs to {dest}!'
            self.positions[pidx] = dest
            self._update_board_positions()
        elif pos in SNAKES:
            dest = SNAKES[pos]
            msg += f' 🐍 Snake! Slides to {dest}.'
            self.positions[pidx] = dest
            self._update_board_positions()

        self.current = (self.current + 1) % 2
        next_name = self.p1_name if self.current == 0 else self.p2_name
        self.log_label.text = msg
        self._refresh_cards()
        self.rolling = False
        self.roll_btn.disabled = False

    def _update_board_positions(self):
        self.board.p1_pos = self.positions[0]
        self.board.p2_pos = self.positions[1]
        self.p1_card['pos'].text = f'Square {self.positions[0]}'
        self.p2_card['pos'].text = f'Square {self.positions[1]}'

    def _show_win(self, winner_name):
        from kivy.uix.popup import Popup
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(16))
        with content.canvas.before:
            Color(*C_CARD)
            Rectangle(size=content.size, pos=content.pos)

        emoji_lbl = Label(text='🏆', font_size=sp(48), size_hint_y=None, height=dp(60))
        title_lbl = Label(text=f'{winner_name} Wins!', font_size=sp(24),
                           bold=True, color=C_ACCENT, size_hint_y=None, height=dp(40))
        sub_lbl = Label(text='Congratulations on reaching Square 100!',
                         font_size=sp(13), color=C_MUTED,
                         size_hint_y=None, height=dp(36), halign='center')
        sub_lbl.bind(size=sub_lbl.setter('text_size'))

        play_btn = Button(text='Play Again', font_size=sp(16), bold=True,
                           background_color=C_ACCENT, color=(0.08, 0.07, 0.06, 1),
                           size_hint_y=None, height=dp(50), border=(0, 0, 0, 0))

        content.add_widget(emoji_lbl)
        content.add_widget(title_lbl)
        content.add_widget(sub_lbl)
        content.add_widget(play_btn)

        popup = Popup(
            title='', content=content,
            size_hint=(0.82, None), height=dp(300),
            background_color=C_CARD,
            separator_height=0,
        )

        def restart(_):
            popup.dismiss()
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'setup'

        play_btn.bind(on_press=restart)
        popup.open()

    def go_back(self, *args):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'setup'


# ── App ──────────────────────────────────────────────────────────────────────────
class SnakeLaddersApp(App):
    def build(self):
        Window.clearcolor = C_BG
        sm = ScreenManager()
        sm.add_widget(SetupScreen(name='setup'))
        sm.add_widget(GameScreen(name='game'))
        return sm


if __name__ == '__main__':
    SnakeLaddersApp().run()
