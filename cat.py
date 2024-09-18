#可以游玩

import pygame
import random

# 初始化 Pygame
pygame.init()

# 缩放系数
SCALE_FACTOR = 1.6  # 1.5 倍放大

# 游戏属性常量定义
TITLE = '猫了个猫'
WIDTH, HEIGHT = (1500, 800)
TILE_WIDTH, TILE_HEIGHT = int(60 * SCALE_FACTOR), int(60 * SCALE_FACTOR)

# 设置屏幕
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

# 定义颜色
WHITE = (255, 255, 255)


# 加载资源并调整尺寸
background = pygame.transform.scale(pygame.image.load('image2/back.jpeg'), (WIDTH, HEIGHT))
mask = pygame.transform.scale(pygame.image.load('image2/mask.png'), (TILE_WIDTH, TILE_HEIGHT))
end_img = pygame.transform.scale(pygame.image.load('image2/lose.jpg'), (WIDTH, HEIGHT))
win_img = pygame.transform.scale(pygame.image.load('image2/win.jpg'), (WIDTH, HEIGHT))
exit_button = pygame.transform.scale(pygame.image.load('image2/tile2.png'), (50, 50))  # 退出按钮
f = pygame.transform.scale(pygame.image.load('image2/frame6.png'), (TILE_WIDTH+35, TILE_HEIGHT+35))
frame=pygame.transform.scale(pygame.image.load('image2/frame5.jpeg'), (TILE_WIDTH+30, TILE_HEIGHT+30))
cat_select=pygame.transform.scale(pygame.image.load('image2/cat_select2.jpeg'), (WIDTH, HEIGHT))
time_man=pygame.transform.scale(pygame.image.load('image2/tile.png'), (190, 100))
record_cat=pygame.transform.scale(pygame.image.load('image2/back22.jpg'), (WIDTH, HEIGHT))

#首页加载
back_start = pygame.transform.scale(pygame.image.load('image2/cat_sleep.jpeg'), (WIDTH, HEIGHT))

# 牌堆区域（DOCK）
# DOCK = pygame.Rect(int(90 * SCALE_FACTOR), int(564 * SCALE_FACTOR), TILE_WIDTH * 7, TILE_HEIGHT)
DOCK = pygame.Rect(600,600,TILE_WIDTH * 7, TILE_HEIGHT)

#按钮位置
exit_button_rect = exit_button.get_rect(topleft=(WIDTH - 50- 10, 10))  # 右上角
# exit_button_rect = exit_button.get_rect(topleft=(WIDTH , 10))  # 右上角

docks = []


def level_select_s(level):
    if level ==3:
        return 3,1,list(range(1, 6)) * 3
    elif level ==1:
        return 6,5,list(range(1, 3)) * 48
    elif level ==2:
        return 7,4,list(range(1, 3)) * 72
    elif level ==4:
        return 7,4,list(range(1, 4)) * 48
    elif level ==5:
        return 6,4,list(range(1, 5)) * 24
    elif level ==6:
        return 7,4,list(range(1,5)) * 36
    elif level ==7:
        return 5,5,list(range(1, 6)) * 12
    elif level ==8:
        return 7,4,list(range(1,7)) * 24
    elif level ==9:
        return 6,5,list(range(1, 9)) * 12
    elif level ==10:
        return 5,5,list(range(1, 11)) * 6
    elif level ==11:
        return 4,3,list(range(1, 12)) * 3
    elif level ==12:
        return 7,4,list(range(1,13)) * 12



def make_titles(level):



    # 游戏中的所有牌及牌堆
    tiles = []

    # level=3

    l,leftover,tile_numbers=level_select_s(level)



    random.shuffle(tile_numbers)

    # 创建牌
    tile_index = 0
    for layer in range(l):  # 7层
        for row in range(l - layer):  # 每层行数递减
            for col in range(l - layer):
                tile_type = tile_numbers[tile_index]
                tile_index += 1
                tile = {
                    "image": pygame.transform.scale(pygame.image.load(f'cats/cat{tile_type}.jpg'), (TILE_WIDTH, TILE_HEIGHT)),
                    "pos": [int((20 + (layer * 0.5 + col) * 60) * SCALE_FACTOR), int((30 + (layer * 0.5 + row) * 66 * 0.9) * SCALE_FACTOR)],  # 放大位置
                    "tag": tile_type,
                    "layer": layer,
                    "status": 1 if layer == l-1 else 0  # 最上层可点击
                }
                tiles.append(tile)

    # 剩余的4张牌放置到牌堆底部
    for i in range(leftover):
        tile_type = tile_numbers[tile_index]
        tile_index += 1
        tile = {
            "image": pygame.transform.scale(pygame.image.load(f'cats/cat{tile_type}.jpg'), (TILE_WIDTH, TILE_HEIGHT)),
            "pos": [870+i*60*SCALE_FACTOR, 400],  # 放大位置
            "tag": tile_type,
            "layer": 0,
            "status": 1
        }
        tiles.append(tile)
    return tiles

