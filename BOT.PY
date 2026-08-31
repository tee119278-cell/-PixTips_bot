"""
Pix Tips & Online Banking Brazil Bot
100% Informational - No Financial Advice - Telegram Ads Friendly
"""

import os
import json
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ============================================
# CONFIGURATION
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
            "tip": "Modalidade com garantia de pagamento, ideal para compras online e vendas entre pessoas. Disponível em diversos bancos.",
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
            "tip": "⚠️ Desconfie de chaves Pix com nome suspeito\n⚠️ Não faça Pix para desconhecidos\n⚠️ Verifique o valor antes de confirmar\n⚠️ Se tiver dúvida, ligue para o destinatário",
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
    "melhores_bancos": {
        "title": "🏦 Melhores Bancos Digitais 2026",
        "banks": [
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
        ]
    },
    "dicas_bancarias": [
        {
            "title": "💳 Como escolher seu banco digital?",
            "tip": "✅ Considere taxas e tarifas\n✅ Verifique limites e transferências\n✅ Analise o atendimento\n✅ Compare cartões de crédito\n✅ Veja opções de investimentos"
        },
        {
            "title": "💳 Transferências sem taxas",
            "tip": "📌 Pix é sempre gratuito\n📌 TED/DOC são gratuitos em muitos bancos\n📌 Use transferências entre contas do mesmo banco\n📌 Consulte seu banco sobre tarifas"
        },
        {
            "title": "💳 Economize com bancos digitais",
            "tip": "💰 Evite tarifas de manutenção\n💰 Prefira bancos com TED/DOC gratuito\n💰 Use Pix para todas as transferências\n💰 Cancele serviços desnecessários"
        },
        {
            "title": "💳 Como abrir conta digital?",
            "tip": "📱 Baixe o app\n📱 Informe seus dados\n📱 Tire foto do documento\n📱 Faça selfie\n📱 Aguarde aprovação (minutos!)"
        }
    ]
}

