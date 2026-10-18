"""
Master translation synchronization script for RocketBank.
Ensures 100% complete translation coverage across Russian (RU), Kazakh (KK), and English (EN)
for all template strings, PO files, and runtime dictionaries.
"""

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from scripts.compile_mo import compile_all  # noqa: E402

# Complete translation dictionary for all missing and template strings
EXTRA_TRANSLATIONS = {
    # ── Hero, CTA & Trust ──
    "See it in action": ("Как это работает", "Жұмыс барысы"),
    "businesses and clients trust RocketBank": (
        "клиентов и компаний доверяют RocketBank",
        "клиент пен бизнес RocketBank-ке сенеді",
    ),
    "12,000+ businesses and clients trust RocketBank": (
        "12 000+ клиентов и компаний доверяют RocketBank",
        "12 000+ клиент пен бизнес RocketBank-ке сенеді",
    ),
    "12,000+ clients trust RocketBank": (
        "12 000+ клиентов доверяют RocketBank",
        "12 000+ клиент RocketBank-ке сенеді",
    ),
    "Start for free": ("Начать бесплатно", "Тегін бастау"),
    "Open Client Dashboard": ("Открыть кабинет", "Жеке кабинетті ашу"),
    "Now with AI-powered financial insights": (
        "Теперь с финансовой аналитикой на базе ИИ",
        "Енді ЖИ негізіндегі қаржылық талдаумен",
    ),
    "Revenue growth": ("Рост выручки", "Кіріс өсімі"),
    "Settlement time": ("Время расчетов", "Есеп айырысу уақыты"),
    "ROCKETBANK COMMAND CENTER": (
        "КОМАНДНЫЙ ЦЕНТР ROCKETBANK",
        "ROCKETBANK БАСҚАРУ ОРТАЛЫҒЫ",
    ),
    "Balance": ("Баланс", "Теңгерім"),
    "Sent": ("Отправлено", "Жіберілді"),
    "Received": ("Получено", "Алынды"),
    "Volume — 7 days": ("Объем — 7 дней", "Көлемі — 7 күн"),
    "Global Clearing Payout": (
        "Международная выплата клиринга",
        "Халықаралық клиринг төлемі",
    ),
    "Kaspi / Stripe Payout": ("Выплата Kaspi / Stripe", "Kaspi / Stripe төлемі"),
    "Subscription renewal": ("Продление подписки", "Жазылымды жаңарту"),
    "Interbank Multi-Currency Swap": (
        "Межбанковский мультивалютный своп",
        "Банкаралық мультивалюталық своп",
    ),
    "Total volume processed": (
        "Общий обработанный объем",
        "Өңделген жалпы көлем",
    ),
    "Active clients & accounts": (
        "Активных клиентов и счетов",
        "Белсенді клиенттер мен шоттар",
    ),
    "Uptime guarantee": ("Гарантия доступности", "Үздіксіз жұмыс кепілдігі"),
    "Zero downtime recorded": (
        "0 минут сбоев за все время",
        "Үзіліссіз тұрақты жұмыс",
    ),
    "Domestic transfer fees": (
        "Комиссия за внутренние переводы",
        "Ішкі аударымдар комиссиясы",
    ),
    "100% free peer-to-peer": (
        "100% бесплатно между клиентами",
        "Клиенттер арасында 100% тегін",
    ),
    # ── Days of the Week & Relative Dates ──
    "Mon": ("Пн", "Дс"),
    "Tue": ("Вт", "Сс"),
    "Wed": ("Ср", "Ср"),
    "Thu": ("Чт", "Бс"),
    "Fri": ("Пт", "Жм"),
    "Sat": ("Сб", "Сн"),
    "Today": ("Сегодня", "Бүгін"),
    "Yesterday": ("Вчера", "Кеше"),
    "today": ("сегодня", "бүгін"),
    "This month": ("В этом месяце", "Осы айда"),
    "this month": ("в этом месяце", "осы айда"),
    "year over year": (
        "по сравнению с прошлым годом",
        "өткен жылмен салыстырғанда",
    ),
    "countries": ("стран", "ел"),
    "currencies": ("валют", "валюта"),
    "transfers": ("переводов", "аударым"),
    # ── Sticky Features Stack ──
    "Platform features": ("Возможности платформы", "Платформа мүмкіндіктері"),
    "Everything your finances need": (
        "Все необходимое для ваших финансов",
        "Сіздің қаржыңызға қажеттінің барлығы",
    ),
    "One platform to send, receive, track, and multiply your capital. No switching between disjointed tools.": (
        "Единая платформа для переводов, аналитики и приумножения капитала без переключения между разрозненными сервисами.",
        "Қаражатты аударуға, бақылауға және көбейтуге арналған бірыңғай платформа. Бөлек құралдар арасында ауысудың қажеті жоқ.",
    ),
    "Instant transfers": ("Мгновенные переводы", "Лездік аударымдар"),
    "Move money in real-time across domestic and international banking rails with sub-second atomic settlement and zero hidden commissions.": (
        "Переводите средства в реальном времени по внутренним и мировым банковским каналам с мгновенным исполнением и без скрытых комиссий.",
        "Ақшаны ішкі және халықаралық банктік желілер арқылы жасырын комиссиясыз, секундтың үлесінде қауіпсіз аударыңыз.",
    ),
    "Sub-second": ("Доли секунды", "Лездік"),
    "190+ countries": ("190+ стран", "190+ ел"),
    "Zero fees": ("0% комиссий", "0% комиссия"),
    "Smart analytics": ("Умная аналитика", "Ақылды талдау"),
    "AI-powered dashboards that surface what matters. Cashflow forecasting, automated anomaly detection, and real-time expense classification.": (
        "Дашборды с искусственным интеллектом: прогнозирование денежных потоков, автоматическое обнаружение аномалий и классификация расходов.",
        "Жасанды интеллект негізіндегі талдау: ақша ағынын болжау, аномалияларды автоматты анықтау және шығындарды нақты уақытта жіктеу.",
    ),
    "AI forecasting": ("Прогнозы ИИ", "ЖИ болжамы"),
    "Anomaly alerts": ("Оповещения об аномалиях", "Аномалия ескертулері"),
    "Custom reports": ("Пользовательские отчеты", "Арнайы есептер"),
    "Multi-currency accounts": (
        "Мультивалютные счета",
        "Мультивалюталық шоттар",
    ),
    "Hold, convert, and pay in KZT, USD, EUR, GBP, and 30+ currencies at interbank rates. Lock live rates and eliminate foreign exchange loss.": (
        "Храните, обменивайте и оплачивайте в KZT, USD, EUR, GBP и еще 30+ валютах по межбанковскому курсу без скрытых наценок.",
        "KZT, USD, EUR, GBP және 30+ валютада банкаралық бағам бойынша сақтаңыз, айырбастаңыз және төлем жасаңыз.",
    ),
    "35+ currencies": ("35+ валют", "35+ валюта"),
    "Interbank rates": ("Межбанковский курс", "Банкаралық бағам"),
    "Live FX swap": ("Мгновенный FX своп", "Лездік FX своп"),
    "Enterprise security": (
        "Корпоративная безопасность",
        "Корпоративтік қауіпсіздік",
    ),
    "Bank-grade encryption, SOC 2 compliance, KDIF state deposit guarantee up to 20,000,000 KZT, and instant 1-click card freeze.": (
        "Банковское шифрование, соответствие стандарту SOC 2, госгарантия КФГД до 20 000 000 ₸ и моментальная заморозка карты в 1 клик.",
        "Банктік шифрлау, SOC 2 стандарты, ҚДКҚ-ның 20 000 000 теңгеге дейінгі мемлекеттік кепілдігі және картаны 1 басумен лезде бұғаттау.",
    ),
    "KDIF Insured": ("Застраховано КФГД", "ҚДКҚ сақтандырған"),
    "AI fraud detection": (
        "ИИ защита от мошенничества",
        "Алаяқтықтан ЖИ қорғау",
    ),
    "256-bit AES": ("256-битное AES", "256-биттік AES"),
    # ── Right Side Panel Mockups ──
    "Transfers": ("Переводы", "Аударымдар"),
    "Analytics": ("Аналитика", "Талдау"),
    "Multi-currency": ("Мультивалюта", "Мультивалюта"),
    "Security": ("Безопасность", "Қауіпсіздік"),
    "Sent today": ("Отправлено сегодня", "Бүгін жіберілген"),
    "Avg. speed": ("Средняя скорость", "Орташа жылдамдық"),
    "Atomic lock": ("Атомарный лок", "Атомдық қорғау"),
    "Completed": ("Завершено", "Орындалды"),
    "Forecasted balance": ("Прогнозный баланс", "Болжамды теңгерім"),
    "Next 30 days": ("Следующие 30 дней", "Алдағы 30 күн"),
    "Anomalies": ("Аномалии", "Аномалиялар"),
    "All clean": ("Все в норме", "Барлығы дұрыс"),
    "Volume trend — 8 weeks": (
        "Тренд объема — 8 недель",
        "Көлем тренді — 8 апта",
    ),
    "Operations": ("Операции", "Операциялар"),
    "Cross-border": ("Трансграничные", "Халықаралық"),
    "Active Currencies": ("Активные валюты", "Белсенді валюталар"),
    "Multi-IBAN active": ("Мульти-IBAN активен", "Мульти-IBAN белсенді"),
    "FX Saved": ("Экономия на FX", "FX бойынша үнемделген"),
    "Primary": ("Основной", "Негізгі"),
    "KDIF Deposit Guarantee": (
        "Гарантия депозитов КФГД",
        "ҚДКҚ депозиттік кепілдігі",
    ),
    "24/7 SOC": ("Круглосуточный SOC", "Тәулік бойы SOC"),
    "AI Anomaly Guard": ("ИИ защита от аномалий", "ЖИ аномалия күзеті"),
    "Protecting": ("Защита активна", "Қорғалуда"),
    "Online": ("В сети", "Желіде"),
    "Active": ("Активно", "Белсенді"),
    "Guaranteed": ("Гарантировано", "Кепілдендірілген"),
    # ── Live Dashboard Preview ──
    "Live platform": ("Интерактивная платформа", "Интерактивті платформа"),
    "Your financial command center": (
        "Ваш финансовый командный центр",
        "Сіздің қаржылық басқару орталығыңыз",
    ),
    "Real-time liquidity, multi-currency balances, and full control over cards and transfers.": (
        "Ликвидность в реальном времени, мультивалютные балансы и полный контроль над картами и переводами.",
        "Нақты уақыттағы өтімділік, мультивалюталық теңгерімдер және карталар мен аударымдарды толық басқару.",
    ),
    "Portfolio overview": ("Обзор портфеля", "Портфельге шолу"),
    "Live data": ("Данные в реальном времени", "Нақты уақыттағы деректер"),
    "Cash flow": ("Денежный поток", "Ақша ағыны"),
    "Net positive this month": (
        "Положительный баланс за месяц",
        "Осы айдағы оң динамика",
    ),
    "Inbound": ("Поступления", "Түсімдер"),
    "Outbound": ("Списания", "Шығыстар"),
    "Monthly Transactions": ("Транзакций за месяц", "Айлық транзакциялар"),
    "Sub-second execution": ("Мгновенное исполнение", "Лездік орындалу"),
    "Successful": ("Успешные", "Сәтті"),
    "Failed": ("Отклоненные", "Қабылданбаған"),
    # ── Pricing & Card Tiers ──
    "Bank Card Tiers": ("Уровни банковских карт", "Банк карталарының деңгейлері"),
    "Tailored for every ambition": (
        "Создано для любых амбиций",
        "Әрбір мақсат үшін жасалған",
    ),
    "Start with zero maintenance, unlock high-yield privileges and priority concierge.": (
        "Начните с бесплатного обслуживания, открывайте привилегии с высоким доходом и консьерж-сервис.",
        "Тегін қызмет көрсетуден бастап, жоғары кірісті артықшылықтар мен басым консьерж қызметін ашыңыз.",
    ),
    "Monthly": ("В месяц", "Ай сайын"),
    "Annual": ("В год", "Жылдық"),
    "Save 35%": ("Скидка 35%", "35% үнемдеу"),
    "Save 35%%": ("Скидка 35%", "35% үнемдеу"),
    "Gold Card": ("Карта Gold", "Gold Card"),
    "Platinum Card": ("Карта Platinum", "Platinum Card"),
    "Black Card": ("Карта Black", "Black Card"),
    "RocketBank Gold": ("RocketBank Gold", "RocketBank Gold"),
    "RocketBank Platinum": ("RocketBank Platinum", "RocketBank Platinum"),
    "RocketBank Black": ("RocketBank Black", "RocketBank Black"),
    "per month": ("в месяц", "айына"),
    "free forever": ("бесплатно навсегда", "мәңгілікке тегін"),
    "Zero annual maintenance fees": (
        "0 ₸ за годовое обслуживание",
        "Жылдық қызмет көрсету 0 ₸",
    ),
    "per month, billed": ("в месяц, при оплате", "айына, төлем түрі"),
    "monthly": ("ежемесячно", "ай сайын"),
    "annually": ("за год", "жылдық"),
    "billed annually": ("при оплате за год", "жылдық төлем кезінде"),
    "billed": ("списание", "төлем"),
    "Most popular": ("Популярный выбор", "Ең танымал"),
    "Cashback on all purchases": (
        "Кэшбэк на все покупки",
        "Барлық сатып алуларға кэшбэк",
    ),
    "Instant digital & physical issuance": (
        "Мгновенный выпуск цифровой и физической карты",
        "Цифрлық және пластикалық картаны лездік шығару",
    ),
    "Zero fee KZT transfers by IBAN": (
        "Бесплатные переводы в KZT по IBAN",
        "IBAN арқылы теңгемен комиссиясыз аударымдар",
    ),
    "Up to 5 multi-currency accounts": (
        "До 5 мультивалютных счетов",
        "5-ке дейін мультивалюталық шот",
    ),
    "Standard 24/7 chat support": (
        "Стандартная поддержка 24/7 в чате",
        "Чатта тәулік бойы стандартты қолдау",
    ),
    "Cashback on dining & travel": (
        "Кэшбэк в ресторанах и путешествиях",
        "Мейрамханалар мен саяхаттардағы кэшбэк",
    ),
    "Titanium metallic physical card": (
        "Титановая металлическая карта",
        "Титаннан жасалған металл карта",
    ),
    "Airport lounge access (LoungeKey)": (
        "Доступ в бизнес-залы аэропортов (LoungeKey)",
        "Әуежайлардың бизнес-залдарына қолжетімділік (LoungeKey)",
    ),
    "Priority 24/7 dedicated banker": (
        "Персональный банкир 24/7",
        "Жеке банкир 24/7",
    ),
    "15 foreign currencies with zero FX fee": (
        "15 иностранных валют без комиссий за конвертацию",
        "Айырбастау комиссиясынсыз 15 шетелдік валюта",
    ),
    "Extended daily withdrawal limits": (
        "Повышенные суточные лимиты на снятие наличных",
        "Қолма-қол ақша алуға ұлғайтылған тәуліктік лимиттер",
    ),
    "Elite": ("Индивидуально", "Арнайы"),
    "tailored for high net worth": (
        "для премиального капитала",
        "ірі капитал иелеріне арналған",
    ),
    "Unlimited premium cashback": (
        "Неограниченный премиальный кэшбэк",
        "Шектеусіз премиум кэшбэк",
    ),
    "PVD-coated obsidian steel card": (
        "Карта из обсидиановой стали с PVD-покрытием",
        "PVD жабындысы бар обсидиан болат картасы",
    ),
    "Personal executive wealth manager": (
        "Персональный управляющий частным капиталом",
        "Жеке капиталды басқарушы менеджер",
    ),
    "Unlimited international SWIFT transfers": (
        "Безлимитные международные переводы SWIFT",
        "Шектеусіз халықаралық SWIFT аударымдары",
    ),
    "All 35+ global currencies included": (
        "Все 35+ мировых валют без ограничений",
        "Барлық 35+ әлемдік валюта қамтылған",
    ),
    "Custom credit limits up to ₸50,000,000": (
        "Индивидуальный кредитный лимит до ₸50,000,000",
        "₸50 000 000-ға дейінгі жеке несиелік лимит",
    ),
    "Order Gold Card": ("Оформить Gold", "Gold картасын ашу"),
    "Order Platinum Card": ("Оформить Platinum", "Platinum картасын ашу"),
    "Request Black Card": ("Запросить Black", "Black картасына өтінім беру"),
    "Compare Other Tiers": ("Сравнить другие карты", "Басқа карталарды салыстыру"),
    "Other Available Card Tiers": (
        "Другие доступные карты",
        "Басқа қолжетімді карталар",
    ),
    "Filter by tier": ("Фильтр по уровню", "Деңгей бойынша сүзу"),
    "Search cards": ("Поиск карт", "Карталарды іздеу"),
    "Search cards by name...": (
        "Поиск карт по названию...",
        "Карталарды атауы бойынша іздеу...",
    ),
    "Sort cards": ("Сортировка карт", "Карталарды сұрыптау"),
    "Highest Cashback": ("Максимальный кэшбэк", "Ең жоғары кэшбэк"),
    "Lowest Annual Fee": (
        "Минимальная годовая плата",
        "Ең төменгі жылдық төлем",
    ),
    "My Payment Cards": ("Мои банковские карты", "Менің төлем карталарым"),
    "My Payment Cards | RocketBank": (
        "Мои банковские карты | RocketBank",
        "Менің төлем карталарым | RocketBank",
    ),
    "RocketBank Payment Cards": (
        "Банковские карты RocketBank",
        "RocketBank төлем карталары",
    ),
    "Order New Card (Wizard)": (
        "Заказать новую карту (Мастер)",
        "Жаңа картаға тапсырыс беру (Шебер)",
    ),
    "Freeze card": ("Заморозить карту", "Картаны бұғаттау"),
    "Unfreeze card": ("Разморозить карту", "Картаны бұғаттан шығару"),
    "No hidden maintenance costs": (
        "Без скрытых комиссий за обслуживание",
        "Жасырын қызмет ақысыз",
    ),
    "Explore RocketBank's premium debit and credit cards with up to 10% cashback, zero maintenance fee, and instant digital issuing.": (
        "Премиальные дебетовые и кредитные карты RocketBank с кэшбэком до 10%, бесплатным обслуживанием и мгновенным цифровым выпуском.",
        "RocketBank-тің 10%-ға дейін кэшбэгі, тегін қызмет көрсетуі және лездік цифрлық шығарылымы бар премиум дебеттік және несиелік карталары.",
    ),
    "Explore RocketBank's premium debit and credit cards with up to 10%% cashback, zero maintenance fee, and instant digital issuing.": (
        "Премиальные дебетовые и кредитные карты RocketBank с кэшбэком до 10%, бесплатным обслуживанием и мгновенным цифровым выпуском.",
        "RocketBank-тің 10%-ға дейін кэшбэгі, тегін қызмет көрсетуі және лездік цифрлық шығарылымы бар премиум дебеттік және несиелік карталары.",
    ),
    # ── Security Section ──
    "Bank-grade protection": (
        "Банковский уровень защиты",
        "Банктік деңгейдегі қорғаныс",
    ),
    "Security is not a feature — it's the foundation": (
        "Безопасность — это не просто функция, это фундамент",
        "Қауіпсіздік — бұл жай ғана функция емес, бұл негіз",
    ),
    "Every transaction is shielded by multiple layers of enterprise-grade cryptographic security. We are audited, regulated, and monitored around the clock.": (
        "Каждая транзакция защищена многоуровневым криптографическим шифрованием корпоративного класса. Мы проходим аудит, регулируемся и круглосуточно находимся под защитой.",
        "Әрбір транзакция корпоративтік деңгейдегі криптографиялық шифрлаудың бірнеше деңгейімен қорғалған. Біз аудиттелген, реттелген және тәулік бойы бақылаудамыз.",
    ),
    "Read architecture report": (
        "Отчет об архитектуре",
        "Архитектуралық есеп",
    ),
    "Insured up to 20,000,000 KZT per depositor": (
        "Застраховано до 20 000 000 ₸ на каждого вкладчика",
        "Әрбір салымшы үшін 20 000 000 ₸ дейін сақтандырылған",
    ),
    "PCI DSS Level 1": ("PCI DSS Уровень 1", "PCI DSS 1-деңгейі"),
    "Highest tier of international payment card security": (
        "Высший международный уровень безопасности банковских карт",
        "Төлем карталары қауіпсіздігінің ең жоғары халықаралық деңгейі",
    ),
    "Compliant": ("Соответствует", "Сәйкес келеді"),
    "ISO 27001": ("ISO 27001", "ISO 27001"),
    "Global standard for information security management": (
        "Глобальный стандарт управления информационной безопасностью",
        "Ақпараттық қауіпсіздікті басқарудың ғаламдық стандарты",
    ),
    "Certified": ("Сертифицирован", "Сертификатталған"),
    "AI Fraud Shield": (
        "ИИ защита от мошенничества",
        "ЖИ антифрод жүйесі",
    ),
    "Blocks 99.98% of fraudulent attempts in sub-seconds": (
        "Блокирует 99.98% попыток мошенничества за доли секунды",
        "Алаяқтық әрекеттердің 99.98%-ын секундтың үлесінде бұғаттайды",
    ),
    "Always on": ("Всегда активно", "Әрдайым қосулы"),
    # ── Testimonials ──
    "Client experiences": ("Отзывы клиентов", "Клиенттердің пікірлері"),
    "Trusted by leaders across industries": (
        "Нам доверяют лидеры различных отраслей",
        "Бізге түрлі сала көшбасшылары сенеді",
    ),
    "Pause": ("Пауза", "Кідірту"),
    "Play": ("Воспроизвести", "Ойнату"),
    "Pause testimonials": ("Приостановить отзывы", "Пікірлерді кідірту"),
    "CFO at Hive Commerce": (
        "CFO в Hive Commerce",
        "Hive Commerce қаржы директоры",
    ),
    "RocketBank cut our corporate international settlement time from 3 days to under 2 seconds. It completely redefined our treasury speed.": (
        "RocketBank сократил время наших международных расчетов с 3 дней до 2 секунд. Это полностью изменило скорость управления нашим капиталом.",
        "RocketBank халықаралық төлемдеріміздің мерзімін 3 күннен 2 секундқа дейін қысқартты. Бұл біздің қаржылық айналым жылдамдығымызды түбегейлі өзгертті.",
    ),
    "Finance Director, Nomad Labs": (
        "Финансовый директор, Nomad Labs",
        "Nomad Labs қаржы директоры",
    ),
    "The multi-currency IBAN accounts saved us over ₸18M in FX conversions this year. The exchange rate transparency is unparalleled.": (
        "Мультивалютные счета IBAN сэкономили нам более ₸18 млн на конвертациях в этом году. Прозрачность обменного курса безупречна.",
        "Мультивалюталық IBAN шоттары биыл бізге валюта айырбастаудан ₸18 млн астам қаржы үнемдеді. Бағамдардың ашықтығы тамаша.",
    ),
    "Head of Ops, Stackflow": (
        "Операционный директор, Stackflow",
        "Stackflow операциялық директоры",
    ),
    "Finally a modern digital banking platform that feels ultra-fast and engineered for modern engineers and tech businesses.": (
        "Наконец-то появился современный цифровой банк, работающий молниеносно и созданный специально для IT-компаний и технологичного бизнеса.",
        "Ақырында IT-компаниялар мен заманауи бизнеске арналған, өте жылдам жұмыс істейтін цифрлық банк пайда болды.",
    ),
    "CTO at Vaulted": (
        "Технический директор Vaulted",
        "Vaulted техникалық директоры",
    ),
    "Migrated our business accounts in one afternoon. The REST API documentation and instant webhooks are exceptional.": (
        "Перевели наши бизнес-счета за один день. Документация REST API и мгновенные вебхуки работают безупречно.",
        "Барлық бизнес-шоттарымызды бір күнде көшірдік. REST API құжаттамасы мен лездік вебхуктер өте керемет жасалған.",
    ),
    "Founder, CloudMint": (
        "Основатель CloudMint",
        "CloudMint негізін қалаушы",
    ),
    "The automated fraud detection and instant card freeze give our executive team complete peace of mind.": (
        "Автоматическая система предотвращения мошенничества и мгновенная блокировка карт дают полное спокойствие нашему руководству.",
        "Алаяқтықты автоматты түрде анықтау және картаны бірден бұғаттау біздің басшылыққа толық сенімділік береді.",
    ),
    "Controller, Drift Studio": (
        "Финансовый контролер, Drift Studio",
        "Drift Studio қаржы бақылаушысы",
    ),
    "Automated payroll and batch payments save our accounting team over 25 hours every month.": (
        "Автоматическая зарплатная ведомость и реестровые платежи экономят нашей бухгалтерии более 25 часов каждый месяц.",
        "Жалақыны автоматты төлеу және жаппай аударымдар біздің есепшілерге ай сайын 25 сағаттан астам уақытты үнемдейді.",
    ),
    # ── Mobile App ──
    "Mobile app": ("Мобильное приложение", "Мобильді қосымша"),
    "Your bank, in your pocket": (
        "Ваш банк всегда под рукой",
        "Сіздің банкіңіз әрқашан қалтаңызда",
    ),
    "Full dashboard access, biometric approval for high-value transfers, and instant transaction push notifications — anywhere in the world.": (
        "Полный доступ к счетам, биометрическое подтверждение крупных переводов и мгновенные push-уведомления — в любой точке мира.",
        "Шоттарға толық қолжетімділік, ірі аударымдарды биометриялық растау және лездік push-хабарламалар — әлемнің кез келген нүктесінде.",
    ),
    "Download on the": ("Загрузите в", "Жүктеп алыңыз:"),
    "Get it on": ("Доступно в", "Қолжетімді:"),
    "Or scan our": ("Или отсканируйте", "Немесе сканерлеңіз:"),
    "Available for iOS & Android": (
        "Доступно для iOS и Android",
        "iOS және Android үшін қолжетімді",
    ),
    # ── FAQ ──
    "Got questions?": ("Есть вопросы?", "Сұрақтарыңыз бар ма?"),
    "Frequently asked": (
        "Часто задаваемые вопросы",
        "Жиі қойылатын сұрақтар",
    ),
    "Expand all": ("Развернуть все", "Барлығын ашу"),
    "Collapse all": ("Свернуть все", "Барлығын жинау"),
    "How quickly can I open an account and start sending payments?": (
        "Как быстро я могу открыть счет и начать переводить деньги?",
        "Шотты қаншалықты жылдам ашып, төлемдерді бастауға болады?",
    ),
    "You can be up and running in under 3 minutes. Register your account online, verify with instant biometric/document check, and start transacting with zero paperwork.": (
        "Вы можете начать работу менее чем за 3 минуты. Зарегистрируйтесь онлайн, пройдите быструю биометрическую проверку и совершайте платежи без бумажной волокиты.",
        "Сіз 3 минуттан аз уақыт ішінде бастай аласыз. Онлайн тіркеліп, жылдам биометриялық тексеруден өтіңіз және құжаттарсыз төлемдерді жасаңыз.",
    ),
    "What are the transaction fees for domestic and global transfers?": (
        "Каковы комиссии за внутренние и международные переводы?",
        "Ішкі және халықаралық аударымдар үшін комиссия қандай?",
    ),
    "All standard domestic transfers and peer-to-peer RocketBank transfers are 100% free with 0.00 KZT commission. Multi-currency international rails start at interbank live FX rates with zero hidden markups.": (
        "Все стандартные внутренние переводы и переводы между клиентами RocketBank бесплатны с комиссией 0,00 ₸. Международные переводы производятся по межбанковским курсам без скрытых наценок.",
        "RocketBank ішіндегі барлық стандартты ішкі және клиент арасындағы аударымдар 0,00 ₸ комиссиямен 100% тегін. Халықаралық аударымдар жасырын үстемеақысыз тікелей банкаралық бағамдар бойынша жүргізіледі.",
    ),
    "Are deposits insured by the Kazakhstan Deposit Insurance Fund?": (
        "Застрахованы ли депозиты Казахстанским фондом гарантирования депозитов?",
        "Депозиттер Қазақстанның депозиттерге кепілдік беру қорымен сақтандырылған ба?",
    ),
    "Yes. All deposits held in RocketBank are fully guaranteed up to 20,000,000 KZT per depositor in savings deposits by the KDIF under the laws of the Republic of Kazakhstan.": (
        "Да. Все сберегательные депозиты в RocketBank застрахованы на сумму до 20 000 000 ₸ на каждого вкладчика КФГД в соответствии с законодательством Республики Казахстан.",
        "Иә. RocketBank-тегі барлық жинақ депозиттеріне Қазақстан Республикасының заңнамасына сәйкес ҚДКҚ тарапынан әрбір салымшыға 20 000 000 ₸ дейін толық мемлекеттік кепілдік беріледі.",
    ),
    "How does RocketBank protect client funds and cards from fraud?": (
        "Как RocketBank защищает средства клиентов и карты от мошенничества?",
        "RocketBank клиенттердің қаражаты мен карталарын алаяқтықтан қалай қорғайды?",
    ),
    "We employ bank-grade 256-bit AES encryption, row-level ACID transactional concurrency locks, SOC 2 compliance, and AI-powered real-time anomaly detection to block fraud instantly.": (
        "Мы используем 256-битное шифрование AES банковского уровня, блокировки транзакций ACID на уровне строк, соответствие стандарту SOC 2 и ИИ-анализ аномалий в реальном времени.",
        "Біз банктік деңгейдегі 256-биттік AES шифрлауын, қатар деңгейіндегі ACID транзакциялық құлыптарын, SOC 2 стандартын және алаяқтықты лезде бұғаттау үшін ЖИ мониторингін қолданамыз.",
    ),
    "Can I integrate RocketBank with accounting tools and REST APIs?": (
        "Могу ли я интегрировать RocketBank с бухгалтерскими системами и REST API?",
        "RocketBank-ті бухгалтерлік бағдарламалармен және REST API-мен біріктіруге бола ма?",
    ),
    "Yes! RocketBank provides a full OpenAPI 3.0 / Swagger REST API with JWT authentication, webhook notifications, and automated export tools for finance and ERP platforms.": (
        "Да! RocketBank предоставляет полный REST API (OpenAPI 3.0 / Swagger) с JWT-аутентификацией, вебхуками и автоматическим экспортом в учетные и ERP-системы.",
        "Иә! RocketBank қаржылық және ERP жүйелері үшін JWT аутентификациясы, вебхук хабарламалары және автоматты экспорт құралдары бар толық OpenAPI 3.0 / Swagger REST API ұсынады.",
    ),
    "How can I freeze my bank card if it is lost or compromised?": (
        "Как заблокировать карту при утере или компрометации?",
        "Карта жоғалған немесе деректері бұзылған жағдайда оны қалай бұғаттауға болады?",
    ),
    "You can freeze or unfreeze any debit or credit card instantly from your Client Dashboard or mobile interface with a single tap, blocking all physical and online transactions immediately.": (
        "Вы можете мгновенно заморозить или разморозить любую карту в личном кабинете или мобильном приложении одним нажатием, мгновенно заблокировав все операции.",
        "Сіз кез келген дебеттік немесе несиелік картаны клиенттік кабинеттен немесе мобильді қосымшадан бір басумен лезде бұғаттай немесе бұғаттан шығара аласыз.",
    ),
    # ── Accounts, Dashboard & Quick Actions ──
    "My Bank Accounts | RocketBank": (
        "Мои банковские счета | RocketBank",
        "Менің банктік шоттарым | RocketBank",
    ),
    "List of client accounts registered under your name in RocketBank": (
        "Список счетов, открытых на ваше имя в RocketBank",
        "RocketBank-те сіздің атыңызға ашылған шоттар тізімі",
    ),
    "Open RocketBank Account": (
        "Открыть счет в RocketBank",
        "RocketBank шотын ашу",
    ),
    "Open an Account | RocketBank": (
        "Открыть счет | RocketBank",
        "Шот ашу | RocketBank",
    ),
    "Open account in 3 minutes": (
        "Открытие счета за 3 минуты",
        "Шотты 3 минутта ашу",
    ),
    "Checking Balance": ("Баланс текущего счета", "Ағымдағы шот теңгерімі"),
    "Savings Balance": ("Баланс сберегательного счета", "Жинақ шотының теңгерімі"),
    "Opened Date": ("Дата открытия", "Ашылған күні"),
    "SAVING GOALS": ("ЦЕЛИ НАКОПЛЕНИЙ", "ЖИНАҚ МАҚСАТТАРЫ"),
    "Saving Goals Tracker": (
        "Трекер целей накоплений",
        "Жинақ мақсаттары трекері",
    ),
    "Active Saving Goals": (
        "Активные цели накоплений",
        "Белсенді жинақ мақсаттары",
    ),
    "Monthly budget expenditure meter": (
        "Индикатор расходов ежемесячного бюджета",
        "Айлық бюджет шығыстарының өлшегіші",
    ),
    "Critical (>85%)": ("Критический (>85%)", "Қауіпті (>85%)"),
    "Critical (>85%%)": ("Критический (>85%)", "Қауіпті (>85%)"),
    "Optimal (<60%)": ("Оптимальный (<60%)", "Оңтайлы (<60%)"),
    "Optimal (<60%%)": ("Оптимальный (<60%)", "Оңтайлы (<60%)"),
    "QUICK SERVICES": ("БЫСТРЫЕ ОПЕРАЦИИ", "ЖЫЛДАМ ҚЫЗМЕТТЕР"),
    "Instant Money Transfer": (
        "Мгновенный перевод денег",
        "Лездік ақша аударымы",
    ),
    "Saved Beneficiaries": (
        "Сохраненные получатели",
        "Сақталған алушылар",
    ),
    "Payment Products": ("Платежные продукты", "Төлем өнімдері"),
    "RECENT TRANSACTIONS": (
        "ПОСЛЕДНИЕ ТРАНЗАКЦИИ",
        "СОҢҒЫ ТРАНЗАКЦИЯЛАР",
    ),
    "Full History": ("Вся история", "Толық тарих"),
    "Support Tickets": (
        "Обращения в поддержку",
        "Қолдау қызметіне өтініштер",
    ),
    "Profile & Settings": ("Профиль и настройки", "Профиль және баптаулар"),
    "Dashboard | RocketBank": ("Кабинет | RocketBank", "Кабинет | RocketBank"),
    "RocketBank client dashboard. View financial balances, multi-currency accounts, and recent transactions.": (
        "Личный кабинет RocketBank. Просматривайте финансовые балансы, мультивалютные счета и историю операций.",
        "RocketBank клиенттік кабинеті. Қаржылық теңгерімді, мультивалюталық шоттарды және соңғы операцияларды қараңыз.",
    ),
    "Financial Analytics & Goals": (
        "Финансовая аналитика и цели",
        "Қаржылық талдау және мақсаттар",
    ),
    # ── Deposits & Loans ──
    "Open Term Deposit": ("Открыть срочный депозит", "Мерзімді депозит ашу"),
    "Daily capitalization active": (
        "Ежедневная капитализация активна",
        "Күнделікті капитализация белсенді",
    ),
    "High-yield savings and term deposits with up to 18% annual return, daily capitalization, and state insurance protection up to 20M KZT.": (
        "Высокодоходные сберегательные и срочные депозиты со ставкой до 18% годовых, ежедневной капитализацией и госгарантией КФГД до 20 млн тенге.",
        "Жылдық 18%-ға дейінгі мөлшерлемесі, күнделікті капитализациясы және 20 млн теңгеге дейін ҚДКҚ мемлекеттік кепілдігі бар жинақ және мерзімді депозиттер.",
    ),
    "High-yield savings and term deposits with up to 18%% annual return, daily capitalization, and state insurance protection up to 20M KZT.": (
        "Высокодоходные сберегательные и срочные депозиты со ставкой до 18% годовых, ежедневной капитализацией и госгарантией КФГД до 20 млн тенге.",
        "Жылдық 18%-ға дейінгі мөлшерлемесі, күнделікті капитализациясы және 20 млн теңгеге дейін ҚДКҚ мемлекеттік кепілдігі бар жинақ және мерзімді депозиттер.",
    ),
    "Maximize your savings with compound daily interest, flexible top-up options, and 100% state deposit guarantee by KDIF.": (
        "Умножайте сбережения с ежедневным сложным процентом, гибким пополнением и 100% государственной гарантией КФГД.",
        "Күнделікті күрделі пайызбен, икемді толықтырумен және ҚДКҚ-ның 100% мемлекеттік кепілдігімен жинақтарыңызды көбейтіңіз.",
    ),
    "Maximize your savings with compound daily interest, flexible top-up options, and 100%% state deposit guarantee by KDIF.": (
        "Умножайте сбережения с ежедневным сложным процентом, гибким пополнением и 100% государственной гарантией КФГД.",
        "Күнделікті күрделі пайызбен, икемді толықтырумен және ҚДКҚ-ның 100% мемлекеттік кепілдігімен жинақтарыңызды көбейтіңіз.",
    ),
    "Paid automatically on the 1st": (
        "Выплачивается 1-го числа каждого месяца",
        "Әр айдың 1-жұлдызында төленеді",
    ),
    # ── Auth & Users ──
    "Sign In Now": ("Войти сейчас", "Қазір кіру"),
    "Sign In to Portal": ("Вход в личный кабинет", "Порталға кіру"),
    "Sign In | RocketBank": ("Вход | RocketBank", "Кіру | RocketBank"),
    "Sign in here": ("Войдите здесь", "Осында кіріңіз"),
    "Sign in securely to your RocketBank account to manage cards, accounts, and payments.": (
        "Безопасный вход в аккаунт RocketBank для управления картами, счетами и платежами.",
        "Карталарды, шоттарды және төлемдерді басқару үшін RocketBank аккаунтына қауіпсіз кіріңіз.",
    ),
    "Create My Account": ("Создать аккаунт", "Аккаунт ашу"),
    "Don't have a RocketBank account?": (
        "Еще нет счета в RocketBank?",
        "RocketBank-те әлі шотыңыз жоқ па?",
    ),
    "Register for RocketBank and gain access to multi-currency IBAN accounts, cashback debit cards, and instant transfers.": (
        "Зарегистрируйтесь в RocketBank и получите доступ к мультивалютным счетам IBAN, дебетовым картам с кэшбэком и мгновенным переводам.",
        "RocketBank-ке тіркеліп, мультивалюталық IBAN шоттарына, кэшбэгі бар дебеттік карталарға және лездік аударымдарға қол жеткізіңіз.",
    ),
    "Email or Username": ("Email или имя пользователя", "Email немесе логин"),
    "Username": ("Имя пользователя", "Пайдаланушы аты"),
    "Phone Number": ("Номер телефона", "Телефон нөмірі"),
    "Security Password": ("Пароль безопасности", "Қауіпсіздік құпиясөзі"),
    "New Password": ("Новый пароль", "Жаңа құпиясөз"),
    "Confirm New Password": (
        "Подтвердите новый пароль",
        "Жаңа құпиясөзді растаңыз",
    ),
    "Change Password": ("Изменить пароль", "Құпиясөзді өзгерту"),
    "Password Changed Successfully!": (
        "Пароль успешно изменен!",
        "Құпиясөз сәтті өзгертілді!",
    ),
    "Password Changed | RocketBank": (
        "Пароль изменен | RocketBank",
        "Құпиясөз өзгертілді | RocketBank",
    ),
    "Forgot Your Password?": ("Забыли пароль?", "Құпиясөзді ұмыттыңыз ба?"),
    "Reset Password | RocketBank": (
        "Восстановление пароля | RocketBank",
        "Құпиясөзді қалпына келтіру | RocketBank",
    ),
    "Reset Link Sent | RocketBank": (
        "Ссылка для сброса отправлена | RocketBank",
        "Сілтеме жіберілді | RocketBank",
    ),
    "Password Reset Link Expired": (
        "Срок действия ссылки истек",
        "Сілтеменің мерзімі аяқталды",
    ),
    "Request a New Link": ("Запросить новую ссылку", "Жаңа сілтеме сұрау"),
    "Return to Sign In": ("Вернуться ко входу", "Кіруге оралу"),
    "name@example.com": ("name@example.com", "name@example.com"),
    "name@company.com or username": (
        "name@company.com или логин",
        "name@company.com немесе логин",
    ),
    "username": ("логин", "логин"),
    # ── General & Validation ──
    "Modern Digital Banking": (
        "Современный цифровой банкинг",
        "Заманауи цифрлық банкинг",
    ),
    "Experience effortless banking with high-yield deposits, zero-fee multi-currency transfers, and modern security.": (
        "Ощутите легкость банкинга с высокодоходными депозитами, бесплатными мультивалютными переводами и современной защитой.",
        "Жоғары кірісті депозиттер, комиссиясыз мультивалюталық аударымдар және сенімді қорғаныспен банктік қызметтің жеңілдігін сезініңіз.",
    ),
    "Security & Guarantee": ("Безопасность и гарантии", "Қауіпсіздік және кепілдіктер"),
    "Terms": ("Условия", "Шарттар"),
    "Privacy": ("Конфиденциальность", "Құпиялылық"),
    "Adapted from": ("Адаптировано на основе", "Негізінде бейімделген"),
    "Welcome": ("Добро пожаловать", "Қош келдіңіз"),
    "Details": ("Детали", "Толық мәлімет"),
    "Date": ("Дата", "Күні"),
    "Type": ("Тип", "Түрі"),
    "View All": ("Посмотреть все", "Барлығын көру"),
    "Multi-currency enabled": (
        "Мультивалюта включена",
        "Мультивалюта қосылған",
    ),
    "Rating must be between 1 and 5. Got %(value)s.": (
        "Оценка должна быть от 1 до 5. Получено: %(value)s.",
        "Бағалау 1 мен 5 аралығында болуы керек. Берілгені: %(value)s.",
    ),
    "Image file size cannot exceed %(max)s MB. Got %(actual).1f MB.": (
        "Размер изображения не должен превышать %(max)s МБ. Текущий размер: %(actual).1f МБ.",
        "Сурет файлының өлшемі %(max)s МБ-тан аспауы керек. Қазіргі өлшемі: %(actual).1f МБ.",
    ),
    "24/7 Client Relations": (
        "Клиентский сервис 24/7",
        "Клиенттерге тәулік бойы қызмет көрсету",
    ),
    "24/7 Priority Emergency Line": (
        "Приоритетная линия экстренной связи 24/7",
        "Тәулік бойы шұғыл байланыс желісі",
    ),
    "Al-Farabi Avenue 77/7, Bostandyk District": (
        "Проспект Аль-Фараби 77/7, Бостандыкский район",
        "Әл-Фараби даңғылы 77/7, Бостандық ауданы",
    ),
    "Account": ("Счет", "Шот"),
    "Accounts": ("Счета", "Шоттар"),
    "Actions": ("Действия", "Әрекеттер"),
    "Active Accounts": ("Активные счета", "Белсенді шоттар"),
    "All Categories": ("Все категории", "Барлық санаттар"),
    "All Statuses": ("Все статусы", "Барлық мәртебелер"),
    "IBAN": ("IBAN", "IBAN"),
    "Sarah Kim": ("Сара Ким", "Сара Ким"),
    "James Adler": ("Джеймс Адлер", "Джеймс Адлер"),
    "Priya Mehta": ("Прия Мехта", "Прия Мехта"),
    "Tom Brennan": ("Том Бреннан", "Том Бреннан"),
    "Liu Wei": ("Лю Вэй", "Лю Вэй"),
    "Amara Osei": ("Амара Осей", "Амара Осей"),
}


