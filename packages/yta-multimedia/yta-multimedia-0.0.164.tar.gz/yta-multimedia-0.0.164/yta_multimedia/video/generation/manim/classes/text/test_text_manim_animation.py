from yta_multimedia.video.generation.manim.classes.base_manim_animation import BaseManimAnimation
from manim import *


class TestTextManimAnimation(BaseManimAnimation):
    """
    Animation just for testing with texts.
    """
    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.animate()

    def generate(self, text: str, duration: float, output_filename: str = 'output.mov'):
        """
        Checks and validates the provided parameters and generates
        the manim animation if those parameters are valid. The 
        'text' parameter is limited to 30 characters.
        """
        # Check and validate all parameters
        parameters = {}

        # Empty, for testing

        if not output_filename:
            output_filename = 'output.mov'

        # Generate the animation when parameters are valid
        super().generate(parameters, output_filename = output_filename)

        return output_filename
    
    def animate(self):
        """
        This code will generate the manim animation and belongs to the
        Scene manim object.
        """
        text = Text('Texto de prueba')

        self.play(
            AnimationGroup(
                text.animate(run_time = 1).shift(RIGHT),
                text.animate.rotate(PI / 8),
                text.animate(run_time = 0.8).scale(2)
            ),
            run_time = 2
        )

        self.wait(1)