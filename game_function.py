
import pygame
import random

"""
游戏功能实现模块
"""

def draw_chessboard(manager):
    """
    绘制棋盘
    """
    # 绘制背景
    manager.screen.fill(manager.bg_color)

    #棋盘宽高以及每个小格子宽度
    WIDTH = manager.WIDTH
    HEIGHT = manager.HEIGHT
    GRID_WIDTH = manager.GRID_WIDTH

    # 画网格线，棋盘为19行19列
    #画出棋盘边框
    rect_lines = [
        ((GRID_WIDTH, GRID_WIDTH), (GRID_WIDTH, HEIGHT - GRID_WIDTH)),
        ((GRID_WIDTH, GRID_WIDTH), (WIDTH - GRID_WIDTH, GRID_WIDTH)),
        ((GRID_WIDTH, HEIGHT - GRID_WIDTH),
            (WIDTH - GRID_WIDTH, HEIGHT - GRID_WIDTH)),
        ((WIDTH - GRID_WIDTH, GRID_WIDTH),
            (WIDTH - GRID_WIDTH, HEIGHT - GRID_WIDTH)),
    ]
    for line in rect_lines:
        pygame.draw.line(manager.screen, manager.BLACK, line[0], line[1], 2)

    #画出棋盘横向纵向各17条网格线
    for i in range(17):
        pygame.draw.line(manager.screen, manager.BLACK,
                         (GRID_WIDTH * (2 + i), GRID_WIDTH),
                         (GRID_WIDTH * (2 + i), HEIGHT - GRID_WIDTH))
        pygame.draw.line(manager.screen, manager.BLACK,
                         (GRID_WIDTH, GRID_WIDTH * (2 + i)),
                         (HEIGHT - GRID_WIDTH, GRID_WIDTH * (2 + i)))

    #画出棋盘上的五个黑色小圆点
    circle_center = [
        (GRID_WIDTH * 4, GRID_WIDTH * 4),
        (WIDTH - GRID_WIDTH * 4, GRID_WIDTH * 4),
        (WIDTH - GRID_WIDTH * 4, HEIGHT - GRID_WIDTH * 4),
        (GRID_WIDTH * 4, HEIGHT - GRID_WIDTH * 4),
        (GRID_WIDTH * 10, GRID_WIDTH * 10)
    ]
    for cc in circle_center:
        pygame.draw.circle(manager.screen, manager.BLACK, cc, 5)

