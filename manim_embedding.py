# word_embedding_visualization.py

from manim import *

class WordEmbedding(Scene):
    def construct(self):
        """
        Main method to construct the word embedding visualization.
        """
        # --- 1. SETUP THE SCENE ---
        self.setup_scene()

        # --- 2. INTRODUCE VECTORS ---
        self.show_word_vectors()

        # --- 3. PERFORM VECTOR ARITHMETIC ---
        self.animate_vector_arithmetic()

        # --- 4. SHOW RELATIONSHIPS ---
        self.show_relationships()
        
        self.wait(4)

    def setup_scene(self):
        """Sets up the 2D coordinate plane and title."""
        self.camera.background_color = "#333333"
        
        # Create a 2D plane to represent the vector space
        self.plane = NumberPlane(
            x_range=[-8, 8, 2],
            y_range=[-5, 5, 2],
            x_length=15,
            y_length=9,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 0.3
            }
        )
        self.add(self.plane)

        # Add title
        title = Text("Visualizing Word Embeddings").to_edge(UP)
        self.play(Write(title))
        self.title = title

    def show_word_vectors(self):
        """Plots the words and their corresponding vectors from the origin."""
        intro_text = Text("Words are represented as vectors (arrows) in a multi-dimensional space.", font_size=28).next_to(self.title, DOWN)
        self.play(Write(intro_text))

        # Define coordinates for our words in this simplified 2D space
        self.coords = {
            "Man": np.array([-2, -2, 0]),
            "Woman": np.array([2, -2, 0]),
            "King": np.array([-2, 2, 0]),
            "Queen": np.array([2, 2, 0]),
        }

        # Create dots and labels for each word
        self.dots = VGroup(*[Dot(self.coords[word], radius=0.1) for word in self.coords])
        self.labels = VGroup(*[Text(word, font_size=24).next_to(self.dots[i], UR, buff=0.1) for i, word in enumerate(self.coords)])
        
        self.play(FadeIn(self.dots), FadeIn(self.labels), FadeOut(intro_text))
        self.wait(1)

    def animate_vector_arithmetic(self):
        """Animates the equation: King - Man + Woman = Queen."""
        equation = MathTex(r"\text{King} - \text{Man} + \text{Woman} \approx \text{Queen}", font_size=48).next_to(self.title, DOWN)
        self.play(Write(equation))

        # 1. Start with the "King" vector
        king_vec = Arrow(ORIGIN, self.coords["King"], buff=0, color=YELLOW)
        king_label = MathTex(r"\vec{King}", color=YELLOW).next_to(king_vec.get_center(), LEFT)
        self.play(GrowArrow(king_vec), Write(king_label))
        self.wait(1)

        # 2. Subtract the "Man" vector
        man_vec = Arrow(ORIGIN, self.coords["Man"], buff=0, color=BLUE)
        man_label = MathTex(r"\vec{Man}", color=BLUE).next_to(man_vec.get_center(), LEFT)
        self.play(GrowArrow(man_vec), Write(man_label))
        self.wait(1)
        
        # Animate subtracting it (i.e., adding the negative)
        neg_man_vec = Arrow(self.coords["King"], self.coords["King"] - self.coords["Man"], buff=0, color=BLUE)
        self.play(
            FadeOut(man_vec, man_label),
            Transform(king_vec, Arrow(ORIGIN, self.coords["King"] - self.coords["Man"], buff=0, color=YELLOW)),
            GrowArrow(neg_man_vec)
        )
        self.wait(1)
        self.play(FadeOut(neg_man_vec))


        # 3. Add the "Woman" vector
        woman_vec = Arrow(ORIGIN, self.coords["Woman"], buff=0, color=RED)
        woman_label = MathTex(r"\vec{Woman}", color=RED).next_to(woman_vec.get_center(), RIGHT)
        self.play(GrowArrow(woman_vec), Write(woman_label))
        self.wait(1)

        # Animate adding it to the result
        add_woman_vec = Arrow(king_vec.get_end(), king_vec.get_end() + self.coords["Woman"], buff=0, color=RED)
        self.play(
            FadeOut(woman_vec, woman_label),
            Transform(king_vec, Arrow(ORIGIN, king_vec.get_end() + self.coords["Woman"], buff=0, color=YELLOW)),
            GrowArrow(add_woman_vec)
        )
        self.wait(1)

        # 4. Show the result is the "Queen" vector
        queen_vec = Arrow(ORIGIN, self.coords["Queen"], buff=0, color=GREEN, stroke_width=8)
        self.play(FadeOut(add_woman_vec, king_label), ReplacementTransform(king_vec, queen_vec))
        
        result_text = Text("Result", font_size=24, color=GREEN).next_to(self.coords["Queen"], DR)
        self.play(Write(result_text))
        self.wait(2)
        self.play(FadeOut(queen_vec, result_text, equation))

    def show_relationships(self):
        """Draws vectors between words to show learned relationships."""
        rel_text = Text("The distances and directions represent relationships.", font_size=28).next_to(self.title, DOWN)
        self.play(Write(rel_text))

        # Gender relationship
        gender_vec1 = Arrow(self.coords["Man"], self.coords["Woman"], buff=0.1, color=PINK, max_tip_length_to_length_ratio=0.1)
        gender_vec2 = Arrow(self.coords["King"], self.coords["Queen"], buff=0.1, color=PINK, max_tip_length_to_length_ratio=0.1)
        gender_label = Text("Gender", font_size=24, color=PINK).next_to(gender_vec1, DOWN)
        
        self.play(GrowArrow(gender_vec1), GrowArrow(gender_vec2))
        self.play(Write(gender_label))
        self.wait(2)

        # Royalty relationship
        royalty_vec1 = Arrow(self.coords["Man"], self.coords["King"], buff=0.1, color=GOLD, max_tip_length_to_length_ratio=0.1)
        royalty_vec2 = Arrow(self.coords["Woman"], self.coords["Queen"], buff=0.1, color=GOLD, max_tip_length_to_length_ratio=0.1)
        royalty_label = Text("Royalty", font_size=24, color=GOLD).next_to(royalty_vec1, LEFT)

        self.play(GrowArrow(royalty_vec1), GrowArrow(royalty_vec2))
        self.play(Write(royalty_label))
        self.wait(2)
