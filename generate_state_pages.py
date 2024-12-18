import os
import pandas as pd

# Load the dataset
file_path = "india_censusa.csv"
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: {file_path} not found. Make sure the file exists in the current directory.")
    exit()

# Directory to save state-specific pages
output_dir = "state_pages"
os.makedirs(output_dir, exist_ok=True)

# Template for state-specific HTML pages
def create_html_page(state_name, population, density, culture, marketplace_link):
    """
    Generates the content of the HTML page for a given state.

    Parameters:
        state_name (str): The name of the state or union territory.
        population (str): The population of the state.
        density (str): The population density of the state.
        culture (str): The culture description of the state.
        marketplace_link (str): The link to the state's marketplace.

    Returns:
        str: The content of the HTML page as a string.
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{state_name} - State Information</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background-color: #f9f9f9;
                color: #333;
            }}
            header {{
                background: #6200ea;
                color: #fff;
                padding: 10px 20px;
                text-align: center;
            }}
            .container {{
                max-width: 800px;
                margin: 20px auto;
                background: #fff;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #6200ea;
            }}
            .button {{
                display: inline-block;
                margin-top: 20px;
                padding: 10px 15px;
                color: #fff;
                background-color: #007bff;
                border: none;
                text-decoration: none;
                border-radius: 5px;
                cursor: pointer;
            }}
            .button:hover {{
                background-color: #0056b3;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>{state_name} - State Information</h1>
        </header>
        <div class="container">
            <h2>State Details</h2>
            <p><b>Population:</b> {population}</p>
            <p><b>Population Density:</b> {density} people per sq. km</p>
            <p><b>Culture:</b> {culture}</p>
            <a href="{marketplace_link}" class="button" target="_blank">Visit the Marketplace</a>
        </div>
    </body>
    </html>
    """

# Generate an HTML page for each state
print("Generating state-specific pages...")
for _, row in df.iterrows():
    try:
        # Extract state-specific information from the dataset
        state_name = row["State or union territory"]
        population = row["Population"]
        density = row.get("Density[a]", "N/A")  # Use "N/A" if Density column is not available
        culture = row["Culture"]
        marketplace_link = f"https://example.com/marketplace/{state_name.replace(' ', '_').lower()}"  # Example marketplace link

        # Generate HTML content for the state
        html_content = create_html_page(state_name, population, density, culture, marketplace_link)

        # Generate a safe file name for the HTML file
        file_name = f"{state_name.replace(' ', '_').lower()}.html"

        # Save the HTML file in the output directory
        with open(os.path.join(output_dir, file_name), "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"Page generated for: {state_name}")
    except Exception as e:
        print(f"Error generating page for {state_name}: {e}")

print(f"All state-specific pages have been generated and saved in the '{output_dir}' directory!")
