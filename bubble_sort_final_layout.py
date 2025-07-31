# bubble_sort_final_layout.py

from manim import *

# Use the more stable OpenGL renderer
config.renderer = "opengl"

class BubbleSortWithCodeScene(Scene):
    """
    A Manim scene to visualize Bubble Sort with a live code trace.
    This version fixes the final layout and overlap issues.
    """
    def construct(self):
        # 1. --- Create Mobjects ---
        title = Text("Bubble Sort with Code Trace", font_size=48).to_edge(UP)

        # --- Create the Code Block ---
        code_lines = [
            "<tt><b>def</b> bubble_sort(arr):</tt>",
            "<tt>n = len(arr)</tt>",
            "<tt>    <b>for</b> i <b>in</b> range(n - 1):</tt>",
            "<tt>        <b>for</b> j <b>in</b> range(n - i - 1):</tt>",
            "<tt>            <b>if</b> arr[j] &gt; arr[j + 1]:</tt>",
            "<tt>                arr[j], arr[j+1] = arr[j+1], arr[j]</tt>"
        ]

        # FIX 1: Slightly reduced font size for a better fit
        code = VGroup(*[
            MarkupText(line, font_size=22, font="Monospace")
            for line in code_lines
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        # Manually apply indentation
        indent_width = 0.4
        code[1].shift(RIGHT * indent_width)
        code[2].shift(RIGHT * indent_width)
        code[3].shift(RIGHT * 2 * indent_width)
        code[4].shift(RIGHT * 3 * indent_width)
        code[5].shift(RIGHT * 4 * indent_width)

        # --- Create the Number Mobjects ---
        numbers = [8, 5, 2, 6]
        mobjects = VGroup(*[
            VGroup(
                Square(side_length=1.0),
                Integer(n)
            ) for n in numbers
        ]).arrange(RIGHT, buff=0.5)
        
        # 2. --- Arrange the Layout ---
        
        # FIX 2: Position numbers first, then code relative to numbers.
        # This prevents any overlap regardless of screen size or font size.
        mobjects.move_to(LEFT * 4)
        code.next_to(mobjects, RIGHT, buff=1.5)
        
        # --- Create the Pointer ---
        pointer = Arrow(start=LEFT, end=RIGHT, color=RED, buff=0.25)
        pointer.next_to(code[0], LEFT)

        # 3. --- Animate the Scene ---
        self.play(Write(title))
        self.play(Write(code), FadeIn(mobjects, shift=UP))
        self.play(FadeIn(pointer))
        self.wait(1)

        # --- Bubble Sort Logic and Animation ---
        n = len(numbers)
        
        self.play(pointer.animate.next_to(code[1], LEFT))
        self.wait(1)

        for i in range(n - 1):
            self.play(pointer.animate.next_to(code[2], LEFT))
            self.wait(1)

            for j in range(n - i - 1):
                self.play(pointer.animate.next_to(code[3], LEFT))
                self.wait(1)

                obj1 = mobjects[j]
                obj2 = mobjects[j+1]
                
                self.play(
                    pointer.animate.next_to(code[4], LEFT),
                    Indicate(obj1, color=YELLOW),
                    Indicate(obj2, color=YELLOW)
                )
                self.wait(1)

                if obj1[1].get_value() > obj2[1].get_value():
                    self.play(pointer.animate.next_to(code[5], LEFT))
                    self.wait(1)

                    pos1 = obj1.get_center()
                    pos2 = obj2.get_center()
                    
                    self.play(
                        obj1.animate.move_to(pos2),
                        obj2.animate.move_to(pos1),
                        run_time=1.5
                    )
                    mobjects[j], mobjects[j+1] = mobjects[j+1], mobjects[j]
                
            sorted_element = mobjects[n - i - 1]
            self.play(sorted_element.animate.set_color(GREEN))
            self.wait(0.5)

        # --- Final Sorted State ---
        self.play(mobjects[0].animate.set_color(GREEN))
        
        sorted_text = Text("List is now sorted!", font_size=40).next_to(mobjects, DOWN, buff=1)
        self.play(Write(sorted_text))
        self.play(FadeOut(pointer))
        self.wait(3)