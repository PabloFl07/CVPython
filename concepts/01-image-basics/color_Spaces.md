# Espacios de color

## Definición de espacio de color

- **Modelo de color**: modelo matemático abstracto que permite representar los colores en forma numérica, utilizando típicamente tres o cuatro valores o componentes cromáticos

- **Espacio de color**: sistema matemático que organiza y define un rango específico de colores para que los dispositivos puedan interpretarlos y reproducirlos de forma uniforme

La visión humana es **tricromática**: la retina tiene tres tipos de conos (S, M, L), sensibles a longitudes de onda cortas, medias y largas (~420, ~530 y ~560 nm). Cualquier espectro de luz, por complejo que sea, se reduce a tres respuestas. Dos espectros distintos que producen la misma respuesta en los conos se ven iguales (**metamerismo**). Por eso tres coordenadas bastan para describir el color percibido.

### Conceptos clave

- **CIE 1931 XYZ**: espacio de referencia estándar, derivado de experimentos psicofísicos de igualación de color. Es independiente del dispositivo y sirve de "puente" entre espacios: la mayoría de conversiones rigurosas pasan por XYZ. La componente $`Y`$ es la luminancia.

- **Gamut (gama)**: subconjunto de colores que un espacio o dispositivo puede representar. Ningún dispositivo RGB con tres primarios reales cubre todos los colores visibles.

- **Punto blanco**: color que se considera "blanco" de referencia (p. ej. **D65**, luz diurna media, ~6500 K).

- **Dependiente vs. independiente del dispositivo**: RGB, HSV, HSL y YCbCr dependen de los primarios del dispositivo o del estándar RGB del que derivan; XYZ y CIELAB son independientes.

- **Uniformidad perceptual**: un espacio es perceptualmente uniforme si distancias iguales en el espacio corresponden a diferencias de color percibidas iguales. RGB no lo es; CIELAB lo aproxima.

- **Separación luminancia/crominancia**: muchos espacios (HSV, HSL, YCbCr, Lab) separan la información de *intensidad* de la de *color*, lo que facilita tareas robustas a cambios de iluminación y permite comprimir aprovechando la menor sensibilidad del ojo al detalle cromático.

- **Lineal vs. codificado con gamma**: los valores almacenados en una imagen (p. ej. sRGB) no son proporcionales a la energía luminosa, sino que están comprimidos con una curva no lineal (gamma). Se suele denotar con prima ($`R'`$, $`G'`$, $`B'`$, $`Y'`$) a los valores codificados.

## Escala de grises

Una imagen en escala de grises tiene **un único canal** que representa la intensidad (brillo) de cada píxel, sin información cromática. Cada valor va del negro (mínimo) al blanco (máximo), pasando por todos los tonos de gris.

Se obtiene a partir de RGB como una **combinación lineal ponderada** de los canales, no como una media simple. Los pesos reflejan la sensibilidad del ojo, que es máxima en el verde (~555 nm) y mínima en el azul:

- **Rec. BT.601** (vídeo SD, JPEG; la usada por OpenCV):

```math
Y' = 0.299\,R' + 0.587\,G' + 0.114\,B'
```

- **Rec. BT.709 / sRGB** (HD):

```math
Y = 0.2126\,R + 0.7152\,G + 0.0722\,B
```

La **luminancia** $`Y`$ es una magnitud fotométrica: se calcula sobre valores RGB **lineales** y es la componente $`Y`$ de CIE XYZ.

La **luma** $`Y'`$ se calcula sobre valores **codificados con gamma**. Es una aproximación más barata y es lo que realmente calculan la mayoría de librerías.

Un píxel es gris neutro en RGB cuando $`R = G = B`$: la escala de grises corresponde a la diagonal principal del cubo RGB.

> Ocupa un tercio de la memoria de una imagen RGB equivalente, por eso es indicada cuando el color no es relevante.

## RGB

