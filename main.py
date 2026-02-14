import random
import arcade
import io
import arcade as ar
from PIL import Image, ImageDraw
from arcade import View
from arcade.gui import UIManager, UIFlatButton, UILabel, UIDropdown, UISlider, UITextureButton
from pyglet.event import EVENT_HANDLE_STATE
screen_width = 800
screen_height = 600
volume = 100
full_screen = False
TITLE = 'The Underworld'  # Потом заменить имя приложения


class OptionsScene(ar.View):
    def __init__(self, window):
        super().__init__(window, ar.color.BLUE_SAPPHIRE)  # Поменять цвет на фон
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
        self.exit_button.on_click = self.escape
        self.manager.add(options_label)
        self.manager.add(resolution_label)
        self.manager.add(volume_label)
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

    def volume_change(self, event):
        global volume
        volume = int(self.slider.value)
        self.slider_label.text = str(volume)

    def resolution_change(self, event):
        import screeninfo
        global screen_height, screen_width
        self.scale_x, self.scale_y = ([int(i) for i in self.resolution_button.value.split(':')][0] / screen_width,
                                      [int(i) for i in self.resolution_button.value.split(':')][1] / screen_height)
        screen_width, screen_height = [int(i) for i in self.resolution_button.value.split(':')]
        self.window.set_fullscreen(False)
        self.window.set_size(screen_width, screen_height)
        self.window.options_view = OptionsScene(self.window)
        self.window.show_view(self.window.options_view)
        monitor = screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height
        self.window.set_location(monitor[0] // 2 - screen_width // 2, monitor[1] // 2 - screen_height // 2)
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

    def on_hide(self):
        """Вызывается когда сцена скрывается"""
        self.manager.disable()
        self.manager.clear()

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


class Bullet(arcade.Sprite):
    def __init__(self, texture: arcade.Texture, start_x: float, start_y: float, facing_right: bool, speed: float = 500):
        super().__init__(texture, scale=1.0)
        self.center_x = start_x + 20
        self.center_y = start_y + 25
        self.speed = speed
        self.max_distance = 500  # Максимальная дистанция полёта
        self.start_x = start_x + 20  # Запоминаем стартовую позицию

        if facing_right:
            self.change_x = self.speed  # летит вправо
            self.angle = 0
        else:
            self.change_x = -self.speed  # летит влево
            self.angle = 180

        self.change_y = 0

    def update(self, delta_time: float):
        self.center_x += self.change_x * delta_time

        # Проверяем, пролетела ли пуля максимальную дистанцию
        if abs(self.center_x - self.start_x) >= self.max_distance:
            self.remove_from_sprite_lists()


class Player(arcade.Sprite):
    def __init__(self, x, y, scale=1.5):
        super().__init__(scale=scale)
        self.center_x = x
        self.center_y = y

        # --- Стояние с прозрачным фоном ---
        stand_image = Image.open("images_for_game/PMCStand.bmp").convert("RGBA")

        # ---- делаем белый цвет прозрачным ----
        datas = stand_image.getdata()
        newData = []
        for item in datas:
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        stand_image.putdata(newData)

        # превращаем в texture для arcade
        buf = io.BytesIO()
        stand_image.save(buf, format="PNG")
        buf.seek(0)
        self.stand_texture = arcade.load_texture(buf)
        self.texture = self.stand_texture

        # --- Бег (GIF → два списка текстур: вправо и влево) ---
        self.run_textures_right = []
        self.run_textures_left = []

        gif = Image.open("images_for_game/KahkisRun.gif")
        for i in range(gif.n_frames):
            gif.seek(i)
            frame = gif.convert("RGBA")

            # ---- делаем белый цвет прозрачным ----
            datas = frame.getdata()
            newData = []
            for item in datas:
                # если почти белый, делаем прозрачным
                if item[0] > 240 and item[1] > 240 and item[2] > 240:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)
            frame.putdata(newData)

            # обычный кадр (вправо)
            buf = io.BytesIO()
            frame.save(buf, format="PNG")
            buf.seek(0)
            tex_right = arcade.load_texture(buf)
            self.run_textures_right.append(tex_right)

            # зеркальный кадр (влево)
            frame_left = frame.transpose(Image.FLIP_LEFT_RIGHT)
            buf_left = io.BytesIO()
            frame_left.save(buf_left, format="PNG")
            buf_left.seek(0)
            tex_left = arcade.load_texture(buf_left)
            self.run_textures_left.append(tex_left)

        # --- Состояние анимации ---
        self.state = "stand"
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_duration = 100  # мс на кадр

        # --- Направление ---
        self.facing_right = True

    # --- переключение состояния ---
    def run(self):
        self.state = "run"

    def stand(self):
        self.state = "stand"
        if self.facing_right:
            self.texture = self.stand_texture
        else:
            self.texture = self.stand_texture.flip_horizontally()

    # --- обновление анимации ---
    def update_animation(self, delta_time: float):
        if self.state == "run":
            self.frame_timer += delta_time * 1000
            if self.frame_timer >= self.frame_duration:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.run_textures_right)

                # выбираем направление
                if self.facing_right:
                    self.texture = self.run_textures_right[self.current_frame]
                else:
                    self.texture = self.run_textures_left[self.current_frame]

    # --- установка направления ---
    def set_direction(self, right: bool):
        self.facing_right = right
        if self.state == "stand":
            self.stand()


