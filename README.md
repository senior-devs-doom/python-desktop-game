20 SECONDS 2 DIE

A straightforward 2D desktop game of bullet hell genre. Player dodges 12 diffrent aliens and their projectiles trying to survive and wrap up highest score.

TECH INFO :
Game is made in python using pyqt library, which itself is binding library for QT. It's an uni project for python course, so my language choice was quite limited, additionally QT was designed with static forms in mind so after finishing the project I can confidently say that it wasn't the right choice for a somewhat dynamic game. Project clocks in at around 1000 lines of code with 5 classes, instead of using events I opted to create interval refreshing at modifiable rate to mirror usual game logic, tying the game to ticks/frames per second. Game size is unoptimized, and I didn't spend any time modifying default processor settings. I'm satisfied with game running smoothly, at 60 refreshes per second, even with default pyQT configuration. That being said without usual game engine optimizations game will become processor intensive eventually, thou making it that far is quite difficult. Game has 12 unique enemies, most shooting varied projectiles, progressively appearing as player survives longer and longer, additonally weighted spawns allow for rarer, higher threat enemies which player has to prioritize. Randomized enemy spawn and attacks create dynamic challanges which is underexplored area of bullet hell games, design wise player.

DOWNLOAD LINK : https://github.com/senior-devs-doom/python-desktop-game/releases/download/game/20.seconds.2.die.rar

SETTINGS :

Threat - player score, incrementing with every enemy kill and each passed wave. Higher threat results in more enemies on screen.

Level - Difficulty setting, Each survived wave increases level by 1. Amount of enemy types able to be spawned is equal to level, capping at 12. Starting enemies are easy while later ones provide progressively increasing danger.

Frames - game speed, amount of game refresh happening in a second, designed with 60 in mind. Setting it to 30 will make game run 2 times slower, to 120 two times faster.

Lives - Health, how much hit one can take before dying. There is no life 0

Press enter to begin game.

CONTROLS :

WASD/Arrow Keys - Directional movement

Mouse Position - Shooting direction

Hold Left Mouse Button - Shooting

!! Note: You need to hold mouse button to shoot instead of clicking it. WHEN YOU RELEASE THE BUTTON YOU NEED TO WAIT A WHILE BEFORE SHOOTING AGAIN. This is a quirk of 'mouse' library, I didn't fix it cause I think it adds flavor  ¯\_(ツ) !!

ENEMIES :

  Crabbo - bruiser

white - moves normally

green - after crossing player on Xaxis moves to him on Y axis 

yellow - follows the player

red - charges into player, acceleration and following player by angle

  Squid - ranger

white - shoots at player periodically

green - shoots in cone of 3

yellow - shoots bullets that bounce

red - shoots a gatling gun spread at player

  Octopus - mage

white - shoots few bullets that zigzag

green - shoots unaimed all around it at once

yellow - shoots hopping bullets(it was supposed to be circle but midway into implementing it looked cooler so I left it)

red - after a second of tracking shoots blocking wall

Reds chances of appearing are 3 in a hundred, kill em fast



