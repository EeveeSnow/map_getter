import io
import requests
import pygame as pg
import PIL.Image as Image
from pygame.rect import Rect
import pygame_gui
from pygame_gui.elements.ui_text_entry_line import UITextEntryLine

pg.init()
screen = pg.display.set_mode((640 + 600, 480 + 450))
manager = pygame_gui.UIManager((640 + 600, 480 + 450))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)


class request():
    def __init__(self):
        self.api_server = "http://static-maps.yandex.ru/1.x/"

    def get(self, lon, lat, delta, type_map):

        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([delta, delta]),
            "l": type_map}
        response = requests.get(self.api_server, params=params)
        if not response:
            response = "bad"
        return response


def to_img(response):
    img = Image.new("RGB", (600, 450), (256, 256, 256))
    code = Image.open(io.BytesIO(response))
    img.paste(code, (0, 0))
    img.save("Map.png")


class OptionBox():

    def __init__(self, x, y, w, h, color, highlight_color, font, option_list, selected=0):
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pg.Rect(x, y, w, h)
        self.font = font
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pg.draw.rect(
            surf, self.highlight_color if self.menu_active else self.color, self.rect)
        pg.draw.rect(surf, (0, 0, 0), self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pg.draw.rect(surf, self.highlight_color if i ==
                                 self.active_option else self.color, rect)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))
            outer_rect = (self.rect.x, self.rect.y + self.rect.height,
                          self.rect.width, self.rect.height * len(self.option_list))
            pg.draw.rect(surf, (0, 0, 0), outer_rect, 2)

    def update(self, event_list):
        mpos = pg.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.selected = self.active_option
                    self.draw_menu = False
                    return self.active_option
        return -1


class Button:
    def __init__(self, position: tuple, butHeigth: int = 70, butWidth: int = 300, text: str = "Кнопка"):
        self.position = position
        self.width = butWidth
        self.heigth = butHeigth
        self.text = text

    def mouse_in(self, mous_pos):
        x, y = mous_pos
        px, py = self.position
        if x > px and x < px + self.width:
            if y > py and y < py + self.heigth:
                return True
            else:
                return False
        else:
            return False

    def render(self, screen):
        mousePos = pg.mouse.get_pos()
        if self.mouse_in(mousePos):
            pg.draw.rect(screen, (112, 112, 112),
                         (self.position[0] - 1, self.position[1] - 1, self.width + 1, self.heigth + 1), 4)
            pg.draw.rect(
                screen, (255, 255, 255), (self.position[0], self.position[1], self.width, self.heigth))
        else:
            pg.draw.rect(screen, (112, 112, 112),
                         (self.position[0] - 1, self.position[1] - 1, self.width + 1, self.heigth + 1), 4)
            pg.draw.rect(
                screen, (237, 237, 237), (self.position[0], self.position[1], self.width, self.heigth))
        # determite size of font
        self.font = pg.font.SysFont("Segoe UI", 30)

        # create text surface with value
        valueSurf = self.font.render(f"{self.text}", True, (112, 112, 112))
        textx = self.position[0] + (self.width / 2) - \
            (valueSurf.get_rect().width / 2)
        texty = self.position[1] + (self.heigth / 2) - \
            (valueSurf.get_rect().height / 2)
        screen.blit(valueSurf, (textx, texty))

def main():
    clock = pg.time.Clock()
    input_box1 = UITextEntryLine(relative_rect=Rect(100, 100, 100, 32), manager=manager)
    input_box2 = UITextEntryLine(relative_rect=Rect(100, 200, 100, 32), manager=manager)
    input_box3 = UITextEntryLine(relative_rect=Rect(100, 300, 100, 32), manager=manager)
    dropbox_type = OptionBox(800, 100, 100, 32, (240, 240, 240), (40, 40, 40),
                                     pg.font.SysFont("Segoe UI", 30), ["map", "satellite", "hybrid"])
    lon = ""
    lat = ""
    delta = ""
    type_map = "map"
    button = Button((100, 400), butWidth=140, text="map")
    done = False
    img = "None.png"
    font = pg.font.SysFont("Segoe UI", 30)
    while not done:
        events = pg.event.get()
        mousePos = pg.mouse.get_pos()
        for event in events:
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.USEREVENT:
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                    if event.ui_element == input_box1:
                        lon = event.text
                    if event.ui_element == input_box2:
                        lat = event.text
                    if event.ui_element == input_box3:
                        delta = event.text
            if event.type == pg.KEYUP and event.key == pg.K_PAGEDOWN:
                delta_fl = float(delta) + 0.01
                if delta_fl <= 90:
                    delta = str(delta_fl)
                img = map(lon, lat, delta, type_map)
            if event.type == pg.KEYUP and event.key == pg.K_PAGEUP:
                delta_fl = float(delta) - 0.01
                if delta_fl >= 0:
                    delta = str(delta_fl)
                img = map(lon, lat, delta, type_map)
            if event.type == pg.KEYUP and event.key == pg.K_RIGHT:
                lon_fl = float(lon) + 0.01
                if lon_fl < 180:
                    lon = str(lon_fl)
                img = map(lon, lat, delta, type_map)
            if event.type == pg.KEYUP and event.key == pg.K_LEFT:
                lon_fl = float(lon) - 0.01
                if lon_fl > -180:
                    lon = str(lon_fl)
                img = map(lon, lat, delta, type_map)
            if event.type == pg.KEYUP and event.key == pg.K_UP:
                lat_fl = float(lat) + 0.01
                if lat_fl < 180:
                    lat = str(lat_fl)
                img = map(lon, lat, delta, type_map)
            if event.type == pg.KEYUP and event.key == pg.K_DOWN:
                lat_fl = float(lat) - 0.01
                if lat_fl > -180:
                    lat = str(lat_fl)
                img = map(lon, lat, delta, type_map)
            if event.type == pg.MOUSEBUTTONDOWN and button.mouse_in(mousePos) is True:
                img = map(lon, lat, delta, type_map)
            manager.process_events(event)
            drop_type = dropbox_type.update(events)
            if drop_type != -1:
                old = type_map
                type_map = ["map", "sat", "sat,skl"][drop_type]
                if old != type_map:
                    img = map(lon, lat, delta, type_map)
        screen.fill((30, 30, 30))
        manager.update(clock.tick(30)/1000.0)
        manager.draw_ui(screen)
        image = pg.image.load(img)
        rect = (300, 100, 100, 50)
        screen.blit(image, rect)
        dropbox_type.draw(screen)
        try:
            lon_txt = font.render(f"lon: {lon[:5]}", True, (112, 112, 112))
            lat_txt = font.render(f"lat: {lat[:5]}", True, (112, 112, 112))
            delta_txt = font.render(f"delta: {delta[:5]}", True, (112, 112, 112))
            type_map_txt = font.render(f"type: {type_map[:5]}", True, (112, 112, 112))
            screen.blit(lon_txt, (100, 500))
            screen.blit(lat_txt, (100, 550))
            screen.blit(delta_txt, (100, 600))
            screen.blit(type_map_txt, (100, 650))
        except:
            pass
        button.render(screen)
        pg.display.flip()
        clock.tick(30)

def map(lon, lat, delta, type_map):
    api_map = request()
    bytes_code = api_map.get(lon, lat, delta, type_map)
    if bytes_code != "bad":
        bytes_code = bytes_code.content
        to_img(bytes_code)
        img = "Map.png"
    else:
        img ="None.png"
    return img

if __name__ == '__main__':
    main()
    pg.quit()
