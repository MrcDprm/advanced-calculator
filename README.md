# Advanced Calculator

Python ile yazılmış, önce konsolda sonra Tkinter arayüzüyle çalışan gelişmiş bir hesap makinesi. İfadeler `eval()` kullanılmadan, sıfırdan yazılmış bir ayrıştırıcı (parser) ile hesaplanır.

> 🚧 Geliştirme aşamasında.

## Özellikler

### MVP (konsol sürümü)
- [x] Kullanıcıdan matematiksel ifade alma (ör. `3 + 4 * 2`)
- [x] Dört işlem: `+`, `-`, `*`, `/`
- [x] İşlem önceliği ve parantezli ifadeler (ör. `(3 + 4) * 2`)
- [x] Üs alma (`^`) ve karekök (`sqrt(16)`)
- [x] Hata yönetimi: sıfıra bölme, geçersiz girdi, kapanmamış parantez
- [x] İşlem geçmişi (`gecmis` komutu)
- [x] Programdan çıkış (`cikis` komutu)

### Sonra eklenecekler

**1. Hesaplama doğruluğu ve gösterim**
- [ ] Çok büyük/küçük sayılarda bilimsel gösterim (`1e+25`, `1e-12`)
- [ ] Binlik ayırıcılı gösterim (`1,234,567`)
- [ ] Örtük çarpma: `2(3)`, `(1+2)(3+4)`, `2π`

**2. Arayüz ve kullanılabilirlik**
- [x] Tkinter arayüzü (düğmeler, Enter/Esc kısayolları)
- [ ] Windows hesap makinesi davranışı: sonuçtan sonra rakam yeni işlem başlatır, operatör sonucun üstüne devam eder; hatadan sonra ilk tuş hatayı temizler
- [ ] Kutuya sadece geçerli karakterlerin yazılabilmesi; `=` tuşu ile hesaplama
- [ ] Renkli ve modern düğmeler (rakam / operatör / eşittir ayrı renk), fareyle üzerine gelince renk değişimi
- [ ] Yeniden boyutlandırılabilir pencere (düğmeler pencereyle büyür)
- [ ] Açık / koyu tema
- [ ] Sonucu kopyalama (Ctrl+C)

**3. Geçmiş ve bellek**
- [ ] Arayüzde geçmiş paneli; tıklanan kayıt kutuya geri gelir
- [ ] Geçmişi ve ayarları dosyaya kaydetme (program kapanınca kaybolmasın)
- [ ] Bellek tuşları: `MC`, `MR`, `M+`, `M-`

**4. Bilimsel fonksiyonlar**
- [ ] `%`, `±`, `1/x`, `x²`
- [ ] `sin`, `cos`, `tan` (derece / radyan seçimi)
- [ ] `log`, `ln`, `π`, `e`, `n!`, `abs`
- [ ] Standart / bilimsel mod geçişi

**5. Kalite ve yayın**
- [ ] Birim testleri (`unittest`)
- [ ] Ekran görüntüleri ve GIF
- [ ] PyInstaller ile Windows `.exe` sürümü (GitHub Release)

## Proje Yapısı

```
advanced-calculator/
├── main.py         # Programın giriş noktası, konsol döngüsü
├── tokenizer.py    # İfadeyi parçalara (token) ayırır
├── evaluator.py    # Token'ları işlem önceliğine göre hesaplar
└── history.py      # İşlem geçmişini tutar
```

## Ekran Görüntüleri
## Kullanılan Teknolojiler
- Python 3.12
- Tkinter (arayüz aşamasında)

## Kurulum ve Çalıştırma
## Öğrendiklerim
## Gelecek Planları
