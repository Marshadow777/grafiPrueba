# Práctica 3: Proyección de modelos tridimensionales virtuales en espacios reales

<div align="center">

## Graficación

### Realidad aumentada con marcador ArUco, OpenCV, GLFW y OpenGL

**Integrantes:**  
Roberto Roque Cervantes  
Luis Gerardo López  
Marcelo Vicente Pascual Tapia  

**Práctica:** Práctica 3  
**Tema:** Proyección de modelos tridimensionales virtuales en espacios reales  
**Modelo utilizado:** Campus ITM 3D / Ciudad 3D del Proyecto 2  
**Archivo principal:** `realidad_aumentada_mapa.py`  

</div>

---

## 1. Descripción general

Esta práctica consiste en implementar una aplicación de **realidad aumentada** capaz de proyectar un modelo tridimensional virtual sobre un espacio real capturado por la cámara. Para lograrlo, hemos utilizdo un **marcador ArUco** como referencia visual. Cuando el marcador es detectado en la imagen de la cámara, el programa calcula su posición y orientación respecto a la cámara, y posteriormente utiliza esa información para colocar encima del marcador el modelo 3D del campus desarrollado en el Proyecto 2.

El modelo virtual corresponde a la ciudad/campus 3D construida previamente con primitivas de OpenGL. En esta práctica no se dibuja el modelo en un espacio puramente virtual, sino que se integra visualmente sobre una imagen real tomada en tiempo real por la cámara. Esto permite observar el campus como si estuviera anclado físicamente al marcador impreso.

La práctica une dos áreas importantes de la graficación computacional:

- La **visión por computadora**, que es la encargada de detectar el marcador y estimar su pose.
- La **graficación 3D**, la encargada de renderizar el modelo virtual con OpenGL sobre la escena real.

---

## 2. Objetivo

El objetivo principal de la práctica es proyectar un modelo tridimensional virtual en un entorno real mediante técnicas de realidad aumentada, utilizando un marcador ArUco como punto de referencia espacial.

### Objetivos específicos

- Capturar video en tiempo real usando la cámara del equipo.
- Detectar un marcador ArUco dentro de cada frame capturado.
- Estimar la posición y orientación del marcador respecto a la cámara.
- Convertir la matriz de calibración de OpenCV a una matriz de proyección compatible con OpenGL.
- Convertir la pose calculada por OpenCV a una matriz de vista/modelo compatible con OpenGL.
- Renderizar el modelo 3D del campus ITM sobre el plano del marcador.
- Relacionar el proyecto con los temas de cámara, proyección, transformaciones, matrices, primitivas 3D y realidad aumentada.

---

## 3. Marco teórico

### 3.1 Realidad aumentada

La realidad aumentada es una técnica que permite combinar elementos virtuales con imágenes del mundo real. A diferencia de una escena 3D tradicional, donde todos los objetos son generados por computadora, en realidad aumentada existe una imagen real capturada por una cámara y sobre ella se colocan objetos digitales.

En esta práctica, la cámara captura el entorno físico y el programa dibuja el campus 3D encima del marcador detectado. De esta manera, el modelo virtual parece formar parte del espacio real.

### 3.2 Marcadores ArUco

Un marcador ArUco es una imagen cuadrada en blanco y negro que contiene un patrón codificado. Este patrón permite que OpenCV identifique el marcador, obtenga sus esquinas y calcule su orientación. Para esta práctica se utilizó un marcador perteneciente al diccionario `DICT_4X4_50` con el identificador configurado en el código como `MARKER_ID = 1`.

> **Observación técnica:** en el comentario inicial del código se menciona un marcador ID 0, pero la constante usada realmente dentro del programa es `MARKER_ID = 1`. Por esa razón, el reporte considera como marcador de trabajo el ArUco ID 1.

### 3.3 Pose del marcador

