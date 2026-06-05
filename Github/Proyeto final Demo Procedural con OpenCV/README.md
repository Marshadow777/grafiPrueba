# Proyecto Final: Demo Procedural con OpenCV

Demo procedural para la materia de **Graficación**, hecho en **Python 3** usando únicamente:

- `numpy`
- `opencv-python`

El demo genera un mundo visual completo sin imágenes externas, sin texturas descargadas y sin modelos importados. Todo se dibuja mediante ecuaciones, primitivas de OpenCV, curvas paramétricas, transformaciones afines, composición por capas y filtros.

---

## 1. Requisitos

Instalar Python 3 y después ejecutar:

```bash
pip install numpy opencv-python
```

---

## 2. Cómo ejecutar la vista previa

Desde la carpeta del proyecto:

```bash
python demo.py --preview
```

Para cerrar la ventana se presiona la tecla **ESC**.

---

## 3. Cómo exportar el video final

```bash
python demo.py --export --duration 30 --out renders/demo_final.mp4 --render-step 10
```


> Nota: `--render-step 10` acelera la exportación calculando un frame cada 2 cuadros, pero el archivo final conserva los 30 FPS. Para máxima suavidad se puede usar `--render-step 1`, aunque tarda más.

El video se guarda en:

```text
renders/demo_final.mp4
```

Características del video:

- Resolución: **800x600 px**
- FPS: **30**
- Duración por defecto: **30 segundos**
- Formato: **.mp4**

---

## 4. Cómo generar las capturas por escena

```bash
python demo.py --screenshots --duration 30 --shots-dir renders
```

Esto genera una imagen por escena:

```text
renders/escena_01.png
renders/escena_02.png
renders/escena_03.png
renders/escena_04.png
renders/escena_05.png
renders/escena_06.png
```

También se puede generar todo junto:

```bash
python demo.py --screenshots --export --duration 30
```

---

# Reporte del demo procedural

## Objetivo

Construir un demo procedural de graficación usando OpenCV, donde todos los elementos visuales sean generados en tiempo real mediante ecuaciones, algoritmos, primitivas de dibujo, curvas paramétricas, transformaciones geométricas y filtros de postprocesamiento. El demo no utiliza imágenes externas, sprites, modelos ni texturas descargadas.

---

## Arquitectura implementada

El proyecto está organizado en componentes simples para evitar código desordenado:

1. **Timeline**  
   Controla qué escena se muestra dependiendo del tiempo global `t`. Cada escena ocupa un bloque temporal dentro de la duración total del video. También aplica transiciones tipo `crossfade` entre escenas.

2. **Renderer**  
   Dibuja el frame actual usando buffers de imagen de OpenCV. Cada escena recibe un arreglo `img` y modifica sus píxeles mediante primitivas, curvas y capas.

3. **Scenes**  
   Cada escena está implementada como una función independiente:

   - `scene_intro`
   - `scene_lissajous`
   - `scene_rose_spiral`
   - `scene_lemniscate_transform`
   - `scene_shear_mirror`
   - `scene_particles_final`

4. **PostFX**  
   Aplica efectos visuales globales como viñeta, líneas de escaneo, posterización, blur y bloom.

5. **Exporter**  
   Permite guardar el video `.mp4` con `cv2.VideoWriter` y también genera una captura por escena con `cv2.imwrite`.

---

## Timeline de escenas

El demo dura **30 segundos** por defecto. Está dividido en 6 escenas de aproximadamente 5 segundos cada una.

| Escena | Tiempo aproximado | Descripción |
|---|---:|---|
| 1 | 0–5 s | Intro con estrellas, texto, órbitas, triángulo procedural y curva senoidal. |
| 2 | 5–10 s | Curva de Lissajous animada con puntos móviles. |
| 3 | 10–15 s | Rosa polar y espiral de Arquímedes combinadas en una composición circular. |
| 4 | 15–20 s | Lemniscata transformada con rotación, escala y traslación. |
| 5 | 20–25 s | Figura geométrica con shear, espejo y cardioide. |
| 6 | 25–30 s | Partículas, fuego procedural y curva tipo spirograph/hipotrocoide. |

Las transiciones entre escenas se hacen con `cv2.addWeighted`, mezclando dos buffers de imagen.

---

## Curvas paramétricas utilizadas

El proyecto usa más de 6 curvas paramétricas. Todas se generan con puntos calculados mediante `numpy` y se dibujan con `cv2.polylines`.

### 1. Curva senoidal de entrada

\[
x = u
\]

\[
y = 0.33\sin(5u + 1.8t) + 0.12\sin(11u - t)
\]

Se usa en la escena de introducción como una firma visual animada.

---

### 2. Curva de Lissajous

\[
x = \sin(au + \delta)
\]

\[
y = \sin(bu)
\]

