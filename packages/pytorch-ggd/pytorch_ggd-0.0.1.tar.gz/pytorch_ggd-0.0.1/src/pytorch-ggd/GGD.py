import torch
from torch import nn

class GGD:
    def __init__(self, loc=0.0, scale=1.0, power=2.0):
        self.loc = loc
        self.scale = scale
        self.power = power

    def cdf(self, x):
        dtype = x.dtype
        device = x.device

        loc = torch.tensor(self.loc, dtype=dtype, device=device)
        scale = torch.tensor(self.scale, dtype=dtype, device=device)
        power = torch.tensor(self.power, dtype=dtype, device=device)

        x_shifted = x - loc
        x_is_zero = x_shifted == 0
        safe_x_shifted = torch.where(x_is_zero, torch.ones_like(x_shifted), x_shifted)

        t = torch.abs(safe_x_shifted) / scale
        t_power = t ** power
        a = 1.0 / power

        gamma_upper = torch.igammac(a, t_power)
        gamma_upper_regularized = gamma_upper / torch.exp(torch.lgamma(a))
        half_gamma = 0.5 * gamma_upper_regularized

        cdf = torch.where(
            x_is_zero,
            0.5,
            torch.where(
                x_shifted > 0,
                1.0 - half_gamma,
                half_gamma
            )
        )
        return cdf

    def icdf(self, p):
        dtype = p.dtype
        device = p.device

        loc = torch.tensor(self.loc, dtype=dtype, device=device)
        scale = torch.tensor(self.scale, dtype=dtype, device=device)
        power = torch.tensor(self.power, dtype=dtype, device=device)

        eps = torch.finfo(dtype).eps
        p = p.clamp(eps, 1 - eps)

        # Initial guess for x
        x = torch.zeros_like(p, dtype=dtype, device=device)

        # Use the quantile of a standard normal as a better initial guess
        normal_icdf = torch.distributions.Normal(0, 1).icdf(p)
        x = normal_icdf * scale + loc

        max_iter = 100
        tol = 1e-6

        for _ in range(max_iter):
            x_old = x
            f = self.cdf(x) - p
            pdf = self.pdf(x)
            update = f / (pdf + eps)
            # Avoid NaNs in update
            update = torch.where(torch.isfinite(update), update, torch.zeros_like(update))
            x = x - update
            # Check convergence
            if torch.max(torch.abs(x - x_old)) < tol:
                break
        return x

    def pdf(self, x):
        dtype = x.dtype
        device = x.device

        loc = torch.tensor(self.loc, dtype=dtype, device=device)
        scale = torch.tensor(self.scale, dtype=dtype, device=device)
        power = torch.tensor(self.power, dtype=dtype, device=device)

        x_shifted = x - loc
        t = torch.abs(x_shifted) / scale
        t_power = t ** power
        normalization = power / (2 * scale * torch.exp(torch.lgamma(1 / power)))
        pdf = normalization * torch.exp(-t_power)
        return pdf

class GGDToUniform(nn.Module):
    def __init__(self, scale, latent_max, loc=0.0, power=2.0):
        super().__init__()
        self.scale = scale
        self.latent_max = latent_max
        self.loc = loc
        self.power = power
        self.ggd = GGD(loc=loc, scale=scale, power=power)

    def forward(self, x):
        x = (x - self.loc) / self.scale
        x = self.ggd.cdf(x)
        x = x - 0.5
        x = 2 * self.latent_max * x
        return x

class UniformToGGD(nn.Module):
    def __init__(self, scale, latent_max, loc=0.0, power=2.0):
        super().__init__()
        self.scale = scale
        self.latent_max = latent_max
        self.loc = loc
        self.power = power
        self.ggd = GGD(loc=loc, scale=scale, power=power)

    def forward(self, x):
        x = x / (2 * self.latent_max)
        x = x + 0.5
        x = torch.clamp(x, min=1e-6, max=1 - 1e-6)
        x = self.ggd.icdf(x)
        x = x * self.scale + self.loc
        return x