La pose describe la posición y orientación de un objeto respecto a la cámara. En el programa, la pose del marcador se calcula con la función `cv2.solvePnP()`, la cual recibe:

- Las coordenadas 3D reales de las esquinas del marcador.
- Las coordenadas 2D detectadas en la imagen.
- La matriz de cámara.
- Los coeficientes de distorsión.

Como resultado se obtienen:

| Variable | Significado |
|---|---|
| `rvec` | Vector de rotación del marcador. |
| `tvec` | Vector de traslación del marcador. |

Estos vectores permiten conocer cómo debe colocarse el modelo 3D para que coincida con el marcador físico.

### 3.4 Proyección en OpenGL

OpenGL necesita una matriz de proyección para saber cómo representar los objetos 3D en la pantalla. En una escena de realidad aumentada, esta matriz debe relacionarse con los parámetros de la cámara real. Por eso, el código transforma la matriz intrínseca de OpenCV en una matriz de proyección de OpenGL.

La matriz de cámara contiene valores como:

| Parámetro | Descripción |
|---|---|
| `fx` | Distancia focal horizontal. |
| `fy` | Distancia focal vertical. |
| `cx` | Centro óptico en X. |
| `cy` | Centro óptico en Y. |

Con esos valores se construye la matriz `P`, que luego se carga en OpenGL usando `glLoadMatrixf(P)`.

---

## 4. Tecnologías utilizadas

| Tecnología | Uso dentro de la práctica |
|---|---|
| Python | Lenguaje principal del programa. |
| OpenCV | Captura de cámara, detección del marcador ArUco y estimación de pose. |
| NumPy | Manejo de matrices, vectores y datos numéricos. |
| GLFW | Creación de ventana, contexto OpenGL y control del ciclo de renderizado. |
| PyOpenGL | Renderizado del fondo de cámara y del modelo 3D. |
| ArUco | Marcador visual usado como referencia para anclar el modelo. |
| Modelo `itm.py` | Archivo del Proyecto 2 que contiene las funciones para dibujar el campus 3D. |

---

## 5. Materiales y recursos

Para realizar la práctica se utilizaron los siguientes elementos:

- Computadora con Python instalado.
- Cámara web o cámara integrada.
- Marcador ArUco ID 1 impreso o mostrado en pantalla.
- Código de realidad aumentada: `realidad_aumentada_mapa.py`.
- Código del modelo 3D del Proyecto 2: `itm.py`.
- Librerías: `opencv-contrib-python`, `glfw`, `PyOpenGL` y `numpy`.
- Archivo opcional de calibración de cámara: `camera_ar.npz`.

---

## 6. Marcador utilizado

El marcador usado para anclar el modelo virtual es un marcador ArUco cuadrado. El código trabaja con el diccionario:

```python
ARUCO_DICT = cv2.aruco.DICT_4X4_50
MARKER_ID = 1
```

La imagen del marcador usada como referencia fue la siguiente:

![Marcador ArUco ID 1](marcador_aruco_id1.png)

Este marcador funciona como el plano real sobre el cual se proyecta el modelo 3D del campus. Cuando la cámara lo detecta, el programa calcula sus cuatro esquinas y coloca el modelo virtual sobre su superficie.

---

## 7. Estructura general del programa

El archivo principal de la práctica es:

```text
realidad_aumentada_mapa.py
```

La estructura del programa puede entenderse en las siguientes secciones:

| Sección | Descripción |
|---|---|
| Importaciones | Carga de OpenCV, GLFW, NumPy, OpenGL y el modelo `itm`. |
| Constantes globales | Configuración de cámara, marcador, escala del mapa, título de ventana y planos de recorte. |
| Calibración de cámara | Carga de `camera_ar.npz` o creación de una matriz de cámara aproximada. |
| Detector ArUco | Creación del detector y búsqueda del marcador en cada frame. |
| Estimación de pose | Cálculo de `rvec` y `tvec` mediante `solvePnP()`. |
| Matriz de proyección | Conversión de la matriz de cámara a matriz de proyección de OpenGL. |
| Matriz modelo-vista | Conversión de la pose de OpenCV al sistema de coordenadas de OpenGL. |
| Fondo de cámara | Conversión del frame de OpenCV en una textura para dibujarlo como fondo. |
| Renderizado del modelo | Dibujo del campus 3D sobre el marcador detectado. |
| Ciclo principal | Captura, detección, renderizado y actualización de ventana en tiempo real. |

