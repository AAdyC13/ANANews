FROM continuumio/miniconda3

# 建立工作目錄
WORKDIR /app

# 複製環境設定與程式碼
COPY environment_forDocker.yml .

# 建立 Conda 環境（命名必須符合 ENV 設定）
RUN conda env create -f environment_forDocker.yml -n ananews

# 設定 PATH（確保用的是你建立的環境）
ENV PATH /opt/conda/envs/ananews/bin:$PATH

# 安裝 GPU 版本的 PyTorch 套件（使用 conda activate 的環境）
RUN /opt/conda/envs/ananews/bin/pip install torch==2.6.0+cu126 --index-url https://download.pytorch.org/whl/cu126
RUN /opt/conda/envs/ananews/bin/pip install torchvision==0.21.0+cu126 --index-url https://download.pytorch.org/whl/cu126
RUN /opt/conda/envs/ananews/bin/pip install torchaudio==2.6.0+cu126 --index-url https://download.pytorch.org/whl/cu126

# 複製其餘 Django 專案程式碼
COPY . .

# 預設執行指令（使用 ananews 環境）
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]