import ephem
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timezone

from views import (
    GeocentricPolarVisualizer,
    Heliocentric3DVisualizer,
    HeliocentricOrbitVisualizer,
)

# --- CONFIGURAÇÕES ---
BODIES_CONFIG = {
    'Moon': ephem.Moon(), 'Mercury': ephem.Mercury(), 'Venus': ephem.Venus(),
    'Mars': ephem.Mars(), 'Jupiter': ephem.Jupiter(), 'Saturn': ephem.Saturn(),
    'Uranus': ephem.Uranus(), 'Neptune': ephem.Neptune(), 'Pluto': ephem.Pluto()
}
DEFAULT_NASC = '2001/08/26 22:42:00'

# Coordenadas para geocentric polar plot
OBSERVER_LAT = '-30.0333'
OBSERVER_LON = '-51.2300'

# Cores otimizadas para alto contraste no fundo escuro
COLOR_NASC = '#00FF41' # Verde Neon
COLOR_AGORA = '#FF00FF' # Magenta Vibrante

# --- LÓGICA DE CÁLCULO ---
class CelestialCalculator:
    @staticmethod
    def get_heliocentric_coords(data, body):
        body.compute(data)
        ecl = ephem.Ecliptic(body)
        r = float(body.sun_distance)
        return r * np.cos(ecl.lat) * np.cos(ecl.lon), \
               r * np.cos(ecl.lat) * np.sin(ecl.lon), \
               r * np.sin(ecl.lat)


class UserInput:
    def __init__(self):
        self.strategies = {
            '1': HeliocentricOrbitVisualizer(BODIES_CONFIG, COLOR_NASC, COLOR_AGORA, CelestialCalculator),
            '2': GeocentricPolarVisualizer(BODIES_CONFIG, COLOR_NASC, COLOR_AGORA, OBSERVER_LAT, OBSERVER_LON),
            '3': Heliocentric3DVisualizer(BODIES_CONFIG, COLOR_NASC, COLOR_AGORA, CelestialCalculator),
        }

    def choose_visualizer(self):
        print("1: Heliocentric 2D | 2: Geocentric Polar | 3: Heliocentric 3D")
        option = input("Escolha: ")
        return self.strategies.get(option)

    def get_current_date(self):
        return datetime.now(timezone.utc).strftime('%Y/%m/%d %H:%M:%S')

    def create_figure(self, visualizer):
        fig = go.Figure()
        visualizer.plot(fig, DEFAULT_NASC, self.get_current_date())
        self.apply_layout(fig, visualizer)
        return fig

    def apply_layout(self, fig, visualizer):
        layout_common = dict(paper_bgcolor="black", font=dict(color="white"))
        if isinstance(visualizer, HeliocentricOrbitVisualizer):
            fig.update_layout(
                **layout_common,
                plot_bgcolor="black",
                xaxis=dict(gridcolor='#222', scaleanchor="x", scaleratio=1),
                yaxis=dict(gridcolor='#222'),
                dragmode='zoom',
                title="Heliocentric 2D",
            )
        elif isinstance(visualizer, Heliocentric3DVisualizer):
            fig.update_layout(
                **layout_common,
                scene=dict(
                    bgcolor="black",
                    xaxis=dict(gridcolor='#222'),
                    yaxis=dict(gridcolor='#222'),
                    zaxis=dict(gridcolor='#222'),
                ),
                title="Heliocentric 3D",
            )
        else:
            fig.update_layout(
                **layout_common,
                polar=dict(
                    bgcolor="black",
                    radialaxis=dict(gridcolor='#333'),
                    angularaxis=dict(gridcolor='#333', rotation=90),
                ),
                title="Geocentric Polar (Porto Alegre)",
            )

    def run(self):
        visualizer = self.choose_visualizer()

        if not visualizer:
            print("Opção inválida.")
            return

        self.create_figure(visualizer).show()

# --- MAIN ---
def main():
    UserInput().run()

if __name__ == "__main__":
    main()