def escape_str(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", '\\n"\n"')


def sync_all():
    from apps.core.translations import TRANSLATIONS_CATALOG
    from scripts.update_translations import TRANSLATIONS

    # 1. Merge EXTRA_TRANSLATIONS into TRANSLATIONS and TRANSLATIONS_CATALOG
    combined_dict = dict(TRANSLATIONS)
    combined_dict.update(EXTRA_TRANSLATIONS)

    # Also build dictionary of catalog
    for key, (ru_val, kk_val) in combined_dict.items():
        if key not in TRANSLATIONS_CATALOG:
            TRANSLATIONS_CATALOG[key] = {
                "en": key,
                "ru": ru_val,
                "kk": kk_val,
            }
        else:
            if not TRANSLATIONS_CATALOG[key].get("ru"):
                TRANSLATIONS_CATALOG[key]["ru"] = ru_val
            if not TRANSLATIONS_CATALOG[key].get("kk"):
                TRANSLATIONS_CATALOG[key]["kk"] = kk_val

    # 2. Update PO files: ru, kk, en
    for lang, filepath in [
        ("ru", BASE_DIR / "locale/ru/LC_MESSAGES/django.po"),
        ("kk", BASE_DIR / "locale/kk/LC_MESSAGES/django.po"),
        ("en", BASE_DIR / "locale/en/LC_MESSAGES/django.po"),
    ]:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.splitlines(keepends=True)
        out_lines = []
        seen_msgids = set()
        current_msgid = ""

        i = 0
        while i < len(lines):
            line = lines[i]

            if line.startswith("msgid "):
                raw_val = line[6:].strip()
                current_msgid = eval(raw_val)
                out_lines.append(line)
                i += 1
                while i < len(lines) and lines[i].startswith('"'):
                    current_msgid += eval(lines[i].strip())
                    out_lines.append(lines[i])
                    i += 1
                seen_msgids.add(current_msgid)
                continue

            elif line.startswith("msgstr "):
                if current_msgid and current_msgid in combined_dict:
                    ru_val, kk_val = combined_dict[current_msgid]
                    chosen = (
                        ru_val
                        if lang == "ru"
                        else (kk_val if lang == "kk" else current_msgid)
                    )
                    if "\n" in chosen:
                        out_lines.append('msgstr ""\n')
                        for part in chosen.split("\n"):
                            out_lines.append(f'"{escape_str(part)}\\n"\n')
                    else:
                        out_lines.append(f'msgstr "{escape_str(chosen)}"\n')
                elif current_msgid and lang == "en":
                    out_lines.append(f'msgstr "{escape_str(current_msgid)}"\n')
                else:
                    out_lines.append(line)

                i += 1
                while i < len(lines) and lines[i].startswith('"'):
                    if current_msgid and (
                        current_msgid in combined_dict or lang == "en"
                    ):
                        i += 1
                    else:
                        out_lines.append(lines[i])
                        i += 1
                current_msgid = ""
                continue

            out_lines.append(line)
            i += 1

        # Append any missing keys that weren't in the PO file yet
        for msgid, (ru_val, kk_val) in combined_dict.items():
            if msgid not in seen_msgids:
                chosen = (
                    ru_val
                    if lang == "ru"
                    else (kk_val if lang == "kk" else msgid)
                )
                out_lines.append(f'\nmsgid "{escape_str(msgid)}"\n')
                if "\n" in chosen:
                    out_lines.append('msgstr ""\n')
                    for part in chosen.split("\n"):
                        out_lines.append(f'"{escape_str(part)}\\n"\n')
                else:
                    out_lines.append(f'msgstr "{escape_str(chosen)}"\n')
                seen_msgids.add(msgid)

        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(out_lines)
        print(f"Updated {filepath.name} for lang={lang} (total {len(seen_msgids)} msgids)")

    # 3. Update apps/core/translations.py with full catalog
    cat_code = (
        '"""\nZero-dependency Trilingual Translation Dictionary (RU, KK, EN) for RocketBank.\n'
        "Ensures immediate, flawless UI translation across all pages and views.\n"
        '"""\n\nfrom django.utils.translation import get_language, gettext\n\n'
    )
    cat_code += "TRANSLATIONS_CATALOG = " + json.dumps(
        TRANSLATIONS_CATALOG, indent=4, ensure_ascii=False
    )
    cat_code += """


def t(key, lang=None):
    \"\"\"
    Returns translated text for `key` in `lang` (defaults to active django language).
    Falls back to non-empty translation: requested lang -> Russian -> English original -> key.
    NEVER returns empty string when key is non-empty.
    \"\"\"
    if not key:
        return ""

    if not lang:
        lang = get_language() or "ru"
    lang = lang.lower()
    if lang not in ("ru", "kk", "en"):
        lang = "ru"

    # 1. Direct dictionary match
    entry = TRANSLATIONS_CATALOG.get(key)
    if entry:
        val = entry.get(lang)
        if val and val.strip():
            return val
        fallback = entry.get("en") or entry.get("ru")
        if fallback and fallback.strip():
            return fallback

    # 2. Case-insensitive / stripped match in catalog
    key_clean = key.strip().lower()
    for k, val in TRANSLATIONS_CATALOG.items():
        if k.strip().lower() == key_clean:
            v = val.get(lang)
            if v and v.strip():
                return v
            fallback = val.get("en") or val.get("ru")
            if fallback and fallback.strip():
                return fallback

    # 3. Fallback to Django gettext
    try:
        translated = gettext(key)
        if translated and translated.strip():
            return translated
    except Exception:
        pass

    return key


class TranslationProxy:
    \"\"\"
    Template-friendly wrapper allowing {{ tr.Cards }} or {{ tr["About RocketBank"] }}.
    Always resolves using the currently active request language and never returns empty strings.
    \"\"\"

    def __getitem__(self, key):
        return t(key)

    def __getattr__(self, name):
        if not name:
            return ""

        # 1. Direct match in catalog
        if name in TRANSLATIONS_CATALOG:
            return t(name)

        # 2. Match lowercased or snake_cased
        name_clean = name.lower()
        for k in TRANSLATIONS_CATALOG:
            if k.lower() == name_clean or k.lower().replace(" ", "_") == name_clean:
                return t(k)

        # 3. Try converting underscores to spaces
        spaced = name.replace("_", " ").title()
        if spaced in TRANSLATIONS_CATALOG:
            return t(spaced)

        return t(name)
"""
    with open(BASE_DIR / "apps/core/translations.py", "w", encoding="utf-8") as f:
        f.write(cat_code)
    print("Updated apps/core/translations.py with full catalog")

    # 4. Compile all MO files
    compile_all(BASE_DIR)


if __name__ == "__main__":
    sync_all()
