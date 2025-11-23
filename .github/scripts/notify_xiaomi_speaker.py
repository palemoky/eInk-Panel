import os
import sys
import asyncio
from miservice import MiAccount, MiNAService

async def main():
    # 从环境变量获取配置
    mi_user = os.environ.get('MI_USER')
    mi_pass = os.environ.get('MI_PASS')
    mi_did = os.environ.get('MI_BOX_DID')
    message = os.environ.get('NOTIFY_MSG', '主人，您的 GitHub Actions 构建失败了，请检查。')

    # 参数验证
    if not all([mi_user, mi_pass, mi_did]):
        print("⚠️  Warning: Missing required environment variables (MI_USER, MI_PASS, MI_DID)")
        print("Skipping notification...")
        return

    try:
        print(f"🔔 Attempting to send notification to device {mi_did}")
        print(f"📝 Message: {message}")
        
        # 登录小米账号
        account = MiAccount(
            mi_user,
            mi_pass,
            os.path.join(os.environ.get('GITHUB_WORKSPACE', '.'), 'mi_token')
        )
        
        # 发送 TTS（带超时控制）
        service = MiNAService(account)
        await asyncio.wait_for(
            service.text_to_speech(mi_did, message),
            timeout=30.0  # 30秒超时
        )
        
        print("✅ Notification sent successfully!")
        
    except asyncio.TimeoutError:
        print("❌ Error: Notification timeout (30s)")
        # 不抛出异常，避免阻塞 workflow
    except Exception as e:
        print(f"❌ Error sending notification: {type(e).__name__}: {e}")
        # 不抛出异常，避免阻塞 workflow

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        sys.exit(1)