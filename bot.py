"""
Pix Tips Brasil - Fixed for Railway
"""
import os
import sys
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== DATA ====================

PIX_TIPS = {
    'basic': [
        '💡 Pix é um sistema de pagamentos instantâneos do Banco Central',
        '💡 Você pode criar chaves usando CPF, email, celular ou chave aleatória',
        '💡 Pix funciona 24h por dia, 7 dias por semana',
        '💡 Pix é gratuito para pessoas físicas'
    ],
    'security': [
        '🔒 Nunca compartilhe sua senha Pix',
        '🔒 Confirme sempre o nome do destinatário',
        '🔒 Bancos NUNCA pedem sua chave por telefone',
        '🔒 Desconfie de ofertas milagrosas'
    ],
    'banks': [
        '🏦 Nubank - Sem taxas, Pix ilimitado',
        '🏦 Banco Inter - Conta digital, investimentos',
        '🏦 Mercado Pago - Integração com e-commerce',
        '🏦 C6 Bank - Cartão com pontos, Pix'
    ]
}

FAQ = [
    ('❓ Pix é gratuito?', '✅ Sim, para pessoas físicas é 100% gratuito'),
    ('❓ Qual o limite do Pix?', '✅ Definido pelo banco, geralmente R$1.000-R$10.000'),
    ('❓ Posso ter várias chaves?', '✅ Sim, em diferentes bancos'),
    ('❓ Pix funciona 24h?', '✅ Sim, 24/7 incluindo feriados')
]

ALERTS = [
    '🚨 Golpe: Falso banco pedindo dados por telefone',
    '🚨 Golpe: Pirâmide financeira com promessas de lucro',
    '🚨 Golpe: Phishing pedindo sua chave Pix',
    '🚨 Golpe: Falso funcionário do banco no WhatsApp'
]

