from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException, ElementNotInteractableException
import time
import random
import signal

# Caminho para o chromedriver
service = Service('C:/Users/User/Desktop/chromedriver-win64/chromedriver.exe')

# Configurar opções do Chrome para usar o perfil específico
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-notifications')
options.add_argument(r"user-data-dir=C:/Users/User/AppData/Local/Google/Chrome/User Data")
options.add_argument("profile-directory=Default")

# Lista de comentários aleatórios
comentarios = [
    "Adorei esse vídeo!", "Conteúdo incrível, parabéns!", "Muito bom, continua postando!",
    "Esse tema é muito interessante!", "Estou aprendendo muito com seus vídeos!",
    "Ótima dica!", "Obrigado por compartilhar!", "Esse vídeo foi muito útil!",
    "Amei esse conteúdo!", "Tô amando seus vídeos, sucesso!"
]

# Variável de contagem de vídeos
contador_videos = 0

# Inicializa o navegador
def iniciar_navegador():
    global driver
    driver = webdriver.Chrome(service=service, options=options)
    print("Passo 1: Navegador iniciado.")

# Função para verificar e fechar o modal de confirmação de saída
def fechar_modal_saida():
    try:
        modal_sair = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Deixar']"))
        )
        modal_sair.click()
        print("Modal de confirmação de saída fechado.")
    except TimeoutException:
        pass  # Nenhum modal detectado

# Função para verificar a presença do reCAPTCHA
def verificar_recaptcha():
    try:
        recaptcha = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "captcha_verify_container"))
        )
        return True
    except TimeoutException:
        return False

# Função para curtir o vídeo somente se ainda não estiver curtido
def tentar_curtir_video():
    try:
        like_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[@aria-label and contains(@class, 'ButtonActionItem')]"))
        )
        if like_button.get_attribute("aria-pressed") == "false":
            like_button.click()
            print("Vídeo curtido com sucesso.")
        else:
            print("Vídeo já está curtido.")
    except Exception as e:
        print(f"Erro ao curtir o vídeo: {e}")

# Função para seguir o usuário somente se ainda não estiver seguido
def seguir_usuario():
    try:
        follow_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-1pcikqk-Button')]"))
        )
        if follow_button.text.lower() == "seguir":
            follow_button.click()
            print("Usuário seguido com sucesso.")
        else:
            print("Usuário já está sendo seguido.")
    except Exception as e:
        print(f"Erro ao seguir o usuário: {e}")

# Função para verificar se o comentário já foi feito e, se não, adicionar um novo comentário
def comentar_video():
    try:
        usuario_comentou = False
        comentarios_existentes = driver.find_elements(By.XPATH, "//span[contains(text(), 'Shoppe_achadinhosFarm')]")
        
        if comentarios_existentes:
            usuario_comentou = True
            print("Comentário já existente. Pulando comentário.")
        
        if not usuario_comentou:
            comment_box_placeholder = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "public-DraftEditorPlaceholder-inner"))
            )
            comment_box_placeholder.click()
            
            comment_box = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "notranslate.public-DraftEditor-content"))
            )
            comentario = random.choice(comentarios)
            comment_box.send_keys(comentario)
            time.sleep(0.5)
            
            publicar_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@data-e2e='comment-post' and not(@aria-disabled='true')]"))
            )
            publicar_button.click()
            print("Comentário enviado, aguardando confirmação.")
            
            # Aguardar que o comentário seja publicado verificando sua presença nos comentários
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{comentario}')]"))
            )
            print("Comentário confirmado como publicado.")
    except Exception as e:
        print(f"Erro ao comentar no vídeo: {e}")

# Função para avançar para o próximo vídeo usando os botões de navegação
def proximo_video():
    fechar_modal_saida()
    try:
        next_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-e2e='arrow-right']"))
        )
        next_button.click()
        print("Avançado para o próximo vídeo.")
    except NoSuchElementException:
        try:
            first_next_button = driver.find_element(By.XPATH, "//button[@aria-label='Ir para o próximo vídeo']")
            first_next_button.click()
            print("Avançado para o próximo vídeo (primeiro botão encontrado).")
        except NoSuchElementException:
            print("Nenhum botão de próximo vídeo encontrado.")
            return False
    return True

# Função principal de automação do TikTok
def automacao_tiktok():
    global contador_videos
    nome_usuario = input("Digite seu nome de usuário no TikTok: ")
    tema = input("Digite o tema para o qual você deseja fazer os comentários: ")

    iniciar_navegador()
    
    # Pesquisa do tema
    driver.get("https://www.tiktok.com/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("Página principal do TikTok carregada.")
    time.sleep(3)

    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Procurar']"))
    )
    search_input.click()
    search_input.send_keys(tema)
    search_input.send_keys(Keys.RETURN)
    print(f"Tema '{tema}' pesquisado.")
    time.sleep(3)

    # Entrar no primeiro vídeo da lista de resultados
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@data-e2e, 'search-card-desc')]"))
    )
    print("Resultados de pesquisa carregados.")
    
    first_video = driver.find_element(By.XPATH, "//div[contains(@class, 'DivPlayerContainer')]")
    first_video.click()
    print("Primeiro vídeo aberto.")
    time.sleep(2)
    
    while True:
        try:
            time.sleep(2)  # Espera de 2 segundos para o vídeo carregar completamente
            
            # Verificar reCAPTCHA
            if verificar_recaptcha():
                print("reCAPTCHA detectado. Aguardando 5 segundos para resolução.")
                time.sleep(5)
            else:
                print("reCAPTCHA não detectado.")
            
            # Curtir o vídeo
            tentar_curtir_video()
            
            # Seguir o usuário
            seguir_usuario()
            
            # Comentar no vídeo
            comentar_video()
            
            # Incrementar e registrar o contador de vídeos
            contador_videos += 1
            print(f"Vídeo {contador_videos} completo.")
            
            # Avançar para o próximo vídeo
            if not proximo_video():
                print("Não foi possível avançar para o próximo vídeo.")
                break
        except TimeoutException:
            print("Timeout ao tentar interagir com o vídeo atual. Tentando novamente.")
            time.sleep(2)

    print(f"Total de vídeos completados: {contador_videos}")
    print("Execução finalizada. O navegador permanecerá aberto.")

# Função para lidar com o sinal de interrupção (CTRL+C)
def handle_exit_signal(signal, frame):
    print("Execução interrompida pelo usuário. O navegador permanecerá aberto.")
    # Remova `driver.quit()` para evitar que o navegador feche
    # driver.quit()
    exit(0)

# Configurar o handler para manter o navegador aberto após interrupção manual
signal.signal(signal.SIGINT, handle_exit_signal)

# Iniciar automação
automacao_tiktok()
