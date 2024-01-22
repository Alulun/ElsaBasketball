import pyxel
import random

WINDOW_H = 170
WINDOW_W = 150

elsaa_W = 15
elsaa_H = 26

basketball_W = 20
basketball_H = 20

SCENE_TITLE    = 0
SCENE_PLAY     = 1
SCENE_GAMEOVER = 2
SCENE_RESULT   = 3

class arurunrun:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class elsaa:
    def __init__(self, img_id):
        self.pos = arurunrun(0, 0)
        self.vec = 0
        self.img_elsaa = img_id

    def update(self, x, y, dx):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx

class Ball:
    def __init__(self):
        self.pos = arurunrun(0, 0)
        self.vec = 0
        self.size = 1
        self.speed = 3
        self.color = 0# 0~15

    def update(self, x, y, dx, size, color):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx
        self.size = size
        self.color = color

class basketball:
    def __init__(self, img_id):
        self.pos = arurunrun(0, 0)
        self.vec = 0
        self.speed = 0.02
        self.img_basketball = img_id

    def update(self, x, y, dx):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx

class App:
    def __init__(self):
        self.state = SCENE_TITLE

        self.IMG_ID0_X = 60
        self.IMG_ID0_Y = 65
        self.IMG_ID0 = 0
        self.IMG_ID1 = 1
        self.IMG_ID2 = 2

        pyxel.init(WINDOW_W, WINDOW_H)
        pyxel.load("./arurun.pyxres")

        pyxel.image(self.IMG_ID0).load(0, 0, "aruruntext.png")
        pyxel.image(self.IMG_ID1).load(0, 0, "elsa.png")
        pyxel.image(self.IMG_ID2).load(0, 0, "arurun.png")


        # make instance
        self.melsaa = elsaa(self.IMG_ID1)
        self.Balls = []
        self.Enemies = []

        # flag
        # self.flag = 1
        self.GameOver_flag = 0

        # Score
        self.Score = 0

        pyxel.run(self.update, self.draw)

    def change2this(self):
        pyxel.load("./arurun.pyxres")
        pyxel.image(self.IMG_ID0).load(0, 0, "aruruntext.png")
        pyxel.image(self.IMG_ID1).load(0, 0, "elsa.png")
        pyxel.image(self.IMG_ID2).load(0, 0, "arurun.png")

    def gameInit(self):
        self.state = SCENE_TITLE
        # make instance
        self.melsaa = elsaa(self.IMG_ID1)
        self.Balls = []
        self.Enemies = []

        # flag
        # self.flag = 1
        self.GameOver_flag = 0

        # Score
        self.Score = 0

    def update(self):
        if self.state == SCENE_TITLE:
            pass
        elif self.state == SCENE_PLAY:
            self.updatePlay()

    def draw(self):
        if self.state == SCENE_TITLE:
            self.drawTitle()
        elif self.state == SCENE_PLAY:
            self.drawPlay()
        elif self.state == SCENE_GAMEOVER:
            self.drawGameover()

