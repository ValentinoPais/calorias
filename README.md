# Calorías

App web de un solo archivo para contar calorías y macros. Sin servidor ni cuenta: los datos quedan en el navegador del celular.

## Archivos

- `index.html`: la app completa (HTML, CSS y JS adentro).
- `foods.js`: base de 391 alimentos y bebidas con kcal, proteína, carbos y grasa por 100 g (o 100 ml) y sus porciones típicas.
- `manifest.json` e `icon-*.png`: para agregarla al inicio del celular con ícono propio.
- `fuente/foods.txt`: la base en formato simple, una línea por alimento. `fuente/build_foods.py` la convierte a `foods.js`.

## Publicar en GitHub Pages

1. Creá un repo (por ejemplo `calorias`) y subí todos los archivos a la raíz.
2. Settings → Pages → Source: "Deploy from a branch" → Branch: `main`, carpeta `/ (root)` → Save.
3. En un minuto queda en `https://TU-USUARIO.github.io/calorias/`.
4. En el celular: abrí esa URL en Safari o Chrome → Compartir → "Agregar a inicio". Abre a pantalla completa, como una app.

Para probarla en la compu alcanza con abrir `index.html` con doble clic.

## Editar la base de alimentos

Cada línea de `fuente/foods.txt` es: `nombre|unidad|kcal|prot|carb|grasa|porciones|alias`

```
Arroz blanco cocido|g|130|2.7|28|0.3|media taza=80;1 taza=160;1 plato=250
Coca-Cola|ml|42|0|10.6|0|vaso=250;lata=354;botella 500 ml=500|coca,gaseosa
```

Los valores son por 100 g o 100 ml. Las porciones van como `etiqueta=gramos` separadas por `;`. Después de editar:

```
python3 fuente/build_foods.py fuente/foods.txt foods.js
```

También se puede editar `foods.js` directo. Lo que cargás a mano desde la app se guarda como "alimento propio" en el navegador, no en este archivo.

## Datos y cálculo

- Todo vive en `localStorage` bajo la clave `calorias.v1`. Exportar baja un `.json` con todo; Importar lo reemplaza. Es el único backup.
- Objetivo diario: Mifflin-St Jeor × actividad (1,2 / 1,375 / 1,55) menos el déficit de la meta (1 kg ≈ 7.700 kcal), nunca por debajo de 1.500 kcal (hombre) o 1.200 (mujer).
- Valores nutricionales aproximados, compilados de tablas estándar (USDA SR Legacy, SARA 2). La app es un estimativo, no una indicación médica.
