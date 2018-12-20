
import pygame
from game_manager import Manager
import game_function as fun

"""
主程序
"""

manager = Manager()
# 初始化游戏
manager.init_game()

while manager.running:

    # 设置屏幕刷新频率
    manager.clock.tick(manager.FPS)

    # 处理不同事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 检查是否关闭窗口
            manager.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not manager.game_over:
            # 每次落子后检查玩家或电脑是否获胜
            response = fun.move(manager, event.pos)
            if response is not None and response[0] is False:
                # 游戏结束
                manager.game_over = True
                manager.winner = response[1]
        elif event.type == pygame.KEYUP and manager.game_over:
            manager.game_over = False
            # 重置游戏
            manager.init_params()

    if manager.game_over:
        # 游戏结束时显示开始界面及游戏结果
        fun.show_start_screen(manager)
        continue

    #绘制棋盘
    fun.draw_chessboard(manager)
    #绘制刷新棋子
    fun.draw_movements(manager)
    pygame.display.flip()

# 关闭游戏
pygame.quit()

