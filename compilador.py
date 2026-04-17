import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

class PreProcessor:
    """Classe responsável pelas regras de negócio da análise léxica."""

    @staticmethod
    def process_content(content: str) -> str:
        """
        Aplica as regras de substituição léxica ao conteúdo fornecido.
        """
        token_specification = [
            ('RESERVED_WORD',  r'\b(?:start|var|read|if|then|write|end)\b'), 
            ('RESERVED_SYM',   r'[\(\)\:\;]'),
            ('LOGICAL',        r'\b(?:AND|OR|NOT)\b'),
            ('ID',             r'[a-zA-Z]+'),
            ('NUMBER',         r'\d+'),
            ('RELATIONAL',     r'[<>=]'),
            ('ARITHMETIC',     r'[\+\*\/\-]'),
            ('WHITESPACE',     r'\s+'),
            ('MISMATCH',       r'.'),
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        
        result = []
        for mo in re.finditer(tok_regex, content):
            kind = mo.lastgroup
            value = mo.group()
            
            if kind == 'RESERVED_WORD' or kind == 'RESERVED_SYM':
                result.append(f"[{value}]")
            elif kind == 'LOGICAL':
                result.append("[OL]")
            elif kind == 'ID':
                result.append("[id]")
            elif kind == 'NUMBER':
                result.append("[Nu]")
            elif kind == 'RELATIONAL':
                result.append("[Or]")
            elif kind == 'ARITHMETIC':
                result.append("[Om]")
            elif kind == 'WHITESPACE':
                result.append(value)
            elif kind == 'MISMATCH':
                result.append(value)
                
        return "".join(result)


class CompilerGUI:
    """Classe responsável pela interface gráfica com o usuário."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.root.title("Compilador - Analisador Léxico")
        self.root.geometry("550x350")
        self.root.configure(bg="#f4f4f4")
        self.root.eval('tk::PlaceWindow . center')

    def create_widgets(self):
        frame = tk.Frame(self.root, bg="#f4f4f4")
        frame.pack(expand=True)

        titulo = tk.Label(
            frame, 
            text="Analisador Léxico: Tokenizador", 
            font=("Segoe UI", 14, "bold"), 
            bg="#f4f4f4"
        )
        titulo.pack(pady=(0, 10))

        regras_texto = (
            "Regras aplicadas ao arquivo:\n\n"
            "1. start, var, read, if, (, ), :, ;, then, write, end ➔ [palavra]\n"
            "2. Letras ou sequências de letras ➔ [id]\n"
            "3. Dígitos ➔ [Nu]\n"
            "4. Operadores <, >, = ➔ [Or]\n"
            "5. Operadores +, *, /, - ➔ [Om]\n"
            "6. Operadores AND, OR, NOT ➔ [OL]"
        )
        regras = tk.Label(
            frame, 
            text=regras_texto, 
            font=("Segoe UI", 10), 
            bg="#f4f4f4", 
            justify="left"
        )
        regras.pack(pady=(0, 20))

        btn_processar = tk.Button(
            frame, 
            text="Selecionar Arquivo .txt", 
            command=self.handle_file_selection, 
            bg="#0078D7", 
            fg="white", 
            font=("Segoe UI", 11, "bold"), 
            padx=15, 
            pady=8, 
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_processar.pack()

    def handle_file_selection(self):
        input_filepath = filedialog.askopenfilename(
            title="Selecione o arquivo de entrada",
            filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")]
        )
        
        if not input_filepath:
            return
            
        try:
            if os.path.getsize(input_filepath) == 0:
                messagebox.showwarning(
                    "Aviso - Arquivo Vazio", 
                    "O arquivo selecionado está completamente em branco (0 bytes) no disco!\n\n"
                    "Se você acabou de digitar texto no seu editor, você precisa SALVAR (Ctrl + S) "
                    "o arquivo antes de selecioná-lo aqui. O compilador só consegue ler o que está salvo."
                )
                return

            with open(input_filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                
            processed_content = PreProcessor.process_content(content)
            
            dir_name = os.path.dirname(input_filepath)
            base_name = os.path.basename(input_filepath)
            name, ext = os.path.splitext(base_name)
            output_filepath = os.path.join(dir_name, f"{name}_analisado{ext}")
            
            with open(output_filepath, 'w', encoding='utf-8') as file:
                file.write(processed_content)
                
            messagebox.showinfo(
                "Sucesso", 
                f"Arquivo processado com sucesso!\n\nSalvo em:\n{output_filepath}"
            )
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao processar o arquivo:\n{str(e)}")


def main():
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
