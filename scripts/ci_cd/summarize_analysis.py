import json
import sys


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "reports/analysis_result.json"

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No se encontro el resultado JSON del analisis.")
        return

    results = [item for item in data.get("results", []) if item.get("analyzed")]
    vulnerable = [item for item in results if item.get("is_vulnerable")]

    if not results:
        print("No se analizaron archivos de codigo en este PR.")
        return

    if vulnerable:
        details = []
        for item in vulnerable:
            probability = item.get("probability_vulnerable", 0.0) * 100
            details.append(f"{item.get('file')}: {probability:.2f}% vulnerable")
        print("Codigo vulnerable detectado. " + " | ".join(details))
        return

    max_item = max(results, key=lambda item: item.get("probability_vulnerable", 0.0))
    probability = max_item.get("probability_vulnerable", 0.0) * 100
    print(
        "Codigo seguro. "
        f"Archivos analizados: {len(results)}. "
        f"Mayor probabilidad de vulnerabilidad: {probability:.2f}% en {max_item.get('file')}."
    )


if __name__ == "__main__":
    main()
