# "C:\py_venv\kivy_venv\scripts\activate"

# untuk keperluan packaging ke executable onefile
import os, sys
from kivy.resources import resource_add_path, resource_find

# konfigurasi untuk open gl dibawah versi 2
'''
from kivy import Config
Config.set('graphics', 'multisamples', '0')

import kivy
kivy.require('2.0.0')
'''
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.properties import StringProperty

from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label

class Manager(Screen):
    float_btn_icon = StringProperty('')
    float_btn_text = StringProperty('')
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        # define id dari boxlayout untuk spawn screen
        self.first_screen = self.ids.layout_for_main
        self.second_screen = self.ids.layout_for_content

        # define main screen
        self.main_screen = MainScreen()
        # spawn MainScreen pada startup
        self.first_screen.add_widget(self.main_screen)

        # konfigurasi floatbutton
        self.float_btn_icon = 'assets/arrow.png'
        self.float_btn_text = 'Lihat Selengkapnya'
        # bind floatbutton
        self.ids.float_btn.bind(on_release = self.gotoContentScreen)

    def contentConfig(self, *args):
        # set content element
        self.content_screen.ids.content_pict.source = self.main_screen.product_pict_path
        self.content_screen.ids.title_text.text = self.main_screen.title_text
        self.content_screen.ids.type_text.text = self.main_screen.type_text
        self.content_screen.ids.rating.text = self.main_screen.product_rating

        # mengatur jumlah star rating yang akan ditampilkan
        rate = self.main_screen.product_rating.split('.')
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

    def gotoContentScreen(self, *args):
        # define content_screen
        self.content_screen = ContentScreen()

        # spawn content screen
        screen = self.second_screen.add_widget(self.content_screen)

        # konfigurasi element untuk content screen
        self.contentConfig()

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
            self.content_screen.animateBackButtonOnSpawn()
        anim.bind(on_complete = remove_main)

        float_btn = self.ids.float_btn
        # config floatbutton
        self.float_btn_text = 'Bagikan'
        self.float_btn_icon = 'assets/share.png'
        # unbind floatbutton dari gotoContentScreen
        float_btn.unbind(on_release = self.gotoContentScreen)
        # bind floatbutton untuk animasi share screen
        float_btn.bind(on_release = self.content_screen.animateShareScreen)
        float_btn.bind(on_release = self.shareScreenEvent)

    def gotoMainScreen(self, *args):
        # tutup share screen
        self.content_screen.closeShareScreen()
        # animate back button
        anim2 = self.content_screen.animateBackButtonOnDisapear()

        # mencegah error saat tombol kembali ditekan 2x
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

        float_btn = self.ids.float_btn
        # config floatbutton
        self.float_btn_text = 'Lihat Selengkapnya'
        self.float_btn_icon = 'assets/arrow.png'
        # unbind floatbutton
        float_btn.unbind(on_release = self.shareScreenEvent)
        self.ids.float_btn.unbind(on_release = self.content_screen.animateShareScreen)
        # bind floatbutton
        float_btn.bind(on_release = self.gotoContentScreen)

    def shareScreenEvent(self, *args):
        if self.content_screen.shareScreenState():
            self.float_btn_icon = 'assets/back-arrow.png'
            self.float_btn_text = 'Kembali'
        else:
            self.float_btn_icon = 'assets/share.png'
            self.float_btn_text = 'Bagikan'

