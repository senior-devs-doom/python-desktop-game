import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
import secrets  # cryptographically secure randomness, at worst 50% slower than normal one.
import keyboard  # pyqt gives me keyboard EVENTS, I need functions that return if key is pressed instead
import mouse # same thing lol
import math #tangens
class MainWindow(QMainWindow):#okno aplikacji
    def __init__(self,stylesheet, parent = None):#konstruktor głównego okna
      super().__init__()#konstruktor-rodzic QMainWindow
      self.setFixedSize(960, 540)
      self.setWindowIcon(QIcon('assets/player.png'))
      self.setWindowTitle("20 seconds 2 die")
      self.setStyleSheet(stylesheet)

      self.player=playerClass(self,stylesheet)

      self.timer = QTimer()
      self.timer.timeout.connect(lambda: tick(self,self.player))

      self.gameover=QLabel(self)
      self.gameover.move(0,50)
      self.gameover.resize(960,45)
      self.gameover.setText('GAME OVER!')
      self.gameover.setAlignment(Qt.AlignCenter)
      self.gameover.setObjectName('gameover')
      self.gameover.hide()

      self.livesLabel=QLabel(self)
      self.livesLabel.move(0,500)
      self.livesLabel.resize(120,25)
      self.livesLabel.setText('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
      self.livesLabel.setAlignment(Qt.AlignCenter)
      self.livesLabel.setObjectName('livesLabel')
      self.livesLabel.lower()
      self.livesLabel.hide()

      self.timeLabel=QLabel(self)
      self.timeLabel.move(0,100)
      self.timeLabel.resize(960,45)
      self.timeLabel.setText('PRESS ENTER TO START')
      self.timeLabel.setAlignment(Qt.AlignCenter)
      self.timeLabel.setObjectName('timeLabel')
      self.timeLabel.lower()

      self.score=QLabel(self)
      self.score.move(0,150)
      self.score.resize(960,30)
      self.score.setText('')
      self.score.setAlignment(Qt.AlignCenter)
      self.score.setObjectName('score')
      self.score.lower()

      self.valLabel1=QLabel(self)
      self.valLabel1.move(0,480)
      self.valLabel1.resize(120,25)
      self.valLabel1.setText('Threat: ')
      self.valLabel1.setAlignment(Qt.AlignCenter)
      self.valLabel1.setObjectName('valLabel')
      self.valLabel1.lower()

      self.val1=QLineEdit(self)
      self.val1.move(125,480)
      self.val1.resize(80,25)
      self.val1.setText('300')
      self.val1.setAlignment(Qt.AlignCenter)
      self.val1.setObjectName('valLabel')
      self.val1.lower()
      self.val1.setValidator(QIntValidator(1, 99999, self))

      self.valLabel2=QLabel(self)
      self.valLabel2.move(240,480)
      self.valLabel2.resize(120,25)
      self.valLabel2.setText('Level: ')
      self.valLabel2.setAlignment(Qt.AlignCenter)
      self.valLabel2.setObjectName('valLabel')
      self.valLabel2.lower()

      self.val2=QLineEdit(self)
      self.val2.move(365,480)
      self.val2.resize(80,25)
      self.val2.setText('1')
      self.val2.setAlignment(Qt.AlignCenter)
      self.val2.setObjectName('valLabel')
      self.val2.lower()
      self.val2.setValidator(QIntValidator(1, 12, self))

      self.valLabel3=QLabel(self)
      self.valLabel3.move(480,480)
      self.valLabel3.resize(120,25)
      self.valLabel3.setText('Frames: ')
      self.valLabel3.setAlignment(Qt.AlignCenter)
      self.valLabel3.setObjectName('valLabel')
      self.valLabel3.lower()

      self.val3=QLineEdit(self)
      self.val3.move(605,480)
      self.val3.resize(80,25)
      self.val3.setText('60')
      self.val3.setAlignment(Qt.AlignCenter)
      self.val3.setObjectName('valLabel')
      self.val3.lower()
      self.val3.setValidator(QIntValidator(1, 999, self))

      self.valLabel4=QLabel(self)
      self.valLabel4.move(720,480)
      self.valLabel4.resize(120,25)
      self.valLabel4.setText('Lives: ')
      self.valLabel4.setAlignment(Qt.AlignCenter)
      self.valLabel4.setObjectName('valLabel')
      self.valLabel4.lower()

      self.val4=QLineEdit(self)
      self.val4.move(860,480)
      self.val4.resize(80,25)
      self.val4.setText('3')
      self.val4.setAlignment(Qt.AlignCenter)
      self.val4.setObjectName('valLabel')
      self.val4.lower()
      self.val4.setValidator(QIntValidator(1, 99, self))
      
    def keyPressEvent(self, event):
            global isGameStart
            if not isGameStart:
                if event.key() == 16777220:
                    self.gameStart()
                    isGameStart=True
        
    def gameStart(self):
        global threat,threatmax,level,fps,frame,waveTime,sound
        isWave=True
        waveTime=20
        frame = 0
        self.player.death=False
        self.timeLabel.setText('20')
        threatmax=int(self.val1.text())
        threat=threatmax
        self.score.setText(str(threatmax))
        level=int(self.val2.text())
        fps=int(self.val3.text())
        self.timer.setInterval(int(1000/fps))#17 ms => 60 fps
        self.player.lives=int(self.val4.text())
        self.timer.start()
        self.livesLabel.show()
        self.livesLabel.setText('lives: '+str(self.player.lives))
        self.valLabel1.hide()
        self.valLabel2.hide()
        self.valLabel3.hide()
        self.valLabel4.hide()
        self.val1.hide()
        self.val2.hide()
        self.val3.hide()
        self.val4.hide()
        self.gameover.hide()
        sound['menuMusic'].stop()
        sound['mainMusic'].play()


class playerClass(QWidget):
    def __init__(self,parent,stylesheet):
        super(QWidget,self).__init__(parent)
        size=30
        #######################################HELL START#####################################################################33
        #Throwing player into graphic scene since its easiest way to support rotating HIM
        #player.graphicsview.scene.proxy.svg
        #THIS ARCHITECTURE IS SO ASSSSSSSSSSSSSS
        self.graphicsview = QGraphicsView(parent)
        self.graphicsview.resize((int)(size*1.41421356237),(int)(size*1.41421356237))#widget has to be flat 22 pixels bigger than the image inside to contain it WHO DESIGNED THIS???
        self.graphicsview.move(475,255)
        # to prevent the graphics view to draw its borders or background, set the
        # FrameShape property to 0 and a transparent background
        self.graphicsview.setFrameShape(0)
        # ignore scroll bars!
        self.graphicsview.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsview.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsview.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.scene = QGraphicsScene(self.graphicsview)
        self.graphicsview.setScene(self.scene)
    
        self.svg = QSvgWidget('assets/player1.svg')
        self.svg.setStyleSheet(stylesheet)
        self.svg.setObjectName('player')
        self.svg.resize(size,size)

        self.proxy = QGraphicsProxyWidget()
        self.proxy.setWidget(self.svg)
        self.proxy.setTransformOriginPoint(self.proxy.boundingRect().center())
        self.scene.addItem(self.proxy)
        self.lives=3
        self.iframes=0
        self.death=False


    def load(self,string):
        self.svg.load(string)
    
    def move(self,x,y):
        self.graphicsview.move(x,y)
    
    def setRotation(self,deg):
        self.proxy.setRotation(deg)

    def show(self):
        self.svg.show()

    def hide(self):
        self.svg.hide()
    
    def width(self):
        return self.svg.width()
    
    def height(self):
        return self.svg.height()
    
    def pos(self):
        return self.graphicsview.pos()
    
    def rotation(self):
        return self.proxy.rotation()
    
    def takeDamage(self):
        if not self.iframes:
            global sound
            sound['playerDamaged'].play()
            self.lives-=1
            self.parent().livesLabel.setText('lives: '+str(self.lives))
            self.iframes=120
            if self.lives==0:
                self.death=True
        #######################################HELL END#####################################################################

class Enemy(QSvgWidget):
    def __init__(self,parent=None,kind=0,color=0):
        super(QSvgWidget,self).__init__(parent)
        #maybe it's better to have these be global?
        global threat
        ratios=[8/11 , 1 , 8/12]#enemy sprites width to height ratio
        names=['crab','squid','octopus']#used when constructing enemy
        size=30 #width in pixels

        self.kind=kind
        self.name=names[kind]
        self.color=color
        self.isNormalMoving=True
        self.isShooting=0
        self.aimAngle=0
        self.hp=(kind+1) * ((color+1)*50)
        self.speed=2
        self.threat=((kind+1)*5) + ((color+1)*10)
        self.resize(size,int(size*ratios[kind]))
        self.load(enemySprites[kind][color][0])
        self.cooldown=0
        enemies.append(self)
        self.show()
        threat -= self.threat

    def delete(self):#boy I sure wish python deconstructors weren't useless
        global threat
        threat+=self.threat
        enemies.remove(self)
        self.deleteLater()
        Corpse(self)
    
    def ruch(self):
        if self.isNormalMoving:
            self.move( self.pos().x()+self.speed , self.pos().y() )#move x by 3

    def takeDamage(self,bullet,score):
        self.hp -= bullet.dmg
        bullet.delete()
        if self.hp <= 0:
            global threat,threatmax,sound
            sound['enemyDeath'].play()
            self.delete()
            threat += self.threat/20
            threatmax +=self.threat/20
            score.setText(str(threatmax))
    
    def attack(self,player):  
        global frame

        if self.kind == 0 and self.color==0:#white crab
            return

        if self.kind == 0 and self.color==1:#green crab
            if self.isNormalMoving:#speed set to 0 when it crosses player and starts attacking
                if self.speed < 0:#moves from right side
                    if player.pos().x() > self.pos().x():#crossed player
                        self.isNormalMoving=False
                        if player.pos().y() > self.pos().y():#player is above
                            self.aimAngle=1
                        else:
                            self.aimAngle=-1
                else:
                    if player.pos().x() < self.pos().x():
                        self.isNormalMoving=False
                        if player.pos().y() > self.pos().y():
                            self.aimAngle=1
                        else:
                            self.aimAngle=-1
            else:
                self.move( self.pos().x() , self.pos().y()+3*self.aimAngle )
            return
        
        #getting angle at which to fire
        if not self.isShooting:
            x=self.pos().x()-player.pos().x()
            y=player.pos().y()-self.pos().y()
            self.aimAngle = math.atan2(y, x)
        
        if self.kind == 0 and self.color==2:#yellow crab
            self.isNormalMoving=0
            self.speedX=self.speed*math.cos(self.aimAngle)*-1
            self.speedY=self.speed*math.sin(self.aimAngle)*1
            self.move( self.pos().x() + (int)(self.speedX) , self.pos().y()+(int)(self.speedY) )
            return
        
        #deciding when to attack
        if (self.cooldown==0):
            if self.color==3:#reds are more agressive, they always attack
                self.cooldown+=frame+120+secrets.randbelow(241)#fire in 2-6 seconds
            else:
                self.cooldown+=frame+120+secrets.randbelow(1201)#fire in 2-12 seconds
            return
        
        if self.cooldown<frame:#attack
            global sound
            #ONE FRAME ATTACKS
            if self.kind==1 and self.color==0:#white squid
                Bullet(self,self.aimAngle,0)
                self.cooldown=0
                sound['enemyShoot'].play()
                return
            if self.kind==1 and self.color==1:#green squid
                Bullet(self,self.aimAngle,0)
                Bullet(self,self.aimAngle+0.34,0)
                Bullet(self,self.aimAngle-0.34,0)
                self.cooldown=0
                sound['enemyShoot'].play()
                return
            if self.kind==1 and self.color==2:#yellow squid
                Bullet(self,self.aimAngle,1)
                self.cooldown=0
                sound['enemyShoot'].play()
                return
            if self.kind==2 and self.color==1:#green octopus
                Bullet(self,1.256,2)
                Bullet(self,2.512,2)
                Bullet(self,3.768,2)
                Bullet(self,5.024,2)
                Bullet(self,6.28,2)
                self.cooldown=0
                sound['enemyShoot'].play()
                return

            #MULTIFRAME ATTACKS
            if self.kind==0 and self.color==3:#red crab
                self.isNormalMoving=False
                self.isShooting+=1
                if self.isShooting==1:
                    self.speed=0
                if self.isShooting==40:
                    self.speed=-3
                if self.isShooting==60:
                    self.speed=4
                if self.isShooting>65:
                    if frame%20==0:#adjust charge
                        self.speed+=3
                        x=self.pos().x()-player.pos().x()
                        y=player.pos().y()-self.pos().y()   
                        currentAngle = math.atan2(y, x)
                        distanceTo0 = self.aimAngle-currentAngle
                        if distanceTo0 <0:distanceTo0*=-1
                        #Radians are annoying as hell, the radius goes like
                        #     pi/2
                        # 0         pi AND -pi
                        #    -pi/2
                        if distanceTo0 < 3.141:#go to left of the rad chart(to 0)
                            if self.aimAngle<currentAngle:
                                self.aimAngle+=0.23
                            else:
                                self.aimAngle-=0.23
                        else:                                           #cheat fix
                            self.aimAngle=currentAngle + 0.23           #cheat fix, makes him spawn of satan
                        if self.aimAngle <-3.14:self.aimAngle+=3.14     #cheat fix
                self.speedX=self.speed*math.cos(self.aimAngle)*-1
                self.speedY=self.speed*math.sin(self.aimAngle)*1
                self.move( self.pos().x() + (int)(self.speedX) , self.pos().y()+(int)(self.speedY) )
                return
            
            if self.kind==1 and self.color==3:#red squid
                x=self.pos().x()-player.pos().x()
                y=player.pos().y()-self.pos().y()#copypasted aimangle here, can't be asked to change architecture.
                self.aimAngle = math.atan2(y, x)
                if not self.isShooting:
                    self.isShooting+=1
                    sound['enemyShoot'].play()
                self.speed=0
                if frame%12==0:
                    if secrets.randbelow(int(2)):#coin flip 50/50k
                        direction=1
                    else:
                        direction=-1
                    marginerror=direction * (secrets.randbelow(int(35))/100)
                    Bullet(self,self.aimAngle+marginerror,0)
                return
                        
            if self.kind==2 and self.color==0:#white octopus
                if not self.isShooting:
                    sound['enemyShoot'].play()
                if frame%4==0:
                    if self.isShooting>=5:
                        self.cooldown=0
                        self.isShooting=0
                        return
                    else:
                        Bullet(self,self.aimAngle,3)
                        self.isShooting+=1
                return

            if self.kind==2 and self.color==2:#yellow octopus
                if not self.isShooting:
                    sound['enemyShoot'].play()
                if frame%4==0:
                    if self.isShooting>=5:
                        self.cooldown=0
                        self.isShooting=0
                        return
                    else:
                        Bullet(self,self.aimAngle,4)
                        self.isShooting+=1
                return

            if self.kind==2 and self.color==3:#red octopus
                if not self.isShooting:
                    sound['enemyShoot'].play()
                self.speed=0
                if frame%12==0:
                    Bullet(self,self.aimAngle,3)
                    self.isShooting+=1
            return

class Corpse(QSvgWidget):
    def __init__(self,parent):
        super(QSvgWidget,self).__init__(parent.parent())
        self.resize(parent.frameGeometry().width() , parent.frameGeometry().width())
        self.move(parent.pos().x() , parent.pos().y())
        self.load(enemySprites[parent.kind][parent.color][2])
        self.show()    
        self.timer = QTimer()
        self.timer.start(500)
        self.timer.timeout.connect(lambda: self.delete())
        
    def delete(self):
        self.timer.stop()
        self.deleteLater()

#Enemy and Player bullets constructors look nothing alike so I'm making them seperate classes, 
#later if they share methods I could merge them. 
#so far it's pointless to have parent class that's just "self.speed == exists"
class Bullet(QSvgWidget):
    def __init__(self,parent,direction,type=0):
        super(QSvgWidget,self).__init__(parent.parent())#dont ask me why Enemy(QSvgWidget) can't have children, I'm not the one that neutered him.
        self.angle=direction
        self.type=type
        self.resize(10,10)

        if type==0:
            self.speed=5
            self.load('assets/bullet1.svg')

        if type==1:
            self.speed=4
            self.load('assets/bullet1.2.svg')
            self.bounceCount=3

        if type>=2:
            self.speed=3
            self.resize(15,15)
            self.load('assets/bullet2.svg')
            self.specialmovement=5

        self.PrecisePosX=parent.pos().x()+10#position needs to be done in floats, ints have large rounding errors
        self.PrecisePosY=parent.pos().y()+10
        self.move(round(self.PrecisePosX),round(self.PrecisePosY))
        self.speedX=self.speed*math.cos(direction)*-1
        self.speedY=self.speed*math.sin(direction)*1
        self.show()
        bullets.append(self)

    def bounce(self):#960, 540
        if self.bounceCount:
            if self.pos().x() < 0:
                self.speedX*=-1
                self.bounceCount-=1
                self.move(1, self.pos().y())
            if self.pos().x() > 950:
                self.speedX*=-1
                self.bounceCount-=1
            if self.pos().y() < 0:
                self.speedY*=-1
                self.bounceCount-=1
                self.move(self.pos().x(),1)
            if self.pos().y() > 530:
                self.speedY*=-1
                self.bounceCount-=1

    def ruch(self):
        self.PrecisePosX+=self.speedX
        self.PrecisePosY+=self.speedY

        if self.type==3:#octopus
            if self.specialmovement<=10:
                self.PrecisePosX+=math.cos(self.angle+1.5707)*-2
                self.PrecisePosY+=math.sin(self.angle+1.5707)*2
            else:
                self.PrecisePosX+=math.cos(self.angle+1.5707)*2
                self.PrecisePosY+=math.sin(self.angle+1.5707)*-2
            self.specialmovement+=1
            if self.specialmovement>=22:
                self.specialmovement=0

        if self.type==4:#octopus
                circle=self.specialmovement*3.14/20
                self.PrecisePosX+=math.cos(self.angle+circle)*-2
                self.PrecisePosY+=math.sin(self.angle+circle)*2
                self.specialmovement+=1

        self.move( round(self.PrecisePosX), round(self.PrecisePosY) )

    def delete(self):#boy I sure wish python deconstructors weren't useless
        bullets.remove(self)
        self.deleteLater()

class BulletP(QSvgWidget):
    def __init__(self,parent,player,PbulletSide):
        global sound
        super(QSvgWidget,self).__init__(parent)
        self.speed=10
        self.dmg=50
        angle=math.radians(player.rotation()+90)
        self.load('assets/bulletP.svg')
        self.resize(7,7)
        self.PrecisePosX=player.pos().x()+15#position needs to be done in floats, ints have large rounding errors
        self.PrecisePosY=player.pos().y()+15

        if PbulletSide:
            self.PrecisePosX+=math.sin(angle)*-11
            self.PrecisePosY+=math.cos(angle)*11
        else:
            self.PrecisePosX+=math.sin(angle)*11
            self.PrecisePosY+=math.cos(angle)*-11

        self.move(round(self.PrecisePosX),round(self.PrecisePosY))
        self.speedX=self.speed*math.cos(angle)*-1
        self.speedY=self.speed*math.sin(angle)*-1
        self.lower()
        self.show()
        bullets.append(self)
    def ruch(self):
        self.PrecisePosX+=self.speedX
        self.PrecisePosY+=self.speedY
        self.move( round(self.PrecisePosX), round(self.PrecisePosY) )

    def delete(self):#boy I sure wish python deconstructors weren't useless
        bullets.remove(self)
        self.deleteLater()
           
def tick(window,player):#główne odświeżanie
    global threatmax
    global frame
    global waveTime
    global isWave
    global enemies
    global bullets
    global level
    global iframeFlashing
    #Use this function if one array with enemies ever fails
    #window.findChildren(Enemy)
    frame+=1
    #timer
    if frame%60==0:
        waveTime-=1
        if waveTime==0:
            if isWave:#end wave
                while len(enemies):
                    enemies[0].delete()
                while len(bullets):
                    bullets[0].delete()
                waveTime=5
                isWave=False
                threatmax+=50
                window.score.setText(str(threatmax))
            else:#start wave
                waveTime=20
                isWave=True
                level+=1
        window.timeLabel.setText(str(waveTime))
    #ruch
    ruchP(player)
    for enemy in enemies:
        enemy.ruch()
    for bullet in bullets:
        bullet.ruch()
    #animacja
    if frame%30 == 0:#co pół sekundy,zmień sprite
        #print(len(window.findChildren(Enemy))) #papa's debug print
        global animFlag
        for enemy in enemies:
            AnimeE(enemy)
        AnimP(player)
        if animFlag:
            animFlag=False
        else:
            animFlag=True 
    #obróć gracza do myszki
    RotateToMouse(player,frame)
    #strzelanie
    if mouse.is_pressed(button='left') and frame%15 == 0:
        shootP(window,player)
    #spawning
    if(threat>0 and frame%10 == 0 and isWave):
        SpawnRow(window,4)
    
    for enemy in enemies:
        if isTouchingBroad(enemy,player):#collision checks
            player.takeDamage()
        enemy.attack(player)

    for bullet in bullets:
        if isinstance(bullet, BulletP):#friendly bullet
            for enemy in enemies:
                if isTouchingBroad(enemy,bullet):#collision checks
                    enemy.takeDamage(bullet,window.score)#takeDamage deletes projectile, must be followed by break, updates score
                    break
        else:#not friendy bullet
            if bullet.type==1:
                bullet.bounce()
            if isTouchingBroad(bullet,player):#collision checks
                player.takeDamage()
                bullet.delete()
    #despawning if out of bounds
    for enemy in enemies:
        OutOfBounds(enemy)
    for bullet in bullets:
        OutOfBounds(bullet)

    #player iframes
    if player.iframes>0:
        player.iframes-=1
        if iframeFlashing:
            iframeFlashing=False
            player.show()
        else:
            iframeFlashing=True
            player.hide()
    else:
        player.show()
    #gameover
    
    if player.death:
        global isGameStart
        while len(enemies):
            enemies[0].delete()
        while len(bullets):
            bullets[0].delete()
        window.gameover.show()
        window.timeLabel.setText("You have survived "+str(round(frame/fps*10)/10)+" seconds!")
        window.score.setText("final score: "+ str(window.score.text()))
        window.timer.stop()
        player.move(475,255)
        player.setRotation(0)
        isGameStart=False
        window.valLabel1.show()
        window.valLabel2.show()
        window.valLabel3.show()
        window.valLabel4.show()
        window.val1.show()
        window.val2.show()
        window.val3.show()
        window.val4.show()
        window.livesLabel.hide()
        

def ruchP(player):
    plX=player.pos().x()
    plY=player.pos().y()
    if keyboard.is_pressed('w') or keyboard.is_pressed('up'):
        plY-=3
    if keyboard.is_pressed('a') or keyboard.is_pressed('left'):
        plX-=3
    if keyboard.is_pressed('s') or keyboard.is_pressed('down'):
        plY+=3
    if keyboard.is_pressed('d') or keyboard.is_pressed('right'):
        plX+=3
    if plX < 0:
        plX=0
    if plX >930:#window width - player size, 960-30
     plX=930
    if plY <0:
        plY=0
    if plY>510:
        plY=510
    player.move(plX,plY)

def AnimeE(enemy):
    global animFlag
    if animFlag:
        enemy.load(enemySprites[enemy.kind][enemy.color][0])
    else:
        enemy.load(enemySprites[enemy.kind][enemy.color][1])
    
def AnimP(player):
    global animFlag
    if animFlag:
        player.load('assets/player1.svg')
    else:
        player.load('assets/player2.svg')

def RotateToMouse(player,frame):
    x=mouse.get_position()[0]-player.mapToGlobal(QPoint(player.pos())).x()-15
    y=player.mapToGlobal(QPoint(player.pos())).y()-mouse.get_position()[1]+15
    #/\ that way player position is at (0,0), x positive is right, y positive is up
    #bcs of that we now spin in opposite direction than setrotation() hence -atan
    #+/- 15 is player size, puts the point in his middle
    if not x:#if eliminates tan = doesn't exist
        x=0.001
    atan=math.degrees(math.atan2(y, x))
    player.setRotation(90-atan)#90 is there to put 0 deg at y=0

def SpawnRow(window,length):#bit unoptimal, creates positions for other enemies then overwrites it. But comfy so might be fine.
    firstEnemy = SpawnE(window)
    posX = firstEnemy.pos().x()
    posY = firstEnemy.pos().y()
    if firstEnemy.speed > 0:#if speed is going opposite direction
        direction=1
    else:
        direction=-1
    for i in range(length-1):
        newEnemy = SpawnE(window)
        newEnemy.move(posX - ((i+1)*30*direction) , posY)
        newEnemy.speed = firstEnemy.speed

def SpawnE(window):
    Kind,Color=RandKC()
    newEnemy = Enemy(window,Kind,Color)
    if secrets.randbelow(int(2)):#coin flip 50/50k
        posX=960#windowwidth
        newEnemy.speed*=-1#reverse direction
    else:
        posX=-30
    posY=secrets.randbelow(int(540-30))#Ywindow height - size
    newEnemy.move(posX,posY)
    return newEnemy#let's keep to this guy a little longer after creating it

def RandKC():
    global level,SpawnRange
    if level>11:
        range=SpawnRange[11]
    else:
        range=SpawnRange[level-1]
    seed=secrets.randbelow(range+1)
    if seed<=32:
        return [0,0]
    if seed<=48:
        return [1,0]
    if seed<=56:
        return [2,0]
    if seed<=72:
        return [0,1]
    if seed<=80:
        return [1,1]
    if seed<=84:
        return [2,1]
    if seed<=92:
        return [0,2]
    if seed<=96:
        return [1,2]
    if seed<=98:
        return [2,2]
    if seed<=99:
        return [0,3]
    if seed<=100:
        return [1,3]
    else:
        return [2,3]


def OutOfBounds(object):
    if object.pos().x() < -200 or object.pos().x() > 1160  or  object.pos().y() < 0 or object.pos().y() > 640:
        object.delete()

def isTouchingBroad(object1,object2): #this is AABB broad detection and simplifies objects to rectangles, might need to go more detail after it.
    if object1.pos().x()+object1.width() > object2.pos().x():                 #object 1 end is to right of where object 2 begins
     if object1.pos().x()                 < object2.pos().x()+object2.width(): #object 1 begin is to left of where object 2 ends
      if object1.pos().y()+object1.height()> object2.pos().y():                 #object 1 end is above of where object 2 begins
       if object1.pos().y()                 < object2.pos().y()+object2.height():#object 1 begin is under of where object 2 ends
        return True
    return False

def shootP(window,player):#creates player bullet
    global PbulletSide
    global sound
    #sound['playerShoot'].play()
    PbulletSide = False if PbulletSide else True#flips between true false. WHERE IS MY "?" OPERATOR PYTHON? YOU CHEAPSKATE
    BulletP(window,player,PbulletSide) 
    

def debugSpawn(window):
    for i in range(3):
        for j in range(4):
            donald=Enemy(window,i,j)
            donald.move((i+1)*160,(j+1)*100)
            donald.speed=0

def makeSound(path):
    url= QUrl.fromLocalFile(path)
    content= QMediaContent(url)
    player = QMediaPlayer()
    player.setMedia(content)
    return player



#pyqt load() break at smallest sizes, so I need backgroung graphic to fill in broken gaps
enemySprites=[#enemies  
    #[enemy][color][sprite]
    #[crab,squid,octopus],[white,green,yellow,red][1,2,ded]
    [#crab
        [#white
            b'<svg viewBox="0 -0.5 11 8" shape-rendering="crispEdges"><path stroke="#ffffff" d="M2 0h1M8 0h1M3 1h1M7 1h1M2 2h7M1 3h2M4 3h3M8 3h2M0 4h11M0 5h1M2 5h7M10 5h1M0 6h1M2 6h1M8 6h1M10 6h1M3 7h2M6 7h2" /></svg>', 
            b'<svg viewBox="0 -0.5 11 8" shape-rendering="crispEdges"><path stroke="#ffffff" d="M0 0h1M2 0h1M8 0h1M10 0h1M0 1h1M3 1h1M7 1h1M10 1h1M0 2h1M2 2h7M10 2h1M0 3h3M4 3h3M8 3h3M1 4h9M2 5h7M2 6h1M8 6h1M0 7h2M9 7h2" /></svg>', 
            b'<svg viewBox="0 -0.5 10 8" shape-rendering="crispEdges"><path stroke="#ffffff" d="M1 0h1M4 0h1M7 0h1M2 1h1M4 1h1M6 1h1M1 3h1M6 3h1M8 3h1M0 4h1M2 4h1M7 4h1M9 4h1M2 6h1M4 6h1M6 6h1M1 7h1M4 7h1M7 7h1" /></svg>'
        ],
        [#green
            b'<svg viewBox="0 -0.5 11 8" shape-rendering="crispEdges"><path stroke="#59cf11" d="M2 0h1M8 0h1M3 1h1M7 1h1M2 2h7M1 3h2M4 3h3M8 3h2M0 4h11M0 5h1M2 5h7M10 5h1M0 6h1M2 6h1M8 6h1M10 6h1M3 7h2M6 7h2" /></svg>', 
            b'<svg viewBox="0 -0.5 11 8" shape-rendering="crispEdges"><path stroke="#59cf11" d="M0 0h1M2 0h1M8 0h1M10 0h1M0 1h1M3 1h1M7 1h1M10 1h1M0 2h1M2 2h7M10 2h1M0 3h3M4 3h3M8 3h3M1 4h9M2 5h7M2 6h1M8 6h1M0 7h2M9 7h2" /></svg>', 
            b'<svg viewBox="0 -0.5 10 8" shape-rendering="crispEdges"><path stroke="#59cf11" d="M1 0h1M4 0h1M7 0h1M2 1h1M4 1h1M6 1h1M1 3h1M6 3h1M8 3h1M0 4h1M2 4h1M7 4h1M9 4h1M2 6h1M4 6h1M6 6h1M1 7h1M4 7h1M7 7h1" /></svg>'
        ],
        [#yellow
            b'<svg viewBox="0 -0.5 11 8" shape-rendering="crispEdges"><path stroke="#dbb80b" d="M2 0h1M8 0h1M3 1h1M7 1h1M2 2h7M1 3h2M4 3h3M8 3h2M0 4h11M0 5h1M2 5h7M10 5h1M0 6h1M2 6h1M8 6h1M10 6h1M3 7h2M6 7h2" /></svg>', 
            b'<svg viewBox="0 -0.5 11 8" shape-rendering="crispEdges"><path stroke="#dbb80b" d="M0 0h1M2 0h1M8 0h1M10 0h1M0 1h1M3 1h1M7 1h1M10 1h1M0 2h1M2 2h7M10 2h1M0 3h3M4 3h3M8 3h3M1 4h9M2 5h7M2 6h1M8 6h1M0 7h2M9 7h2" /></svg>', 
            b'<svg viewBox="0 -0.5 10 8" shape-rendering="crispEdges"><path stroke="#dbb80b" d="M1 0h1M4 0h1M7 0h1M2 1h1M4 1h1M6 1h1M1 3h1M6 3h1M8 3h1M0 4h1M2 4h1M7 4h1M9 4h1M2 6h1M4 6h1M6 6h1M1 7h1M4 7h1M7 7h1" /></svg>'
        ],
        [#red
            b'<svg viewBox="0 -0.5 11 8" shape-rendering="crispEdges"><path stroke="#910b09" d="M2 0h1M8 0h1M3 1h1M7 1h1M2 2h7M1 3h2M4 3h3M8 3h2M0 4h11M0 5h1M2 5h7M10 5h1M0 6h1M2 6h1M8 6h1M10 6h1M3 7h2M6 7h2" /></svg>', 
            b'<svg viewBox="0 -0.5 11 8" shape-rendering="crispEdges"><path stroke="#910b09" d="M0 0h1M2 0h1M8 0h1M10 0h1M0 1h1M3 1h1M7 1h1M10 1h1M0 2h1M2 2h7M10 2h1M0 3h3M4 3h3M8 3h3M1 4h9M2 5h7M2 6h1M8 6h1M0 7h2M9 7h2" /></svg>', 
            b'<svg viewBox="0 -0.5 10 8" shape-rendering="crispEdges"><path stroke="#910b09" d="M1 0h1M4 0h1M7 0h1M2 1h1M4 1h1M6 1h1M1 3h1M6 3h1M8 3h1M0 4h1M2 4h1M7 4h1M9 4h1M2 6h1M4 6h1M6 6h1M1 7h1M4 7h1M7 7h1" /></svg>'
        ]
    ],
    [#squid
        [#white
            b'<svg viewBox="0 -0.5 8 8" shape-rendering="crispEdges"><path stroke="#ffffff" d="M3 0h2M2 1h4M1 2h6M0 3h2M3 3h2M6 3h2M0 4h8M2 5h1M5 5h1M1 6h1M3 6h2M6 6h1M0 7h1M2 7h1M5 7h1M7 7h1" /></svg>', 
            b'<svg viewBox="0 -0.5 8 8" shape-rendering="crispEdges"><path stroke="#ffffff" d="M3 0h2M2 1h4M1 2h6M0 3h2M3 3h2M6 3h2M0 4h8M1 5h1M6 5h1M0 6h1M7 6h1M1 7h1M6 7h1" /></svg>', 
            b'<svg viewBox="0 -0.5 8 8" shape-rendering="crispEdges"><path stroke="#ffffff" d="M1 0h1M3 0h1M7 0h1M4 1h1M0 3h1M2 3h1M6 3h1M1 4h1M5 4h1M7 4h1M3 6h1M1 7h1M4 7h1M7 7h1" /></svg>'
        ],
        [#green
            b'<svg viewBox="0 -0.5 8 8" shape-rendering="crispEdges"><path stroke="#59cf11" d="M3 0h2M2 1h4M1 2h6M0 3h2M3 3h2M6 3h2M0 4h8M2 5h1M5 5h1M1 6h1M3 6h2M6 6h1M0 7h1M2 7h1M5 7h1M7 7h1" /></svg>', 
            b'<svg viewBox="0 -0.5 8 8" shape-rendering="crispEdges"><path stroke="#59cf11" d="M3 0h2M2 1h4M1 2h6M0 3h2M3 3h2M6 3h2M0 4h8M1 5h1M6 5h1M0 6h1M7 6h1M1 7h1M6 7h1" /></svg>', 
            b'<svg viewBox="0 -0.5 8 8" shape-rendering="crispEdges"><path stroke="#59cf11" d="M1 0h1M3 0h1M7 0h1M4 1h1M0 3h1M2 3h1M6 3h1M1 4h1M5 4h1M7 4h1M3 6h1M1 7h1M4 7h1M7 7h1" /></svg>'
        ],
        [#yellow
            b'<svg viewBox="0 -0.5 8 8" shape-rendering="crispEdges"><path stroke="#dbb80b" d="M3 0h2M2 1h4M1 2h6M0 3h2M3 3h2M6 3h2M0 4h8M2 5h1M5 5h1M1 6h1M3 6h2M6 6h1M0 7h1M2 7h1M5 7h1M7 7h1" /></svg>', 
            b'<svg viewBox="0 -0.5 8 8" shape-rendering="crispEdges"><path stroke="#dbb80b" d="M3 0h2M2 1h4M1 2h6M0 3h2M3 3h2M6 3h2M0 4h8M1 5h1M6 5h1M0 6h1M7 6h1M1 7h1M6 7h1" /></svg>', 
            b'<svg viewBox="0 -0.5 8 8" shape-rendering="crispEdges"><path stroke="#dbb80b" d="M1 0h1M3 0h1M7 0h1M4 1h1M0 3h1M2 3h1M6 3h1M1 4h1M5 4h1M7 4h1M3 6h1M1 7h1M4 7h1M7 7h1" /></svg>'
        ],
        [#red
            b'<svg viewBox="0 -0.5 8 8" shape-rendering="crispEdges"><path stroke="#910b09" d="M3 0h2M2 1h4M1 2h6M0 3h2M3 3h2M6 3h2M0 4h8M2 5h1M5 5h1M1 6h1M3 6h2M6 6h1M0 7h1M2 7h1M5 7h1M7 7h1" /></svg>', 
            b'<svg viewBox="0 -0.5 8 8" shape-rendering="crispEdges"><path stroke="#910b09" d="M3 0h2M2 1h4M1 2h6M0 3h2M3 3h2M6 3h2M0 4h8M1 5h1M6 5h1M0 6h1M7 6h1M1 7h1M6 7h1" /></svg>', 
            b'<svg viewBox="0 -0.5 8 8" shape-rendering="crispEdges"><path stroke="#910b09" d="M1 0h1M3 0h1M7 0h1M4 1h1M0 3h1M2 3h1M6 3h1M1 4h1M5 4h1M7 4h1M3 6h1M1 7h1M4 7h1M7 7h1" /></svg>'
        ]
    ],
    [#octopus
        [#white
            b'<svg viewBox="0 -0.5 12 8" shape-rendering="crispEdges"><path stroke="#ffffff" d="M4 0h4M1 1h10M0 2h12M0 3h3M5 3h2M9 3h3M0 4h12M2 5h3M7 5h3M1 6h2M5 6h2M9 6h2M2 7h2M8 7h2" /></svg>', 
            b'<svg viewBox="0 -0.5 12 8" shape-rendering="crispEdges"><path stroke="#ffffff" d="M4 0h4M1 1h10M0 2h12M0 3h3M5 3h2M9 3h3M0 4h12M2 5h3M7 5h3M2 6h2M5 6h2M8 6h2M0 7h2M10 7h2" /></svg>', 
            b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -0.5 11 8" shape-rendering="crispEdges"><metadata>Made with Pixels to Svg https://codepen.io/shshaw/pen/XbxvNj</metadata><path stroke="#ffffff" d="M0 0h1M5 0h1M9 0h1M1 1h2M4 1h1M7 1h2M0 3h1M2 3h1M6 3h1M8 3h1M10 3h1M1 4h1M3 4h1M7 4h1M9 4h1M1 6h2M5 6h1M7 6h2M0 7h1M4 7h1M9 7h1" /></svg>'
        ],
        [#green
            b'<svg viewBox="0 -0.5 12 8" shape-rendering="crispEdges"><path stroke="#59cf11" d="M4 0h4M1 1h10M0 2h12M0 3h3M5 3h2M9 3h3M0 4h12M2 5h3M7 5h3M1 6h2M5 6h2M9 6h2M2 7h2M8 7h2" /></svg>', 
            b'<svg viewBox="0 -0.5 12 8" shape-rendering="crispEdges"><path stroke="#59cf11" d="M4 0h4M1 1h10M0 2h12M0 3h3M5 3h2M9 3h3M0 4h12M2 5h3M7 5h3M2 6h2M5 6h2M8 6h2M0 7h2M10 7h2" /></svg>', 
            b'<svg viewBox="0 -0.5 11 8" shape-rendering="crispEdges"><path stroke="#59cf11" d="M0 0h1M5 0h1M9 0h1M1 1h2M4 1h1M7 1h2M0 3h1M2 3h1M6 3h1M8 3h1M10 3h1M1 4h1M3 4h1M7 4h1M9 4h1M1 6h2M5 6h1M7 6h2M0 7h1M4 7h1M9 7h1" /></svg>'
        ],
        [#yellow
            b'<svg viewBox="0 -0.5 12 8" shape-rendering="crispEdges"><path stroke="#dbb80b" d="M4 0h4M1 1h10M0 2h12M0 3h3M5 3h2M9 3h3M0 4h12M2 5h3M7 5h3M1 6h2M5 6h2M9 6h2M2 7h2M8 7h2" /></svg>', 
            b'<svg viewBox="0 -0.5 12 8" shape-rendering="crispEdges"><path stroke="#dbb80b" d="M4 0h4M1 1h10M0 2h12M0 3h3M5 3h2M9 3h3M0 4h12M2 5h3M7 5h3M2 6h2M5 6h2M8 6h2M0 7h2M10 7h2" /></svg>', 
            b'<svg viewBox="0 -0.5 11 8" shape-rendering="crispEdges"><path stroke="#dbb80b" d="M0 0h1M5 0h1M9 0h1M1 1h2M4 1h1M7 1h2M0 3h1M2 3h1M6 3h1M8 3h1M10 3h1M1 4h1M3 4h1M7 4h1M9 4h1M1 6h2M5 6h1M7 6h2M0 7h1M4 7h1M9 7h1" /></svg>'
        ],
        [#red
            b'<svg viewBox="0 -0.5 12 8" shape-rendering="crispEdges"><path stroke="#910b09" d="M4 0h4M1 1h10M0 2h12M0 3h3M5 3h2M9 3h3M0 4h12M2 5h3M7 5h3M1 6h2M5 6h2M9 6h2M2 7h2M8 7h2" /></svg>', 
            b'<svg viewBox="0 -0.5 12 8" shape-rendering="crispEdges"><path stroke="#910b09" d="M4 0h4M1 1h10M0 2h12M0 3h3M5 3h2M9 3h3M0 4h12M2 5h3M7 5h3M2 6h2M5 6h2M8 6h2M0 7h2M10 7h2" /></svg>', 
            b'<svg viewBox="0 -0.5 11 8" shape-rendering="crispEdges"><path stroke="#910b09" d="M0 0h1M5 0h1M9 0h1M1 1h2M4 1h1M7 1h2M0 3h1M2 3h1M6 3h1M8 3h1M10 3h1M1 4h1M3 4h1M7 4h1M9 4h1M1 6h2M5 6h1M7 6h2M0 7h1M4 7h1M9 7h1" /></svg>'
        ]
    ]
]
SpawnRange=[32,48,56,72,80,84,92,96,98,99,100,101]
sound = {
    'enemyDeath': makeSound("assets/pokemonfaintgen3.wav"),
    'playerDamaged': makeSound("assets/pokemonbite.wav"),
    'playerShoot': makeSound("assets/pew.wav"),
    'enemyShoot': makeSound("assets/space-invader-shoot-arcade-game-fx_120bpm.wav"),
    'mainMusic' : makeSound("assets/PopcornRemix_HD_JohnnyBraveOfficial.wav"),
    'menuMusic' : makeSound("assets/8bit-loading-pixabay.wav")
}
sound['enemyShoot'].setVolume(20)
sound['enemyDeath'].setVolume(60)
threatmax = 0
threat = threatmax
waveTime=60
level=1
frame = 0
fps=0
enemies = []
bullets = []
PbulletSide=True#used to make player bullets shoot from left/right side of him
isGameStart=False
iframeFlashing=True
isWave=True
animFlag = True#2 frame animation, flag used to flip between the frames

def main():
    global sound
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont("assets/VerminVibes1989.ttf")
    stylesheet= open('assets/stylesheet.qss').read()
    window = MainWindow(stylesheet)
    window.show()
    sound['menuMusic'].play()
    
    #debugSpawn(window)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
   