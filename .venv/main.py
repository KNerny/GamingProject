import arcade as ar
from arcade.gui import UIManager, UIFlatButton, UILabel

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class FirstScene(ar.View):
    def __init__(self, window):
        super().__init__(window, ar.color.BLUE_SAPPHIRE)
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
        self.manager.add(main_menu_label)
        play_button = UIFlatButton(
            x=285,
            y=360,
            text='Играть',
            width=230,
            height=31
        )
        self.manager.add(play_button)
        options_button = UIFlatButton(
            x=285,
            y=300,
            text='Настройки',
            width=230,
            height=31
        )
        self.manager.add(options_button)
        autors_button = UIFlatButton(
            x=285,
            y=240,
            text='Авторы',
            width=230,
            height=31
        )
        self.manager.add(autors_button)
        exit_button = UIFlatButton(
            x=285,
            y=180,
            text='Выйти',
            width=230,
            height=31
        )
        exit_button.on_click = self.exit
        self.manager.add(exit_button)

    def on_draw(self) -> bool | None:
        self.clear()
        self.manager.draw()
        return

    def exit(self, event):
        self.window.close()


class Game(ar.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, 'Game', )  # Потом заменить имя приложения
        self.first_scene = FirstScene(self)
        self.show_view(self.first_scene)


game = Game()
game.run()
