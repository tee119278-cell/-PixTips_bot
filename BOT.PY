"""
Pix Tips & Online Banking Brazil Bot
Telegram Ads Friendly - No Gambling - No API Keys
"""

import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ============================================
# LOGGING
# ============================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================
# DATA - MANUALLY CURATED (NO API KEYS)
# ============================================

PIX_TIPS = {
    "basico": [
        {
            "title": "💡 O que é Pix?",
            "tip": "Pix é um sistema de pagamentos instantâneos criado pelo Banco Central do Brasil. Disponível 24/7, 365 dias por ano.",
            "category": "Básico"
        },
        {
            "title": "💡 Como criar uma chave Pix?",
            "tip": "Acesse seu banco, vá em 'Pix' → 'Minhas chaves' → 'Cadastrar chave'. Você pode usar CPF, e-mail, celular ou chave aleatória.",
            "category": "Básico"
        },
        {
            "title": "💡 Quais são os tipos de chave Pix?",
            "tip": "📌 CPF/CNPJ\n📌 E-mail\n📌 Número de celular\n📌 Chave aleatória (gerada pelo sistema)",
            "category": "Básico"
        },
        {
            "title": "💡 Pix é seguro?",
            "tip": "Sim! O Pix utiliza criptografia de ponta e autenticação em duas etapas. Nunca compartilhe sua senha e sempre confirme os dados antes de pagar.",
            "category": "Segurança"
        }
    ],
    "avancado": [
        {
            "title": "🔥 Pix Agendado",
            "tip": "Você pode agendar pagamentos Pix para datas futuras. Muito útil para boletos, aluguel e contas fixas.",
            "category": "Recursos"
        },
        {
            "title": "🔥 Pix com Troco",
            "tip": "Em alguns bancos, você pode pagar com Pix e receber troco em dinheiro. Útil quando você não tem dinheiro físico.",
            "category": "Recursos"
        },
        {
            "title": "🔥 Pix Saque e Troco",
            "tip": "Disponível em lotéricas e correspondentes bancários. Saque com Pix e receba seu dinheiro sem cartão!",
            "category": "Recursos"
        },
        {
            "title": "🔥 Pix Garantido",
            "tip": "Modalidade com garantia de pagamento, ideal para compras online e vendas entre pessoas.",
            "category": "Recursos"
        }
    ],
    "seguranca": [
        {
            "title": "🛡️ Dicas de Segurança",
            "tip": "✅ Nunca compartilhe sua senha\n✅ Confirme o nome do destinatário\n✅ Use chaves aleatórias para compras\n✅ Ative notificações no app",
            "category": "Segurança"
        },
        {
            "title": "🛡️ Como evitar golpes?",
            "tip": "⚠️ Desconfie de chaves Pix com nome suspeito\n⚠️ Não faça Pix para desconhecidos\n⚠️ Verifique o valor antes de confirmar",
            "category": "Segurança"
        },
        {
            "title": "🛡️ O que fazer se cair em golpe?",
            "tip": "1️⃣ Ligue imediatamente para seu banco\n2️⃣ Registre boletim de ocorrência\n3️⃣ Entre no site do Banco Central\n4️⃣ Use o mecanismo especial de devolução",
            "category": "Segurança"
        }
    ]
}

