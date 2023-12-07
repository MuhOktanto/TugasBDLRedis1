import tkinter as tk
import redis

class ScoreCounterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Penghitung Skor")
        self.master.geometry("300x200")

        # Koneksi ke server Redis lokal
        self.redis_host = '127.0.0.1'
        self.redis_port = 6379
        self.redis_db = 0
        self.r = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=self.redis_db)

        # Label dan Entry untuk input nama pemain
        self.label_name = tk.Label(master, text="Nama Pemain:")
        self.label_name.pack()

        self.entry_name = tk.Entry(master)
        self.entry_name.pack()

        # Tombol untuk menambahkan skor
        self.add_score_button = tk.Button(master, text="Tambah Skor", command=self.add_score)
        self.add_score_button.pack()

        # Tombol untuk melihat skor
        self.show_score_button = tk.Button(master, text="Lihat Skor", command=self.show_score)
        self.show_score_button.pack()

        # Label untuk menampilkan skor
        self.label_score = tk.Label(master, text="")
        self.label_score.pack()

    def add_score(self):
        try:
            # Mendapatkan nama pemain dari Entry
            player_name = self.entry_name.get()
            score_key = f'score:{player_name}'

            # Menginkrementasi nilai skor menggunakan perintah INCR
            new_score = self.r.incr(score_key)

            # Menampilkan pesan sukses
            self.label_score.config(text=f"Skor untuk {player_name}: {new_score}")

        except Exception as e:
            # Menampilkan pesan error jika terjadi masalah
            self.label_score.config(text=f"Terjadi kesalahan: {e}")

    def show_score(self):
        try:
            # Mendapatkan nama pemain dari Entry
            player_name = self.entry_name.get()
            score_key = f'score:{player_name}'

            # Mengambil nilai skor dari Redis
            current_score = self.r.get(score_key)

            if current_score is not None:
                # Menampilkan skor
                self.label_score.config(text=f"Skor untuk {player_name}: {current_score.decode()}")
            else:
                # Menampilkan pesan jika pemain belum memiliki skor
                self.label_score.config(text=f"{player_name} belum memiliki skor.")

        except Exception as e:
            # Menampilkan pesan error jika terjadi masalah
            self.label_score.config(text=f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScoreCounterApp(root)
    root.mainloop()
