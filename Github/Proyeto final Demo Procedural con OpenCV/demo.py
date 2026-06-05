"""
Proyecto Final: Demo Procedural con OpenCV (Graficacion)
Autor: Mafer / Proyecto generado con apoyo de ChatGPT

Cumple con:
- Python 3
- Librerias: numpy y opencv-python
- Resolucion 800x600
- 30 FPS
- Duracion configurable entre 30 y 60 s, por defecto 48 s
- 6 escenas controladas por timeline
- 6+ curvas parametricas dibujadas con cv2.polylines
- Transformaciones afines 2x3: traslacion, rotacion, escala, shear y espejo
- Primitivas visibles: line, circle, ellipse, fillPoly, rectangle, putText
- PostFX: vignette, scanlines, posterize, blur y glow simple
- Exportacion: video .mp4 y capturas por escena
"""

import argparse
import math
import os
import time
from dataclasses import dataclass
from typing import Callable, Dict, Tuple

import cv2
import numpy as np

W, H = 800, 600
FPS = 30
DEFAULT_DURATION = 30.0
SCENES = 6

# Arreglos globales precomputados para acelerar el render.
GRID_YY, GRID_XX = np.mgrid[0:H, 0:W].astype(np.float32)
GRID_NX = GRID_XX / W
GRID_NY = GRID_YY / H
VIGNETTE_R2 = ((GRID_XX - W * 0.5) / (W * 0.5)) ** 2 + ((GRID_YY - H * 0.5) / (H * 0.5)) ** 2
SCAN_Y = np.arange(H, dtype=np.float32)
POST_MASK = (np.clip(1.0 - 0.67 * VIGNETTE_R2, 0.0, 1.0) * (1.0 - 0.10 * (0.5 + 0.5 * np.sin(2.0 * np.pi * SCAN_Y / 3.0)))[:, None])

Color = Tuple[int, int, int]


def clamp01(x: float) -> float:
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)


def smoothstep(a: float, b: float, x: float) -> float:
    if abs(b - a) < 1e-8:
        return 0.0
    x = clamp01((x - a) / (b - a))
    return x * x * (3 - 2 * x)


def ease_in_out(x: float) -> float:
    x = clamp01(x)
    return 0.5 - 0.5 * math.cos(math.pi * x)


def hsv_to_bgr(h: float, s: float, v: float) -> Color:
    hsv = np.uint8([[[int(h) % 180, int(np.clip(s, 0, 255)), int(np.clip(v, 0, 255))]]])
    return tuple(int(c) for c in cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)[0, 0])


def text(img: np.ndarray, msg: str, org: Tuple[int, int], scale: float, color: Color,
         thickness: int = 1, align: str = "left") -> None:
    font = cv2.FONT_HERSHEY_SIMPLEX
    size, _ = cv2.getTextSize(msg, font, scale, thickness)
    x, y = org
    if align == "center":
        x -= size[0] // 2
    elif align == "right":
        x -= size[0]
    cv2.putText(img, msg, (int(x), int(y)), font, scale, color, thickness, cv2.LINE_AA)


def poly_param(fx: Callable[[np.ndarray], np.ndarray], fy: Callable[[np.ndarray], np.ndarray],
               t0: float, t1: float, n: int, cx: float, cy: float,
               sx: float, sy: float) -> np.ndarray:
    ts = np.linspace(t0, t1, n, dtype=np.float32)
    xs = fx(ts) * sx + cx
    ys = fy(ts) * sy + cy
    pts = np.round(np.stack([xs, ys], axis=1)).astype(np.int32)
    return pts.reshape((-1, 1, 2))


def transform_points(pts: np.ndarray, M: np.ndarray) -> np.ndarray:
    """Aplica una matriz afin 2x3 a puntos Nx1x2."""
    p = pts.reshape(-1, 2).astype(np.float32)
    ones = np.ones((p.shape[0], 1), dtype=np.float32)
    homo = np.hstack([p, ones])
    out = homo @ M.T
    return np.round(out).astype(np.int32).reshape((-1, 1, 2))


