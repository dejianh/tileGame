import pygame
import game_model

FRAME_RATE = 30
_INITIAL_WIDTH = 600
_INITIAL_HEIGHT = 600
_BACKGROUND_COLOR = pygame.Color(255, 255, 255)
_SQUARE_FRACTION_WIDTH = 1/6
_SQUARE_FRACTION_HEIGHT = 1/13

class ColumnsGame:
    def __init__(self):
        self._running = True
        self._state = game_model.GameState()
        self._game_faller = None

    
    def run(self)->None:
        try:
            pygame.init()

            self._create_surface((_INITIAL_WIDTH, _INITIAL_HEIGHT))

            clock = pygame.time.Clock()
            
            self._state.initiate_game_board_to_empty(13,6)

            time_count = 0

            while self._running:
                clock.tick(FRAME_RATE)

                if time_count %30 == 0:
                    self._time_tick()
                    
                self._handling_event()

                self._draw_frame()
                
                time_count += 1
                
            pygame.quit()
        except game_model.GameOverError:
            print('GAME Over')
            pass


    def _frac_to_pixel(self,frac:float,max_pixel:int)->int:
        return int(frac*max_pixel)


    def _frac_x_to_pixel_x(self,frac_x:float)->int:
        return self._frac_to_pixel(frac_x,self._surface.get_width())

    def _frac_y_to_pixel_y(self,frac_y:float)->int:
        return self._frac_to_pixel(frac_y,self._surface.get_height())
        

    def _draw_frame(self):
        self._surface.fill(_BACKGROUND_COLOR)
        
        self._draw_jewels()
        
        pygame.display.flip()


    def _change_str_color_to_color(self,color:str)->'Color':
        if color == 'R':
            return pygame.Color(255,0,0)

        elif color == 'O':
            return pygame.Color(255,128,0)

        elif color == 'Y':
            return pygame.Color(255,255,0)
        
        elif color == 'G':
            return pygame.Color(0,255,0)
        
        elif color == 'B':
            return pygame.Color(0,128,255)
        
        elif color == 'P':
            return pygame.Color(204,0,204)
        
        elif color == 'D':
            return pygame.Color(0,0,0)
            


    def _draw_jewels(self):
        for jewel_list in self._state.get_board():
            for jewel in jewel_list:
                if jewel != None:
                    if jewel.get_status() == 'freeze' or jewel.get_status() == 'faller':
                        self._draw_jewel(jewel)
                    elif jewel.get_status() == 'faller_land':
                        self._draw_landed_jewel(jewel)
                    elif jewel.get_status() == 'matched':
                        self._draw_matched_jewel(jewel)
                        
    def _draw_landed_jewel(self,jewel:'Jewel'):
        jewel_rect = self._get_jewel_rect(jewel)

        pygame.draw.rect(self._surface,pygame.Color(255,0,127),jewel_rect)


    def _get_jewel_rect(self,jewel:game_model.Jewel)->pygame.rect:
        jewel_row = jewel.get_row()
        jewel_col = jewel.get_col()

        jewel_fraction_x = (jewel_col)*_SQUARE_FRACTION_WIDTH
        jewel_fraction_y = 1-(jewel_row+1)*_SQUARE_FRACTION_HEIGHT

        jewel_pixel_x_left = self._frac_x_to_pixel_x(jewel_fraction_x,)
        jewel_pixel_y_up = self._frac_y_to_pixel_y(jewel_fraction_y,)

        pixel_width = self._frac_x_to_pixel_x(_SQUARE_FRACTION_WIDTH)
        pixel_height = self._frac_y_to_pixel_y(_SQUARE_FRACTION_HEIGHT)

        jewel_rect = pygame.Rect(
            jewel_pixel_x_left,jewel_pixel_y_up,
            pixel_width,pixel_height
            )

        return jewel_rect

        
    def _draw_matched_jewel(self,jewel:'Jewel'):
        jewel_rect = self._get_jewel_rect(jewel)

        pygame.draw.rect(self._surface,pygame.Color(255,255,255),jewel_rect)
        
    def _draw_jewel(self,jewel:'Jewel')->None:
        jewel_rect = self._get_jewel_rect(jewel)
        jewel_color_str = jewel.get_color()

        jewel_color = self._change_str_color_to_color(jewel_color_str)

        pygame.draw.rect(self._surface,jewel_color,jewel_rect)

            

    def _handling_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._create_surface(event.size)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self._game_faller.check_if_faller_could_move_left_and_move_left(self._state)
                if event.key == pygame.K_RIGHT:
                    self._game_faller.check_if_faller_could_move_right_and_move_right(self._state)
                if event.key == pygame.K_SPACE:
                    self._game_faller.rotate(self._state)
                    
                
        
    def _time_tick(self):
        if game_model.check_if_add_random_faller(self._state) == True:
            self._game_faller = game_model.create_random_faller(self._state)

        elif game_model.check_if_add_random_faller(self._state) == False and self._game_faller != None:
            self._state.time_tick(self._game_faller,self._state)

    def _create_surface(self, size: tuple[int, int]) -> None:
        self._surface = pygame.display.set_mode(size, pygame.RESIZABLE)



    def _end_game(self):
        self._running = False
        
if __name__ == '__main__':
    ColumnsGame().run()
