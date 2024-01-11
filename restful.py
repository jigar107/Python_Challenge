#!/usr/bin/env python3
import argparse
import requests
import json
import csv

class RestfulClient:
    API_BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self):
        self.parser = self.setup_argparse()

    def setup_argparse(self):
        parser = argparse.ArgumentParser(description="Simple REST client for JSONPlaceholder.")
        parser.add_argument("method", choices=["get", "post"], help="Request method")
        parser.add_argument("endpoint", help="Request endpoint URI fragment")
        parser.add_argument("-d", "--data", help="Data to send with request")
        parser.add_argument("-o", "--output", help="Output to .json or .csv file (default: dump to stdout)")

        return parser

    def execute(self):
        args = self.parser.parse_args()
        method = args.method
        endpoint = args.endpoint
        url = f"{self.API_BASE_URL}{endpoint}"

        if method == "get":
            response = requests.get(url)
        elif method == "post":
            data = json.loads(args.data)
            response = requests.post(url, json=data)

        self.handle_response(response, args.output)

    def handle_response(self, response, output_file):
        print(f"HTTP Status Code: {response.status_code}")
        
        if response.status_code // 100 != 2:
            print("Error: Non-2XX response received. Exiting.")
            exit(1)

        if output_file and output_file.endswith(".json"):
            self.write_json(response.json(), output_file)
        elif output_file and output_file.endswith(".csv"):
            self.write_csv(response.json(), output_file)
        else:
            print(json.dumps(response.json(), indent=2))

    @staticmethod
    def write_json(data, file_path):
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=2)
            print(f"Response written to {file_path}")

    @staticmethod
    def write_csv(data, file_path):
        keys = data[0].keys() if data else []
        with open(file_path, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
            print(f"Response written to {file_path}")

if __name__ == "__main__":
    client = RestfulClient()
    client.execute()
