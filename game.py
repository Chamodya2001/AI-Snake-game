# game.py

import cv2
import numpy as np

# Load and resize images for snake and food
snake_img = cv2.imread("assets/snake.jpg", cv2.IMREAD_UNCHANGED)
food_img = cv2.imread("assets/apple.jpg", cv2.IMREAD_UNCHANGED)

# Resize to fit block size
snake_img = cv2.resize(snake_img, (20, 20))
food_img = cv2.resize(food_img, (20, 20))

def render(snake, food, width, height, score):
    # Create black game window
    img = np.zeros((height, width, 3), np.uint8)

    # Draw snake segments
    for segment in snake.body:
        x, y = segment
        try:
            img[y:y+20, x:x+20] = snake_img[:, :, :3]
        except:
            pass  # Avoid errors on out-of-bounds

    # Draw food item
    fx, fy = food.position
    try:
        img[fy:fy+20, fx:fx+20] = food_img[:, :, :3]
    except:
        pass

    # Draw current score
    cv2.putText(img, f"Score: {score}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # --- Draw Touch Zones ---

    # Start (top-left)
    cv2.rectangle(img, (0, 0), (100, 100), (0, 255, 255), 2)
    cv2.putText(img, "START", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    # Pause (top-center)
    cv2.rectangle(img, (250, 0), (350, 100), (255, 255, 0), 2)
    cv2.putText(img, "PAUSE", (260, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    # Stop (top-right)
    cv2.rectangle(img, (500, 0), (600, 100), (0, 0, 255), 2)
    cv2.putText(img, "STOP", (510, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    return img
