import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx

class DesertGame:
    def __init__(self, params):
        # 初始化参数
        self.T = params['T']  # 总天数
        self.N = params['N']  # 区域个数
        self.M = params['M']  # 每天购买上限
        self.G = params['G']  # 采矿基础收益
        self.L = params['L']  # 负重上限
        self.S0 = params['S0']  # 初始资金
        self.W1 = params['W1']  # 水的单位重量
        self.W2 = params['W2']  # 食物的单位重量
        self.P1 = params['P1']  # 水的基准价格
        self.P2 = params['P2']  # 食物的基准价格
        self.A = params['A']    # 水的基础消耗量
        self.B = params['B']    # 食物的基础消耗量
        self.C = params['C']    # 天气状况
        self.D = params['D']    # 村庄区域
        self.E = params['E']    # 矿山区域
        self.F = params['F']    # 终点区域
        self.H = params['H']    # 相邻区域矩阵
        self.map_layout = params.get('map_layout', None)  # 地图布局（用于可视化）

        # 初始化状态
        self.state = {
            'position': 0,  # 当前位置
            'water': 0,     # 剩余水
            'food': 0,      # 剩余食物
            'money': self.S0  # 剩余资金
        }

        # 动态规划表
        self.dp = defaultdict(lambda: -np.inf)  # 初始化为负无穷
        self.dp[(0, 0, 0)] = self.S0  # 初始状态

        # 存储每天的状态（用于可视化）
        self.daily_states = []

    def is_adjacent(self, i, j):
        """检查区域i和j是否相邻"""
        return self.H[i][j] == 1

    def can_mine(self, t, position):
        """检查是否可以在当前位置挖矿"""
        return self.E[position] == 1 and t > 0

    def can_buy(self, t, position):
        """检查是否可以在当前位置购买资源"""
        return self.D[position] == 1

    def must_stay(self, t):
        """检查当天是否必须停留"""
        return self.C[t] == 1

    def update_state(self, current_state, action):
        """根据动作更新状态"""
        t, water, food = current_state
        position, move, mine, buy_water, buy_food = action

        # 计算资源消耗
        if mine:
            water_consumption = (1 + 2 * mine) * self.A[t]
            food_consumption = (1 + 2 * mine) * self.B[t]
        else:
            water_consumption = (2 - (move == 0)) * self.A[t]
            food_consumption = (2 - (move == 0)) * self.B[t]

        # 更新资源
        new_water = water - water_consumption + buy_water
        new_food = food - food_consumption + buy_food

        # 检查资源是否非负
        if new_water < 0 or new_food < 0:
            return None

        # 检查负重限制
        if (new_water * self.W1 + new_food * self.W2) > self.L:
            return None

        # 更新资金
        new_money = self.state['money'] + (self.G if mine else 0) - (buy_water * self.P1 + buy_food * self.P2)

        return (t + 1, new_water, new_food, new_money)

    def solve(self):
        """使用动态规划求解最优策略"""
        for t in range(self.T):
            next_dp = defaultdict(lambda: -np.inf)
            for state in self.dp:
                current_money = self.dp[state]
                t, water, food = state

                # 遍历所有可能的区域
                for next_position in range(self.N):
                    if not self.is_adjacent(self.state['position'], next_position):
                        continue

                    # 检查是否必须停留
                    if self.must_stay(t):
                        move = 0
                    else:
                        move = 1 if next_position != self.state['position'] else 0

                    # 检查是否可以挖矿
                    can_mine = self.can_mine(t, next_position)

                    # 遍历可能的购买量
                    for buy_water in range(0, self.M + 1):
                        for buy_food in range(0, self.M + 1):
                            # 更新状态
                            new_state = self.update_state((t, water, food), (next_position, move, can_mine, buy_water, buy_food))
                            if new_state is not None:
                                new_t, new_water, new_food, new_money = new_state
                                if new_money > next_dp[(new_t, new_water, new_food)]:
                                    next_dp[(new_t, new_water, new_food)] = new_money

            self.dp = next_dp

        # 计算最终回收所得
        max_money = 0
        for state in self.dp:
            t, water, food = state
            money = self.dp[state]
            recycle_value = (water * self.P1 + food * self.P2) / 2
            total = money + recycle_value
            if total > max_money:
                max_money = total

        return max_money

    def simulate(self):
        """模拟游戏过程并记录每天的状态"""
        position = 0  # 初始位置为起点
        water = 0     # 初始水为0
        food = 0      # 初始食物为0
        money = self.S0  # 初始资金
        self.daily_states = []
        initial_purchase_made = False  # 标志：是否已在起点购买资源

        # 在起点购买初始资源
        if self.can_buy(0, position) and not initial_purchase_made:
            # 计算可以购买的最大水量和食物量
            max_buy_water = min(self.M, (self.L - water * self.W1) // self.W1)
            max_buy_food = min(self.M, (self.L - food * self.W2) // self.W2)
            
            # 购买初始资源
            buy_water = max_buy_water
            buy_food = max_buy_food
            water += buy_water
            food += buy_food
            money -= buy_water * self.P1 + buy_food * self.P2
            initial_purchase_made = True  # 标志设置为已购买

        for t in range(self.T):
            self.daily_states.append({
                'day': t + 1,
                'position': position,
                'water': water,
                'food': food,
                'money': money
            })

            # 在这里可以添加逻辑来选择最优动作
            # 例如，选择移动到相邻区域、挖矿或购买资源

            # 示例：简单逻辑，实际应基于动态规划结果
            if self.can_buy(t, position) and position != 0:  # 只有非起点的村庄可以购买
                buy_water = min(self.M, (self.L - water * self.W1) // self.W1)
                buy_food = min(self.M, (self.L - food * self.W2) // self.W2)
                water += buy_water
                food += buy_food
                money -= buy_water * self.P1 + buy_food * self.P2

            if self.can_mine(t, position):
                money += self.G
                water -= 2 * self.A[t]
                food -= 2 * self.B[t]

            if not self.must_stay(t):
                # 移动到相邻区域
                moved = False
                for next_position in range(self.N):
                    if self.is_adjacent(position, next_position):
                        position = next_position
                        moved = True
                        break

            # 消耗资源
            water -= self.A[t]
            food -= self.B[t]

            # 检查资源是否耗尽
            if water < 0 or food < 0:
                print(f"游戏失败：资源耗尽于第 {t + 1} 天")
                return

        # 检查是否到达终点
        if position == self.F.index(1):  # 假设终点区域标记为1
            # 回收剩余资源
            recycle_value = (water * self.P1 + food * self.P2) / 2
            money += recycle_value
            print(f"到达终点！剩余资金（含回收所得）: {money}")
        else:
            print(f"未到达终点。剩余资金（不含回收所得）: {money}")

        self.daily_states.append({
            'day': self.T + 1,
            'position': position,
            'water': water,
            'food': food,
            'money': money
        })

    def visualize_map(self):
        """可视化地图和玩家路径"""
        if self.map_layout is None:
            print("地图布局未提供，无法可视化。")
            return

        # 创建图形
        plt.figure(figsize=(10, 8))
        G = nx.Graph()

        # 添加节点
        for i in range(self.N):
            G.add_node(i, pos=self.map_layout[i])

        # 添加边
        for i in range(self.N):
            for j in range(self.N):
                if self.H[i][j] == 1:
                    G.add_edge(i, j)

        # 绘制地图
        pos = nx.get_node_attributes(G, 'pos')
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, edge_color='gray')

        # 绘制玩家路径
        if self.daily_states:
            path = [state['position'] for state in self.daily_states]
            path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

            # 绘制起点和终点
            start_node = path[0]
            end_node = path[-1]
            nx.draw_networkx_nodes(G, pos, nodelist=[start_node], node_color='green', node_size=500, label='Start')
            nx.draw_networkx_nodes(G, pos, nodelist=[end_node], node_color='red', node_size=500, label='End')

        plt.title("Player Path Visualization")
        plt.legend()
        plt.show()

    def visualize_states(self):
        """可视化每天的状态"""
        if not self.daily_states:
            print("没有记录状态数据，无法可视化。")
            return

        days = [state['day'] for state in self.daily_states]
        water = [state['water'] for state in self.daily_states]
        food = [state['food'] for state in self.daily_states]
        money = [state['money'] for state in self.daily_states]

        plt.figure(figsize=(12, 8))

        # 绘制水的变化
        plt.subplot(3, 1, 1)
        plt.plot(days, water, marker='o', label='Water')
        plt.title("Water Changes")
        plt.xlabel("Day")
        plt.ylabel("Water (units)")
        plt.legend()

        # 绘制食物的变化
        plt.subplot(3, 1, 2)
        plt.plot(days, food, marker='o', label='Food')
        plt.title("Food Changes")
        plt.xlabel("Day")
        plt.ylabel("Food (units)")
        plt.legend()

        # 绘制资金的变化
        plt.subplot(3, 1, 3)
        plt.plot(days, money, marker='o', label='Money')
        plt.title("Money Changes")
        plt.xlabel("Day")
        plt.ylabel("Money (units)")
        plt.legend()

        plt.tight_layout()
        plt.show()