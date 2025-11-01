import pygame
import sys
import os

# 初始化pygame
pygame.init()

# 常量定义
CELL_SIZE = 50
WALL_COLOR = (139, 69, 19)
FLOOR_COLOR = (245, 245, 220)
BOX_COLOR = (200, 0, 0)  # 红色
TARGET_COLOR = (255, 215, 0)
PLAYER_COLOR = (0, 191, 255)
BOX_ON_TARGET_COLOR = (150, 0, 0)  # 深红色

# 地图元素
WALL = '#'
FLOOR = ' '
BOX = '$'
TARGET = '.'
PLAYER = '@'
BOX_ON_TARGET = '*'
PLAYER_ON_TARGET = '+'

def load_levels(filename="levels.txt"):
    """从文件加载关卡地图"""
    levels = []
    
    if not os.path.exists(filename):
        # 如果文件不存在，返回默认关卡
        print(f"Warning: {filename} not found, using default levels")
        return [
            [
                "########",
                "#      #",
                "#  $$  #",
                "#  @   #",
                "#      #",
                "#  ..  #",
                "########"
            ]
        ]
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            current_level = []
            for line in f:
                line = line.strip()
                if line == "---":
                    # 分隔符，表示一个关卡结束
                    if current_level:
                        levels.append(current_level)
                        current_level = []
                elif line:
                    # 非空行，添加到当前关卡
                    current_level.append(line)
            
            # 添加最后一个关卡（如果存在）
            if current_level:
                levels.append(current_level)
        
        if not levels:
            raise ValueError("No levels found in file")
        
        return levels
    except Exception as e:
        print(f"Error loading levels: {e}")
        # 返回默认关卡
        return [
            [
                "########",
                "#      #",
                "#  $$  #",
                "#  @   #",
                "#      #",
                "#  ..  #",
                "########"
            ]
        ]

# 从文件加载关卡地图
LEVELS = load_levels("levels.txt")

