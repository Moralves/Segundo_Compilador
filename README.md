# Segundo Compilador — Guia Didático de Estudo

Este projeto implementa um **analisador léxico** com interface gráfica em Python.  
Na prática, ele lê um arquivo `.txt`, identifica lexemas e gera uma versão tokenizada do conteúdo.

---

## 1) O que você está estudando aqui (visão de Compiladores)

Em Compiladores, o fluxo clássico é:

1. **Análise Léxica**: transforma caracteres em tokens.
2. **Análise Sintática**: valida se os tokens formam sentenças da gramática.
3. **Análise Semântica**: valida significado (tipos, escopo, uso de variáveis).
4. **Geração de código** (em compiladores completos).

Este projeto cobre a **fase léxica**, que é a base das demais fases.

---

## 2) Como o programa funciona

Ao selecionar um arquivo `.txt`, o programa:

1. lê o conteúdo salvo em disco;
2. aplica regras léxicas com expressões regulares;
3. mantém tabela dinâmica para identificadores;
4. gera `nome_analisado.txt` com os tokens;
5. se houver entradas inválidas, gera `nome_erros.txt`.

Exemplo: `teste.txt` gera `teste_analisado.txt` e, se necessário, `teste_erros.txt`.

---

## 3) Regras atuais (na ordem do código)

As regras abaixo refletem exatamente `compilador.py`:

| Ordem | Regra | Padrão | Saída |
|---|---|---|---|
| 1 | `write("texto")` | `\bwrite\s*\(\s*"[^"\n]*"\s*\)` | `[write, fr, "texto"]` |
| 2 | Palavras reservadas | `start, var, read, if, then, write, end` | `[palavra]` |
| 3 | Símbolos reservados | `(` `)` `:` `;` | `[símbolo]` |
| 4 | Operadores lógicos | `AND, OR, NOT` | `[OL, valor]` |
| 5 | Identificadores | letra + (letra/dígito/`_`) | `[id,indice]` |
| 6 | Números inteiros | `\d+` | `[NU, valor]` |
| 7 | Operadores relacionais | `<` `>` `=` | `[OR, valor]` |
| 8 | Operadores aritméticos | `+` `-` `*` `/` | `[Om, valor]` |
| 9 | Espaços e quebras | `\s+` | preservados no arquivo tokenizado |
| 10 | Não mapeados (`MISMATCH`) | qualquer outro caractere | **não entra na saída tokenizada**; vai para lista de inválidos |

**Importante:** a regra de `write("...")` vem antes de `write` como palavra reservada para capturar a chamada completa.

---

## 4) Tabela dinâmica de identificadores (mini tabela de símbolos)

Quando aparece um identificador:

- se for a primeira vez, recebe um índice (`0, 1, 2...`);
- se repetir, reutiliza o mesmo índice.

Exemplo:

```txt
contador1 contador1 nome_usuario
```

Saída (resumo):

```txt
[id,0] [id,0] [id,1]
```

---

## 5) Tratamento de erros léxicos

Caracteres fora das regras (como `%`, `$`, `&`) são registrados em `*_erros.txt` no formato:

```txt
Inputs fora das regras de validação:

1. '%'
2. '$'
...
```

Isso ajuda a separar:

- o que foi reconhecido como token válido;
- o que precisa ser corrigido na entrada.

---

## 6) Exemplo rápido de tokenização

Entrada:

```txt
var contador1 : 10 ;
if ( contador1 > 5 ) AND NOT ( nome_usuario = Pedro ) then
    write("Pedro Moreira e Luiz Gustavo") ;
```

Transformações importantes:

- `var` -> `[var]`
- `contador1` -> `[id,0]`
- `10` -> `[NU, 10]`
- `>` -> `[OR, >]`
- `AND` -> `[OL, AND]`
- `write("Pedro Moreira e Luiz Gustavo")` -> `[write, fr, "Pedro Moreira e Luiz Gustavo"]`

---

## 7) Como executar

### Requisitos

- Python 3.x
- Tkinter (normalmente já vem no Python para Windows)

### Execução

No terminal, dentro da pasta do projeto:

```bash
python compilador.py
```

Depois, na janela:

1. clique em **Selecionar Arquivo .txt**;
2. escolha o arquivo de entrada;
3. o sistema salva o(s) arquivo(s) de saída na mesma pasta.

> Se o arquivo estiver vazio (0 bytes), o programa avisa para salvar o conteúdo antes de processar.

---

## 8) Estrutura do projeto

- `compilador.py` -> analisador léxico + interface gráfica
- `teste.txt` -> arquivo de exemplo
- `README.md` -> material didático

---

## 9) Limitações atuais (ótimas para estudo)

- não há analisador sintático;
- não há analisador semântico;
- apenas inteiros (`\d+`) são reconhecidos como número;
- string é reconhecida especificamente no formato `write("...")`;
- rótulo `[OR, valor]` para relacional pode confundir com o operador lógico `OR`.

---

## 10) Roteiro de estudo sugerido

1. Relacione cada regex com a classe de token correspondente.
2. Rode com entradas válidas e inválidas e compare `*_analisado.txt` vs `*_erros.txt`.
3. Observe a evolução da tabela de identificadores conforme os nomes se repetem.
4. Evolua o projeto com novos desafios: `<=`, `>=`, `!=`, números reais, análise sintática e semântica.

Esse fluxo conecta teoria de compiladores com prática de implementação.