# ==================== HANDLERS ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message"""
    user = update.effective_user
    text = f"""
👋 Olá {user.first_name}! Bem-vindo ao **Pix Tips Brasil** 🏦

Seu guia completo sobre **Pix e Bancos Digitais**!

---

📌 **Comandos disponíveis:**

💡 `/pix` - Dicas sobre Pix
🔒 `/seguranca` - Dicas de segurança
🏦 `/bancos` - Melhores bancos digitais
❓ `/faq` - Perguntas frequentes
🔔 `/alertas` - Alertas de segurança
📊 `/stats` - Estatísticas
🆘 `/help` - Ajuda

---

📢 **100% gratuito | Conteúdo informativo**
❌ **Sem apostas, sem promessas financeiras**
    """
    
    keyboard = [
        [InlineKeyboardButton("💡 Pix", callback_data='pix')],
        [InlineKeyboardButton("🔒 Segurança", callback_data='seguranca')],
        [InlineKeyboardButton("🏦 Bancos", callback_data='bancos')],
        [InlineKeyboardButton("❓ FAQ", callback_data='faq')],
        [InlineKeyboardButton("📢 Anunciar", callback_data='ad')]
    ]
    
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def pix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pix tips"""
    text = "💡 **Dicas sobre Pix:**\n\n"
    for tip in PIX_TIPS['basic']:
        text += f"{tip}\n\n"
    
    keyboard = [[InlineKeyboardButton("🏠 Voltar", callback_data='home')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def seguranca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Security tips"""
    text = "🔒 **Dicas de Segurança:**\n\n"
    for tip in PIX_TIPS['security']:
        text += f"{tip}\n\n"
    
    keyboard = [[InlineKeyboardButton("🏠 Voltar", callback_data='home')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def bancos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bank recommendations"""
    text = "🏦 **Melhores Bancos Digitais:**\n\n"
    for bank in PIX_TIPS['banks']:
        text += f"{bank}\n\n"
    
    keyboard = [[InlineKeyboardButton("🏠 Voltar", callback_data='home')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """FAQ"""
    text = "❓ **Perguntas Frequentes:**\n\n"
    for q, a in FAQ:
        text += f"{q}\n{a}\n\n"
    
    keyboard = [[InlineKeyboardButton("🏠 Voltar", callback_data='home')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def alertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Alerts"""
    text = "🔔 **Alertas de Segurança:**\n\n"
    for alert in ALERTS:
        text += f"{alert}\n\n"
    
    keyboard = [[InlineKeyboardButton("🏠 Voltar", callback_data='home')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistics"""
    text = """
📊 **Estatísticas do Pix Tips Brasil**

👥 **Membros:** 1,500+
📈 **Crescimento mensal:** +15%
💬 **Engajamento:** 9.8%

📱 **Conteúdo mais visto:**
1️⃣ Segurança - 42%
2️⃣ Pix Básico - 30%
3️⃣ Bancos Digitais - 18%

📢 **Anuncie aqui!** 
Contato: @seu_usuario
    """
    
    keyboard = [[InlineKeyboardButton("📢 Anunciar", callback_data='ad')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help"""
    text = """
📖 **Comandos Disponíveis:**

/pix - Dicas sobre Pix
/seguranca - Dicas de segurança
/bancos - Melhores bancos
/faq - Perguntas frequentes
/alertas - Alertas de segurança
/stats - Estatísticas
/help - Ajuda

✅ **Conteúdo 100% informativo**
❌ **Sem apostas, sem promessas financeiras**

📢 **Anuncie:** @seu_usuario
    """
    
    await update.message.reply_text(text, parse_mode='Markdown')

# ==================== CALLBACK ====================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'home':
        await start(update, context)
    
    elif query.data == 'pix':
        text = "💡 **Dicas sobre Pix:**\n\n"
        for tip in PIX_TIPS['basic']:
            text += f"{tip}\n\n"
        keyboard = [[InlineKeyboardButton("🏠 Voltar", callback_data='home')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'seguranca':
        text = "🔒 **Dicas de Segurança:**\n\n"
        for tip in PIX_TIPS['security']:
            text += f"{tip}\n\n"
        keyboard = [[InlineKeyboardButton("🏠 Voltar", callback_data='home')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'bancos':
        text = "🏦 **Melhores Bancos Digitais:**\n\n"
        for bank in PIX_TIPS['banks']:
            text += f"{bank}\n\n"
        keyboard = [[InlineKeyboardButton("🏠 Voltar", callback_data='home')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'faq':
        text = "❓ **Perguntas Frequentes:**\n\n"
        for q, a in FAQ:
            text += f"{q}\n{a}\n\n"
        keyboard = [[InlineKeyboardButton("🏠 Voltar", callback_data='home')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'ad':
        text = """
📢 **Anuncie no Pix Tips Brasil!**

✅ **Vantagens:**
• Alcance: 1,500+ membros
• Segmentação: Brasil (75%)
• Engajamento: 9.8%

💰 **Pacotes:**
• 📝 Post patrocinado: R$ 50
• ⭐ Post + destaque: R$ 100
• 📅 Pacote mensal: R$ 300

📩 **Contato:** @seu_usuario
        """
        await query.edit_message_text(text, parse_mode='Markdown')

# ==================== MAIN ====================

def main():
    """Start the bot"""
    # Get token from environment
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    
    if not token:
        logger.error("❌ TELEGRAM_BOT_TOKEN not found in environment variables!")
        logger.error("Please set: railway variables set TELEGRAM_BOT_TOKEN=your_token")
        sys.exit(1)
    
    logger.info("🚀 Starting Pix Tips Brasil bot...")
    logger.info(f"✓ Token found: {token[:10]}...")
    
    try:
        # Create application
        app = Application.builder().token(token).build()
        
        # Add command handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("pix", pix))
        app.add_handler(CommandHandler("seguranca", seguranca))
        app.add_handler(CommandHandler("bancos", bancos))
        app.add_handler(CommandHandler("faq", faq))
        app.add_handler(CommandHandler("alertas", alertas))
        app.add_handler(CommandHandler("stats", stats))
        app.add_handler(CommandHandler("help", help))
        
        # Add callback handler
        app.add_handler(CallbackQueryHandler(button_callback))
        
        # Start the bot
        logger.info("✅ Bot is running! Waiting for messages...")
        app.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
