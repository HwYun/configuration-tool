class CoordinatePt:
    def __init__(self):
        self.x = 0
        self.y = 0


class TopView:
    def __init__(self):
        self.pts = list()
        for i in range(4):
            pt = CoordinatePt()
            self.pts.append(pt)


if __name__ == "__main__":
    a = TopView()
    a.pts[0].x = 2
    a.pts[0].y = 4

    print(a)
    for i in range(4):
        print(a.pts[i].x)
        print(a.pts[i].y)