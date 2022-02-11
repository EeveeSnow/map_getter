import io
import requests
import pygame as pg
import PIL.Image as Image

pg.init()
screen = pg.display.set_mode((640 + 600, 480 + 450))
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


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

    @property
    def return_text(self):
        return self.text


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
    input_box1 = InputBox(100, 100, 100, 32)
    input_box2 = InputBox(100, 200, 100, 32)
    input_box3 = InputBox(100, 300, 100, 32)
    button = Button((100, 400), butWidth=140, text="map")
    input_boxes = [input_box1, input_box2, input_box3]
    done = False
    api = request()
    img = "None.png"
    while not done:
        for event in pg.event.get():
            mousePos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pg.MOUSEBUTTONDOWN and button.mouse_in(mousePos) is True:
                bytes_code = api.get(lon, lat, delta)
                if bytes_code != "bad":
                    bytes_code = bytes_code.content
                    to_img(bytes_code)
                    img = "Map.png"
        for box in input_boxes:
            box.update()
        screen.fill((30, 30, 30))
        image = pg.image.load(img)
        rect = (300, 100, 100, 50)
        screen.blit(image, rect)
        button.render(screen)
        lon = input_box1.return_text
        lat = input_box2.return_text
        delta = input_box3.return_text
        for box in input_boxes:
            box.draw(screen)
        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()
