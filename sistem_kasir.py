class Produk:
    # Class attribute untuk menghitung total jenis produk yang dibuat
    jumlah_produk = 0

    def __init__(self, kode, nama, harga, stok):
        # Encapsulation menggunakan atribut private (__)
        self.__kode = kode
        self.__nama = nama
        self.__harga = harga
        self.__stok = stok
        Produk.jumlah_produk += 1

    # Property (Getter) untuk mengakses atribut private
    @property
    def kode(self):
        return self.__kode

    @property
    def nama(self):
        return self.__nama

    @property
    def harga(self):
        return self.__harga

    # Setter untuk mengubah harga dengan validasi
    @harga.setter
    def harga(self, harga_baru):
        if harga_baru > 0:
            self.__harga = harga_baru
        else:
            print("Harga harus lebih dari 0!")

    @property
    def stok(self):
        return self.__stok

    # Setter untuk mengubah stok dengan validasi
    @stok.setter
    def stok(self, stok_baru):
        if stok_baru >= 0:
            self.__stok = stok_baru
        else:
            print("Stok tidak boleh negatif!")

    # Instance method
    def info_produk(self):
        return f"[{self.__kode}] {self.__nama} - {TransaksiKasir.format_rupiah(self.__harga)} (Stok: {self.__stok})"

    # Class method
    @classmethod
    def total_jenis_produk(cls):
        return cls.jumlah_produk


class TransaksiKasir:
    pajak_ppn = 0.11  # Class attribute (11%)

    def __init__(self, nama_kasir):
        self.__nama_kasir = nama_kasir
        self.__keranjang = []  # Menyimpan dictionary {'produk': obj_produk, 'qty': int}

    @property
    def nama_kasir(self):
        return self.__nama_kasir

    # Instance method untuk menambah barang ke keranjang
    def tambah_ke_keranjang(self, produk, qty):
        if qty <= 0:
            print("Jumlah beli harus minimal 1.")
            return
        if produk.stok >= qty:
            produk.stok -= qty  # Mengurangi stok menggunakan setter
            self.__keranjang.append({"produk": produk, "qty": qty})
            print(f"Berhasil menambahkan {qty}x {produk.nama} ke keranjang.")
        else:
            print(f"Stok {produk.nama} tidak mencukupi! Sisa stok: {produk.stok}")

    def hitung_subtotal(self):
        return sum(item["produk"].harga * item["qty"] for item in self.__keranjang)

    def cetak_struk(self, uang_bayar):
        subtotal = self.hitung_subtotal()
        nominal_pajak = subtotal * TransaksiKasir.pajak_ppn
        total_akhir = subtotal + nominal_pajak

        if uang_bayar < total_akhir:
            print(f"\nUang pembayaran kurang! Total yang harus dibayar: {self.format_rupiah(total_akhir)}")
            return False

        kembalian = uang_bayar - total_akhir

        print("\n" + "=" * 42)
        print("           STRUK PEMBAYARAN")
        print(f"Kasir: {self.__nama_kasir}")
        print("=" * 42)
        for item in self.__keranjang:
            p = item["produk"]
            q = item["qty"]
            total_item = p.harga * q
            print(f"{p.nama} ({q}x @ {self.format_rupiah(p.harga)})")
            print(f"   Subtotal Item : {self.format_rupiah(total_item)}")
        print("-" * 42)
        print(f"Subtotal         : {self.format_rupiah(subtotal)}")
        print(f"PPN (11%)        : {self.format_rupiah(nominal_pajak)}")
        print(f"Total Bayar      : {self.format_rupiah(total_akhir)}")
        print(f"Tunai            : {self.format_rupiah(uang_bayar)}")
        print(f"Kembalian        : {self.format_rupiah(kembalian)}")
        print("=" * 42)
        print("      Terima Kasih Telah Berbelanja!")
        print("=" * 42)
        return True

    # Class method untuk mengubah persentase pajak
    @classmethod
    def ubah_pajak(cls, pajak_baru):
        cls.pajak_ppn = pajak_baru

    # Static method untuk utilitas pemformatan mata uang
    @staticmethod
    def format_rupiah(angka):
        return f"Rp {angka:,.0f}".replace(",", ".")


# ================= PROGRAM UTAMA (INPUT TERMINAL) =================
def main():
    # Membuat object dari class Produk
    daftar_produk = [
        Produk("P01", "Kopi Susu Gula Aren", 18000, 20),
        Produk("P02", "Roti Bakar Cokelat", 15000, 15),
        Produk("P03", "Mie Goreng Spesial", 22000, 10),
        Produk("P04", "Es Teh Manis", 8000, 30),
    ]

    print("=== SISTEM KASIR SEDERHANA ===")
    nama_kasir = input("Masukkan nama kasir: ")
    
    # Membuat object dari class TransaksiKasir
    kasir = TransaksiKasir(nama_kasir)

    while True:
        print("\n--- MENU UTAMA ---")
        print("1. Lihat Daftar Produk")
        print("2. Tambah Barang ke Keranjang")
        print("3. Tambah Produk Baru ke Toko")
        print("4. Checkout & Cetak Struk")
        print("5. Keluar")

        pilihan = input("Pilih menu (1-5): ")

        if pilihan == "1":
            print(f"\n--- DAFTAR PRODUK (Total {Produk.total_jenis_produk()} Jenis) ---")
            for p in daftar_produk:
                print(p.info_produk())

        elif pilihan == "2":
            kode_cari = input("Masukkan kode produk (contoh: P01): ").upper()
            produk_ditemukan = next((p for p in daftar_produk if p.kode == kode_cari), None)
            
            if produk_ditemukan:
                try:
                    qty = int(input(f"Masukkan jumlah beli ({produk_ditemukan.nama}): "))
                    kasir.tambah_ke_keranjang(produk_ditemukan, qty)
                except ValueError:
                    print("Input jumlah harus berupa angka!")
            else:
                print("Kode produk tidak ditemukan.")

        elif pilihan == "3":
            kode = input("Kode produk baru: ").upper()
            nama = input("Nama produk: ")
            try:
                harga = int(input("Harga produk: "))
                stok = int(input("Stok awal: "))
                produk_baru = Produk(kode, nama, harga, stok)
                daftar_produk.append(produk_baru)
                print("Produk baru berhasil ditambahkan!")
            except ValueError:
                print("Harga dan stok harus berupa angka!")

        elif pilihan == "4":
            if kasir.hitung_subtotal() == 0:
                print("Keranjang masih kosong!")
                continue

            total_tagihan = kasir.hitung_subtotal() * (1 + TransaksiKasir.pajak_ppn)
            print(f"\nTotal tagihan (termasuk PPN 11%): {TransaksiKasir.format_rupiah(total_tagihan)}")
            
            try:
                bayar = int(input("Masukkan nominal uang pembayaran: "))
                if kasir.cetak_struk(bayar):
                    # Reset keranjang untuk transaksi pelanggan berikutnya
                    kasir = TransaksiKasir(nama_kasir)
            except ValueError:
                print("Nominal uang harus berupa angka!")

        elif pilihan == "5":
            print("Program selesai. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid, silakan pilih 1-5.")


if __name__ == "__main__":
    main()