# 加载背景音乐
pygame.mixer.music.load('music/bgm.mp3')
pygame.mixer.music.play(-1)  # 循环播放

# 游戏帧绘制函数
def draw(elapsed_time):
    screen.blit(background, (0, 0))  # 绘制背景
    # screen.blit(f, (750,DOCK.y))
    for tile in tiles:
        screen.blit(frame,(tile["pos"][0]-15,tile["pos"][1]-15))
        screen.blit(tile['image'], tile['pos'])  # 绘制牌
        if tile['status'] == 0:
            screen.blit(mask, tile['pos'])  # 不可点击的牌显示遮罩

    for i in range(7):
        dock_pos = (755+i * (TILE_WIDTH+10),590)
        screen.blit(pygame.transform.scale(f,(109,109)), dock_pos)

    for i, tile in enumerate(docks):

        # dock_pos = (DOCK.x + i * TILE_WIDTH+173, DOCK.y+6)
        dock_pos = (i * (TILE_WIDTH+10)+755+15,590+15)

        screen.blit(pygame.transform.scale(tile['image'],(80,80)), dock_pos)

    screen.blit(time_man, (990, 30))
    screen.blit(exit_button, exit_button_rect.topleft)


# 鼠标点击处理
def handle_mouse_click(pos):
    global docks

    if exit_button_rect.collidepoint(pos):
        pygame.quit()
        return

    if len(docks) >= 7 or len(tiles) == 0:  # 游戏结束时不处理点击
        # game_over = True
        return


    for tile in reversed(tiles):  # 从最上层的牌开始判断
        rect = pygame.Rect(tile['pos'][0], tile['pos'][1], TILE_WIDTH, TILE_HEIGHT)
        if tile['status'] == 1 and rect.collidepoint(pos):
            tile['status'] = 2
            tiles.remove(tile)

            unmatched_tiles = [t for t in docks if t['tag'] != tile['tag']]

            if len(docks) - len(unmatched_tiles) < 2:
                docks.append(tile)
            else:
                docks = unmatched_tiles

            for down_tile in tiles:
                if down_tile['layer'] == tile['layer'] - 1 and pygame.Rect(down_tile['pos'][0], down_tile['pos'][1],
                                                                           TILE_WIDTH, TILE_HEIGHT).colliderect(
                        pygame.Rect(tile['pos'][0], tile['pos'][1], TILE_WIDTH, TILE_HEIGHT)):
                    for up_tile in tiles:
                        if up_tile['layer'] == down_tile['layer'] + 1 and pygame.Rect(up_tile['pos'][0],
                                                                                      up_tile['pos'][1], TILE_WIDTH,
                                                                                      TILE_HEIGHT).colliderect(
                                pygame.Rect(down_tile['pos'][0], down_tile['pos'][1], TILE_WIDTH, TILE_HEIGHT)):
                            break
                    else:
                        down_tile['status'] = 1  # 如果没有其他牌覆盖，则变为可点击状态

            break



BUTTON_WIDTH = 280
BUTTON_HEIGHT = 75
BUTTON_COLOR = (218, 198, 165)  # 绿色按钮
BUTTON_TEXT_COLOR = (255, 255, 255)  # 白色文字

# 定义按钮的矩形区域
button_rect = pygame.Rect((WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2-50), (BUTTON_WIDTH, BUTTON_HEIGHT))
button_record = pygame.Rect((WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2+40), (BUTTON_WIDTH, BUTTON_HEIGHT))


