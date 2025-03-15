from selenium import webdriver
from selenium.webdriver.common.by import By 
from getpass import getpass
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import openpyxl
import os
import matplotlib.pyplot as plt
import seaborn 

# excel dosyası için küçük bir veri yapısı oluşturuyoruz
phone_dict = {
    'name': [], 'price': [], 'marca': [],
    'color': [], 'capacity': [],
    'operating_system': [], 'ram': [],
    'model':[] , 'url': []}



options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--lang=en')
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)
driver.get('https://www.ebay.com/sch/i.html?_from=R40&_nkw=apple%20iphone%2011&_sacat=0&LH_All=1&Brand=Apple&_dcat=9355&_udlo=100&rt=nc')


list_items = driver.find_elements(By.CSS_SELECTOR, 'li.s-item')
phone_urls = []


# her bir sayfada bulunan telefonların linklerini alıyoruz
def get_phone_urls():
     while True:
        list_items = driver.find_elements(By.CSS_SELECTOR, 'li.s-item')
        for list_item in list_items:
            phone_link = list_item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            phone_urls.append(phone_link)
              

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'a.pagination__next')
            next_button.click()
        except:
            break


get_phone_urls()
phone_urls = list(set(phone_urls))

count = 0

# her bir telefonun özelliklerini safalardan döngü ile alıyoruz
print(len(phone_urls))

for url in phone_urls:
    driver.get(url)

    phone_dict['url'].append(url)

    # scarping için farklı diller
    marca_lang=["Marca", "Brand", "Marque", "Marke", "Marchio", "Merk", "Marka"]
    model_lang = ["Modelo", "Model", "Modèle","Modello"]
    color_lang= ["Colore","Color",]
    cap_lang=["Capacidad de almacenamiento","Capacità di memorizzazione","Capacité de stockage","Speicherkapazität",""]
    sis_lang = ["Sistema operativo", "Operating System", "Système d'exploitation", "Betriebssystem", "Sistema Operacional", "Sistema Operacyjny"]
    ram_lang = ["Memoria RAM", "RAM"]

    try:
        name = driver.find_element(By.XPATH, '//div[@class="vim x-item-title"]//span[@class="ux-textspans ux-textspans--BOLD"]').text
        phone_dict['name'].append(name)
    except:
        phone_dict['name'].append('Name not found')

    try:
        price = driver.find_element(By.XPATH, '//div[@class="x-price-primary"]//span[@class="ux-textspans"]').text
        phone_dict['price'].append(price)
    except:
        phone_dict['price'].append('Price not found')
    
    marca='none' 
    for lang in marca_lang:
        try:
            marca = driver.find_element(By.XPATH,f'//span[text()="{lang}"]/ancestor::dl/dd').text
            break
        except:
            continue
    
    phone_dict['marca'].append(marca)
    
    model = 'None'
    for lang in model_lang:
        try:
            model = driver.find_element(By.XPATH, f'//span[text()="{lang}"]/ancestor::dl/dd').text
            break  # Öğe bulunduysa döngüden çık
        except:
            continue

    phone_dict['model'].append(model)

    
    color ='None'
    for lang in color_lang:
        try:
            color = driver.find_element(By.XPATH,f'//span[text()="{lang}"]/ancestor::dl/dd').text
            break
        except:
            continue
    phone_dict['color'].append(color)


    capacity='None'
    for lang in cap_lang:
        try:
            capacity= driver.find_element(By.XPATH,f'//span[text()="{lang}"]/ancestor::dl/dd').text
            break
        except:
            continue
    phone_dict['capacity'].append(capacity)


    operating_system = 'None'
    for lang in sis_lang:
        try:
            operating_system = driver.find_element(By.XPATH, f'//span[text()="{lang}"]/ancestor::dl/dd').text
            break
        except:
            continue
    phone_dict['operating_system'].append(operating_system)



    ram='None'
    for lang in ram_lang:
        try:
            ram=driver.find_element(By.XPATH,f'//span[text()="{lang}"]/ancestor::dl/dd').text
            break
        except:
            continue
    phone_dict['ram'].append(ram)
    

    count +=1
    print(count)
    for key, value in phone_dict.items():
        print(f"{key}: {len(value)}")
    print('name')
    print(name) 
    print(model)
    print(price)
    print(marca)
    print(color)
    print(capacity)
    print(operating_system)
    print(ram)
    print(url)




def balance_dict_lengths(data_dict):
    max_length = max(len(v) for v in data_dict.values())
    for key, value in data_dict.items():
        while len(value) < max_length:
            value.append('Not Found')

balance_dict_lengths(phone_dict)


df=pd.DataFrame(phone_dict)
df.to_excel('phoneinfo.xlsx', index=False)


print("------- Veriyi Çekildi-----")


