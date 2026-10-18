"""
Zero-dependency Trilingual Translation Dictionary (RU, KK, EN) for RocketBank.
Ensures immediate, flawless UI translation across all pages and views.
"""

from django.utils.translation import get_language, gettext

TRANSLATIONS_CATALOG = {
    # ── 1. Navbar & Header ──────────────────────────
    "Cards": {
        "en": "Cards",
        "ru": "Карты",
        "kk": "Карталар",
    },
    "Loans": {
        "en": "Loans",
        "ru": "Кредиты",
        "kk": "Несиелер",
    },
    "Deposits": {
        "en": "Deposits",
        "ru": "Депозиты",
        "kk": "Депозиттер",
    },
    "About": {
        "en": "About",
        "ru": "О банке",
        "kk": "Банк туралы",
    },
    "FAQ": {
        "en": "FAQ",
        "ru": "FAQ",
        "kk": "FAQ",
    },
    "Contacts": {
        "en": "Contacts",
        "ru": "Контакты",
        "kk": "Байланыс",
    },
    "Sign in": {
        "en": "Sign in",
        "ru": "Войти",
        "kk": "Кіру",
    },
    "Get started": {
        "en": "Get started",
        "ru": "Открыть счёт",
        "kk": "Шот ашу",
    },
    "Get started free": {
        "en": "Get started free",
        "ru": "Открыть счёт",
        "kk": "Шот ашу",
    },
    "Dashboard": {
        "en": "Dashboard",
        "ru": "Кабинет",
        "kk": "Кабинет",
    },
    "Client Portal": {
        "en": "Client Portal",
        "ru": "Личный кабинет",
        "kk": "Клиенттік кабинет",
    },
    "Log out": {
        "en": "Log out",
        "ru": "Выйти",
        "kk": "Шығу",
    },
    "Sign out": {
        "en": "Sign out",
        "ru": "Выйти",
        "kk": "Шығу",
    },
    "Profile": {
        "en": "Profile",
        "ru": "Профиль",
        "kk": "Профиль",
    },
    "Notifications": {
        "en": "Notifications",
        "ru": "Уведомления",
        "kk": "Хабарламалар",
    },
    "Live": {
        "en": "Live",
        "ru": "Онлайн",
        "kk": "Тікелей",
    },
    "Toggle theme": {
        "en": "Toggle theme",
        "ru": "Сменить тему",
        "kk": "Тақырыпты ауыстыру",
    },
    "Skip to main content": {
        "en": "Skip to main content",
        "ru": "Перейти к основному содержимому",
        "kk": "Негізгі мазмұнға өту",
    },

    # ── 2. Footer ───────────────────────────────────
    "Products": {
        "en": "Products",
        "ru": "Продукты",
        "kk": "Өнімдер",
    },
    "Debit & Credit Cards": {
        "en": "Debit & Credit Cards",
        "ru": "Дебетовые и кредитные карты",
        "kk": "Дебеттік және несиелік карталар",
    },
    "Consumer & Auto Loans": {
        "en": "Consumer & Auto Loans",
        "ru": "Потребительские и автокредиты",
        "kk": "Тұтынушылық және автонесиелер",
    },
    "Fixed-Term Deposits": {
        "en": "Fixed-Term Deposits",
        "ru": "Срочные депозиты",
        "kk": "Мерзімді депозиттер",
    },
    "Loan Calculator": {
        "en": "Loan Calculator",
        "ru": "Кредитный калькулятор",
        "kk": "Несие калькуляторы",
    },
    "Company": {
        "en": "Company",
        "ru": "О компании",
        "kk": "Компания туралы",
    },
    "About RocketBank": {
        "en": "About RocketBank",
        "ru": "О RocketBank",
        "kk": "RocketBank туралы",
    },
    "Help Center & FAQ": {
        "en": "Help Center & FAQ",
        "ru": "Центр помощи и FAQ",
        "kk": "Көмек орталығы және FAQ",
    },
    "Contacts & Headquarters": {
        "en": "Contacts & Headquarters",
        "ru": "Контакты и штаб-квартира",
        "kk": "Байланыс және бас кеңсе",
    },
    "System Health Status": {
        "en": "System Health Status",
        "ru": "Статус работы сервисов",
        "kk": "Жүйенің жұмыс күйі",
    },
    "Legal & Security": {
        "en": "Legal & Security",
        "ru": "Безопасность и право",
        "kk": "Құқықтық ақпарат және қауіпсіздік",
    },
    "Terms of Service": {
        "en": "Terms of Service",
        "ru": "Условия обслуживания",
        "kk": "Қызмет көрсету шарттары",
    },
    "Privacy Policy": {
        "en": "Privacy Policy",
        "ru": "Политика конфиденциальности",
        "kk": "Құпиялылық саясаты",
    },
    "Security Standards": {
        "en": "Security Standards",
        "ru": "Стандарты безопасности",
        "kk": "Қауіпсіздік стандарттары",
    },
    "Regulatory Disclosures": {
        "en": "Regulatory Disclosures",
        "ru": "Раскрытие информации",
        "kk": "Ақпаратты ашу",
    },
    "Next-generation digital banking platform empowering clients worldwide with real-time payments, smart cards, high-yield deposits, and enterprise security.": {
        "en": "Next-generation digital banking platform empowering clients worldwide with real-time payments, smart cards, high-yield deposits, and enterprise security.",
        "ru": "Цифровая банковская платформа нового поколения: мгновенные платежи, умные карты, доходные депозиты и корпоративный уровень безопасности.",
        "kk": "Жаңа буын цифрлық банк платформасы: лездік төлемдер, смарт карталар, жоғары кірісті депозиттер және сенімді қауіпсіздік.",
    },
    "Regulated by the Agency for Regulation and Development of the Financial Market.": {
        "en": "Regulated by the Agency for Regulation and Development of the Financial Market.",
        "ru": "Регулируется Агентством Республики Казахстан по регулированию и развитию финансового рынка.",
        "kk": "Қазақстан Республикасының Қаржы нарығын реттеу және дамыту агенттігімен реттеледі.",
    },
    "Deposits insured up to 20,000,000 KZT by the Kazakhstan Deposit Insurance Fund (KDIF).": {
        "en": "Deposits insured up to 20,000,000 KZT by the Kazakhstan Deposit Insurance Fund (KDIF).",
        "ru": "Вклады застрахованы Казахстанским фондом гарантирования депозитов (КФГД) на сумму до 20 000 000 тенге.",
        "kk": "Салымдар Қазақстанның депозиттерге кепілдік беру қорымен (ҚДКБҚ) 20 000 000 теңгеге дейін сақтандырылған.",
    },
    "256-bit AES banking encryption & SOC 2 Type II certified infrastructure.": {
        "en": "256-bit AES banking encryption & SOC 2 Type II certified infrastructure.",
        "ru": "256-битное шифрование AES банковского уровня и инфраструктура, сертифицированная по стандарту SOC 2 Type II.",
        "kk": "256-биттік AES банктік шифрлауы және SOC 2 Type II сертификатталған инфрақұрылымы.",
    },
    "Licensed by the Agency for Regulation and Development of the Financial Market. All rights reserved.": {
        "en": "Licensed by the Agency for Regulation and Development of the Financial Market. All rights reserved.",
        "ru": "Лицензия Агентства Республики Казахстан по регулированию и развитию финансового рынка. Все права защищены.",
        "kk": "Қазақстан Республикасының Қаржы нарығын реттеу және дамыту агенттігінің лицензиясы. Барлық құқықтар қорғалған.",
    },

    # ── 3. Home Landing Page ────────────────────────
    "Now with AI-powered financial insights": {
        "en": "Now with AI-powered financial insights",
        "ru": "Теперь с финансовой аналитикой на базе ИИ",
        "kk": "Енді ЖИ негізіндегі қаржылық талдаумен",
    },
    "Finance that": {
        "en": "Finance that",
        "ru": "Финансы, которые",
        "kk": "Сіздің",
    },
    "moves at": {
        "en": "moves at",
        "ru": "движутся со скоростью",
        "kk": "жылдамдығыңыздағы",
    },
    "your speed": {
        "en": "your speed",
        "ru": "ваших решений",
        "kk": "қаржылық жүйе",
    },
    "RocketBank is the modern financial platform built for businesses and individuals who refuse to wait. Real-time payments, intelligent analytics, and enterprise-grade security — all in one dashboard.": {
        "en": "RocketBank is the modern financial platform built for businesses and individuals who refuse to wait. Real-time payments, intelligent analytics, and enterprise-grade security — all in one dashboard.",
        "ru": "RocketBank — современная финансовая платформа для бизнеса и частных лиц, ценящих время. Мгновенные платежи, умная аналитика и безопасность корпоративного уровня — в едином интерфейсе.",
        "kk": "RocketBank — уақытын бағалайтын бизнес пен жеке тұлғаларға арналған заманауи қаржылық платформа. Бірыңғай интерфейстегі лездік төлемдер, ақылды аналитика және сенімді қауіпсіздік.",
    },
    "Start for free": {
        "en": "Start for free",
        "ru": "Начать бесплатно",
        "kk": "Тегін бастау",
    },
    "Explore Products": {
        "en": "Explore Products",
        "ru": "Посмотреть продукты",
        "kk": "Өнімдерді көру",
    },
    "Open Client Dashboard": {
        "en": "Open Client Dashboard",
        "ru": "Перейти в кабинет",
        "kk": "Кабинетке өту",
    },
    "Trusted by modern teams & financial institutions": {
        "en": "Trusted by modern teams & financial institutions",
        "ru": "Нам доверяют технологичные компании и финансовые институты",
        "kk": "Бізге заманауи компаниялар мен қаржы институттары сенеді",
    },
    "Daily Transaction Volume": {
        "en": "Daily Transaction Volume",
        "ru": "Дневной объем транзакций",
        "kk": "Күндік транзакция көлемі",
    },
    "Financial License Protection": {
        "en": "Financial License Protection",
        "ru": "Защита государственной лицензией",
        "kk": "Мемлекеттік лицензиямен қорғалған",
    },
    "Real-Time Ledger Latency": {
        "en": "Real-Time Ledger Latency",
        "ru": "Задержка финансового реестра",
        "kk": "Қаржылық тізілім кідірісі",
    },
    "Continuous System Uptime": {
        "en": "Continuous System Uptime",
        "ru": "Бесперебойная доступность",
        "kk": "Үздіксіз қолжетімділік",
    },
    "Everything You Need": {
        "en": "Everything You Need",
        "ru": "Всё необходимое для финансов",
        "kk": "Қаржыға қажеттінің барлығы",
    },
    "A Complete Suite for Personal & Business Capital": {
        "en": "A Complete Suite for Personal & Business Capital",
        "ru": "Полный набор решений для частного и корпоративного капитала",
        "kk": "Жеке және корпоративтік капиталға арналған толық шешімдер кешені",
    },
    "Instant Settlement Rails": {
        "en": "Instant Settlement Rails",
        "ru": "Мгновенные финансовые рельсы",
        "kk": "Лездік қаржылық есеп айырысу",
    },
    "Move money in real-time across domestic and international banking rails with sub-second atomic settlement and zero hidden commissions.": {
        "en": "Move money in real-time across domestic and international banking rails with sub-second atomic settlement and zero hidden commissions.",
        "ru": "Переводите средства в реальном времени по внутренним и международным банковским каналам с атомарным расчетом быстрее секунды и без скрытых комиссий.",
        "kk": "Ішкі және халықаралық банктік бағыттар бойынша қаражатты жасырын комиссиясыз, секундына жетпейтін атомарлық есеп айырысумен аударыңыз.",
    },
    "Predictive Intelligence": {
        "en": "Predictive Intelligence",
        "ru": "Предиктивная аналитика",
        "kk": "Болжамдық аналитика",
    },
    "AI-powered dashboards that surface what matters. Cashflow forecasting, automated anomaly detection, and real-time expense classification.": {
        "en": "AI-powered dashboards that surface what matters. Cashflow forecasting, automated anomaly detection, and real-time expense classification.",
        "ru": "Интеллектуальные панели управления: прогнозирование денежных потоков, автоматическое выявление аномалий и классификация расходов в реальном времени.",
        "kk": "Маңыздыны көрсететін интеллектуалды панельдер: ақша ағындарын болжау, аномалияларды автоматты анықтау және шығыстарды жіктеу.",
    },
    "Multi-Currency Treasury": {
        "en": "Multi-Currency Treasury",
        "ru": "Мультивалютное казначейство",
        "kk": "Көпвалюталық қазынашылық",
    },
    "Hold, convert, and pay in KZT, USD, EUR, GBP, and 30+ currencies at interbank rates. Lock live rates and eliminate foreign exchange loss.": {
        "en": "Hold, convert, and pay in KZT, USD, EUR, GBP, and 30+ currencies at interbank rates. Lock live rates and eliminate foreign exchange loss.",
        "ru": "Храните, конвертируйте и оплачивайте в KZT, USD, EUR, GBP и еще более 30 валютах по межбанковскому курсу. Фиксируйте курсы без потерь на конвертации.",
        "kk": "KZT, USD, EUR, GBP және 30-дан астам валютада банкаралық бағам бойынша сақтаңыз, айырбастаңыз және төлеңіз.",
    },
    "Zero-Trust Architecture": {
        "en": "Zero-Trust Architecture",
        "ru": "Архитектура Zero-Trust",
        "kk": "Zero-Trust қауіпсіздік архитектурасы",
    },
    "Bank-grade encryption, SOC 2 compliance, KDIF state deposit guarantee up to 20,000,000 KZT, and instant 1-click card freeze.": {
        "en": "Bank-grade encryption, SOC 2 compliance, KDIF state deposit guarantee up to 20,000,000 KZT, and instant 1-click card freeze.",
        "ru": "Банковское шифрование, соответствие SOC 2, государственная гарантия КФГД до 20 000 000 тенге и мгновенная заморозка карты в 1 клик.",
        "kk": "Банктік шифрлау, SOC 2 сәйкестігі, ҚДКБҚ 20 000 000 теңгеге дейінгі мемлекеттік кепілдігі және картаны 1 басумен лезде бұғаттау.",
    },
    "Real-Time Overview": {
        "en": "Real-Time Overview",
        "ru": "Обзор в реальном времени",
        "kk": "Нақты уақыттағы шолу",
    },
    "Built for Speed, Control & Clarity": {
        "en": "Built for Speed, Control & Clarity",
        "ru": "Создано для скорости, контроля и прозрачности",
        "kk": "Жылдамдық, бақылау және ашықтық үшін жасалған",
    },
    "Real-time liquidity, multi-currency balances, and full control over cards and transfers.": {
        "en": "Real-time liquidity, multi-currency balances, and full control over cards and transfers.",
        "ru": "Мгновенная ликвидность, мультивалютные балансы и полный контроль над картами и переводами.",
        "kk": "Лездік өтімділік, көпвалюталық теңгерімдер және карталар мен аударымдарды толық бақылау.",
    },
    "Open Free Account": {
        "en": "Open Free Account",
        "ru": "Открыть бесплатный счет",
        "kk": "Тегін шот ашу",
    },
    "View Analytics": {
        "en": "View Analytics",
        "ru": "Перейти к аналитике",
        "kk": "Аналитиканы қарау",
    },
    "Transparent Pricing": {
        "en": "Transparent Pricing",
        "ru": "Прозрачные тарифы",
        "kk": "Ашық тарифтер",
    },
    "Card Tiers Engineered for You": {
        "en": "Card Tiers Engineered for You",
        "ru": "Уровни карт, созданные под ваши задачи",
        "kk": "Сіздің мақсаттарыңызға арналған карталар",
    },
    "Start with zero maintenance, unlock high-yield privileges and priority concierge.": {
        "en": "Start with zero maintenance, unlock high-yield privileges and priority concierge.",
        "ru": "Начните с бесплатного обслуживания, открывайте премиальные привилегии и персональный консьерж-сервис.",
        "kk": "Тегін қызмет көрсетуден бастаңыз, артықшылықтар мен жеке консьерж-сервисті пайдаланыңыз.",
    },
    "Monthly billing": {
        "en": "Monthly billing",
        "ru": "Ежемесячно",
        "kk": "Ай сайын",
    },
    "Annual billing": {
        "en": "Annual billing",
        "ru": "Ежегодно",
        "kk": "Жыл сайын",
    },
    "Save 20%": {
        "en": "Save 20%",
        "ru": "Скидка 20%",
        "kk": "20% жеңілдік",
    },
    "Institutional Security": {
        "en": "Institutional Security",
        "ru": "Институциональная безопасность",
        "kk": "Институционалдық қауіпсіздік",
    },
    "Security is not a feature — it's the foundation": {
        "en": "Security is not a feature — it's the foundation",
        "ru": "Безопасность — это не опция, а фундамент",
        "kk": "Қауіпсіздік — бұл басты негіз",
    },
    "Every transaction is shielded by multiple layers of enterprise-grade cryptographic security. We are audited, regulated, and monitored around the clock.": {
        "en": "Every transaction is shielded by multiple layers of enterprise-grade cryptographic security. We are audited, regulated, and monitored around the clock.",
        "ru": "Каждая операция защищена многоуровневым криптографическим шифрованием. Система круглосуточно проверяется и контролируется регуляторами.",
        "kk": "Әрбір операция көпдеңгейлі криптографиялық қорғаныспен қорғалған. Жүйе тәулік бойы реттеушілердің қадағалауында.",
    },
    "KDIF Insured": {
        "en": "KDIF Insured",
        "ru": "Гарантия КФГД",
        "kk": "ҚДКБҚ кепілдігі",
    },
    "PCI DSS Level 1": {
        "en": "PCI DSS Level 1",
        "ru": "Сертификат PCI DSS Level 1",
        "kk": "PCI DSS Level 1 сертификаты",
    },
    "ISO 27001": {
        "en": "ISO 27001",
        "ru": "Стандарт ISO 27001",
        "kk": "ISO 27001 стандарты",
    },
    "AI Fraud Shield": {
        "en": "AI Fraud Shield",
        "ru": "ИИ-защита от мошенничества",
        "kk": "Алаяқтықтан қорғайтын ЖИ",
    },
    "RocketBank Mobile Experience": {
        "en": "RocketBank Mobile Experience",
        "ru": "Мобильное приложение RocketBank",
        "kk": "RocketBank мобильді қосымшасы",
    },
    "Full dashboard access, biometric approval for high-value transfers, and instant transaction push notifications — anywhere in the world.": {
        "en": "Full dashboard access, biometric approval for high-value transfers, and instant transaction push notifications — anywhere in the world.",
        "ru": "Полный доступ к счетам, биометрическое подтверждение крупных переводов и мгновенные пуш-уведомления в любой точке мира.",
        "kk": "Шоттарға толық қолжетімділік, ірі аударымдарды биометриялық растау және әлемнің кез келген жерінде лездік хабарламалар.",
    },
    "Available for iOS & Android": {
        "en": "Available for iOS & Android",
        "ru": "Доступно для iOS и Android",
        "kk": "iOS және Android үшін қолжетімді",
    },
    "Common Questions": {
        "en": "Common Questions",
        "ru": "Частые вопросы",
        "kk": "Жиі қойылатын сұрақтар",
    },
    "Everything You Need to Know": {
        "en": "Everything You Need to Know",
        "ru": "Все, что вам нужно знать о банке",
        "kk": "Банк туралы білуіңіз керек барлық ақпарат",
    },

    # ── 4. About RocketBank Page ────────────────────
    "About RocketBank — Architecture & Leadership": {
        "en": "About RocketBank — Architecture & Leadership",
        "ru": "О RocketBank — Архитектура и руководство",
        "kk": "RocketBank туралы — Архитектура және басшылық",
    },
    "Corporate Overview": {
        "en": "Corporate Overview",
        "ru": "Корпоративный обзор",
        "kk": "Корпоративтік шолу",
    },
    "Engineered to redefine digital finance through real-time distributed architecture, strict ACID atomicity, and uncompromising human-centric design.": {
        "en": "Engineered to redefine digital finance through real-time distributed architecture, strict ACID atomicity, and uncompromising human-centric design.",
        "ru": "Создан для трансформации цифровых финансов благодаря распределенной архитектуре реального времени, строгой атомарности ACID и бескомпромиссному дизайну.",
        "kk": "Нақты уақыттағы үлестірілген архитектура, ACID атомарлығы және клиентке бағдарланған дизайн арқылы қаржы саласын жаңғырту үшін құрылған.",
    },
    "Engineering Architecture": {
        "en": "Engineering Architecture",
        "ru": "Инженерная архитектура",
        "kk": "Инженерлік архитектура",
    },
    "High-Concurrency Real-Time Infrastructure": {
        "en": "High-Concurrency Real-Time Infrastructure",
        "ru": "Высоконагруженная инфраструктура реального времени",
        "kk": "Жоғары жүктемелі нақты уақыттағы инфрақұрылым",
    },
    "RocketBank is architected on a high-availability Django core coupled with PostgreSQL transactional persistence, Celery asynchronous pipelines, and Redis low-latency caching.": {
        "en": "RocketBank is architected on a high-availability Django core coupled with PostgreSQL transactional persistence, Celery asynchronous pipelines, and Redis low-latency caching.",
        "ru": "RocketBank построен на высоконадежном ядре Django в связке с транзакционным хранилищем PostgreSQL, асинхронными очередями Celery и быстрой памятью Redis.",
        "kk": "RocketBank жоғары сенімді Django өзегінде, PostgreSQL транзакциялық базасымен, Celery асинхронды кезегімен және жылдам Redis кэшімен жасалған.",
    },
    "Our financial ledger guarantees full ACID atomicity with row-level locks (select_for_update) to prevent race conditions during peak transaction spikes, processing sub-second multi-currency transfers across domestic and international banking rails.": {
        "en": "Our financial ledger guarantees full ACID atomicity with row-level locks (select_for_update) to prevent race conditions during peak transaction spikes, processing sub-second multi-currency transfers across domestic and international banking rails.",
        "ru": "Наш финансовый реестр гарантирует полную атомарность ACID с блокировками на уровне строк (select_for_update) для исключения состояния гонки при пиковых нагрузках, обрабатывая мультивалютные переводы быстрее секунды.",
        "kk": "Біздің қаржылық тізілім жоғары жүктеме кезінде қателіктерді болдырмау үшін жолдар деңгейіндегі құлыптаумен (select_for_update) толық ACID атомарлығына кепілдік береді.",
    },
    "Ledger Latency": {
        "en": "Ledger Latency",
        "ru": "Задержка реестра",
        "kk": "Тізілім кідірісі",
    },
    "Platform Uptime": {
        "en": "Platform Uptime",
        "ru": "Доступность платформы",
        "kk": "Платформа қолжетімділігі",
    },
    "Operational": {
        "en": "Operational",
        "ru": "Работает стабильно",
        "kk": "Тұрақты жұмыс істейді",
    },
    "Regulatory Licensing & Protection": {
        "en": "Regulatory Licensing & Protection",
        "ru": "Лицензирование и государственная защита",
        "kk": "Лицензиялау және мемлекеттік қорғаныс",
    },
    "Licensed by the ARDFM of Kazakhstan. Deposits insured up to 20,000,000 KZT by the KDIF.": {
        "en": "Licensed by the ARDFM of Kazakhstan. Deposits insured up to 20,000,000 KZT by the KDIF.",
        "ru": "Лицензировано АРРФР Казахстана. Депозиты застрахованы КФГД на сумму до 20 000 000 тенге.",
        "kk": "Қазақстанның ҚНРДА тарапынан лицензияланған. Депозиттерге ҚДКБҚ тарапынан 20 000 000 теңгеге дейін кепілдік берілген.",
    },
    "Sub-second Atomic Payments": {
        "en": "Sub-second Atomic Payments",
        "ru": "Атомарные платежи быстрее секунды",
        "kk": "Секундына жетпейтін атомарлық төлемдер",
    },
    "Zero-Trust Security Perimeter": {
        "en": "Zero-Trust Security Perimeter",
        "ru": "Периметр безопасности Zero-Trust",
        "kk": "Zero-Trust қауіпсіздік шеңбері",
    },
    "Governance": {
        "en": "Governance",
        "ru": "Корпоративное управление",
        "kk": "Басқару",
    },
    "Leadership & Architecture": {
        "en": "Leadership & Architecture",
        "ru": "Руководство и архитектура",
        "kk": "Басшылық және архитектура",
    },
    "Ayan": {
        "en": "Ayan",
        "ru": "Аян",
        "kk": "Аян",
    },
    "Founder & CEO • Chief System Architect": {
        "en": "Founder & CEO • Chief System Architect",
        "ru": "Основатель и CEO • Главный системный архитектор",
        "kk": "Негізін қалаушы және CEO • Бас жүйелік архитектор",
    },
    "Executive Direction": {
        "en": "Executive Direction",
        "ru": "Видение руководства",
        "kk": "Басшылықтың көзқарасы",
    },
    "We architected RocketBank from the ground up on modern, open principles: elimination of opaque banking bureaucracy, execution speed measured in milliseconds, and rock-solid cryptographic security. Every component is designed to give individuals and businesses complete, effortless command over their financial destiny.": {
        "en": "We architected RocketBank from the ground up on modern, open principles: elimination of opaque banking bureaucracy, execution speed measured in milliseconds, and rock-solid cryptographic security. Every component is designed to give individuals and businesses complete, effortless command over their financial destiny.",
        "ru": "Мы создали RocketBank с нуля на современных принципах: устранение непрозрачной бюрократии, скорость операций за миллисекунды и несокрушимая криптографическая безопасность. Каждый элемент спроектирован так, чтобы дать частным лицам и бизнесу легкий и полный контроль над своим капиталом.",
        "kk": "Біз RocketBank-ті басынан бастап заманауи қағидаттар бойынша құрдық: бюрократияны жою, миллисекундтық жылдамдық және мықты криптографиялық қауіпсіздік. Әрбір құрамдас бөлік клиенттерге өз қаражатын оңай әрі толық басқаруға мүмкіндік беру үшін жасалған.",
    },
    "Global Presence": {
        "en": "Global Presence",
        "ru": "Штаб-квартира",
        "kk": "Бас кеңсе",
    },
    "Headquarters & Operations": {
        "en": "Headquarters & Operations",
        "ru": "Главный офис и управление",
        "kk": "Бас кеңсе және операциялық орталық",
    },
    "Located in the heart of Almaty's premier financial and technology corridor.": {
        "en": "Located in the heart of Almaty's premier financial and technology corridor.",
        "ru": "Расположен в главном финансовом и технологическом деловом центре Алматы.",
        "kk": "Алматы қаласының басты қаржылық және технологиялық орталығында орналасқан.",
    },
    "RocketBank Headquarters": {
        "en": "RocketBank Headquarters",
        "ru": "Штаб-квартира RocketBank",
        "kk": "RocketBank бас кеңсесі",
    },
    "Esentai Tower, Al-Farabi Avenue 77/7, Almaty Financial District, Republic of Kazakhstan, 050040.": {
        "en": "Esentai Tower, Al-Farabi Avenue 77/7, Almaty Financial District, Republic of Kazakhstan, 050040.",
        "ru": "Esentai Tower, проспект Аль-Фараби 77/7, Финансовый район Алматы, Республика Казахстан, 050040.",
        "kk": "Esentai Tower, Әл-Фараби даңғылы 77/7, Алматы қ., Қазақстан Республикасы, 050040.",
    },
    "Interactive Location Map": {
        "en": "Interactive Location Map",
        "ru": "Интерактивная карта",
        "kk": "Интерактивті карта",
    },
    "Central operations, engineering labs, and client relations center. Open Mon–Fri, 09:00–18:00 (UTC+5).": {
        "en": "Central operations, engineering labs, and client relations center. Open Mon–Fri, 09:00–18:00 (UTC+5).",
        "ru": "Операционный центр, лаборатории разработки и центр обслуживания клиентов. Пн–Пт, 09:00–18:00 (UTC+5).",
        "kk": "Операциялық орталық, әзірлеу зертханалары және клиенттерге қызмет көрсету бөлімі. Дүйсенбі–Жұма, 09:00–18:00 (UTC+5).",
    },

    # ── 5. Internal Dashboard, Accounts, Cards, Transfers ──
    "Financial Portfolio": {
        "en": "Financial Portfolio",
        "ru": "Финансовый портфель",
        "kk": "Қаржылық портфель",
    },
    "Here is your real-time financial portfolio overview for today": {
        "en": "Here is your real-time financial portfolio overview for today",
        "ru": "Обзор вашего финансового портфеля в реальном времени на сегодня",
        "kk": "Бүгінгі күнгі нақты уақыттағы қаржылық портфеліңіздің шолуы",
    },
    "Total Net Liquidity": {
        "en": "Total Net Liquidity",
        "ru": "Общая чистая ликвидность",
        "kk": "Жалпы таза өтімділік",
    },
    "Estimated across all accounts": {
        "en": "Estimated across all accounts",
        "ru": "Оценка по всем вашим счетам",
        "kk": "Барлық шоттар бойынша бағалау",
    },
    "Active Accounts Total": {
        "en": "Active Accounts Total",
        "ru": "Всего активных счетов",
        "kk": "Белсенді шоттар саны",
    },
    "Checking & Savings": {
        "en": "Checking & Savings",
        "ru": "Текущие и сберегательные",
        "kk": "Ағымдағы және жинақ",
    },
    "Active Plastic & Virtual": {
        "en": "Active Plastic & Virtual",
        "ru": "Активные пластиковые и виртуальные",
        "kk": "Белсенді пластикалық және виртуалды",
    },
    "Active Loans Balance": {
        "en": "Active Loans Balance",
        "ru": "Остаток по кредитам",
        "kk": "Несиелер бойынша қалдық",
    },
    "Pending repayment": {
        "en": "Pending repayment",
        "ru": "К погашению",
        "kk": "Өтеуге жатады",
    },
    "Quick Banking Services": {
        "en": "Quick Banking Services",
        "ru": "Быстрые банковские операции",
        "kk": "Жылдам банктік қызметтер",
    },
    "Send Money": {
        "en": "Send Money",
        "ru": "Перевести деньги",
        "kk": "Ақша аудару",
    },
    "Instant IBAN & P2P": {
        "en": "Instant IBAN & P2P",
        "ru": "Мгновенно по IBAN и P2P",
        "kk": "IBAN және P2P бойынша лезде",
    },
    "Order Card": {
        "en": "Order Card",
        "ru": "Заказать карту",
        "kk": "Картаға тапсырыс беру",
    },
    "Take a Loan": {
        "en": "Take a Loan",
        "ru": "Оформить кредит",
        "kk": "Несие алу",
    },
    "Open Deposit": {
        "en": "Open Deposit",
        "ru": "Открыть депозит",
        "kk": "Депозит ашу",
    },
    "Recent Transactions": {
        "en": "Recent Transactions",
        "ru": "Последние транзакции",
        "kk": "Соңғы транзакциялар",
    },
    "View Full History": {
        "en": "View Full History",
        "ru": "Вся история",
        "kk": "Толық тарих",
    },
    "My Bank Accounts": {
        "en": "My Bank Accounts",
        "ru": "Мои банковские счета",
        "kk": "Менің банктік шоттарым",
    },
    "Bank Accounts": {
        "en": "Bank Accounts",
        "ru": "Банковские счета",
        "kk": "Банктік шоттар",
    },
    "Manage all your checking, savings, business, and deposit IBAN accounts": {
        "en": "Manage all your checking, savings, business, and deposit IBAN accounts",
        "ru": "Управляйте всеми текущими, сберегательными и депозитными счетами IBAN",
        "kk": "Барлық ағымдағы, жинақ және депозиттік IBAN шоттарыңызды басқарыңыз",
    },
    "Open New Account": {
        "en": "Open New Account",
        "ru": "Открыть новый счет",
        "kk": "Жаңа шот ашу",
    },
    "Search by IBAN...": {
        "en": "Search by IBAN...",
        "ru": "Поиск по IBAN...",
        "kk": "IBAN бойынша іздеу...",
    },
    "Filter by account type": {
        "en": "Filter by account type",
        "ru": "Фильтр по типу счета",
        "kk": "Шот түрі бойынша сүзу",
    },
    "All Account Types": {
        "en": "All Account Types",
        "ru": "Все типы счетов",
        "kk": "Шоттардың барлық түрлері",
    },
    "Checking": {
        "en": "Checking",
        "ru": "Текущий",
        "kk": "Ағымдағы",
    },
    "Savings": {
        "en": "Savings",
        "ru": "Сберегательный",
        "kk": "Жинақ",
    },
    "Filter": {
        "en": "Filter",
        "ru": "Применить",
        "kk": "Сүзу",
    },
    "Reset": {
        "en": "Reset",
        "ru": "Сбросить",
        "kk": "Қалпына келтіру",
    },
    "Transfer Money": {
        "en": "Transfer Money",
        "ru": "Перевести деньги",
        "kk": "Ақша аудару",
    },
    "Send instant, zero-commission payments to any RocketBank account": {
        "en": "Send instant, zero-commission payments to any RocketBank account",
        "ru": "Мгновенные переводы без комиссий на любые счета RocketBank",
        "kk": "Кез келген RocketBank шоттарына комиссиясыз лездік аударымдар",
    },
    "Confirm & Send Transfer": {
        "en": "Confirm & Send Transfer",
        "ru": "Подтвердить и перевести",
        "kk": "Растау және аудару",
    },
    "Cancel": {
        "en": "Cancel",
        "ru": "Отмена",
        "kk": "Бас тарту",
    },
    "Transaction History": {
        "en": "Transaction History",
        "ru": "История транзакций",
        "kk": "Транзакциялар тарихы",
    },
    "New Transfer": {
        "en": "New Transfer",
        "ru": "Новый перевод",
        "kk": "Жаңа аударым",
    },

    # ── 6. Auth Screens ─────────────────────────────
    "Sign In to RocketBank": {
        "en": "Sign In to RocketBank",
        "ru": "Вход в RocketBank",
        "kk": "RocketBank-ке кіру",
    },
    "Enter your credentials to access your digital command center": {
        "en": "Enter your credentials to access your digital command center",
        "ru": "Введите ваши учетные данные для доступа к личному кабинету",
        "kk": "Жеке кабинетке кіру үшін деректеріңізді енгізіңіз",
    },
    "Remember this device for 30 days": {
        "en": "Remember this device for 30 days",
        "ru": "Запомнить это устройство на 30 дней",
        "kk": "Бұл құрылғыны 30 күнге сақтау",
    },
    "Forgot password?": {
        "en": "Forgot password?",
        "ru": "Забыли пароль?",
        "kk": "Құпиясөзді ұмыттыңыз ба?",
    },
    "Don't have an account?": {
        "en": "Don't have an account?",
        "ru": "Еще нет аккаунта?",
        "kk": "Әлі тіркелмедіңіз бе?",
    },
    "Create Free Account": {
        "en": "Create Free Account",
        "ru": "Зарегистрироваться бесплатно",
        "kk": "Тегін тіркелу",
    },
    "Create Your RocketBank Account": {
        "en": "Create Your RocketBank Account",
        "ru": "Регистрация в RocketBank",
        "kk": "RocketBank-те тіркелу",
    },
    "Join next-generation banking with zero monthly maintenance fee": {
        "en": "Join next-generation banking with zero monthly maintenance fee",
        "ru": "Откройте счет в банке нового поколения с бесплатным обслуживанием",
        "kk": "Тегін қызмет көрсететін жаңа буын банкінде шот ашыңыз",
    },
    "Already have an account?": {
        "en": "Already have an account?",
        "ru": "Уже зарегистрированы?",
        "kk": "Бұрыннан тіркелгенсіз бе?",
    },
    "Reset Your Password": {
        "en": "Reset Your Password",
        "ru": "Восстановление пароля",
        "kk": "Құпиясөзді қалпына келтіру",
    },
    "Back to Sign In": {
        "en": "Back to Sign In",
        "ru": "Вернуться ко входу",
        "kk": "Кіруге оралу",
    },
}


