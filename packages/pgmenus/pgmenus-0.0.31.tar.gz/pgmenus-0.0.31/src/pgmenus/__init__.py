import pygame as pg

class Label():
    '''Display easily text .'''
    def __init__(self, text: str, font_color: tuple|str, rect: pg.Rect, centered: bool = False) -> None:
        self.text:          str         = text
        self.font_color:    tuple|str   = font_color
        self.rect:          pg.Rect     = rect
        self.centered:      bool        = centered

    def draw(self, surface: pg.Surface, font: pg.font.Font, parent_rect: pg.Rect = None, center_text: bool = False) -> None:
        '''Draw the Label onto the screen.'''
        text = font.render(
            self.text,
            True,
            self.font_color
        )
        text_rect = text.get_rect()

        if parent_rect:
            if self.centered: # Center from the Label's perspektive.
                text_rect.center = (
                    text_rect.x,
                    text_rect.y
                )
            else:
                if center_text: # Center to the parent.
                    text_rect.center = parent_rect.center
                else:
                    text_rect.x = self.rect.x
                    text_rect.y = self.rect.y

        else:
            if self.centered:
                text_rect.center = (
                    self.rect.x,
                    self.rect.y
                )
            else:
                text_rect.x = self.rect.x
                text_rect.y = self.rect.y

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
            self.label.draw(surface, font, self.collision_rect, self.center_text)

    def handle_action(self) -> None:
        '''Handle Action.'''
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
        '''Draw the Slider onto the screen.'''
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
            self.label.draw(surface, font, self.collision_rect, self.center_text) # display text Label.

    def handle_action(self) -> None:
        '''Handle an action as a function and pass it a value between 0 and 1 - [0;1].'''
        self.action(self.value) # send the value to the action function.

    def update(self) -> None:
        '''Update the current value.'''
        mouse_pos = mx, my = pg.mouse.get_pos()
        if self.collision_rect.collidepoint(mouse_pos):
            # Mouse hovers over the slide.
            if pg.mouse.get_pressed()[0]:
                # Mouse left click.
                relative_pos = rel_x, rel_y = mx - self.collision_rect.x, my - self.collision_rect.y
                value = rel_x / self.collision_rect.width * 100 # in percentage - [0;100].
                self.value = value # set the new acquired value.
                if self.action != None:
                    self.handle_action()


class Dropdown():
    '''Dropdown and choose values from list.'''
    def __init__(self, background_color: tuple|str, rect: pg.Rect, centered: bool = False, label: Label = None, center_text: bool = False, auto_size: bool = False, action: any = None, border_radius: int = 5, list_of_values: list[str|int|float] = ['No Values']) -> None:
        self.background_color:  tuple|str               = background_color
        self.rect:              pg.Rect                 = pg.Rect(rect)
        self.centered:          bool                    = centered
        self.label:             Label|None              = label
        self.center_text:       bool                    = center_text
        self.auto_size:         bool                    = auto_size
        self.action:            any                     = action
        self.list_of_values:    list[str|int|float]     = list_of_values
        self.index:             int                     = 0

        self.ele_height:        int                     = 100
        self.collision_rect:    pg.Rect                 = pg.Rect(rect) # Handels Collision detection.
        self.item_collision_rect: pg.Rect               = pg.Rect(
            self.collision_rect.x,
            self.collision_rect.y,
            self.collision_rect.width,
            self.ele_height * len(self.list_of_values),
        )

        self.border_radius:     int                     = border_radius
        self.hovered:           bool                    = False # Current State.
        self.delay:             int                     = 0 # Delay in milliseconds.
        self.max_delay:         int                     = 400 # Maximum delay in milliseconds.

    def draw(self, surface: pg.surface, font: pg.font.Font) -> None:
        new_rect: pg.Rect = pg.Rect(self.rect) # make a copy of the Rect instance --- to prevent unexpected behavior.
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

        self.collision_rect: pg.Rect = pg.Rect(new_rect) # Update the collision rect.

        # BG (Background)
        pg.draw.rect(
            surface,
            self.background_color,
            self.collision_rect,
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
            self.label.draw(surface, font, self.collision_rect, self.center_text) # display text Label.

        if len(self.list_of_values) >= 1:
            display_current_value = Label(
                rect=pg.Rect(
                    new_rect.centerx,
                    new_rect.centery,
                    new_rect.width,
                    new_rect.height
                ),
                centered=True,
                font_color=self.background_color,
                text=self.list_of_values[self.index]
            )
            display_current_value.draw(surface, font)

        self.item_collision_rect: pg.Rect = pg.Rect(
            self.collision_rect.x,
            self.collision_rect.y,
            self.collision_rect.width,
            self.ele_height * len(self.list_of_values),
        )

        # Display hover.
        if self.hovered:
            # so display all possible values
            dy = self.collision_rect.height
            for ele in self.list_of_values:
                ele_rect = pg.Rect(
                    self.collision_rect.x,
                    self.collision_rect.y + dy,
                    self.collision_rect.width,
                    self.ele_height
                )
                pg.draw.rect(
                    surface,
                    self.background_color,
                    ele_rect,
                    1
                )
                ele_b = Button(
                    action=None,
                    background_color=self.background_color,
                    rect=ele_rect,
                    label=Label(
                        font_color='white',
                        rect=pg.Rect(0, 0, 0, 0),
                        text=str(ele)
                    ),
                    center_text=True,
                )
                ele_b.draw(surface, font)
                dy += self.ele_height

    # def handle_action(self) -> None:
    #     self.action(self.value) # send the value to the action function.

    def update(self) -> None: # update value
        mouse_pos = mx, my = pg.mouse.get_pos()
        if self.collision_rect.collidepoint(mouse_pos) or (self.item_collision_rect.collidepoint(mouse_pos) and self.hovered):
            # Mouse hovers over the slide.
            if pg.mouse.get_pressed()[0]:
                # Mouse left click press.
                if self.delay == 0:
                    self.delay = self.max_delay
                    self.hovered = not self.hovered
        else:
            self.hovered = False

            # Check if click on listed value.
            # maybe a Button.

            # relative_pos = rel_x, rel_y = mx - self.rect.x, my - self.rect.y
            # value = rel_x / self.rect.width * 100 # in percentage - [0;100].
            # self.value = value # set the new acquired value.
            # self.handle_action()

        self.delay = max(0, self.delay - 1) # Update delay.
