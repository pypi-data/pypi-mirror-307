import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

import time
import warnings
import sys
import csv
import torch
from torch.utils.data import Dataset, DataLoader
from sentence_transformers import SentenceTransformer
import uuid
import ast
import os


warnings.warn("Beginning of the script.", UserWarning)

# Define the path to your preloaded models directory
models_directory = os.path.abspath("./models")
os.environ["TRANSFORMERS_CACHE"] = models_directory
os.environ["HF_HOME"] = models_directory
os.environ["TF_ENABLE_ONEDNN_OPTS"] = '0'

# Start measuring process and elapsed time
start_process_time = time.process_time()
start_time = time.time()


# Define the delimiter for splitting input lines
DELIMITER = ','

# Get parameters from sys.argv
model_name = sys.argv[1] if len(sys.argv) > 1 else sys.exit("Please provide the model name")
batch_size = int(sys.argv[2])  # the batch size
text_column = int(sys.argv[3])  # Convert the second argument to an integer (text_column)
accumulate = ast.literal_eval(sys.argv[4])  # Convert third argument (accumulate) from string to list
if len(sys.argv) == 6:
    DELIMITER = sys.argv[5]


colNames = ['text_column'] + [f'accumulate_{idx}' for idx in range(len(accumulate))]
# Generate a unique identifier for this script instance
script_uuid = uuid.uuid4()

def restore_model_name(model_fname: str) -> str:
    if model_fname.startswith("models--"):
        model_name = model_fname[len("models--"):].replace("--", "/")
        return model_name
    else:
        return model_name

# Load SentenceTransformer model and move to CUDA if available
device = 'cuda' if torch.cuda.is_available() else 'cpu'
sentence_transformer = SentenceTransformer(restore_model_name(model_name)).to(device)

class StdinDataset(Dataset):
    def __init__(self, transform=None):
        self.transform = transform
        self.csv_reader = csv.DictReader(
            sys.stdin,
            fieldnames= colNames,
            delimiter = DELIMITER
        )
        self.eof_reached = False  # Initialize EOF flag

    def __len__(self):
        return 10**9  # Large number simulating indefinite streaming

    def parse_row(self, row):
        try:
            warnings.warn(f"row : {list(row.keys())}", UserWarning)
            text_data = row['text_column']
            additional_data = [row[f'accumulate_{idx}'] for idx in range(len(accumulate))]
            return text_data, additional_data
        except IndexError:
            sys.exit()

    def __getitem__(self, idx):
        if self.eof_reached:
            return [], [], True  # Return empty lists and EOF flag

        while not self.eof_reached:
            try:
                row = next(self.csv_reader)
                sample = self.parse_row(row)
                if sample is not None:
                    text_data, additional_data = sample
                    return additional_data, text_data, False
            except StopIteration:
                self.eof_reached = True
                return [], [], True

# Custom collate function to handle empty (EOF) items
def collate_fn(batch):
    # Filter out empty entries (EOF signals)
    batch = [item for item in batch if item[1] != []]
    if len(batch) == 0:
        return [], [], True  # Return EOF-only batch if nothing valid remains

    additional_data, text_data, eof_status = zip(*batch)
    return additional_data, text_data, any(eof_status)

def create_stdin_dataloader(batch_size=1):
    dataset = StdinDataset()
    return DataLoader(dataset, batch_size=batch_size, shuffle=False, collate_fn=collate_fn)

warnings.warn("Before create_stdin_dataloader.", UserWarning)
dataloader = create_stdin_dataloader(batch_size=batch_size)
warnings.warn("create_stdin_dataloader successful.", UserWarning)
try:
    warnings.warn("before the for loop.", UserWarning)
    for additional_data, text_data, eof_status in dataloader:
        if len(text_data) == 0 or len(text_data[0]) == 0:
            sys.exit()
        warnings.warn("in the for loop.", UserWarning)
        warnings.warn(f"text_data {text_data}.", UserWarning)
        warnings.warn(f"additional data {additional_data}.", UserWarning)
        warnings.warn(f"len additional data {len(additional_data)}.", UserWarning)

        # Perform batch encoding
        embeddings = sentence_transformer.encode(text_data, convert_to_tensor=True, device=device)

        # Calculate process and elapsed time
        process_time_used = time.process_time() - start_process_time
        elapsed_time      = time.time() - start_time

        # Print output embeddings along with additional data
        for i in range(len(embeddings)):
            # i the is position of the vector embedding
            embedding_vector = embeddings[i].cpu().numpy()

            # Prepare output data for each embedding
            warnings.warn(f"additional data[i] {additional_data[i]}.", UserWarning)
            base_output_data = ""
            for j in range(len(additional_data[i])):
                base_output_data = base_output_data + str(additional_data[i][j]) + DELIMITER
            base_output_data = base_output_data + str(script_uuid) + DELIMITER
            base_output_data = base_output_data + str(process_time_used / len(embeddings)) + DELIMITER
            base_output_data = base_output_data + str(elapsed_time / len(embeddings)) + DELIMITER
            #base_output_data = base_output_data + str(text_data[i].replace(DELIMITER,' ').replace('\n',' ')) + DELIMITER
            base_output_data = base_output_data + str(model_name) + DELIMITER
            base_output_data = base_output_data + str(device)

            # base_output_data = [
            #     *[str(additional_data[i][j]) for j in range(len(additional_data[i]))],
            #     str(script_uuid),
            #     str(process_time_used / len(embeddings)),
            #     str(elapsed_time / len(embeddings)),
            #     text_data[i],
            #     model_name,
            #     device
            # ]

            # # Convert base output data to a concatenated string
            # base_output_str = ""
            # for j, item in enumerate(base_output_data):
            #     if j < len(base_output_data) - 1:
            #         base_output_str += str(item) + DELIMITER
            #     else:
            #         base_output_str += str(item)  # No DELIMITER after the last item

            # Iterate over each dimension of the embedding vector
            for dim_index, value in enumerate(embedding_vector):
                # Add the embedding dimension and value to the base output
                output_str = base_output_data + DELIMITER + str(dim_index) + DELIMITER + str(value)
                print(output_str)
            warnings.warn(f"output_str : {output_str}", UserWarning)

            start_process_time = time.process_time()
            start_time = time.time()

        if eof_status:
            sys.exit()  # Exit if EOF reached

except SystemExit:
    pass
except Exception as e:
    print("Script Failure :", sys.exc_info()[0], file=sys.stderr)
    raise
    sys.exit()