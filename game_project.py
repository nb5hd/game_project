# Nikhil Bhaip (nb5hd)
# Ben Thomas (bdt2hw)
# game_project

import pygame
import gamebox
import random

camera = gamebox.Camera(800,600)
plane = gamebox.from_image(400, 100, "http://www.clker.com/cliparts/U/Z/Y/q/y/e/airplane-top-view-md.png")
plane.size = 25, 25
plane.rotate(90)

counter = 0
scroll = 5
clouds = []
cloud_sep_dist = 45

def tick(keys):
    global counter
    global scroll
    global cloud_sep_dist
    camera.y -= scroll  # background scrolls

    if pygame.K_RIGHT in keys:
        plane.x += 15
    if pygame.K_LEFT in keys:
        plane.x -= 15
    if pygame.K_DOWN in keys:
        plane.y += 15
    if pygame.K_UP in keys:
        plane.y -= 15

    camera.clear("cyan")  # sky is blue

    if plane.x >= 800:  # prevents plane from going off-screen
        plane.x -= 15
    elif plane.x <= 0:
        plane.x += 15
    if plane.y <= camera.y - 300:
        plane.y += 13

    if counter == 1000 or counter == 2000:  # difficulty increases every 1000
        scroll += 3
        cloud_sep_dist -= 10

    counter += 1 # each tick is an increase

    if counter % cloud_sep_dist == 0:  # create clouds every (cloud_sep_dist/30) seconds
        left_width = random.randint(0, 700)  # this changes the location of the gap
        new_left_cloud = gamebox.from_color(0, camera.y-300,  "white", left_width, 10)  # clouds are white
        new_left_cloud.left = 0
        new_right_cloud = gamebox.from_color(600, camera.y-300, "white", 750-left_width, 10)  # the gap is always 50 px
        new_right_cloud.right = 800
        clouds.append(new_left_cloud)
        clouds.append(new_right_cloud)

    for cloud in clouds:
        if plane.top_touches(cloud):
            plane.y += 15  # moves the plane backwards
        if plane.bottom_touches(cloud):
            plane.y -= 15  # move the plane forwards
        if plane.left_touches(cloud):
            plane.move_to_stop_overlapping(cloud)
        if plane.right_touches(cloud):
            plane.move_to_stop_overlapping(cloud)
        camera.draw(cloud)

    if counter < 50:  # title screen
        camera.draw(gamebox.from_text(400, camera.y, "Let's play Dodge Cloud!","Helvetica", 50, "red"))

    # counter is the score, counter// 30 (the FPS) is the time
    camera.draw(gamebox.from_text(400, camera.y +200, "Score: " + str(counter),"Helvetica", 50, "red"))
    camera.draw(gamebox.from_text(150, camera.y +200, "Timer: " + str(counter // 25),"Helvetica", 50, "red"))
    camera.draw(plane)

    if plane.y - 15 >= camera.y + 300:  # if you go off screen from the bottom, you lose!
        camera.draw(gamebox.from_text(400, camera.y-200, "You Lose!", "Helvetica", 120, "red"))
        gamebox.pause()

    if counter == 3000:  # You win! 3000 is the max score.
        camera.draw(gamebox.from_text(400, camera.y-200,"You win!","Helvetica",120,"red"))
        gamebox.pause()

    camera.display()
ticks_per_second = 30

# keep this line the last one in your program
gamebox.timer_loop(ticks_per_second, tick)
