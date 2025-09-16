from markitdown import MarkItDown
import os
import glob
import time
import datetime

md = MarkItDown(enable_plugins=True) # Set to True to enable plugins

## get list of folders within llm/scenarios
folders = glob.glob("llm/scenarios/*")

if __name__ == "__main__":

    print(f"Starting processing at {datetime.datetime.now()}")

    ### loop through each folder, and process all .docx, .doc, .pptx, .xlsx, .pdf files within each folder
    for folder in folders:
        print(f"Processing folder: {folder}")
        files = glob.glob(f"{folder}/*")
        for file in files:
            if file.endswith(('.docx', '.doc', '.pptx', '.xlsx', '.pdf')):
                print(f"Processing file: {file}")
                start_time = time.time()
                try:
                    test = md.convert(file)
                    elapsed_time = time.time() - start_time
                    print(f"Processed {file} in {elapsed_time:.2f} seconds")
                    print(f"Text content length: {len(test.text_content)} characters")
                except Exception as e:
                    print(f"Error processing {file}: {str(e)}")
                # save text_content to a .md file with the same name as the input file
                output_file = os.path.splitext(file)[0] + ".md"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(test.text_content)
                print(f"Saved text content to {output_file}")

    print(f"Finished processing at {datetime.datetime.now()}")  

    print("All done!")




