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

    def get(self, lon, lat, delta):

        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([delta, delta]),
            "l": "map"}
        response = requests.get(self.api_server, params=params)
        if not response:
            response = "bad"
        return response


def to_img(response):
    img = Image.new("RGB", (600, 450), (256, 256, 256))
    code = Image.open(io.BytesIO(response))
    img.paste(code, (0, 0))
    img.save("Map.png")


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
    button = Button((100, 400), butWidth=140, text="map")
    done = False
    img = "None.png"
    font = pg.font.SysFont("Segoe UI", 30)
    while not done:
        for event in pg.event.get():
            mousePos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.USEREVENT:
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
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
                img = map(lon, lat, delta)
            if event.type == pg.KEYUP and event.key == pg.K_PAGEUP:
                delta_fl = float(delta) - 0.01
                if delta_fl >= 0:
                    delta = str(delta_fl)
                img = map(lon, lat, delta)
            if event.type == pg.KEYUP and event.key == pg.K_RIGHT:
                lon_fl = float(lon) + 0.01
                if lon_fl < 180:
                    lon = str(lon_fl)
                img = map(lon, lat, delta)
            if event.type == pg.KEYUP and event.key == pg.K_LEFT:
                lon_fl = float(lon) - 0.01
                if lon_fl > -180:
                    lon = str(lon_fl)
                img = map(lon, lat, delta)
            if event.type == pg.KEYUP and event.key == pg.K_UP:
                lat_fl = float(lat) + 0.01
                if lat_fl < 180:
                    lat = str(lat_fl)
                img = map(lon, lat, delta)
            if event.type == pg.KEYUP and event.key == pg.K_DOWN:
                lat_fl = float(lat) - 0.01
                if lat_fl > -180:
                    lat = str(lat_fl)
                img = map(lon, lat, delta)
            if event.type == pg.MOUSEBUTTONDOWN and button.mouse_in(mousePos) is True:
                img = map(lon, lat, delta)
            manager.process_events(event)
        screen.fill((30, 30, 30))
        manager.update(clock.tick(30)/1000.0)
        manager.draw_ui(screen)
        image = pg.image.load(img)
        rect = (300, 100, 100, 50)
        screen.blit(image, rect)
        try:
            lon_txt = font.render(f"{lon}", True, (112, 112, 112))
            lat_txt = font.render(f"{lat}", True, (112, 112, 112))
            delta_txt = font.render(f"{delta}", True, (112, 112, 112))
            screen.blit(lon_txt, (100, 500))
            screen.blit(lat_txt, (100, 550))
            screen.blit(delta_txt, (100, 600))
        except:
            pass
        button.render(screen)
        pg.display.flip()
        clock.tick(30)

def map(lon, lat, delta):
    api_map = request()
    bytes_code = api_map.get(lon, lat, delta)
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
