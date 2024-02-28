20 SECONDS 2 DIE

A straightforward 2D desktop game of bullet hell genre. Player dodges 12 diffrent aliens and their projectiles trying to survive and wrap up highest score.

Tech info:
Game is made in python using pyqt library, which itself is binding library for QT. It's an uni project for python course, so my language choice was quite limited, additionally QT was designed with static forms in mind so after finishing the project I can confidently say that it wasn't the right choice for a somewhat dynamic game. Project clocks in at around 1000 lines of code with 5 classes, instead of using events I opted to create interval refreshing at modifiable rate to mirror usual game logic, tying the game to ticks/frames per second instead. Game size is unoptimized, and I didn't spend any time modifying default processing power. I made limiting myself to one thread 

DOWNLOAD LINK : https://github.com/senior-devs-doom/python-desktop-game/releases/download/game/20.seconds.2.die.rar

Settings:
Threat - player score, incrementing with every enemy kill and each passed wave. Higher threat results in more enemies on screen.
Level - Difficulty setting, Each survived wave increases level by 1. Amount of enemy types able to be spawned is equal to level, capping at 12. Starting enemies are easy while later ones provide progressively increasing danger.
Frames - game speed, amount of game refresh happening in a second, designed with 60 in mind. All logic is tied to refreshes so once set to 30 it
