# osi_visualization.py

from manim import *

# Define custom colors for clarity
COLORS = {
    "data": PURE_BLUE,
    "l7": RED,
    "l6": ORANGE,
    "l5": YELLOW,
    "l4": GREEN,
    "l3": BLUE,
    "l2": PURPLE,
    "bits": LIGHT_GRAY,
    "layer_bg": "#333333",
}

class OSITraversal(Scene):
    def construct(self):
        """
        Main method to construct the OSI model traversal animation.
        """
        # --- 1. SETUP THE SCENE ---
        self.setup_layout()
        self.introduce_scene()

        # --- 2. ENCAPSULATION AT CLIENT ---
        self.show_encapsulation()

        # --- 3. TRANSMISSION ---
        self.show_transmission()

        # --- 4. DECAPSULATION AT SERVER ---
        self.show_decapsulation()

        # --- 5. CONCLUSION ---
        self.show_conclusion()

    def setup_layout(self):
        """Creates the visual layout of the OSI stacks and labels."""
        # Create Client and Server Stacks
        self.client_stack = self.create_osi_stack("Client", LEFT * 5)
        self.server_stack = self.create_osi_stack("Server", RIGHT * 5)
        
        # Create the physical medium line
        physical_medium = Line(
            # Corrected positioning to connect the physical layers
            self.client_stack[1][-1].get_bottom() + LEFT * 0.5,
            self.server_stack[1][-1].get_bottom() + RIGHT * 0.5,
            stroke_width=2,
            color=WHITE
        )
        
        self.play(
            FadeIn(self.client_stack),
            FadeIn(self.server_stack),
            Create(physical_medium)
        )
        self.wait(1)
        self.physical_medium = physical_medium

    def introduce_scene(self):
        """Displays the title and introduction text."""
        title = Text("HTTP Packet Traversal (OSI Model)").to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        self.title = title

    def show_encapsulation(self):
        """Animates the data encapsulation process down the client's OSI stack."""
        encapsulation_title = Text("1. Encapsulation (Client Side)").scale(0.7).next_to(self.title, DOWN)
        self.play(Write(encapsulation_title))

        # Start with the initial data packet at the Application Layer
        packet = self.create_packet_segment("Data", COLORS["data"])
        # Correctly position packet in the Application layer (index 0 of the layers VGroup)
        packet.move_to(self.client_stack[1][0].get_center())
        self.play(FadeIn(packet))
        self.wait(0.5)

        # Animate down the stack, adding a header at each layer
        for i in range(1, 7):  # i = 1..6 (destination layers 6 down to 1)
            source_layer_index = i - 1
            source_layer_number = 7 - source_layer_index
            
            # Correctly get layer name from the layers VGroup
            layer_name = self.client_stack[1][source_layer_index].submobjects[0].text
            step_text = Text(f"Adding {layer_name} Header", font_size=24).next_to(encapsulation_title, DOWN)
            self.play(Write(step_text))

            new_header = self.create_packet_segment(f"H{source_layer_number}", COLORS[f"l{source_layer_number}"])
            new_packet = VGroup(new_header, packet).arrange(RIGHT, buff=0)
            
            destination_layer_index = i
            self.play(
                # Correctly transform and move packet to the next layer
                Transform(packet, new_packet.move_to(self.client_stack[1][destination_layer_index].get_center())),
                FadeOut(step_text)
            )
            self.wait(0.5)

        self.final_packet = packet

    def show_transmission(self):
        """Animates the packet turning into bits and traversing the physical medium."""
        transmission_title = Text("2. Transmission (Physical Layer)").scale(0.7).next_to(self.title, DOWN)
        self.play(Write(transmission_title))

        # Transform the packet into a representation of bits
        bits = Text("01101000011101000111010001110000...", font_size=18, color=COLORS["bits"])
        # Correctly position bits in the Physical layer (index 6)
        bits.move_to(self.client_stack[1][6].get_center())
        self.play(ReplacementTransform(self.final_packet, bits))
        self.wait(0.5)

        # Animate bits moving across the physical medium
        self.play(bits.animate.move_to(self.server_stack[1][6].get_center()), run_time=3)
        self.wait(0.5)
        
        # Transform bits back into the full packet at the server side
        self.play(ReplacementTransform(bits, self.final_packet.copy().move_to(self.server_stack[1][6].get_center())))
        self.wait(0.5)
        self.play(FadeOut(transmission_title))

    def show_decapsulation(self):
        """Animates the data decapsulation process up the server's OSI stack."""
        decapsulation_title = Text("3. Decapsulation (Server Side)").scale(0.7).next_to(self.title, DOWN)
        self.play(Write(decapsulation_title))

        packet = self.final_packet.copy() # Use a copy to avoid modifying the original
        self.add(packet) # Add the copy to the scene to be manipulated

        # Animate up the stack, removing a header at each layer
        for i in range(5, -1, -1): # i = 5..0 (destination layers 2 up to 7)
            source_layer_index = i + 1
            
            # Correctly get layer name from the layers VGroup
            layer_name = self.server_stack[1][source_layer_index].submobjects[0].text
            step_text = Text(f"Processing & Removing {layer_name} Header", font_size=24).next_to(decapsulation_title, DOWN)
            self.play(Write(step_text))

            # The packet to be left after removing the header
            remaining_packet = packet.submobjects[1]
            
            destination_layer_index = i
            self.play(
                packet.submobjects[0].animate.fade(1), # Fade out the header
                # Correctly transform and move packet to the next layer
                Transform(packet, remaining_packet.copy().move_to(self.server_stack[1][destination_layer_index].get_center())),
                FadeOut(step_text)
            )
            self.wait(0.5)

        self.play(FadeOut(decapsulation_title))

    def show_conclusion(self):
        """Shows the final state and conclusion text."""
        conclusion_text = Text("Data successfully received by the Server's Application Layer!").scale(0.7)
        conclusion_text.next_to(self.title, DOWN)
        self.play(Write(conclusion_text))
        self.wait(3)
        # FIX: Use Group instead of VGroup for fading out all objects, as self.mobjects can contain non-VMobjects.
        self.play(FadeOut(Group(*self.mobjects)))

    def create_osi_stack(self, title_text, position):
        """Helper function to create a labeled OSI stack VGroup."""
        layers = VGroup()
        layer_names = [
            "7. Application", "6. Presentation", "5. Session",
            "4. Transport", "3. Network", "2. Data Link", "1. Physical"
        ]
        
        for name in layer_names:
            layer_box = Rectangle(width=3, height=0.7, fill_color=COLORS["layer_bg"], fill_opacity=0.8, stroke_color=WHITE)
            layer_text = Text(name, font_size=18).move_to(layer_box.get_center())
            layer = VGroup(layer_text, layer_box)
            layers.add(layer)
            
        layers.arrange(DOWN, buff=0)
        
        title = Text(title_text, font_size=32).next_to(layers, UP)
        # The final stack is a VGroup containing the title and the layers VGroup
        stack = VGroup(title, layers).move_to(position)
        return stack

    def create_packet_segment(self, text, color):
        """Helper function to create a segment of a packet (header or data)."""
        box = Rectangle(height=0.5, width=1.5, fill_color=color, fill_opacity=0.9, stroke_width=2)
        label = Text(text, font_size=18).move_to(box.get_center())
        return VGroup(box, label)
