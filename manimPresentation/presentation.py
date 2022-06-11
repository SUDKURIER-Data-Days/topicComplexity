import csv
import sys
from manim import *
from manim_fontawesome import *
from manim_presentation import Slide
import math
import math as m

class Title(Slide):
    def sprach_komp_slide(self):
        arrow = Arrow(start=config.left_side, end=config.right_side)
        self.add(arrow)
        dashed0 = DashedLine(config.bottom, config.top, dash_length=0.1).shift(LEFT*7+10/3*RIGHT)
        dashed1 = DashedLine(config.bottom, config.top, dash_length=0.1).shift(LEFT*7+25/3*RIGHT)
        self.add(dashed0, dashed1)


        with open("cxense_out_mittel.csv") as data:
            reader = csv.reader(data,delimiter=";")
            next(reader)
            i = 1.5
            for row in reader:
                color = 0;
                if row[0] == "medical-health":
                    color=RED
                elif row[0] == "news-and-politics":
                    color=GREY
                elif row[0] == "video-gaming":
                    color=GREEN
                elif row[0] == "sports":
                    color=BLUE
                elif row[0] == "business-and-finance":
                    color=YELLOW
                else:
                    color=BROWN

                r = float(row[1])/200-1
                wien = float(row[4]) - 9
                circle = Circle(radius=r,color=color,fill_opacity=1.0,stroke_color=color)
                circle.set_fill(color)
                circle.shift(LEFT* 7)
                text = Text(text=row[0],font_size=36,color=color)
                self.play(GrowFromCenter(circle),circle.animate.shift(RIGHT*10/3*wien))
                k = 0
                if i >= 3:
                    k=1
                self.play(GrowFromCenter(text), Write(text),text.animate.shift(RIGHT*(5.5-k)+ DOWN * i))
                i+=0.5

    def construct(self):
        self.sprach_komp_slide()
        self.pause()
