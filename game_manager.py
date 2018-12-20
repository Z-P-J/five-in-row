
import pygame
import os

"""
管理游戏的类
"""

class Manager:
    def __init__(self):
        self.game_over = True
        self.running = True
        self.winner = None
        self.USER, self.AI = 1, 0
        # 游戏窗口宽高及网格大小
        self.WIDTH = 720
        self.HEIGHT = 720
        self.GRID_WIDTH = self.WIDTH // 20
        # 屏幕刷新频率
        self.FPS = 30
        #权重等级
        self.value_level = [0, 1, 10, 100, 1000, 10000, 100000, 1000000, 1000000]
        # 颜色
        self.bg_color = (230, 230, 230)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        # 游戏标题
        self.caption = "五子棋"
        # 初始化一些参数
        self.init_params()

    def init_params(self):
        self.movements = [] #统计所有走的每一步棋
        self.remain = set(range(1, 19 ** 2 + 1)) #统计棋盘上剩下的没有棋子的位置
        self.player_value_metrix = [[0] * 20 for i in range(20)] #用于记录用户下一步可能走的棋权重的矩阵
        self.ai_value_metrix = [[0] * 20 for i in range(20)] #用于记录用户下一步可能走的棋权重的矩阵
        self.color_metrix = [[None] * 20 for i in range(20)] #用于记录网格中棋子颜色的矩阵
        self.player_optimal_set = set() #记录用户在棋子附近可能走的所有棋位置的集合

    def init_game(self):
        # 初始化pygame
        pygame.init()
        pygame.mixer.init()
        # 初始化窗口
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        # 设置标题
        pygame.display.set_caption(self.caption)
        # 加载资源文件夹
        self.base_folder = os.path.dirname(__file__)
        self.snd_folder = os.path.join(self.base_folder, 'music')
        # 加载下棋音乐
        self.hit_sound = pygame.mixer.Sound(os.path.join(self.snd_folder, 'buw.wav'))
        # 加载播放背景音乐
        self.back_music = pygame.mixer.music.load(os.path.join(self.snd_folder, 'background.mp3'))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)
        self.clock = pygame.time.Clock()