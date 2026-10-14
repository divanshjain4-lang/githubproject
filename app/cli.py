import argparse

from app.core.config import SAMPLE_DATA_PATH
from app.services.model_service import train_model


def main() -> None:
    parser = argparse.ArgumentParser(description="Bank Muscat customer segmentation utility")
    parser.add_argument("command", choices=["train-sample", "train"])
    parser.add_argument("--data", help="Path to an approved training CSV")
    args = parser.parse_args()
    if args.command == "train" and not args.data:
        parser.error("train requires --data; use train-sample for the synthetic demonstration")

    dataset = args.data if args.command == "train" and args.data else str(SAMPLE_DATA_PATH)
    result = train_model(dataset)
    print(f"Model trained: {result['training_rows']} rows, validation accuracy {result['accuracy']}")


if __name__ == "__main__":
    main()
