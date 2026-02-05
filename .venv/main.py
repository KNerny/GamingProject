import random

import arcade as ar
from PIL import Image, ImageDraw
from PIL.ImageOps import scale
from arcade import View
from arcade.gui import UIManager, UIFlatButton, UILabel, UIDropdown, UISlider, UITextureButton
from pyglet.event import EVENT_HANDLE_STATE

screen_width = 800
screen_height = 600
volume = 100
full_screen = False
TITLE = 'Game'  # Потом заменить имя приложения


class OptionsScene(ar.View):
    def __init__(self, window):
        super().__init__(window, ar.color.BLUE_SAPPHIRE)# Поменять цвет на фон
        global screen_width, screen_height
        self.scale_x, self.scale_y = screen_width / 800, screen_height / 600
        self.window = window
        self.manager = UIManager()
        self.manager.enable()
        options_label = UILabel(
            text='Настройки',
            x=200 * self.scale_x,
            y=459 * self.scale_y,
            height=81 * self.scale_x,
            width=400 * self.scale_y,
            font_size=30 * self.scale_y,
            align='center',
            text_color=ar.color.WHITE
        )
        volume_label = UILabel(
            text='Громкость звука',
            x=160 * self.scale_x,
            y=450 * self.scale_y,
            height=20 * self.scale_x,
            width=171 * self.scale_y,
            font_size=20 * self.scale_y,
            align='left',
            text_color=ar.color.WHITE
        )
        self.main_button = UIFlatButton(
            text='Выйти в главное меню',
            x=50 * scale,
            y=200 * scale,
            height=40,
            width=250,
            font_size=20 * scale,
            align='center',
            text_color=ar.color.WHITE
        )
        self.random_color_background = UIFlatButton(
            text='Сменить цвет фона',
            x=350 * scale,
            y=200 * scale,
            height=40,
            width=160,
            font_size=20 * scale,
            align='center',
            text_color=ar.color.WHITE,
        )
        self.set_default_color = UIFlatButton(
            text='Начальный фон',
            x=600 * scale,
            y=200 * scale,
            height=40,
            width=150,
            font_size=20 * scale,
            align='center',
            text_color=ar.color.WHITE
        )
        resolution_label = UILabel(
            text='Разрешение',
            x=160 * self.scale_x,
            y=360 * self.scale_y,
            height=20 * self.scale_x,
            width=171 * self.scale_y,
            font_size=20 * self.scale_y,
            align='left',
            text_color=ar.color.WHITE
        )
        full_screen_label = UILabel(
            text='Полный экран',
            x=160 * self.scale_x,
            y=270 * self.scale_y,
            height=20 * self.scale_x,
            width=171 * self.scale_y,
            font_size=20 * self.scale_y,
            align='left',
            text_color=ar.color.WHITE
        )
        self.slider_label = UILabel(
            text=str(volume),
            x=544 * self.scale_x,
            y=460 * self.scale_y,
            height=21 * self.scale_x,
            width=16 * self.scale_y,
            font_size=10 * self.scale_y,
            align='left',
            text_color=ar.color.WHITE
        )
        self.slider = UISlider(
            value=volume,
            x=464 * self.scale_x,
            y=430 * self.scale_y,
            width=171 * self.scale_x,
            height=22 * self.scale_y,
            min_value=0,
            max_value=100,
            step=1
        )
        self.resolution_button = UIDropdown(
            x=464 * self.scale_x,
            y=360 * self.scale_y,
            width=171 * self.scale_x,
            height=22 * self.scale_y,
            options=[
                '800:600',
                '1600:900',
                '1920:1080',
                '2560:1440',
                '3840:2160'
            ],
            default=f'{screen_width}:{screen_height}',
            font_size=20 * self.scale_y
        )
        self.full_screen_button = UIDropdown(
            x=530 * self.scale_x,
            y=270 * self.scale_y,
            width=40 * self.scale_x,
            height=20 * self.scale_y,
            options=[
                'Да',
                'Нет'
            ],
            default=str('Да' if self.window.fullscreen else 'Нет'),
            font_size=20 * self.scale_y
        )
        self.exit_button = UIFlatButton(
            x=314 * self.scale_x,
            y=150 * self.scale_y,
            width=171 * self.scale_x,
            height=22 * self.scale_y,
            text='Назад'
        )
        self.slider.on_change = self.volume_change
        self.resolution_button.on_change = self.resolution_change
        self.full_screen_button.on_change = self.full_screen_change
        self.main_button.on_click = self.go_to_main_menu
        self.random_color_background.on_click = self.set_random_color
        self.set_default_color.on_click = self.set_color_default
        self.exit_button.on_click = self.escape
        self.manager.add(options_label)
        self.manager.add(self.set_default_color)
        self.manager.add(resolution_label)
        self.manager.add(volume_label)
        self.manager.add(self.random_color_background)
        self.manager.add(self.main_button)
        self.manager.add(full_screen_label)
        self.manager.add(self.slider_label)
        self.manager.add(self.slider)
        self.manager.add(self.full_screen_button)
        self.manager.add(self.resolution_button)
        self.manager.add(self.exit_button)
        self.ui = [
            options_label,
            resolution_label,
            full_screen_label,
            volume_label,
            self.slider_label,
            self.slider,
            self.full_screen_button,
            self.resolution_button,
            self.exit_button
        ]

    def on_draw(self) -> bool | None:
        self.clear()
        self.manager.draw()
        return

    def escape(self, event):
        self.window.show_view_new(self.window.sub_view(self.window))

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == ar.key.ESCAPE:
            self.window.show_view_new(self.window.sub_view(self.window))
        return True

    def set_color_default(self, event):
        self.background_color = ar.color.BLUE_SAPPHIRE

    def volume_change(self, event):
        global volume
        volume = int(self.slider.value)
        self.slider_label.text = str(volume)

    def set_random_color(self, event):
        self.background_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def resolution_change(self, event):
        global screen_height, screen_width
        self.scale_x, self.scale_y = ([int(i) for i in self.resolution_button.value.split(':')][0] / screen_width,
                                      [int(i) for i in self.resolution_button.value.split(':')][1] / screen_height)
        screen_width, screen_height = [int(i) for i in self.resolution_button.value.split(':')]
        self.window.set_fullscreen(False)
        self.window.set_size(screen_width, screen_height)
        self.window.options_view = OptionsScene(self.window)
        self.window.show_view(self.window.options_view)
        '''return
        global screen_height, screen_width
        self.scale_x, self.scale_y = ([int(i) for i in self.resolution_button.value.split(':')][0] / screen_width,
                                      [int(i) for i in self.resolution_button.value.split(':')][1] / screen_height)
        screen_width, screen_height = [int(i) for i in self.resolution_button.value.split(':')]
        self.window.set_size(screen_width, screen_height)
        for i in self.ui:
            x, y = i.center_x, i.center_y
            i.resize(width=i.size[0] * self.scale_x, height=i.size[1] * self.scale_y)
            i.move(x * self.scale_x - x, y * self.scale_y - y)
            try:
                i.font_size = i.font_size * self.scale
            except Exception:
                pass'''

    def go_to_main_menu(self, event):
        self.window.show_view_new(self.window.first_scene)

    def full_screen_change(self, event):
        global screen_height, screen_width
        import screeninfo
        if self.full_screen_button.value == 'Да':
            self.window.pre_size = screen_width, screen_height
            screen_width, screen_height = screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height
        else:
            screen_width, screen_height = self.window.pre_size
        self.window.set_fullscreen(self.full_screen_button.value == 'Да')
        self.window.options_view = OptionsScene(self.window)
        self.window.show_view(self.window.options_view)
        if not self.window.fullscreen:
            self.window.set_size(screen_width, screen_height)
        '''return
        global screen_height, screen_width
        import screeninfo
        self.scale_x, self.scale_y = (screeninfo.get_monitors()[0].width / screen_width,
                                      screeninfo.get_monitors()[0].height / screen_height)
        screen_width, screen_height = screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height
        self.window.set_size(screen_width, screen_height)
        for_delete = []
        for i in self.ui:
            x, y = i.center_x, i.center_y
            i.resize(width=i.size[0] * self.scale_x, height=i.size[1] * self.scale_y)
            i.move(x * self.scale_x - x, y * self.scale_y - y)
            if i is UILabel:
                self.manager.remove(i)
                for_delete.append(i)
                self.manager.add(UILabel(
                    text=i.text,
                    x=i.center_x,
                    y=i.center_y,
                    width=i.width,
                    height=i.height,
                    font_size=i.font_size * self.scale_y
                ))
        for i in for_delete:
            self.ui.remove(i)
        self.window.set_fullscreen(self.full_screen_button.value == 'Да')'''