def draw_start(screen, mouse_pos, is_clicked):

    screen.blit(back_start, (0, 0))

    # 检查鼠标是否在按钮范围内
    if button_rect.collidepoint(mouse_pos):
        if is_clicked:
            color1 = (100, 200, 100)  # 点击时颜色
        else:
            color1 = (206, 179, 131)  # 悬停时颜色
    else:
        color1 = BUTTON_COLOR  # 正常按钮颜色

    if button_record.collidepoint(mouse_pos):
        if is_clicked:
            color2 = (100, 200, 100)  # 点击时颜色
        else:
            color2 = (206, 179, 131)  # 悬停时颜色
    else:
        color2 = BUTTON_COLOR  # 正常按钮颜色



    # 绘制按钮的外边框
    border_color = (0, 0, 0)  # 边框颜色
    pygame.draw.rect(screen, border_color, button_rect, border_radius=15)  # 边框
    # 绘制按钮本身（带圆角）
    pygame.draw.rect(screen, color1, button_rect.inflate(-4, -4), border_radius=15)  # -4让边框可见
    # 创建并绘制按钮文字
    font = pygame.font.SysFont(None, 36)
    text = font.render("Start !", True, BUTTON_TEXT_COLOR)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)  # 显示文字


    # 绘制按钮的外边框
    border_color = (0, 0, 0)  # 边框颜色
    pygame.draw.rect(screen, border_color, button_record, border_radius=15)  # 边框
    # 绘制按钮本身（带圆角）
    pygame.draw.rect(screen, color2, button_record.inflate(-4, -4), border_radius=15)  # -4让边框可见
    # 创建并绘制按钮文字
    font = pygame.font.SysFont(None, 36)
    text = font.render("Record", True, BUTTON_TEXT_COLOR)
    text_rect = text.get_rect(center=button_record.center)
    screen.blit(text, text_rect)  # 显示文字





# 定义按钮的宽度、高度和颜色
BUTTON_WIDTH_b = 200
BUTTON_HEIGHT_b = 60
BUTTON_COLOR2 = (0, 255, 0)  # 按钮颜色
BUTTON_TEXT_COLOR2 = (255, 255, 255)  # 文字颜色

# 回到主页按钮的位置
home_button_rect = pygame.Rect(10, 10, BUTTON_WIDTH_b, BUTTON_HEIGHT_b)

# 退出游戏按钮的位置
exit_button_rect2 = pygame.Rect(250, 10, BUTTON_WIDTH_b, BUTTON_HEIGHT_b)


def draw_game_over_screen(screen, mouse_pos, is_clicked):


    # 游戏结束判定
    if len(docks) >= 7:
        screen.blit(end_img, (0, 0))  # 绘制游戏结束图
    elif len(tiles) == 0:
        screen.blit(win_img, (0, 0))  # 绘制胜利图


    # 检查鼠标是否在按钮范围内
    if home_button_rect.collidepoint(mouse_pos):
        if is_clicked:
            color = (100, 200, 100)  # 点击时颜色
        else:
            color = (206, 179, 131)  # 悬停时颜色
    else:
        color = BUTTON_COLOR  # 正常按钮颜色

    # 检查鼠标是否在按钮范围内
    if exit_button_rect2.collidepoint(mouse_pos):
        if is_clicked:
            color2 = (100, 200, 100)  # 点击时颜色
        else:
            color2 = (206, 179, 131)  # 悬停时颜色
    else:
        color2 = BUTTON_COLOR  # 正常按钮颜色



    # 绘制回到主页按钮
    pygame.draw.rect(screen, color, home_button_rect)
    font = pygame.font.SysFont(None, 36)
    home_text = font.render("Home", True, BUTTON_TEXT_COLOR2)
    home_text_rect = home_text.get_rect(center=home_button_rect.center)
    screen.blit(home_text, home_text_rect)

    # 绘制退出游戏按钮
    pygame.draw.rect(screen, color2, exit_button_rect2)
    exit_text = font.render("Exit", True, BUTTON_TEXT_COLOR2)
    exit_text_rect = exit_text.get_rect(center=exit_button_rect2.center)
    screen.blit(exit_text, exit_text_rect)




def handle_game_over_click(pos):
    global selected_level
    if home_button_rect.collidepoint(pos):
        # 玩家点击了回到主页按钮
        reset_game(selected_level)  # 重置游戏状态并返回主页
    elif exit_button_rect2.collidepoint(pos):
        # 玩家点击了退出游戏按钮
        pygame.quit()
        exit()

# 定义按钮的宽度、高度、颜色和关卡数
LEVEL_BUTTON_WIDTH_s = 200
LEVEL_BUTTON_HEIGHT_s = 60
BUTTON_COLOR3 = (0, 255, 0)
BUTTON_TEXT_COLOR3 = (255, 255, 255)

# 定义关卡数量
TOTAL_LEVELS_R = 3
TOTAL_LEVELS_C = 4

# 创建关卡按钮的矩形
level_buttons = []
for i in range(TOTAL_LEVELS_R):
    for j in range(TOTAL_LEVELS_C):

        # button_rect = pygame.Rect(WIDTH // 2 - LEVEL_BUTTON_WIDTH_s // 2, 200 + i * (LEVEL_BUTTON_HEIGHT_s + 20), LEVEL_BUTTON_WIDTH_s, LEVEL_BUTTON_HEIGHT_s)
        button_rect3 = pygame.Rect(200+j*(LEVEL_BUTTON_WIDTH_s+100), 250 + i * (LEVEL_BUTTON_HEIGHT_s + 20), LEVEL_BUTTON_WIDTH_s, LEVEL_BUTTON_HEIGHT_s)
        level_buttons.append(button_rect3)


