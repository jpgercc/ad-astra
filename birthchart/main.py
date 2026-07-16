import ephem
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timezone
from abc import ABC, abstractmethod

# --- CONFIGURAÇÕES ---
BODIES_CONFIG = {
    'Moon': ephem.Moon(), 'Mercury': ephem.Mercury(), 'Venus': ephem.Venus(),
    'Mars': ephem.Mars(), 'Jupiter': ephem.Jupiter(), 'Saturn': ephem.Saturn(),
    'Uranus': ephem.Uranus(), 'Neptune': ephem.Neptune(), 'Pluto': ephem.Pluto()
}
DEFAULT_NASC = '2001/08/26 22:42:00'
# Coordenadas fixas para Porto Alegre
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

# --- VISUALIZADORES ---
class Visualizer(ABC):
    @abstractmethod
    def plot(self, fig, data_nasc, data_agora):
        pass

class HeliocentricOrbitVisualizer(Visualizer):
    def plot(self, fig, data_nasc, data_agora):
        for name, body in BODIES_CONFIG.items():
            body.compute(data_nasc)
            r = float(body.sun_distance)
            theta = np.linspace(0, 2 * np.pi, 200)
            fig.add_trace(go.Scatter(x=r*np.cos(theta), y=r*np.sin(theta), mode='lines', 
                                     name=f"Orbit {name}", line=dict(color='#444', width=0.8, dash='dot'), 
                                     hoverinfo='text', text=f"Orbit: {name}", showlegend=False))
        
        for data, name_group, color in [(data_nasc, 'Birthchart', COLOR_NASC), (data_agora, 'Current', COLOR_AGORA)]:
            pts_x, pts_y, labels = [0], [0], ['Sun']
            for name_b, body in BODIES_CONFIG.items():
                x, y, _ = CelestialCalculator.get_heliocentric_coords(data, body)
                pts_x.append(x); pts_y.append(y); labels.append(name_b)
            fig.add_trace(go.Scatter(x=pts_x, y=pts_y, mode='markers+text', name=name_group, text=labels, 
                                     textposition="top center", marker=dict(size=8, color=color)))

class Heliocentric3DVisualizer(Visualizer):
    def plot(self, fig, data_nasc, data_agora):
        for data, name_group, color in [(data_nasc, 'Birthchart', COLOR_NASC), (data_agora, 'Current', COLOR_AGORA)]:
            pts_x, pts_y, pts_z, labels = [0], [0], [0], ['Sun']
            for name_b, body in BODIES_CONFIG.items():
                x, y, z = CelestialCalculator.get_heliocentric_coords(data, body)
                pts_x.append(x); pts_y.append(y); pts_z.append(z); labels.append(name_b)
            fig.add_trace(go.Scatter3d(x=pts_x, y=pts_y, z=pts_z, mode='markers+text', name=name_group, 
                                       text=labels, marker=dict(size=6, color=color, opacity=0.9)))

class GeocentricPolarVisualizer(Visualizer):
    def plot(self, fig, data_nasc, data_agora):
        obs = ephem.Observer()
        obs.lat = OBSERVER_LAT
        obs.lon = OBSERVER_LON
        
        for data, name, color, sym in [(data_nasc, 'Birthchart', COLOR_NASC, 'circle'), 
                                      (data_agora, 'Current', COLOR_AGORA, 'x')]:
            obs.date = data
            longs = []
            radii = []
            labels = []
            
            for n, b in BODIES_CONFIG.items():
                b.compute(obs)
                # Longitude eclíptica para o eixo angular
                longs.append(np.degrees(ephem.Ecliptic(b).lon))
                # Distância geocêntrica normalizada (Log para compressão de escala)
                # Adicionado pequeno epsilon para evitar log(0)
                dist = float(b.earth_distance)
                radii.append(np.log1p(dist)) 
                labels.append(n)
            
            fig.add_trace(go.Scatterpolar(
                r=radii, 
                theta=longs, 
                mode='markers+text', 
                name=name, 
                text=labels, 
                marker=dict(size=10, color=color, symbol=sym)
            ))

# --- MAIN ---
def main():
    print("1: Heliocentric 2D | 2: Geocentric Polar | 3: Heliocentric 3D")
    opcao = input("Escolha: ")
    
    strategies = {'1': HeliocentricOrbitVisualizer(), '2': GeocentricPolarVisualizer(), '3': Heliocentric3DVisualizer()}
    visualizer = strategies.get(opcao)
    
    if not visualizer:
        print("Opção inválida.")
        return

    fig = go.Figure()
    data_agora = datetime.now(timezone.utc).strftime('%Y/%m/%d %H:%M:%S')
    visualizer.plot(fig, DEFAULT_NASC, data_agora)
    
    layout_common = dict(paper_bgcolor="black", font=dict(color="white"))
    if isinstance(visualizer, HeliocentricOrbitVisualizer):
        fig.update_layout(**layout_common, plot_bgcolor="black", xaxis=dict(gridcolor='#222', scaleanchor="x", scaleratio=1), 
                          yaxis=dict(gridcolor='#222'), dragmode='zoom', title="Heliocentric 2D")
    elif isinstance(visualizer, Heliocentric3DVisualizer):
        fig.update_layout(**layout_common, scene=dict(bgcolor="black", xaxis=dict(gridcolor='#222'), yaxis=dict(gridcolor='#222'), zaxis=dict(gridcolor='#222')), title="Heliocentric 3D")
    else:
        fig.update_layout(**layout_common, polar=dict(bgcolor="black", radialaxis=dict(gridcolor='#333'), angularaxis=dict(gridcolor='#333', rotation=90)), title="Geocentric Polar (Porto Alegre)")
    
    fig.show()

if __name__ == "__main__":
    main()
