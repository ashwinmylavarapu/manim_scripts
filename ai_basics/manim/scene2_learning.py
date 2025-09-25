from manim import *
import numpy as np

# This is the full code for Scene 2, Part A

class FeedForwardScene(Scene):
    def construct(self):
        title = Text("Scene 2A: The Feed-Forward Pass").to_edge(UP)
        axes = Axes(x_range=[0, 6, 1], y_range=[0, 6, 1], x_length=5, y_length=5)
        
        # --- Store data and predictions separately ---
        data_coords = [(1, 2), (2, 3), (3, 2.5), (4, 4), (5, 5)]
        pred_coords = [(x, y - 0.5) for x, y in data_coords] # Example poor predictions

        data_points = VGroup(*[Dot(axes.c2p(x, y), color=GREEN) for x, y in data_coords])
        data_label = Text("Our Data").next_to(axes, UP)
        data_group = VGroup(axes, data_points, data_label).to_edge(LEFT)

        nn = VGroup(
            VGroup(*[Circle(radius=0.3) for _ in range(2)]).arrange(DOWN, buff=0.75),
            VGroup(*[Circle(radius=0.3) for _ in range(4)]).arrange(DOWN, buff=0.5),
            Circle(radius=0.3)
        ).arrange(RIGHT, buff=1.5).center()
        
        lines = VGroup()
        for i in range(len(nn) - 1):
            for n1 in nn[i]:
                for n2 in nn[i+1]:
                    lines.add(Line(n1.get_right(), n2.get_left(), stroke_width=1.5, color=GREY))

        # --- ANIMATION (Using multiple self.play calls) ---
        self.play(Write(title))
        self.play(Create(data_group))
        self.play(Create(nn))
        self.play(Create(lines))
        self.wait(1)

        # Animate each data point feeding forward in a simple loop
        for i in range(len(data_coords)):
            x_data, y_data = data_coords[i]
            x_pred, y_pred = pred_coords[i]
            
            prediction_dot = Dot(axes.c2p(x_pred, y_pred), color=RED, radius=0.08)
            error_line = DashedLine(axes.c2p(x_data, y_data), axes.c2p(x_pred, y_pred), stroke_width=2, color=RED)
            flash_anim = ShowPassingFlash(lines.copy().set_color(YELLOW), time_width=0.5)

            self.play(AnimationGroup(
                flash_anim,
                Create(prediction_dot),
                Create(error_line)
            ), run_time=0.5)

        self.wait(1)
        self.play(Write(Text("High Initial Loss!", color=RED).next_to(data_group, RIGHT, buff=0.5)))
        self.wait(3)

# This is the full code for Scene 2, Part B

class GradientDescentScene(Scene):
    def construct(self):
        title = Text("Scene 2B: Minimizing Loss with Gradient Descent").to_edge(UP)

        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[0, 8, 2], x_length=7, y_length=7, z_length=5)
        
        # A 3D surface with a clear global and local minimum
        def loss_func(u, v):
            return 1.5 + (u**2 + v**2) * (1 + 0.5 * np.sin(2 * PI * u)) / (1 + 0.1 * (u**2 + v**2))

        loss_surface = Surface(
            lambda u, v: loss_func(u,v),
            u_range=[-2, 2], v_range=[-2, 2], resolution=(32, 32),
            fill_opacity=0.7,
            checkerboard_colors=[BLUE_D, BLUE_E]
        )
        
        ball = Sphere(radius=0.1, color=RED).move_to(axes.c2p(1.5, 1.0, loss_func(1.5, 1.0)))
        
        local_min_point = axes.c2p(0.8, 0, loss_func(0.8, 0))
        global_min_point = axes.c2p(-0.7, 0, loss_func(-0.7, 0))

        self.set_camera_orientation(phi=70 * DEGREES, theta=-110 * DEGREES)
        
        self.play(Write(title))
        self.play(Create(axes), Create(loss_surface))
        self.wait(1)
        self.play(Write(Text("Loss Landscape").to_edge(UR)))
        self.play(Create(ball))
        self.wait(1)

        # First descent into a local minimum
        self.play(MoveAlongPath(ball, ArcBetweenPoints(ball.get_center(), local_min_point)), run_time=2)
        self.wait(0.5)
        self.play(Write(Text("Local Minimum", font_size=36).next_to(ball, UP)))
        self.wait(2)
        
        # Fade out text and reset ball
        self.play(FadeOut(VGroup(ball, VGroup(*self.mobjects).get_family()[-1]))) # Fade last text
        ball.move_to(axes.c2p(-1.5, -1.5, loss_func(-1.5, -1.5)))
        self.play(Create(ball))
        self.wait(1)

        # Second descent into the global minimum
        self.play(MoveAlongPath(ball, ArcBetweenPoints(ball.get_center(), global_min_point)), run_time=2.5)
        self.wait(0.5)
        self.play(Write(Text("Global Minimum", font_size=36).next_to(ball, UP)))
        self.wait(3)

# This is the full code for Scene 2, Part C

class BackpropagationScene(Scene):
    def construct(self):
        title = Text("Scene 2C: How We Learn - Backpropagation").to_edge(UP)

        nn = VGroup(
            VGroup(*[Circle(radius=0.3) for _ in range(2)]).arrange(DOWN, buff=0.75),
            VGroup(*[Circle(radius=0.3) for _ in range(4)]).arrange(DOWN, buff=0.5),
            Circle(radius=0.3)
        ).arrange(RIGHT, buff=1.5).center()
        lines1 = VGroup(*[Line(n1.get_right(), n2.get_left()) for n1 in nn[0] for n2 in nn[1]])
        lines2 = VGroup(*[Line(n1.get_right(), n2.get_left()) for n1 in nn[1] for n2 in nn[2]])
        
        error_text = MathTex("\\text{error} = \\hat{y} - y", color=RED).next_to(nn[2], RIGHT)
        
        self.play(Write(title))
        self.play(Create(nn), Create(VGroup(lines1, lines2)))
        self.wait(1)
        
        self.play(Write(error_text))
        
        # Animate backward pass from output to hidden
        self.play(ShowPassingFlash(lines2.copy().set_color(RED).reverse_direction(), time_width=0.7))
        self.play(Indicate(lines2, color=RED))
        self.wait(0.5)

        # Animate backward pass from hidden to input
        self.play(ShowPassingFlash(lines1.copy().set_color(RED).reverse_direction(), time_width=0.7))
        self.play(Indicate(lines1, color=RED))
        self.wait(2)
        
        self.play(Write(Text("Weights are updated!", font_size=36).next_to(nn, DOWN)))
        self.wait(3)