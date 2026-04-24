import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

class PreProcessor:
    """Classe responsável pelas regras de negócio da análise léxica."""

    @staticmethod
    def _extract_write_text(write_call: str) -> str:
        """Extrai o texto entre aspas de write("...") mantendo as aspas."""
        text_match = re.search(r'\(\s*(".*?")\s*\)', write_call)
        return text_match.group(1) if text_match else '""'

    @staticmethod
    def _get_identifier_index(identifier: str, identifier_table: dict) -> int:
        """Retorna o índice do identificador; cria um novo índice se não existir."""
        if identifier not in identifier_table:
            identifier_table[identifier] = len(identifier_table)
        return identifier_table[identifier]

    @staticmethod
    def _build_error_report(invalid_inputs: list[str]) -> str:
        """Monta o conteúdo do arquivo com os inputs fora das regras válidas."""
        lines = ["Inputs fora das regras de validação:", ""]
        lines.extend(f"{index}. {repr(token)}" for index, token in enumerate(invalid_inputs, 1))
        return "\n".join(lines)

    @staticmethod
    def process_content(content: str) -> tuple[str, list[str]]:
        """Aplica as regras léxicas e retorna o conteúdo tokenizado + entradas inválidas."""
        token_specification = [
            # Regra 1: write("texto") -> [write, token-fr, "texto"]
            # Deve vir antes de RESERVED_WORD para capturar a chamada completa.
            ('WRITE_TEXT', r'\bwrite\s*\(\s*"[^"\n]*"\s*\)'),

            # Regra 2: palavras reservadas -> [palavra]
            ('RESERVED_WORD', r'\b(?:start|var|read|if|then|write|end)\b'),

            # Regra 3: símbolos reservados -> [(], [)], [:], [;]
            ('RESERVED_SYM', r'[\(\)\:\;]'),

            # Regra 4: operadores lógicos AND, OR, NOT -> [OL, valor]
            ('LOGICAL', r'\b(?:AND|OR|NOT)\b'),

            # Regra 5: identificadores -> [id,indice] usando tabela dinâmica
            ('ID', r'[a-zA-Z][a-zA-Z0-9_]*'),

            # Regra 6: números inteiros -> [NU, valor]
            ('NUMBER', r'\d+'),

            # Regra 7: operadores relacionais <, >, = -> [OR, valor]
            ('RELATIONAL', r'[<>=]'),

            # Regra 8: operadores aritméticos +, -, *, / -> [Om, valor]
            ('ARITHMETIC', r'[\+\*\/\-]'),

            # Regra 9: espaços e quebras de linha são preservados no resultado
            ('WHITESPACE', r'\s+'),

            # Regra 10: qualquer caractere não mapeado é mantido como está
            ('MISMATCH', r'.'),
        ]
        tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

        result = []
        invalid_inputs = []
        identifier_table = {}

        for mo in re.finditer(tok_regex, content):
            kind = mo.lastgroup
            value = mo.group()

            if kind == 'WRITE_TEXT':
                text_value = PreProcessor._extract_write_text(value)
                result.append(f'[write, fr, {text_value}]')
            elif kind in ('RESERVED_WORD', 'RESERVED_SYM'):
                result.append(f"[{value}]")
            elif kind == 'LOGICAL':
                result.append(f"[OL, {value}]")
            elif kind == 'ID':
                identifier_index = PreProcessor._get_identifier_index(value, identifier_table)
                result.append(f"[id,{identifier_index}]")
            elif kind == 'NUMBER':
                result.append(f"[NU, {value}]")
            elif kind == 'RELATIONAL':
                result.append(f"[OR, {value}]")
            elif kind == 'ARITHMETIC':
                result.append(f"[Om, {value}]")
            elif kind == 'WHITESPACE':
                result.append(value)
            elif kind == 'MISMATCH':
                invalid_inputs.append(value)

        return "".join(result), invalid_inputs


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
            "2. Identificadores usam tabela dinâmica ➔ [id,indice]\n"
            "3. Dígitos ➔ [NU, valor]\n"
            "4. Operadores <, >, = ➔ [OR, valor]\n"
            "5. Operadores +, *, /, - ➔ [Om, valor]\n"
            "6. Operadores AND, OR, NOT ➔ [OL, valor]\n"
            '7. write("texto") ➔ [write, fr, "texto"]'
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
                
            processed_content, invalid_inputs = PreProcessor.process_content(content)
            
            dir_name = os.path.dirname(input_filepath)
            base_name = os.path.basename(input_filepath)
            name, ext = os.path.splitext(base_name)
            output_filepath = os.path.join(dir_name, f"{name}_analisado{ext}")
            
            with open(output_filepath, 'w', encoding='utf-8') as file:
                file.write(processed_content)

            error_filepath = os.path.join(dir_name, f"{name}_erros{ext}")
            if invalid_inputs:
                error_report = PreProcessor._build_error_report(invalid_inputs)
                with open(error_filepath, 'w', encoding='utf-8') as file:
                    file.write(error_report)
                success_message = (
                    "Arquivo processado com sucesso!\n\n"
                    f"Saída tokenizada:\n{output_filepath}\n\n"
                    f"Arquivo de erros:\n{error_filepath}"
                )
            else:
                success_message = (
                    "Arquivo processado com sucesso!\n\n"
                    f"Salvo em:\n{output_filepath}"
                )
                
            messagebox.showinfo(
                "Sucesso", 
                success_message
            )
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao processar o arquivo:\n{str(e)}")


def main():
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
