# "C:\py_venv\kivy_venv\scripts\activate"

# konfigurasi untuk open gl dibawah versi 2

'''from kivy import Config
Config.set('graphics', 'multisamples', '0')
import kivy
kivy.require('2.0.0')'''

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.properties import StringProperty

from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.image import Image

class Manager(Screen):
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        # define id dari boxlayout untuk spawn screen
        self.first_screen = self.ids.layout_for_main
        self.second_screen = self.ids.layout_for_content

        # define main screen
        self.main_screen = MainScreen()
        # spawn MainScreen pada startup
        self.first_screen.add_widget(self.main_screen)

        # bind floatbutton
        self.ids.float_btn.bind(on_release = self.goto_content_screen)

    def goto_content_screen(self, *args):
        # define content_screen
        self.content_screen = ContentScreen()
        # spawn content screen
        screen = self.second_screen.add_widget(self.content_screen)

        # animate content screen saat spawn
        anim = Animation(
            my_direct = 1,
            opacity = 1,
            duration = .5,
            t = 'out_circ'
        )
        anim.start(self.content_screen.ids.content_screen_layout)

        # hapus main screen
        def remove_main(*args):
            self.first_screen.remove_widget(self.main_screen)
            # animate back button
            self.content_screen.animate_back_button_on_spawn()
        anim.bind(on_complete = remove_main)

        ######### konfigurasi content screen #########

        def add_star_image_total(num):
            rate = num.split('.')

            for i in range(int(rate[0])):
                star = Image(source = 'assets/star.png',
                    size_hint = (None, None),
                    width = 15,
                    height = 15,
                    pos_hint = {'center_y':.5},
                    allow_stretch = True)

                self.content_screen.ids.rating_star.add_widget(star)

            if len(rate) == 2:
                if rate[1] == '5':
                    half_star = Image(source = 'assets/half star.png',
                        size_hint = (None, None),
                        width = 15,
                        height = 15,
                        pos_hint = {'center_y':.5},
                        allow_stretch = True)

                    self.content_screen.ids.rating_star.add_widget(half_star)

            else:
                pass

        add_star_image_total(self.main_screen.product_rating)

        # set content element
        self.content_screen.ids.content_pict.source = self.main_screen.product_pict_path
        self.content_screen.ids.title_text.text = self.main_screen.title_text
        self.content_screen.ids.type_text.text = self.main_screen.type_text
        self.content_screen.ids.rating.text = self.main_screen.product_rating

        # config floatbutton
        self.ids.float_btn.text = 'Bagikan'
        self.ids.float_btn.icon = 'assets/share.png'

        # unbind floatbutton
        self.ids.float_btn.unbind(on_release = self.goto_content_screen)

    def goto_main_screen(self, *args):
        # animate back button
        anim2 = self.content_screen.animate_back_button_on_disapear()

        try:
            screen = self.first_screen.add_widget(self.main_screen)
        except:
            pass

        # animate content screen saat disapear
        anim = Animation(
            my_direct = 2,
            duration = .4,
            t = 'out_circ'
        )
        anim.start(self.content_screen.ids.content_screen_layout)

        # menghapus content screen
        def remove_content(*args):
            self.second_screen.remove_widget(self.content_screen)
        anim.bind(on_complete = remove_content)

        # config floatbutton
        self.ids.float_btn.text = 'Lihat Selengkapnya'
        self.ids.float_btn.icon = 'assets/arrow.png'

        # bind floatbutton
        self.ids.float_btn.bind(on_release = self.goto_content_screen)

