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
- [ ] Tkinter arayüzü
- [ ] Geçmişi dosyaya kaydetme
- [ ] Ek fonksiyonlar: `sin`, `cos`, `log`, `%`
- [ ] Arayüzde klavye kısayolları

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
