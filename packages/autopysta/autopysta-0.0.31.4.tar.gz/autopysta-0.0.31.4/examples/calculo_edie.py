class Box:
    x_a = 0
    x_b = 0
    t_a = 0
    t_b = 0
    A = 0
    trails = []

    def __init__(self, xa, xb, ta, tb):
        self.x_a = xa
        self.x_b = xb
        self.t_a = ta
        self.t_b = tb
        self.A = (self.t_b - self.t_a)*(self.x_b - self.x_a)
        self.trails = [[{"x": -1, "t": -1}, {"x": -1, "t": -1}]]

    def contains(self, p):
        return self.x_a <= p['x'] <= self.x_b and self.t_a <= p['t'] <= self.t_b

    def get_intersection(self, p1, p2):
        t = -1
        x = -1
        if p1['x'] <= self.x_a <= p2['x']:
            t = (self.x_a - p1['x']) * (p2['t'] - p1['t']) / (p2['x'] - p1['x']) + p1['t']
            x = self.x_a
        elif p1['x'] <= self.x_b <= p2['x']:
            t = (self.x_b - p1['x']) * (p2['t'] - p1['t']) / (p2['x'] - p1['x']) + p1['t']
            x = self.x_b
        return {'x': x, 't': t}

    def get_edie(self):
        d = 0
        t = 0
        for tx in self.trails:
            d += tx[1]['x'] - tx[0]['x']
            t += tx[1]['t'] - tx[0]['t']
        return d/self.A, t/self.A


lane_1 = [
    [{"x": 5, "t": 0},
     {"x": 5.5, "t": 1},
     {"x": 6, "t": 2},
     ],  # tray 1
    [{"x": 2.5, "t": 3},
     {"x": 3, "t": 4},
     {"x": 3.5, "t": 5},
     ],  # tray 2
    [{"x": 0, "t": 0},
     {"x": 1.5, "t": 1},
     {"x": 3, "t": 2},
     {"x": 4.5, "t": 3},
     {"x": 6, "t": 4},
     ],  # tray 3
    [{"x": 0, "t": 3},
     {"x": 1, "t": 4},
     {"x": 2, "t": 5},
     {"x": 3, "t": 6},
     ],  # tray 4
]


def get_box_edges(t_a=0, t_b=0, t_size=0):
    intervals = []
    cuts = int((t_b - t_a) / t_size)
    t_size = int((t_b - t_a)/cuts)
    for i_ in range(cuts):
        intervals.append([t_a, t_a + t_size])
        t_a += t_size
    return intervals


t_1 = 0
t_2 = 6
t_s = 2
x_1 = 2
x_2 = 4

boxes = []
for i in get_box_edges(t_1, t_2, t_s):
    boxes.append(Box(x_1, x_2, i[0], i[1]))

# There must be at least one box
for t_i in range(len(lane_1)):
    trajectory = lane_1[t_i]
    for box in boxes:
        if box.trails[-1][0]['t'] != -1:
            box.trails.append([{"x": -1, "t": -1}, {"x": -1, "t": -1}])
    p_i = 0
    while p_i < len(trajectory):
        point = trajectory[p_i]
        # Get the box where t_a <= point <= t_b
        for box in boxes:
            if box.contains(point):
                if box.trails[-1][0]['t'] == -1:
                    box.trails[-1][0] = point
                    if p_i > 0:
                        prev_point = trajectory[p_i-1]
                        if not box.contains(prev_point):
                            mid = box.get_intersection(prev_point, point)
                            if box.contains(mid):
                                box.trails[-1][0] = mid
                if point['t'] >= box.trails[-1][1]['t']:
                    box.trails[-1][1] = point
                    if p_i + 1 < len(trajectory):
                        next_point = trajectory[p_i+1]
                        if not box.contains(next_point):
                            mid = box.get_intersection(point, next_point)
                            if box.contains(mid):
                                box.trails[-1][1] = mid
        p_i += 1

b_i = 1
for box in boxes:
    q, k = box.get_edie()
    print("Box:", b_i, "Q:", q, "K:", k)
    b_i += 1
