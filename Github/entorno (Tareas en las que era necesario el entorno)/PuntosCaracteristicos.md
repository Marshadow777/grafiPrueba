# Aplicación de SIFT, SURF y otros algoritmos de puntos característicos en Realidad Aumentada y Machine Learning

Los algoritmos como **SIFT, SURF, ORB, BRISK, AKAZE, Harris y FAST** se utilizan para encontrar **puntos característicos** en una imagen.  
Estos puntos son zonas importantes que pueden reconocerse aunque la imagen cambie de tamaño, rote, tenga diferente iluminación o se vea desde otro ángulo.

En palabras simples, estos algoritmos ayudan a que una computadora pueda decir:

> “Este punto de esta imagen corresponde con este punto de otra imagen”.

Esto es muy útil en áreas como la **realidad aumentada** y el **machine learning**.

---

## 1. ¿Qué son los puntos característicos?

Un **punto característico** es una zona de la imagen que contiene información visual importante, por ejemplo:

- Esquinas.
- Bordes.
- Texturas.
- Patrones únicos.
- Detalles fáciles de reconocer.

Por ejemplo:

```text
Una pared lisa → tiene pocos puntos característicos.
Un código QR, una portada de libro o una tarjeta con dibujos → tiene muchos puntos característicos.
```
Los algoritmos detectan esos puntos y luego generan una especie de “huella digital” de cada punto, llamada descriptor.

## 2. Proceso general de SIFT, SURF y similares

Normalmente funcionan así:

### Paso 1: Detectar puntos importantes

El algoritmo busca zonas de interés en la imagen.

Ejemplo:
```text
Imagen de una portada de libro
↓
Se detectan esquinas, letras, bordes y detalles
```

### Paso 2: Crear descriptores

Cada punto detectado se convierte en un vector numérico.

Por ejemplo:

```text
Punto 1 → [0.23, 0.55, 0.12, ...]
Punto 2 → [0.78, 0.13, 0.40, ...]
```

Ese vector describe cómo se ve la zona alrededor del punto.

### Paso 3: Comparar puntos entre imágenes

Se comparan los descriptores de una imagen con los de otra.

Por ejemplo:
```text
Imagen de referencia: portada.jpg
Imagen de cámara: frame_actual
```

Si muchos puntos coinciden, entonces el sistema sabe que la portada aparece en la cámara.

### Paso 4: Calcular posición y orientación

Después de encontrar coincidencias, se puede calcular:

- Dónde está el objeto.
- Qué tan lejos está.
- Si está inclinado.
- Si está rotado.
- Su perspectiva.

Esto se hace usando técnicas como:

```text
Homografía
RANSAC
Pose estimation
PnP
```

## Aplicación en realidad aumentada

