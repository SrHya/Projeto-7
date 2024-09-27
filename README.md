# Projeto-7

# Assistente Virtual Isa - Easy Market BR

## Descrição do Projeto
A Assistente Virtual **Isa** é uma inteligência artificial projetada para analisar planilhas e fornecer insights detalhados de forma interativa. Isa foi desenvolvida com o propósito de facilitar a análise de dados complexos para empresas e indivíduos, utilizando uma interface web intuitiva que permite ao usuário fazer upload de arquivos, enviar mensagens de texto ou áudio, e receber respostas personalizadas.

## Funcionalidades
- **Análise de Planilhas**: O usuário pode enviar planilhas para a Isa, e a IA será capaz de interpretar os dados e responder a perguntas específicas, realizar cálculos como somas, médias, e fornecer insights sobre produtos mais vendidos, entre outros.
- **Chat interativo**: A interface inclui uma funcionalidade de chat que permite interação em tempo real. O usuário pode fazer perguntas por texto ou áudio, e a IA responderá com base nos dados fornecidos.
- **Login e Cadastro de Usuário**: A aplicação permite que os usuários criem contas e façam login, garantindo que as conversas e planilhas enviadas fiquem armazenadas e associadas a cada usuário.
- **Suporte para Vários Formatos de Arquivo**: Isa pode receber e processar arquivos como `.csv`, `.xlsx`, e outros formatos de planilhas populares.
- **Memória de Conversa**: A IA mantém o histórico de todas as interações realizadas durante uma sessão, permitindo a continuidade de análises e comparações entre diferentes planilhas.
- **Modo Claro/Escuro**: O usuário pode alternar entre os modos claro e escuro para personalizar a interface.
- **Respostas por Áudio**: Isa também responde em áudio, o que facilita a interação para usuários que preferem ouvir as respostas.

## Tecnologias Utilizadas
- **Flask**: Framework web utilizado para gerenciar as rotas e controlar as interações do frontend com o backend.
- **Python**: Linguagem principal do projeto, utilizada para a lógica de processamento de dados e integração com a API da OpenAI.
- **SQLAlchemy**: Utilizado para o gerenciamento de banco de dados e manipulação dos usuários.
- **OpenAI API**: Utilizada para alimentar a inteligência artificial Isa, permitindo a interação natural com o usuário.
- **Pandas**: Biblioteca de análise de dados em Python, usada para processar e analisar as planilhas enviadas pelos usuários.
- **HTML/CSS/JavaScript**: Tecnologias usadas para criar a interface web interativa e responsiva.
- **VSCode**: Ferramenta de desenvolvimento usada no projeto.

## Como Executar o Projeto

### Requisitos:
- Python 3.8+
- Pip (Gerenciador de pacotes do Python)
- Ambiente Virtual Python (opcional, mas recomendado)

### Passos para Rodar Localmente:

1. **Clone o repositório**:
   ```bash
   git clone x
   cd x
   
2. **Instale as dependências: No diretório raiz do projeto, execute**:
   
pip install -r requirements.txt

4. Configure as variáveis de ambiente: Crie um arquivo .env na raiz do projeto com as variáveis de ambiente necessárias. Por exemplo:

FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=sua-chave-secreta
OPENAI_API_KEY=sua-chave-api-openai

5.Acesse o projeto no navegador: Abra o navegador e vá até http://127.0.0.1:5000/ para acessar a interface da Assistente Virtual Isa.

Próximos Passos
O projeto ainda está em desenvolvimento e algumas funcionalidades futuras incluem:

Melhoria na interface para oferecer uma experiência ainda mais intuitiva.
Suporte a novos tipos de arquivos e uma análise mais detalhada dos dados.
Integração com outras APIs para oferecer relatórios ainda mais completos.
Contribuições
Se você deseja contribuir com o projeto, sinta-se à vontade para enviar pull requests ou abrir issues no repositório.

Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
