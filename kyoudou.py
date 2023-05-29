import random
import sys
import time
from typing import Any
import pygame as pg

WIDTH = 800
HEIGHT = 600

def check_bound(obj: pg.Rect) -> tuple[bool]:
    """
    オブジェクトが画面内か画面外かを判定し，真理値タプルを返す
    引数 obj：オブジェクトこうかとんSurfaceのRect
    戻り値：縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    tate = True
    
    if obj.top < 0 or HEIGHT < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return tate


class Bird(pg.sprite.Sprite):
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1)
    }

    def __init__(self, xy: tuple[int, int]):
        super().__init__()
        self.image = pg.image.load("ex01/fig/3.png")
        self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.speed = 6

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                self.rect.move_ip(+self.speed*mv[0], +self.speed*mv[1])
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        if check_bound(self.rect) != True:
            for k, mv in __class__.delta.items():
                if key_lst[k]:
                    self.rect.move_ip(0, -self.speed*mv[1])
        screen.blit(self.image, self.rect)


class Enemy(pg.sprite.Sprite):
    """
    敵機に関するクラス
    """
    imgs = [pg.image.load(f"ex04/fig/alien{i}.png") for i in range(1, 4)]
    
    def __init__(self):
        super().__init__()
        self.image = random.choice(__class__.imgs)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH, random.randint(0, HEIGHT)
        self.vx = -6
        self.bound = random.randint(50, HEIGHT/2)  # 停止位置
        self.state = "down"  # 降下状態or停止状態
        self.interval = random.randint(50, 300)  

    def update(self):
        """
        敵機を速度ベクトルself.vxに基づき移動させる
        """
        self.rect.move_ip(self.vx, 0)


class Coin(pg.sprite.Sprite):
    """
    コインに関するクラス
    """
    colors = [(237, 204, 45), (233, 233, 233), (233, 233, 233), (233, 233, 233)]

    def __init__(self):
        """
        コインSurfaceを生成する
        引数1 emy：敵機
        引数2 bird：攻撃対象のこうかとん
        """
        super().__init__()
        rad = 30 
        self.color = random.choice(__class__.colors)
        self.image = pg.Surface((2*rad, 2*rad))
        pg.draw.circle(self.image, self.color, (rad, rad), rad)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.vx, self.vy = -6, 0 
        self.rect.center = WIDTH, random.randint(0, HEIGHT)

    def update(self):
        """
        コインを速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        self.rect.move_ip(self.vx, self.vy)
        

class Score:
    """
    コインの得た数をスコアとして表示する
    銀:10点
    金:20点
    """
    def __init__(self):
        self.font = pg.font.Font(None, 40)
        self.color = (255, 128, 0)
        self.score = 0
        self.image = self.font.render(f"Score: {self.score}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH - 100, 30

    def score_up(self, add):
        self.score += add

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"score: {self.score}", 0, self.color)
        screen.blit(self.image, self.rect)
    
def main():
    pg.display.set_caption("避けながら稼げ！")
    score = Score()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex01/fig/pg_bg.jpg")
    r_bg_img = pg.transform.flip(bg_img, True, False)
    kk_img = pg.image.load("ex01/fig/3.png")
    kk_img = pg.transform.flip(kk_img, True, False)
    emys = pg.sprite.Group()  # Enemyのグループ
    coins = pg.sprite.Group()  # Coinのグループ
       
    tmr = 0

    bird = Bird([100, 200])
    while True:
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        tmr += 1
        if tmr%200 == 0:
            for i in range(3):
                emys.add(Enemy())
            coins.add(Coin())
        
        for coin in pg.sprite.spritecollide(bird, coins, True):
            if coin.color == coin.colors[0]:
                score.score_up(20) 
            else:
                score.score_up(10)
        
        if len(pg.sprite.spritecollide(bird, emys, True)) != 0:
            pg.display.update()
            time.sleep(2)
            return
    
        if score.score >= 50:
            pg.display.update()
            time.sleep(1)
            return

        screen.blit(bg_img, [0, 0])
        x = tmr % 3200
        screen.blit(bg_img, [-x, 0])
        screen.blit(r_bg_img, [1600 - x, 0])
        screen.blit(bg_img, [3200 - x, 0])

        bird.update(key_lst, screen)
        emys.update()
        emys.draw(screen)
        coins.update()
        coins.draw(screen)
        score.update(screen)
        pg.display.update()
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()