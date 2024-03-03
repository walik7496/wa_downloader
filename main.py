import tkinter as tk
import requests
from bs4 import BeautifulSoup
import threading
import os
from urllib.parse import urljoin, urlparse

class WebArchiveDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Archive Downloader")

        self.url_label = tk.Label(root, text="Enter URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack()

        self.download_button = tk.Button(root, text="Download", command=self.download_site)
        self.download_button.pack()

        self.status_label = tk.Label(root, text="Status:")
        self.status_label.pack()

        self.status_text = tk.Text(root, height=10, width=50)
        self.status_text.pack()

    def download_site(self):
        url = self.url_entry.get()
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url

        self.status_text.delete('1.0', tk.END)
        self.status_text.insert(tk.END, "Downloading site...\n")

        # Start a new thread to prevent GUI freeze
        threading.Thread(target=self.download_thread, args=(url,)).start()

    def download_thread(self, url):
        try:
            response = requests.get("https://web.archive.org/save/" + url)
            if response.status_code == 200:
                self.status_text.insert(tk.END, "Site downloaded successfully!\n")

                # Збереження HTML-файлу
                html_content = response.text
                with open("index.html", "w", encoding="utf-8") as html_file:
                    html_file.write(html_content)

                # Збереження інших ресурсів
                self.save_resources(response.text, url)

                self.status_text.insert(tk.END, "Files saved successfully!\n")
            else:
                self.status_text.insert(tk.END, "Failed to download site. Status code: {}\n".format(response.status_code))
        except Exception as e:
            self.status_text.insert(tk.END, "Error: {}\n".format(str(e)))

    def save_resources(self, html_content, base_url):
        soup = BeautifulSoup(html_content, 'html.parser')
        for tag in soup.find_all(['link', 'script', 'img']):
            if tag.get('src'):
                resource_url = urljoin(base_url, tag['src'])
                self.download_resource(resource_url)
            if tag.get('href'):
                resource_url = urljoin(base_url, tag['href'])
                self.download_resource(resource_url)

    def download_resource(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Отримуємо шлях до поточної директорії
                current_dir = os.getcwd()
                # Отримуємо шлях до директорії, в яку зберігатимемо ресурс
                resource_dir = os.path.join(current_dir, "resources")
                # Перевіряємо, чи існує директорія, якщо ні - створюємо її
                if not os.path.exists(resource_dir):
                    os.makedirs(resource_dir)

                # Отримуємо ім'я файлу з URL
                filename = os.path.basename(urlparse(url).path)
                # Зберігаємо ресурс
                with open(os.path.join(resource_dir, filename), 'wb') as f:
                    f.write(response.content)
        except Exception as e:
            self.status_text.insert(tk.END, "Error downloading resource {}: {}\n".format(url, str(e)))

if __name__ == "__main__":
    root = tk.Tk()
    app = WebArchiveDownloader(root)
    root.mainloop()
