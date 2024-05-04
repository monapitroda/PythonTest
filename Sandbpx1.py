import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import time 
from time import sleep

def collect_all_links_from_homePage():
    # To collect all the links which are shown on home page
    links = []
    links_element = driver.find_elements(By.TAG_NAME, 'a')
    for link in  links_element:
        href = link.get_attribute("href")
        if href:
            links.append(href)

    # store links in json file
    with open("links.json","w") as json_file:
        json.dump(links,json_file,indent=4)

driver = webdriver.Chrome()

class PageScraper:
    def __init__(self, driver):
        self.driver = driver
    
    def home_page_header_links(self, url):
        header_links = []

        try:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # Find all header links
            header_items = soup.find_all('li', class_='menu-item')
            for item in header_items:
                link = item.find('a')['href']
                header_links.append({"header_link": link})
        except Exception as e:
            print(f"Error scraping URL: {url}, Error: {e}")

        return header_links

    def scrape_home_page(self,url):

        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        sleep(5)
        home_data = {}

        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ body content Section1 slider container
        home_slider_div = soup.find('div', class_='home-slider')
        sec_one_image_url = home_slider_div.find('img')['src']
        sec_one_slider_text = home_slider_div.find('div', class_='slider-text')
        sec_one_heading = sec_one_slider_text.find('h2').text.strip()
        # print('heading:-',sec_one_heading)
        paragraph = sec_one_slider_text.find('p').text.strip()
        # print('paragraph:- ',paragraph)
        home_data["section_1"] = {
        "ImageURL": sec_one_image_url,
        "Heading": sec_one_heading,
        "Paragraph": paragraph
        }

        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2@@@@@@@@@@@  Section2 why choose
        section_two_why_choose = soup.find('section', class_='home-why-choose')
        sec_two_heading = section_two_why_choose.find('h2').text.strip()
        secTwoBodyLists = []
        sec_two_body_list = section_two_why_choose.find_all('li')

        for sec_two_li in sec_two_body_list:
            sec_two_image_url = sec_two_li.find('img')['src']
            sec_two_header_text = sec_two_li.find('h3').text.strip()
            sec_two_paragraph = sec_two_li.find('p').text.strip()
            item_dict = {
                'HeaderText': sec_two_header_text,
                'ImageURL': sec_two_image_url,                
                'Paragraph': sec_two_paragraph
            }
            secTwoBodyLists.append(item_dict)
        home_data['section_2'] = {
            'Section2Header': sec_two_heading,
            'Section2BodyList':secTwoBodyLists
        }

        # print(secTwoBodyLists)

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2 Sec 3 
        section_three_home_awards = soup.find('section', class_='home-awards')
        sec_three_heading = section_three_home_awards.find('h2').text.strip()
        secThreeImageList = []
        sec_three_image_list = section_three_home_awards.find_all('li')

        for sec_three_li in sec_three_image_list:
            ImageUrl = sec_three_li.find('img')['src']
            secThreeImageList.append(ImageUrl)

        home_data['Section3'] = {
            'Section3Header': sec_three_heading,
            'Section3ImageList':secThreeImageList
        }

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ sec 4 
        sec_four_process = soup.find('div', class_='process')
        sec_four_heading = sec_four_process.find('h2').text.strip()
        sec_four_paragraph = sec_four_process.find('p').text.strip()
        secFourProcessNameList = []
        sec_four_process_list = sec_four_process.find_all('div', class_='process-box')

        for sec_four_process in sec_four_process_list:
            sec_four_image_url = sec_four_process.find('img')['src']
            sec_four_heading = sec_four_process.find('h3').text.strip()
            sec_four_paragraph = sec_four_process.find('p').text.strip()
            # 
            item_dict = {
                'Section4ImageUrl': sec_four_image_url,
                'Section4Header': sec_four_heading,
                'Section4Paragraph': sec_four_paragraph
            }
            secFourProcessNameList.append(item_dict)

        home_data['Section4']={
            'Header': sec_four_heading,
            'Paragraph': sec_four_paragraph,
            'ProcessList':secFourProcessNameList
        }

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@22 featuresupplier class
        sec_feature_supplier = soup.find('section', class_='featured-suppliers home-fs')
        sec_feature_supplier_heading = sec_feature_supplier.find('h2').text.strip()
        sec_feature_supplier_paragrapg = sec_feature_supplier.find('p').text.strip()
        featurelist = []
        sec_feature_lists = sec_feature_supplier.find_all('div', class_='fs-single')

        for secfeaturelists in sec_feature_lists:
            feature_categoryName = secfeaturelists.find('span', class_='fs-cat')
            feature_categoryName = feature_categoryName.text.strip()
            feature_cat_header = secfeaturelists.find('h3').text.strip()
            Feature_url = secfeaturelists.find('a')
            url = Feature_url.get('href')
            feature_cat_image = secfeaturelists.find_all('img')
            if len(feature_cat_image) >= 2:
                second_img = feature_cat_image[1]
                feature_cat_image = second_img.get('src')
            item_dict = {
                'FeatureSectionImageUrl': feature_cat_image,
                'FeatureSectionHeader': feature_cat_header,
                'FeatureSectionCategoryName': feature_categoryName,
                'FeatureURL': url
            }
            featurelist.append(item_dict)

        home_data['FeatureSection'] = {
            'Header': sec_feature_supplier_heading,
            'Paragraph': sec_feature_supplier_paragrapg,
            'CategoryList': featurelist
        }
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ sec class hcwh-home
        sec_hcwh_home = soup.find('section', class_='hcwh-home')
        sec_hcwh_home_header = sec_hcwh_home.find('h2').text.strip()
        sec_one = sec_hcwh_home.find('div', class_='hcwh-sec-01')
        # print(sec_hcwh_home_header)
        sechcwhhomehelplist = []
        sec_hcwh_home_help = sec_one.find_all('a')
        # print(sec_hcwh_home_help)
        for helplinks in sec_hcwh_home_help:
            img_tag = helplinks.find('img')
            if img_tag:
                    help_image_url = img_tag['src']
            else:
                    help_image_url = None
            altattribute_text = img_tag['alt']
            help_text = helplinks.get_text(strip=True)
            item_dict = {
                'SectionHCWHImageUrl': help_image_url,
                'SectionHCWHText': help_text,
                'SectionHCWHAttributeText': altattribute_text
            }
            sechcwhhomehelplist.append(item_dict)  
        # print(sechcwhhomehelplist)

        home_data['HCWHSecationOne'] = {
            'Header': sec_hcwh_home_header,
            'HelpLinkLists': sechcwhhomehelplist
        }

        # Section 2 of sec_hcwh_home
        sec_two_hceh_block = sec_hcwh_home.find_all('div', class_='hceh-block')
        sectwohcehblocklist = []

        for allblock in sec_two_hceh_block:
            hceh_header = allblock.find('h2').text.strip()
            hech_image_url = allblock.find('img')['src']
            attribute_name = allblock.find('img')['alt']
            hceh_paragraph = allblock.find_all('p')
            # print(hceh_paragraph)
            if len(hceh_paragraph) >= 2:
                first_paragrapg = hceh_paragraph[0]
                first_paragrapg = first_paragrapg.text.strip()
                next_url = hceh_paragraph[1]        
                a_tag = next_url.find('a')
                url = a_tag.get('href')
                if url is None or url == '':
                    url = ''
                text = next_url.text.strip()
            item_dict = {
                'HCEHHeader': hceh_header,
                'HCEHImageUrl': hech_image_url,
                'HCEHParagraph': first_paragrapg,
                'HCEHUrl': url,
                'HCEHText': text
            }
            sectwohcehblocklist.append(item_dict)

        home_data['HCWHSecationTwo'] = {
            'HCEHLists': sectwohcehblocklist
        }         

        combined_data =  {'Home': home_data}
        return combined_data
        # print(combined_data)
        # json_data = json.dumps(combined_data, indent=4)

        # with open('HomeScraped_data.json', 'w') as json_file:
        #     json.dump(combined_data, json_file, indent=4)     
     
    def scrape_assessment(self,url):
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        sleep(10)

        assessment_data = {}
        # banner image and text
        home_slider_div = soup.find('div', class_='banner-con')
        banner_image = home_slider_div.find('img')['src']
        banner_text = home_slider_div.find('h1').text.strip()
        # print(banner_image)
        # print(banner_text)
        assessment_data["Section1"] = {
            'HeaderImage': banner_image,
            'HeaderText': banner_text
        }

        # Inner section 
        inner_section = soup.find('section',class_='inner-content test')
        inner_header = inner_section.find('h2').text.strip()
        # print('inner_header:- ',inner_header)
        inner_small_header = inner_section.find('h3').text.strip()
        # print('inner_small_header:- ',inner_small_header)
        inner_paragraph = inner_section.find('p').text.strip()
        # print('inner_paragraph:- ',inner_paragraph)

        field_set = inner_section.find_all('div',class_='form-card')
       
        fieldcategory = []
        for field in field_set:
            field_header = field.find('h2').text.strip()
            field_paragraph = field.find('p').text.strip()
            field_category = field.find_all('li')
            
            for cate in field_category:
                category = cate.find('div',class_='main-cat').text.strip()        
                sub_category = cate.find_all('span',class_='wpcf7-list-item-label') 

                subcategory = []
                for sub_cat in sub_category:
                    subcat = sub_cat.get_text()
                    subcategory.append(subcat)
                    # print(subcat)
                fieldcategory.append({
                    'category': category,
                    'subCategory': subcategory
                })
            # print(fieldcategory)
        assessment_data["Section2"] = {
            "Header": inner_header,
            "SubHeader": inner_small_header,
            "Paragraph": inner_paragraph,
            "CategoryLists": fieldcategory
        }     
        
        combined_data2 = {'Assessment': assessment_data}

        return combined_data2
        # print(combined_data)
        # json_data = json.dumps(combined_data, indent=4)

        # with open('AssessmentScraped_data.json', 'w') as json_file:
        #     json.dump(combined_data, json_file, indent=4)
        
    def scrape_FSN_suppliers(self,url):
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        sleep(10)

        FSN_data = {}
        banner_text = soup.find('h1').text.strip()
        banner_image = soup.find('div', class_='banner-con')
        image_url = banner_image.find('img')['src']
        FSN_data["SectionHeader"] = {
            "HeaderImage": image_url,
            "HeaderText": banner_text
        }


        base_url = 'https://franchisesuppliernetwork.com/fsn-suppliers/page/'
        sleep(7)
        page_number = 1
        categorylists = []
        while True:
            url = f"{base_url}{page_number}/"
            driver.get(url)
            driver.implicitly_wait(10)
            sleep(7)
            html_source = driver.page_source
            soup = BeautifulSoup(html_source, 'html.parser')

            # Find all div tags with class "fs-single-col"
            fs_single_cols = soup.find_all('div', class_='fs-single-col')

            for fs_single_col in fs_single_cols:
                    # Extract category information
                    categories = fs_single_col.find('div', class_='featured-catg-btns')
                    category_names = [cat.text.strip() for cat in categories.find_all('span', class_='fs-cat')]
            
                    # Extract company name and image URL
                    company_name = fs_single_col.find('h3').text.strip()
                    image_url = fs_single_col.find('img')['src']
                    Category_url = fs_single_col.find('a')['href']
            
                    item_dict = {
                    'Category': category_names,
                    'CompanyName': company_name,                
                    'ImageURL': image_url,
                    'CategoryUrl': Category_url
                    }
                    categorylists.append(item_dict)                  

            # Check if there is a next page
            next_page = soup.find('a', class_='nextpostslink')
            sleep(7)
            if not next_page:
                break  # Exit the loop if there's no next page

            # Increment the page number for the next iteration
            page_number += 1

        FSN_data["Category"] = categorylists
        combined_data3 = {'FNS Supplier': FSN_data}
        return combined_data3
        # json_data = json.dumps(combined_data, indent=4)

        # with open('FNSSuppliedScraped_data.json', 'w') as json_file:
        #     json.dump(combined_data, json_file, indent=4)

    def scrape_resources(self,url):

        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        sleep(10)

        resources_data = {}
        banner_text = soup.find('h1').text.strip()
        banner_image = soup.find('div', class_='banner-con')
        image_url = banner_image.find('img')['src']
        resources_data["Header"] = {
            "HeaderText": banner_text,
            "HeaderImage": image_url
        }

        base_url = 'https://franchisesuppliernetwork.com/resources/page/'
        page_number = 1
        categorylists=[]
        while True:
            url = f"{base_url}{page_number}/"
            driver.get(url)
            driver.implicitly_wait(10)
            sleep(7)
            html_source = driver.page_source
            soup = BeautifulSoup(html_source, 'html.parser')

            # Find all div tags with class "single-news"
            news_items = soup.find_all('div', class_='single-news')

            for item in news_items:
                image_url = item.find('img')['src']
                category = item.find('div', class_='lncategory').text.strip()
                title = item.find('h3').text.strip()
                paragraph = item.find('p').text.strip()
                article_url = item.find('a', class_='btn')['href']
                
                item_dict = {
                'Category': category,
                'Title': title,                
                'ImageURL': image_url,
                'CategoryUrl': article_url,
                'paragraph': paragraph
                }
                categorylists.append(item_dict) 

           
            next_page = soup.find('a', class_='nextpostslink')
            sleep(7)
            if not next_page:
                break  
            
            page_number += 1

        resources_data["Category"] = categorylists
            # Add a delay to avoid hitting the server too frequently
        time.sleep(2)
        combined_data4 = {'Resources': resources_data}
        return combined_data4
        # print(combined_data)
        # json_data = json.dumps(combined_data, indent=4)

        # with open('ResourcesScraped_data.json', 'w') as json_file:
        #     json.dump(combined_data, json_file, indent=4)

    def scrape_about(self,url):
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        sleep(5)

        data_about={}
        banner_text = soup.find('h1').text.strip()
        banner_image = soup.find('div', class_='banner-con')
        image_url = banner_image.find('img')['src']

        about_div = soup.find('div', class_='contentside')
        Header = ""
        Paragraph = ""
        if about_div:
            h2_tag = about_div.find('h2')
            if h2_tag:
               Header =  h2_tag.text.strip()
            
            p_tags = about_div.find_all('p')
            for p_tag in p_tags:
                Paragraph =  p_tag.text.strip()
        else:
            print("Div element not found.")
        
        data_about["AboutNetwork"] ={
            "HeaderText": banner_text,
            "HeaderImage": image_url,
            "Header": Header,
            "Paragraph": Paragraph
        }

        inner_header = soup.find('h2').text.strip()
        team_row_scraping = soup.find_all('div',class_='row team-row')
        teamrow = []

        for row in team_row_scraping:
            image_url = row.find('img')['src']
            member_name = row.find('h3').text.strip()
            member_designation = row.find('h4').text.strip()
            history = ""
            teamhistory = ''.join([p.text.strip() for p in row.find_all('p')])
            item_dict = {
                    'image_url': image_url,
                    'member_name': member_name,
                    'member_designation': member_designation,
                    'teamhistory': teamhistory
                }
            teamrow.append(item_dict)
        
        data_about["TeamList"] =teamrow

        time.sleep(2)
        combined_data5 = {'About': data_about}
        return combined_data5
        # print(combined_data)
        # json_data = json.dumps(combined_data, indent=4)

        # with open('AboutScraped_data.json', 'w') as json_file:
        #     json.dump(combined_data, json_file, indent=4)

    def scrape_contact(self,url):

        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        sleep(10)

        data_contact = {}
        banner_text = soup.find('h1').text.strip()
        banner_image = soup.find('div', class_='banner-con')
        image_url = banner_image.find('img')['src']
        contact_left = soup.find('div', class_='contact-left')

        data_contact["HeaderSection"] = {
            "HeaderText": banner_text,
            "HeaderImage": image_url
        }

        contact = []

        if contact_left:
            contact_infos = contact_left.find_all('div', class_='contact-info')
            # print('newcontact_infos:-',contact_infos)
            for contact_info in contact_infos:
                text_content = contact_info.get_text(separator='\n').strip()
                if 'Email:' in text_content:
                    address, email = map(str.strip, text_content.split('Email:'))
                else:
                    address, email = text_content.strip(), None

            item_dict = {
            'Address': address,
            'email': email
            }
            contact.append(item_dict)

        data_contact["TeamList"] =contact

        time.sleep(2)
        combined_data6 = {'About': data_contact}
        return combined_data6
        # print(combined_data)
        # json_data = json.dumps(combined_data, indent=4)

        # with open('ContactScraped_data.json', 'w') as json_file:
        #     json.dump(combined_data, json_file, indent=4)

    def scrape_financial_services(self,url):
        
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        sleep(10)

        data = {}
        banner_text = soup.find('h1').text.strip()
        banner_image = soup.find('div', class_='banner-con')
        image_url = banner_image.find('img')['src']

        data["HeaderSection"] = {
            "HeaderText": banner_text,
            "HeaderImage": image_url
        }
        data_list = []
        contentside_div = soup.find('div', class_='contentside')
        if contentside_div:
            headers_and_paragraphs = contentside_div.find_all(['h2', 'p'])    
            current_header = ""
            current_paragraphs = []
            
            for tag in headers_and_paragraphs:
                if tag.name == 'h2':            
                    if current_header:
                        current_data = {'header': current_header, 'paragraphs': [p.text.strip() for p in current_paragraphs]}
                        data_list.append(current_data)
                        current_paragraphs = []
                    current_header = tag.text.strip()                        
                elif tag.name == 'p':            
                    current_paragraphs.append(tag)
            
            if current_header:
                current_data = {'header': current_header, 'paragraphs': [p.text.strip() for p in current_paragraphs]}
                data_list.append(current_data)
        data["DetailsofFinancialServices"] = data_list
        print(data_list)
        time.sleep(2)
        combined_data = {'DetailsofFinancialServices': data}
        return combined_data
        # # print(combined_data)
        # json_data = json.dumps(combined_data, indent=4)

        # with open('FinancialServices_data.json', 'w') as json_file:
        #     json.dump(combined_data, json_file, indent=4)

    def scrape_human_resource_services(self,url):
        
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        sleep(15)

        data = {}
        banner_text = soup.find('h1').text.strip()
        banner_image = soup.find('div', class_='banner-con')
        image_url = banner_image.find('img')['src']
        contentside_div = soup.find('div', class_='contentside')

        # data["HeaderSection"] = {
        #     "HeaderText": banner_text,
        #     "HeaderImage": image_url
        # }

        data_list = []
        if contentside_div:
            headers_and_paragraphs = contentside_div.find_all(['h2', 'p'])    
            current_header = ""
            current_paragraphs = []
            
            for tag in headers_and_paragraphs:
                if tag.name == 'h2':            
                    if current_header:
                        current_data = {'header': current_header, 'paragraphs': [p.text.strip() for p in current_paragraphs]}
                        data_list.append(current_data)
                        current_paragraphs = []
                    current_header = tag.text.strip()  
                elif tag.name == 'p':            
                    current_paragraphs.append(tag)
            
            if current_header:
                current_data = {'header': current_header, 'paragraphs': [p.text.strip() for p in current_paragraphs]}
                data_list.append(current_data)

        data["DetailsofHumanResourceServices"] = data_list

        time.sleep(2)
        combined_data = {'DetailsofHumanResourceServices': data}
        # print(combined_data)
        return combined_data
        # json_data = json.dumps(combined_data, indent=4)

        # with open('HumanResourceServices_data.json', 'w') as json_file:
        #     json.dump(combined_data, json_file, indent=4)

    def scrape_marketing_services(self,url):
        
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        sleep(10)

        data = {}
        banner_text = soup.find('h1').text.strip()
        banner_image = soup.find('div', class_='banner-con')
        image_url = banner_image.find('img')['src']
        data["HeaderSection"] = {
            "HeaderText": banner_text,
            "HeaderImage": image_url
        }

        data_list = []
        contentside_div = soup.find('div', class_='contentside')
        if contentside_div:
            headers_and_paragraphs = contentside_div.find_all(['h2', 'p'])    
            current_header = ""
            current_paragraphs = []
            
            for tag in headers_and_paragraphs:
                if tag.name == 'h2':            
                    if current_header:
                        current_data = {'header': current_header, 'paragraphs': [p.text.strip() for p in current_paragraphs]}
                        data_list.append(current_data)
                        current_paragraphs = []
                    current_header = tag.text.strip()  
                elif tag.name == 'p':            
                    current_paragraphs.append(tag)
            
            if current_header:
                current_data = {'header': current_header, 'paragraphs': [p.text.strip() for p in current_paragraphs]}
                data_list.append(current_data)

        data["DetailsofMarketingServices"] = data_list

        time.sleep(2)
        combined_data = {'DetailsofMarketingServices': data}
        return combined_data
        # print(combined_data)
        # json_data = json.dumps(combined_data, indent=4)

        # with open('MarketingServices_data.json', 'w') as json_file:
        #     json.dump(combined_data, json_file, indent=4)

    def scrape_opertation_services(self,url):
        
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        sleep(10)

        data={}
        banner_text = soup.find('h1').text.strip()
        banner_image = soup.find('div', class_='banner-con')
        image_url = banner_image.find('img')['src']

        data["HeaderSection"] = {
            "HeaderText": banner_text,
            "HeaderImage": image_url
        }

        data_list =[]
        contentside_div = soup.find('div', class_='contentside')
        if contentside_div:
            headers_and_paragraphs = contentside_div.find_all(['h2', 'p'])    
            current_header = ""
            current_paragraphs = []
            
            for tag in headers_and_paragraphs:
                if tag.name == 'h2':            
                    if current_header:
                        current_data = {'header': current_header, 'paragraphs': [p.text.strip() for p in current_paragraphs]}
                        data_list.append(current_data)
                        current_paragraphs = []
                    current_header = tag.text.strip()  
                elif tag.name == 'p':            
                    current_paragraphs.append(tag)
            
            if current_header:
                current_data = {'header': current_header, 'paragraphs': [p.text.strip() for p in current_paragraphs]}
                data_list.append(current_data)
            
        data["DetailsofOperationServices"] = data_list

        time.sleep(5)
        combined_data = {'DetailsofOperationServices': data}
        return combined_data
        # print(combined_data)
        # json_data = json.dumps(combined_data, indent=4)

        # with open('OperationServices_data.json', 'w') as json_file:
        #     json.dump(combined_data, json_file, indent=4)

    def scrape_real_estate_services(self,url):
        
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        sleep(10)

        data = {}
        banner_text = soup.find('h1').text.strip()
        banner_image = soup.find('div', class_='banner-con')
        image_url = banner_image.find('img')['src']

        data["HeaderSection"] = {
            "HeaderText": banner_text,
            "HeaderImage": image_url
        }

        data_list = []
        contentside_div = soup.find('div', class_='contentside')
        if contentside_div:
            headers_and_paragraphs = contentside_div.find_all(['h2', 'p'])    
            current_header = ""
            current_paragraphs = []
            
            for tag in headers_and_paragraphs:
                if tag.name == 'h2':            
                    if current_header:
                        current_data = {'header': current_header, 'paragraphs': [p.text.strip() for p in current_paragraphs]}
                        data_list.append(current_data)
                        current_paragraphs = []
                    current_header = tag.text.strip()  
                elif tag.name == 'p':            
                    current_paragraphs.append(tag)
            
            if current_header:
                current_data = {'header': current_header, 'paragraphs': [p.text.strip() for p in current_paragraphs]}
                data_list.append(current_data)
        data["DetailsofRealEstateServices"] = data_list

        time.sleep(2)
        combined_data = {'DetailsofRealEstateServices': data}
        return combined_data
        # print(combined_data)
        # json_data = json.dumps(combined_data, indent=4)

        # with open('RealEstateServices_data.json', 'w') as json_file:
        #     json.dump(combined_data, json_file, indent=4)

    def scrape_legal_services(self,url):
        
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        sleep(10)

        data = {}
        banner_text = soup.find('h1').text.strip()
        banner_image = soup.find('div', class_='banner-con')
        image_url = banner_image.find('img')['src']

        data["HeaderSection"] = {
            "HeaderText": banner_text,
            "HeaderImage": image_url
        }
        contentside_div = soup.find('div', class_='contentside')

        data_list = []
        if contentside_div:
            headers_and_paragraphs = contentside_div.find_all(['h2', 'p'])    
            current_header = ""
            current_paragraphs = []
            
            for tag in headers_and_paragraphs:
                if tag.name == 'h2':            
                    if current_header:
                        current_data = {'header': current_header, 'paragraphs': [p.text.strip() for p in current_paragraphs]}
                        data_list.append(current_data)
                        current_paragraphs = []
                    current_header = tag.text.strip()  
                elif tag.name == 'p':            
                    current_paragraphs.append(tag)
            
            if current_header:
                current_data = {'header': current_header, 'paragraphs': [p.text.strip() for p in current_paragraphs]}
                data_list.append(current_data)

        data["DetailsofLegalServices"] = data_list

        time.sleep(2)
        combined_data = {'DetailsofLegalServices': data}

        return combined_data
        # # print(combined_data)
        # json_data = json.dumps(combined_data, indent=4)

        # with open('LegalServices_data.json', 'w') as json_file:
        #     json.dump(combined_data, json_file, indent=4)



