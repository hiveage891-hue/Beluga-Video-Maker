import customtkinter as ctk
import json
import os
import threading
import traceback
import sys
from tkinter import filedialog
from PIL import Image

# Import scripts
try:
    from scripts.desenhador import desenhar_conversa
    from scripts.editor_video import montar_video_final
except ImportError as e:
    with open("crashlog.txt", "w") as f:
        f.write(f"Import Error: {str(e)}\n{traceback.format_exc()}")
    sys.exit(1)


def log_crash(error_msg):
    with open("crashlog.txt", "a") as f:
        f.write(
            f"\n{'='*30}\nCRASH REPORT - {error_msg}\n{traceback.format_exc()}{'='*30}\n"
        )


class BelugaVideoMaker(ctk.CTk):
    def __init__(self):
        super().__init__()
        try:
            self.title("Beluga Video Maker")
            self.geometry("1100x850")
            self.messages = []
            self.full_hd_frames = []

            # Tabs Setup
            self.tabview = ctk.CTkTabview(self)
            self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

            self.tab_gen = self.tabview.add("General")
            self.tab_prev = self.tabview.add("Preview")

            self.setup_general_tab()
            self.setup_preview_tab()
        except Exception as e:
            log_crash("Error during Initialization")
            raise e

    def setup_general_tab(self):
        input_frame = ctk.CTkFrame(self.tab_gen)
        input_frame.pack(pady=10, padx=20, fill="x")

        self.ent_user = ctk.CTkEntry(input_frame, placeholder_text="Username")
        self.ent_user.grid(row=0, column=0, padx=10, pady=10)

        self.ent_avatar = ctk.CTkEntry(input_frame, placeholder_text="Avatar File")
        self.ent_avatar.grid(row=0, column=1, padx=10, pady=10)

        self.ent_time = ctk.CTkEntry(
            input_frame, placeholder_text="Time (e.g. 10:00 PM)"
        )
        self.ent_time.grid(row=1, column=0, padx=10, pady=10)

        self.ent_duration = ctk.CTkEntry(input_frame, placeholder_text="Duration (sec)")
        self.ent_duration.grid(row=1, column=1, padx=10, pady=10)

        self.check_conn = ctk.CTkCheckBox(input_frame, text="Connected Message (__)")
        self.check_conn.grid(row=2, column=0, pady=10)

        self.txt_msg = ctk.CTkTextbox(self.tab_gen, height=120)
        self.txt_msg.pack(pady=10, padx=20, fill="x")

        btn_frame = ctk.CTkFrame(self.tab_gen)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Add Message", command=self.add_message).pack(
            side="left", padx=5
        )
        ctk.CTkButton(
            btn_frame, text="Load JSON", fg_color="gray", command=self.load_json
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            btn_frame, text="Save JSON", fg_color="gray", command=self.save_json
        ).pack(side="left", padx=5)

        self.lbl_status = ctk.CTkLabel(self.tab_gen, text="Messages in queue: 0")
        self.lbl_status.pack()

        self.btn_render = ctk.CTkButton(
            self.tab_gen,
            text="RENDER VIDEO",
            fg_color="#2ecc71",
            command=self.start_render,
        )
        self.btn_render.pack(pady=20)

    def setup_preview_tab(self):
        # FIX: Cria um container preto com tamanho fixo para centralizar o preview.
        # Isso evitará que a imagem "dance" na tela e fique distorcida.
        self.preview_container = ctk.CTkFrame(
            self.tab_prev, width=900, height=550, fg_color="black"
        )
        self.preview_container.pack(pady=20, padx=20, expand=True)
        # Impede que o frame mude de tamanho para caber o label.
        self.preview_container.pack_propagate(False)

        self.prev_label = ctk.CTkLabel(
            self.preview_container, text="No preview available", text_color="gray"
        )
        self.prev_label.pack(expand=True, fill="both")

    def add_message(self):
        try:
            text = self.txt_msg.get("0.0", "end").strip()
            msg = {
                "usuario": self.ent_user.get() or "User",
                "texto": f"__{text}" if self.check_conn.get() else text,
                "avatar": self.ent_avatar.get() or "",
                "tempo": float(self.ent_duration.get() or 2.0),
                "time": self.ent_time.get() or "12:00",
            }
            self.messages.append(msg)
            self.update_ui()
        except Exception:
            log_crash("Error adding message")

    def load_json(self):
        try:
            path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            if path:
                with open(path, "r") as f:
                    self.messages = json.load(f)
                self.update_ui()
        except Exception:
            log_crash("Error loading JSON")

    def save_json(self):
        try:
            path = filedialog.asksaveasfilename(defaultextension=".json")
            if path:
                with open(path, "w") as f:
                    json.dump(self.messages, f, indent=4)
        except Exception:
            log_crash("Error saving JSON")

    def update_ui(self):
        try:
            self.lbl_status.configure(text=f"Messages in queue: {len(self.messages)}")
            # Gera os frames ORIGINAIS (Full HD) chamando seu desenhador.py
            # Sem redimensionar aqui para não estragar o vídeo final
            self.full_hd_frames = desenhar_conversa(self.messages)
            if self.full_hd_frames:
                # FIX: Redimensionamento inteligente mantendo a proporção para preview.
                # Pega uma CÓPIA para o preview não afetar o original Full HD.
                img_to_resize = self.full_hd_frames[-1].copy()

                # Tamanho alvo para o preview dentro da janela.
                target_w = 850
                target_h = 480

                # Redimensionamento inteligente mantendo a proporção.
                w, h = img_to_resize.size
                ratio = min(target_w / w, target_h / h)
                new_w = int(w * ratio)
                new_h = int(h * ratio)

                # Redimensiona a cópia com alta qualidade.
                img_resized = img_to_resize.resize(
                    (new_w, new_h), Image.Resampling.LANCZOS
                )

                # Cria a CTkImage com o tamanho redimensionado correto.
                ctk_img = ctk.CTkImage(
                    light_image=img_resized, dark_image=img_resized, size=(new_w, new_h)
                )

                self.prev_label.configure(image=ctk_img, text="")
        except Exception:
            log_crash("Error updating UI")

    def start_render(self):
        self.btn_render.configure(state="disabled", text="Processing...")
        threading.Thread(target=self.render_thread).start()

    def render_thread(self):
        try:
            # GARANTE que estamos usando os frames em 1920x1080 do desenhador.py.
            full_res_frames = desenhar_conversa(self.messages)
            durations = [m["tempo"] for m in self.messages]
            montar_video_final(full_res_frames, durations, "output/final_video.mp4")
            self.btn_render.configure(state="normal", text="VIDEO GENERATED!")
        except Exception:
            log_crash("Error during rendering")
            self.btn_render.configure(state="normal", text="ERROR (Check Log)")


if __name__ == "__main__":
    try:
        app = BelugaVideoMaker()
        app.mainloop()
    except Exception:
        log_crash("Critical failure")
