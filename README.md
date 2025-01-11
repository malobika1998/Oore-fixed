The issue with the colliderect method might stem from a couple of potential factors:

Bullet list mismatch: In the Game class, when bullets are created, they are appended to the spaceship's bullets list (either y_spcshp.bullets or r_spcshp.bullets). However, in the handle_bullets method, you are iterating over self.y_bullets and self.r_bullets instead of the bullets attribute of each spaceship (self.y_spcshp.bullets and self.r_spcshp.bullets). This results in no bullets being processed for collision detection because the lists don't match.

Collision detection issue: You might also want to check if the bullet and spaceship rectangles are properly aligned and the size of the bullet is suitable for detection.