---

## 8. Desarrollo de la práctica

### 8.1 Inicialización de la cámara

El programa inicia abriendo la cámara configurada en la constante `CAMERA_INDEX`:

```python
CAMERA_INDEX = 0
cap = cv2.VideoCapture(CAMERA_INDEX)
```

El valor `0` indica que se usará la cámara principal del equipo. Si el programa no puede abrir la cámara o no puede leer un frame inicial, se muestra un mensaje de error y se detiene la ejecución.

---

### 8.2 Configuración del marcador ArUco

El marcador se define mediante tres constantes principales:

```python
MARKER_LENGTH_M = 0.10
ARUCO_DICT = cv2.aruco.DICT_4X4_50
MARKER_ID = 1
```

Donde:

| Constante | Significado |
|---|---|
| `MARKER_LENGTH_M` | Tamaño físico del lado del marcador, en metros. En este caso es de 0.10 m. |
| `ARUCO_DICT` | Diccionario ArUco utilizado para interpretar el patrón del marcador. |
| `MARKER_ID` | Identificador específico del marcador que debe detectarse. |

El tamaño físico del marcador es importante porque permite que la estimación de pose tenga una escala real aproximada.

---

### 8.3 Calibración de cámara

El programa intenta cargar una calibración desde el archivo:

```python
camera_ar.npz
```

La función encargada es:

```python
def load_calibration(width: int, height: int):
    if CALIB_NPZ.is_file():
        data = np.load(CALIB_NPZ)
        return data["camera_matrix"], data["dist_coeffs"]
    return default_camera_matrix(width, height), np.zeros((5, 1), dtype=np.float64)
```

Si el archivo existe, se usan los parámetros reales de calibración. Si no existe, se genera una matriz aproximada mediante `default_camera_matrix()`. Esta solución permite ejecutar la práctica aunque no se haya realizado una calibración formal, aunque la precisión puede ser menor.

---

### 8.4 Creación del detector ArUco

El detector se crea con la función:

```python
def make_aruco_detector():
    dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
    params = cv2.aruco.DetectorParameters()
    if hasattr(cv2.aruco, "ArucoDetector"):
        return cv2.aruco.ArucoDetector(dictionary, params), dictionary
    return None, dictionary
```

Esta función usa el diccionario configurado y crea los parámetros de detección. Además, verifica si la versión instalada de OpenCV cuenta con la clase `ArucoDetector`. Si no está disponible, el programa puede utilizar la función clásica `cv2.aruco.detectMarkers()`.

---

### 8.5 Detección del marcador

Cada frame capturado por la cámara se convierte primero a escala de grises:

```python
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```

Después se busca el marcador:

```python
corners, _, _ = detect_marker(gray, detector, dictionary)
```

La función `detect_marker()` revisa si existen marcadores detectados y, posteriormente, filtra el resultado para conservar únicamente el marcador con el identificador establecido en `MARKER_ID`.

```python
if MARKER_ID is not None:
    matches = np.where(ids.flatten() == MARKER_ID)[0]
    if len(matches) == 0:
        return None, None, None
```

Esto evita que el programa proyecte el modelo sobre un marcador incorrecto.

---

### 8.6 Representación visual de la detección

Cuando el marcador se detecta correctamente, se dibuja un contorno verde sobre el frame y se escribe el texto `ArUco detectado`:

