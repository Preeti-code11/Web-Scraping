import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options to ignore certificate errors
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--log-level=3')  # Suppress logging output

# Initialize ChromeDriver with the specified options
driver = webdriver.Chrome(options=options)

# Open the CSV file for writing
with open('product_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['Product Name', 'Product Description', 'Main Image URL', 'Thumbnail Image URLs', 'Breadcrumb Navigation'])

    try:
        # Open a webpage
        driver.get('https://www.daltile.com/products/Natural-Stone/Marble')

        # Locate elements with the specified class and retrieve attribute
        elements = driver.find_elements(By.XPATH, '//*[@class="color-swatch-card"]')
        if elements:  # Check if the elements list is not empty
            for index in range(len(elements)):
                try:
                    # Re-locate the element to avoid stale element exception
                    elements = driver.find_elements(By.XPATH, '//*[@class="color-swatch-card"]')
                    element = elements[index]

                    # Scroll into view and click using JavaScript
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    driver.execute_script("arguments[0].click();", element.find_element(By.XPATH, './/img'))

                    # Extract product name and description
                    product_name = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@class="page-title"]'))
                    ).text
                    product_description = driver.find_element(By.XPATH, '//*[@class="product-bullets"]').text
        
                    # Extract main image URL
                    main_image_element = driver.find_element(By.XPATH, '//*[@class="carousel-image-border"]/img')
                    main_image_url = main_image_element.get_attribute('src')
        
                    # Extract thumbnail image URLs
                    thumbnail_elements = driver.find_elements(By.XPATH, '//*[@class="carousel-image-border"]')[1:]
                    thumbnail_image_urls = [element.find_element(By.XPATH, './/img').get_attribute('src') for element in thumbnail_elements]
        
                    # Extract breadcrumb navigation
                    breadcrumb_elements = driver.find_elements(By.XPATH, '//*[@class="breadcrumb initialized"]//li | //*[@class="breadcrumb-item home "]//a')
                    breadcrumb_list = []
                    for element in breadcrumb_elements:
                        breadcrumb_text = element.text
                        breadcrumb_url = element.get_attribute('href') if element.tag_name == 'a' else None
                        breadcrumb_list.append(f"{breadcrumb_text} ({breadcrumb_url})" if breadcrumb_url else breadcrumb_text)

                    # Write the extracted information to the CSV file
                    writer.writerow([
                        product_name,
                        product_description,
                        main_image_url,
                        ', '.join(thumbnail_image_urls),
                        ' > '.join(breadcrumb_list)
                    ])

                    # Go back to the previous page
                    driver.back()

                except Exception as e:
                    print(f"Error processing element at index {index}: {e}")
                
        else:
            print("No elements found with the specified class.")
    finally:
        # Close the browser
        driver.quit()
