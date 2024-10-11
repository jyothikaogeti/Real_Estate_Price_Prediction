import os
import time
import requests
import math
from bs4 import BeautifulSoup
import pandas as pd

# Get the city name from user as input
city = input("Enter the city name (e.g., hyderabad): ").strip().lower()
html_directory = f"data/html/{city}/"

# Create the Directory to save the scraped data.
save_directory = f"data/raw_data/{city}/"
os.makedirs(save_directory, exist_ok=True)

# Get all the HTML files from the directory
html_files = [file for file in os.listdir(html_directory) if file.endswith(".html")]

links = []
print("-----------------------------------------------------------------")
print("Extracting links from HTML Pages")
print("-----------------------------------------------------------------")

# Extract links from HTML files
for html_file in html_files:
    file_path = os.path.join(html_directory,html_file)
        
    with open(file_path, "r", encoding="utf-8") as file:
        html = BeautifulSoup(file, "lxml")

    # Extracting all the links from the HTML page
    for element in html.find_all("li", class_="cardholder"):
        card = element.find("div", class_="cardLayout clearfix")
        if card:
            link = card.get("itemid")
            if link:  # Ensure the link exists
                links.append(link)
        print("extracted till now: ", len(links))



print("-----------------------------------------------------------------")
print("Total Links Extracted: ", len(links))
print("-----------------------------------------------------------------")
print("Scraping the Data Started")
print("-----------------------------------------------------------------")

# Initialize the data dictionary to store results
data1 = {
    "link": [], "name": [], "area": [], "society_name": [], "locality": [], "city": [], "price": [], "price_per_sqft": []
}
data2 = {}
data3 = {}
data4 = {
    "amenities":  []
}
data5 = {
    "furnish_details": []
}

timeout = 0

# Function to equalize the lengths of Dataframes.
def equalize_lengths(data_dicts, num):
    max_length = num
    for d in data_dicts:
        for key in d:
            if len(d[key]) < max_length:
                d[key].extend([""] * (max_length - len(d[key])))

# Loop through the links and scrape the data
for num in range(1, len(links)+1):
    while True:
        link = links[num-1]
        response = requests.get(link)
        if response.status_code == 200:
            data1["link"].append(link)
            try:
                page = BeautifulSoup(response.text, "lxml")
            except Exception as e:
                print(f"Error parsing page {num}: {e}")
                page = ""
            
            time.sleep(1)
            timeout = 0  # Reset timeout after a successful request
            
            try:
                head = page.find("h1", class_="type-wrap")
            except Exception as e:
                print(f"Error finding head for page {num}: {e}")
                head = ""
            
            # Extracting property details
            # property_name
            try:
                name = head.find("span", class_="type").text.strip() if head else ""
            except:
                name = ""
            data1["name"].append(name)
            
            # area
            try:
                area = head.find("span", class_="size").text.strip() if head else ""
            except:
                area = ""
            data1["area"].append(area)
            
            #society_name
            try:
                society = head.find("a", class_="loclink").text.strip() if head else ""
            except:
                society = ""
            data1["society_name"].append(society)

            #locality
            try:
                locality = head.find("span", class_="ib loc-name").text.strip() if head else ""
            except:
                locality = ""
            data1["locality"].append(locality)

            #city
            try:
                city = head.find("span", class_="ib city-name").text.strip() if head else ""
            except:
                city = ""
            data1["city"].append(city)

            try:
                head1 = page.find("div", class_="i-row clearfix")
            except Exception as e:
                print(f"Error finding head for page {num}: {e}")
                head = ""
            
            try:
                price_details = head1.find("div", class_="i-lcol")
            except:
                price_details = ""
            
            #price
            try:
                price = price_details.find("div",class_="price-wrap").text if price_details else ""
            except:
                price = ""
            data1["price"].append(price)
            
            #price_per_sqft
            try:
                price_per_sqft = price_details.find("div",class_="rate-wrap").text if price_details else ""
            except:
                price_per_sqft = ""
            data1["price_per_sqft"].append(price_per_sqft)


            try:
                details = head1.find("div",class_="i-rcol").find_all("tr",class_="ditem")
            except:
                details = ""

            try:
                keys = [ element.find("td",class_="lbl").text for element in details ]
                values= [ element.find("td",class_="val").text for element in details ]
                for col in keys:
                    if col not in list(data2.keys()):
                        if num == 1:
                            data2[col] = []
                        else:
                            data2[col] = (num-1)*[""]
                for x in range(len(values)):
                    data2[keys[x]].append(values[x])
                for key in data2:
                    if key not in keys:
                        data2[key].append("")
            except:
                for key in data2:
                    data2[key].append("")

            try:
                other_details = page.find("table", class_="kd-list js-list").find_all("tr", class_="listitem")
            except:
                other_details = ""
            
            try:
                keys = [ element.find("td",class_="lbl").text for element in other_details ]
                values= [ element.find("td",class_="val").text for element in other_details ]
                for col in keys:
                    if col not in list(data3.keys()):
                        if num == 1:
                            data3[col] = []
                        else:
                            data3[col] = (num-1)*[""]
                for x in range(len(values)):
                    data3[keys[x]].append(values[x])
                for key in data3:
                    if key not in keys:
                        data3[key].append("")
            except:
                for key in data3:
                    data3[key].append("")
            
            #amenities
            try:
                values = []
                for elements in page.find_all("div",class_="amenities-wrap js-list-wrap"):
                    values.append(str([element.text.strip().replace("\\","").replace("'","").replace("'","") for element in elements.find_all("div",class_="js-moblist-item") if "Not Available" not in element.text]).replace("'",""))

                if values:
                    data4["amenities"].append(values)
                else:
                    data4["amenities"].append("")
            except:
                data4["amenities"].append("")
            
            #furnish_details
            try:
                values = []
                for elements in page.find_all("div",class_="furnishings-wrap js-list-wrap"):
                    values.append(str([element.text.strip().replace("\\","").replace("'","").replace("'","") for element in elements.find_all("div",class_="js-moblist-item") if "Not Available" not in element.text]).replace("'",""))

                if values:
                    data5["furnish_details"].append(values)
                else:
                    data5["furnish_details"].append("")
            except:
                data5["furnish_details"].append("")


            name_= data1["name"][-1]
            print(f"{num}: {name_}")
            break  # Exit the while loop for successful scrape
        
        else:
            if timeout == 1:
                print(f"{num}: failed to connect to server and following to next page")
                break
            print(f"{num}: server error")
            timeout += 1
            time.sleep(20)  # Wait before retrying the request
            continue

# Convert dictionary to DataFrame and save to CSV
equalize_lengths([data1,data2,data3,data4,data5], len(links))
df = pd.concat([pd.DataFrame(data1), pd.DataFrame(data2), pd.DataFrame(data3), pd.DataFrame(data4), pd.DataFrame(data5)], axis=1)
df.to_csv(os.path.join(save_directory, "scraped_data.csv"), index=False)
print(f"Data saved to {save_directory} as scraped_data.csv")