class BoxPusherGame:
    def __init__(self):
        self.current_level = 0
        self.level = [list(row) for row in LEVELS[self.current_level]]
        self.player_pos = self.find_player()
        self.moves = 0
        self.player_direction = 'down'  # 玩家当前方向：'up', 'down', 'left', 'right'
        self.history = []  # 保存移动历史，用于撤销功能
        self.screen_width = len(LEVELS[0][0]) * CELL_SIZE
        self.screen_height = len(LEVELS[0]) * CELL_SIZE + 85  # 额外空间显示信息
        self.screen = None  # 延迟初始化
        pygame.display.set_caption("Sokoban Game")
        self.font = None  # 延迟初始化
        self.small_font = None
        self.clock = pygame.time.Clock()
        
        # 加载玩家图片
        try:
            player_image = pygame.image.load("Picture/Player.png")
            self.player_image = pygame.transform.scale(player_image, (CELL_SIZE - 10, CELL_SIZE - 10))
        except:
            self.player_image = None
        
        # 加载背景音乐
        try:
            pygame.mixer.music.load("BGM/game-background-music.mp3")
            self.music_enabled = True
        except:
            self.music_enabled = False
        
    def init_fonts(self):
        """初始化字体"""
        if self.font is None or self.small_font is None:
            try:
                self.font = pygame.font.Font(None, 36)
                self.small_font = pygame.font.Font(None, 24)
            except:
                self.font = pygame.font.SysFont('arial', 36)
                self.small_font = pygame.font.SysFont('arial', 24)
    
    def find_player(self):
        """找到玩家位置"""
        for y, row in enumerate(self.level):
            for x, cell in enumerate(row):
                if cell in [PLAYER, PLAYER_ON_TARGET]:
                    return (x, y)
        return None
    
    def get_cell(self, x, y):
        """获取指定位置的元素"""
        if 0 <= y < len(self.level) and 0 <= x < len(self.level[y]):
            return self.level[y][x]
        return None
    
    def set_cell(self, x, y, value):
        """设置指定位置的元素"""
        if 0 <= y < len(self.level) and 0 <= x < len(self.level[y]):
            self.level[y][x] = value
    
    def can_move(self, dx, dy):
        """检查是否可以移动"""
        px, py = self.player_pos
        nx, ny = px + dx, py + dy
        cell = self.get_cell(nx, ny)
        
        if cell is None or cell == WALL:
            return False
        
        if cell in [BOX, BOX_ON_TARGET]:
            # 尝试推动箱子
            nnx, nny = nx + dx, ny + dy
            next_cell = self.get_cell(nnx, nny)
            
            if next_cell is None or next_cell in [WALL, BOX, BOX_ON_TARGET]:
                return False
        
        return True
    
    def save_state(self):
        """保存当前游戏状态到历史记录"""
        # 深拷贝地图状态
        level_copy = [list(row) for row in self.level]
        state = {
            'level': level_copy,
            'player_pos': self.player_pos,
            'moves': self.moves,
            'player_direction': self.player_direction
        }
        self.history.append(state)
    
    def undo(self):
        """撤销上一步操作"""
        if len(self.history) == 0:
            return False  # 没有历史记录，无法撤销
        
        # 恢复上一个状态
        prev_state = self.history.pop()
        self.level = [list(row) for row in prev_state['level']]
        self.player_pos = prev_state['player_pos']
        self.moves = prev_state['moves']
        self.player_direction = prev_state['player_direction']
        return True
    
    def move_player(self, dx, dy):
        """移动玩家"""
        if not self.can_move(dx, dy):
            return False
        
        # 在移动前保存当前状态
        self.save_state()
        
        # 更新玩家方向
        if dx == 1:
            self.player_direction = 'right'
        elif dx == -1:
            self.player_direction = 'left'
        elif dy == 1:
            self.player_direction = 'down'
        elif dy == -1:
            self.player_direction = 'up'
        
        px, py = self.player_pos
        nx, ny = px + dx, py + dy
        cell = self.get_cell(nx, ny)
        
        # 处理玩家当前位置
        current_cell = self.get_cell(px, py)
        if current_cell == PLAYER_ON_TARGET:
            self.set_cell(px, py, TARGET)
        else:
            self.set_cell(px, py, FLOOR)
        
        # 处理新位置
        if cell in [BOX, BOX_ON_TARGET]:
            # 推动箱子
            nnx, nny = nx + dx, ny + dy
            next_cell = self.get_cell(nnx, nny)
            
            if next_cell == TARGET:
                self.set_cell(nnx, nny, BOX_ON_TARGET)
            else:
                self.set_cell(nnx, nny, BOX)
            
            # 更新箱子原位置
            if cell == BOX_ON_TARGET:
                self.set_cell(nx, ny, PLAYER_ON_TARGET)
            else:
                self.set_cell(nx, ny, PLAYER)
        else:
            # 直接移动到新位置
            if cell == TARGET:
                self.set_cell(nx, ny, PLAYER_ON_TARGET)
            else:
                self.set_cell(nx, ny, PLAYER)
        
        self.player_pos = (nx, ny)
        self.moves += 1
        return True
    
    def get_player_image(self):
        """根据玩家方向获取翻转后的图片"""
        if self.player_image is None:
            return None
        
        # 根据方向水平翻转图片（原始图片面向左边）
        if self.player_direction == 'right':
            return pygame.transform.flip(self.player_image, True, False)  # 水平翻转，面向右
        else:  # 'left', 'up', 'down' 使用原始图片（面向左）
            return self.player_image
    
    def is_complete(self):
        """检查关卡是否完成"""
        # 遍历当前关卡，查找所有目标位置状态
        boxes_on_targets = 0
        empty_targets = 0
        
        for row in self.level:
            for cell in row:
                if cell == BOX_ON_TARGET:
                    boxes_on_targets += 1
                elif cell == TARGET or cell == PLAYER_ON_TARGET:
                    empty_targets += 1
        
        # 只有当没有空目标且所有目标上都有箱子时才完成
        return empty_targets == 0 and boxes_on_targets > 0
    
    def reset_level(self):
        """重置当前关卡"""
        self.level = [list(row) for row in LEVELS[self.current_level]]
        self.player_pos = self.find_player()
        self.moves = 0
        self.player_direction = 'down'
        self.history = []  # 清空历史记录
    
    def next_level(self):
        """进入下一关"""
        self.current_level += 1
        if self.current_level >= len(LEVELS):
            return False  # 所有关卡完成
        self.level = [list(row) for row in LEVELS[self.current_level]]
        self.player_pos = self.find_player()
        self.moves = 0
        self.player_direction = 'down'
        self.history = []  # 清空历史记录
        return True
    
    def draw(self):
        """绘制游戏界面"""
        self.init_fonts()  # 确保字体已初始化
        self.screen.fill((200, 200, 200))
        
        # 绘制地图
        for y, row in enumerate(self.level):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                # 绘制地板
                pygame.draw.rect(self.screen, FLOOR_COLOR, rect)
                pygame.draw.rect(self.screen, (200, 200, 180), rect, 1)
                
                # 绘制不同的元素
                if cell == WALL:
                    pygame.draw.rect(self.screen, WALL_COLOR, rect)
                    pygame.draw.rect(self.screen, (100, 50, 10), rect, 1)
                    # 绘制墙壁纹理
                    for i in range(0, CELL_SIZE, 10):
                        pygame.draw.line(self.screen, (100, 50, 10), 
                                       (rect.x, rect.y + i), 
                                       (rect.x + CELL_SIZE, rect.y + i), 1)
                elif cell == TARGET:
                    pygame.draw.circle(self.screen, TARGET_COLOR, 
                                     (x * CELL_SIZE + CELL_SIZE // 2, 
                                      y * CELL_SIZE + CELL_SIZE // 2), 
                                     CELL_SIZE // 3)
                elif cell == BOX:
                    # 绘制球（圆形）
                    pygame.draw.circle(self.screen, BOX_COLOR, 
                                     (x * CELL_SIZE + CELL_SIZE // 2, 
                                      y * CELL_SIZE + CELL_SIZE // 2), 
                                     CELL_SIZE // 2 - 8)
                    # 绘制球的边框
                    pygame.draw.circle(self.screen, (150, 0, 0), 
                                     (x * CELL_SIZE + CELL_SIZE // 2, 
                                      y * CELL_SIZE + CELL_SIZE // 2), 
                                     CELL_SIZE // 2 - 8, 2)
                    # 绘制球的反光效果
                    pygame.draw.circle(self.screen, (255, 100, 100), 
                                     (x * CELL_SIZE + CELL_SIZE // 2 - 8, 
                                      y * CELL_SIZE + CELL_SIZE // 2 - 8), 
                                     CELL_SIZE // 4 - 4)
                elif cell == BOX_ON_TARGET:
                    pygame.draw.circle(self.screen, TARGET_COLOR, 
                                     (x * CELL_SIZE + CELL_SIZE // 2, 
                                      y * CELL_SIZE + CELL_SIZE // 2), 
                                     CELL_SIZE // 3)
                    # 绘制在目标上的球（圆形）
                    pygame.draw.circle(self.screen, BOX_ON_TARGET_COLOR, 
                                     (x * CELL_SIZE + CELL_SIZE // 2, 
                                      y * CELL_SIZE + CELL_SIZE // 2), 
                                     CELL_SIZE // 2 - 8)
                    # 绘制球的边框
                    pygame.draw.circle(self.screen, (100, 0, 0), 
                                     (x * CELL_SIZE + CELL_SIZE // 2, 
                                      y * CELL_SIZE + CELL_SIZE // 2), 
                                     CELL_SIZE // 2 - 8, 2)
                    # 绘制球的反光效果
                    pygame.draw.circle(self.screen, (255, 100, 100), 
                                     (x * CELL_SIZE + CELL_SIZE // 2 - 8, 
                                      y * CELL_SIZE + CELL_SIZE // 2 - 8), 
                                     CELL_SIZE // 4 - 4)
                elif cell == PLAYER:
                    # 绘制玩家图片
                    player_img = self.get_player_image()
                    if player_img:
                        self.screen.blit(player_img, (x * CELL_SIZE + 5, y * CELL_SIZE + 5))
                    else:
                        pygame.draw.circle(self.screen, PLAYER_COLOR, 
                                         (x * CELL_SIZE + CELL_SIZE // 2, 
                                          y * CELL_SIZE + CELL_SIZE // 2), 
                                         CELL_SIZE // 3)
                elif cell == PLAYER_ON_TARGET:
                    pygame.draw.circle(self.screen, TARGET_COLOR, 
                                     (x * CELL_SIZE + CELL_SIZE // 2, 
                                      y * CELL_SIZE + CELL_SIZE // 2), 
                                     CELL_SIZE // 3)
                    # 绘制玩家图片
                    player_img = self.get_player_image()
                    if player_img:
                        self.screen.blit(player_img, (x * CELL_SIZE + 5, y * CELL_SIZE + 5))
                    else:
                        pygame.draw.circle(self.screen, PLAYER_COLOR, 
                                         (x * CELL_SIZE + CELL_SIZE // 2, 
                                          y * CELL_SIZE + CELL_SIZE // 2), 
                                         CELL_SIZE // 3 - 5)
        
        # 绘制信息栏
        info_y = len(self.level) * CELL_SIZE + 5
        level_text = self.font.render(f"Level {self.current_level + 1}/{len(LEVELS)}", True, (0, 0, 0))
        self.screen.blit(level_text, (10, info_y))
        
        moves_text = self.font.render(f"Moves: {self.moves}", True, (0, 0, 0))
        self.screen.blit(moves_text, (200, info_y))
        
        # 显示操作提示
        hint_y = info_y + 30
        hint_text1 = self.small_font.render("Arrow/WASD: Move | R: Reset | U: Undo", True, (100, 100, 100))
        self.screen.blit(hint_text1, (10, hint_y))
        
        hint_y2 = hint_y + 20
        hint_text2 = self.small_font.render("ESC: Exit", True, (100, 100, 100))
        self.screen.blit(hint_text2, (10, hint_y2))
        
        pygame.display.flip()
    
    def show_menu(self):
        """显示主菜单"""
        self.init_fonts()  # 初始化字体
        menu_screen = pygame.display.set_mode((600, 500))
        pygame.display.set_caption("Sokoban Game - Menu")
        
        # 开始播放背景音乐
        if self.music_enabled:
            pygame.mixer.music.play(-1)  # -1 表示循环播放
        
        clock = pygame.time.Clock()
        
        while True:
            menu_screen.fill((240, 240, 240))
            
            # 标题
            title = self.font.render("Sokoban Game", True, (0, 0, 0))
            title_rect = title.get_rect(center=(300, 150))
            menu_screen.blit(title, title_rect)
            
            # 绘制小丑骑在球上的装饰
            ball_center = (300, 100)
            ball_radius = 25
            pygame.draw.circle(menu_screen, BOX_COLOR, ball_center, ball_radius)
            pygame.draw.circle(menu_screen, (150, 0, 0), ball_center, ball_radius, 3)
            # 反光
            pygame.draw.circle(menu_screen, (255, 100, 100), (ball_center[0] - 8, ball_center[1] - 8), 10)
            # 小丑
            if self.player_image:
                scaled_clown = pygame.transform.scale(self.player_image, (50, 50))
                menu_screen.blit(scaled_clown, (ball_center[0] - 25, ball_center[1] - 60))
            
            # 开始游戏按钮
            start_rect = pygame.Rect(200, 250, 200, 50)
            pygame.draw.rect(menu_screen, (70, 130, 180), start_rect)
            pygame.draw.rect(menu_screen, (0, 0, 0), start_rect, 2)
            start_text = self.font.render("Start Game (S)", True, (255, 255, 255))
            start_text_rect = start_text.get_rect(center=start_rect.center)
            menu_screen.blit(start_text, start_text_rect)
            
            # 退出按钮
            exit_rect = pygame.Rect(200, 320, 200, 50)
            pygame.draw.rect(menu_screen, (220, 20, 60), exit_rect)
            pygame.draw.rect(menu_screen, (0, 0, 0), exit_rect, 2)
            exit_text = self.font.render("Exit (Q)", True, (255, 255, 255))
            exit_text_rect = exit_text.get_rect(center=exit_rect.center)
            menu_screen.blit(exit_text, exit_text_rect)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        return True
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(event.pos):
                        return True
                    elif exit_rect.collidepoint(event.pos):
                        return False
            
            clock.tick(60)
    
    def show_victory(self):
        """显示胜利信息"""
        self.init_fonts()  # 确保字体已初始化
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # 胜利文本
        victory_text = self.font.render("Level Complete!", True, (255, 215, 0))
        victory_rect = victory_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.screen.blit(victory_text, victory_rect)
        
        # 步数信息
        moves_info = self.small_font.render(f"Total Moves: {self.moves}", True, (255, 255, 255))
        moves_rect = moves_info.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(moves_info, moves_rect)
        
        # 下一关提示
        if self.current_level < len(LEVELS) - 1:
            next_text = self.small_font.render("Press N for Next Level", True, (255, 255, 255))
        else:
            next_text = self.small_font.render("All Levels Complete! Press N to See Ending", True, (255, 255, 255))
        next_rect = next_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        self.screen.blit(next_text, next_rect)
        
        pygame.display.flip()
    
    def show_ending(self):
        """显示通关结局"""
        self.init_fonts()  # 确保字体已初始化
        
        # 创建全屏结局画面
        ending_screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Sokoban Game - Congratulations!")
        
        clock = pygame.time.Clock()
        
        while True:
            ending_screen.fill((20, 20, 50))  # 深蓝色背景
            
            # 标题 - Congratulations
            title_text = self.font.render("Congratulations! You Win!", True, (255, 215, 0))
            title_rect = title_text.get_rect(center=(400, 150))
            ending_screen.blit(title_text, title_rect)
            
            # 完成信息
            moves_text = self.small_font.render("You have completed all levels!", True, (255, 255, 255))
            moves_rect = moves_text.get_rect(center=(400, 220))
            ending_screen.blit(moves_text, moves_rect)
            
            # 重新开始按钮（缩小尺寸并调整位置）
            restart_rect = pygame.Rect(300, 270, 200, 50)
            mouse_pos = pygame.mouse.get_pos()
            if restart_rect.collidepoint(mouse_pos):
                button_color = (80, 150, 80)
            else:
                button_color = (70, 130, 180)
            pygame.draw.rect(ending_screen, button_color, restart_rect)
            pygame.draw.rect(ending_screen, (255, 255, 255), restart_rect, 2)
            restart_text = self.small_font.render("Restart Game (R)", True, (255, 255, 255))
            restart_text_rect = restart_text.get_rect(center=restart_rect.center)
            ending_screen.blit(restart_text, restart_text_rect)
            
            # 退出按钮（缩小尺寸并调整位置）
            exit_rect = pygame.Rect(300, 330, 200, 50)
            if exit_rect.collidepoint(mouse_pos):
                exit_button_color = (200, 60, 60)
            else:
                exit_button_color = (220, 20, 60)
            pygame.draw.rect(ending_screen, exit_button_color, exit_rect)
            pygame.draw.rect(ending_screen, (255, 255, 255), exit_rect, 2)
            exit_text = self.small_font.render("Exit (ESC/Q)", True, (255, 255, 255))
            exit_text_rect = exit_text.get_rect(center=exit_rect.center)
            ending_screen.blit(exit_text, exit_text_rect)
            
            # 绘制装饰元素（球和玩家）- 下移到更下方
            ball_center = (400, 520)
            ball_radius = 25
            pygame.draw.circle(ending_screen, BOX_COLOR, ball_center, ball_radius)
            pygame.draw.circle(ending_screen, (150, 0, 0), ball_center, ball_radius, 3)
            pygame.draw.circle(ending_screen, (255, 100, 100), (ball_center[0] - 8, ball_center[1] - 8), 10)
            
            if self.player_image:
                scaled_player = pygame.transform.scale(self.player_image, (50, 50))
                ending_screen.blit(scaled_player, (ball_center[0] - 25, ball_center[1] - 70))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True  # 重新开始
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        return False  # 退出
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_rect.collidepoint(event.pos):
                        return True  # 重新开始
                    elif exit_rect.collidepoint(event.pos):
                        return False  # 退出
            
            clock.tick(60)
    
    def run(self):
        """运行游戏主循环"""
        while True:
            if not self.show_menu():
                break
            
            # 重置游戏状态
            self.current_level = 0
            self.level = [list(row) for row in LEVELS[self.current_level]]
            self.player_pos = self.find_player()
            self.moves = 0
            self.player_direction = 'down'
            self.history = []  # 清空历史记录
            
            # 调整屏幕大小以适应当前关卡
            self.screen_width = len(self.level[0]) * CELL_SIZE
            self.screen_height = len(self.level) * CELL_SIZE + 85
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            pygame.display.set_caption("Sokoban Game - Playing")
            
            running = True
            waiting_for_next = False
            
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if waiting_for_next:
                            if event.key == pygame.K_n:
                                if self.current_level < len(LEVELS) - 1:
                                    # 进入下一关
                                    self.next_level()
                                    waiting_for_next = False
                                    # 调整屏幕大小
                                    self.screen_width = len(self.level[0]) * CELL_SIZE
                                    self.screen_height = len(self.level) * CELL_SIZE + 85
                                    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
                                else:
                                    # 所有关卡完成，显示通关结局
                                    running = False
                                    should_restart = self.show_ending()
                                    if not should_restart:
                                        pygame.quit()
                                        sys.exit()
                                    # 如果should_restart为True，则重置游戏状态并重新开始
                                    self.current_level = 0
                                    self.level = [list(row) for row in LEVELS[self.current_level]]
                                    self.player_pos = self.find_player()
                                    self.moves = 0
                                    self.player_direction = 'down'
                                    self.history = []  # 清空历史记录
                                    running = True
                                    waiting_for_next = False
                                    # 调整屏幕大小
                                    self.screen_width = len(self.level[0]) * CELL_SIZE
                                    self.screen_height = len(self.level) * CELL_SIZE + 85
                                    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
                            elif event.key == pygame.K_ESCAPE:
                                running = False
                        else:
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                self.move_player(0, -1)
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                self.move_player(0, 1)
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                self.move_player(-1, 0)
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                                self.move_player(1, 0)
                            elif event.key == pygame.K_r:
                                self.reset_level()
                            elif event.key == pygame.K_u:
                                self.undo()
                            elif event.key == pygame.K_ESCAPE:
                                running = False
                
                if not running:
                    break
                
                if not waiting_for_next:
                    self.draw()
                    
                    # 检查是否完成
                    if self.is_complete():
                        waiting_for_next = True
                        self.show_victory()
                
                self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = BoxPusherGame()
    game.run()