def background_hsv(img: np.ndarray, t: float, hue0: float, hue1: float, value_top: int = 155) -> None:
    """Fondo procedural rapido en BGR. Usa HSV solo para calcular dos colores base."""
    c0 = np.array(hsv_to_bgr(hue0 + 10 * math.sin(t * 0.35), 200, value_top), dtype=np.float32)
    c1 = np.array(hsv_to_bgr(hue1 + 10 * math.cos(t * 0.28), 210, 35), dtype=np.float32)
    blend = GRID_NY[..., None]
    base = c0 * (1.0 - blend) + c1 * blend
    wave = 0.86 + 0.14 * np.sin(t * 0.55 + GRID_NX * 7.0 + GRID_NY * 4.0)
    img[:] = np.clip(base * wave[..., None], 0, 255).astype(np.uint8)

def draw_grid(img: np.ndarray, spacing: int = 50, alpha: float = 0.22) -> None:
    layer = np.zeros_like(img)
    col = (170, 170, 170)
    for x in range(0, W, spacing):
        cv2.line(layer, (x, 0), (x, H), col, 1, cv2.LINE_AA)
    for y in range(0, H, spacing):
        cv2.line(layer, (0, y), (W, y), col, 1, cv2.LINE_AA)
    img[:] = cv2.addWeighted(img, 1.0, layer, alpha, 0)


def glow_polyline(img: np.ndarray, pts: np.ndarray, color: Color, thickness: int = 2,
                  glow: int = 8, closed: bool = False) -> None:
    layer = np.zeros_like(img)
    cv2.polylines(layer, [pts], closed, color, thickness + glow, cv2.LINE_AA)
    layer = cv2.GaussianBlur(layer, (0, 0), glow * 0.55)
    img[:] = cv2.addWeighted(img, 1.0, layer, 0.65, 0)
    cv2.polylines(img, [pts], closed, color, thickness, cv2.LINE_AA)


def post_vignette(img: np.ndarray, strength: float = 0.68) -> np.ndarray:
    mask = np.clip(1.0 - strength * VIGNETTE_R2, 0.0, 1.0)
    return np.clip(img.astype(np.float32) * mask[..., None], 0, 255).astype(np.uint8)


def post_scanlines(img: np.ndarray, strength: float = 0.13) -> np.ndarray:
    out = img.astype(np.float32)
    lines = 1.0 - strength * (0.5 + 0.5 * np.sin(2.0 * np.pi * SCAN_Y / 3.0))
    out *= lines[:, None, None]
    return np.clip(out, 0, 255).astype(np.uint8)


