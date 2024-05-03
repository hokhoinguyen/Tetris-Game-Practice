import sys
import pygame
from colors import Colors
from game import Game
from datetime import timedelta

pygame.init()

title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)
time_surface = title_font.render("Time", True, Colors.white)

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)
time_rect = pygame.Rect(10, 155, 170, 60)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris")

clock = pygame.time.Clock()

game = Game()

GAME_UPDATE = pygame.USEREVENT
time_interval = 500
pygame.time.set_timer(GAME_UPDATE, time_interval)

# Initialize time tracking variables
current_time = pygame.time.get_ticks()  # Current time in milliseconds
time_since_last_second = 0  # Time since last second update

while True:
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if game.game_over == True:
				game.game_over = False
				game.reset()
			if event.key == pygame.K_LEFT and game.game_over == False:
				game.move_left()
			if event.key == pygame.K_RIGHT and game.game_over == False:
				game.move_right()
			if event.key == pygame.K_DOWN and game.game_over == False:
				game.move_down()
				game.update_score(0, 1)

			if event.key == pygame.K_UP and game.game_over == False:
				game.rotate()
		if event.type == GAME_UPDATE and game.game_over == False:
			game.move_down()

	# Update time tracking variables
	current_tick = pygame.time.get_ticks()
	time_since_last_second += current_tick - current_time
	current_time = current_tick
	# If a second has passed, decrease time_interval by 10 milliseconds

	if time_since_last_second >= 1000:
		time_since_last_second -= 1000
		if time_interval > 60:
			time_interval -= 10
			pygame.time.set_timer(GAME_UPDATE, time_interval)
			print(time_interval)




	#Drawing
	score_value_surface = title_font.render(str(game.score), True, Colors.white)
	screen.fill(Colors.dark_blue)
	screen.blit(score_surface, (365, 20, 50, 50))
	screen.blit(next_surface, (375, 180, 50, 50))
	screen.blit(time_surface, (375, 450, 50, 50))

	if game.game_over == True:
		screen.blit(game_over_surface, (320, 500, 50, 50))
	else:
		game.update_timer()
		time_remaining_surface = title_font.render(str(timedelta(seconds=max(int(game.countdown_time), 0))), True, Colors.white)
		screen.blit(time_remaining_surface, (360, 500, 50, 50))


	pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
	screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx,
		centery = score_rect.centery))
	pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
	game.draw(screen)

	pygame.display.update()
	clock.tick(60)