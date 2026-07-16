from abc import ABC, abstractmethod

import ephem
import numpy as np
import plotly.graph_objects as go


class Visualizer(ABC):
    def __init__(self, bodies_config, color_nasc, color_agora):
        self.bodies_config = bodies_config
        self.color_nasc = color_nasc
        self.color_agora = color_agora

    @abstractmethod
    def plot(self, fig, data_nasc, data_agora):
        pass


class HeliocentricOrbitVisualizer(Visualizer):
    def __init__(self, bodies_config, color_nasc, color_agora, calculator):
        super().__init__(bodies_config, color_nasc, color_agora)
        self.calculator = calculator

    def plot(self, fig, data_nasc, data_agora):
        for name, body in self.bodies_config.items():
            body.compute(data_nasc)
            r = float(body.sun_distance)
            theta = np.linspace(0, 2 * np.pi, 200)
            fig.add_trace(
                go.Scatter(
                    x=r * np.cos(theta),
                    y=r * np.sin(theta),
                    mode='lines',
                    name=f"Orbit {name}",
                    line=dict(color='#444', width=0.8, dash='dot'),
                    hoverinfo='text',
                    text=f"Orbit: {name}",
                    showlegend=False,
                )
            )

        for data, name_group, color in [
            (data_nasc, 'Birthchart', self.color_nasc),
            (data_agora, 'Current', self.color_agora),
        ]:
            pts_x, pts_y, labels = [0], [0], ['Sun']
            for name_b, body in self.bodies_config.items():
                x, y, _ = self.calculator.get_heliocentric_coords(data, body)
                pts_x.append(x)
                pts_y.append(y)
                labels.append(name_b)
            fig.add_trace(
                go.Scatter(
                    x=pts_x,
                    y=pts_y,
                    mode='markers+text',
                    name=name_group,
                    text=labels,
                    textposition='top center',
                    marker=dict(size=8, color=color),
                )
            )


class Heliocentric3DVisualizer(Visualizer):
    def __init__(self, bodies_config, color_nasc, color_agora, calculator):
        super().__init__(bodies_config, color_nasc, color_agora)
        self.calculator = calculator

    def plot(self, fig, data_nasc, data_agora):
        for data, name_group, color in [
            (data_nasc, 'Birthchart', self.color_nasc),
            (data_agora, 'Current', self.color_agora),
        ]:
            pts_x, pts_y, pts_z, labels = [0], [0], [0], ['Sun']
            for name_b, body in self.bodies_config.items():
                x, y, z = self.calculator.get_heliocentric_coords(data, body)
                pts_x.append(x)
                pts_y.append(y)
                pts_z.append(z)
                labels.append(name_b)
            fig.add_trace(
                go.Scatter3d(
                    x=pts_x,
                    y=pts_y,
                    z=pts_z,
                    mode='markers+text',
                    name=name_group,
                    text=labels,
                    marker=dict(size=6, color=color, opacity=0.9),
                )
            )


class GeocentricPolarVisualizer(Visualizer):
    def __init__(self, bodies_config, color_nasc, color_agora, observer_lat, observer_lon):
        super().__init__(bodies_config, color_nasc, color_agora)
        self.observer_lat = observer_lat
        self.observer_lon = observer_lon

    def plot(self, fig, data_nasc, data_agora):
        obs = ephem.Observer()
        obs.lat = self.observer_lat
        obs.lon = self.observer_lon

        for data, name, color, sym in [
            (data_nasc, 'Birthchart', self.color_nasc, 'circle'),
            (data_agora, 'Current', self.color_agora, 'x'),
        ]:
            obs.date = data
            longs = []
            radii = []
            labels = []

            for n, b in self.bodies_config.items():
                b.compute(obs)
                longs.append(np.degrees(ephem.Ecliptic(b).lon))
                dist = float(b.earth_distance)
                radii.append(np.log1p(dist))
                labels.append(n)

            fig.add_trace(
                go.Scatterpolar(
                    r=radii,
                    theta=longs,
                    mode='markers+text',
                    name=name,
                    text=labels,
                    marker=dict(size=10, color=color, symbol=sym),
                )
            )