RGB es un modelo **aditivo**: cada color se forma sumando distintas cantidades de luz de tres primarios, **rojo (R)**, **verde (G)** y **azul (B)**. Con los tres a cero se obtiene negro; con los tres al máximo, blanco.

Los colores representables forman un **cubo** con vértices en negro $`(0,0,0)`$, blanco $`(1,1,1)`$, los tres primarios (R, G, B) y los tres secundarios (cian, magenta, amarillo). La diagonal negro–blanco es el eje de grises.

RGB es un modelo, **sRGB** es un espacio. El estándar más común, **sRGB** (IEC 61966-2-1, 1999), fija:

- Primarios de Rec. BT.709.

- Punto blanco D65.

- Una **función de transferencia** no lineal (gamma ≈ 2.2) para pasar de un valor codificado $`C' \in [0,1]`$ a lineal:

```math
C_{\text{lin}} = \begin{cases} \dfrac{C'}{12.92} & C' \le 0.04045 \\ \left(\dfrac{C' + 0.055}{1.055}\right)^{2.4} & C' > 0.04045 \end{cases}
```

> [!IMPORTANT]
> Convierte entre los valores **codificados** $`C'`$ guardados en el archivo y los valores **lineales** ($`C_{\text{lin}}`$, proporcionales a la luz física) *dentro del mismo espacio sRGB*.

Esto se realiza con el objetivo de realizar operaciones con sentido físico para posteriormente volver a codificarlas.

#### Limitaciones para visión por computador:

- Los tres canales están fuertemente correlacionados, de modo que un cambio de **iluminación** modifica los tres a la vez.

- **No es perceptualmente uniforme**: la distancia euclídea entre dos tripletes RGB no refleja la diferencia de color percibida.

### Estructura digital

- Tensor $`H \times W \times 3`$.

- **Profundidad de color**: con 8 bits por canal (24 bits por píxel) se representan $`2^{24} = 16\,777\,216`$ colores ("color verdadero"). Formatos HDR y profesionales usan 10, 12 o 16 bits por canal, o `float16`/`float32`.

- **Rangos**: `uint8` en $`[0, 255]`$; `float32` normalizado en $`[0, 1]`$.

## HSV

HSV (**Hue, Saturation, Value**; tono, saturación, valor) es una reorganización **cilíndrica** del cubo RGB (Alvy Ray Smith, 1978) pensada para ser más intuitiva: describe el color como lo haría una persona, separando *qué color es* (tono), *cuán puro es* (saturación) y *cuán claro es* (valor).

- **H (tono)**: ángulo en el círculo cromático, $`[0°, 360°)`$. 0° rojo, 60° amarillo, 120° verde, 180° cian, 240° azul, 300° magenta.

- **S (saturación)**: pureza del color, $`[0, 1]`$. 0 = gris, 1 = color puro.

- **V (valor)**: brillo, $`[0, 1]`$. 0 = negro.

**Conversión desde RGB** (con $`R, G, B \in [0,1]`$). Sea $`M = \max(R,G,B)`$, $`m = \min(R,G,B)`$ y el croma $`C = M - m`$:

```math
V = M \qquad S = \begin{cases} 0 & V = 0 \\ C / V & V > 0 \end{cases}
```

```math
H = 60° \times \begin{cases} \text{indefinido (se usa 0)} & C = 0 \\ \left(\dfrac{G - B}{C}\right) \bmod 6 & M = R \\ \dfrac{B - R}{C} + 2 & M = G \\ \dfrac{R - G}{C} + 4 & M = B \end{cases}
```

> [!IMPORTANT]
> **El tono es una variable circular**: 359° y 1° son casi el mismo rojo. La distancia entre tonos debe calcularse como $`d = \min(|h_1 - h_2|,\ 360° - |h_1 - h_2|)`$, y un rango que incluya el rojo debe partirse en dos intervalos.