Donde `a`, `b` y `delta` cambian suavemente con el tiempo para generar movimiento.

---

### 3. Rosa polar

\[
r = \cos(k\theta)
\]

Convertida a coordenadas cartesianas:

\[
x = r\cos(\theta + \theta_0)
\]

\[
y = r\sin(\theta + \theta_0)
\]

En el código se usa `k = 5`, generando una rosa de cinco pétalos.

---

### 4. Espiral de Arquímedes

\[
r = a\theta
\]

En forma cartesiana:

\[
x = r\cos(\theta)
\]

\[
y = r\sin(\theta)
\]

Se utiliza para crear una sensación de expansión alrededor de la rosa polar.

---

### 5. Lemniscata de Gerono

\[
x = \sin(u)
\]

\[
y = \sin(u)\cos(u)
\]

Después de generarse, esta curva es modificada mediante una matriz afín para mostrar transformación geométrica.

---

### 6. Cardioide

\[
r = 1 - \cos(u)
\]

Convertida a forma cartesiana:

\[
x = (1 - \cos u)\cos u
\]

\[
y = (1 - \cos u)\sin u
\]

Se dibuja alrededor de la figura transformada en la escena de shear y espejo.

---

### 7. Hipotrocoide / Spirograph

\[
x = (R-r)\cos(u) + d\cos\left(\frac{R-r}{r}u\right)
\]

\[
y = (R-r)\sin(u) - d\sin\left(\frac{R-r}{r}u\right)
\]

Aparece en la escena final junto con partículas y fuego procedural.

---

## Transformaciones implementadas

El proyecto incluye varias transformaciones geométricas visibles.

### 1. Rotación, escala y traslación

Se aplica a la lemniscata mediante una matriz afín 2x3 generada con:

```python
cv2.getRotationMatrix2D(centro, angulo, escala)
```

Después se modifica la columna de traslación:

```python
M[:, 2] += [dx, dy]
```

Con esto la curva cambia de tamaño, gira y se desplaza en la pantalla.

---

### 2. Shear

El shear horizontal se implementa con la matriz:

\[
M =
\begin{bmatrix}
1 & sh & -sh\cdot H/2 \\
0 & 1 & 0
\end{bmatrix}
\]

En código:

```python
M_shear = np.float32([[1.0, sh, -sh * H * 0.5], [0.0, 1.0, 0.0]])
cv2.warpAffine(layer, M_shear, (W, H))
```

Esto deforma la figura principal inclinándola horizontalmente.

---

### 3. Espejo

La reflexión o espejo sobre el eje vertical se hace con:

\[
M =
\begin{bmatrix}
-1 & 0 & W \\
0 & 1 & 0
\end{bmatrix}
\]

En código:

```python
M_mirror = np.float32([[-1.0, 0.0, W], [0.0, 1.0, 0.0]])
cv2.warpAffine(layer, M_mirror, (W, H))
```

Esto permite mostrar una copia reflejada de la figura.

---

## Composición por capas

El demo usa varios buffers o capas para componer imágenes:

```python
layer = np.zeros_like(img)
img[:] = cv2.addWeighted(img, 1.0, layer, alpha, 0)
```

También se usa composición con máscaras para mezclar el fuego procedural con la escena final. Esto permite que algunos efectos aparezcan gradualmente y no como elementos pegados de forma brusca.

---

## Primitivas de OpenCV utilizadas

El proyecto usa primitivas visibles de OpenCV:

- `cv2.line` para líneas, ejes y retículas.
- `cv2.circle` para partículas, puntos y órbitas.
- `cv2.ellipse` para órbitas y figuras geométricas.
- `cv2.fillPoly` para polígonos rellenos.
- `cv2.polylines` para curvas paramétricas.
- `cv2.rectangle` para paneles, base de fuego y zonas de texto.
- `cv2.putText` para créditos y títulos.

---

## Filtros y postprocesamiento

Se aplicaron varios efectos de postprocesamiento:

### Viñeta

Oscurece los bordes del frame para dirigir la atención al centro.

### Scanlines

Agrega líneas horizontales sutiles para dar un estilo de demo digital.

### Posterize

Reduce la cantidad de niveles de color en algunas escenas, produciendo un estilo más gráfico.

### Blur y bloom

El blur suaviza partículas y fuego. El bloom se logra mezclando la imagen original con una versión desenfocada para simular brillo.

---

## Conclusión

El demo demuestra el uso de graficación procedural mediante OpenCV. Cada escena se genera con ecuaciones matemáticas y primitivas de dibujo, sin utilizar imágenes externas ni modelos descargados. El proyecto integra curvas paramétricas, timeline, transiciones, composición por capas, transformaciones afines y filtros de postprocesamiento. Además, la estructura del código separa escenas, renderizado, timeline, efectos y exportación, lo cual facilita modificar o extender el demo en futuras versiones.
