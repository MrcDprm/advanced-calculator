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
- [x] Çok büyük/küçük sayılarda bilimsel gösterim (`1e+25`, `1e-12`)
- [x] Binlik ayırıcılı gösterim (`1,234,567`)
- [x] Örtük çarpma: `2(3)`, `(1+2)(3+4)`, `2π`

**2. Arayüz ve kullanılabilirlik**
- [x] Tkinter arayüzü (düğmeler, Enter/Esc kısayolları)
- [x] Windows hesap makinesi davranışı: sonuçtan sonra rakam yeni işlem başlatır, operatör sonucun üstüne devam eder; hatadan sonra ilk tuş hatayı temizler
- [x] Kutuya sadece geçerli karakterlerin yazılabilmesi; `=` tuşu ile hesaplama
- [x] Renkli ve modern düğmeler (rakam / operatör / eşittir ayrı renk), fareyle üzerine gelince renk değişimi
- [x] Yeniden boyutlandırılabilir pencere (düğmeler pencereyle büyür)
- [x] Açık / koyu tema
- [x] Sonucu kopyalama (Ctrl+C)

**3. Geçmiş ve bellek**
- [x] Arayüzde geçmiş paneli; tıklanan kayıt kutuya geri gelir
- [x] Geçmişi ve ayarları dosyaya kaydetme (program kapanınca kaybolmasın)
- [x] Bellek tuşları: `MC`, `MR`, `M+`, `M-`

**4. Bilimsel fonksiyonlar**
- [x] `%`, `±`, `1/x`, `x²`
- [x] `sin`, `cos`, `tan` (derece / radyan seçimi)
- [x] `log`, `ln`, `π`, `e`, `n!`, `abs`
- [x] Standart / bilimsel mod geçişi

**5. Kalite ve yayın**
- [x] Birim testleri (`unittest`)
- [ ] Ekran görüntüleri ve GIF
- [x] Uygulama ikonu, sürüm numarası ve "Hakkında" penceresi
- [ ] Düğme ipuçları (tooltip) ve README'de klavye kısayolları tablosu
- [ ] PyInstaller ile tek dosyalık `.exe`
- [ ] Inno Setup ile Windows kurulum sihirbazı (Başlat menüsü kısayolu, kaldırma desteği)
- [ ] GitHub Release üzerinden indirme bağlantısı

## Klavye Kısayolları

| Tuş | İşlev | Tuş | İşlev |
|---|---|---|---|
| `Enter` veya `=` | Hesapla | `Esc` | Temizle |
| `Backspace` / `Delete` | Sil (fonksiyon adları bütün olarak silinir) | `Ctrl+C` / `Ctrl+V` | Kopyala / yapıştır |
| `s` / `o` / `t` | sin / cos / tan | `F3` / `F4` | Derece / radyan |
| `l` / `n` | log / ln | `p` / `e` | π / e |
| `q` | x² | `r` | 1/x |
| `@` | √ | `F9` | ± |
| `\|` | \|x\| | `!` / `%` | Faktöriyel / yüzde |
| `Ctrl+L` / `Ctrl+R` | Belleği temizle / bellekten oku | `Ctrl+P` / `Ctrl+Q` | Belleğe ekle / bellekten çıkar |
| `Ctrl+H` | Geçmiş paneli | `Alt+1` / `Alt+2` | Standart / bilimsel mod |

## Proje Yapısı

```
advanced-calculator/
├── gui.py          # Tkinter arayüzü
├── main.py         # Konsol arayüzü
├── tokenizer.py    # İfadeyi parçalara (token) ayırır
├── evaluator.py    # Token'ları işlem önceliğine göre hesaplar
├── formatter.py    # Sonucu okunabilir biçimde gösterir
├── history.py      # İşlem geçmişini tutar
├── storage.py      # Geçmiş ve ayarları dosyaya kaydeder
├── tooltip.py      # Düğme ipuçları
├── app_info.py     # Uygulama adı, sürüm, kaynak dosya yolları
├── assets/         # Uygulama ikonu
└── tests/          # Birim testleri
```

## Ekran Görüntüleri
## Kullanılan Teknolojiler
- Python 3.12
- Tkinter (arayüz aşamasında)

## Kurulum ve Çalıştırma

Python 3.12 veya üstü gerekir; harici paket kullanılmaz.

```bash
python gui.py     # arayüz
python main.py    # konsol sürümü
```

### Testleri çalıştırma

```bash
python -m unittest -v
```

## Öğrendiklerim
## Gelecek Planları