Cuando $`S`$ o $`V`$ son bajos (grises, zonas oscuras), $`C \approx 0`$ y el tono está mal definido: pequeñas variaciones por ruido producen saltos enormes de H. Por eso se suele descartar H en píxeles de baja saturación o bajo brillo.

#### Limitaciones para visión por computador:

- Es una transformación **no lineal** de RGB y hereda su dependencia del dispositivo.

- **No es perceptualmente uniforme**.

- **V no es luminancia**: un azul puro $`(0,0,1)`$ y el blanco $`(1,1,1)`$ tienen ambos $`V = 1`$, aunque el azul se perciba mucho más oscuro.

- **Inestabilidad del tono** en píxeles poco saturados u oscuros.

### Estructura digital

- Tensor $`H \times W \times 3`$ con canales en orden H, S, V.

- **Rangos**: las convenciones **dependen de la librería**, lo que es una fuente habitual de errores:
  - Convención matemática / `float`: $`H \in [0, 360)`$, $`S, V \in [0, 1]`$.
  - OpenCV con `uint8`: $`H \in [0, 179]`$ (el ángulo se divide entre 2 para caber en 8 bits), $`S, V \in [0, 255]`$. Existe una variante `FULL` que escala H a $`[0, 255]`$.
  - scikit-image: los tres canales en $`[0, 1]`$.

## HSL

HSL (**Hue, Saturation, Lightness**; tono, saturación, luminosidad), también llamado **HLS**, es otra representación cilíndrica de RGB, hermana de HSV. La diferencia está en el tercer eje: la **luminosidad** trata al negro y al blanco de forma simétrica, de modo que los colores puros quedan a media altura.

- **H (tono)**: idéntico al de HSV.

- **S (saturación)**: $`[0, 1]`$, pero con una definición distinta a la de HSV.

- **L (luminosidad)**: $`[0, 1]`$. 0 = negro, 1 = blanco, 0.5 = colores puros.

**Conversión desde RGB** (mismas $`M`$, $`m`$, $`C`$ que en HSV):

```math
L = \frac{M + m}{2} \qquad S = \begin{cases} 0 & L = 0 \text{ o } L = 1 \\ \dfrac{C}{1 - |2L - 1|} & \text{en otro caso} \end{cases}
```

Geométricamente es un **doble cono** (bicono): el vértice inferior es negro, el superior blanco y el ecuador ($`L = 0.5`$) contiene los colores más saturados.

| | HSV | HSL |
|---|---|---|
| Tercer eje | $`V = \max(R,G,B)`$ | $`L = (\max + \min)/2`$ |
| Colores puros | $`V = 1`$ | $`L = 0.5`$ |
| Blanco | $`V = 1`$, $`S = 0`$ | $`L = 1`$ |
| Forma | Cono hexagonal | Doble cono |
| "Aclarar" un color | Reducir S | Aumentar L |

**Conversión HSV → HSL**:

```math
L = V\left(1 - \frac{S_V}{2}\right) \qquad S_L = \frac{V - L}{\min(L,\ 1 - L)}
```

con $`S_L = 0`$ si $`L \in \{0, 1\}`$.

#### Limitaciones para visión por computador:

- Las mismas que HSV: no es perceptualmente uniforme, el tono es inestable con baja saturación y depende del dispositivo.

- **L tampoco es luminancia perceptual**: el amarillo y el azul puros tienen ambos $`L = 0.5`$.

### Estructura digital

- Tensor $`H \times W \times 3`$.

- **Orden de canales**: en OpenCV la conversión se llama HLS y el orden es **H, L, S**, no H, S, L.

- **Rangos** en OpenCV con `uint8`: $`H \in [0, 179]`$, $`L, S \in [0, 255]`$.

## YCbCr

