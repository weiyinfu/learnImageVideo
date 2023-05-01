import numpy as np


def ball2rec(ps, rows, cols):
    if ps.shape[-1] != 3 or len(ps.shape) != 2:
        raise Exception(f"invalid shape {ps.shape}")
    pp = np.array(ps, dtype=np.float32)
    pp /= np.linalg.norm(pp, axis=1, keepdims=True)
    alpha = np.arccos(pp[:, 2])
    beta = np.arctan2(pp[:, 0], pp[:, 1])
    tx = np.round(alpha / np.pi * rows) % rows
    ty = np.round(beta / np.pi * cols) % cols
    ans = np.hstack([tx, ty])
    return ans


def rec2ball(ps, rows, cols):
    if ps.shape[-1] != 2 or len(ps.shape) != 2:
        raise Exception(f"invalid shape {ps.shape}")
    pp = np.array(ps, dtype=np.float32)
    alpha = pp[:, 0] / rows * np.pi
    beta = pp[:, 1] / cols * np.pi
    ball_z = np.cos(alpha)
    ball_x = np.sin(alpha) * np.sin(beta)
    ball_y = np.sin(alpha) * np.cos(beta)
    return np.hstack(ball_x, ball_y, ball_z)
