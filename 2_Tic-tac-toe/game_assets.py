import pygame


class Image():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class Button(Image):
    def draw(self, surface):
        pos = pygame.mouse.get_pos()

        action = False
        clicked = False

        if self.rect.collidepoint(pos):
            # 0 is left mouse button
            if pygame.mouse.get_pressed()[0] == True and clicked == False:
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == False:
                clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
