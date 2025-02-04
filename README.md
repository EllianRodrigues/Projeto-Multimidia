# 🎵 Controle Multimídia por Gestos 🎮

Este projeto utiliza a câmera do computador para detectar gestos manuais e controlar funções multimídia, como ajuste de volume e controle de reprodução de músicas no Spotify.

## 🚀 Funcionalidades

- **Ajustar volume** (Aumentar/Diminuir)
- **Trocar faixas** (Próxima/Anterior)
- **Reproduzir/Pausar música**
- **Registro de gestos personalizados**
- **HUD informativa com comandos disponíveis**

## 🛠 Tecnologias Utilizadas

- Python
- OpenCV
- MediaPipe
- NumPy
- SciPy
- Pycaw (Para controle de áudio)
- Comtypes (Para simulação de teclas)

## 📦 Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/EllianRodrigues/Projeto-Multimidia.git
   cd Projeto-Multimidia
   ```

2. Instale as dependências:
   ```bash
   pip install opencv-python mediapipe numpy scipy pycaw comtypes
   ```

3. Execute o script:
   ```bash
   python Source.py
   ```

## 🎯 Como Usar

1. Inicie o programa e posicione sua mão na frente da câmera.
2. Pressione uma tecla numérica (`1-5`) para registrar um novo gesto.
3. Quando o mesmo gesto for detectado novamente, a ação correspondente será executada automaticamente.
4. Pressione `Q` para sair do programa.

## 🎮 Mapeamento de Comandos

| Gesto Registrado | Ação Executada |
|-----------------|---------------|
| **1** | Aumentar volume |
| **2** | Diminuir volume |
| **3** | Próxima música |
| **4** | Música anterior |
| **5** | Reproduzir/Pausar |

## 📌 Observações

- O script precisa de acesso à câmera para funcionar corretamente.
- O código é compatível apenas com **Windows**, pois utiliza atalhos do sistema.
