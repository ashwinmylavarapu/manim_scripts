# the_calculator.py
from manim import *

class SingleNeuronProcess(Scene):
    def construct(self):
        # --- CONFIGURATION ---
        x_val = 0.8
        w_val = 0.7
        b_val = -0.4

        # --- PART 1: LINEAR CALCULATION ---

        # 1. Define all mobjects up front
        x_text = MathTex("x = {{%.1f}}" % x_val).to_edge(LEFT, buff=1.5)
        neuron = Circle(radius=1.2, color=BLUE, fill_opacity=0.2)
        neuron_group = VGroup(neuron).center()

        line = Line(x_text.get_right(), neuron.get_left())
        w_text = MathTex(f"w = {w_val}").next_to(line, UP, buff=0.2)
        
        bias_text = MathTex(f"b = {b_val}", color=ORANGE).next_to(neuron, DOWN, buff=1.5)
        line_bias = DashedLine(bias_text.get_top(), neuron.get_bottom())

        # Create copies for animation
        prod_val = x_val * w_val
        prod_text = MathTex(f"{prod_val:.2f}", color=GREEN)
        bias_anim_text = bias_text.copy()

        # Create the sum expression for inside the neuron
        sum_expression = MathTex("0.56", "+", "(-0.4)").move_to(neuron).scale(0.8)
        
        z_val = prod_val + b_val
        z_result = MathTex(f"z = {z_val:.2f}", color=YELLOW).move_to(neuron)
        
        # --- PART 2: ACTIVATION ---
        
        axes = Axes(x_range=[-4, 4, 1], y_range=[-0.1, 1.1, 0.2])
        axes.set(height=5.5, width=6.5).to_edge(RIGHT, buff=1)
        sigmoid_graph = axes.plot(lambda x: 1 / (1 + np.exp(-x)), color=GREEN)
        graph_label = Text("Activation Function").next_to(axes, UP, buff=0.2)

        output_val = sigmoid_graph.underlying_function(z_val)
        z_point = axes.c2p(z_val, 0)
        y_graph_point = axes.c2p(z_val, output_val)
        y_axis_point = axes.c2p(0, output_val)

        v_line = DashedLine(z_point, y_graph_point, color=YELLOW)
        h_line = DashedLine(y_graph_point, y_axis_point, color=YELLOW)
        final_output_text = MathTex(f"\\hat{{y}} \\approx {output_val:.2f}").next_to(y_axis_point, LEFT, buff=0.2)

        # --- THE ANIMATION (Single Play Call) ---
        self.play(
            Succession(
                # Initial setup
                Write(x_text),
                AnimationGroup(FadeIn(neuron_group), Write(w_text), Create(line)),
                Wait(0.5),

                # Multiplication
                ReplacementTransform(x_text.get_part_by_tex("0.8").copy().set_color(GREEN), prod_text.move_to(line.get_center())),
                FadeOut(w_text),
                Wait(0.5),

                # Move values into neuron and sum them
                AnimationGroup(
                    prod_text.animate.move_to(sum_expression[0].get_center()),
                    Write(bias_text),
                    Create(line_bias)
                ),
                ReplacementTransform(bias_text.copy(), bias_anim_text.move_to(sum_expression[2].get_center())),
                FadeIn(sum_expression[1]), # Fade in the '+' sign
                
                # Combine into the final sum z
                Wait(1),
                Transform(VGroup(prod_text, bias_anim_text, sum_expression[1]), z_result),
                Wait(1.5),

                # Transition to activation graph
                AnimationGroup(
                    FadeOut(x_text, line, bias_text, line_bias),
                    VGroup(neuron_group, VGroup(prod_text, bias_anim_text, sum_expression[1])).animate.to_edge(LEFT)
                ),
                AnimationGroup(Create(axes), Create(sigmoid_graph), Write(graph_label)),
                Wait(0.5),

                # Show activation mapping
                Create(v_line),
                Create(h_line),
                Write(final_output_text),
                Wait(3)
            ),
            run_time=20 # Total duration for the entire animation sequence
        )

# In the_calculator.py
from manim import *