```python
pts = corners.astype(np.int32).reshape(-1, 1, 2)
cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
cv2.putText(frame, "ArUco detectado", (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
```

Esto sirve como retroalimentación visual para comprobar que el marcador está siendo reconocido antes de dibujar el modelo 3D.

---

### 8.7 Puntos 3D del marcador

Para estimar la pose del marcador, el código define las coordenadas 3D de sus cuatro esquinas:

```python
def marker_object_points(side_length):
    s = side_length / 2.0
    return np.array([[-s, s, 0], [s, s, 0], [s, -s, 0], [-s, -s, 0]], dtype=np.float32)
```

Estas coordenadas describen un cuadrado centrado en el origen, ubicado sobre el plano `z = 0`. Al conocer la posición real de las esquinas, OpenCV puede comparar estos puntos 3D con los puntos 2D detectados en la imagen.

---

### 8.8 Estimación de pose

La pose se calcula mediante la función `estimate_pose()`:

```python
def estimate_pose(corners, camera_matrix, dist_coeffs):
    image_points = corners[0] if corners.ndim == 3 else corners
    image_points = np.asarray(image_points, dtype=np.float32).reshape(-1, 2)
    obj_pts = marker_object_points(MARKER_LENGTH_M)
    flags = cv2.SOLVEPNP_IPPE_SQUARE if hasattr(cv2, "SOLVEPNP_IPPE_SQUARE") else cv2.SOLVEPNP_ITERATIVE
    ok, rvec, tvec = cv2.solvePnP(obj_pts, image_points, camera_matrix, dist_coeffs, flags=flags)
    if not ok:
        return None, None
    return rvec, tvec
```

En este bloque se calcula cómo está orientado y ubicado el marcador en el espacio real. El algoritmo `SOLVEPNP_IPPE_SQUARE` es adecuado para marcadores planos cuadrados, por lo que mejora la estimación cuando está disponible.

---

### 8.9 Conversión de matriz de cámara a proyección OpenGL

Para que el modelo 3D se alinee con la imagen real, la cámara virtual de OpenGL debe comportarse de manera semejante a la cámara física. Esto se logra con la función:

```python
def projection_from_k(K, width, height, znear, zfar):
    fx, fy = K[0, 0], K[1, 1]
    cx, cy = K[0, 2], K[1, 2]
    P = np.zeros((4, 4), dtype=np.float32)
    P[0, 0] = 2.0 * fx / width
    P[1, 1] = 2.0 * fy / height
    P[0, 2] = (width - 2.0 * cx) / width
    P[1, 2] = (2.0 * cy - height) / height
    P[2, 2] = -(zfar + znear) / (zfar - znear)
    P[2, 3] = -1.0
    P[3, 2] = -2.0 * zfar * znear / (zfar - znear)
    return P
```

Esta función toma la matriz intrínseca `K` de OpenCV y la transforma en una matriz `P` compatible con OpenGL. Después, dicha matriz se carga en el modo de proyección:

```python
glMatrixMode(GL_PROJECTION)
glLoadMatrixf(P)
```

---

### 8.10 Conversión de pose OpenCV a matriz modelo-vista OpenGL

OpenCV y OpenGL utilizan sistemas de coordenadas diferentes. Por esta razón, la pose calculada por OpenCV debe convertirse antes de dibujar el modelo.

```python
def modelview_from_pose(rvec, tvec) -> np.ndarray:
    R, _ = cv2.Rodrigues(rvec)
    M = np.eye(4, dtype=np.float64)
    M[:3, :3] = R
    M[:3, 3] = tvec.flatten()
    cv_to_gl = np.diag([1.0, -1.0, -1.0, 1.0])
    return (cv_to_gl @ M).T.astype(np.float32)
```

Primero se convierte el vector de rotación `rvec` a una matriz de rotación `R` usando `cv2.Rodrigues()`. Después se construye una matriz de transformación 4x4 y se aplica una conversión de ejes para adaptarla al sistema de OpenGL.