YCbCr separa la imagen en un canal de **luma** ($`Y'`$, el "blanco y negro") y dos canales de **crominancia**: $`C_b`$ (diferencia respecto al azul) y $`C_r`$ (diferencia respecto al rojo). Nace de la televisión, donde permitía que los televisores en blanco y negro siguieran funcionando con la señal en color (sus antecesores analógicos son YUV y YIQ).

El ojo humano es mucho más sensible al detalle espacial en la luminancia que en el color (hay muchos más bastones y conos L/M que conos S, y el sistema visual procesa el color a menor resolución). Separar $`Y'`$ de la crominancia permite **reducir la resolución del color sin pérdida visible**.

**Forma general**: dados los coeficientes $`K_R`$ y $`K_B`$ del estándar ($`K_G = 1 - K_R - K_B`$):

```math
Y' = K_R R' + K_G G' + K_B B' \qquad C_b = \frac{1}{2}\,\frac{B' - Y'}{1 - K_B} \qquad C_r = \frac{1}{2}\,\frac{R' - Y'}{1 - K_R}
```

- **BT.601** (SD, JPEG): $`K_R = 0.299`$, $`K_B = 0.114`$.

- **BT.709** (HD): $`K_R = 0.2126`$, $`K_B = 0.0722`$.

- **BT.2020** (UHD): $`K_R = 0.2627`$, $`K_B = 0.0593`$.

**Versión JPEG (JFIF)**, rango completo con 8 bits:

```math
\begin{aligned}
Y' &= 0.299\,R' + 0.587\,G' + 0.114\,B' \\
C_b &= 128 - 0.168736\,R' - 0.331264\,G' + 0.5\,B' \\
C_r &= 128 + 0.5\,R' - 0.418688\,G' - 0.081312\,B'
\end{aligned}
```

El offset de 128 centra la crominancia: un gris tiene $`C_b = C_r = 128`$.

Es una **transformación afín** (matriz $`3 \times 3`$ más un desplazamiento), por lo que es invertible y barata de calcular. Las pérdidas en la ida y vuelta vienen solo del redondeo a enteros.

> [!IMPORTANT]
> **Rango completo vs. limitado**: en vídeo se usa el rango "de estudio": $`Y' \in [16, 235]`$ y $`C_b, C_r \in [16, 240]`$, reservando los extremos como margen. JPEG usa el rango completo $`[0, 255]`$. Interpretar un rango como el otro produce imágenes lavadas o con negros aplastados.

**Submuestreo de crominancia** (notación $`J{:}a{:}b`$ sobre un bloque de 4 × 2 píxeles):

- **4:4:4**: sin submuestreo, resolución completa en los tres canales.

- **4:2:2**: crominancia a mitad de resolución horizontal (reducción del 33 %).

- **4:2:0**: crominancia a mitad de resolución horizontal y vertical. Por cada 4 muestras de $`Y'`$ hay 1 de $`C_b`$ y 1 de $`C_r`$: 1.5 muestras por píxel frente a 3, es decir, **un 50 % menos de datos** casi sin pérdida perceptible.

> "YUV" se usa a menudo, de forma imprecisa, para referirse a YCbCr digital.

#### Limitaciones para visión por computador:

- **No es un espacio de color independiente**: es una *codificación* de un espacio RGB concreto; su significado depende del RGB y del estándar del que proviene.

- **No es perceptualmente uniforme**.

### Estructura digital

- Sin submuestreo: tensor $`H \times W \times 3`$. En OpenCV el orden es **Y, Cr, Cb** (conversión YCrCb).

- Con submuestreo, los canales tienen tamaños distintos y ya no forman un tensor $`H \times W \times 3`$; se almacenan en **formato planar** o semiplanar (p. ej. I420: plano Y completo seguido de planos U y V de $`\tfrac{H}{2} \times \tfrac{W}{2}`$; NV12: plano Y seguido de un plano con U y V intercalados).

- **Rangos**: `uint8` en $`[0, 255]`$ (completo) o $`[16, 235/240]`$ (limitado).

### Aplicaciones