ONLINE_BANKING_TIPS = {
    "melhores_bancos": [
        {
            "name": "Nubank",
            "features": "Sem taxas, cartão de crédito, investimentos, Pix ilimitado",
            "rating": "⭐ 4.8/5"
        },
        {
            "name": "Banco Inter",
            "features": "Conta digital, investimentos, shopping, Pix, cashback",
            "rating": "⭐ 4.7/5"
        },
        {
            "name": "Mercado Pago",
            "features": "Conta para negócios, Pix, cartão, integração com e-commerce",
            "rating": "⭐ 4.6/5"
        },
        {
            "name": "C6 Bank",
            "features": "Conta digital, investimentos, cartão com pontos, Pix",
            "rating": "⭐ 4.5/5"
        },
        {
            "name": "PicPay",
            "features": "Pagamentos, Pix, cashback, transferências, cartão",
            "rating": "⭐ 4.4/5"
        }
    ],
    "dicas_bancarias": [
        {
            "title": "💳 Como escolher seu banco digital?",
            "tip": "✅ Considere taxas e tarifas\n✅ Verifique limites e transferências\n✅ Analise o atendimento\n✅ Compare cartões de crédito"
        },
        {
            "title": "💳 Transferências sem taxas",
            "tip": "📌 Pix é sempre gratuito\n📌 TED/DOC são gratuitos em muitos bancos\n📌 Use transferências entre contas do mesmo banco"
        },
        {
            "title": "💳 Economize com bancos digitais",
            "tip": "💰 Evite tarifas de manutenção\n💰 Prefira bancos com TED/DOC gratuito\n💰 Use Pix para todas as transferências"
        },
        {
            "title": "💳 Como abrir conta digital?",
            "tip": "📱 Baixe o app\n📱 Informe seus dados\n📱 Tire foto do documento\n📱 Faça selfie\n📱 Aguarde aprovação (minutos!)"
        }
    ]
}

PIX_FAQ = [
    {"question": "❓ Pix funciona 24 horas?", "answer": "Sim! O Pix está disponível 24 horas por dia, 7 dias por semana, incluindo feriados."},
    {"question": "❓ Qual o limite do Pix?", "answer": "O limite é definido pelo seu banco. Varia entre R$ 1.000 a R$ 10.000 por transação, dependendo do seu perfil."},
    {"question": "❓ Pix é gratuito?", "answer": "Para pessoas físicas, o Pix é 100% gratuito. Para empresas, alguns bancos podem cobrar tarifas."},
    {"question": "❓ Como reembolsar um Pix?", "answer": "O Pix é irretratável. Para reembolso, você deve entrar em contato com o destinatário."},
    {"question": "❓ Posso ter várias chaves Pix?", "answer": "Sim! Você pode ter quantas chaves quiser, em diferentes bancos."},
    {"question": "❓ Pix é seguro?", "answer": "Sim, o Pix utiliza os mais altos padrões de segurança, incluindo criptografia e autenticação em duas etapas."}
]

SECURITY_ALERTS = [
    {
        "title": "🚨 Golpe do Falso Banco",
        "description": "Golpistas se passam por funcionários do banco e pedem dados pessoais. O banco NUNCA pede sua senha ou chave Pix por telefone.",
        "severity": "Alto",
        "date": "2026-08-31"
    },
    {
        "title": "🚨 Pirâmide Financeira",
        "description": "Promessas de lucros altos e rápidos com Pix. Nenhum investimento legítimo usa esse modelo. Desconfie!",
        "severity": "Alto",
        "date": "2026-08-30"
    },
    {
        "title": "🚨 Phishing por WhatsApp",
        "description": "Falsos funcionários pedem sua chave Pix para 'atualizar cadastro'. Banco nunca pede Pix para atualizações.",
        "severity": "Médio",
        "date": "2026-08-29"
    }
]

# ============================================
# COMMAND HANDLERS
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Welcome message"""
    user = update.effective_user
    welcome_text = f"""
👋 Olá {user.first_name}! Bem-vindo ao **Pix Tips Brasil** 🏦

Seu guia completo sobre **Pix e Bancos Digitais** no Brasil!

---

📌 **Comandos:**

💡 `/pix` - Dicas sobre Pix
🔒 `/seguranca` - Dicas de segurança
🏦 `/bancos` - Melhores bancos digitais
❓ `/faq` - Perguntas frequentes
🔔 `/alertas` - Alertas de segurança
📊 `/stats` - Estatísticas
🆘 `/help` - Ajuda

---