class MainScreen(Screen):
    '''
    set global variable untuk class lain
    karena variabel dalam init+super() tidak bisa digunakan untuk global dalam kivy
    '''

    product_pict_path = StringProperty('')
    title_text = StringProperty('')
    type_text = StringProperty('')
    product_rating = StringProperty('')

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.primary_color = 206/255, 18/255, 18/255, 1

        '''
        [ LIST ID ELEMEN ]
        attribute 'children' berisi list yang reversed dari container,
        sehingga index 0 = -1,
        atau jika diperlukan untuk slicing list menggunakan rumus 0-(index asli+1).
        untuk carousel childrens bisa menggunakan 'slides'
        dengan list yang tidak reversed,
        '''

        self.button_list = self.ids.btn_container.children
        self.card_list = self.ids.card_carousel.slides

        # add indikator berdasarkan banyak card item
        for i in range(len(self.card_list)):
            self.ids.indicator_container.add_widget(MyIndicator())

        self.indicator_list = self.ids.indicator_container.children

        # konfigurasi indikator
        self.active_indicator_width = 20
        self.active_indicator_color = (206/255, 18/255, 18/255, 1)
        self.inactive_indicator_color = (0,0,0,.2)

        self.indicator_list[-1].width = self.active_indicator_width
        self.indicator_list[-1].my_color = self.active_indicator_color

        # list dari indikator index untuk di animasikan
        self.active_indicator = [self.indicator_list[-1],'']

        # mengubah state dari btn pertama saat startup
        self.button_list[-1].state = 'down'

        # set default global variable value (antar class)
        self.product_pict_path = self.card_list[0].product_preview_path
        self.title_text = self.card_list[0].title_text
        self.type_text = self.card_list[0].type_text
        self.product_rating = self.card_list[0].rating

    def activateIndicator(self, index):
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

        # jika index 1 sama dengan index 0 maka do nothing.
        # terjadi jika event dijalankan dari satu btn yang sama
        if self.active_indicator[1] == self.active_indicator[0]:
            pass
        else:
            anim1.start(self.active_indicator[0])
            anim2.start(self.active_indicator[1])

    def currentProductElement(self, path, title, type, rate):
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

    def animateBackButtonOnSpawn(self):
        anim = Animation(
            opacity = 1,
            my_left = 1,
            duration = .3,
            t = 'out_circ'
        )
        anim.start(self.ids.back_button)

    def animateBackButtonOnDisapear(self):
        anim = Animation(
            my_left = -200,
            duration = .3,
            t = 'in_out_back'
        )
        anim.start(self.ids.back_button)

    def shareScreenState(self):
        if self.ids.share_screen.my_bottom == 0:
            return False
        else:
            return True

    def animateShareScreen(self, *args):
        if self.ids.share_screen.my_bottom != 0:
            btm = 0
            self.animateScreenCover()
        elif self.ids.share_screen.my_bottom == 0:
            btm = -.5
            self.animateScreenCover()

        anim = Animation(
            my_bottom = btm,
            duration = .3,
            t = 'out_circ'
        ).start(self.ids.share_screen)

    def animateScreenCover(self):
        if self.ids.share_screen.my_bottom == 0:
            self.ids.main_scroll_view.enable_scroll = True
            opacity = 0
        else:
            self.ids.main_scroll_view.enable_scroll = False
            opacity = .4

        anim = Animation(
            opacity = opacity,
            duration = .4,
            t = 'out_circ'
        ).start(self.ids.screen_cover)

    def closeShareScreen(self, *args):
        if self.ids.share_screen.my_bottom == 0:
            anim = Animation(
                my_bottom = -.5,
                duration = .5,
                t = 'out_circ'
            ).start(self.ids.share_screen)
            self.animateScreenCover()
        else:
            pass

############################ UIX ############################

class MyIndicator(Label):
    pass

class ReadMoreBtn(Button):
    def animateOnPress(self, target):
        anim = Animation(
            width = (target.width - 3),
            height = (target.height - 3),
            duration = .04,
            t = 'out_circ'
        ).start(target)

    def animateOnRelease(self, target):
        default_width = self.width
        default_height = self.height

        anim2 = Animation(
            width = default_width,
            height = default_height,
            duration = .2,
            t = 'out_circ'
        ).start(target)

    def animateIcon(self, target):
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

    def animateTouch(self, state):
        anim = Animation(my_color = self.untouch_color,
            duration = .2, t = 'out_circ')

        if state == 'down':
            anim.start(self)
        else:
            pass

############################ APP ############################
class IndomieApp(App):
    def build(self):
        kv = Builder.load_file('screens/manager.kv')
        # default window size
        Window.size = (350, 680)
        # limit window size
        Window.minimum_width, Window.minimum_height = Window.size
        #Window.borderless = True
        return Manager()

if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    IndomieApp().run()