- **Compresión JPEG**: RGB → YCbCr → submuestreo 4:2:0 de la crominancia → DCT sobre bloques de 8 × 8 → cuantización (más agresiva en crominancia).

- **Códecs de vídeo** (H.264, H.265, AV1) y televisión digital: prácticamente todo el vídeo se transmite en YCbCr 4:2:0.

- **Detección de piel**: los tonos de piel de distintas personas forman un cúmulo compacto en el plano $`C_b`$–$`C_r`$, relativamente independiente de la iluminación ($`Y'`$).

- **Superresolución y restauración**: métodos clásicos (p. ej. SRCNN) procesan solo el canal $`Y'`$ y escalan la crominancia con interpolación simple, y las métricas PSNR/SSIM se calculan a menudo sobre $`Y'`$.

- **Procesado del brillo** (ecualización, nitidez) sobre $`Y'`$ sin alterar los colores.

## Lab

**CIELAB** (CIE 1976 $`L^*a^*b^*`$) es un espacio **independiente del dispositivo** diseñado para ser aproximadamente **perceptualmente uniforme**: la distancia euclídea entre dos colores refleja razonablemente la diferencia que percibe una persona. Sigue la **teoría de los procesos oponentes** (Hering): el sistema visual codifica el color como claro–oscuro, rojo–verde y amarillo–azul.

- **$`L^*`$ (luminosidad)**: $`[0, 100]`$, de negro a blanco difuso.

- **$`a^*`$**: eje verde ($`-`$) ↔ rojo ($`+`$).

- **$`b^*`$**: eje azul ($`-`$) ↔ amarillo ($`+`$).

Los grises cumplen $`a^* = b^* = 0`$. Los ejes $`a^*`$ y $`b^*`$ no tienen límites fijos; en la práctica quedan aproximadamente en $`[-128, 127]`$.

**Conversión desde sRGB** (no lineal, en tres pasos):

1. **Linealizar** los valores sRGB con la función de transferencia inversa (ver sección RGB).

2. **RGB lineal → XYZ** (matriz fija para sRGB con blanco D65):

```math
\begin{pmatrix} X \\ Y \\ Z \end{pmatrix} = \begin{pmatrix} 0.4124 & 0.3576 & 0.1805 \\ 0.2126 & 0.7152 & 0.0722 \\ 0.0193 & 0.1192 & 0.9505 \end{pmatrix} \begin{pmatrix} R \\ G \\ B \end{pmatrix}
```

3. **XYZ → Lab**, relativo al blanco de referencia $`(X_n, Y_n, Z_n)`$ (para D65: $`0.9505,\ 1.0,\ 1.0890`$):

```math
L^* = 116\, f\!\left(\tfrac{Y}{Y_n}\right) - 16 \qquad a^* = 500\left[f\!\left(\tfrac{X}{X_n}\right) - f\!\left(\tfrac{Y}{Y_n}\right)\right] \qquad b^* = 200\left[f\!\left(\tfrac{Y}{Y_n}\right) - f\!\left(\tfrac{Z}{Z_n}\right)\right]
```

```math
f(t) = \begin{cases} t^{1/3} & t > \left(\tfrac{6}{29}\right)^3 \\ \dfrac{t}{3\,(6/29)^2} + \dfrac{4}{29} & \text{en otro caso} \end{cases}
```

La raíz cúbica modela la respuesta no lineal del ojo a la intensidad; el tramo lineal evita la pendiente infinita cerca de cero.

**Diferencia de color** $`\Delta E`$ (CIE76), la distancia euclídea:

```math
\Delta E^*_{ab} = \sqrt{(\Delta L^*)^2 + (\Delta a^*)^2 + (\Delta b^*)^2}
```

Como referencia, $`\Delta E \approx 2.3`$ se considera la diferencia apenas perceptible (JND); por debajo de 1 es imperceptible para la mayoría de observadores.