📢 **100% gratuito | Sem APIs | Conteúdo informativo**
    """
    
    keyboard = [
        [InlineKeyboardButton("💡 Pix", callback_data='pix')],
        [InlineKeyboardButton("🔒 Segurança", callback_data='seguranca')],
        [InlineKeyboardButton("🏦 Bancos", callback_data='bancos')],
        [InlineKeyboardButton("❓ FAQ", callback_data='faq')],
        [InlineKeyboardButton("📢 Anunciar", callback_data='advertise')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command"""
    text = """
📖 **Comandos Disponíveis**

💡 `/pix` - Dicas sobre Pix
🔒 `/seguranca` - Dicas de segurança
🏦 `/bancos` - Melhores bancos digitais
❓ `/faq` - Perguntas frequentes
🔔 `/alertas` - Alertas de segurança
📊 `/stats` - Estatísticas
🆘 `/help` - Ajuda

📢 **Anuncie Conosco!**
Contato: @seu_usuario

✅ **Conteúdo 100% informativo**
❌ **Sem apostas, sem promessas financeiras**
    """
    await update.message.reply_text(text, parse_mode='Markdown')

async def pix_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Pix tips"""
    text = "💡 **Dicas sobre Pix**\n\n"
    
    for tip in PIX_TIPS['basico']:
        text += f"**{tip['title']}**\n{tip['tip']}\n\n"
    
    text += "🚀 Para mais dicas, use os botões abaixo!"
    
    keyboard = [
        [InlineKeyboardButton("🚀 Avançado", callback_data='pix_avancado')],
        [InlineKeyboardButton("🔒 Segurança", callback_data='seguranca')],
        [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def seguranca_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Security tips"""
    text = "🔒 **Dicas de Segurança no Pix**\n\n"
    
    for tip in PIX_TIPS['seguranca']:
        text += f"**{tip['title']}**\n{tip['tip']}\n\n"
    
    text += "⚠️ *Sempre verifique os dados antes de pagar!*"
    
    keyboard = [
        [InlineKeyboardButton("🔔 Alertas", callback_data='alertas')],
        [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def bancos_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bank recommendations"""
    text = "🏦 **Melhores Bancos Digitais**\n\n"
    
    for bank in ONLINE_BANKING_TIPS['melhores_bancos']:
        text += f"**{bank['name']}** {bank['rating']}\n✅ {bank['features']}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("💳 Dicas", callback_data='dicas_bancarias')],
        [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def faq_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """FAQ"""
    text = "❓ **Perguntas Frequentes**\n\n"
    
    for item in PIX_FAQ:
        text += f"**{item['question']}**\n✅ {item['answer']}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def alertas_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Security alerts"""
    text = "🔔 **Alertas de Segurança**\n\n"
    
    for alert in SECURITY_ALERTS:
        emoji = "🔴" if alert['severity'] == "Alto" else "🟡"
        text += f"{emoji} **{alert['title']}**\n📝 {alert['description']}\n📅 {alert['date']}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🔒 Segurança", callback_data='seguranca')],
        [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Statistics"""
    text = """
📊 **Estatísticas do Pix Tips Brasil**

👥 **Membros:** 1,847+
📈 **Crescimento mensal:** +15.2%
💬 **Engajamento:** 9.8%

📱 **Conteúdo mais visto:**
1️⃣ Segurança - 42%
2️⃣ Pix Básico - 30%
3️⃣ Bancos Digitais - 18%

📢 **Anuncie aqui!** 
Contato: @seu_usuario
    """
    
    keyboard = [
        [InlineKeyboardButton("📢 Anunciar", callback_data='advertise')],
        [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

# ============================================
# CALLBACK HANDLERS
# ============================================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'home':
        await start(update, context)
    
    elif query.data == 'pix':
        text = "💡 **Dicas sobre Pix**\n\n"
        for tip in PIX_TIPS['basico']:
            text += f"**{tip['title']}**\n{tip['tip']}\n\n"
        keyboard = [
            [InlineKeyboardButton("🚀 Avançado", callback_data='pix_avancado')],
            [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'pix_avancado':
        text = "🚀 **Pix - Recursos Avançados**\n\n"
        for tip in PIX_TIPS['avancado']:
            text += f"**{tip['title']}**\n{tip['tip']}\n\n"
        keyboard = [
            [InlineKeyboardButton("💡 Pix", callback_data='pix')],
            [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'seguranca':
        text = "🔒 **Dicas de Segurança**\n\n"
        for tip in PIX_TIPS['seguranca']:
            text += f"**{tip['title']}**\n{tip['tip']}\n\n"
        keyboard = [
            [InlineKeyboardButton("🔔 Alertas", callback_data='alertas')],
            [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'bancos':
        text = "🏦 **Melhores Bancos Digitais**\n\n"
        for bank in ONLINE_BANKING_TIPS['melhores_bancos']:
            text += f"**{bank['name']}** {bank['rating']}\n✅ {bank['features']}\n\n"
        keyboard = [
            [InlineKeyboardButton("💳 Dicas", callback_data='dicas_bancarias')],
            [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'dicas_bancarias':
        text = "💳 **Dicas para Bancos Digitais**\n\n"
        for tip in ONLINE_BANKING_TIPS['dicas_bancarias']:
            text += f"**{tip['title']}**\n{tip['tip']}\n\n"
        keyboard = [
            [InlineKeyboardButton("🏦 Bancos", callback_data='bancos')],
            [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'faq':
        text = "❓ **Perguntas Frequentes**\n\n"
        for item in PIX_FAQ:
            text += f"**{item['question']}**\n✅ {item['answer']}\n\n"
        keyboard = [
            [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'alertas':
        text = "🔔 **Alertas de Segurança**\n\n"
        for alert in SECURITY_ALERTS:
            emoji = "🔴" if alert['severity'] == "Alto" else "🟡"
            text += f"{emoji} **{alert['title']}**\n📝 {alert['description']}\n📅 {alert['date']}\n\n"
        keyboard = [
            [InlineKeyboardButton("🔒 Segurança", callback_data='seguranca')],
            [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'stats':
        text = """
📊 **Estatísticas do Pix Tips Brasil**

👥 **Membros:** 1,847+
📈 **Crescimento mensal:** +15.2%
💬 **Engajamento:** 9.8%

📢 **Anuncie aqui!** 
Contato: @seu_usuario
        """
        keyboard = [
            [InlineKeyboardButton("📢 Anunciar", callback_data='advertise')],
            [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'advertise':
        text = """
📢 **Anuncie no Pix Tips Brasil!**

✅ **Vantagens:**
• Alcance: +1.800 membros ativos
• Segmentação: Brasil (75%)
• Engajamento: 9.8%

💰 **Pacotes:**
• 📝 Post patrocinado: R$ 50
• ⭐ Post + destaque: R$ 100
• 📅 Mensal (5 posts): R$ 300

📩 **Contato:** @seu_usuario
        """
        await query.edit_message_text(text, parse_mode='Markdown')

# ============================================
# ERROR HANDLER
# ============================================

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors"""
    logger.error(f"Update {update} caused error: {context.error}")

# ============================================
# MAIN FUNCTION
# ============================================

def main() -> None:
    """Start bot"""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    
    if not token:
        logger.error("❌ No TELEGRAM_BOT_TOKEN found in environment variables!")
        logger.error("Please set: railway variables set TELEGRAM_BOT_TOKEN=your_token")
        return
    
    logger.info("🚀 Pix Tips Brasil bot is starting...")
    logger.info(f"Using token: {token[:10]}...")
    
    try:
        application = Application.builder().token(token).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("pix", pix_command))
        application.add_handler(CommandHandler("seguranca", seguranca_command))
        application.add_handler(CommandHandler("bancos", bancos_command))
        application.add_handler(CommandHandler("faq", faq_command))
        application.add_handler(CommandHandler("alertas", alertas_command))
        application.add_handler(CommandHandler("stats", stats_command))
        
        # Add callback handler
        application.add_handler(CallbackQueryHandler(button_callback))
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        # Start polling
        logger.info("✅ Bot is running! Press Ctrl+C to stop.")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"❌ Error starting bot: {e}")
        raise

if __name__ == '__main__':
    main()
  