class FirstScene(ar.View):
    def __init__(self, window):
        super().__init__(window, ar.color.BLUE_SAPPHIRE) # Поменять цвет на фон\
        global screen_height, screen_width
        self.scale_x, self.scale_y = screen_width / 800, screen_height / 600
        self.manager = UIManager()
        self.manager.enable()
        main_menu_label = UILabel(
            text="Главное Меню",
            font_size=30 * self.scale_y,
            text_color=ar.color.WHITE,
            width=400 * self.scale_x,
            align="center",
            x=200 * self.scale_x,
            y=520 * self.scale_y
        )
        play_button = UIFlatButton(
            x=285 * self.scale_x,
            y=360 * self.scale_y,
            text='Играть',
            width=230 * self.scale_x,
            height=31 * self.scale_y
        )
        options_button = UIFlatButton(
            x=285 * self.scale_x,
            y=300 * self.scale_y,
            text='Настройки',
            width=230 * self.scale_x,
            height=31 * self.scale_y
        )
        autors_button = UIFlatButton(
            x=285 * self.scale_x,
            y=240 * self.scale_y,
            text='Авторы',
            width=230 * self.scale_x,
            height=31 * self.scale_y
        )
        exit_button = UIFlatButton(
            x=285 * self.scale_x,
            y=180 * self.scale_y,
            text='Выйти',
            width=230 * self.scale_x,
            height=31 * self.scale_y
        )
        exit_button.on_click = self.exit
        options_button.on_click = self.options
        autors_button.on_click = self.autors
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
        self.window.options_view = OptionsScene(self.window)
        self.window.show_view_new(self.window.options_view)

    def autors(self, event):
        self.window.show_view_new(AutorsScene(self.window))


