from matplotlib import pyplot as plt
import math

class Plotter:
    @staticmethod
    def plot_bar_chart(x, y, xlabel="Errors", ylabel="Frequency", figsize=(12, 8)):
        # Create a bar chart
        fig, ax = plt.subplots(figsize=figsize)
        bars = ax.bar(x, y)

        # Add bar labels
        ax.bar_label(bars, label_type='edge', padding = 4)  # 'edge' places labels at the bar's edge; use 'center' for center placement

        # Add labels and title
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title('Bar Chart with Labels')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        plt.show()

    @staticmethod
    def polar_projection(a, b, theta):
        """Projects points from a unit circle onto an ellipse.

        Args:
            a: Semi-major axis of the ellipse.
            b: Semi-minor axis of the ellipse.
            theta: Angle in radians.

        Returns:
            Tuple of x and y coordinates of the projected point.
        """
        x = a * math.cos(theta)
        y = b * math.sin(theta)
        return x, y

    @staticmethod
    def plot_pie_chart(labels, data, figsize=(10, 10)):
        fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(aspect="equal"))
        wedges, texts = ax.pie(data)

        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"), bbox=bbox_props, zorder=0, va="center")
        
        try:
            for i, p in enumerate(wedges):
                ang = (p.theta2 - p.theta1)/2. + p.theta1
                y = math.sin(ang * math.pi / 180)
                x = math.cos(ang * math.pi / 180)
                horizontalalignment = {-1: "right", 1: "left"}[int(math.copysign(1, x))]
                connectionstyle = f"angle,angleA=0,angleB={ang},rad=16"
                kw["arrowprops"].update({"connectionstyle": connectionstyle})
                # Using this function for label arrangement
                xt, yt = Plotter.polar_projection(2, 1.5, ang * math.pi / 180)
                ax.annotate(labels[i], xy=(x, y), xytext=(xt, yt), horizontalalignment=horizontalalignment, **kw)
        except Exception as e:
            print(f"Warning: {e}")
        finally:
            plt.show()


# E_SPEED_5 I_POWER_ON