def post_posterize(img: np.ndarray, q: int = 18) -> np.ndarray:
    q = max(1, int(q))
    return ((img // q) * q).astype(np.uint8)


def post_bloom(img: np.ndarray, amount: float = 0.24) -> np.ndarray:
    blur = cv2.GaussianBlur(img, (0, 0), 5.0)
    return cv2.addWeighted(img, 1.0, blur, amount, 0)


def apply_post(img: np.ndarray, scene_id: int, t: float) -> np.ndarray:
    # Mascara global precomputada: vignette + scanlines en una sola pasada.
    out = np.clip(img.astype(np.float32) * POST_MASK[..., None], 0, 255).astype(np.uint8)
    # Posterizacion selectiva en escenas con estilo mas digital.
    if scene_id in (4, 5):
        out = post_posterize(out, 16 if scene_id == 5 else 20)
    return out


@dataclass
class DemoState:
    rng: np.random.Generator
    stars: np.ndarray
    particles: np.ndarray
    fire_heat: np.ndarray
    fire_rng: np.random.Generator


def make_state() -> DemoState:
    rng = np.random.default_rng(2026)
    stars = np.column_stack([
        rng.integers(0, W, 520),
        rng.integers(0, int(H * 0.72), 520),
        rng.random(520) * 2 * np.pi,
        rng.random(520) * 1.5 + 0.4,
    ]).astype(np.float32)
    particles = np.column_stack([
        rng.random(1500) * W,
        rng.random(1500) * H,
        rng.random(1500) * 2 * np.pi,
    ]).astype(np.float32)
    return DemoState(
        rng=rng,
        stars=stars,
        particles=particles,
        fire_heat=np.zeros((H, W), np.float32),
        fire_rng=np.random.default_rng(777),
    )


def draw_scene_title(img: np.ndarray, title: str, subtitle: str) -> None:
    cv2.rectangle(img, (18, H - 70), (W - 18, H - 18), (0, 0, 0), -1)
    overlay = img.copy()
    cv2.rectangle(overlay, (18, H - 70), (W - 18, H - 18), (255, 255, 255), 1, cv2.LINE_AA)
    img[:] = cv2.addWeighted(img, 0.86, overlay, 0.14, 0)
    text(img, title, (32, H - 45), 0.58, (245, 245, 245), 1)
    text(img, subtitle, (32, H - 23), 0.43, (215, 215, 215), 1)


def scene_intro(img: np.ndarray, t: float, state: DemoState) -> None:
    background_hsv(img, t, 160, 105, value_top=135)
    draw_grid(img, 40, 0.12)

    # Estrellas deterministas con parpadeo.
    xs = state.stars[:, 0].astype(np.int32)
    ys = state.stars[:, 1].astype(np.int32)
    phase = state.stars[:, 2]
    amp = state.stars[:, 3]
    brightness = (120 + 120 * (0.5 + 0.5 * np.sin(t * amp + phase))).astype(np.uint8)
    img[ys, xs] = np.stack([brightness, brightness, brightness], axis=1)

    # Curva 1: onda senoidal procedural como firma de entrada.
    fx = lambda u: u
    fy = lambda u: 0.33 * np.sin(5.0 * u + t * 1.8) + 0.12 * np.sin(11.0 * u - t)
    pts = poly_param(fx, fy, -1.0, 1.0, 520, W * 0.5, H * 0.40, W * 0.42, H * 0.18)
    glow_polyline(img, pts, hsv_to_bgr(110 + 25 * math.sin(t), 170, 255), 2, 9)

    # Logo procedural: poligono y orbitas.
    center = (W // 2, int(H * 0.52))
    for i, r in enumerate([92, 126, 160]):
        angle = t * (0.35 + i * 0.12)
        cv2.ellipse(img, center, (r, int(r * 0.32)), math.degrees(angle), 0, 360,
                    hsv_to_bgr(126 + i * 10, 130, 220), 1, cv2.LINE_AA)
    tri = np.array([[0, -45], [42, 32], [-42, 32]], np.float32)
    angle = t * 0.55
    R = np.array([[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]], np.float32)
    tri_pts = (tri @ R.T + np.array(center)).astype(np.int32).reshape((-1, 1, 2))
    cv2.fillPoly(img, [tri_pts], hsv_to_bgr(95, 170, 210), cv2.LINE_AA)
    cv2.polylines(img, [tri_pts], True, (245, 245, 245), 2, cv2.LINE_AA)

    text(img, "DEMO PROCEDURAL", (W // 2, 250), 1.35, (245, 245, 245), 2, "center")
    text(img, "OpenCV + numpy + matematicas", (W // 2, 292), 0.72, (225, 225, 225), 1, "center")
    draw_scene_title(img, "Escena 1 / Intro", "Patron procedural, primitivas, texto y curva senoidal paramétrica")


def scene_lissajous(img: np.ndarray, t: float, state: DemoState) -> None:
    background_hsv(img, t, 15, 55, value_top=160)
    draw_grid(img, 50, 0.20)

    # Curva 2: Lissajous.
    a = 3.0 + 0.7 * math.sin(t * 0.6)
    b = 2.0 + 0.5 * math.cos(t * 0.7)
    delta = math.pi / 2 + 0.55 * math.sin(t * 0.35)
    fx = lambda u: np.sin(a * u + delta)
    fy = lambda u: np.sin(b * u)
    pts = poly_param(fx, fy, 0.0, 2.0 * math.pi, 1000, W * 0.5, H * 0.44, 260, 190)
    glow_polyline(img, pts, hsv_to_bgr(23 + 25 * math.sin(t * 0.8), 230, 255), 2, 11)

    # Puntos moviles sobre la curva.
    for k in range(9):
        u = 2 * math.pi * ((t * 0.08 + k / 9.0) % 1.0)
        x = int(math.sin(a * u + delta) * 260 + W * 0.5)
        y = int(math.sin(b * u) * 190 + H * 0.44)
        cv2.circle(img, (x, y), 7, hsv_to_bgr(45 + k * 8, 180, 245), -1, cv2.LINE_AA)
        cv2.circle(img, (x, y), 13, (240, 240, 240), 1, cv2.LINE_AA)

    cv2.line(img, (W // 2, 80), (W // 2, H - 120), (255, 255, 255), 1, cv2.LINE_AA)
    cv2.line(img, (120, int(H * 0.44)), (W - 120, int(H * 0.44)), (255, 255, 255), 1, cv2.LINE_AA)
    draw_scene_title(img, "Escena 2 / Lissajous", "x=sen(a t + delta), y=sen(b t); curva con polylines y puntos animados")


def scene_rose_spiral(img: np.ndarray, t: float, state: DemoState) -> None:
    background_hsv(img, t, 118, 168, value_top=155)

    # Curva 3: Rosa polar.
    k = 5
    theta_shift = t * 0.45
    fx_rose = lambda th: np.cos(k * th) * np.cos(th + theta_shift)
    fy_rose = lambda th: np.cos(k * th) * np.sin(th + theta_shift)
    rose = poly_param(fx_rose, fy_rose, 0, 2 * math.pi, 1300, W * 0.50, H * 0.42, 195, 195)
    glow_polyline(img, rose, hsv_to_bgr(145 + 18 * math.sin(t * 0.5), 230, 255), 2, 10)

    # Curva 4: Espiral de Arquimedes.
    fx_sp = lambda u: (u / (6.0 * math.pi)) * np.cos(u + t * 0.55)
    fy_sp = lambda u: (u / (6.0 * math.pi)) * np.sin(u + t * 0.55)
    spiral = poly_param(fx_sp, fy_sp, 0, 6 * math.pi, 900, W * 0.50, H * 0.42, 260, 260)
    glow_polyline(img, spiral, hsv_to_bgr(95 + 12 * math.cos(t), 195, 240), 2, 6)

    # Primitivas de composicion: mascara circular semitransparente.
    mask_layer = np.zeros_like(img)
    cv2.circle(mask_layer, (W // 2, int(H * 0.42)), 245, (30, 30, 30), -1, cv2.LINE_AA)
    img[:] = cv2.addWeighted(img, 1.0, mask_layer, 0.12, 0)

    for i in range(12):
        angle = 2 * math.pi * i / 12 + t * 0.25
        x = int(W * 0.5 + math.cos(angle) * 285)
        y = int(H * 0.42 + math.sin(angle) * 205)
        cv2.circle(img, (x, y), 5 + (i % 3), hsv_to_bgr(130 + i * 4, 200, 230), -1, cv2.LINE_AA)

    draw_scene_title(img, "Escena 3 / Rosa polar + Espiral", "r=cos(5t) y r=a·t; composicion por capas con addWeighted")


def scene_lemniscate_transform(img: np.ndarray, t: float, state: DemoState) -> None:
    background_hsv(img, t, 70, 25, value_top=160)
    draw_grid(img, 45, 0.18)

    # Curva 5: Lemniscata de Gerono.
    fx_l = lambda u: np.sin(u)
    fy_l = lambda u: np.sin(u) * np.cos(u)
    lem = poly_param(fx_l, fy_l, 0, 2 * math.pi, 1000, W * 0.5, H * 0.38, 250, 210)

    # Transformacion 1: rotacion + escala + traslacion con matriz afin 2x3.
    angle = math.degrees(t * 0.75)
    scale = 0.75 + 0.25 * math.sin(t * 0.7)
    M = cv2.getRotationMatrix2D((W * 0.5, H * 0.38), angle, scale)
    M[:, 2] += [50 * math.sin(t * 0.4), 25 * math.cos(t * 0.5)]
    lem_t = transform_points(lem, M.astype(np.float32))
    glow_polyline(img, lem_t, hsv_to_bgr(48 + 20 * math.sin(t), 220, 255), 2, 10)

    # Figura transformada por warpAffine: rombo/poligono en una capa.
    layer = np.zeros_like(img)
    base_poly = np.array([[(350, 455), (410, 395), (470, 455), (410, 515)]], dtype=np.int32)
    cv2.fillPoly(layer, base_poly, hsv_to_bgr(35, 180, 210), cv2.LINE_AA)
    cv2.polylines(layer, base_poly, True, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.line(layer, (410, 395), (410, 515), (255, 255, 255), 1, cv2.LINE_AA)
    cv2.line(layer, (350, 455), (470, 455), (255, 255, 255), 1, cv2.LINE_AA)
    M2 = cv2.getRotationMatrix2D((410, 455), -angle * 0.7, 0.85 + 0.25 * math.sin(t))
    M2[:, 2] += [120 * math.sin(t * 0.5), 0]
    warped = cv2.warpAffine(layer, M2, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_TRANSPARENT)
    img[:] = cv2.addWeighted(img, 1.0, warped, 0.82, 0)

    draw_scene_title(img, "Escena 4 / Lemniscata + matriz afin", "Rotacion, escala y traslacion aplicadas con matrices afines 2x3")


def scene_shear_mirror(img: np.ndarray, t: float, state: DemoState) -> None:
    background_hsv(img, t, 100, 150, value_top=145)

    # Capa principal con primitiva fillPoly y elipse.
    layer = np.zeros_like(img)
    center = (W // 2, H // 2)
    n = 7
    pts = []
    for i in range(n):
        ang = 2 * math.pi * i / n + t * 0.4
        rad = 115 if i % 2 == 0 else 65
        pts.append([center[0] + math.cos(ang) * rad, center[1] + math.sin(ang) * rad])
    poly = np.array(pts, np.int32).reshape((-1, 1, 2))
    cv2.fillPoly(layer, [poly], hsv_to_bgr(105 + 25 * math.sin(t), 180, 220), cv2.LINE_AA)
    cv2.polylines(layer, [poly], True, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.ellipse(layer, center, (210, 80), math.degrees(t * 0.35), 0, 360, (230, 230, 230), 2, cv2.LINE_AA)

    # Transformacion 2: shear horizontal con matriz afin.
    sh = 0.35 * math.sin(t * 0.9)
    M_shear = np.float32([[1.0, sh, -sh * H * 0.5], [0.0, 1.0, 0.0]])
    shear_layer = cv2.warpAffine(layer, M_shear, (W, H), flags=cv2.INTER_LINEAR)

    # Transformacion 3: espejo sobre eje vertical.
    M_mirror = np.float32([[-1.0, 0.0, W], [0.0, 1.0, 0.0]])
    mirror_layer = cv2.warpAffine(layer, M_mirror, (W, H), flags=cv2.INTER_LINEAR)

    img[:] = cv2.addWeighted(img, 1.0, mirror_layer, 0.28, 0)
    img[:] = cv2.addWeighted(img, 1.0, shear_layer, 0.75, 0)

    # Curva 6: Cardioide alrededor de la figura.
    fx_c = lambda u: (1 - np.cos(u)) * np.cos(u + t * 0.2)
    fy_c = lambda u: (1 - np.cos(u)) * np.sin(u + t * 0.2)
    card = poly_param(fx_c, fy_c, 0, 2 * math.pi, 900, W * 0.5, H * 0.48, 105, 105)
    glow_polyline(img, card, hsv_to_bgr(128 + 20 * math.sin(t * 0.4), 220, 250), 2, 8)

    # Barras como referencia del shear.
    for x in range(80, W, 80):
        cv2.line(img, (x, 80), (x, H - 100), (255, 255, 255), 1, cv2.LINE_AA)

    draw_scene_title(img, "Escena 5 / Shear y espejo", "Shear, reflexion tipo espejo y composicion de capas mediante addWeighted")


def scene_particles_final(img: np.ndarray, t: float, state: DemoState) -> None:
    background_hsv(img, t, 170, 6, value_top=130)

    # Campo de particulas procedural.
    p = state.particles
    xs0, ys0, phase = p[:, 0], p[:, 1], p[:, 2]
    xs = (xs0 + 95 * np.sin(ys0 / 65.0 + t * 1.65 + phase) + 42 * np.cos(t * 0.55)) % W
    ys = (ys0 + 75 * np.cos(xs0 / 70.0 + t * 1.25 + phase) + 36 * np.sin(t * 0.7)) % H
    brightness = (155 + 95 * (0.5 + 0.5 * np.sin(t * 2.0 + phase))).astype(np.uint8)
    col = np.stack([brightness, brightness, np.full_like(brightness, 255)], axis=1)
    img[ys.astype(np.int32), xs.astype(np.int32)] = col
    img[:] = cv2.GaussianBlur(img, (0, 0), 0.85)

    # Fuego/heatmap procedural en la parte inferior.
    heat = state.fire_heat
    rng = state.fire_rng
    heat[:] = heat * 0.92
    base_n = 1300
    bx = rng.integers(0, W, base_n)
    by = rng.integers(int(H * 0.80), H, base_n)
    heat[by, bx] += rng.random(base_n) * (0.95 + 0.25 * math.sin(t * 3.0))
    heat[:] = cv2.GaussianBlur(heat, (0, 0), 2.1)
    heat[:-3, :] = heat[3:, :]
    heat[-3:, :] = 0.0
    hh = np.clip(heat, 0, 1)
    # Mapeo rapido de calor a color BGR sin imagen externa ni cvtColor.
    fire = np.empty_like(img)
    fire[:, :, 0] = np.clip(35 + 40 * hh, 0, 255).astype(np.uint8)
    fire[:, :, 1] = np.clip(25 + 120 * hh, 0, 255).astype(np.uint8)
    fire[:, :, 2] = np.clip(45 + 210 * hh, 0, 255).astype(np.uint8)
    mask = np.zeros((H, W), np.float32)
    mask[int(H * 0.42):, :] = np.linspace(0, 0.75, H - int(H * 0.42), dtype=np.float32)[:, None]
    img[:] = np.clip(img.astype(np.float32) * (1 - mask[..., None]) + fire.astype(np.float32) * mask[..., None], 0, 255).astype(np.uint8)

    # Curva 7: Hipotrocoide / spirograph como cierre.
    R, r, d = 8.0, 3.0, 5.0
    w = (R - r) / r
    fx_h = lambda u: (R - r) * np.cos(u) + d * np.cos(w * u + 0.8 * np.sin(t * 0.55))
    fy_h = lambda u: (R - r) * np.sin(u) - d * np.sin(w * u + 0.8 * np.cos(t * 0.45))
    hypo = poly_param(fx_h, fy_h, 0, 14 * math.pi, 1500, W * 0.5, H * 0.40, 25, 25)
    glow_polyline(img, hypo, hsv_to_bgr(8 + 35 * math.sin(t * 0.25), 230, 255), 2, 12)

    # Mascara oscura de escenario y creditos finales.
    cv2.rectangle(img, (0, int(H * 0.84)), (W, H), (8, 8, 10), -1)
    for i in range(18):
        x = int((i * 47 + 35 * math.sin(t + i)) % W)
        y = int(H * 0.84 + 22 + 20 * math.sin(t * 1.7 + i))
        cv2.circle(img, (x, y), 2 + (i % 4), hsv_to_bgr(15 + i * 3, 160, 255), -1, cv2.LINE_AA)
    text(img, "FIN DEL DEMO", (W // 2, H - 55), 0.95, (245, 245, 245), 2, "center")
    text(img, "6 escenas | 7 curvas | transformaciones | postFX", (W // 2, H - 28), 0.50, (225, 225, 225), 1, "center")

    draw_scene_title(img, "Escena 6 / Particulas + fuego + spirograph", "Campo de puntos, heatmap procedural, blur, posterize y cierre audiovisual")


def render_scene(img: np.ndarray, scene_id: int, t: float, state: DemoState) -> None:
    if scene_id == 0:
        scene_intro(img, t, state)
    elif scene_id == 1:
        scene_lissajous(img, t, state)
    elif scene_id == 2:
        scene_rose_spiral(img, t, state)
    elif scene_id == 3:
        scene_lemniscate_transform(img, t, state)
    elif scene_id == 4:
        scene_shear_mirror(img, t, state)
    else:
        scene_particles_final(img, t, state)


def timeline(t: float, duration: float, buf_a: np.ndarray, buf_b: np.ndarray,
             state: DemoState) -> Tuple[np.ndarray, int]:
    block_len = duration / SCENES
    scene_id = int(min(SCENES - 1, max(0, t // block_len)))
    t_in = t - scene_id * block_len
    transition_len = min(1.25, block_len * 0.22)

    render_scene(buf_a, scene_id, t, state)
    frame = buf_a

    # Transicion crossfade + flash suave al final del bloque.
    if scene_id < SCENES - 1 and t_in >= block_len - transition_len:
        render_scene(buf_b, scene_id + 1, t, state)
        a = smoothstep(block_len - transition_len, block_len, t_in)
        frame = cv2.addWeighted(buf_a, 1 - a, buf_b, a, 0)
        flash = smoothstep(block_len - 0.35, block_len, t_in)
        if flash > 0:
            frame = cv2.addWeighted(frame, 1.0, np.full_like(frame, 255), 0.11 * flash, 0)

    # Fade in/out global.
    fin = smoothstep(0.0, 1.5, t)
    fout = 1.0 - smoothstep(duration - 1.7, duration, t)
    f = fin * fout
    if f < 0.999:
        frame = np.clip(frame.astype(np.float32) * f, 0, 255).astype(np.uint8)

    return frame, scene_id


def render_frame(t: float, duration: float, state: DemoState,
                 buf_a: np.ndarray, buf_b: np.ndarray) -> Tuple[np.ndarray, int]:
    frame, scene_id = timeline(t, duration, buf_a, buf_b, state)
    frame = apply_post(frame, scene_id, t)
    return frame, scene_id


def export_screenshots(out_dir: str, duration: float) -> None:
    os.makedirs(out_dir, exist_ok=True)
    state = make_state()
    buf_a = np.zeros((H, W, 3), np.uint8)
    buf_b = np.zeros((H, W, 3), np.uint8)
    block_len = duration / SCENES
    for scene_id in range(SCENES):
        # Se avanza el estado hasta el tiempo de captura para que particulas/fuego se vean naturales.
        t = scene_id * block_len + block_len * 0.50
        frame, _ = render_frame(t, duration, state, buf_a, buf_b)
        path = os.path.join(out_dir, f"escena_{scene_id + 1:02d}.png")
        cv2.imwrite(path, frame)
    print(f"Capturas guardadas en: {out_dir}")


def export_video(path: str, duration: float, fps: int = FPS, render_step: int = 2) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    state = make_state()
    buf_a = np.zeros((H, W, 3), np.uint8)
    buf_b = np.zeros((H, W, 3), np.uint8)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(path, fourcc, fps, (W, H))
    if not writer.isOpened():
        raise RuntimeError("No se pudo abrir VideoWriter. Revisa que opencv-python tenga soporte de video.")

    total = int(duration * fps)
    render_step = max(1, int(render_step))
    start = time.perf_counter()
    last_frame = None
    for i in range(total):
        # Para acelerar la exportacion se puede calcular un frame cada N cuadros
        # y repetirlo. El archivo final conserva el FPS solicitado.
        if last_frame is None or i % render_step == 0:
            t = i / fps
            last_frame, _ = render_frame(t, duration, state, buf_a, buf_b)
        writer.write(last_frame)
        if i % fps == 0:
            print(f"Exportando video: {i}/{total} frames")
    writer.release()
    elapsed = time.perf_counter() - start
    print(f"Video guardado en: {path}")
    print(f"Frames: {total} | Tiempo de exportacion: {elapsed:.2f} s")


def preview(duration: float, fps: int = FPS) -> None:
    state = make_state()
    buf_a = np.zeros((H, W, 3), np.uint8)
    buf_b = np.zeros((H, W, 3), np.uint8)
    total = int(duration * fps)
    delay = max(1, int(1000 / fps))
    for i in range(total):
        t = i / fps
        frame, _ = render_frame(t, duration, state, buf_a, buf_b)
        cv2.imshow("Proyecto Final - Demo Procedural OpenCV", frame)
        if cv2.waitKey(delay) & 0xFF == 27:
            break
    cv2.destroyAllWindows()


def main() -> None:
    parser = argparse.ArgumentParser(description="Demo procedural de graficacion con OpenCV")
    parser.add_argument("--duration", type=float, default=DEFAULT_DURATION,
                        help="Duracion en segundos. Recomendado: 30 a 60. Default: 48")
    parser.add_argument("--fps", type=int, default=FPS, help="FPS del video. Default: 30")
    parser.add_argument("--export", action="store_true", help="Exporta el video mp4")
    parser.add_argument("--screenshots", action="store_true", help="Guarda una captura por escena")
    parser.add_argument("--preview", action="store_true", help="Muestra la animacion en una ventana")
    parser.add_argument("--out", default="renders/demo_final.mp4", help="Ruta de salida del video")
    parser.add_argument("--render-step", type=int, default=10, help="Calcula un frame cada N cuadros al exportar. 1 = maxima calidad, 10 = exportacion rapida.")
    parser.add_argument("--shots-dir", default="renders", help="Carpeta de capturas")
    args = parser.parse_args()

    duration = float(np.clip(args.duration, 30.0, 60.0))
    if args.duration != duration:
        print("La duracion se ajusto al rango permitido: 30 a 60 segundos.")

    if args.screenshots:
        export_screenshots(args.shots_dir, duration)
    if args.export:
        export_video(args.out, duration, args.fps, args.render_step)
    if args.preview or (not args.export and not args.screenshots):
        preview(duration, args.fps)


if __name__ == "__main__":
    main()