# タイトルシーン ===============================================================
    def drawTitle(self):
        pyxel.cls(10)

        pyxel.text(45, 110, "- PRESS SPACE -", pyxel.frame_count % 16)
        pyxel.blt(48,60, self.IMG_ID0, 0, 0, 51, 15,5)
        pyxel.blt(67,80, self.IMG_ID1, 0, 0, 15, 26,5)

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.state = SCENE_PLAY
# ===========================================================================
    def updatePlay(self):

        # ====== ctrl elsaa ======
        dx = pyxel.mouse_x - self.melsaa.pos.x  # x軸方向の移動量(マウス座標 - elsaa座標)
        dy = pyxel.mouse_y - self.melsaa.pos.y  # y軸方向の移動量(マウス座標 - elsaa座標)
        if dx != 0:
            self.melsaa.update(pyxel.mouse_x, pyxel.mouse_y, dx) # 座標と向きを更新
        elif dy != 0:
            self.melsaa.update(pyxel.mouse_x, pyxel.mouse_y, self.melsaa.vec) # 座標のみ更新（真上or真下に移動）

        # ====== ctrl basketball ======
        if pyxel.frame_count % 120 == 1:
            # 画面の右端から
            new_basketball = basketball(self.IMG_ID2)
            new_basketball.update(random.randint(WINDOW_W, WINDOW_W+5), random.randint(0, WINDOW_H+5), -self.melsaa.vec)
            self.Enemies.append(new_basketball)
            # 画面の左端から
            new_basketball = basketball(self.IMG_ID2)
            new_basketball.update(random.randint(-5, 0), random.randint(0, WINDOW_H+5), -self.melsaa.vec)
            self.Enemies.append(new_basketball)

        basketball_count = len(self.Enemies)
        for i in range(basketball_count):
            # P制御
            ex = (self.melsaa.pos.x - self.Enemies[i].pos.x)
            ey = (self.melsaa.pos.y - self.Enemies[i].pos.y)
            Kp = self.Enemies[i].speed
            if ex != 0 or ey != 0:
                self.Enemies[i].update(self.Enemies[i].pos.x + ex * Kp,
                                        self.Enemies[i].pos.y + ey * Kp,
                                        self.melsaa.vec)
            # 当たり判定(敵キャラとelsa)
            if ((self.melsaa.pos.x < self.Enemies[i].pos.x + basketball_W)
                 and (self.Enemies[i].pos.x + basketball_W < self.melsaa.pos.x + elsaa_W)
                 and (self.melsaa.pos.y < self.Enemies[i].pos.y + basketball_H)
                 and (self.Enemies[i].pos.y + basketball_H < self.melsaa.pos.y + elsaa_H)
                or (self.melsaa.pos.x < self.Enemies[i].pos.x)
                 and (self.Enemies[i].pos.x < self.melsaa.pos.x + elsaa_W)
                 and (self.melsaa.pos.y < self.Enemies[i].pos.y + basketball_H)
                 and (self.Enemies[i].pos.y + basketball_H < self.melsaa.pos.y + elsaa_H)
                or (self.melsaa.pos.x < self.Enemies[i].pos.x + basketball_W)
                 and (self.Enemies[i].pos.x + basketball_W < self.melsaa.pos.x + elsaa_W)
                 and (self.melsaa.pos.y < self.Enemies[i].pos.y)
                 and (self.Enemies[i].pos.y < self.melsaa.pos.y + elsaa_H)
                or (self.melsaa.pos.x < self.Enemies[i].pos.x)
                 and (self.Enemies[i].pos.x < self.melsaa.pos.x + elsaa_W)
                 and (self.melsaa.pos.y < self.Enemies[i].pos.y)
                 and (self.Enemies[i].pos.y < self.melsaa.pos.y + elsaa_H)):
                # Game Overフラグを立てる
                self.GameOver_flag = 1

        # ====== ctrl Ball ======
        if pyxel.btnp(pyxel.KEY_SPACE):
            new_ball = Ball()
            if self.melsaa.vec > 0:
                new_ball.update(self.melsaa.pos.x + elsaa_W/2 + 6,
                                self.melsaa.pos.y + elsaa_H/2,
                                self.melsaa.vec, new_ball.size, new_ball.color)
            else:
                new_ball.update(self.melsaa.pos.x + elsaa_W/2 - 6,
                                self.melsaa.pos.y + elsaa_H/2,
                                self.melsaa.vec, new_ball.size, new_ball.color)
            self.Balls.append(new_ball)

        ball_count = len(self.Balls)
        for i in range(ball_count):
            if 0 < self.Balls[i].pos.x and self.Balls[i].pos.x < WINDOW_W:
                # Ball update
                if self.Balls[i].vec > 0:
                    self.Balls[i].update(self.Balls[i].pos.x + self.Balls[i].speed,
                                        self.Balls[i].pos.y,
                                        self.Balls[i].vec, self.Balls[i].size, self.Balls[i].color)
                else:
                    self.Balls[i].update(self.Balls[i].pos.x - self.Balls[i].speed,
                                        self.Balls[i].pos.y,
                                        self.Balls[i].vec, self.Balls[i].size, self.Balls[i].color)
                # 当たり判定(敵キャラとボール)
                basketball_count = len(self.Enemies)
                for j in range(basketball_count):
                    if ((self.Enemies[j].pos.x < self.Balls[i].pos.x)
                        and (self.Balls[i].pos.x < self.Enemies[j].pos.x + basketball_W)
                        and (self.Enemies[j].pos.y < self.Balls[i].pos.y)
                        and (self.Balls[i].pos.y < self.Enemies[j].pos.y + basketball_H)):
                        # 消滅(敵インスタンス破棄)
                        del self.Enemies[j]
                        if not self.GameOver_flag:
                            self.Score += 100
                        break
            else:
                del self.Balls[i]
                ball_count -= 1
                break

    def drawPlay(self):
        pyxel.cls(10)
        pyxel.text(10, 25, "arurun Game", pyxel.frame_count % 16)
        pyxel.blt(5,5, self.IMG_ID0, 0, 0, 51, 15,5)

        # ====== draw score ======
        score_x = 2
        score_y = WINDOW_H-8
        score = "SCORE:" + str(self.Score)
        pyxel.text(score_x, score_y, score, pyxel.frame_count % 16)

        # ======= draw elsaa ========
        if self.melsaa.vec > 0:
            pyxel.blt(self.melsaa.pos.x, self.melsaa.pos.y, self.IMG_ID1, 0, 0, -elsaa_W, elsaa_H, 5)
        else:
            pyxel.blt(self.melsaa.pos.x, self.melsaa.pos.y, self.IMG_ID1, 0, 0, elsaa_W, elsaa_H, 5)

        # ====== draw Balls ======
        for ball in self.Balls:
            pyxel.circ(ball.pos.x, ball.pos.y, ball.size, ball.color)

        # ====== draw basketball ======
        for basketball in self.Enemies:
            if basketball.vec > 0:
                pyxel.blt(basketball.pos.x, basketball.pos.y, basketball.img_basketball, 0, 0, -basketball_W, basketball_H, 5)
            else:
                pyxel.blt(basketball.pos.x, basketball.pos.y, basketball.img_basketball, 0, 0, basketball_W, basketball_H, 5)

        # ====== draw game over ======
        if self.GameOver_flag == 1:
            pyxel.text(self.melsaa.pos.x - 10, self.melsaa.pos.y - 5, "GAME OVER", 8)
            self.state = SCENE_GAMEOVER
#ゲームオーバーサーバー ===============================================================
    def drawGameover(self):
        pyxel.cls(10)

        pyxel.text(48, 45, "- Game Over -", 0)
        pyxel.text(50, 91, "SCORE:"+str(self.Score), 0)
        pyxel.blt(48,60, self.IMG_ID0, 0, 0, 51, 15,5)
        pyxel.blt(95,80, self.IMG_ID1, 0, 0, 15, 26,5)
        pyxel.text(45, 110, "- PRESS SPACE -", 0)

        if pyxel.btnp(pyxel.KEY_SPACE):
             self.gameInit()
             self.state = SCENE_TITLE





#==================================================================================
App()