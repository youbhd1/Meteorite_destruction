import pygame
import sys
import random
import os
from time import sleep
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_SPACE

# 화면구성 (검정배경, 500*750)
padWidth = 500  # 가로크기
padHeight = 750 # 세로크기

# 플레이어 비행선
plyaerShips = [
    'asset/game_02/players/Spaceship_01.png', 'asset/game_02/players/Spaceship_02.png', 'asset/game_02/players/Spaceship_03.png',
    'asset/game_02/players/Spaceship_04.png', 'asset/game_02/players/Spaceship_05.png', 'asset/game_02/players/Spaceship_06.png',
    'asset/game_02/players/Spaceship_07.png'
]

# 우주쓰레기
spaceGarbages = [
    'asset/game_02/garbages/garbages_01.png', 'asset/game_02/garbages/garbages_02.png', 'asset/game_02/garbages/garbages_03.png', 'asset/game_02/garbages/garbages_04.png',
    'asset/game_02/garbages/garbages_05.png', 'asset/game_02/garbages/garbages_06.png', 'asset/game_02/garbages/garbages_07.png', 'asset/game_02/garbages/garbages_08.png',
    'asset/game_02/garbages/garbages_09.png', 'asset/game_02/garbages/garbages_10.png', 'asset/game_02/garbages/garbages_11.png', 'asset/game_02/garbages/garbages_12.png',
    'asset/game_02/garbages/garbages_13.png', 'asset/game_02/garbages/garbages_14.png', 'asset/game_02/garbages/garbages_15.png', 'asset/game_02/garbages/garbages_16.png',
    'asset/game_02/garbages/garbages_17.png', 'asset/game_02/garbages/garbages_18.png', 'asset/game_02/garbages/garbages_19.png',
]

# 플레이어 총알
playerBullets = [
    'asset/game_02/bullet/bullet_01.png', 'asset/game_02/bullet/bullet_02.png', 'asset/game_02/bullet/bullet_03.png'
]

# 파괴 이펙트
garbageExplosions = [
    'asset/game_02/effects/explosion_01.png', 'asset/game_02/effects/explosion_02.png', 'asset/game_02/effects/explosion_03.png', 'asset/game_02/effects/explosion_04.png'
]

# 파괴 사운드
garbageExplosionSounds = [
    'asset/game_02/sounds/explosion_01.wav', 'asset/game_02/sounds/explosion_02.wav', 'asset/game_02/sounds/explosion_03.wav', 'asset/game_02/sounds/explosion_04.wav'
]

# 총알 사운드
bulletFlyingSounds = [
    'asset/game_02/sounds/bullet.wav'
]

# 오브젝트 세팅 (오브젝트, x값, y값)
def setObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

# 폰트 세팅
def setFont(fontNm, fontSiez):
    if(fontNm == ''):
        fontNm = 'asset/game_02/fonts/NanumGothic.ttf'
        font = pygame.font.Font(fontNm, fontSiez)
        return font

# 파괴한 수 체크
def writeLogScore(count):
    global gamePad
    font = setFont('', 20)
    text = font.render('파괴된 쓰레기 수: ' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))

# 놓친 수 체크
def writeLogPassed(count):
    global gamePad
    font = setFont('', 20)
    text = font.render('놓친 쓰레기 수: ' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (10, 25))

# 결과 출력
def writeOutput(text, textSize):
    global gamePad
    font = setFont('', textSize)
    text = font.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    sleep(2)
    runGame()

# 우주쓰레기와 충돌
def crash():
    global gamePad
    writeOutput('쓰레기와 충돌했습니다.', 35)

# 게임오버
def gameOver():
    global gamePad
    writeOutput('게임 오버!', 60)
    
# 플레이어 설정
def players():
    global player, playerSize, playerWidth, playerHeight
    player = pygame.image.load(random.choice(plyaerShips))
    player = pygame.transform.scale(player,(90,90))
    
    # 크기 설정
    playerSize = player.get_rect().size
    playerWidth = playerSize[0]
    playerHeight = playerSize[1]

# 플레이어 총알 설정
def bullets():
    global bullet, bulletXY
    bullet = pygame.image.load(random.choice(playerBullets))
    bullet = pygame.transform.scale(bullet,(10,45))

    bulletXY = []

# 우주쓰레기 설정
def garbages():
    global garbage, garbageSize, garbageWidth, garbageHeight, garbageSpeed
    garbage = pygame.image.load(random.choice(spaceGarbages))
    garbage = pygame.transform.scale(garbage,(100,100))

    # 크기 설정
    garbageSize = garbage.get_rect().size
    garbageWidth = garbageSize[0]
    garbageHeight = garbageSize[1]

