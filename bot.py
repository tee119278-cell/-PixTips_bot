import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Data
PIX_TIPS = {
    'basic': [
        '💡 Pix é um sistema de pagamentos instantâneos do Banco Central',
        '💡 Você pode criar chaves usando CPF, email, celular ou chave aleatória',
        '💡 Pix funciona 24h por dia, 7 dias por semana'
    ],
    'security': [
        '🔒 Nunca compartilhe sua senha Pix',
        '🔒 Confirme sempre o nome do destinatário',
        '🔒 Bancos NUNCA pedem sua chave por telefone'
    ],
    'banks': [
        '🏦 Nubank - Sem taxas, Pix ilimitado',
        '🏦 Banco Inter - Conta digital, investimentos',
        '🏦 Mercado Pago - Integração com e-commerce'
    ]
}

FAQ = [
    ('❓ Pix é gratuito?', '✅ Sim, para pessoas físicas é 100% gratuito'),
    ('❓ Qual o limite do Pix?', '✅ Definido pelo banco, geralmente R$1.000-R$10.000'),
    ('❓ Posso ter várias chaves?', '✅ Sim, em diferentes bancos')
]

ALERTS = [
    '🚨 Golpe: Falso banco pedindo dados por telefone',
    '🚨 Golpe: Pirâmide financeira com promessas de lucro',
    '🚨 Golpe: Phishing pedindo sua chave Pix'
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = f"""
👋 Olá {user.first_name}! Bem-vindo ao **Pix Tips Brasil**

📌 **Comandos:**
/pix - Dicas sobre Pix
/seguranca - Dicas de segurança  
/bancos - Melhores bancos
/faq - Perguntas frequentes
/alertas - Alertas de segurança
/stats - Estatísticas
/help - Ajuda

📢 **100% Gratuito | Sem API**
    """
    
    keyboard = [
        [InlineKeyboardButton("💡 Pix", callback_data='pix')],
        [InlineKeyboardButton("🔒 Segurança", callback_data='seguranca')],
        [InlineKeyboardButton("🏦 Bancos", callback_data='bancos')],
        [InlineKeyboardButton("📢 Anunciar", callback_data='ad')]
    ]
    
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def pix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "💡 **Dicas sobre Pix:**\n\n"
    for tip in PIX_TIPS['basic']:
        text += f"{tip}\n\n"
    
    keyboard = [[InlineKeyboardButton("🏠 Voltar", callback_data='home')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def seguranca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🔒 **Dicas de Segurança:**\n\n"
    for tip in PIX_TIPS['security']:
        text += f"{tip}\n\n"
    
    keyboard = [[InlineKeyboardButton("🏠 Voltar", callback_data='home')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def bancos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🏦 **Melhores Bancos Digitais:**\n\n"
    for bank in PIX_TIPS['banks']:
        text += f"{bank}\n\n"
    
    keyboard = [[InlineKeyboardButton("🏠 Voltar", callback_data='home')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "❓ **Perguntas Frequentes:**\n\n"
    for q, a in FAQ:
        text += f"{q}\n{a}\n\n"
    
    keyboard = [[InlineKeyboardButton("🏠 Voltar", callback_data='home')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def alertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🔔 **Alertas de Segurança:**\n\n"
    for alert in ALERTS:
        text += f"{alert}\n\n"
    
    keyboard = [[InlineKeyboardButton("🏠 Voltar", callback_data='home')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
📊 **Estatísticas**

👥 Membros: 1,500+
📈 Crescimento: +15% mês
💬 Engajamento: 9.8%

📢 **Anuncie aqui!**
Contato: @seu_usuario
    """
    
    keyboard = [[InlineKeyboardButton("📢 Anunciar", callback_data='ad')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
📖 **Comandos:**

/pix - Dicas sobre Pix
/seguranca - Dicas de segurança
/bancos - Melhores bancos
/faq - Perguntas frequentes
/alertas - Alertas de segurança
/stats - Estatísticas
/help - Ajuda

✅ Conteúdo informativo
❌ Sem apostas, sem promessas
    """
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    
    elif query.data == 'ad':
        text = """
📢 **Anuncie no Pix Tips Brasil!**

✅ Alcance: 1,500+ membros
💰 Post patrocinado: R$ 50
⭐ Post + destaque: R$ 100
📅 Pacote mensal: R$ 300

📩 Contato: @seu_usuario
        """
        await query.edit_message_text(text, parse_mode='Markdown')

def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    
    if not token:
        logger.error("❌ TELEGRAM_BOT_TOKEN not found!")
        return
    
    logger.info("🚀 Starting Pix Tips Brasil bot...")
    
    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pix", pix))
    app.add_handler(CommandHandler("seguranca", seguranca))
    app.add_handler(CommandHandler("bancos", bancos))
    app.add_handler(CommandHandler("faq", faq))
    app.add_handler(CommandHandler("alertas", alertas))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