def t(key, lang=None):
    """
    Returns translated text for `key` in `lang` (defaults to active django language).
    Falls back to Russian if active language missing, then English original.
    """
    if not lang:
        lang = get_language() or "ru"
    lang = lang.lower()
    if lang not in ("ru", "kk", "en"):
        lang = "ru"

    entry = TRANSLATIONS_CATALOG.get(key)
    if entry and lang in entry:
        return entry[lang]

    # Fallback to gettext
    translated = gettext(key)
    if translated and translated != key:
        return translated

    # If still equal and lang is ru/kk, check if we have it under a stripped or lower key
    for k, val in TRANSLATIONS_CATALOG.items():
        if k.strip().lower() == key.strip().lower():
            if lang in val:
                return val[lang]

    return key


class TranslationProxy:
    """
    Template-friendly wrapper allowing {{ tr.Cards }} or {{ tr["About RocketBank"] }}.
    Always resolves using the currently active request language.
    """

    def __getitem__(self, key):
        return t(key)

    def __getattr__(self, name):
        # Convert snake_case or clean name: tr.about_rocketbank -> "About RocketBank"
        # First try direct match
        if name in TRANSLATIONS_CATALOG:
            return t(name)

        # Try converting underscores to spaces
        spaced = name.replace("_", " ").title()
        if spaced in TRANSLATIONS_CATALOG:
            return t(spaced)

        for k in TRANSLATIONS_CATALOG:
            if k.lower().replace(" ", "_") == name.lower():
                return t(k)

        return t(name)