def show_start_screen(manager):
    """
    绘制游戏开始页
    """
    note_height = 10
    if manager.winner is not None:
        draw_text(manager.screen, 'You {0} !'.format('win!' if manager.winner == manager.USER else 'lose!'),
                  64, manager.WIDTH // 2, note_height, manager.RED)
    else:
        # manager.screen.blit(manager.background, manager.back_rect)
        manager.screen.fill(manager.bg_color)

    draw_text(manager.screen, 'Five In Row', 64, manager.WIDTH // 2, note_height + manager.HEIGHT // 4, manager.BLACK)
    draw_text(manager.screen, 'press any key to start game', 22, manager.WIDTH // 2, note_height + manager.HEIGHT // 2,
              manager.BLUE)
    pygame.display.flip()

def draw_text(screen, text, size, x, y, color):
    """
    在屏幕上绘制文字
    """
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def update_value(manager, pos, color, ident):
    """
    更新权重
    """
    hori = 1
    verti = 1
    slash = 1
    backslash = 1
    left = pos[0] - 1

    #从当前走的棋子处统计左右相连的相同颜色棋子的个数，判断这步棋的权重
    while left > 0 and manager.color_metrix[left][pos[1]] == color:
        left -= 1
        if hori == 4:
            hori += 1
            break
        if left > 0 and\
                (manager.color_metrix[left][pos[1]] == color or
                 manager.color_metrix[left][pos[1]] is None):
            hori += 1

    right = pos[0] + 1
    while right < 20 and manager.color_metrix[right][pos[1]] == color:
        right += 1
        if hori == 4:
            hori += 1
            break
        if right < 20 and\
                (manager.color_metrix[right][pos[1]] == color or
                 manager.color_metrix[right][pos[1]] is None):
            hori += 1

    hori = manager.value_level[hori]

    up = pos[1] - 1
    # 从当前走的棋子处统计纵向相连的相同颜色棋子的个数，判断这步棋的权重
    while up > 0 and manager.color_metrix[pos[0]][up] == color:
        up -= 1
        if verti == 4:
            verti += 1
            break
        if up > 0 and\
                (manager.color_metrix[pos[0]][up] == color or
                 manager.color_metrix[pos[0]][up] is None):
            verti += 1

    down = pos[1] + 1
    while down < 20 and manager.color_metrix[pos[0]][down] == color:
        down += 1
        if verti == 4:
            verti += 1
            break
        if down < 20 and\
                (manager.color_metrix[pos[0]][down] == color or
                 manager.color_metrix[pos[0]][down] is None):
            verti += 1

    verti = manager.value_level[verti]

    # 从当前走的棋子处统计左上方和右下方相连的相同颜色棋子的个数，判断这步棋的权重
    left = pos[0] - 1
    up = pos[1] - 1
    while left > 0 and up > 0 and manager.color_metrix[left][up] == color:
        left -= 1
        up -= 1
        if backslash == 4:
            backslash += 1
            break
        if left > 0 and up > 0 and\
                (manager.color_metrix[left][up] == color or
                 manager.color_metrix[left][up] is None):
            backslash += 1

    right = pos[0] + 1
    down = pos[1] + 1
    while right < 20 and down < 20 and manager.color_metrix[right][down] == color:
        right += 1
        down += 1
        if backslash == 4:
            backslash += 1
            break
        if right < 20 and down < 20 and\
                (manager.color_metrix[right][down] == color or
                 manager.color_metrix[right][down] is None):
            backslash += 1
    backslash = manager.value_level[backslash]

    # 从当前走的棋子处统计右上方和左下方相连的相同颜色棋子的个数，判断这步棋的权重
    right = pos[0] + 1
    up = pos[1] - 1
    while right < 20 and up > 0 and manager.color_metrix[right][up] == color:
        right += 1
        up -= 1
        if slash == 4:
            slash += 1
            break
        if right < 20 and up > 0 and (manager.color_metrix[right][up] == color or
                                      manager.color_metrix[right][up] is None):
            slash += 1

    left = pos[0] - 1
    down = pos[1] + 1
    while left > 0 and down < 20 and manager.color_metrix[left][down] == color:
        left -= 1
        down += 1
        if slash == 4:
            slash += 1
            break
        if left > 0 and down < 20 and (manager.color_metrix[left][down] == color or
                                       manager.color_metrix[left][down] is None):
            slash += 1

    slash = manager.value_level[slash]

    # 判断这步棋是谁走的
    if ident == manager.USER:
        # 更新玩家走的棋的权重
        manager.player_value_metrix[pos[0]][pos[1]] =\
            int((hori + verti + slash + backslash) * 0.9)
    else:
        #更新电脑走的棋的权重
        manager.ai_value_metrix[pos[0]][pos[1]] = hori + verti + slash + backslash


def game_is_over(manager, pos, color):
    """
    判断游戏是否结束，是否产生胜者
    """

    hori = 1
    verti = 1
    slash = 1
    backslash = 1
    left = pos[0] - 1

    # 统计当前棋子位置各个方向相同颜色的棋子数目
    # 统计当前棋子左边相同颜色棋子个数
    while left > 0 and manager.color_metrix[left][pos[1]] == color:
        left -= 1
        hori += 1

    # 统计当前棋子右边相同颜色棋子个数
    right = pos[0] + 1
    while right < 20 and manager.color_metrix[right][pos[1]] == color:
        right += 1
        hori += 1

    # 统计当前棋子上方相同颜色棋子个数
    up = pos[1] - 1
    while up > 0 and manager.color_metrix[pos[0]][up] == color:
        up -= 1
        verti += 1

    # 统计当前棋子下方相同颜色棋子个数
    down = pos[1] + 1
    while down < 20 and manager.color_metrix[pos[0]][down] == color:
        down += 1
        verti += 1

    # 统计当前棋子左上方相同颜色棋子个数
    left = pos[0] - 1
    up = pos[1] - 1
    while left > 0 and up > 0 and manager.color_metrix[left][up] == color:
        left -= 1
        up -= 1
        backslash += 1

    # 统计当前棋子右下方相同颜色棋子个数
    right = pos[0] + 1
    down = pos[1] + 1
    while right < 20 and down < 20 and manager.color_metrix[right][down] == color:
        right += 1
        down += 1
        backslash += 1

    # 统计当前棋子右上方相同颜色棋子个数
    right = pos[0] + 1
    up = pos[1] - 1
    while right < 20 and up > 0 and manager.color_metrix[right][up] == color:
        right += 1
        up -= 1
        slash += 1

    # 统计当前棋子左下方相同颜色棋子个数
    left = pos[0] - 1
    down = pos[1] + 1
    while left > 0 and down < 20 and manager.color_metrix[left][down] == color:
        left -= 1
        down += 1
        slash += 1

    # 判断各个方向是否有相同的五子连线
    if max([hori, verti, backslash, slash]) >= 5:
        return True


def add_coin(manager, color, pos, ident, radius=16):
    # 添加走的棋子

    num_pos = gridpos_2_num(pos)
    # 将该位置加入落子集合中
    manager.movements.append(((pos[0] * manager.GRID_WIDTH, pos[1] * manager.GRID_WIDTH), color))
    #将该位置从remain和player_optimal_set中移除
    manager.remain.remove(num_pos)
    if num_pos in manager.player_optimal_set:
        manager.player_optimal_set.remove(num_pos)

    #由于该位置已有棋子，先将该位置的权重记为负值，并记下该棋子颜色
    manager.player_value_metrix[pos[0]][pos[1]] = -1 - ident
    manager.ai_value_metrix[pos[0]][pos[1]] = -1 - ident
    manager.color_metrix[pos[0]][pos[1]] = color
    #绘制走的棋
    pygame.draw.circle(manager.screen, color,
                       manager.movements[-1][0], radius)
    manager.hit_sound.play()
    manager.clock.tick(manager.FPS)

    #更新棋子所落的位置周围落子的权重
    around = around_grid(pos, 4)
    for rx in range(around[0], around[1] + 1):
        for ry in range(around[2], around[3] + 1):
            num_pos = gridpos_2_num((rx, ry))
            if num_pos in manager.remain:
                # 更新黑子或白子在某处棋子权重
                update_value(manager, (rx, ry), color, ident)
                if color == manager.BLACK:
                    tpcolor = manager.WHITE
                else:
                    tpcolor = manager.BLACK
                # 更新白子或黑子在某处棋子权重
                update_value(manager, (rx, ry), tpcolor, 1 - ident)


def num_2_gridpos(num):
    # 将数字转换为棋盘上对应的位置
    return (1 + (num % 19), (num // 19) + 1)


def gridpos_2_num(grid):
    # 将棋盘上的位置转换为数字
    return (grid[1] - 1) * 19 + grid[0] - 1


def around_grid(curr_move_pos, step=2):
    """
    获取棋子上下左右位置的网格
    """
    left = curr_move_pos[0] - step if (curr_move_pos[0] - step) > 0 else 1
    right = curr_move_pos[0] + step if (curr_move_pos[0] + step) < 20 else 19
    top = curr_move_pos[1] - step if (curr_move_pos[1] - step) > 0 else 1
    bottom = curr_move_pos[1] + step if (curr_move_pos[1] + step) < 20 else 19
    return (left, right, top, bottom)


def get_next_move(manager, curr_move):
    """
    实现电脑走下一步棋的逻辑
    """

    # 获取用户当前所走的棋周围的位置
    around = around_grid((curr_move[0][0] // manager.GRID_WIDTH,
                          curr_move[0][1] // manager.GRID_WIDTH))
    # 将玩家下的棋周围的位置添加到玩家下一步可能走的棋的集合中
    for rx in range(around[0], around[1] + 1):
        for ry in range(around[2], around[3] + 1):
            num_pos = gridpos_2_num((rx, ry))
            if num_pos in manager.remain:
                manager.player_optimal_set.add(gridpos_2_num((rx, ry)))

    max_value = -1000000
    next_move = 0
    for i in manager.player_optimal_set:
        grid = num_2_gridpos(i)
        #根据权重判断电脑下一步是否可以五子成线
        if manager.ai_value_metrix[grid[0]][grid[1]] >= manager.value_level[5]:
            next_move = i
            break
        # 根据权重判断玩家下一步是否可以四子成线，阻止玩家四子连成线
        if manager.player_value_metrix[grid[0]][grid[1]] >= manager.value_level[4]:
            next_move = i
            break
        #如果不符合上诉情况，则根据权重大小，电脑选择最佳落子位置
        value = manager.ai_value_metrix[grid[0]][grid[1]] + \
                manager.player_value_metrix[grid[0]][grid[1]]

        if max_value < value:
            max_value = value
            next_move = i
        elif max_value == value:
            if (random.randint(0, 100) % 2) == 0:
                next_move = i

    # 将电脑下的棋周围的位置添加到玩家下一步可能走的棋的集合中
    around = around_grid(num_2_gridpos(next_move))
    for rx in range(around[0], around[1] + 1):
        for ry in range(around[2], around[1] + 1):
            num_pos = gridpos_2_num((rx, ry))
            if num_pos in manager.remain:
                manager.player_optimal_set.add(gridpos_2_num((rx, ry)))
    return next_move


def respond(manager, curr_move):
    """
    玩家下一步棋后电脑走下一步棋
    """

    # 获取电脑下一步下的棋
    next_move = get_next_move(manager, curr_move)
    grid_pos = num_2_gridpos(next_move)

    add_coin(manager, manager.WHITE, grid_pos, manager.AI)

    if game_is_over(manager, grid_pos, manager.WHITE):
        return (False, manager.AI)


def move(manager, pos):
    """
    玩家走下一步棋
    """
    grid = (int(round(pos[0] / (manager.GRID_WIDTH + .0))),
            int(round(pos[1] / (manager.GRID_WIDTH + .0))))

    # 判断落子位置是否在网格上
    if grid[0] <= 0 or grid[0] > 19:
        return
    if grid[1] <= 0 or grid[1] > 19:
        return

    pos = (grid[0] * manager.GRID_WIDTH, grid[1] * manager.GRID_WIDTH)

    if manager.color_metrix[grid[0]][grid[1]] is not None:
        return None

    # 绘制玩家所下的棋
    curr_move = (pos, manager.BLACK)
    add_coin(manager, manager.BLACK, grid, manager.USER)

    # 判断玩家落子后是否获胜
    if game_is_over(manager, grid, manager.BLACK):
        return (False, manager.USER)

    # 返回电脑落子结果
    return respond(manager, curr_move)


def draw_movements(manager):
    """
    刷新所有的棋子
    """
    for move in manager.movements[:-1]:
        pygame.draw.circle(manager.screen, move[1], move[0], 16)
    if manager.movements:
        pygame.draw.circle(manager.screen, manager.GREEN, manager.movements[-1][0], 16)




