import argparse
import json
from .core import search_artwork


def main() -> None:
    parser = argparse.ArgumentParser(description="Search iTunes artwork")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--entity", default="tvSeason", help="iTunes entity")
    parser.add_argument("--country", default="us", help="Country code")
    parser.add_argument("--limit", type=int, default=25, help="Number of results")
    args = parser.parse_args()

    results = search_artwork(args.query, entity=args.entity, country=args.country, limit=args.limit)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
