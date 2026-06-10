import os
import random
import argparse


PALABRAS = [
    "peru", "elecciones", "votos", "mesa", "acta", "partido",
    "candidato", "region", "provincia", "distrito", "resultado",
    "conteo", "onpe", "jurado", "nacional", "presidente",
    "congreso", "democracia", "ciudadano", "urna",
    "computacion", "algoritmo", "hadoop", "mapreduce",
    "indice", "invertido", "documento", "archivo", "palabra",
    "frecuencia", "busqueda", "texto", "datos", "cluster"
]

PALABRAS_COMUNES = [
    "el", "la", "los", "las", "de", "del", "en", "y", "a",
    "un", "una", "por", "para", "con", "que", "se"
]


def generar_texto(num_palabras: int, prob_palabra_comun: float = 0.25) -> str:
    palabras = []

    for i in range(num_palabras):
        if random.random() < prob_palabra_comun:
            palabra = random.choice(PALABRAS_COMUNES)
        else:
            palabra = random.choice(PALABRAS)

        palabras.append(palabra)
        
        if (i + 1) % 100 == 0:
            palabras.append("\n")

    return " ".join(palabras)


def generar_archivos(
    carpeta_salida: str,
    num_archivos: int,
    min_palabras: int,
    max_palabras: int
):
    os.makedirs(carpeta_salida, exist_ok=True)

    for i in range(1, num_archivos + 1):
        nombre_archivo = f"doc_{i:03}.txt"
        ruta_archivo = os.path.join(carpeta_salida, nombre_archivo)

        cantidad_palabras = random.randint(min_palabras, max_palabras)
        contenido = generar_texto(cantidad_palabras)

        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(contenido)

        print(f"Generado: {ruta_archivo} ({cantidad_palabras} palabras)")


def main():
    parser = argparse.ArgumentParser(
        description="Generador de documentos de prueba para índice invertido"
    )

    parser.add_argument(
        "--salida",
        default="data",
        help="Carpeta donde se guardarán los documentos"
    )

    parser.add_argument(
        "--archivos",
        type=int,
        default=10,
        help="Cantidad de archivos a generar"
    )

    parser.add_argument(
        "--min",
        type=int,
        default=50,
        help="Cantidad mínima de palabras por archivo"
    )

    parser.add_argument(
        "--max",
        type=int,
        default=150,
        help="Cantidad máxima de palabras por archivo"
    )

    args = parser.parse_args()

    generar_archivos(
        carpeta_salida=args.salida,
        num_archivos=args.archivos,
        min_palabras=args.min,
        max_palabras=args.max
    )


if __name__ == "__main__":
    main()