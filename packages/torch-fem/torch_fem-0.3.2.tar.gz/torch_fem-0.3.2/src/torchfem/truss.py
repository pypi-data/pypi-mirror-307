import torch
from torch import Tensor

from .base import FEM
from .elements import Bar1, Bar2
from .materials import Material


class Truss(FEM):
    def __init__(self, nodes: Tensor, elements: Tensor, material: Material):
        """Initialize a truss FEM problem."""

        super().__init__(nodes, elements, material)

        # Set up areas
        self.areas = torch.ones((len(elements)))

        # Element type
        if len(elements[0]) == 2:
            self.etype = Bar1()
        elif len(elements[0]) == 3:
            self.etype = Bar2()
        else:
            raise ValueError("Element type not supported.")

        # Set element type specific sizes
        self.n_strains = 1
        self.n_int = len(self.etype.iweights())

        # Initialize external strain
        self.ext_strain = torch.zeros(self.n_elem, self.n_strains)

    def D(self, B: Tensor, nodes: Tensor) -> Tensor:
        """Element gradient operator."""

        # Direction of the element
        dx = nodes[:, 1] - nodes[:, 0]
        # Length of the element
        l0 = torch.linalg.norm(dx, dim=-1)
        # Cosine and sine of the element
        cs = dx / l0[:, None]

        return torch.einsum("ijk,il->ijkl", B, cs).reshape(self.n_elem, -1)[:, None, :]

    def compute_k(self, detJ: Tensor, DCD: Tensor) -> Tensor:
        """Element stiffness matrix."""
        return torch.einsum("j,j,jkl->jkl", self.areas, detJ, DCD)

    def compute_f(self, detJ: Tensor, D: Tensor, S: Tensor) -> Tensor:
        """Element internal force vector."""
        return torch.einsum("j,j,jkl,jk->jl", self.areas, detJ, D, S)

    def plot(self, **kwargs):
        if self.n_dim == 2:
            self.plot2d(**kwargs)
        elif self.n_dim == 3:
            self.plot3d(**kwargs)

    @torch.no_grad()
    def plot2d(
        self,
        u: float | Tensor = 0.0,
        sigma: Tensor | None = None,
        node_labels: bool = True,
        show_thickness: bool = False,
        thickness_threshold: float = 0.0,
        default_color: str = "black",
    ):
        try:
            import matplotlib.pyplot as plt
            from matplotlib import cm
        except ImportError:
            raise Exception("Plotting 2D requires matplotlib.")

        # Line widths from areas
        if show_thickness:
            a_max = torch.max(self.areas)
            linewidth = 8.0 * self.areas / a_max
        else:
            linewidth = 2.0 * torch.ones(self.n_elem)
            linewidth[self.areas < thickness_threshold] = 0.0

        # Line color from stress (if present)
        if sigma is not None:
            cmap = cm.viridis
            vmin = min(float(sigma.min()), 0.0)
            vmax = max(float(sigma.max()), 0.0)
            color = cmap((sigma - vmin) / (vmax - vmin))
            sm = plt.cm.ScalarMappable(
                cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax)
            )
            plt.colorbar(sm, ax=plt.gca(), label="Stress", shrink=0.5)
        else:
            color = self.n_elem * [default_color]

        # Nodes
        pos = self.nodes + u
        plt.scatter(pos[:, 0], pos[:, 1], color=default_color, marker="o")
        if node_labels:
            for i, node in enumerate(pos):
                plt.annotate(
                    str(i), (node[0] + 0.01, node[1] + 0.1), color=default_color
                )

        # Bounding box
        size = torch.linalg.norm(pos.max() - pos.min())

        # Bars
        for j, element in enumerate(self.elements):
            n1 = element[0]
            n2 = element[1]
            x = [pos[n1][0], pos[n2][0]]
            y = [pos[n1][1], pos[n2][1]]
            plt.plot(x, y, linewidth=linewidth[j], c=color[j])

        # Forces
        for i, force in enumerate(self.forces):
            if torch.norm(force) > 0.0:
                s = 0.05 * size / torch.linalg.norm(force)  # scale
                plt.arrow(
                    float(pos[i][0]),
                    float(pos[i][1]),
                    s * force[0],
                    s * force[1],
                    width=0.05,
                    facecolor="gray",
                )

        # Constraints
        for i, constraint in enumerate(self.constraints):
            if constraint[0]:
                plt.plot(pos[i][0] - 0.1, pos[i][1], ">", color="gray")
            if constraint[1]:
                plt.plot(pos[i][0], pos[i][1] - 0.1, "^", color="gray")

        # Adjustments
        nmin = pos.min(dim=0).values
        nmax = pos.max(dim=0).values
        plt.axis(
            (
                float(nmin[0]) - 0.5,
                float(nmax[0]) + 0.5,
                float(nmin[1]) - 0.5,
                float(nmax[1]) + 0.5,
            )
        )
        plt.gca().set_aspect("equal", adjustable="box")
        plt.axis("off")

    @torch.no_grad()
    def plot3d(
        self, u=0.0, sigma=None, force_size_factor=0.5, constraint_size_factor=0.1
    ):
        try:
            import pyvista
        except ImportError:
            raise Exception("Plotting 3D requires pyvista.")

        pyvista.set_plot_theme("document")
        pyvista.set_jupyter_backend("client")
        pl = pyvista.Plotter()
        pl.enable_anti_aliasing("ssaa")

        # Nodes
        pos = self.nodes + u

        # Bounding box
        size = torch.linalg.norm(pos.max() - pos.min()).item()

        # Radii
        radii = torch.sqrt(self.areas / torch.pi)

        # Elements
        for j, element in enumerate(self.elements):
            n1 = element[0]
            n2 = element[1]
            tube = pyvista.Tube(pos[n1], pos[n2], radius=radii[j])
            if sigma is not None:
                sigma = sigma.squeeze()
                tube.cell_data["Stress"] = sigma[j]
                pl.add_mesh(tube, scalars="Stress", cmap="viridis")
            else:
                pl.add_mesh(tube, color="gray")

        # Forces
        force_centers = []
        force_directions = []
        for i, force in enumerate(self.forces):
            if torch.norm(force) > 0.0:
                force_centers.append(pos[i])
                force_directions.append(force / torch.linalg.norm(force))
        pl.add_arrows(
            torch.stack(force_centers).numpy(),
            torch.stack(force_directions).numpy(),
            mag=force_size_factor * size,
            color="gray",
        )

        # Constraints
        for i, constraint in enumerate(self.constraints):
            if constraint.any():
                sphere = pyvista.Sphere(
                    radius=constraint_size_factor * size, center=pos[i].numpy()
                )
                pl.add_mesh(sphere, color="gray")

        pl.show(jupyter_backend="client")
