# 易镜 · 模拟周易筮占系统
# Docker容器配置

# 使用Python 3.11 slim版本作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    PORT=5000

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 创建非root用户
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 复制项目文件并设置权限
COPY --chown=appuser:appuser requirements.txt .
COPY --chown=appuser:appuser app/ ./app/
COPY --chown=appuser:appuser instance/ ./instance/

# 安装Python依赖
RUN pip install --no-cache-dir --user -r requirements.txt

# 确保用户bin目录在PATH中
ENV PATH="/home/appuser/.local/bin:${PATH}"

# 暴露端口
EXPOSE $PORT

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# 启动命令
# 使用gunicorn作为生产服务器
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "--access-logfile", "-", "app.main:app"]

# 开发模式启动命令（如需要）
# CMD ["python", "app/main.py"]