---

### 8.11 Dibujo del frame de la cámara como fondo

La realidad aumentada necesita que la imagen real se muestre como fondo. Para lograrlo, cada frame capturado por OpenCV se convierte en una textura de OpenGL:

```python
def upload_frame_texture(frame_bgr, width, height) -> None:
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    rgb = cv2.flip(rgb, 0)
    glBindTexture(GL_TEXTURE_2D, _tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, _tex_buf)
```

Posteriormente, la textura se dibuja sobre un rectángulo 2D que cubre toda la ventana:

```python
glBegin(GL_QUADS)
glTexCoord2f(0, 0)
glVertex2f(0, 0)
glTexCoord2f(1, 0)
glVertex2f(width, 0)
glTexCoord2f(1, 1)
glVertex2f(width, height)
glTexCoord2f(0, 1)
glVertex2f(0, height)
glEnd()
```

Así, el usuario ve en la ventana la imagen real capturada por la cámara y, sobre ella, el modelo 3D.

---

### 8.12 Proyección del campus 3D sobre el marcador

La función más importante de la práctica es:

```python
def draw_itm_map_on_marker(rvec, tvec, camera_matrix, width, height) -> None:
    P = projection_from_k(camera_matrix, width, height, ZNear, ZFar)
    MV = modelview_from_pose(rvec, tvec)

    glMatrixMode(GL_PROJECTION)
    glLoadMatrixf(P)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glMultMatrixf(MV)

    glDisable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glScalef(MAP_SCALE, MAP_SCALE, MAP_SCALE)
    glRotatef(90.0, 1.0, 0.0, 0.0)
    itm.draw_campus_base()
    itm.draw_sports_fields()
    itm.draw_campus_fences()
    itm.draw_buildings()
    itm.draw_trees()
    glPopMatrix()
```

Esta función realiza el proceso completo de proyección:

1. Calcula la matriz de proyección de OpenGL.
2. Calcula la matriz modelo-vista a partir de la pose del marcador.
3. Carga ambas matrices en OpenGL.
4. Activa la prueba de profundidad.
5. Escala y rota el modelo para ajustarlo al plano del marcador.
6. Llama a las funciones del Proyecto 2 para dibujar el campus.

El modelo se escala con:

```python
MAP_SCALE = 0.006
```

Y se rota con:

```python
glRotatef(90.0, 1.0, 0.0, 0.0)
```

La escala reduce el tamaño del campus para que pueda visualizarse sobre el marcador. La rotación acomoda el plano del campus para que coincida con el plano físico del ArUco.

---

## 9. Relación con el Proyecto 2

El Proyecto 2 consistió en crear una ciudad/campus 3D inspirada en el Instituto Tecnológico de Morelia. Ese modelo fue construido con primitivas de OpenGL, incluyendo edificios, áreas verdes, caminos, canchas, bardas y árboles.

En la Práctica 3, ese mismo modelo se reutiliza mediante la importación:

```python
import itm
```

Después, el código llama directamente a las funciones de dibujo del campus:

```python
itm.draw_campus_base()
itm.draw_sports_fields()
itm.draw_campus_fences()
itm.draw_buildings()
itm.draw_trees()
```

Esto demuestra una ventaja importante de organizar el código por funciones: el modelo 3D creado en una práctica anterior puede reutilizarse en un nuevo contexto, ahora como un objeto virtual dentro de una escena de realidad aumentada.

---

## 10. Ciclo principal del programa

El ciclo principal se ejecuta mientras la ventana permanezca abierta:

```python
while not glfw.window_should_close(window):
    ret, frame = cap.read()
    if not ret:
        continue

    h, w = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, _, _ = detect_marker(gray, detector, dictionary)

    glViewport(0, 0, w, h)
    upload_frame_texture(frame, w, h)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_background_quad(w, h)

    if corners is not None:
        rvec, tvec = estimate_pose(corners, camera_matrix, dist_coeffs)
        if rvec is not None:
            draw_itm_map_on_marker(rvec, tvec, camera_matrix, w, h)

    glfw.swap_buffers(window)
    glfw.poll_events()
```