def draw_level_select_screen(screen,mouse_pos, is_clicked):
    screen.blit(cat_select, (0, 0))


    font = pygame.font.SysFont(None, 36)

    # 绘制每个关卡按钮
    for i, button_rect in enumerate(level_buttons):

        # 检查鼠标是否在按钮范围内
        if button_rect.collidepoint(mouse_pos):
            if is_clicked:
                color = (100, 200, 100)  # 点击时颜色
            else:
                color = (206, 179, 131)  # 悬停时颜色
        else:
            color = BUTTON_COLOR  # 正常按钮颜色

        pygame.draw.rect(screen, color, button_rect)
        level_text = font.render(f"Level {i + 1}", True, BUTTON_TEXT_COLOR)
        text_rect = level_text.get_rect(center=button_rect.center)
        screen.blit(level_text, text_rect)

def draw_record(screen):
    screen.blit(record_cat, (0, 0))  # 绘制背景

    font = pygame.font.SysFont(None, 50)

    # 遍历 record 列表，逐行显示内容
    for i, entry in enumerate(record):
        text = font.render(f"record{i + 1}    level:{entry[0]}    time:{entry[1]}s", True, (255, 255, 255))  # 将 record 里的内容绘制成文字
        screen.blit(text, (125, 100 + i * 40))  # 将每个记录绘制到不同的位置，避免重叠


def handle_level_select_click(pos):
    global selected_level, level_select

    for i, button_rect in enumerate(level_buttons):
        if button_rect.collidepoint(pos):
            selected_level = i + 1  # 玩家选择的关卡
            reset_game(selected_level)  # 重置游戏状态
            # game_started = True  # 开始游戏
            level_select = False
            # print(selected_level)
            break

def handle_record(pos):
    global show_record

    if button_record.collidepoint(pos):
        show_record = True


def reset_game(level):
    global game_started, game_over, tiles, docks, start_time
    game_started = False
    game_over = False
    tiles = make_titles(level)  # 重新初始化游戏的牌组
    docks = []  # 重置牌堆
    start_time = None  # 重置计时器


def main():
    global level_select,tiles,selected_level,record,show_record
    pygame.init()
    clock = pygame.time.Clock()
    running = True
    game_started = False  # 游戏是否开始标志
    game_over = False  # 游戏结束标志
    start_time = None  # 计时起始时间
    # level_select = True
    level_select = False
    selected_level=0#选择关卡
    tiles = make_titles(selected_level+1)
    record=[]
    elapsed_time2=0
    time_record_control=False
    show_record=False
    # count=0
    while running:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        is_clicked = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    handle_game_over_click(event.pos)
                    game_over = False
                    game_started = False
                    level_select=True
                elif not game_started and button_rect.collidepoint(event.pos):
                    game_started = True
                    level_select=True
                elif not show_record and button_record.collidepoint(event.pos):
                    show_record = True
                elif game_started and level_select:
                    handle_level_select_click(event.pos)
                    start_time = pygame.time.get_ticks()  # 开始计时
                elif level_select:
                    handle_record(event.pos)
                elif game_started and not level_select:
                    handle_mouse_click(event.pos)

        if len(docks) >= 7 or len(tiles) == 0:
            level_select=False
            game_over = True  #


        if len(tiles) == 0 and time_record_control:

            record.append((selected_level, elapsed_time2))

            time_record_control = False


        if not game_started:
            draw_start(screen, mouse_pos, is_clicked)

        elif game_over:
            draw_game_over_screen(screen, mouse_pos, is_clicked)
        elif show_record:
            draw_record(screen)

        elif level_select:
            draw_level_select_screen(screen, mouse_pos, is_clicked)

        else:
            draw(tiles)  # 绘制游戏内容
            time_record_control = True
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # 计算经过时间
            elapsed_time2 = round((pygame.time.get_ticks() - start_time) / 1000,3)

            font = pygame.font.SysFont(None, 60)
            time_text = font.render(f"Time: {elapsed_time}s", True, (0, 0, 0))
            screen.blit(time_text, (1000, 50))  # 显示计时器


        # print(record)
        pygame.display.update()
        clock.tick(60)  # 控制帧率


    pygame.quit()


if __name__ == "__main__":
    main()
