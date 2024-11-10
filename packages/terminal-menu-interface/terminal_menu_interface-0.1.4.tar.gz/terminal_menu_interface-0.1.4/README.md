## Menu

Este projeto é uma implementação de um menu interativo em Python, permitindo que os usuários naveguem por opções usando o teclado.

## 🚀 Começando

Essas instruções permitirão que você compreenda como utilizar a classe `Menu` para criar um menu interativo em seu aplicativo Python.

### 📋 Pré-requisitos

Para utilizar esta classe, você precisa do Python instalado em sua máquina, além de algumas bibliotecas:

* `tabulate`: Para formatar as opções do menu em uma tabela.
* `readchar`: Para capturar entradas do teclado.

### 🔧 Uso

1. **Importação da Classe**

   Primeiro, importe a classe `Menu` no seu código:

   ```python
   from terminal_manu.common import Menu
   ```

2. **Instância da Classe**

   Crie uma instância da classe `Menu`. Você pode definir se deseja inserir o índice da opção selecionada na chamada da função e se o menu deve terminar após uma opção ser selecionada.

   ```python
   menu = Menu(insert_index=True, end_with_select=True)
   ```

3. **Definição de Opções de Menu**

   Use o decorador `@menu.show()` para registrar funções como opções no menu. O nome da função será o texto que aparecerá para o usuário.

   ```python
   @menu.show()
   def opcao1():
       print("Você selecionou a Opção 1!")

   @menu.show()
   def opcao2():
       print("Você selecionou a Opção 2!")
   ```

4. **Início do Menu**

   Para iniciar o menu, chame o método `start()` na instância do menu:

   ```python
   menu.start()
   ```

   Durante a execução, os usuários poderão navegar pelas opções usando as teclas `W` (cima), `S` (baixo), `A` (esquerda), `D` (direita) e `Enter` para selecionar uma opção. A tecla `Q` é usada para sair do menu.

5. **Lista de opções**

   Para utilizar o código como um seletor de opções cujos valores não são funções, pode ser usado o método 'options_selection'. A forma de uso é bem simples:

   ```python
   from terminal_menu.common import Menu

   valor_selecionado = Menu().options_selection(['opcao1','opcao2'])
   ```
   A função irá retornar o valor selecionado pelo menu e irá encerrar imediatamente o menu de seleção

## ⚙️ Interação com o Menu

- **Navegação**: Os usuários podem usar as teclas `W` e `S` para mover-se para cima e para baixo entre as opções do menu.
- **Seleção**: Ao pressionar `Enter`, a função associada à opção selecionada será executada.
- **Sair**: Pressione `Q` para sair do menu.

## 🛠️ Construído com

Mencione as ferramentas que você usou para criar seu projeto.

* [Python](https://www.python.org/) - A linguagem de programação usada
* [tabulate](https://pypi.org/project/tabulate/) - Usada para formatar tabelas
* [readchar](https://pypi.org/project/readchar/) - Usada para ler entradas do teclado