El flujo del programa es el siguiente:

1. Captura un frame de la cámara.
2. Convierte el frame a escala de grises.
3. Detecta el marcador ArUco.
4. Dibuja el frame como fondo.
5. Si el marcador fue detectado, calcula su pose.
6. Si la pose es válida, dibuja el campus 3D sobre el marcador.
7. Actualiza la ventana.
8. Procesa eventos de teclado y ventana.

---

## 11. Funcionamiento esperado

Al ejecutar el programa, debe abrirse una ventana con el título:

```text
RA: marcador ArUco + mapa ITM (ESC=salir)
```

El funcionamiento esperado es el siguiente:

| Acción | Resultado esperado |
|---|---|
| Abrir el programa | Se activa la cámara y se muestra la imagen en una ventana OpenGL. |
| Mostrar el marcador ArUco ID 1 | El programa detecta el marcador y dibuja un contorno verde. |
| Mantener el marcador visible | El campus 3D aparece proyectado sobre el marcador. |
| Mover o girar el marcador | El modelo 3D cambia su posición y orientación en tiempo real. |
| Ocultar el marcador | El modelo deja de mostrarse porque no hay referencia espacial. |
| Presionar `ESC` o `Q` | La ventana se cierra y se liberan los recursos. |

---

## 12. Resultados

Con la implementación realizada, se logró proyectar el modelo 3D del campus ITM sobre un marcador ArUco en tiempo real. El programa utiliza la imagen de la cámara como fondo y superpone el modelo cuando detecta correctamente el marcador.

Los resultados principales fueron:

- Se integró la captura de cámara con OpenCV dentro de una ventana OpenGL.
- Se detectó el marcador ArUco ID 1 mediante el diccionario `DICT_4X4_50`.
- Se calculó la pose del marcador con base en sus esquinas detectadas.
- Se transformó la matriz de cámara al sistema de proyección de OpenGL.
- Se convirtió la pose de OpenCV a una matriz modelo-vista compatible con OpenGL.
- Se reutilizó el modelo 3D del Proyecto 2 para proyectarlo en un espacio real.
- Se obtuvo una representación visual de realidad aumentada donde el campus queda anclado al marcador.

---

## 13. Análisis de resultados

El resultado obtenido muestra que la realidad aumentada depende de tres factores principales: detección correcta del marcador, estimación precisa de la pose y correspondencia adecuada entre los sistemas de coordenadas de OpenCV y OpenGL.

La detección del marcador permite establecer una referencia espacial dentro de la imagen real. Sin esta referencia, OpenGL no sabría dónde colocar el modelo. Por eso, cuando el marcador desaparece de la cámara, el campus también deja de renderizarse.

La estimación de pose permite que el modelo no solo aparezca sobre el marcador, sino que también respete su inclinación, distancia y rotación. Esto genera la sensación de que el objeto virtual está realmente apoyado sobre el marcador.

La conversión entre OpenCV y OpenGL es una de las partes más importantes del proyecto. OpenCV trabaja con un sistema de coordenadas orientado a visión por computadora, mientras que OpenGL utiliza otro sistema para renderizado 3D. Si esta conversión no se realiza correctamente, el modelo puede aparecer invertido, mal orientado o separado del marcador.

También se observó que la escala del modelo es fundamental. Debido a que el campus del Proyecto 2 fue diseñado como una escena amplia, fue necesario reducirlo mediante `MAP_SCALE = 0.006` para que pudiera visualizarse de manera adecuada sobre un marcador físico de 10 cm.

---

## 14. Problemas posibles y soluciones