# 폭발이펙트
def garbageEffects():
    global effect
    effect = pygame.image.load(random.choice(garbageExplosions))
    effect = pygame.transform.scale(effect,(150,150))

# 사운드
def sounds(soundNm):
    global sound
    sound = pygame.mixer.Sound(random.choice(soundNm))
    return sound

# 게임 초기화 및 각 설정 
def initGame():
    global gamePad, clock, background

    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('Devdog Shooting')                  # 게임명칭
    background = pygame.image.load('asset/game_02/background.png') # 게임배경

    # 플레이어
    players()

    # 플레이어 총알
    bullets()

    # 우주쓰레기
    garbages()

    clock = pygame.time.Clock()

def runGame():
    global gamePad, clock, background

    # 플레이어 위치
    _player_x = padWidth * 0.45
    _player_y = padHeight * 0.88
    playerX = 0

    # 우주쓰레기 위치
    _garbage_x = random.randrange(0, padWidth - garbageWidth)
    _garbage_y = 0
    garbageSpeed = 2

    # 게임플레이 여부
    onGame = False

    # 우주쓰레기 명중여부, 명중 카운트
    isShot = False
    shotCount = 0

    # 우주쓰레기 비명중, 통과 카운트
    garbagePassed = 0

    # 플레이어 총알 수
    bulletCount = 0
        
    while not onGame:
        for event in pygame.event.get():
            # 게임종료처리
            if event.type in [QUIT]:
                pygame.quit()
                sys.exit()

            # 플레이어 컨트롤
            if event.type in [KEYDOWN]:
                if event.key == K_LEFT:
                    playerX -= 5

                elif event.key == K_RIGHT:
                    playerX += 5

                elif event.key == K_SPACE:
                    # 총알사운드
                    bulletFlySound = sounds(bulletFlyingSounds)
                    bulletFlySound.play()
                    
                    _bullet_x = _player_x + playerWidth/2
                    _bullet_y = _player_y - playerHeight
                    bulletXY.append([_bullet_x, _bullet_y])

            if event.type in [pygame.KEYUP]:
                if event.key == K_LEFT or event.key == K_RIGHT:
                    playerX = 0

        setObject(background, 0, 0)

        _player_x += playerX
        if _player_x < 0:
            _player_x = 0
        elif _player_x > padWidth - playerWidth:
            _player_x = padWidth - playerWidth

        # 우주쓰레기와 전투기 충돌
        if _player_y < _garbage_y + garbageHeight:
            if(_garbage_x > _player_x and _garbage_x < _player_x + playerWidth) or \
                (_garbage_x + garbageWidth > _player_x and _garbage_x + garbageWidth < _player_x + playerWidth): 
                crash()

        setObject(player, _player_x, _player_y)

        # 플레이어 총알 컨트롤
        if len(bulletXY) != 0:
            for i, bxy in enumerate(bulletXY):
                bxy[1] -= 5
                bulletXY[i][1] = bxy[1]

                # 우주쓰레기 명중 분기
                if bxy[1] < _garbage_y:
                    if bxy[0] > _garbage_x and bxy[0] < _garbage_x + garbageWidth:
                        bulletXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                if bxy[1] <= 0:
                    try:
                        bulletXY.remove(bxy)
                    except:
                        pass

        if len(bulletXY) != 0:
            for bx, by in bulletXY:
                setObject(bullet, bx, by)

        writeLogScore(shotCount)

        # 우주쓰레기 컨트롤
        _garbage_y += garbageSpeed
        if _garbage_y > padHeight:
            garbages()
            _garbage_x = random.randrange(0, padWidth - garbageWidth)
            _garbage_y = 0
            garbagePassed += 1

        # 우주쓰레기 놓쳤을 때 
        if garbagePassed == 5:
            gameOver()

        writeLogPassed(garbagePassed)
        
        # 우주쓰레기 명중 분기
        if isShot:
            garbageEffects()
            setObject(effect, _garbage_x, _garbage_y)
            
            # 충돌 사운드
            garbageDistorySound = sounds(garbageExplosionSounds)
            garbageDistorySound.play()

            garbages()
            _garbage_x = random.randrange(0, padWidth - garbageWidth)
            _garbage_y = 0
            isShot = False

            # 난이도 업
            garbageSpeed += 0.05
            if garbageSpeed >= 20:
                garbageSpeed = 20

        setObject(garbage, _garbage_x, _garbage_y)
                
        # 게임화면 재선언
        pygame.display.update()
        
         # 게임화면 초당프레임 설정
        clock.tick(60)
    pygame.quit()

initGame()
runGame()