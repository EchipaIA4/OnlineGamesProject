import pygame
import asyncio
import sys
import random
import json
import traceback

WIDTH, HEIGHT = 800, 600
GAME_TITLE = "PONG"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 255, 50)
RED = (255, 50, 50)

status_msg = "Network: Ready"
status_color = WHITE

async def submit_score_native(score):
    global status_msg, status_color
    
    if sys.platform != "emscripten":
        status_msg = "Skipped (Desktop Mode)"
        return

    url = "/api/submit-score"
    status_msg = f"Sending {score}..."
    status_color = WHITE
    
    try:
        from platform import window
        
        score_payload = json.dumps({"game_id": "pong", "score": score})
        
        fetch_config = {
            "method": "POST",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": score_payload,
            "credentials": "include"
        }
        
        config_str = json.dumps(fetch_config)
        
        js_options = window.JSON.parse(config_str)
        
        response = await window.fetch(url, js_options)

        if response.status == 200:
            status_msg = "SUCCESS: Saved!"
            status_color = GREEN
        else:
            status_msg = f"FAIL: {response.status}"
            status_color = RED
            
    except Exception as e:
        # Print error to screen and console
        status_msg = f"Err: {str(e)[:20]}"
        status_color = RED
        print(f"Full Error: {e}")
        traceback.print_exc()

async def run_game():
    global status_msg, status_color
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.SysFont(None, 55)
    small_font = pygame.font.SysFont(None, 30)

    player = pygame.Rect(WIDTH - 40, HEIGHT // 2 - 50, 20, 100)
    opponent = pygame.Rect(20, HEIGHT // 2 - 50, 20, 100)
    ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)
    ball_speed_x = 7 * random.choice((1, -1))
    ball_speed_y = 7 * random.choice((1, -1))

    player_score = 0
    opponent_score = 0
    game_over = False
    score_submitted = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_over:
                game_over = False
                score_submitted = False
                player_score = 0
                opponent_score = 0
                ball.center = (WIDTH // 2, HEIGHT // 2)
                ball_speed_x = 7 * random.choice((1, -1))
                ball_speed_y = 7 * random.choice((1, -1))
                status_msg = "Network: Ready"
                status_color = WHITE

        if not game_over:
            mouse_y = pygame.mouse.get_pos()[1]
            player.center = (WIDTH - 30, mouse_y)
            player.clamp_ip(screen.get_rect())
            if opponent.centery < ball.centery: opponent.y += 6
            if opponent.centery > ball.centery: opponent.y -= 6
            opponent.clamp_ip(screen.get_rect())
            ball.x += ball_speed_x
            ball.y += ball_speed_y
            if ball.top <= 0 or ball.bottom >= HEIGHT: ball_speed_y *= -1
            if ball.colliderect(player) or ball.colliderect(opponent): ball_speed_x *= -1
            if ball.left <= 0:
                player_score += 1
                ball.center = (WIDTH // 2, HEIGHT // 2)
                ball_speed_x *= -1
            if ball.right >= WIDTH:
                opponent_score += 1
                ball.center = (WIDTH // 2, HEIGHT // 2)
                ball_speed_x *= -1
            if player_score >= 5 or opponent_score >= 5:
                game_over = True

        if game_over and not score_submitted:
            asyncio.create_task(submit_score_native(player_score))
            score_submitted = True

        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, player)
        pygame.draw.rect(screen, WHITE, opponent)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        score_text = font.render(f"{opponent_score} - {player_score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

        # status_surf = small_font.render(status_msg, True, status_color)
        # screen.blit(status_surf, (10, HEIGHT - 30))

        if game_over:
            res_text = font.render("GAME OVER", True, WHITE)
            screen.blit(res_text, (WIDTH // 2 - res_text.get_width() // 2, HEIGHT // 2 - 50))
            restart_text = font.render("Press SPACE to Restart", True, WHITE)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))

        pygame.display.flip()
        await asyncio.sleep(0)

async def main():
    try:
        await run_game()
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())