import re
import pandas as pd
import pdfplumber

def pdf_reader_plumber(pdf_path):
    def clean_cell(cell):
        """Ensure the text is clean, fixing spacing issues."""
        if isinstance(cell, str):
            # Replace multiple spaces with a single space
            cell = ' '.join(cell.split())
            # Replace missing spaces between numbers and units, e.g., "33501/min" to "3350 1/min"
            cell = re.sub(r'(\d)(?=[A-Za-z])', r'\1 ', cell)
            # Replace missing spaces between letters and numbers, e.g., "94,7W" to "94,7 W"
            cell = re.sub(r'([A-Za-z])(?=\d)', r'\1 ', cell)
        return cell

    dfs = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            for table_number, table in enumerate(tables):
                if table:
                    # Convert the table to a DataFrame
                    df = pd.DataFrame(table)

                    # Clean each cell in the DataFrame
                    df = df.apply(lambda col: col.map(clean_cell))

                    # Set generic column names
                    df.columns = [f'Col_{j+1}' for j in range(df.shape[1])]

                    # Reset index position
                    df.reset_index(drop=True, inplace=True)

                    # Append the DataFrame to the list
                    dfs.append(df)
    return dfs