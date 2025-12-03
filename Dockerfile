# syntax=docker/dockerfile:1

# ==========================================
# Stage 1: Builder
# ==========================================
FROM python:3.14-slim-bookworm AS builder

WORKDIR /app

# 1. 配置树莓派官方源 & 安装编译依赖
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    swig \
    curl \
    gnupg \
    ca-certificates \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL http://archive.raspberrypi.org/debian/raspberrypi.gpg.key | gpg --dearmor -o /etc/apt/keyrings/raspberrypi.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/raspberrypi.gpg] http://archive.raspberrypi.org/debian bookworm main" > /etc/apt/sources.list.d/raspi.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends liblgpio-dev

# 2. 高效安装 uv (直接从官方镜像复制二进制文件)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 3. 安装 Python 依赖
ENV UV_COMPILE_BYTECODE=1
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev --extra hardware

# ==========================================
# Stage 2: Runtime
# ==========================================
FROM python:3.14-slim-bookworm

WORKDIR /app

# 1. 安装运行时依赖 & lgpio 运行时库
# 注意：Runtime 只需要 liblgpio1，不需要 -dev 和 swig/gcc
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo \
    libopenjp2-7 \
    libtiff6 \
    curl \
    gnupg \
    ca-certificates \
    # 再次添加源 (为了安装 liblgpio1)
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL http://archive.raspberrypi.org/debian/raspberrypi.gpg.key | gpg --dearmor -o /etc/apt/keyrings/raspberrypi.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/raspberrypi.gpg] http://archive.raspberrypi.org/debian bookworm main" > /etc/apt/sources.list.d/raspi.list \
    && apt-get update \
    # 仅安装运行时库
    && apt-get install -y --no-install-recommends liblgpio1 \
    # 清理不必要的工具以减小体积
    && apt-get purge -y curl gnupg build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# 2. 从 Builder 复制虚拟环境
COPY --from=builder /app/.venv /app/.venv

# 3. 设置 PATH，自动激活虚拟环境
ENV PATH="/app/.venv/bin:$PATH"

# 4. 复制源代码（排除 fonts 目录以减小镜像体积）
COPY src ./src
COPY resources ./resources
COPY pyproject.toml uv.lock ./

# 5. 环境变量与配置
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV GPIOZERO_PIN_FACTORY=lgpio
ENV DISPLAY_MODE=dashboard

# 6. 权限与存储卷
RUN mkdir -p /app/data && chown -R root:root /app/data
VOLUME /app/data

# 7. 启动
CMD ["python", "-m", "src.main"]
