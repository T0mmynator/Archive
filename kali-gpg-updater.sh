#!/bin/bash

# Eksik olan GPG anahtarı ID'si
KEYID="827C8569F2518CC677FECA1AED65462EC8D5E4C5"
KEYSERVER="keyserver.ubuntu.com"

echo "GPG anahtarı $KEYID alınıyor..."

# Anahtarı indir
gpg --keyserver hkp://$KEYSERVER --recv-keys $KEYID

# Anahtarı sisteme ekle
echo "Anahtar sisteme aktarılıyor..."
gpg --export $KEYID | sudo tee /etc/apt/trusted.gpg.d/kali.gpg > /dev/null

# apt update çalıştır
echo "Paket listesi güncelleniyor..."
sudo apt update

echo "İşlem tamamlandı."