# veri analizi yapmak için fonksiyon oluşturuyoruz
def get_data_analyz():
    # Renk çevirisi için eşleşme tablosu
    color_translation = {
        "Nero": "Black",
        "Morado": "Purple",
        "Rosso": "Red",
        "Blu": "Blue",
        "Negro": "Black",
        "Verde": "Green",
        "Bianco": "White",
        "Oro": "Gold",
        "None": "None",
        "Viola": "Purple"
    }

    # Renk sözlüğü
    color_map = {
        'Black': 'black',
        'White': '#FFFFFF',
        'Blue': '#ACDBC7',
        'Red': '#E70013',
        'Green': '#A3AAA7',
        'Purple': '#CAC4CE',
    }

    # İlk Excel dosyasını kontrol et ve oku
    file_path = 'C:\\Users\\90543\\Desktop\\pyhton\\phoneinfo.xlsx'
    if os.path.exists(file_path):
        print("Dosya mevcut!")
    else:
        print("Dosya bulunamadı. Yolunu kontrol et!")

    # Excel dosyasını oku
    df = pd.read_excel(file_path)

    # "iPhone 11" olmayan satırları sil
    df = df[df['model'] == 'Apple iPhone 11'] 

    # Renk sütununu İngilizce'ye çevir
    if 'color' in df.columns:
        df.loc[:, 'color'] = df['color'].map(color_translation).fillna("Unknown")
        print("Renkler İngilizce'ye çevrildi.")
    else:
        print("Excel dosyasında 'color' sütunu bulunamadı!")

    # 'price' sütunundaki 'EUR' kısmını sil ve sayısal değere çevir
    if 'price' in df.columns:
        df.loc[:, 'price'] = df['price'].astype(str).str.replace('EUR ', '', regex=False)
        df.loc[:, 'price'] = pd.to_numeric(df['price'], errors='coerce')

        # İstatistiksel hesaplamalar
        median_price = df['price'].median()
        mode_price = df['price'].mode()[0] if not df['price'].mode().empty else None
        std_price = df['price'].std()
        variance_price = df['price'].var()

        # Hesaplanan değerleri yazdır
        print(f"Medyan: {median_price}")
        print(f"Mod: {mode_price}")
        print(f"Standart Sapma: {std_price}")
        print(f"Varyans: {variance_price}")
    else:
        print("Excel dosyasında 'price' sütunu bulunamadı!")

    # Color ve Capacity sütunlarındaki eksik değerleri doldur
    for index, row in df.iterrows():
        # Eksik renk kontrolü
        if row['color'] in ['None', 'Unknown']:
            name_parts = row['name'].split()
            for part in name_parts:
                if part.lower() in ['black', 'blue', 'green', 'red', 'white','Purple', 'gold']:
                    df.at[index, 'color'] = part.capitalize()
                    break
            


        # Eksik kapasite kontrolü
        if row['capacity'] in ['None','Used'] or pd.isna(row['capacity']):
            name_parts = row['name'].split()
            for part in name_parts:
                if 'gb' in part.lower():
                    df.at[index, 'capacity'] = part.upper()
                    break
        df['capacity'] = df['capacity'].str.replace('Go', 'GB', regex=False) #dil dönüşümü
        df['capacity'] = df['capacity'].str.strip().str.replace(' ', '') 

    # Güncellenmiş Excel dosyasını kaydet
    output_path = 'C:\\Users\\90543\\Desktop\\pyhton\\phoneinfo_update.xlsx'
    df.to_excel(output_path, index=False)
    print("Eksik renkler ve kapasiteler 'name' sütunundan alınarak tamamlandı ve dosya güncellendi.")

    # Fiyat için Box-plot oluştur
    if 'price' in df.columns:
        plt.figure(figsize=(8, 6))
        box = plt.boxplot(df['price'].dropna(), vert=True, patch_artist=True)
        for patch in box['boxes']:
            patch.set(facecolor='#da627d')
        plt.title('Box Plot of Price for Apple iPhone 11')
        plt.ylabel('Price')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.show()

    else:
        print("Box-plot oluşturulamadi çünkü 'price' sütunu bulunamadi!")

    #Farklı depolama kapasitelerine sahip telefonların yüzdesini görmek için pie-chart
    capacity_counts = df['capacity'].value_counts()
    plt.figure(figsize=(8, 6))
    colo = [ 'purple', 'pink', 'gold']
    capacity_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=colo)
    plt.title('Capacity Distribution for Apple iPhone 11')
    plt.ylabel('')  
    plt.show()

    #Renk ve Fiyat Arasındaki ilişki
    df_grouped = df.groupby('color')['price'].mean().sort_values()
    colors = [color_map.get(color, 'orange') for color in df_grouped.index]  # Her bar için rengi renk haritasından al
    # Bar grafiği
    plt.figure(figsize=(8, 6))
    df_grouped.plot(kind='bar', color=colors, edgecolor='black')
    plt.title('Average Price by Color for Apple iPhone 11')
    plt.xlabel('Color')
    plt.ylabel('Average Price')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=1)
    plt.show()

    #Fiyat Ve Kapasite arasındaki ilişkisi
    df['capacity_numeric'] = df['capacity'].str.replace('GB', '').astype(float) # Kapasiteyi sayıya çevirm
    sns.regplot(x='capacity_numeric', y='price', data=df, scatter_kws={'color': 'blue'}, line_kws={'color': 'red'})
    plt.title('Regression Plot: Price vs Capacity')
    plt.xlabel('Capacity (GB)')
    plt.ylabel('Price')
    plt.grid(linestyle='--', alpha=0.7)
    plt.show()

get_data_analyz()

