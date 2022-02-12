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

    def get(self, lon, lat, delta, type_map, lon_pt, lat_pt):
        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([delta, delta]),
            "l": type_map,
            "pt": ",".join([lon_pt, lat_pt, "ya_ru"])}
        response = requests.get(self.api_server, params=params)
        if not response:
            response = "bad"
        return response
    
    def search(self, location):
        geocoder_request = "http://geocode-maps.yandex.ru/1.x/"
        params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": location,
            "format": "json"}
        response = requests.get(geocoder_request, params)
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            toponym_coodrinates = toponym_coodrinates.split()
        else:
            toponym_coodrinates = None
        return toponym_coodrinates

def to_img(response):
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


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
    input_box4 = UITextEntryLine(relative_rect=Rect(900, 100, 100, 32), manager=manager)
    dropbox_type = OptionBox(900, 150, 100, 32, (240, 240, 240), (40, 40, 40),
                                     pg.font.SysFont("Segoe UI", 30), ["map", "satellite", "hybrid"])
    button = Button((100, 400), butWidth=140, text="map")
    button2 = Button((900, 400), butWidth=140, text="search")                                  
    lon = "30"
    lat = "60"
    lon_pt, lat_pt = "0", "0"
    delta = "1"
    type_map = "map"
    location = ""
    done = False
    img = "None.png"
    font = pg.font.SysFont("Segoe UI", 30)
    while not done:
        events = pg.event.get()
        mousePos = pg.mouse.get_pos()
        for event in events:
            try:
                map_zoom = {float(delta) >= 4: 1, 4 > float(delta) > 1: 0.5,
                 1 >= float(delta) >= 0.2: 0.1, 0.2 > float(delta) >= 0.02: 0.01,
                  0.02 > float(delta) >= 0.002: 0.001, 0.002 > float(delta) >= 0.0002: 0.0001}[True]
            except:
                map_zoom = 0.0001
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.USEREVENT:
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                    if event.ui_element == input_box1:
                        lon = event.text
                    elif event.ui_element == input_box2:
                        lat = event.text
                    elif event.ui_element == input_box3:
                        delta = event.text
                    elif event.ui_element == input_box4:
                        location = event.text
            if event.type == pg.KEYUP and event.key == pg.K_PAGEDOWN:
                delta_fl = float(delta) + map_zoom
                if delta_fl <= 90:
                    delta = str(delta_fl)
                img, lon, lat, delta, lon_pt, lat_pt = map(lon, lat, delta, type_map, lon_pt, lat_pt)
            if event.type == pg.KEYUP and event.key == pg.K_PAGEUP:
                delta_fl = float(delta) - map_zoom
                if delta_fl >= 0:
                    delta = str(delta_fl)
                img, lon, lat, delta, lon_pt, lat_pt = map(lon, lat, delta, type_map, lon_pt, lat_pt)
            if event.type == pg.KEYUP and event.key == pg.K_RIGHT:
                lon_fl = float(lon) + map_zoom
                if lon_fl < 180:
                    lon = str(lon_fl)
                img, lon, lat, delta, lon_pt, lat_pt = map(lon, lat, delta, type_map, lon_pt, lat_pt)
            if event.type == pg.KEYUP and event.key == pg.K_LEFT:
                lon_fl = float(lon) - map_zoom
                if lon_fl > -180:
                    lon = str(lon_fl)
                img, lon, lat, delta, lon_pt, lat_pt = map(lon, lat, delta, type_map, lon_pt, lat_pt)
            if event.type == pg.KEYUP and event.key == pg.K_UP:
                lat_fl = float(lat) + map_zoom
                if lat_fl < 180:
                    lat = str(lat_fl)
                img, lon, lat, delta, lon_pt, lat_pt = map(lon, lat, delta, type_map, lon_pt, lat_pt)
            if event.type == pg.KEYUP and event.key == pg.K_DOWN:
                lat_fl = float(lat) - map_zoom
                if lat_fl > -180:
                    lat = str(lat_fl)
                img, lon, lat, delta, lon_pt, lat_pt = map(lon, lat, delta, type_map, lon_pt, lat_pt)
            if event.type == pg.MOUSEBUTTONDOWN and button.mouse_in(mousePos) is True:
                img, lon, lat, delta, lon_pt, lat_pt = map(lon, lat, delta, type_map, lon_pt, lat_pt, "map")
            elif event.type == pg.MOUSEBUTTONDOWN and button2.mouse_in(mousePos) is True:
                img, lon, lat, delta, lon_pt, lat_pt = map(lon, lat, delta, type_map, lon_pt, lat_pt, "location", location)
            manager.process_events(event)
            drop_type = dropbox_type.update(events)
            if drop_type != -1:
                old = type_map
                type_map = ["map", "sat", "sat,skl"][drop_type]
                if old != type_map:
                    img, lon, lat, delta, lon_pt, lat_pt = map(lon, lat, delta, type_map, lon_pt, lat_pt)
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
            delta_txt = font.render(f"delta: {delta[:7]}", True, (112, 112, 112))
            type_map_txt = font.render(f"type: {type_map[:5]}", True, (112, 112, 112))
            location_txt = font.render(f"location: {location}", True, (112, 112, 112))
            screen.blit(lon_txt, (100, 500))
            screen.blit(lat_txt, (100, 550))
            screen.blit(delta_txt, (100, 600))
            screen.blit(type_map_txt, (100, 650))
            screen.blit(location_txt, (100, 700))
        except:
            pass
        button.render(screen)
        button2.render(screen)
        pg.display.flip()
        clock.tick(30)

def map(lon, lat, delta, type_map, lon_pt, lat_pt, type_call: str = "none", location: str = "none"):
    api_map = request()
    if type_call == "location":
        print(api_map.search(location))
        lon, lat = api_map.search(location)
        delta = "0.002"
        lon_pt, lat_pt = lon, lat
    if type_call == "map":
        lon_pt, lat_pt = "0", "0"
    bytes_code = api_map.get(lon, lat, delta, type_map, lon_pt, lat_pt)
    if bytes_code != "bad":
        to_img(bytes_code)
        img = "Map.png"
    else:
        img = "None.png"
    return img, lon, lat, delta, lon_pt, lat_pt

if __name__ == '__main__':
    main()
    pg.quit()
