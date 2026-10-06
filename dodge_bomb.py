import os
import sys
import time  # 5秒停止処理のために追加
import random
import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),  # 練習1
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect: pg.Rect) -> tuple[bool, bool]:  # 練習3
    """
    引数:こうかとんRectかばくだんRect
    戻り値:タプル(横方向判定結果，縦方向判定結果)
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:
        tate = False
    return yoko, tate


# 追加機能1
def gameover(screen: pg.Surface) -> None:
    Surface_out = pg.Surface((WIDTH, HEIGHT))
    Surface_out.fill((0, 0, 0))  # 黒塗り
    Surface_out.set_alpha(200)   # ちょっと透明

    font = pg.font.Font(None, 80)
    txt = font.render("Game Over", True, (255, 255, 255))
    kk_cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)

    Surface_out.blit(txt, [400, 280])
    Surface_out.blit(kk_cry_img, [300, 270])  # 文字の左側
    Surface_out.blit(kk_cry_img, [730, 270])  # 文字の右側

    screen.blit(Surface_out, [0, 0])
    pg.display.update()
    time.sleep(5)  # 5秒間停止


# 追加機能2
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)

    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs


# 追加機能3
def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    base_img = pg.image.load("fig/3.png")
    flipped_img = pg.transform.flip(base_img, True, False)  # 左右反転

    kk_dict = {
        (0, 0): pg.transform.rotozoom(base_img, 0, 0.9),
        (-5, 0): pg.transform.rotozoom(base_img, 0, 0.9),       # 左
        (-5, -5): pg.transform.rotozoom(base_img, -45, 0.9),    # 左上
        (0, -5): pg.transform.rotozoom(flipped_img, 90, 0.9),    # 上
        (+5, -5): pg.transform.rotozoom(flipped_img, 45, 0.9),   # 右上
        (+5, 0): pg.transform.rotozoom(flipped_img, 0, 0.9),     # 右
        (+5, +5): pg.transform.rotozoom(flipped_img, -45, 0.9),  # 右下
        (0, +5): pg.transform.rotozoom(flipped_img, -90, 0.9),   # 下
        (-5, +5): pg.transform.rotozoom(base_img, 45, 0.9),     # 左下
    }
    return kk_dict


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

    # 追加機能3: 辞書と初期画像
    kk_imgs = get_kk_imgs()
    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 追加機能2: 画像リストと加速度リスト
    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])

        # 練習5
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()

        sum_mv = [0, 0]
        for k, tpl in DELTA.items():  # 練習1
            if key_lst[k]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # 練習3
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        # 追加機能3：向きに応じた画像変更
        kk_img = kk_imgs[tuple(sum_mv)]
        screen.blit(kk_img, kk_rct)

        # 追加機能2：拡大・加速の計算と更新
        idx = min(tmr // 500, 9)
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        bb_img = bb_imgs[idx]
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height

        # 爆弾移動
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)  # 練習3
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()