class AutorsScene(ar.View):
    def __init__(self, window):
        super().__init__(window)
        from random import choice, randint
        self.window = window
        global screen_height, screen_width
        self.scale_x, self.scale_y = screen_width / 800, screen_height / 600
        self.background_color = ar.color.BLUE_SAPPHIRE
        self.manager = UIManager(window)
        self.manager.enable()
        self.autors_label = UILabel(
            x=randint(50, 750) * self.scale_x,
            y=randint(50, 550) * self.scale_y,
            width=400 * self.scale_x,
            height=50 * self.scale_y,
            text='Авторы',
            align='center',
            font_size=40 * self.scale_y
        )
        self.first_autor_label = UILabel(
            x=randint(50, 750) * self.scale_x,
            y=randint(50, 550) * self.scale_y,
            width=400 * self.scale_x,
            height=50 * self.scale_y,
            text='Tim',
            align='center',
            font_size=25 * self.scale_y
        )
        self.second_autor_label = UILabel(
            x=randint(50, 750) * self.scale_x,
            y=randint(50, 550) * self.scale_y,
            width=400 * self.scale_x,
            height=50 * self.scale_y,
            text='Ner',
            align='center',
            font_size=25 * self.scale_y
        )
        self.second_autor_label.dirr = [choice((-1, 1)), choice((-1, 1))]
        self.first_autor_label.dirr = [choice((-1, 1)), choice((-1, 1))]
        self.autors_label.dirr = [choice((-1, 1)), choice((-1, 1))]
        self.ui = [
            self.autors_label,
            self.second_autor_label,
            self.first_autor_label
        ]
        self.manager.add(self.autors_label)
        self.manager.add(self.first_autor_label)
        self.manager.add(self.second_autor_label)

    def on_draw(self) -> bool | None:
        from random import randint
        import time
        self.clear()
        self.manager.draw()

    def on_update(self, delta_time: float) -> bool | None:
        from random import randint
        for i in self.ui:
            i.move(randint(0, 20) * self.scale_x * i.dirr[0] * delta_time * 60,
                   randint(0, 20) * self.scale_y * i.dirr[1] * delta_time * 60)
            if 0 >= i.center_x:
                i.dirr[0] = 1
            if i.center_x >= screen_width:
                i.dirr[0] = -1
            if 0 >= i.center_y:
                i.dirr[1] = 1
            if i.center_y >= screen_height:
                i.dirr[1] = -1

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == ar.key.ESCAPE:
            self.window.show_view_new(self.window.sub_view(self.window))
        return True


class Game(ar.Window):

    def __init__(self):
        super().__init__(screen_width, screen_height, TITLE)
        self.first_scene = FirstScene(self)
        self.options_view = OptionsScene(self)
        self.sub_view = self.first_scene.__class__
        self.pres_view = self.first_scene.__class__
        self.show_view_new(self.first_scene)
        self.sub_view = self.first_scene
        self.on_resize_old = self.on_resize

#    def on_resize(self, width: int, height: int) -> EVENT_HANDLE_STATE:
#        self.on_resize_old(SCREEN_WIDTH, SCREEN_HEIGHT)

    def show_view_new(self, new_view: View) -> None:
        self.sub_view = self.pres_view
        self.pres_view = new_view.__class__
        self.show_view(new_view)


if __name__ == '__main__':
    game = Game()
    game.run()