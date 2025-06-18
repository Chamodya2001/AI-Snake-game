import cv2
import time
from snake import Snake
from food import Food
from hand_tracking import HandTracker

# Constants
WIDTH, HEIGHT = 600, 600
BLOCK_SIZE = 20
DELAY = 100
CONTROL_PANEL_AREA = (0, 0, 210, 60)  # (x1, y1, x2, y2) of the control panel

# Game objects
snake = Snake(block_size=BLOCK_SIZE)
snake.set_direction((BLOCK_SIZE, 0))  # Start moving right
food = Food(WIDTH, HEIGHT, BLOCK_SIZE)
hand_tracker = HandTracker()
score = 0
final_score_displayed = False

# Game state flags
game_started = False
game_paused = False

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Camera failed to open. Check permissions or camera index.")
    exit()

print("🖐️ Show your hand to the camera to start controlling.")
time.sleep(2)

def handle_controls(finger_x, finger_y):
    global game_started, game_paused
    if 10 <= finger_x <= 50 and 10 <= finger_y <= 50:
        game_started = True
        game_paused = False
    elif 60 <= finger_x <= 100 and 10 <= finger_y <= 50:
        if game_started:
            game_paused = False
    elif 110 <= finger_x <= 150 and 10 <= finger_y <= 50:
        game_paused = True
    elif 160 <= finger_x <= 200 and 10 <= finger_y <= 50:
        return "close"
    return None

def control_snake_with_finger(finger_x, finger_y):
    if finger_x is None or finger_y is None:
        return
    head_x, head_y = snake.body[-1]
    dx, dy = snake.direction
    if abs(finger_x - head_x) > abs(finger_y - head_y):
        if finger_x > head_x and dx <= 0:
            snake.set_direction((BLOCK_SIZE, 0))
        elif finger_x < head_x and dx >= 0:
            snake.set_direction((-BLOCK_SIZE, 0))
    else:
        if finger_y > head_y and dy <= 0:
            snake.set_direction((0, BLOCK_SIZE))
        elif finger_y < head_y and dy >= 0:
            snake.set_direction((0, -BLOCK_SIZE))

def avoid_control_panel_for_food():
    while True:
        food.spawn()
        fx, fy = food.position
        if not (CONTROL_PANEL_AREA[0] <= fx <= CONTROL_PANEL_AREA[2] and
                CONTROL_PANEL_AREA[1] <= fy <= CONTROL_PANEL_AREA[3]):
            break

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame")
        break
    frame = cv2.flip(frame, 1)
    background = frame.copy()
    finger_pos = hand_tracker.get_index_finger_tip(frame)
    if finger_pos:
        fx, fy = finger_pos
        result = handle_controls(fx, fy)
        if result == "close":
            break
        if game_started and not game_paused:
            control_snake_with_finger(fx, fy)
    if game_started and not game_paused:
        snake.move()
        if snake.check_collision(WIDTH, HEIGHT):
            print(f"💀 Game Over! Final Score: {score}")
            game_started = False
            game_paused = True
            final_score_displayed = True
            continue
        if snake.body[-1] == food.position:
            snake.grow()
            score += 1
            avoid_control_panel_for_food()
    game_img = background.copy()
    if game_started:
        for segment in snake.body:
            x, y = segment
            cv2.circle(game_img, (x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2), BLOCK_SIZE // 2 - 2, (0, 255, 0), -1)
        fx, fy = food.position
        cv2.circle(game_img, (fx + BLOCK_SIZE // 2, fy + BLOCK_SIZE // 2), BLOCK_SIZE // 2 - 2, (0, 0, 255), -1)
    if final_score_displayed:
        game_img[:] = (0, 0, 0)
        cv2.putText(game_img, f"Game Over!", (130, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        cv2.putText(game_img, f"Final Score: {score}", (100, 300),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
        cv2.putText(game_img, "Touch START to play again", (70, 400),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 255, 100), 2)
        snake = Snake(block_size=BLOCK_SIZE)
        snake.set_direction((BLOCK_SIZE, 0))
        food = Food(WIDTH, HEIGHT, BLOCK_SIZE)
        avoid_control_panel_for_food()
        score = 0
        final_score_displayed = False
    else:
        cv2.putText(game_img, f"Score: {score}", (WIDTH - 200, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.rectangle(game_img, (10, 10), (50, 50), (0, 255, 0), 2)
    cv2.putText(game_img, "S", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.rectangle(game_img, (60, 10), (100, 50), (255, 255, 0), 2)
    cv2.putText(game_img, "R", (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    cv2.rectangle(game_img, (110, 10), (150, 50), (0, 0, 255), 2)
    cv2.putText(game_img, "P", (125, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.rectangle(game_img, (160, 10), (200, 50), (100, 0, 255), 2)
    cv2.putText(game_img, "X", (175, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 0, 255), 2)

    if finger_pos:
        cv2.circle(game_img, (fx, fy), 8, (255, 0, 0), -1)

    cv2.imshow("🐍 Snake Game - Hand Controlled", game_img)
    if cv2.waitKey(DELAY) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()