import os
import google.generativeai as genai
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
import requests


class GeminiVideoApp(App):
    def build(self):
        self.api_key = ""
        self.image_path = None

        main_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # API Key
        main_layout.add_widget(Label(text="API Key Gemini:"))
        self.api_input = TextInput(hint_text="Masukkan API Key", multiline=False, password=True)
        main_layout.add_widget(self.api_input)

        # Prompt
        main_layout.add_widget(Label(text="Prompt:"))
        self.prompt_input = TextInput(hint_text="Tulis prompt video...", multiline=True)
        main_layout.add_widget(self.prompt_input)

        # Rasio
        main_layout.add_widget(Label(text="Pilih Rasio:"))
        self.ratio_spinner = Spinner(text="16:9", values=("16:9", "9:16", "1:1"))
        main_layout.add_widget(self.ratio_spinner)

        # Output Format
        main_layout.add_widget(Label(text="Pilih Output Format:"))
        self.format_spinner = Spinner(text="MP4", values=("MP4", "GIF", "MOV"))
        main_layout.add_widget(self.format_spinner)

        # Voice Language
        main_layout.add_widget(Label(text="Bahasa Suara:"))
        self.lang_spinner = Spinner(text="Indonesia", values=("Indonesia", "English"))
        main_layout.add_widget(self.lang_spinner)

        # Voice Gender
        main_layout.add_widget(Label(text="Gender Suara:"))
        self.voice_spinner = Spinner(text="Laki-laki", values=("Laki-laki", "Perempuan"))
        main_layout.add_widget(self.voice_spinner)

        # Character Consistency
        main_layout.add_widget(Label(text="Konsistensi Karakter:"))
        self.character_spinner = Spinner(text="None", values=("None", "Deskripsi Teks", "Gambar Referensi"))
        self.character_spinner.bind(text=self.on_character_mode)
        main_layout.add_widget(self.character_spinner)

        # Character input (dinamis)
        self.character_input = TextInput(hint_text="Deskripsi karakter...", multiline=True)
        self.character_input.opacity = 0
        self.character_input.disabled = True
        main_layout.add_widget(self.character_input)

        # Generate Button
        self.generate_btn = Button(text="Generate Video", size_hint=(1, 0.2))
        self.generate_btn.bind(on_press=self.generate_video)
        main_layout.add_widget(self.generate_btn)

        return main_layout

    def on_character_mode(self, spinner, text):
        if text == "Deskripsi Teks":
            self.character_input.opacity = 1
            self.character_input.disabled = False
        else:
            self.character_input.opacity = 0
            self.character_input.disabled = True
            if text == "Gambar Referensi":
                self.open_file_chooser()

    def open_file_chooser(self):
        filechooser = FileChooserIconView()
        popup = Popup(title="Pilih Gambar Referensi", content=filechooser, size_hint=(0.9, 0.9))

        def select_file(instance, selection):
            if selection:
                self.image_path = selection[0]
                popup.dismiss()

        filechooser.bind(on_submit=select_file)
        popup.open()

    def generate_video(self, instance):
        api_key = self.api_input.text.strip()
        prompt = self.prompt_input.text.strip()
        ratio = self.ratio_spinner.text
        fmt = self.format_spinner.text.lower()
        lang = self.lang_spinner.text
        voice = self.voice_spinner.text
        character_mode = self.character_spinner.text

        # Setup Gemini API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-pro")

        # Extra karakter
        extra_info = ""
        if character_mode == "Deskripsi Teks":
            extra_info = f"Konsistensi karakter: {self.character_input.text.strip()}"
        elif character_mode == "Gambar Referensi" and self.image_path:
            extra_info = f"Konsistensi karakter dengan gambar referensi ({self.image_path})"

        # Gabungkan prompt
        full_prompt = f"""
        {prompt}
        Rasio: {ratio}
        Format Output: {fmt}
        Bahasa Suara: {lang}
        Gender: {voice}
        {extra_info}
        """

        try:
            # Kirim ke Gemini
            response = model.generate_content(full_prompt)

            # Ambil URL video (simulasi, biasanya ada link CDN)
            video_url = None
            if response and hasattr(response, "candidates"):
                text_response = response.candidates[0].content.parts[0].text
                print("Raw Response:", text_response)

                # Simulasi: cari link download dari response
                if "http" in text_response:
                    video_url = text_response.split()[0]

            if video_url:
                file_name = f"output.{fmt}"
                r = requests.get(video_url, stream=True)
                with open(file_name, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                msg = f"Video berhasil diunduh: {file_name}"
            else:
                msg = "Video berhasil dibuat, tapi link tidak ditemukan. Lihat console."

        except Exception as e:
            msg = f"Error: {str(e)}"

        popup = Popup(title="Status", content=Label(text=msg), size_hint=(0.6, 0.4))
        popup.open()


if __name__ == "__main__":
    GeminiVideoApp().run()
