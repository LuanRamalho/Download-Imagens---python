import os
import requests
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox
import re  # Biblioteca para manipulação de expressões regulares


def sanitize_filename(filename):
    """
    Remove caracteres inválidos para nomes de arquivos.
    """
    filename = re.sub(r'[\\/*?:"<>|]', "_", filename)  # Substitui caracteres inválidos por "_"
    filename = filename.split("?")[0]  # Remove parâmetros da URL, se houver
    return filename


def get_extension_from_content_type(content_type):
    """
    Retorna a extensão do arquivo com base no tipo de conteúdo.
    """
    content_type_to_extension = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "image/gif": ".gif",
        "image/bmp": ".bmp",
        "image/tiff": ".tiff",
    }
    return content_type_to_extension.get(content_type, "")


def download_image():
    # Obtém o URL e o caminho do diretório
    url = url_entry.get()
    save_directory = filedialog.askdirectory(title="Selecione o Diretório para Salvar a Imagem")
    
    if not url:
        messagebox.showerror("Erro", "Por favor, insira um link válido.")
        return
    
    if not save_directory:
        messagebox.showerror("Erro", "Por favor, selecione um diretório para salvar a imagem.")
        return
    
    try:
        # Faz o download da imagem
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Obtém o tipo de conteúdo do cabeçalho HTTP
        content_type = response.headers.get("Content-Type", "")
        file_extension = get_extension_from_content_type(content_type)
        
        # Determina o nome do arquivo e o limpa
        filename = os.path.basename(url)
        filename = sanitize_filename(filename)
        
        # Garante que o arquivo tenha a extensão correta
        if not filename.endswith(file_extension):
            filename += file_extension
        
        # Define um nome padrão se o nome estiver vazio
        if not filename:
            filename = f"imagem_baixada{file_extension}"
        
        filepath = os.path.join(save_directory, filename)
        
        # Salva o arquivo
        with open(filepath, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        
        messagebox.showinfo("Sucesso", f"Imagem salva com sucesso em:\n{filepath}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Não foi possível baixar a imagem.\nErro: {e}")


# Configuração da janela principal
root = Tk()
root.title("Downloader de Imagens")
root.geometry("500x200")
root.resizable(False, False)
root.configure(bg="#b3d9ff")  # Fundo azul claro

# Rótulo e entrada para URL
url_label = Label(root, text="Insira o link da imagem:", bg="#b3d9ff", font=("Arial", 12, "bold"))
url_label.pack(pady=10)

url_entry = Entry(root, width=50, font=("Arial", 12))
url_entry.pack(pady=5)

# Botão para baixar a imagem
download_button = Button(root, text="Baixar Imagem", command=download_image, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
download_button.pack(pady=20)

# Inicia o loop da interface gráfica
root.mainloop()
