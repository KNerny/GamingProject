import arcade as ar
from PIL import Image, ImageDraw
from arcade import View
from arcade.gui import UIManager, UIFlatButton, UILabel, UIDropdown, UISlider, UITextureButton
from pyglet.event import EVENT_HANDLE_STATE

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
VOLUME = 100
FULL_SCREEN = False
TITLE = 'Game'  # Потом заменить имя приложения


class OptionsScene(ar.View):
    def __init__(self, window):
        super().__init__(window, ar.color.BLUE_SAPPHIRE) # Поменять цвет на фон
        self.window = window
        self.manager = UIManager()
        self.manager.enable()
        scale = window.width / 800
        options_label = UILabel(
            text='Настройки',
            x=200 * scale,
            y=459 * scale,
            height=81 * scale,
            width=400 * scale,
            font_size=30 * scale,
            align='center',
            text_color=ar.color.WHITE
        )
        volume_label = UILabel(
            text='Громкость звука',
            x=160 * scale,
            y=450 * scale,
            height=20 * scale,
            width=171 * scale,
            font_size=20 * scale,
            align='left',
            text_color=ar.color.WHITE
        )
        resolution_label = UILabel(
            text='Разрешение',
            x=160 * scale,
            y=360 * scale,
            height=20 * scale,
            width=171 * scale,
            font_size=20 * scale,
            align='left',
            text_color=ar.color.WHITE
        )
        full_screen_label = UILabel(
            text='Полный экран',
            x=160 * scale,
            y=270 * scale,
            height=20 * scale,
            width=171 * scale,
            font_size=20 * scale,
            align='left',
            text_color=ar.color.WHITE
        )
        self.slider_label = UILabel(
            text='100',
            x=544 * scale,
            y=460 * scale,
            height=21 * scale,
            width=16 * scale,
            font_size=10 * scale,
            align='left',
            text_color=ar.color.WHITE
        )
        self.slider = UISlider(
            value=100,
            x=464 * scale,
            y=430 * scale,
            width=171 * scale,
            height=22 * scale,
            min_value=0,
            max_value=100,
            step=1
        )
        self.resolution_button = UIDropdown(
            x=464 * scale,
            y=360 * scale,
            width=171 * scale,
            height=22 * scale,
            options=[
                '800:600',
                '1600:900',
                '1920:1080',
                '2560:1440',
                '3840:2160'
            ],
            default=f'{SCREEN_WIDTH}:{SCREEN_HEIGHT}'
        )
        self.full_screen_button = UIDropdown(
            x=530 * scale,
            y=270 * scale,
            width=40 * scale,
            height=20 * scale,
            options=[
                'Да',
                'Нет'
            ],
            default='Нет'
        )
        self.slider.on_change = self.volume_change
        self.resolution_button.on_change = self.resolution_change
        self.full_screen_button.on_change = self.full_screen_change
        self.manager.add(options_label)
        self.manager.add(resolution_label)
        self.manager.add(volume_label)
        self.manager.add(full_screen_label)
        self.manager.add(self.slider_label)
        self.manager.add(self.slider)
        self.manager.add(self.full_screen_button)
        self.manager.add(self.resolution_button)

    def on_draw(self) -> bool | None:
        self.clear()
        self.manager.draw()
        return

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == ar.key.ESCAPE:
            self.window.show_view(self.window.sub_view)
        return

    def volume_change(self, event):
        global VOLUME
        VOLUME = int(self.slider.value)
        self.slider_label.text = str(VOLUME)

    def resolution_change(self, event):
        global SCREEN_HEIGHT, SCREEN_WIDTH
        SCREEN_WIDTH, SCREEN_HEIGHT = [int(i) for i in self.resolution_button.value.split(':')]
        self.window.on_resize(0, 0)

    def full_screen_change(self, event):
        self.window.set_fullscreen(self.full_screen_button.value == 'ДА')


class FirstScene(ar.View):
    def __init__(self, window):
        super().__init__(window, ar.color.BLUE_SAPPHIRE) # Поменять цвет на фон
        self.manager = UIManager()
        self.manager.enable()
        main_menu_label = UILabel(
            text="Главное Меню",
            font_size=30,
            text_color=ar.color.WHITE,
            width=400,
            align="center",
            x=200,
            y=520
        )
        play_button = UIFlatButton(
            x=285,
            y=360,
            text='Играть',
            width=230,
            height=31
        )
        options_button = UIFlatButton(
            x=285,
            y=300,
            text='Настройки',
            width=230,
            height=31
        )
        autors_button = UIFlatButton(
            x=285,
            y=240,
            text='Авторы',
            width=230,
            height=31
        )
        exit_button = UIFlatButton(
            x=285,
            y=180,
            text='Выйти',
            width=230,
            height=31
        )
        exit_button.on_click = self.exit
        options_button.on_click = self.options
        self.manager.add(main_menu_label)
        self.manager.add(play_button)
        self.manager.add(options_button)
        self.manager.add(autors_button)
        self.manager.add(exit_button)

    def on_draw(self) -> bool | None:
        self.clear()
        self.manager.draw()
        return

    def exit(self, event):
        self.window.close()

    def options(self, event):
        self.window.show_view_new(self.window.options_view)


class Game(ar.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, resizable=True)
        self.first_scene = FirstScene(self)
        self.options_view = OptionsScene(self)
        self.show_view_new(self.first_scene)
        self.sub_view = self.first_scene
        self.on_resize_old = self.on_resize

    def on_resize(self, width: int, height: int) -> EVENT_HANDLE_STATE:
        self.on_resize_old(SCREEN_WIDTH, SCREEN_HEIGHT)

    def show_view_new(self, new_view: View) -> None:
        self.sub_view = self.view
        self.show_view(new_view)


game = Game()
game.run()