**Forma cilíndrica LCh**: croma $`C^*_{ab} = \sqrt{a^{*2} + b^{*2}}`$ y tono $`h_{ab} = \operatorname{atan2}(b^*, a^*)`$. Es el equivalente "perceptual" de HSV/HSL.

> [!IMPORTANT]
> **Dependencia del blanco de referencia**: los valores Lab solo son comparables si se calcularon con el mismo punto blanco (D65 en imagen digital, D50 en artes gráficas).

#### Limitaciones para visión por computador:

- **No es perfectamente uniforme** (falla sobre todo en azules y en colores muy saturados). Las fórmulas **CIE94** y **CIEDE2000** ($`\Delta E_{00}`$) corrigen la métrica con pesos dependientes de luminosidad, croma y tono.

- **Gamut**: Lab puede representar todos los colores visibles (e incluso coordenadas que no corresponden a ningún color real). Al volver a sRGB, muchos valores Lab caen **fuera de gamut** y deben recortarse.

- **Coste**: la conversión es más costosa que las de HSV o YCbCr (potencias y raíces cúbicas por píxel).

### Estructura digital

- Tensor $`H \times W \times 3`$ con canales $`L^*, a^*, b^*`$.

- **Rangos** en `float32`: $`L^* \in [0, 100]`$, $`a^*, b^* \approx [-128, 127]`$.

- En `uint8`, OpenCV reescala: $`L \to L^* \cdot 255/100`$, $`a \to a^* + 128`$, $`b \to b^* + 128`$. Esta cuantización pierde precisión, por lo que para medir distancias conviene convertir desde imágenes en coma flotante.

### Aplicaciones

- **Medida de diferencias de color** ($`\Delta E`$): control de calidad industrial (textil, pintura, impresión, alimentación), calibración de pantallas e impresoras.

- **Clustering en espacio de color**: k-means sobre $`(L^*, a^*, b^*)`$ agrupa colores de forma más coherente con la percepción que sobre RGB.

- **Superpíxeles SLIC**: combina distancia en Lab con distancia espacial $`(x, y)`$.

- **Mejora de contraste**: aplicar ecualización o CLAHE solo sobre $`L^*`$ mejora el contraste sin desplazar los tonos, algo que no ocurre al ecualizar R, G y B por separado.

- **Transferencia de color** entre imágenes (igualando medias y desviaciones en un espacio oponente tipo Lab).

- **Colorización automática**: redes que reciben $`L^*`$ y predicen los canales $`a^*`$ y $`b^*`$.

- **Gestión de color**: espacio de conexión (PCS) en los perfiles ICC, junto con XYZ.

## Resumen comparativo

| Espacio | Canales | Tipo de conversión desde RGB | Independiente del dispositivo | Perceptualmente uniforme | Uso típico |
|---|---|---|---|---|---|
| Escala de grises | 1 (intensidad) | Lineal (proyección, irreversible) | No | — | Algoritmos clásicos, reducir datos |
| RGB | 3 (R, G, B) | — | No (sí, si se fija sRGB, etc.) | No | Captura, visualización, deep learning |
| HSV | 3 (tono, saturación, valor) | No lineal | No | No | Segmentación por color |
| HSL | 3 (tono, luminosidad, saturación) | No lineal | No | No | Diseño, detección de blancos |
| YCbCr | 3 (luma, 2 crominancias) | Afín | No | No | Compresión de imagen y vídeo |
| CIELAB | 3 ($`L^*`$, $`a^*`$, $`b^*`$) | No lineal, vía XYZ | Sí | Aproximadamente | Distancias de color, clustering |
| RGB lineal | 3 (R, G, B) | Linealización por canal | Sí, si se fijan primarios y blanco | No | Operaciones físicas: mezcla, desenfoque, balance de blancos |
| rgb normalizado | 2 independientes ($`r`$, $`g`$) | No lineal (división) | No | No | Segmentación invariante a la intensidad |

