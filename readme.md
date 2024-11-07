# Automação de Interações no TikTok com Selenium
===========================================================<br>

Este script Python automatiza interações no TikTok usando Selenium, incluindo busca por um tema específico, curtir, seguir e comentar em vídeos. O objetivo é facilitar a interação com vídeos relacionados a um tema de interesse de forma programática.

# Funcionalidades
===========================================================<br>

1 - Busca de Tema: O script inicia uma busca no TikTok com o tema fornecido.<br>
2 - Curtir Vídeos: Se o vídeo ainda não foi curtido, o script realiza essa ação.<br>
3 - Seguir Usuário: Caso o usuário do vídeo não esteja sendo seguido, o script realiza o "seguir".<br>
4 - Adicionar Comentários: Escolhe um comentário aleatório de uma lista e publica no vídeo.<br>
5 - Controle de Tentativas: Realiza várias tentativas para ações como adicionar comentários, caso falhem inicialmente.<br>

# Pré-Requisitos
===========================================================<br>

Python 3.x: Instale a versão mais recente do Python em python.org.<br>
Selenium: Instale o pacote Selenium com o comando:<br>
bash<br>
Copiar código<br>
pip install selenium<br>
Chromedriver: Baixe o ChromeDriver na versão correspondente à versão do seu navegador Chrome em ChromeDriver - WebDriver for Chrome. Coloque o executável em um local conhecido e atualize o caminho no código (service = Service('Caminho/para/seu/chromedriver')).<br>
Perfil de Usuário do Chrome: O script usa um perfil de usuário específico do Chrome para evitar login repetido. Verifique o caminho do perfil (user-data-dir) e altere conforme necessário.<br>


# Configuração
===========================================================<br>

Atualize o caminho do ChromeDriver e do perfil de usuário no script:<br>
python<br>
Copiar código<br>
# Caminho para o chromedriver<br>
service = Service('C:/Users/User/Desktop/chromedriver-win64/chromedriver.exe')<br>

# Configuração do perfil de usuário do Chrome
options.add_argument(r"user-data-dir=C:/Users/User/AppData/Local/Google/Chrome/User Data")<br>

# Execução do Script<br>
===========================================================<br>

Para executar a automação:<br>
Abra o terminal ou prompt de comando.<br>
Navegue até o diretório onde o script está salvo.<br>
Execute o script com o comando:<br>
bash<br>
Copiar código<br>
python nome_do_script.py<br>
O script começará a abrir o navegador, fazer uma busca no TikTok pelo tema fornecido e realizar as interações automaticamente.<br>

# Estrutura do Código<br>
===========================================================<br>

Funções<br>
iniciar_navegador: Configura e abre uma instância do navegador com as opções especificadas.<br>
automacao_tiktok: Função principal que realiza as interações no TikTok, incluindo busca, curtir, seguir e comentar em vídeos.

# Comportamento do Script<br>
O script executa um loop contínuo que:<br>

Acessa o site do TikTok.<br>
Realiza uma busca com o tema especificado.<br>
Seleciona um vídeo aleatório da lista de resultados e interage com ele (curte, segue e comenta).<br>
Fecha o vídeo e volta para a lista de resultados, repetindo o processo.<br>
Caso o script encontre um erro de timeout ao carregar elementos, ele tenta novamente após recarregar a página.<br>

# Comentários Aleatórios<br>
A lista comentarios armazena comentários pré-definidos, e o script escolhe um aleatoriamente para cada vídeo. Isso ajuda a manter a interação mais natural.<br>

# Exceções e Tentativas<br>
O script trata possíveis erros, como timeouts ao carregar elementos, e tenta adicionar comentários até 3 vezes se houver falhas.<br>

# Melhorias Possíveis<br>
Controle de Comentários Repetidos: Evitar comentários duplicados com uma lista de controle.<br>
Palavras-chave no Comentário: Personalizar os comentários com base nas palavras-chave da descrição do vídeo, tornando as interações mais relevantes.<br>

# Observações de Uso<br>
Legalidade e Termos de Uso: Esse script é para fins educacionais e não deve ser usado para spam ou violação dos Termos de Serviço do TikTok.<br>
Riscos de Bloqueio: Automação excessiva em plataformas como TikTok pode resultar em bloqueios temporários ou permanentes da conta.<br>
Esse README fornece uma visão geral do script, instruções de instalação, explicação das funcionalidades e estrutura do código.<br>