class NeuronLayerScene(Scene):
    def construct(self):
        # --- CONFIGURATION ---
        title = Text("Part B: A Single Neuron Layer").to_edge(UP)

        # --- MOBJECT DEFINITIONS ---

        # 1. Diagram Components
        x_vec_obj = Matrix([["x_1"], ["x_2"]], h_buff=1.5)
        x_label = MathTex("\\vec{x} =").next_to(x_vec_obj, LEFT)
        x_group = VGroup(x_label, x_vec_obj)

        neurons = VGroup(*[Circle(radius=0.5, color=BLUE, fill_opacity=0.2) for _ in range(3)])
        neurons.arrange(DOWN, buff=0.5)

        lines = VGroup()
        input_entries = x_vec_obj.get_entries()
        for entry in input_entries:
            for neuron in neurons:
                lines.add(Line(entry.get_center(), neuron.get_left(), stroke_width=2, color=GREY))

        diagram_top = VGroup(x_group, lines, neurons).arrange(RIGHT, buff=2)

        W_matrix_obj = Matrix([["w_{11}", "w_{12}"], ["w_{21}", "w_{22}"], ["w_{31}", "w_{32}"]], h_buff=2).scale(0.7)
        W_label = MathTex("\\mathbf{W} =").next_to(W_matrix_obj, LEFT)
        W_group = VGroup(W_label, W_matrix_obj)

        b_vec_obj = Matrix([["b_1"], ["b_2"], ["b_3"]]).scale(0.7)
        b_label = MathTex("\\vec{b} =").next_to(b_vec_obj, LEFT)
        b_group = VGroup(b_label, b_vec_obj)
        
        matrices_group = VGroup(W_group, b_group).arrange(RIGHT, buff=0.8).next_to(diagram_top, DOWN, buff=0.75)
        
        full_diagram = VGroup(diagram_top, matrices_group).scale(0.8).move_to(ORIGIN)

        # 2. Equation Components (as targets)
        eq_z = MathTex("\\vec{z}").scale(1.2)
        eq_eq = MathTex("=").scale(1.2)
        eq_W = MathTex("\\mathbf{W}").scale(1.2)
        eq_x = MathTex("\\vec{x}").scale(1.2)
        eq_plus = MathTex("+").scale(1.2)
        eq_b = MathTex("\\vec{b}").scale(1.2)
        
        equation_group = VGroup(eq_z, eq_eq, eq_W, eq_x, eq_plus, eq_b).arrange(RIGHT).next_to(title, DOWN, buff=0.75)
        
        z_vec_final = Matrix([["z_1"], ["z_2"], ["z_3"]], h_buff=1.3).scale(0.9)
        y_hat_vec_final = Matrix([["\\hat{y}_1"], ["\\hat{y}_2"], ["\\hat{y}_3"]]).scale(0.8)

        # --- THE ANIMATION (Single Play Call) ---
        self.play(Succession(
            # Step 1: Show the full, clean diagram
            Write(title),
            FadeIn(full_diagram),
            Wait(2),

            # Step 2: Form the equation by moving parts of the diagram
            AnimationGroup(
                FadeOut(lines, neurons),
                Transform(W_group, eq_W),
                Transform(x_group, eq_x),
                Transform(b_group, eq_b),
                Write(eq_z),
                Write(eq_eq),
                Write(eq_plus)
            ),
            Wait(2),

            # Step 3: "Calculate" z by transforming the equation components
            Transform(
                VGroup(W_group, x_group, b_group, eq_plus), 
                z_vec_final.move_to(VGroup(W_group, x_group, b_group, eq_plus))
            ),
            Wait(2),
            
            # Step 4: Show the activation function
            Transform(
                VGroup(eq_z, eq_eq), 
                MathTex("\\vec{\\hat{y}}", "=").arrange(RIGHT).next_to(z_vec_final, LEFT)
            ),
            Write(MathTex("\\sigma(").next_to(z_vec_final, LEFT, buff=0.1)),
            Write(MathTex(")").next_to(z_vec_final, RIGHT, buff=0.1)),
            Wait(1.5),

            # Step 5: Show the final result
            FadeOut(VGroup(W_group, x_group, b_group, eq_plus)), # Fade out the now-empty z_vec_final placeholder
            ReplacementTransform(z_vec_final, y_hat_vec_final.move_to(neurons)),
            Wait(3)
        ))