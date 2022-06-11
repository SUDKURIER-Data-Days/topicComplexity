import csv
import sys
from manim import *
from manim_fontawesome import *
from manim_presentation import Slide
import math
import math as m
class Title(Slide):
    sys.setrecursionlimit(100000)

    def start_slide(self):
            text0 = Text("Wie komplex schreibt welches Ressort", font="Roboto").set_color(RED).scale(2)
            text1 = Text("Felix Kunze, Eric Jacob, Patrick Sonnentag", font="Roboto").scale(0.75).to_edge(DOWN)
            self.play(Write(text0))
            self.play(Write(text1))
            self.pause()
            self.clear()

    def complexity_slide(self):
        caption = Text("Runtime Complexity", font = "Roboto").to_edge(UP)
        axes = Axes(
            x_range = [0.001, 12.0, 1],
            y_range = [0.3, 9.0, 1],
            axis_config={"color": WHITE},
            x_axis_config = {
                "numbers_with_elongated_ticks": np.arange(0, 3.01, 2)
            },
            y_axis_config = {
                "numbers_with_elongated_ticks": None
            },
            tips = False
        )
        axes_labels = axes.get_axis_labels()

        exp_curve = axes.plot(lambda x: 1.25 ** x + 0.1, color = RED)
        log_curve = axes.plot(lambda x: m.log(x + 1) + 0.3, color = BLUE)

        exp_curve_label = axes.get_graph_label(exp_curve, "\\text{Classical Computer}").set_y(1).set_x(4.5)
        log_curve_label = axes.get_graph_label(log_curve, "\\text{Quantum Computer}").set_y(-1).set_x(4.5)

        self.add_foreground_mobject(caption)
        self.play(Create(caption), run_time = 1)
        self.play(Create(axes), run_time = 1)
        self.play(Create(exp_curve), run_time = 3)
        self.play(Create(exp_curve_label), run_time = 1)
        self.play(Create(log_curve), run_time = 5)
        self.play(Create(log_curve_label), run_time = 1)
        self.wait(1)
        self.pause()
        self.clear()

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
