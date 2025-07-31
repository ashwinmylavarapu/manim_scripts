# merge_sort.py (Corrected Version)

from manim import *

# Use the more stable OpenGL renderer
config.renderer = "opengl"

class MergeSortScene(Scene):
    """
    A Manim scene to visualize the Merge Sort algorithm with 4 numbers.
    This version fixes the premature ending bug.
    """
    def construct(self):
        # 1. --- Initial Setup ---
        title = Text("Merge Sort Algorithm", font_size=48).to_edge(UP)
        self.play(Write(title))

        numbers = [8, 5, 2, 6]
        
        mobjects = VGroup(*[
            VGroup(
                Square(side_length=1.0),
                Integer(n)
            ) for n in numbers
        ]).arrange(RIGHT, buff=0.5)

        status_text = Text("Start with an unsorted list.", font_size=36).next_to(mobjects, DOWN, buff=1.5)

        self.play(FadeIn(mobjects, shift=UP))
        self.play(Write(status_text))
        self.wait(2)

        # 2. --- Divide Phase ---
        new_text = Text("1. Divide: Split the list until each element is in its own list.", font_size=36).next_to(mobjects, DOWN, buff=1.5)
        left_half = VGroup(mobjects[0], mobjects[1])
        right_half = VGroup(mobjects[2], mobjects[3])
        
        self.play(
            FadeOut(status_text), FadeIn(new_text),
            left_half.animate.shift(LEFT * 2 + DOWN * 1.5),
            right_half.animate.shift(RIGHT * 2 + DOWN * 1.5)
        )
        status_text = new_text
        self.wait(2)
        
        elem_8, elem_5 = left_half[0], left_half[1]
        elem_2, elem_6 = right_half[0], right_half[1]
        
        self.play(
            elem_8.animate.shift(LEFT * 1 + DOWN * 1.5),
            elem_5.animate.shift(RIGHT * 1 + DOWN * 1.5),
            elem_2.animate.shift(LEFT * 1 + DOWN * 1.5),
            elem_6.animate.shift(RIGHT * 1 + DOWN * 1.5),
        )
        self.wait(2)

        # 3. --- Conquer & Merge Phase ---
        new_text = Text("2. Conquer: Merge the lists back together in sorted order.", font_size=36).to_edge(DOWN)
        self.play(FadeOut(status_text), FadeIn(new_text))
        status_text = new_text
        self.wait(2)

        # Merge [8] and [5] -> [5, 8]
        new_text = Text("Compare 5 and 8... 5 is smaller.", font_size=36).to_edge(DOWN)
        self.play(FadeOut(status_text), FadeIn(new_text), Indicate(elem_5), Indicate(elem_8))
        status_text = new_text
        
        # FIX: Animate movement instead of transforming
        sorted_left_group = VGroup(elem_5, elem_8).arrange(RIGHT, buff=0.5).move_to(left_half.get_center())
        self.play(
            elem_5.animate.move_to(sorted_left_group[0].get_center()),
            elem_8.animate.move_to(sorted_left_group[1].get_center())
        )
        self.wait(2)
        
        # Merge [2] and [6] -> [2, 6]
        new_text = Text("Compare 2 and 6... 2 is smaller.", font_size=36).to_edge(DOWN)
        self.play(FadeOut(status_text), FadeIn(new_text), Indicate(elem_2), Indicate(elem_6))
        status_text = new_text

        # FIX: Animate movement instead of transforming
        sorted_right_group = VGroup(elem_2, elem_6).arrange(RIGHT, buff=0.5).move_to(right_half.get_center())
        self.play(
            elem_2.animate.move_to(sorted_right_group[0].get_center()),
            elem_6.animate.move_to(sorted_right_group[1].get_center())
        )
        self.wait(2)

        # Final Merge: [5, 8] and [2, 6] -> [2, 5, 6, 8]
        new_text = Text("Finally, merge the two sorted halves.", font_size=36).to_edge(DOWN)
        self.play(FadeOut(status_text), FadeIn(new_text))
        status_text = new_text
        self.wait(1)

        placeholders = VGroup(*[Square(side_length=1.0, color=BLUE) for _ in range(4)])
        placeholders.arrange(RIGHT, buff=0.5).move_to(ORIGIN)
        self.play(DrawBorderThenFill(placeholders))

        # --- Step-by-step comparison ---
        # Compare 5 and 2 -> move 2
        new_text = Text("Compare 5 and 2... 2 is smaller.", font_size=36).to_edge(DOWN)
        self.play(FadeOut(status_text), FadeIn(new_text), Indicate(elem_5), Indicate(elem_2))
        status_text = new_text
        self.play(elem_2.animate.move_to(placeholders[0].get_center()))
        
        # Compare 5 and 6 -> move 5
        new_text = Text("Compare 5 and 6... 5 is smaller.", font_size=36).to_edge(DOWN)
        self.play(FadeOut(status_text), FadeIn(new_text), Indicate(elem_5), Indicate(elem_6))
        status_text = new_text
        self.play(elem_5.animate.move_to(placeholders[1].get_center()))
        
        # Compare 8 and 6 -> move 6
        new_text = Text("Compare 8 and 6... 6 is smaller.", font_size=36).to_edge(DOWN)
        self.play(FadeOut(status_text), FadeIn(new_text), Indicate(elem_8), Indicate(elem_6))
        status_text = new_text
        self.play(elem_6.animate.move_to(placeholders[2].get_center()))
        
        # 8 is the last remaining element
        new_text = Text("Move the last element, 8.", font_size=36).to_edge(DOWN)
        self.play(FadeOut(status_text), FadeIn(new_text), Indicate(elem_8))
        status_text = new_text
        self.play(elem_8.animate.move_to(placeholders[3].get_center()))

        self.play(FadeOut(placeholders))
        self.wait(1)

        # 4. --- Final Sorted State ---
        new_text = Text("List is now sorted!", font_size=40).to_edge(DOWN)
        final_group = VGroup(elem_2, elem_5, elem_6, elem_8)
        self.play(FadeOut(status_text), FadeIn(new_text))
        self.play(Wiggle(final_group))
        self.wait(3)