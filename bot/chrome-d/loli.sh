#!bin/bash

CHROME_VERSION=$(google-chrome --version | grep -oP "\d+\.\d+\.\d+" | cut -d '.' -f 1)
LATEST_DRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}")

# Eğer uyumlu sürüm bulunamazsa genel en son sürümü indir
if [ -z "$LATEST_DRIVER_VERSION" ]; then
    echo "Uygun bir ChromeDriver sürümü bulunamadı, genel en son sürüm indiriliyor."
    LATEST_DRIVER_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
fi

# ChromeDriver'ı indir, çıkart ve kur
wget -q "https://chromedriver.storage.googleapis.com/${LATEST_DRIVER_VERSION}/chromedriver_linux64.zip" -O chromedriver_linux64.zip
unzip -o chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
rm chromedriver_linux64.zip

# Yüklenen ChromeDriver sürümünü kontrol et