class MainScreen(Screen):
    # set global variable untuk class lain
    # karena variabel dalam init+super() tidak bisa digunakan untuk global dalam kivy
    product_pict_path = StringProperty('')
    title_text = StringProperty('')
    type_text = StringProperty('')
    product_rating = StringProperty('')

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.primary_color = 206/255, 18/255, 18/255, 1

        # LIST ID ELEMEN
        # attribute 'children' berisi list yang reversed dari container
        # sehingga index 0 = -1
        # atau jika diperlukan untuk slicing list menggunakan rumus 0-(index asli+1)

        # untuk carousel childrens bisa menggunakan 'slides'
        # dengan list yang tidak reversed
        self.button_list = self.ids.btn_container.children
        self.card_list = self.ids.card_carousel.slides
        self.indicator_list = self.ids.indicator_container.children

        # KONFIGURASI INDIKATOR
        self.active_indicator_width = 20
        self.active_indicator_color = (206/255, 18/255, 18/255, 1)
        self.inactive_indicator_color = (0,0,0,.2)

        self.indicator_list[-1].width = self.active_indicator_width-8
        self.indicator_list[-1].my_color = self.active_indicator_color

        # mengubah state dari btn pertama saat startup
        self.button_list[-1].state = 'down'

        # list dari indikator index untuk di animasikan
        self.active_indicator = [self.indicator_list[-1],'']

        # set default global varible value
        self.product_pict_path = self.card_list[0].product_preview_path
        self.title_text = self.card_list[0].title_text
        self.type_text = self.card_list[0].type_text
        self.product_rating = self.card_list[0].rating

    def activate_indicator(self, index):
        # jika index 1 tidak kosong, maka index 0 digantikan index 1
        if self.active_indicator[1] != '':
            self.active_indicator[0] = self.active_indicator[1]
        else:
            pass

        # dan update index 1 dengan yang baru,
        # yang kemudian akan menggantikan index 0 selanjutnya saat event berjalan lagi
        self.active_indicator[1] = self.indicator_list[0-(index+1)]

        # anim1 untuk animasi index 0
        anim1 = Animation(
            width = self.active_indicator_width if self.active_indicator[1] == '' else 8,
            duration = .1,
            my_color = self.active_indicator_color if self.active_indicator[1] == '' else self.inactive_indicator_color,
            t = 'out_circ')

        # anim2 untuk animasi index 1
        anim2 = Animation(
            width = self.active_indicator_width,
            my_color = self.active_indicator_color,
            duration = .1,
            t = 'out_circ')

        # jika index 1 sama dengan index 0 maka do nothing
        # terjadi jika event dijalankan dari satu btn yang sama
        if self.active_indicator[1] == self.active_indicator[0]:
            pass
        else:
            anim1.start(self.active_indicator[0])
            anim2.start(self.active_indicator[1])

    def current_product_element(self, path, title, type, rate):
        self.product_pict_path = path
        self.title_text = title
        self.type_text = type
        self.product_rating = rate
        print('###################')
        print(f'path = {path}')
        print(f'title = {title}')
        print(f'type = {type}')
        print(f'rating = {rate}')

class ContentScreen(Screen):
    def __init__(self, **kwargs):
        super(ContentScreen, self).__init__(**kwargs)
        self.ids.content_screen_layout.opacity = 0
        #self.ids.back_button.my_direct = 2

    def animate_back_button_on_spawn(self):
        anim = Animation(
            opacity = 1,
            duration = .4,
        )
        anim.start(self.ids.back_button)

    def animate_back_button_on_disapear(self):
        anim = Animation(
            opacity = 0,
            duration = .25,
            t = 'out_circ'
        )
        anim.start(self.ids.back_button)

class ReadMoreBtn(Button):
    def animate_on_press(self, target):
        anim = Animation(
            width = (target.width - 3),
            height = (target.height - 3),
            duration = .04,
            t = 'out_circ'
        ).start(target)

    def animate_on_release(self, target):
        default_width = self.width
        default_height = self.height

        anim2 = Animation(
            width = default_width,
            height = default_height,
            duration = .2,
            t = 'out_circ'
        ).start(target)

    def animate_icon(self, target):
        default_size = 17
        anim = Animation(
            my_size = (target.my_size+2),
            duration = .06,
        )
        anim += Animation(
            my_size = default_size,
            duration = .3,
            t = 'out_circ'
        )
        anim.start(target)

class ChooserButton(ToggleButton):
    def __init__(self, **kwargs):
        super(ChooserButton, self).__init__(**kwargs)
        self.untouch_color = (255/255, 224/255, 224/255, 1) # warna default

    def animate_touch(self, state):
        anim = Animation(my_color = self.untouch_color,
            duration = .2, t = 'out_circ')

        if state == 'down':
            anim.start(self)
        else:
            pass

class MainApp(App):
    def build(self):
        kv = Builder.load_file('screens/manager.kv')
        # default window size
        Window.size = (350, 680)
        # limit window size
        Window.minimum_width, Window.minimum_height = Window.size
        #Window.borderless = True
        return Manager()

if __name__ == '__main__':
    MainApp().run()
