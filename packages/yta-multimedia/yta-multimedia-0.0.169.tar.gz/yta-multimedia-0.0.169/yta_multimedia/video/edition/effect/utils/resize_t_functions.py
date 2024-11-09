#TODO: Remove this, it is now in C:\Users\dania\Desktop\PROYECTOS\yta-multimedia\yta_multimedia\video\edition\effect\moviepy\rate_functions\__init__.py
def zoom_in_t_func(zoom_ratio: float = 0.2):
    """
    Function that returns the resize value to make a moviepy
    video be zoomed in the 'zoom_ratio' zoom all the time.
    """
    return 1 + zoom_ratio

def zoom_out_t_func(zoom_ratio: float = 0.2):
    """
    Function that returns the resize value to make a moviepy
    video be zoomed out the 'zoom_ratio' zoom all the time.
    """
    return 1 - zoom_ratio

def linear_zoom_in_t_func(t, duration, zoom_ratio: float = 0.2):
    """
    Function that returns the resize value to make a moviepy
    video zoom in linearly to the 'zoom_ratio' zoom.
    """
    # TODO: Check 'zoom_ratio' is valid

    return 1 + zoom_ratio * (t / duration)

def linear_zoom_out_t_func(t, duration, zoom_ratio: float = 0.2):
    """
    Function that returns the resize value to make a moviepy
    video zoom out linearly to the 'zoom_ratio' zoom.
    """
    # TODO: Check 'zoom_ratio' is valid

    return 1 + zoom_ratio * (duration - (t / duration))

def linear_zoom_transition_t_func(t, duration, zoom_start: float = 1, zoom_end: float = 0.8):
    """
    Function that returns the resize value to make a moviepy
    video zoom in or out from the 'zoom_start' to the 'zoom_end'
    in the provided 'duration' time. If 'zoom_start' is greater
    than 'zoom_end' that will be a zoom out.
    """
    return zoom_start + (zoom_end - zoom_start) * (t / duration)

def logaritmic_zoom_transition_t_func(t, duration, zoom_start: float = 1, zoom_end: float = 0.8):
    # TODO: This has not been tested...
    import math

    zoom_start = math.log(zoom_start)
    zoom_end = math.log(zoom_end)

    # Interpolación logarítmica
    return math.exp(zoom_start + (zoom_end - zoom_start) * (t / duration))

def test_zoom_t_func(t, duration):
    import numpy as np
    
    zoom_base = 1 + 0.5 * (t / duration)  # Incrementa el zoom progresivamente desde 1 hasta 1.5 (ajusta como desees)
    
    # Amplitud de la oscilación, pequeña oscilación en el zoom
    oscillation_amplitude = 0.05  # La amplitud del balanceo, ajusta si es necesario
    oscillation_frequency = 2 * np.pi / 3  # Frecuencia de la oscilación (cada cuánto ocurre el ciclo de balanceo)
    
    # Oscilación suave basada en una función seno
    oscillation = np.sin(t * oscillation_frequency) * oscillation_amplitude
    
    # Factor final de zoom con oscilación aplicada
    return zoom_base + oscillation

    # # La base del zoom (por ejemplo, 1 significa sin zoom)
    # zoom_base = 1.1  
    # # La magnitud de las oscilaciones, puedes ajustarlo
    # oscilation_amplitude = 0.05  
    # # El tiempo t provoca una oscilación suave, usando sin(t) o cos(t)
    # oscillation = np.sin(t * 2 * np.pi / 3) * oscilation_amplitude
    # # Devolver el factor de zoom, que varía a lo largo del tiempo
    # return zoom_base + oscillation

