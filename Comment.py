from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random

# Caminho para o chromedriver
service = Service('C:/Users/User/Desktop/chromedriver-win64/chromedriver.exe')

# Configurar opções do Chrome para usar o perfil específico
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-notifications')
options.add_argument(r"user-data-dir=C:/Users/User/AppData/Local/Google/Chrome/User Data")
options.add_argument("profile-directory=Default")  # Ajuste para "Profile 6" se necessário

# Lista de comentários aleatórios
comentarios = [
    "Adorei esse vídeo!",
    "Conteúdo incrível, parabéns!",
    "Muito bom, continua postando!",
    "Esse tema é muito interessante!",
    "Estou aprendendo muito com seus vídeos!",
    "Ótima dica!",
    "Obrigado por compartilhar!",
    "Esse vídeo foi muito útil!",
    "Amei esse conteúdo!",
    "Tô amando seus vídeos, sucesso!"
]

def iniciar_navegador():
    # Inicializa o navegador com as opções especificadas
    global driver
    driver = webdriver.Chrome(service=service, options=options)

def automacao_tiktok(tema):
    global driver
    iniciar_navegador()
    
    while True:
        try:
            driver.get("https://www.tiktok.com/")
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(5)
            
            # Aceitar cookies se necessário
            try:
                aceitar_cookies = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Aceitar todos']"))
                )
                aceitar_cookies.click()
            except:
                pass  # Se o botão não aparecer, continue

            # Campo de pesquisa e envio do tema
            search_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Procurar']"))
            )
            search_input.click()
            search_input.send_keys(tema)
            search_input.send_keys(Keys.RETURN)
            time.sleep(5)

            # Aguardar que os resultados de pesquisa carreguem completamente
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@data-e2e, 'search-card-desc')]"))
            )

            # Selecionar um vídeo aleatório dos resultados
            videos = driver.find_elements(By.XPATH, "//div[contains(@class, 'DivPlayerContainer')]")
            if videos:
                video_aleatorio = random.choice(videos)
                video_aleatorio.click()
                time.sleep(5)

                # Curtir o vídeo se ainda não estiver curtido
                try:
                    like_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//button[@aria-label and contains(@class, 'ButtonActionItem')]"))
                    )
                    if "aria-pressed" in like_button.get_attribute("outerHTML") and like_button.get_attribute("aria-pressed") == "false":
                        like_button.click()
                        print("Vídeo curtido com sucesso.")
                    else:
                        print("Vídeo já está curtido.")
                except:
                    print("Não foi possível curtir o vídeo.")

                # Seguir o usuário
                try:
                    follow_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-1pcikqk-Button')]"))
                    )
                    if follow_button.text.lower() == "seguir":
                        follow_button.click()
                        print("Usuário seguido com sucesso.")
                    else:
                        print("Usuário já está sendo seguido.")
                except:
                    print("Não foi possível seguir o usuário.")

                # Adicionar um comentário aleatório
                comentario_enviado = False
                for tentativa in range(3):  # Tentar até 3 vezes se o campo de comentário falhar
                    try:
                        # Clicar na área de comentário para ativar
                        comment_box_placeholder = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CLASS_NAME, "public-DraftEditorPlaceholder-inner"))
                        )
                        comment_box_placeholder.click()
                        
                        # Digitar o comentário
                        comment_box = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "notranslate.public-DraftEditor-content"))
                        )
                        comentario = random.choice(comentarios)
                        comment_box.send_keys(comentario)
                        time.sleep(1)
                        
                        # Aguarde até que o botão "Publicar" esteja habilitado
                        publicar_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//div[@data-e2e='comment-post' and not(@aria-disabled='true')]"))
                        )
                        publicar_button.click()
                        time.sleep(2)

                        comentario_enviado = True
                        print("Comentário enviado com sucesso.")
                        
                        break
                    except:
                        print(f"Tentativa {tentativa + 1} de adicionar comentário falhou.")
                        time.sleep(2)

                if not comentario_enviado:
                    print("Não foi possível adicionar o comentário após várias tentativas.")

                # Fechar o vídeo e voltar à lista de vídeos
                close_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Fechar']"))
                )
                close_button.click()
                time.sleep(3)

            else:
                print("Nenhum vídeo encontrado para o tema pesquisado.")
                break  # Sair do loop se não houver vídeos

        except TimeoutException:
            print("Timeout ao tentar acessar o TikTok ou encontrar um elemento. Tentando novamente.")
            driver.refresh()
            time.sleep(5)

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            driver.quit()  # Fechar a sessão atual
            iniciar_navegador()  # Reiniciar o navegador
            time.sleep(5)

# Iniciar automação com um tema específico
automacao_tiktok("condicionamento e energia")
