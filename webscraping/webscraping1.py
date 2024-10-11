import time
import requests
import math
import os

def scrape_makaan_house_data(place, num_pages):
    # Create a directory to save HTML files if it doesn't exists.
    directory = f"data/html/{place}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    sleep = 4
    timeout = 0

    for num in range(1, num_pages+1):
        while True:
            try:
                # Fetch the page data
                response = requests.get(f"https://www.makaan.com/{place}-residential-property/buy-property-in-{place}-city?page={num}")

                if response.status_code ==  200:
                    sleep += 1
                    time.sleep(2 + int(math.log(sleep)))  # Sleep to avoid server overload
                    timeout = 0
                    print(f"Page {num}: successful")

                    # Save the HTML content
                    html = response.text
                    with open(f"{directory}/{num}.html", "w", encoding="utf-8") as file:
                        file.write(html)

                    break # Move to the next page after successful scrape
                
                else:
                    # Handle server errors
                    print(f"Page {num}: server error (status code: {response.status_code})")
                    timeout += 1
                    time.sleep(10)  # Retry after waiting for 10 seconds
                    
                    # If multiple timeouts, skip the page
                    if timeout == 2:
                        print(f"Page {num}: Failed to connect to server, moving to next page.")
                        break
                    continue

            except requests.RequestException as e:
                # Catch network-related errors and retry
                print(f"Page {num}: Request failed due to an error - {str(e)}")
                timeout += 1
                time.sleep(10)

                # If multiple timeouts, skip the page
                if timeout == 2:
                    print(f"Page {num}: Skipping this page due to multiple errors.")
                    break

# Input from the user for place and number of pages
if __name__ == "__main__":
    place = input("Entee the place name to scrape (e.g., hyderabad, mumbai): ").strip().lower()
    num_pages = int(input("Enter the number of pages to scrape: "))

    # Call the scraping function
    scrape_makaan_house_data(place, num_pages)
    print("Scraping Done Successfully....")