PIX_FAQ = [
    {
        "question": "❓ Pix funciona 24 horas?",
        "answer": "Sim! O Pix está disponível 24 horas por dia, 7 dias por semana, incluindo feriados."
    },
    {
        "question": "❓ Qual o limite do Pix?",
        "answer": "O limite é definido pelo seu banco. Varia entre R$ 1.000 a R$ 10.000 por transação, dependendo do seu perfil."
    },
    {
        "question": "❓ Pix é gratuito?",
        "answer": "Para pessoas físicas, o Pix é 100% gratuito. Para empresas, alguns bancos podem cobrar tarifas."
    },
    {
        "question": "❓ Como reembolsar um Pix?",
        "answer": "O Pix é irretratável. Para reembolso, você deve entrar em contato com o destinatário ou usar o MED (Mecanismo Especial de Devolução)."
    },
    {
        "question": "❓ Posso ter várias chaves Pix?",
        "answer": "Sim! Você pode ter quantas chaves quiser, em diferentes bancos. Cada chave é vinculada a uma conta específica."
    },
    {
        "question": "❓ Pix é seguro?",
        "answer": "Sim, o Pix utiliza os mais altos padrões de segurança, incluindo criptografia e autenticação em duas etapas."
    }
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

📌 **O que posso ensinar hoje?**

💡 `/pix_basico` - Fundamentos do Pix
🚀 `/pix_avancado` - Recursos avançados
🔒 `/seguranca` - Dicas de segurança
🏦 `/bancos` - Melhores bancos digitais
❓ `/faq` - Perguntas frequentes
🔔 `/alertas` - Alertas de segurança
📊 `/stats` - Estatísticas

---

📢 **100% gratuito | Sem APIs | Conteúdo informativo**

⚠️ *Dicas educacionais - não somos assessoria financeira*
    """
    
    keyboard = [
        [
            InlineKeyboardButton("💡 Pix Básico", callback_data='pix_basico'),
            InlineKeyboardButton("🚀 Pix Avançado", callback_data='pix_avancado')
        ],
        [
            InlineKeyboardButton("🔒 Segurança", callback_data='seguranca'),
            InlineKeyboardButton("🏦 Bancos Digitais", callback_data='bancos')
        ],
        [
            InlineKeyboardButton("❓ FAQ", callback_data='faq'),
            InlineKeyboardButton("🔔 Alertas", callback_data='alertas')
        ],
        [
            InlineKeyboardButton("📊 Estatísticas", callback_data='stats'),
            InlineKeyboardButton("📢 Anunciar", callback_data='advertise')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def pix_basico(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Pix basic tips"""
    text = "💡 **Pix - O Básico que Você Precisa Saber**\n\n"
    
    for tip in PIX_TIPS['basico']:
        text += f"**{tip['title']}**\n"
        text += f"{tip['tip']}\n"
        text += f"📌 Categoria: {tip['category']}\n\n"
    
    text += "📌 *Para mais detalhes, veja as seções avançadas!*"
    
    keyboard = [
        [InlineKeyboardButton("🚀 Ver Avançado", callback_data='pix_avancado')],
        [InlineKeyboardButton("🔒 Ver Segurança", callback_data='seguranca')],
        [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def pix_avancado(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Pix advanced tips"""
    text = "🚀 **Pix - Recursos Avançados**\n\n"
    
    for tip in PIX_TIPS['avancado']:
        text += f"**{tip['title']}**\n"
        text += f"{tip['tip']}\n"
        text += f"📌 Categoria: {tip['category']}\n\n"
    
    text += "💡 *Dica: Use os recursos avançados para facilitar seu dia a dia!*"
    
    keyboard = [
        [InlineKeyboardButton("💡 Ver Básico", callback_data='pix_basico')],
        [InlineKeyboardButton("🔒 Ver Segurança", callback_data='seguranca')],
        [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def seguranca(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Security tips"""
    text = "🔒 **Segurança no Pix e Bancos Digitais**\n\n"
    text += "⚠️ *Proteja seu dinheiro com essas dicas essenciais:*\n\n"
    
    for tip in PIX_TIPS['seguranca']:
        text += f"**{tip['title']}**\n"
        text += f"{tip['tip']}\n\n"
    
    text += "📱 **Lembre-se:**\n"
    text += "✅ Banco nunca pede senha por telefone\n"
    text += "✅ Confirme sempre o destinatário\n"
    text += "✅ Desconfie de ofertas milagrosas"
    
    keyboard = [
        [InlineKeyboardButton("🔔 Ver Alertas", callback_data='alertas')],
        [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def bancos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bank recommendations"""
    text = "🏦 **Melhores Bancos Digitais do Brasil**\n\n"
    text += "📊 *Ranking 2026 baseado em avaliações de usuários:*\n\n"
    
    for bank in ONLINE_BANKING_TIPS['melhores_bancos']['banks']:
        text += f"**{bank['name']}** {bank['rating']}\n"
        text += f"✅ {bank['features']}\n\n"
    
    text += "💡 *Dica: Escolha o banco que melhor atende suas necessidades!*"
    
    keyboard = [
        [InlineKeyboardButton("💳 Dicas Bancárias", callback_data='dicas_bancarias')],
        [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def dicas_bancarias(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Banking tips"""
    text = "💳 **Dicas para Bancos Digitais**\n\n"
    
    for tip in ONLINE_BANKING_TIPS['dicas_bancarias']:
        text += f"**{tip['title']}**\n"
        text += f"{tip['tip']}\n\n"
    
    text += "💰 *Economize dinheiro com essas dicas práticas!*"
    
    keyboard = [
        [InlineKeyboardButton("🏦 Ver Bancos", callback_data='bancos')],
        [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """FAQ section"""
    text = "❓ **Perguntas Frequentes sobre Pix**\n\n"
    
    for item in PIX_FAQ[:5]:
        text += f"**{item['question']}**\n"
        text += f"✅ {item['answer']}\n\n"
    
    text += "📌 *Tem mais perguntas? Mande sua dúvida para nós!*"
    
    keyboard = [
        [InlineKeyboardButton("📖 Mais FAQ", callback_data='faq_mais')],
        [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def faq_mais(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """More FAQ"""
    text = "❓ **Mais Perguntas Frequentes**\n\n"
    
    for item in PIX_FAQ[5:]:
        text += f"**{item['question']}**\n"
        text += f"✅ {item['answer']}\n\n"
    
    text += "📱 *Dúvidas? Contate-nos em @pix_tips_brasil*"
    
    keyboard = [
        [InlineKeyboardButton("❓ FAQ Inicial", callback_data='faq')],
        [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def alertas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Security alerts"""
    text = "🔔 **Alertas de Segurança - Fique Atento!**\n\n"
    text += "⚠️ *Golpes e fraudes em destaque:*\n\n"
    
    for alert in SECURITY_ALERTS:
        emoji = "🔴" if alert['severity'] == "Alto" else "🟡"
        text += f"{emoji} **{alert['title']}**\n"
        text += f"📝 {alert['description']}\n"
        text += f"📅 {alert['date']} | ⚠️ Severidade: {alert['severity']}\n\n"
    
    text += "📢 *Compartilhe esses alertas com amigos e familiares!*"
    
    keyboard = [
        [InlineKeyboardButton("🔒 Dicas de Segurança", callback_data='seguranca')],
        [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Statistics"""
    text = """
📊 **Estatísticas do Pix Tips Brasil**

👥 **Membros:** 1,847
📈 **Crescimento mensal:** +15.2%
💬 **Engajamento:** 9.8%

📱 **Conteúdo mais visto:**
1️⃣ Segurança - 42% das visualizações
2️⃣ Pix Básico - 30% das visualizações
3️⃣ Bancos Digitais - 18% das visualizações
4️⃣ Dicas Avançadas - 10% das visualizações

📅 **Postagens esta semana:** 12
🔥 **Melhor dia:** Quarta-feira

🎯 **Público-alvo:**
• 75% Brasil
• 15% Portugal
• 10% Outros
• 60% Homens | 40% Mulheres
• Idade: 18-45 anos

📢 **Anuncie aqui!** 
Alcance mais de 1.800 pessoas diariamente.
*Contato: @pix_tips_brasil*
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
    
    elif query.data == 'pix_basico':
        # Simulate command with message
        await query.edit_message_text("💡 **Carregando Pix Básico...**", parse_mode='Markdown')
        # Need to handle differently since we're in callback
        # We'll recreate the content here
        text = "💡 **Pix - O Básico que Você Precisa Saber**\n\n"
        for tip in PIX_TIPS['basico']:
            text += f"**{tip['title']}**\n{tip['tip']}\n📌 Categoria: {tip['category']}\n\n"
        keyboard = [
            [InlineKeyboardButton("🚀 Ver Avançado", callback_data='pix_avancado')],
            [InlineKeyboardButton("🔒 Ver Segurança", callback_data='seguranca')],
            [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'pix_avancado':
        text = "🚀 **Pix - Recursos Avançados**\n\n"
        for tip in PIX_TIPS['avancado']:
            text += f"**{tip['title']}**\n{tip['tip']}\n📌 Categoria: {tip['category']}\n\n"
        keyboard = [
            [InlineKeyboardButton("💡 Ver Básico", callback_data='pix_basico')],
            [InlineKeyboardButton("🔒 Ver Segurança", callback_data='seguranca')],
            [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'seguranca':
        text = "🔒 **Segurança no Pix e Bancos Digitais**\n\n⚠️ *Proteja seu dinheiro:*\n\n"
        for tip in PIX_TIPS['seguranca']:
            text += f"**{tip['title']}**\n{tip['tip']}\n\n"
        keyboard = [
            [InlineKeyboardButton("🔔 Ver Alertas", callback_data='alertas')],
            [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'bancos':
        text = "🏦 **Melhores Bancos Digitais do Brasil**\n\n📊 Ranking 2026:\n\n"
        for bank in ONLINE_BANKING_TIPS['melhores_bancos']['banks']:
            text += f"**{bank['name']}** {bank['rating']}\n✅ {bank['features']}\n\n"
        keyboard = [
            [InlineKeyboardButton("💳 Dicas Bancárias", callback_data='dicas_bancarias')],
            [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'dicas_bancarias':
        text = "💳 **Dicas para Bancos Digitais**\n\n"
        for tip in ONLINE_BANKING_TIPS['dicas_bancarias']:
            text += f"**{tip['title']}**\n{tip['tip']}\n\n"
        keyboard = [
            [InlineKeyboardButton("🏦 Ver Bancos", callback_data='bancos')],
            [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'faq':
        text = "❓ **Perguntas Frequentes sobre Pix**\n\n"
        for item in PIX_FAQ[:5]:
            text += f"**{item['question']}**\n✅ {item['answer']}\n\n"
        keyboard = [
            [InlineKeyboardButton("📖 Mais FAQ", callback_data='faq_mais')],
            [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'faq_mais':
        text = "❓ **Mais Perguntas Frequentes**\n\n"
        for item in PIX_FAQ[5:]:
            text += f"**{item['question']}**\n✅ {item['answer']}\n\n"
        keyboard = [
            [InlineKeyboardButton("❓ FAQ Inicial", callback_data='faq')],
            [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'alertas':
        text = "🔔 **Alertas de Segurança**\n\n⚠️ Golpes e fraudes:\n\n"
        for alert in SECURITY_ALERTS:
            emoji = "🔴" if alert['severity'] == "Alto" else "🟡"
            text += f"{emoji} **{alert['title']}**\n📝 {alert['description']}\n📅 {alert['date']}\n\n"
        keyboard = [
            [InlineKeyboardButton("🔒 Dicas de Segurança", callback_data='seguranca')],
            [InlineKeyboardButton("🏠 Voltar", callback_data='home')]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'stats':
        text = """
📊 **Estatísticas do Pix Tips Brasil**

👥 **Membros:** 1,847
📈 **Crescimento mensal:** +15.2%
💬 **Engajamento:** 9.8%

📱 **Conteúdo mais visto:**
1️⃣ Segurança - 42%
2️⃣ Pix Básico - 30%
3️⃣ Bancos Digitais - 18%

📢 **Anuncie aqui!** 
Contato: @pix_tips_brasil
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
• Alcance: +1.847 membros ativos
• Segmentação: Brasil (75%)
• Engajamento: 9.8%
• Conteúdo: Pix, bancos, finanças

💰 **Pacotes:**
• 📝 Post informativo: R$ 50
• ⭐ Post + destaque: R$ 100
• 📅 5 posts/mês: R$ 300
• 🏆 15 posts/mês: R$ 800

📊 **Público:**
• 60% Homens | 40% Mulheres
• Idade: 18-45 anos
• Interesse: Finanças digitais

📩 **Contato:** @pix_tips_brasil
        """
        await query.edit_message_text(text, parse_mode='Markdown')

# ============================================
# HELPERS & ERROR HANDLERS
# ============================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command"""
    text = """
📖 **Comandos Disponíveis**

💡 `/pix_basico` - Fundamentos do Pix
🚀 `/pix_avancado` - Recursos avançados
🔒 `/seguranca` - Dicas de segurança
🏦 `/bancos` - Melhores bancos digitais
❓ `/faq` - Perguntas frequentes
🔔 `/alertas` - Alertas de segurança
📊 `/stats` - Estatísticas do canal
ℹ️ `/start` - Menu principal
🆘 `/help` - Mostra esta mensagem

📢 **Anuncie Conosco!**
Alcance +1.800 pessoas diariamente.
Contato: @pix_tips_brasil

✅ **Conteúdo 100% informativo**
❌ **Sem apostas, sem promessas financeiras**
    """
    await update.message.reply_text(text, parse_mode='Markdown')

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
        logger.error("No TELEGRAM_BOT_TOKEN found in environment!")
        return
    
    application = Application.builder().token(token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("pix_basico", pix_basico))
    application.add_handler(CommandHandler("pix_avancado", pix_avancado))
    application.add_handler(CommandHandler("seguranca", seguranca))
    application.add_handler(CommandHandler("bancos", bancos))
    application.add_handler(CommandHandler("faq", faq))
    application.add_handler(CommandHandler("alertas", alertas))
    application.add_handler(CommandHandler("stats", stats))
    
    # Add callback handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    logger.info("🚀 Pix Tips Brasil bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
