import os
import glob

# input_prefix = "input"
# output_prefix = "output"
input_prefix = input("Enter input file prefix. Default: input\n") or "input"
output_prefix = input("Enter output file prefix. Default: output\n") or "output"
file_suffix = ".txt"
chunk_size = 20000

def split_file(file, chunk_size):
    with open(file, 'r') as f:
        print("Initializing text splitter.")
        text = f.read()
        print(f"Character length of input file: {len(text)}")
        chunk = text[:chunk_size]
        remaining = ""
        chunk_number = 1
        last_break = 0
        logging_count = 0
        while chunk and logging_count < 100:
            chunk = remaining + chunk
            last_period = chunk.rfind(".\n")
            if last_period != -1 and last_period <= chunk_size:
                with open(f'{output_prefix}-{str(chunk_number).zfill(2)}{file_suffix}', 'w') as chunk_file:
                    chunk_file.write(chunk[:last_period+2])
                print(f"Text break {chunk_number}: Char dist of last text break before {chunk_size} character mark is {last_period}")
                logging_count += 1
                last_break = last_break + last_period + 2
                chunk = text[last_break:last_break + chunk_size]
                remaining = ""
                chunk_number += 1
            else:
                remaining = chunk
                chunk = text[last_break + chunk_size:]
                if len(remaining + chunk) <= chunk_size:
                    last_period = (remaining + chunk).rfind(".\n")
                    if last_period != -1:
                        with open(f'{output_prefix}-{str(chunk_number).zfill(2)}{file_suffix}', 'w') as chunk_file:
                            chunk_file.write((remaining + chunk)[:last_period+2])
                        print(f"Text break {chunk_number}: Char dist of last text break before {chunk_size} character mark is {last_period}")
                        logging_count += 1
                        last_break = last_break + last_period + 2
                        chunk = text[last_break:last_break + chunk_size]
                        remaining = ""
                        chunk_number += 1
        if remaining:
            with open(f'{output_prefix}-{str(chunk_number).zfill(2)}{file_suffix}', 'w') as chunk_file:
                chunk_file.write(remaining)

files = glob.glob('{output_prefix}-*{file_suffix}')
for f in files:
    os.remove(f)

split_file(input_prefix+file_suffix, chunk_size)
