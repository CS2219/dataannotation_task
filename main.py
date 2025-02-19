import requests
from bs4 import BeautifulSoup

def decode_secret_message(doc_url):
    # Fetch the raw document content (HTML)
    response = requests.get(doc_url)
    document_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(document_content, 'html.parser')

    # Find the table in the document (assuming the table is the first one in the document)
    table = soup.find('table')

    # Initialize a dictionary to hold the character grid, using (x, y) as keys
    grid = {}

    # Loop through the rows of the table, skipping the header row
    for row in table.find_all('tr')[1:]:  # Skip the header row
        # Get all the columns in this row
        cols = row.find_all('td')
        
        if len(cols) == 3:
            try:
                x = int(cols[0].text.strip())  # x-coordinate
                y = int(cols[2].text.strip())  # y-coordinate
                character = cols[1].text.strip()  # Character
                
                # Store the character in the grid dictionary
                grid[(x, y)] = character
            except ValueError:
                print(f"Skipping invalid row: {row}")
                continue

    # If the grid is empty, return a message indicating no valid data was found
    if not grid:
        print("No valid coordinate data found in the document.")
        return

    # Find the dimensions of the grid by inspecting the coordinates
    max_x = max([x for x, y in grid.keys()])
    max_y = max([y for x, y in grid.keys()])

    # Construct the grid as a list of strings, filling with spaces where necessary
    grid_output = []
    for y in range(max_y + 1):
        row = []
        for x in range(max_x + 1):
            # If the coordinate has a character, use it; otherwise, use a space
            row.append(grid.get((x, y), ' '))
        grid_output.append("".join(row))

    # Print the grid to reveal the secret message
    for row in grid_output:
        print(row)

# Example usage
decode_secret_message("https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub")
