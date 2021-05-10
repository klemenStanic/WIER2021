import utils
import os
import sys
import time

# "document": ""
# "snippets": []

results = []


def sequential_search(q):
    global results
    data_dir = "../data/"
    for dir in os.listdir(data_dir):
        if dir == "nltk_data":
            continue
        site_dir = os.path.join(data_dir, dir)
        for file_name in os.listdir(site_dir):
            file_path = os.path.join(site_dir, file_name)
            print(f'\rImporting file: {file_path}', end="")
            with open(file_path, 'r') as file:
                file_text = file.read()
                file_text = utils.get_only_text_from_html(file_text)
                indexed_data = utils.preprocess_text(file_text)

                item = {"document": file_path, "snippets": [], "freq": 0}
                for query in q:
                    if query in indexed_data:
                        item["snippets"].extend(utils.find_surroundings_from_text(file_text, indexed_data[query]))
                item["freq"] = len(item["snippets"])
                if item["freq"] > 0:
                    results.append(item)
        print("", flush=True)
        break


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Please enter query string.')
        sys.exit()

    time_start = time.time()
    # Query preprocessing
    q = list(utils.preprocess_text(sys.argv[1]).keys())

    # Do sequential searching
    sequential_search(q)

    print("Processing data...")
    # Sort data by frequency
    results.sort(reverse=True, key=lambda x: len(x["snippets"]))

    for result in results:
        print(f'Document: {result["document"]}')
        print(f'Frequency: {len(result["snippets"])}')
        for i in result["snippets"]:
            print(f'... {i} ', end='')
        print('...\n---------------------')

    time_stop = time.time()
    print(f"The needed: {time_stop - time_start}s")



