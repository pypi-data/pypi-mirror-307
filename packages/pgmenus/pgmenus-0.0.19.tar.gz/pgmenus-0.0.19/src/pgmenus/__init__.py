import pygame as pg

class Label():
    '''Display easily text .'''
    def __init__(self, text: str, font_color: tuple|str, rect: pg.Rect, centered: bool = False) -> None:
        self.text:          str         = text
        self.font_color:    tuple|str   = font_color
        self.rect:          pg.Rect     = rect
        self.centered:      bool        = centered


    def draw(self, surface: pg.Surface, font: pg.font.Font, parent_rect: pg.Rect = None, center_text: bool = False) -> None:
        text = font.render(
            self.text,
            True,
            self.font_color
        )
        text_rect = text.get_rect()
        if self.centered:
            text_rect.center = (
                self.rect.x,
                self.rect.y
            )
        if parent_rect:
            text_rect.x += parent_rect.x
            text_rect.y += parent_rect.y
            if center_text:
                text_rect.x += (parent_rect.width - text_rect.width) // 2
                text_rect.y += (parent_rect.height - text_rect.height) // 2
        surface.blit(text, text_rect)



class Button():
    '''Make actions happen on click.'''
    def __init__(self, background_color: tuple|str, rect: pg.Rect, centered: bool = False, label: Label = None, center_text: bool = False, auto_size: bool = False, action: any = None) -> None:
        self.background_color:  tuple|str   = background_color
        self.rect:              pg.Rect     = rect
        self.centered:          bool        = centered
        self.label:             Label|None  = label
        self.center_text:       bool        = center_text
        self.auto_size:         bool        = auto_size
        self.action:            any         = action

        self.collision_rect: pg.Rect = rect # Handels Collision detection.


    def draw(self, surface: pg.surface, font: pg.font.Font) -> None:
        '''Draw Button on surface.'''
        new_rect: pg.Rect = pg.Rect(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height
        )

        if self.auto_size:
            if self.label != None:
                text = font.render(
                    self.label.text,
                    True,
                    self.label.font_color
                )
                text_rect = text.get_rect()
                new_rect.width = text_rect.width + 10 ####

        if self.centered:
            new_rect.x -= new_rect.width//2
            new_rect.y -= new_rect.height//2

        self.collision_rect: pg.Rect = new_rect

        pg.draw.rect(
            surface,
            self.background_color,
            new_rect
        )
        if self.label != None:
            self.label.draw(surface, font, self.rect, self.center_text)


    def handle_action(self) -> None:
        self.action()



class Slider():
    '''Slide between 0 and 100 and get its current value.'''
    def __init__(self, background_color: tuple|str, rect: pg.Rect, centered: bool = False, label: Label = None, center_text: bool = False, auto_size: bool = False, action: any = None, border_radius: int = 5) -> None:
        self.background_color:  tuple|str   = background_color
        self.rect:              pg.Rect     = rect
        self.centered:          bool        = centered
        self.label:             Label|None  = label
        self.center_text:       bool        = center_text
        self.auto_size:         bool        = auto_size
        self.action:            any         = action
        self.value:             int         = 50
        self.min_value:         int         = 0
        self.max_value:         int         = 100

        self.collision_rect: pg.Rect = rect # Handels Collision detection.

        self.border_radius:     int         = border_radius


    def draw(self, surface: pg.surface, font: pg.font.Font) -> None:
        new_rect: pg.Rect = pg.Rect(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height
        ) # make a copy of the Rect instance --- to prevent unexpected behavior.
        self.padding = 5

        if self.auto_size:
            if self.label != None:
                text = font.render(
                    self.label.text,
                    True,
                    self.label.font_color
                )
                text_rect = text.get_rect()
                new_rect.width = text_rect.width + 10 ####

        if self.centered:
            new_rect.x -= new_rect.width//2
            new_rect.y -= new_rect.height//2

        self.collision_rect: pg.Rect = new_rect

        # BG (Background)
        pg.draw.rect(
            surface,
            self.background_color,
            new_rect,
            border_radius=self.border_radius
        )
        # MG (Middleground)
        pg.draw.rect(
            surface,
            'white',
            pg.Rect(
                new_rect.x + self.padding,
                new_rect.y + self.padding,
                new_rect.width - 2 * self.padding,
                new_rect.height - 2 * self.padding
            ),
            border_radius=self.border_radius
        )
        # FG (Foreground) -> Handle
        pg.draw.circle(
            surface,
            self.background_color,
            (
                new_rect.x + round(new_rect.width * self.value/self.max_value),
                new_rect.y + new_rect.height/2
            ),
            (new_rect.height - 2 * self.padding)/2
        )

        if self.label != None:
            self.label.draw(surface, font, self.rect, self.center_text) # display text Label.


    def handle_action(self) -> None:
        self.action(self.value) # send the value to the action function.


    # update value
    def update(self) -> None:
        mouse_pos = mx, my = pg.mouse.get_pos()
        print(mouse_pos)
        if self.collision_rect.collidepoint(mouse_pos):
            # Mouse hovers over the slide
            relative_pos = rel_x, rel_y = mx - self.collision_rect.x, my - self.collision_rect.y
            value = rel_x / self.collision_rect.width * 100 # in percentage - [0;100].
            self.value = value # set the new acquired value.
            if self.action != None:
                self.handle_action()