class Enemy(ar.Sprite):
    def __init__(self, x, y):
        super().__init__(center_x=x, center_y=y)
        self.texture = ar.load_texture('1')  # Заменить на имя файла
        self.textures = [ar.load_texture('1') for i in range(1)]  # Заменить имя файла и количество
        self.speed = 1  # Заменить на скорость


class GameView(ar.View):
    def __init__(self, window):
        super().__init__(window)
        from random import randint, random
        self.window = window
        self.window.playing = True
        # Временная камера
        self.camera = ar.camera.Camera2D()

        # ===== СОЛДАТ =====
        self.player = Player(screen_width // 2, screen_height // 2, scale=1.5)
        self.player.center_x = screen_width // 2
        self.player.center_y = screen_height // 2

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # ===== ФИЗИКА =====
        self.moving_left = False
        self.moving_right = False
        self.jump = False
        self.speed = 200
        self.is_jumping = False
        self.vertical_speed = 0
        self.gravity = 1000
        self.jump_strength = 400

        # ===== ПУЛИ =====
        self.bullet_list = arcade.SpriteList()
        try:
            self.bullet_texture = arcade.load_texture("images_for_game/bullet.png")
        except FileNotFoundError:
            print("Файл images_for_game/bullet.png не найден.")
            self.bullet_texture = None


        self.world = [[None] * 80 for _ in range(15)]
        self.ground = 4
        self.mud_block = ar.load_texture('textures/blocks/mud_block.png')
        self.betone_block = ar.load_texture('textures/blocks/betone_block.png')
        self.down_to_right_tube = ar.load_texture('textures/blocks/down_to_right_tube.png')
        self.left_to_down_tube = ar.load_texture('textures/blocks/left_to_down_tube.png')
        self.left_tube = ar.load_texture('textures/blocks/left_tube.png')
        self.gor_tube = ar.load_texture('textures/blocks/gor_tube.png')
        self.right_tube = ar.load_texture('textures/blocks/right_tube.png')
        self.blocks = ar.SpriteList()
        for i in range(self.ground):
            for j in range(80):
                self.world[14 - i][j] = self.mud_block
        for j in range(80):
            i = self.ground
            self.world[14 - i][j] = self.betone_block
        self.hills = ((randint(0, 9), randint(30, 39)), (randint(40, 49), randint(70, 79)))
        self.hills1 = []
        a = randint(1, 2)
        for i in range(a):
            if i:
                self.hills1.append(tuple(sorted((randint((self.hills[0][1] - self.hills[0][0]) // a + \
                                                         self.hills[0][0] - 1, self.hills[0][1] - 1),
                                                 randint((self.hills[0][1] - self.hills[0][0]) // a + \
                                                         self.hills[0][0] - 1, self.hills[0][1] - 1)))))
            else:
                self.hills1.append(tuple(sorted((randint(self.hills[0][0] + 1,
                                                         (self.hills[0][1] - self.hills[0][0]) // a + \
                                                         self.hills[0][0] - 1),
                                                 randint(self.hills[0][0] + 1,
                                                         (self.hills[0][1] - self.hills[0][0]) // a + \
                                                         self.hills[0][0] - 1)))))
        a = randint(1, 2)
        for i in range(a):
            if i:
                self.hills1.append(tuple(sorted((randint((self.hills[1][1] - self.hills[1][0]) // a + \
                                                         self.hills[1][0] - 1, self.hills[1][1] - 1),
                                                 randint((self.hills[1][1] - self.hills[1][0]) // a + \
                                                         self.hills[1][0] - 1, self.hills[1][1] - 1)))))
            else:
                self.hills1.append(tuple(sorted((randint(self.hills[1][0] + 1,
                                                         (self.hills[1][1] - self.hills[1][0]) // a + \
                                                         self.hills[1][0] - 1),
                                                 randint(self.hills[1][0] + 1,
                                                         (self.hills[1][1] - self.hills[1][0]) // a + \
                                                         self.hills[1][0] - 1)))))
        self.hills1 = tuple(self.hills1)
        self.hills2 = []
        for i in self.hills1:
            if i[1] - i[0] < 3:
                continue
            if random() <= 0.7:
                self.hills2.append(tuple(sorted((randint(i[0] + 1, i[1]), randint(i[0] + 1, i[1])))))
        self.hills2 = tuple(self.hills2)
        for i in self.hills:
            for j in range(i[0], i[1] + 1):
                if self.hills1[self.hills.index(i)][0] <= j <= self.hills1[self.hills.index(i)][1]:
                    self.world[14 - self.ground - 1][j] = self.mud_block
                else:
                    self.world[14 - self.ground - 1][j] = self.betone_block
        for i in self.hills1:
            for j in range(i[0], i[1] + 1):
                self.world[14 - self.ground - 2][j] = self.betone_block

        for i in self.hills2:
            for j in range(i[0], i[1] + 1):
                if j == i[0]:
                    self.world[14 - self.ground - 3][j] = self.down_to_right_tube
                elif j == i[1]:
                    self.world[14 - self.ground - 3][j] = self.left_to_down_tube
                else:
                    self.world[14 - self.ground - 3][j] = self.gor_tube
        for i in range(80):
            for j in self.hills:
                if j[0] <= i <= j[1]:
                    self.world[14 - self.ground][i] = self.mud_block
        for i in range(80):
            for j in self.hills1:
                if j[0] <= i <= j[1]:
                    self.world[14 - self.ground - 1][i] = self.mud_block
        for i in range(15):
            for j in range(80):
                if self.world[i][j] is not None:
                    sprite = ar.Sprite(center_x=(j + 1) * (40 * screen_width / 800) - (20 * screen_width / 800),
                                       center_y=(15 - i) * (40 * screen_width / 800) - (20 * screen_width / 800) + (
                                               screen_height - 600 * (screen_width / 800)),
                                       scale=(screen_width / 800 * 40) / 64)
                    sprite.texture = self.world[i][j]
                    self.world[i][j] = sprite
                    self.blocks.append(sprite)

    # ===== ОТРИСОВКА =====
    def on_draw(self) -> bool | None:
        self.clear()
        self.camera.use()
        self.blocks.draw()  # Мир
        self.player_list.draw()  # Солдат
        self.bullet_list.draw()  # Пули
        return True

    # ===== ОБНОВЛЕНИЕ =====
    def on_update(self, delta_time: float) -> bool | None:
        # Движение влево-вправо
        if self.moving_left:
            self.player.center_x -= self.speed * delta_time
            self.player.set_direction(False)
        if self.moving_right:
            self.player.center_x += self.speed * delta_time
            self.player.set_direction(True)

        # Анимация бега/стояния
        if self.moving_left or self.moving_right:
            self.player.run()
        else:
            self.player.stand()

        # Физика прыжка
        self.vertical_speed -= self.gravity * delta_time
        self.player.center_y += self.vertical_speed * delta_time

        collisions = self.player.collides_with_list(self.blocks)
        if collisions and self.vertical_speed < 0:  # Падаем вниз
            # Находим самый верхний блок, с которым столкнулись
            highest_block = max(collisions, key=lambda b: b.center_y)
            # Ставим игрока на блок
            self.player.center_y = highest_block.center_y + highest_block.height / 2 + self.player.height / 2
            self.vertical_speed = 0
            self.is_jumping = False

        # Прыжок
        if self.jump and not self.is_jumping:
            self.vertical_speed = self.jump_strength
            self.is_jumping = True

        # Простая проверка пола (на уровне земли)
        if self.player.center_y <= self.player.height / 2:
            self.player.center_y = self.player.height / 2
            self.vertical_speed = 0
            self.is_jumping = False

        # Анимация солдата
        self.player_list.update_animation(delta_time)

        # Обновление пуль
        self.bullet_list.update(delta_time)

        # Удаление пуль за экраном

        # Обновление камеры - следует за игроком
        target_x = self.player.center_x
        target_y = self.player.center_y
        self.camera.position = (
            self.camera.position[0] + (target_x - self.camera.position[0]) * 0.1,
            self.camera.position[1] + (target_y - self.camera.position[1]) * 0.1
        )

        return True

    # ===== НАЖАТИЕ КЛАВИШ =====
    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == ar.key.ESCAPE:
            self.window.show_view_new(FirstScene(self.window))
        elif symbol == arcade.key.A:
            self.moving_left = True
            self.player.set_direction(False)
        elif symbol == arcade.key.D:
            self.moving_right = True
            self.player.set_direction(True)
        elif symbol == arcade.key.SPACE:
            self.jump = True
        return True

    # ===== ОТПУСКАНИЕ КЛАВИШ =====
    def on_key_release(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.A:
            self.moving_left = False
            self.player.set_direction(False)
        elif symbol == arcade.key.D:
            self.moving_right = False
            self.player.set_direction(True)
        elif symbol == arcade.key.SPACE:
            self.jump = False
        return True

    # ===== НАЖАТИЕ МЫШИ =====
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):

        if button == arcade.MOUSE_BUTTON_LEFT and self.bullet_texture:
            bullet = Bullet(
                texture=self.bullet_texture,
                start_x=self.player.center_x,
                start_y=self.player.center_y,
                facing_right=self.player.facing_right,
                speed=600
            )
            self.bullet_list.append(bullet)

class FirstScene(ar.View):
    def __init__(self, window):
        super().__init__(window, ar.color.BLUE_SAPPHIRE)  # Поменять цвет на фон\
        global screen_height, screen_width
        self.scale_x, self.scale_y = screen_width / 800, screen_height / 600
        self.manager = UIManager()
        self.manager.enable()
        main_menu_label = UILabel(
            text=TITLE,
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
        play_button.on_click = self.play
        self.manager.add(main_menu_label)
        self.manager.add(play_button)
        self.manager.add(options_button)
        self.manager.add(autors_button)
        self.manager.add(exit_button)

    def on_draw(self) -> bool | None:
        self.clear()
        self.manager.draw()
        return

    def on_hide(self):
        """Вызывается когда сцена скрывается"""
        self.manager.disable()
        self.manager.clear()

    def exit(self, event):
        self.window.close()

    def options(self, event):
        self.window.options_view = OptionsScene(self.window)
        self.window.show_view_new(self.window.options_view)

    def autors(self, event):
        self.window.show_view_new(AutorsScene(self.window))

    def play(self, event):
        self.window.show_view_new(GameView(self.window))

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == ar.key.ESCAPE:
            if self.window.playing:
                self.window.show_view_new(GameView(self.window))
                return True
            self.exit(1)
        return True


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

    def on_hide(self):
        """Вызывается когда сцена скрывается"""
        self.manager.disable()
        self.manager.clear()


class Game(ar.Window):

    def __init__(self):
        super().__init__(screen_width, screen_height, TITLE)
        arcade.set_background_color(arcade.color.TEA_GREEN)

        self.playing = False
        self.first_scene = FirstScene(self)
        self.options_view = OptionsScene(self)
        self.sub_view = self.first_scene.__class__
        self.pres_view = self.first_scene.__class__

        self.show_view(self.first_scene)
        self.on_resize_old = self.on_resize

    def show_view_new(self, new_view: View) -> None:
        """Кастомный метод для смены вида"""
        self.sub_view = self.pres_view
        self.pres_view = new_view.__class__
        self.show_view(new_view)


if __name__ == '__main__':
    game = Game()
    game.run()