| Problema | Causa probable | Solución recomendada |
|---|---|---|
| No se abre la cámara | Índice incorrecto o cámara ocupada por otra aplicación. | Cambiar `CAMERA_INDEX` a 1 o cerrar otras aplicaciones que usen la cámara. |
| No se detecta el marcador | El ID del marcador no coincide con `MARKER_ID`. | Usar el marcador ID 1 o modificar la constante en el código. |
| El modelo aparece inestable | Mala iluminación o movimiento excesivo del marcador. | Usar buena iluminación y mantener el marcador firme. |
| El modelo aparece muy grande o pequeño | Escala inadecuada del mapa. | Ajustar `MAP_SCALE`. |
| El modelo aparece rotado incorrectamente | Diferencia de ejes entre OpenCV y OpenGL. | Revisar `glRotatef()` y la matriz `cv_to_gl`. |
| Error con `cv2.aruco` | Instalación incompleta de OpenCV. | Instalar `opencv-contrib-python`. |
| Error al importar `itm` | Falta el archivo del Proyecto 2. | Colocar `itm.py` en la misma carpeta que `realidad_aumentada_mapa.py`. |

---

## 15. Requisitos de ejecución

Para ejecutar la práctica se recomienda instalar las dependencias con:

```bash
pip install glfw PyOpenGL numpy opencv-contrib-python
```

La carpeta del proyecto debe contener al menos:

```text
realidad_aumentada_mapa.py
itm.py
marcador_aruco_id1.png
```

Opcionalmente, puede incluirse:

```text
camera_ar.npz
```

Ejecución del programa:

```bash
python realidad_aumentada_mapa.py
```

---

## 16. Conclusión

La Práctica 3 nos permitió aplicar los conceptos de graficación tridimensional en un contexto de realidad aumentada. A diferencia del Proyecto 2, donde el campus se visualizaba únicamente en un entorno virtual, en esta práctica el modelo se proyecta sobre una imagen real capturada por la cámara.

El uso del marcador ArUco nos permitió establecer una referencia física para ubicar el modelo 3D. A partir de la detección de sus esquinas, OpenCV calculó la pose del marcador y esa información fue convertida para ser utilizada por OpenGL. De esta manera, el programa pudo renderizar el campus ITM sobre el plano del marcador, manteniendo su orientación y escala de forma dinámica.

Esta práctica demuestra la importancia de las matrices de transformación, la proyección en perspectiva y la relación entre visión por computadora y graficación 3D. Además, evidencia que un modelo desarrollado previamente con primitivas de OpenGL puede reutilizarse en aplicaciones más avanzadas, como la realidad aumentada.

En conclusión, el proyecto cumple con el propósito de proyectar modelos tridimensionales virtuales en espacios reales, integrando captura de cámara, detección de marcadores, estimación de pose, matrices de proyección y renderizado 3D en tiempo real.

---

## 17. Posibles mejoras

Algunas mejoras que podrían agregarse en versiones posteriores son:

- Calibrar formalmente la cámara para mejorar la alineación del modelo.
- Agregar iluminación y sombras al modelo 3D para aumentar el realismo.
- Permitir seleccionar diferentes marcadores para proyectar distintos modelos.
- Incluir una interfaz gráfica para modificar escala, rotación y posición del modelo.
- Usar modelos 3D externos en formatos como `.obj` o `.fbx`.
- Incorporar oclusión para que objetos reales puedan tapar parcialmente el modelo virtual.
- Agregar texturas al campus para mejorar la apariencia visual.
- Optimizar el renderizado para obtener mayor estabilidad en tiempo real.

---

## 18. Referencias

- Apuntes de la materia de Graficación: `https://ealcaraz85.github.io/Graficacion.io/`
- Código base de la Práctica 3: `realidad_aumentada_mapa.py`.
- Modelo 3D del Proyecto 2: `itm.py` / Campus ITM 3D.
- OpenGL / PyOpenGL.
- GLFW.
- GLU.
- OpenCV.
