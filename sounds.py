import pygame

class SoundPlayer:
    class Effects:
        def Crash():
            crash_sound = pygame.mixer.Sound("sounds/crash.mp3")
            crash_sound.play()

