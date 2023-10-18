import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

class ETendersScraper:
    def __init__(self):
        self.url = "https://etenders.gov.in/eprocure/app"

    def scrape_tender_data(self):
        try:
            r = requests.get(self.url)
            r.raise_for_status()  # Raise an error if the request is not successful

            soup = BeautifulSoup(r.text, "html.parser")
            table = soup.find("table", id="activeTenders")

            if not table:
                raise ValueError("Table with id 'activeTenders' not found on the page.")

            titles = []
            reference_numbers = []
            closing_dates = []
            bid_opening_dates = []

            for row in table.find_all("tr"):
                cells = row.find_all("td")
                if len(cells) == 4:
                    title = cells[0].text.strip()
                    title = re.sub(r'^\d+\.\s+', '', title)
                    reference_no = cells[1].text.strip()
                    closing_date = cells[2].text.strip()
                    bid_opening_date = cells[3].text.strip()
                    titles.append(title)
                    reference_numbers.append(reference_no)
                    closing_dates.append(closing_date)
                    bid_opening_dates.append(bid_opening_date)

            data = {
                "Tender Title": titles,
                "Reference No": reference_numbers,
                "Closing Date": closing_dates,
                "Bid Opening Date": bid_opening_dates,
            }
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            # Log the error for debugging and monitoring
            print(f"Error: {e}")
            return None

if __name__ == "__main__":
    scraper = ETendersScraper()
    tender_data = scraper.scrape_tender_data()

    if tender_data is not None:
        # Save the data to a CSV file
        tender_data.to_csv("tender_data.csv", index=False)