class Dropdown():
    '''Dropdown and choose values from list.'''
    def __init__(self, background_color: tuple|str, rect: pg.Rect, centered: bool = False, label: Label = None, center_text: bool = False, auto_size: bool = False, action: any = None, border_radius: int = 5, list_of_values: list[str|int|float] = ['No Values']) -> None:
        self.background_color:  tuple|str               = background_color
        self.rect:              pg.Rect                 = rect
        self.centered:          bool                    = centered
        self.label:             Label|None              = label
        self.center_text:       bool                    = center_text
        self.auto_size:         bool                    = auto_size
        self.action:            any                     = action
        self.list_of_values:    list[str|int|float]     = list_of_values
        self.index:             int                     = 0

        self.collision_rect: pg.Rect = rect # Handels Collision detection.

        self.border_radius:     int                     = border_radius
        # Current State
        self.hovered:           bool                    = False


    def draw(self, surface: pg.surface, font: pg.font.Font) -> None:
        new_rect: pg.Rect = pg.Rect(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height
        ) # make a copy of the Rect instance --- to prevent unexpected behavior.
        self.padding = 5

        if self.auto_size:
            if self.label != None:
                text = font.render(
                    self.label.text,
                    True,
                    self.label.font_color
                )
                text_rect = text.get_rect()
                new_rect.width = text_rect.width + 10 ####

        if self.centered:
            new_rect.x -= new_rect.width//2
            new_rect.y -= new_rect.height//2

        self.collision_rect: pg.Rect = new_rect

        # BG (Background)
        pg.draw.rect(
            surface,
            self.background_color,
            new_rect,
            border_radius=self.border_radius
        )
        # MG (Middleground)
        pg.draw.rect(
            surface,
            'white',
            pg.Rect(
                new_rect.x + self.padding,
                new_rect.y + self.padding,
                new_rect.width - 2 * self.padding,
                new_rect.height - 2 * self.padding
            ),
            border_radius=self.border_radius
        )
        # FG (Foreground) -> Handle '\/' dropdown triangle
        pg.draw.polygon(
            surface,
            self.background_color,
            [
                (
                    new_rect.x + new_rect.width - 2 * self.padding - 2 * self.padding,
                    new_rect.y + new_rect.height - 2 * self.padding
                ),
                (
                    new_rect.x + new_rect.width - 4 * self.padding - 2 * self.padding,
                    new_rect.y + 2 * self.padding
                ),
                (
                    new_rect.x + new_rect.width - 2 * self.padding,
                    new_rect.y + 2 * self.padding
                ),
            ]
        )

        if len(self.list_of_values) >= 1:
            self.label.text = self.list_of_values[self.index]

        if self.label != None:
            self.label.draw(surface, font, self.rect, self.center_text) # display text Label.

        if len(self.list_of_values) >= 1:
            display_current_value = Label(
                rect=pg.Rect(
                    new_rect.x + new_rect.width//2,
                    new_rect.y + new_rect.height//2,
                    new_rect.width,
                    new_rect.height
                ),
                centered=True,
                font_color=self.background_color,
                text=self.list_of_values[self.index]
            )
            display_current_value.draw(surface, font, self.rect, self.center_text)

        # Display hover.
        if self.hovered:
            # so display all possible values
            dy = 0
            ele_height = 100
            for ele in self.list_of_values:
                ele_rect = pg.Rect(
                    new_rect.x,
                    new_rect.y + dy,
                    new_rect.width,
                    ele_height
                )
                ele_b = Button(
                    action=None,
                    background_color='red',
                    rect=ele_rect,
                    label=Label(
                        centered=True,
                        font_color='red',
                        rect=ele_rect,
                        text=str(ele)
                    )
                )
                ele_b.draw(surface, font)
                dy += ele_height


    # def handle_action(self) -> None:
    #     self.action(self.value) # send the value to the action function.


    # update value
    def update(self) -> None:
        mouse_pos = mx, my = pg.mouse.get_pos()
        print(mouse_pos)
        if self.collision_rect.collidepoint(mouse_pos):
            # Mouse hovers over the slide
            self.hovered = True
            print('hovering')
        else:
            self.hovered = False

            # Check if click on listed value.
            # maybe a Button.

            # relative_pos = rel_x, rel_y = mx - self.rect.x, my - self.rect.y
            # value = rel_x / self.rect.width * 100 # in percentage - [0;100].
            # self.value = value # set the new acquired value.
            # self.handle_action()

