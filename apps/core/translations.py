"""
Zero-dependency Trilingual Translation Dictionary (RU, KK, EN) for RocketBank.
Ensures immediate, flawless UI translation across all pages and views.
"""

from django.utils.translation import get_language, gettext

TRANSLATIONS_CATALOG = {
    "Cards": {
        "en": "Cards",
        "ru": "Карты",
        "kk": "Карталар"
    },
    "Loans": {
        "en": "Loans",
        "ru": "Кредиты",
        "kk": "Несиелер"
    },
    "Deposits": {
        "en": "Deposits",
        "ru": "Депозиты",
        "kk": "Депозиттер"
    },
    "About": {
        "en": "About",
        "ru": "О банке",
        "kk": "Банк туралы"
    },
    "FAQ": {
        "en": "FAQ",
        "ru": "FAQ",
        "kk": "FAQ"
    },
    "Contacts": {
        "en": "Contacts",
        "ru": "Контакты",
        "kk": "Байланыс"
    },
    "Sign in": {
        "en": "Sign in",
        "ru": "Войти",
        "kk": "Кіру"
    },
    "Get started": {
        "en": "Get started",
        "ru": "Открыть счёт",
        "kk": "Шот ашу"
    },
    "Get started free": {
        "en": "Get started free",
        "ru": "Открыть счёт",
        "kk": "Шот ашу"
    },
    "Dashboard": {
        "en": "Dashboard",
        "ru": "Кабинет",
        "kk": "Кабинет"
    },
    "Client Portal": {
        "en": "Client Portal",
        "ru": "Личный кабинет",
        "kk": "Клиенттік кабинет"
    },
    "Log out": {
        "en": "Log out",
        "ru": "Выйти",
        "kk": "Шығу"
    },
    "Sign out": {
        "en": "Sign out",
        "ru": "Выйти",
        "kk": "Шығу"
    },
    "Profile": {
        "en": "Profile",
        "ru": "Профиль",
        "kk": "Профиль"
    },
    "Notifications": {
        "en": "Notifications",
        "ru": "Уведомления",
        "kk": "Хабарламалар"
    },
    "Live": {
        "en": "Live",
        "ru": "Онлайн",
        "kk": "Тікелей"
    },
    "Toggle theme": {
        "en": "Toggle theme",
        "ru": "Сменить тему",
        "kk": "Тақырыпты ауыстыру"
    },
    "Skip to main content": {
        "en": "Skip to main content",
        "ru": "Перейти к основному содержимому",
        "kk": "Негізгі мазмұнға өту"
    },
    "Products": {
        "en": "Products",
        "ru": "Продукты",
        "kk": "Өнімдер"
    },
    "Debit & Credit Cards": {
        "en": "Debit & Credit Cards",
        "ru": "Дебетовые и кредитные карты",
        "kk": "Дебеттік және несиелік карталар"
    },
    "Consumer & Auto Loans": {
        "en": "Consumer & Auto Loans",
        "ru": "Потребительские и автокредиты",
        "kk": "Тұтынушылық және автонесиелер"
    },
    "Fixed-Term Deposits": {
        "en": "Fixed-Term Deposits",
        "ru": "Срочные депозиты",
        "kk": "Мерзімді депозиттер"
    },
    "Loan Calculator": {
        "en": "Loan Calculator",
        "ru": "Кредитный калькулятор",
        "kk": "Несие калькуляторы"
    },
    "Company": {
        "en": "Company",
        "ru": "О компании",
        "kk": "Компания туралы"
    },
    "About RocketBank": {
        "en": "About RocketBank",
        "ru": "О RocketBank",
        "kk": "RocketBank туралы"
    },
    "Help Center & FAQ": {
        "en": "Help Center & FAQ",
        "ru": "Центр помощи и FAQ",
        "kk": "Көмек орталығы және FAQ"
    },
    "Contacts & Headquarters": {
        "en": "Contacts & Headquarters",
        "ru": "Контакты и штаб-квартира",
        "kk": "Байланыс және бас кеңсе"
    },
    "System Health Status": {
        "en": "System Health Status",
        "ru": "Статус работы сервисов",
        "kk": "Жүйенің жұмыс күйі"
    },
    "Legal & Security": {
        "en": "Legal & Security",
        "ru": "Безопасность и право",
        "kk": "Құқықтық ақпарат және қауіпсіздік"
    },
    "Terms of Service": {
        "en": "Terms of Service",
        "ru": "Условия обслуживания",
        "kk": "Қызмет көрсету шарттары"
    },
    "Privacy Policy": {
        "en": "Privacy Policy",
        "ru": "Политика конфиденциальности",
        "kk": "Құпиялылық саясаты"
    },
    "Security Standards": {
        "en": "Security Standards",
        "ru": "Стандарты безопасности",
        "kk": "Қауіпсіздік стандарттары"
    },
    "Regulatory Disclosures": {
        "en": "Regulatory Disclosures",
        "ru": "Раскрытие информации",
        "kk": "Ақпаратты ашу"
    },
    "Next-generation digital banking platform empowering clients worldwide with real-time payments, smart cards, high-yield deposits, and enterprise security.": {
        "en": "Next-generation digital banking platform empowering clients worldwide with real-time payments, smart cards, high-yield deposits, and enterprise security.",
        "ru": "Цифровая банковская платформа нового поколения: мгновенные платежи, умные карты, доходные депозиты и корпоративный уровень безопасности.",
        "kk": "Жаңа буын цифрлық банк платформасы: лездік төлемдер, смарт карталар, жоғары кірісті депозиттер және сенімді қауіпсіздік."
    },
    "Regulated by the Agency for Regulation and Development of the Financial Market.": {
        "en": "Regulated by the Agency for Regulation and Development of the Financial Market.",
        "ru": "Регулируется Агентством Республики Казахстан по регулированию и развитию финансового рынка.",
        "kk": "Қазақстан Республикасының Қаржы нарығын реттеу және дамыту агенттігімен реттеледі."
    },
    "Deposits insured up to 20,000,000 KZT by the Kazakhstan Deposit Insurance Fund (KDIF).": {
        "en": "Deposits insured up to 20,000,000 KZT by the Kazakhstan Deposit Insurance Fund (KDIF).",
        "ru": "Вклады застрахованы Казахстанским фондом гарантирования депозитов (КФГД) на сумму до 20 000 000 тенге.",
        "kk": "Салымдар Қазақстанның депозиттерге кепілдік беру қорымен (ҚДКБҚ) 20 000 000 теңгеге дейін сақтандырылған."
    },
    "256-bit AES banking encryption & SOC 2 Type II certified infrastructure.": {
        "en": "256-bit AES banking encryption & SOC 2 Type II certified infrastructure.",
        "ru": "256-битное шифрование AES банковского уровня и инфраструктура, сертифицированная по стандарту SOC 2 Type II.",
        "kk": "256-биттік AES банктік шифрлауы және SOC 2 Type II сертификатталған инфрақұрылымы."
    },
    "Licensed by the Agency for Regulation and Development of the Financial Market. All rights reserved.": {
        "en": "Licensed by the Agency for Regulation and Development of the Financial Market. All rights reserved.",
        "ru": "Лицензия Агентства Республики Казахстан по регулированию и развитию финансового рынка. Все права защищены.",
        "kk": "Қазақстан Республикасының Қаржы нарығын реттеу және дамыту агенттігінің лицензиясы. Барлық құқықтар қорғалған."
    },
    "Now with AI-powered financial insights": {
        "en": "Now with AI-powered financial insights",
        "ru": "Теперь с финансовой аналитикой на базе ИИ",
        "kk": "Енді ЖИ негізіндегі қаржылық талдаумен"
    },
    "Finance that": {
        "en": "Finance that",
        "ru": "Финансы, которые",
        "kk": "Сіздің"
    },
    "moves at": {
        "en": "moves at",
        "ru": "движутся со скоростью",
        "kk": "жылдамдығыңыздағы"
    },
    "your speed": {
        "en": "your speed",
        "ru": "ваших решений",
        "kk": "қаржылық жүйе"
    },
    "RocketBank is the modern financial platform built for businesses and individuals who refuse to wait. Real-time payments, intelligent analytics, and enterprise-grade security — all in one dashboard.": {
        "en": "RocketBank is the modern financial platform built for businesses and individuals who refuse to wait. Real-time payments, intelligent analytics, and enterprise-grade security — all in one dashboard.",
        "ru": "RocketBank — современная финансовая платформа для бизнеса и частных лиц, ценящих время. Мгновенные платежи, умная аналитика и безопасность корпоративного уровня — в едином интерфейсе.",
        "kk": "RocketBank — уақытын бағалайтын бизнес пен жеке тұлғаларға арналған заманауи қаржылық платформа. Бірыңғай интерфейстегі лездік төлемдер, ақылды аналитика және сенімді қауіпсіздік."
    },
    "Start for free": {
        "en": "Start for free",
        "ru": "Начать бесплатно",
        "kk": "Тегін бастау"
    },
    "Explore Products": {
        "en": "Explore Products",
        "ru": "Посмотреть продукты",
        "kk": "Өнімдерді көру"
    },
    "Open Client Dashboard": {
        "en": "Open Client Dashboard",
        "ru": "Перейти в кабинет",
        "kk": "Кабинетке өту"
    },
    "Trusted by modern teams & financial institutions": {
        "en": "Trusted by modern teams & financial institutions",
        "ru": "Нам доверяют технологичные компании и финансовые институты",
        "kk": "Бізге заманауи компаниялар мен қаржы институттары сенеді"
    },
    "Daily Transaction Volume": {
        "en": "Daily Transaction Volume",
        "ru": "Дневной объем транзакций",
        "kk": "Күндік транзакция көлемі"
    },
    "Financial License Protection": {
        "en": "Financial License Protection",
        "ru": "Защита государственной лицензией",
        "kk": "Мемлекеттік лицензиямен қорғалған"
    },
    "Real-Time Ledger Latency": {
        "en": "Real-Time Ledger Latency",
        "ru": "Задержка финансового реестра",
        "kk": "Қаржылық тізілім кідірісі"
    },
    "Continuous System Uptime": {
        "en": "Continuous System Uptime",
        "ru": "Бесперебойная доступность",
        "kk": "Үздіксіз қолжетімділік"
    },
    "Everything You Need": {
        "en": "Everything You Need",
        "ru": "Всё необходимое для финансов",
        "kk": "Қаржыға қажеттінің барлығы"
    },
    "A Complete Suite for Personal & Business Capital": {
        "en": "A Complete Suite for Personal & Business Capital",
        "ru": "Полный набор решений для частного и корпоративного капитала",
        "kk": "Жеке және корпоративтік капиталға арналған толық шешімдер кешені"
    },
    "Instant Settlement Rails": {
        "en": "Instant Settlement Rails",
        "ru": "Мгновенные финансовые рельсы",
        "kk": "Лездік қаржылық есеп айырысу"
    },
    "Move money in real-time across domestic and international banking rails with sub-second atomic settlement and zero hidden commissions.": {
        "en": "Move money in real-time across domestic and international banking rails with sub-second atomic settlement and zero hidden commissions.",
        "ru": "Переводите средства в реальном времени по внутренним и международным банковским каналам с атомарным расчетом быстрее секунды и без скрытых комиссий.",
        "kk": "Ішкі және халықаралық банктік бағыттар бойынша қаражатты жасырын комиссиясыз, секундына жетпейтін атомарлық есеп айырысумен аударыңыз."
    },
    "Predictive Intelligence": {
        "en": "Predictive Intelligence",
        "ru": "Предиктивная аналитика",
        "kk": "Болжамдық аналитика"
    },
    "AI-powered dashboards that surface what matters. Cashflow forecasting, automated anomaly detection, and real-time expense classification.": {
        "en": "AI-powered dashboards that surface what matters. Cashflow forecasting, automated anomaly detection, and real-time expense classification.",
        "ru": "Интеллектуальные панели управления: прогнозирование денежных потоков, автоматическое выявление аномалий и классификация расходов в реальном времени.",
        "kk": "Маңыздыны көрсететін интеллектуалды панельдер: ақша ағындарын болжау, аномалияларды автоматты анықтау және шығыстарды жіктеу."
    },
    "Multi-Currency Treasury": {
        "en": "Multi-Currency Treasury",
        "ru": "Мультивалютное казначейство",
        "kk": "Көпвалюталық қазынашылық"
    },
    "Hold, convert, and pay in KZT, USD, EUR, GBP, and 30+ currencies at interbank rates. Lock live rates and eliminate foreign exchange loss.": {
        "en": "Hold, convert, and pay in KZT, USD, EUR, GBP, and 30+ currencies at interbank rates. Lock live rates and eliminate foreign exchange loss.",
        "ru": "Храните, конвертируйте и оплачивайте в KZT, USD, EUR, GBP и еще более 30 валютах по межбанковскому курсу. Фиксируйте курсы без потерь на конвертации.",
        "kk": "KZT, USD, EUR, GBP және 30-дан астам валютада банкаралық бағам бойынша сақтаңыз, айырбастаңыз және төлеңіз."
    },
    "Zero-Trust Architecture": {
        "en": "Zero-Trust Architecture",
        "ru": "Архитектура Zero-Trust",
        "kk": "Zero-Trust қауіпсіздік архитектурасы"
    },
    "Bank-grade encryption, SOC 2 compliance, KDIF state deposit guarantee up to 20,000,000 KZT, and instant 1-click card freeze.": {
        "en": "Bank-grade encryption, SOC 2 compliance, KDIF state deposit guarantee up to 20,000,000 KZT, and instant 1-click card freeze.",
        "ru": "Банковское шифрование, соответствие SOC 2, государственная гарантия КФГД до 20 000 000 тенге и мгновенная заморозка карты в 1 клик.",
        "kk": "Банктік шифрлау, SOC 2 сәйкестігі, ҚДКБҚ 20 000 000 теңгеге дейінгі мемлекеттік кепілдігі және картаны 1 басумен лезде бұғаттау."
    },
    "Real-Time Overview": {
        "en": "Real-Time Overview",
        "ru": "Обзор в реальном времени",
        "kk": "Нақты уақыттағы шолу"
    },
    "Built for Speed, Control & Clarity": {
        "en": "Built for Speed, Control & Clarity",
        "ru": "Создано для скорости, контроля и прозрачности",
        "kk": "Жылдамдық, бақылау және ашықтық үшін жасалған"
    },
    "Real-time liquidity, multi-currency balances, and full control over cards and transfers.": {
        "en": "Real-time liquidity, multi-currency balances, and full control over cards and transfers.",
        "ru": "Мгновенная ликвидность, мультивалютные балансы и полный контроль над картами и переводами.",
        "kk": "Лездік өтімділік, көпвалюталық теңгерімдер және карталар мен аударымдарды толық бақылау."
    },
    "Open Free Account": {
        "en": "Open Free Account",
        "ru": "Открыть бесплатный счет",
        "kk": "Тегін шот ашу"
    },
    "View Analytics": {
        "en": "View Analytics",
        "ru": "Перейти к аналитике",
        "kk": "Аналитиканы қарау"
    },
    "Transparent Pricing": {
        "en": "Transparent Pricing",
        "ru": "Прозрачные тарифы",
        "kk": "Ашық тарифтер"
    },
    "Card Tiers Engineered for You": {
        "en": "Card Tiers Engineered for You",
        "ru": "Уровни карт, созданные под ваши задачи",
        "kk": "Сіздің мақсаттарыңызға арналған карталар"
    },
    "Start with zero maintenance, unlock high-yield privileges and priority concierge.": {
        "en": "Start with zero maintenance, unlock high-yield privileges and priority concierge.",
        "ru": "Начните с бесплатного обслуживания, открывайте премиальные привилегии и персональный консьерж-сервис.",
        "kk": "Тегін қызмет көрсетуден бастаңыз, артықшылықтар мен жеке консьерж-сервисті пайдаланыңыз."
    },
    "Monthly billing": {
        "en": "Monthly billing",
        "ru": "Ежемесячно",
        "kk": "Ай сайын"
    },
    "Annual billing": {
        "en": "Annual billing",
        "ru": "Ежегодно",
        "kk": "Жыл сайын"
    },
    "Save 20%": {
        "en": "Save 20%",
        "ru": "Скидка 20%",
        "kk": "20% жеңілдік"
    },
    "Institutional Security": {
        "en": "Institutional Security",
        "ru": "Институциональная безопасность",
        "kk": "Институционалдық қауіпсіздік"
    },
    "Security is not a feature — it's the foundation": {
        "en": "Security is not a feature — it's the foundation",
        "ru": "Безопасность — это не опция, а фундамент",
        "kk": "Қауіпсіздік — бұл басты негіз"
    },
    "Every transaction is shielded by multiple layers of enterprise-grade cryptographic security. We are audited, regulated, and monitored around the clock.": {
        "en": "Every transaction is shielded by multiple layers of enterprise-grade cryptographic security. We are audited, regulated, and monitored around the clock.",
        "ru": "Каждая операция защищена многоуровневым криптографическим шифрованием. Система круглосуточно проверяется и контролируется регуляторами.",
        "kk": "Әрбір операция көпдеңгейлі криптографиялық қорғаныспен қорғалған. Жүйе тәулік бойы реттеушілердің қадағалауында."
    },
    "KDIF Insured": {
        "en": "KDIF Insured",
        "ru": "Гарантия КФГД",
        "kk": "ҚДКБҚ кепілдігі"
    },
    "PCI DSS Level 1": {
        "en": "PCI DSS Level 1",
        "ru": "Сертификат PCI DSS Level 1",
        "kk": "PCI DSS Level 1 сертификаты"
    },
    "ISO 27001": {
        "en": "ISO 27001",
        "ru": "Стандарт ISO 27001",
        "kk": "ISO 27001 стандарты"
    },
    "AI Fraud Shield": {
        "en": "AI Fraud Shield",
        "ru": "ИИ-защита от мошенничества",
        "kk": "Алаяқтықтан қорғайтын ЖИ"
    },
    "RocketBank Mobile Experience": {
        "en": "RocketBank Mobile Experience",
        "ru": "Мобильное приложение RocketBank",
        "kk": "RocketBank мобильді қосымшасы"
    },
    "Full dashboard access, biometric approval for high-value transfers, and instant transaction push notifications — anywhere in the world.": {
        "en": "Full dashboard access, biometric approval for high-value transfers, and instant transaction push notifications — anywhere in the world.",
        "ru": "Полный доступ к счетам, биометрическое подтверждение крупных переводов и мгновенные пуш-уведомления в любой точке мира.",
        "kk": "Шоттарға толық қолжетімділік, ірі аударымдарды биометриялық растау және әлемнің кез келген жерінде лездік хабарламалар."
    },
    "Available for iOS & Android": {
        "en": "Available for iOS & Android",
        "ru": "Доступно для iOS и Android",
        "kk": "iOS және Android үшін қолжетімді"
    },
    "Common Questions": {
        "en": "Common Questions",
        "ru": "Частые вопросы",
        "kk": "Жиі қойылатын сұрақтар"
    },
    "Everything You Need to Know": {
        "en": "Everything You Need to Know",
        "ru": "Все, что вам нужно знать о банке",
        "kk": "Банк туралы білуіңіз керек барлық ақпарат"
    },
    "About RocketBank — Architecture & Leadership": {
        "en": "About RocketBank — Architecture & Leadership",
        "ru": "О RocketBank — Архитектура и руководство",
        "kk": "RocketBank туралы — Архитектура және басшылық"
    },
    "Corporate Overview": {
        "en": "Corporate Overview",
        "ru": "Корпоративный обзор",
        "kk": "Корпоративтік шолу"
    },
    "Engineered to redefine digital finance through real-time distributed architecture, strict ACID atomicity, and uncompromising human-centric design.": {
        "en": "Engineered to redefine digital finance through real-time distributed architecture, strict ACID atomicity, and uncompromising human-centric design.",
        "ru": "Создан для трансформации цифровых финансов благодаря распределенной архитектуре реального времени, строгой атомарности ACID и бескомпромиссному дизайну.",
        "kk": "Нақты уақыттағы үлестірілген архитектура, ACID атомарлығы және клиентке бағдарланған дизайн арқылы қаржы саласын жаңғырту үшін құрылған."
    },
    "Engineering Architecture": {
        "en": "Engineering Architecture",
        "ru": "Инженерная архитектура",
        "kk": "Инженерлік архитектура"
    },
    "High-Concurrency Real-Time Infrastructure": {
        "en": "High-Concurrency Real-Time Infrastructure",
        "ru": "Высоконагруженная инфраструктура реального времени",
        "kk": "Жоғары жүктемелі нақты уақыттағы инфрақұрылым"
    },
    "RocketBank is architected on a high-availability Django core coupled with PostgreSQL transactional persistence, Celery asynchronous pipelines, and Redis low-latency caching.": {
        "en": "RocketBank is architected on a high-availability Django core coupled with PostgreSQL transactional persistence, Celery asynchronous pipelines, and Redis low-latency caching.",
        "ru": "RocketBank построен на высоконадежном ядре Django в связке с транзакционным хранилищем PostgreSQL, асинхронными очередями Celery и быстрой памятью Redis.",
        "kk": "RocketBank жоғары сенімді Django өзегінде, PostgreSQL транзакциялық базасымен, Celery асинхронды кезегімен және жылдам Redis кэшімен жасалған."
    },
    "Our financial ledger guarantees full ACID atomicity with row-level locks (select_for_update) to prevent race conditions during peak transaction spikes, processing sub-second multi-currency transfers across domestic and international banking rails.": {
        "en": "Our financial ledger guarantees full ACID atomicity with row-level locks (select_for_update) to prevent race conditions during peak transaction spikes, processing sub-second multi-currency transfers across domestic and international banking rails.",
        "ru": "Наш финансовый реестр гарантирует полную атомарность ACID с блокировками на уровне строк (select_for_update) для исключения состояния гонки при пиковых нагрузках, обрабатывая мультивалютные переводы быстрее секунды.",
        "kk": "Біздің қаржылық тізілім жоғары жүктеме кезінде қателіктерді болдырмау үшін жолдар деңгейіндегі құлыптаумен (select_for_update) толық ACID атомарлығына кепілдік береді."
    },
    "Ledger Latency": {
        "en": "Ledger Latency",
        "ru": "Задержка реестра",
        "kk": "Тізілім кідірісі"
    },
    "Platform Uptime": {
        "en": "Platform Uptime",
        "ru": "Доступность платформы",
        "kk": "Платформа қолжетімділігі"
    },
    "Operational": {
        "en": "Operational",
        "ru": "Работает стабильно",
        "kk": "Тұрақты жұмыс істейді"
    },
    "Regulatory Licensing & Protection": {
        "en": "Regulatory Licensing & Protection",
        "ru": "Лицензирование и государственная защита",
        "kk": "Лицензиялау және мемлекеттік қорғаныс"
    },
    "Licensed by the ARDFM of Kazakhstan. Deposits insured up to 20,000,000 KZT by the KDIF.": {
        "en": "Licensed by the ARDFM of Kazakhstan. Deposits insured up to 20,000,000 KZT by the KDIF.",
        "ru": "Лицензировано АРРФР Казахстана. Депозиты застрахованы КФГД на сумму до 20 000 000 тенге.",
        "kk": "Қазақстанның ҚНРДА тарапынан лицензияланған. Депозиттерге ҚДКБҚ тарапынан 20 000 000 теңгеге дейін кепілдік берілген."
    },
    "Sub-second Atomic Payments": {
        "en": "Sub-second Atomic Payments",
        "ru": "Атомарные платежи быстрее секунды",
        "kk": "Секундына жетпейтін атомарлық төлемдер"
    },
    "Zero-Trust Security Perimeter": {
        "en": "Zero-Trust Security Perimeter",
        "ru": "Периметр безопасности Zero-Trust",
        "kk": "Zero-Trust қауіпсіздік шеңбері"
    },
    "Governance": {
        "en": "Governance",
        "ru": "Корпоративное управление",
        "kk": "Басқару"
    },
    "Leadership & Architecture": {
        "en": "Leadership & Architecture",
        "ru": "Руководство и архитектура",
        "kk": "Басшылық және архитектура"
    },
    "Ayan": {
        "en": "Ayan",
        "ru": "Аян",
        "kk": "Аян"
    },
    "Founder & CEO • Chief System Architect": {
        "en": "Founder & CEO • Chief System Architect",
        "ru": "Основатель и CEO • Главный системный архитектор",
        "kk": "Негізін қалаушы және CEO • Бас жүйелік архитектор"
    },
    "Executive Direction": {
        "en": "Executive Direction",
        "ru": "Видение руководства",
        "kk": "Басшылықтың көзқарасы"
    },
    "We architected RocketBank from the ground up on modern, open principles: elimination of opaque banking bureaucracy, execution speed measured in milliseconds, and rock-solid cryptographic security. Every component is designed to give individuals and businesses complete, effortless command over their financial destiny.": {
        "en": "We architected RocketBank from the ground up on modern, open principles: elimination of opaque banking bureaucracy, execution speed measured in milliseconds, and rock-solid cryptographic security. Every component is designed to give individuals and businesses complete, effortless command over their financial destiny.",
        "ru": "Мы создали RocketBank с нуля на современных принципах: устранение непрозрачной бюрократии, скорость операций за миллисекунды и несокрушимая криптографическая безопасность. Каждый элемент спроектирован так, чтобы дать частным лицам и бизнесу легкий и полный контроль над своим капиталом.",
        "kk": "Біз RocketBank-ті басынан бастап заманауи қағидаттар бойынша құрдық: бюрократияны жою, миллисекундтық жылдамдық және мықты криптографиялық қауіпсіздік. Әрбір құрамдас бөлік клиенттерге өз қаражатын оңай әрі толық басқаруға мүмкіндік беру үшін жасалған."
    },
    "Global Presence": {
        "en": "Global Presence",
        "ru": "Штаб-квартира",
        "kk": "Бас кеңсе"
    },
    "Headquarters & Operations": {
        "en": "Headquarters & Operations",
        "ru": "Главный офис и управление",
        "kk": "Бас кеңсе және операциялық орталық"
    },
    "Located in the heart of Almaty's premier financial and technology corridor.": {
        "en": "Located in the heart of Almaty's premier financial and technology corridor.",
        "ru": "Расположен в главном финансовом и технологическом деловом центре Алматы.",
        "kk": "Алматы қаласының басты қаржылық және технологиялық орталығында орналасқан."
    },
    "RocketBank Headquarters": {
        "en": "RocketBank Headquarters",
        "ru": "Штаб-квартира RocketBank",
        "kk": "RocketBank бас кеңсесі"
    },
    "Esentai Tower, Al-Farabi Avenue 77/7, Almaty Financial District, Republic of Kazakhstan, 050040.": {
        "en": "Esentai Tower, Al-Farabi Avenue 77/7, Almaty Financial District, Republic of Kazakhstan, 050040.",
        "ru": "Esentai Tower, проспект Аль-Фараби 77/7, Финансовый район Алматы, Республика Казахстан, 050040.",
        "kk": "Esentai Tower, Әл-Фараби даңғылы 77/7, Алматы қ., Қазақстан Республикасы, 050040."
    },
    "Interactive Location Map": {
        "en": "Interactive Location Map",
        "ru": "Интерактивная карта",
        "kk": "Интерактивті карта"
    },
    "Central operations, engineering labs, and client relations center. Open Mon–Fri, 09:00–18:00 (UTC+5).": {
        "en": "Central operations, engineering labs, and client relations center. Open Mon–Fri, 09:00–18:00 (UTC+5).",
        "ru": "Операционный центр, лаборатории разработки и центр обслуживания клиентов. Пн–Пт, 09:00–18:00 (UTC+5).",
        "kk": "Операциялық орталық, әзірлеу зертханалары және клиенттерге қызмет көрсету бөлімі. Дүйсенбі–Жұма, 09:00–18:00 (UTC+5)."
    },
    "Financial Portfolio": {
        "en": "Financial Portfolio",
        "ru": "Финансовый портфель",
        "kk": "Қаржылық портфель"
    },
    "Here is your real-time financial portfolio overview for today": {
        "en": "Here is your real-time financial portfolio overview for today",
        "ru": "Обзор вашего финансового портфеля в реальном времени на сегодня",
        "kk": "Бүгінгі күнгі нақты уақыттағы қаржылық портфеліңіздің шолуы"
    },
    "Total Net Liquidity": {
        "en": "Total Net Liquidity",
        "ru": "Общая чистая ликвидность",
        "kk": "Жалпы таза өтімділік"
    },
    "Estimated across all accounts": {
        "en": "Estimated across all accounts",
        "ru": "Оценка по всем вашим счетам",
        "kk": "Барлық шоттар бойынша бағалау"
    },
    "Active Accounts Total": {
        "en": "Active Accounts Total",
        "ru": "Всего активных счетов",
        "kk": "Белсенді шоттар саны"
    },
    "Checking & Savings": {
        "en": "Checking & Savings",
        "ru": "Текущие и сберегательные",
        "kk": "Ағымдағы және жинақ"
    },
    "Active Plastic & Virtual": {
        "en": "Active Plastic & Virtual",
        "ru": "Активные пластиковые и виртуальные",
        "kk": "Белсенді пластикалық және виртуалды"
    },
    "Active Loans Balance": {
        "en": "Active Loans Balance",
        "ru": "Остаток по кредитам",
        "kk": "Несиелер бойынша қалдық"
    },
    "Pending repayment": {
        "en": "Pending repayment",
        "ru": "К погашению",
        "kk": "Өтеуге жатады"
    },
    "Quick Banking Services": {
        "en": "Quick Banking Services",
        "ru": "Быстрые банковские операции",
        "kk": "Жылдам банктік қызметтер"
    },
    "Send Money": {
        "en": "Send Money",
        "ru": "Перевести деньги",
        "kk": "Ақша аудару"
    },
    "Instant IBAN & P2P": {
        "en": "Instant IBAN & P2P",
        "ru": "Мгновенно по IBAN и P2P",
        "kk": "IBAN және P2P бойынша лезде"
    },
    "Order Card": {
        "en": "Order Card",
        "ru": "Заказать карту",
        "kk": "Картаға тапсырыс беру"
    },
    "Take a Loan": {
        "en": "Take a Loan",
        "ru": "Оформить кредит",
        "kk": "Несие алу"
    },
    "Open Deposit": {
        "en": "Open Deposit",
        "ru": "Открыть депозит",
        "kk": "Депозит ашу"
    },
    "Recent Transactions": {
        "en": "Recent Transactions",
        "ru": "Последние транзакции",
        "kk": "Соңғы транзакциялар"
    },
    "View Full History": {
        "en": "View Full History",
        "ru": "Вся история",
        "kk": "Толық тарих"
    },
    "My Bank Accounts": {
        "en": "My Bank Accounts",
        "ru": "Мои банковские счета",
        "kk": "Менің банктік шоттарым"
    },
    "Bank Accounts": {
        "en": "Bank Accounts",
        "ru": "Банковские счета",
        "kk": "Банктік шоттар"
    },
    "Manage all your checking, savings, business, and deposit IBAN accounts": {
        "en": "Manage all your checking, savings, business, and deposit IBAN accounts",
        "ru": "Управляйте всеми текущими, сберегательными и депозитными счетами IBAN",
        "kk": "Барлық ағымдағы, жинақ және депозиттік IBAN шоттарыңызды басқарыңыз"
    },
    "Open New Account": {
        "en": "Open New Account",
        "ru": "Открыть новый счет",
        "kk": "Жаңа шот ашу"
    },
    "Search by IBAN...": {
        "en": "Search by IBAN...",
        "ru": "Поиск по IBAN...",
        "kk": "IBAN бойынша іздеу..."
    },
    "Filter by account type": {
        "en": "Filter by account type",
        "ru": "Фильтр по типу счета",
        "kk": "Шот түрі бойынша сүзу"
    },
    "All Account Types": {
        "en": "All Account Types",
        "ru": "Все типы счетов",
        "kk": "Шоттардың барлық түрлері"
    },
    "Checking": {
        "en": "Checking",
        "ru": "Текущий",
        "kk": "Ағымдағы"
    },
    "Savings": {
        "en": "Savings",
        "ru": "Сберегательный",
        "kk": "Жинақ"
    },
    "Filter": {
        "en": "Filter",
        "ru": "Применить",
        "kk": "Сүзу"
    },
    "Reset": {
        "en": "Reset",
        "ru": "Сбросить",
        "kk": "Қалпына келтіру"
    },
    "Transfer Money": {
        "en": "Transfer Money",
        "ru": "Перевести деньги",
        "kk": "Ақша аудару"
    },
    "Send instant, zero-commission payments to any RocketBank account": {
        "en": "Send instant, zero-commission payments to any RocketBank account",
        "ru": "Мгновенные переводы без комиссий на любые счета RocketBank",
        "kk": "Кез келген RocketBank шоттарына комиссиясыз лездік аударымдар"
    },
    "Confirm & Send Transfer": {
        "en": "Confirm & Send Transfer",
        "ru": "Подтвердить и перевести",
        "kk": "Растау және аудару"
    },
    "Cancel": {
        "en": "Cancel",
        "ru": "Отмена",
        "kk": "Бас тарту"
    },
    "Transaction History": {
        "en": "Transaction History",
        "ru": "История транзакций",
        "kk": "Транзакциялар тарихы"
    },
    "New Transfer": {
        "en": "New Transfer",
        "ru": "Новый перевод",
        "kk": "Жаңа аударым"
    },
    "Sign In to RocketBank": {
        "en": "Sign In to RocketBank",
        "ru": "Вход в RocketBank",
        "kk": "RocketBank-ке кіру"
    },
    "Enter your credentials to access your digital command center": {
        "en": "Enter your credentials to access your digital command center",
        "ru": "Введите ваши учетные данные для доступа к личному кабинету",
        "kk": "Жеке кабинетке кіру үшін деректеріңізді енгізіңіз"
    },
    "Remember this device for 30 days": {
        "en": "Remember this device for 30 days",
        "ru": "Запомнить это устройство на 30 дней",
        "kk": "Бұл құрылғыны 30 күнге сақтау"
    },
    "Forgot password?": {
        "en": "Forgot password?",
        "ru": "Забыли пароль?",
        "kk": "Құпиясөзді ұмыттыңыз ба?"
    },
    "Don't have an account?": {
        "en": "Don't have an account?",
        "ru": "Еще нет аккаунта?",
        "kk": "Әлі тіркелмедіңіз бе?"
    },
    "Create Free Account": {
        "en": "Create Free Account",
        "ru": "Зарегистрироваться бесплатно",
        "kk": "Тегін тіркелу"
    },
    "Create Your RocketBank Account": {
        "en": "Create Your RocketBank Account",
        "ru": "Регистрация в RocketBank",
        "kk": "RocketBank-те тіркелу"
    },
    "Join next-generation banking with zero monthly maintenance fee": {
        "en": "Join next-generation banking with zero monthly maintenance fee",
        "ru": "Откройте счет в банке нового поколения с бесплатным обслуживанием",
        "kk": "Тегін қызмет көрсететін жаңа буын банкінде шот ашыңыз"
    },
    "Already have an account?": {
        "en": "Already have an account?",
        "ru": "Уже зарегистрированы?",
        "kk": "Бұрыннан тіркелгенсіз бе?"
    },
    "Reset Your Password": {
        "en": "Reset Your Password",
        "ru": "Восстановление пароля",
        "kk": "Құпиясөзді қалпына келтіру"
    },
    "Back to Sign In": {
        "en": "Back to Sign In",
        "ru": "Вернуться ко входу",
        "kk": "Кіруге оралу"
    },
    "Home": {
        "en": "Home",
        "ru": "Главная",
        "kk": "Басты бет"
    },
    "Toggle dark/light theme": {
        "en": "Toggle dark/light theme",
        "ru": "Переключить темную/светлую тему",
        "kk": "Күңгірт/жарық тақырыпты ауыстыру"
    },
    "Close menu": {
        "en": "Close menu",
        "ru": "Закрыть меню",
        "kk": "Мәзірді жабу"
    },
    "Open menu": {
        "en": "Open menu",
        "ru": "Открыть меню",
        "kk": "Мәзірді ашу"
    },
    "Dashboard navigation": {
        "en": "Dashboard navigation",
        "ru": "Навигация панели",
        "kk": "Панель навигациясы"
    },
    "Dashboard sections": {
        "en": "Dashboard sections",
        "ru": "Разделы панели",
        "kk": "Панель бөлімдері"
    },
    "Enterprise Digital Banking": {
        "en": "Enterprise Digital Banking",
        "ru": "Цифровой банкинг для бизнеса и частных лиц",
        "kk": "Бизнес пен жеке тұлғаларға арналған цифрлық банкинг"
    },
    "Accounts": {
        "en": "Accounts",
        "ru": "Счета",
        "kk": "Шоттар"
    },
    "Transactions": {
        "en": "Transactions",
        "ru": "Транзакции",
        "kk": "Транзакциялар"
    },
    "My Cards": {
        "en": "My Cards",
        "ru": "Мои карты",
        "kk": "Менің карталарым"
    },
    "Order Card (Wizard)": {
        "en": "Order Card (Wizard)",
        "ru": "Заказ карты (Мастер)",
        "kk": "Картаға тапсырыс беру"
    },
    "Loans & Credit": {
        "en": "Loans & Credit",
        "ru": "Кредиты и займы",
        "kk": "Несиелер мен қарыздар"
    },
    "Term Deposits": {
        "en": "Term Deposits",
        "ru": "Срочные депозиты",
        "kk": "Мерзімді депозиттер"
    },
    "Analytics & Goals": {
        "en": "Analytics & Goals",
        "ru": "Аналитика и цели",
        "kk": "Талдау және мақсаттар"
    },
    "Support & Tickets": {
        "en": "Support & Tickets",
        "ru": "Поддержка и тикеты",
        "kk": "Қолдау қызметі"
    },
    "Security Settings": {
        "en": "Security Settings",
        "ru": "Настройки безопасности",
        "kk": "Қауіпсіздік баптаулары"
    },
    "Current Session": {
        "en": "Current Session",
        "ru": "Текущая сессия",
        "kk": "Ағымдағы сессия"
    },
    "unread notifications": {
        "en": "unread notifications",
        "ru": "непрочитанных уведомлений",
        "kk": "оқылмаған хабарламалар"
    },
    "View notifications": {
        "en": "View notifications",
        "ru": "Посмотреть уведомления",
        "kk": "Хабарламаларды көру"
    },
    "User profile avatar": {
        "en": "User profile avatar",
        "ru": "Аватар профиля",
        "kk": "Профиль аватары"
    },
    "Modern Digital Financial Platform": {
        "en": "Modern Digital Financial Platform",
        "ru": "Современная цифровая финансовая платформа",
        "kk": "Заманауи цифрлық қаржылық платформа"
    },
    "RocketBank is the modern financial platform engineered for speed. Real-time payments, intelligent analytics, enterprise-grade security, and zero-commission multi-currency accounts.": {
        "en": "RocketBank is the modern financial platform engineered for speed. Real-time payments, intelligent analytics, enterprise-grade security, and zero-commission multi-currency accounts.",
        "ru": "RocketBank — современная финансовая платформа, созданная для скорости: расчеты в реальном времени, интеллектуальная аналитика, надежная безопасность и мультивалютные счета без комиссий.",
        "kk": "RocketBank — жылдамдық үшін жасалған заманауи қаржылық платформа: нақты уақыттағы төлемдер, интеллектуалды талдау, сенімді қауіпсіздік және комиссиясыз көпвалюталық шоттар."
    },
    "Insured up to 20,000,000 KZT per depositor": {
        "en": "Insured up to 20,000,000 KZT per depositor",
        "ru": "Застраховано до 20 000 000 ₸ на каждого вкладчика",
        "kk": "Әрбір салымшы үшін 20 000 000 ₸ дейін сақтандырылған"
    },
    "Highest tier of international payment card security": {
        "en": "Highest tier of international payment card security",
        "ru": "Высший международный уровень безопасности банковских карт",
        "kk": "Төлем карталары қауіпсіздігінің ең жоғары халықаралық деңгейі"
    },
    "Global standard for information security management": {
        "en": "Global standard for information security management",
        "ru": "Глобальный стандарт управления информационной безопасностью",
        "kk": "Ақпараттық қауіпсіздікті басқарудың ғаламдық стандарты"
    },
    "Blocks 99.98% of fraudulent attempts in sub-seconds": {
        "en": "Blocks 99.98% of fraudulent attempts in sub-seconds",
        "ru": "Блокирует 99.98% попыток мошенничества за доли секунды",
        "kk": "Алаяқтық әрекеттердің 99.98%-ын секундтың үлесінде бұғаттайды"
    },
    "Indexed IBAN routing and precomputed aggregation algorithms enable instant domestic and international clearance.": {
        "en": "Indexed IBAN routing and precomputed aggregation algorithms enable instant domestic and international clearance.",
        "ru": "Индексированная маршрутизация IBAN и алгоритмы предварительной агрегации обеспечивают мгновенный клиринг внутри страны и за рубежом.",
        "kk": "Индекстелген IBAN бағыттауы және алдын ала есептелген алгоритмдер лездік клирингті қамтамасыз етеді."
    },
    "256-bit AES encryption at rest and in transit, PBKDF2 credential hashing, and AI-driven fraud anomaly detection.": {
        "en": "256-bit AES encryption at rest and in transit, PBKDF2 credential hashing, and AI-driven fraud anomaly detection.",
        "ru": "256-битное шифрование AES при хранении и передаче данных, хэширование паролей PBKDF2 и выявление аномалий с помощью ИИ.",
        "kk": "Деректерді сақтау және тасымалдаудағы 256-биттік AES шифрлауы, PBKDF2 хэштеуі және алаяқтықты анықтауға арналған ЖИ."
    },
    "See it in action": {
        "en": "See it in action",
        "ru": "Как это работает",
        "kk": "Жұмыс барысы"
    },
    "businesses and clients trust RocketBank": {
        "en": "businesses and clients trust RocketBank",
        "ru": "клиентов и компаний доверяют RocketBank",
        "kk": "клиент пен бизнес RocketBank-ке сенеді"
    },
    "12,000+ businesses and clients trust RocketBank": {
        "en": "12,000+ businesses and clients trust RocketBank",
        "ru": "12 000+ клиентов и компаний доверяют RocketBank",
        "kk": "12 000+ клиент пен бизнес RocketBank-ке сенеді"
    },
    "12,000+ clients trust RocketBank": {
        "en": "12,000+ clients trust RocketBank",
        "ru": "12 000+ клиентов доверяют RocketBank",
        "kk": "12 000+ клиент RocketBank-ке сенеді"
    },
    "Revenue growth": {
        "en": "Revenue growth",
        "ru": "Рост выручки",
        "kk": "Кіріс өсімі"
    },
    "Settlement time": {
        "en": "Settlement time",
        "ru": "Время расчетов",
        "kk": "Есеп айырысу уақыты"
    },
    "ROCKETBANK COMMAND CENTER": {
        "en": "ROCKETBANK COMMAND CENTER",
        "ru": "КОМАНДНЫЙ ЦЕНТР ROCKETBANK",
        "kk": "ROCKETBANK БАСҚАРУ ОРТАЛЫҒЫ"
    },
    "Balance": {
        "en": "Balance",
        "ru": "Баланс",
        "kk": "Теңгерім"
    },
    "Sent": {
        "en": "Sent",
        "ru": "Отправлено",
        "kk": "Жіберілді"
    },
    "Received": {
        "en": "Received",
        "ru": "Получено",
        "kk": "Алынды"
    },
    "Volume — 7 days": {
        "en": "Volume — 7 days",
        "ru": "Объем — 7 дней",
        "kk": "Көлемі — 7 күн"
    },
    "Global Clearing Payout": {
        "en": "Global Clearing Payout",
        "ru": "Международная выплата клиринга",
        "kk": "Халықаралық клиринг төлемі"
    },
    "Kaspi / Stripe Payout": {
        "en": "Kaspi / Stripe Payout",
        "ru": "Выплата Kaspi / Stripe",
        "kk": "Kaspi / Stripe төлемі"
    },
    "Subscription renewal": {
        "en": "Subscription renewal",
        "ru": "Продление подписки",
        "kk": "Жазылымды жаңарту"
    },
    "Interbank Multi-Currency Swap": {
        "en": "Interbank Multi-Currency Swap",
        "ru": "Межбанковский мультивалютный своп",
        "kk": "Банкаралық мультивалюталық своп"
    },
    "Total volume processed": {
        "en": "Total volume processed",
        "ru": "Общий обработанный объем",
        "kk": "Өңделген жалпы көлем"
    },
    "Active clients & accounts": {
        "en": "Active clients & accounts",
        "ru": "Активных клиентов и счетов",
        "kk": "Белсенді клиенттер мен шоттар"
    },
    "Uptime guarantee": {
        "en": "Uptime guarantee",
        "ru": "Гарантия доступности",
        "kk": "Үздіксіз жұмыс кепілдігі"
    },
    "Zero downtime recorded": {
        "en": "Zero downtime recorded",
        "ru": "0 минут сбоев за все время",
        "kk": "Үзіліссіз тұрақты жұмыс"
    },
    "Domestic transfer fees": {
        "en": "Domestic transfer fees",
        "ru": "Комиссия за внутренние переводы",
        "kk": "Ішкі аударымдар комиссиясы"
    },
    "100% free peer-to-peer": {
        "en": "100% free peer-to-peer",
        "ru": "100% бесплатно между клиентами",
        "kk": "Клиенттер арасында 100% тегін"
    },
    "Mon": {
        "en": "Mon",
        "ru": "Пн",
        "kk": "Дс"
    },
    "Tue": {
        "en": "Tue",
        "ru": "Вт",
        "kk": "Сс"
    },
    "Wed": {
        "en": "Wed",
        "ru": "Ср",
        "kk": "Ср"
    },
    "Thu": {
        "en": "Thu",
        "ru": "Чт",
        "kk": "Бс"
    },
    "Fri": {
        "en": "Fri",
        "ru": "Пт",
        "kk": "Жм"
    },
    "Sat": {
        "en": "Sat",
        "ru": "Сб",
        "kk": "Сн"
    },
    "Today": {
        "en": "Today",
        "ru": "Сегодня",
        "kk": "Бүгін"
    },
    "Yesterday": {
        "en": "Yesterday",
        "ru": "Вчера",
        "kk": "Кеше"
    },
    "today": {
        "en": "today",
        "ru": "сегодня",
        "kk": "бүгін"
    },
    "This month": {
        "en": "This month",
        "ru": "В этом месяце",
        "kk": "Осы айда"
    },
    "this month": {
        "en": "this month",
        "ru": "в этом месяце",
        "kk": "осы айда"
    },
    "year over year": {
        "en": "year over year",
        "ru": "по сравнению с прошлым годом",
        "kk": "өткен жылмен салыстырғанда"
    },
    "countries": {
        "en": "countries",
        "ru": "стран",
        "kk": "ел"
    },
    "currencies": {
        "en": "currencies",
        "ru": "валют",
        "kk": "валюта"
    },
    "transfers": {
        "en": "transfers",
        "ru": "переводов",
        "kk": "аударым"
    },
    "Platform features": {
        "en": "Platform features",
        "ru": "Возможности платформы",
        "kk": "Платформа мүмкіндіктері"
    },
    "Everything your finances need": {
        "en": "Everything your finances need",
        "ru": "Все необходимое для ваших финансов",
        "kk": "Сіздің қаржыңызға қажеттінің барлығы"
    },
    "One platform to send, receive, track, and multiply your capital. No switching between disjointed tools.": {
        "en": "One platform to send, receive, track, and multiply your capital. No switching between disjointed tools.",
        "ru": "Единая платформа для переводов, аналитики и приумножения капитала без переключения между разрозненными сервисами.",
        "kk": "Қаражатты аударуға, бақылауға және көбейтуге арналған бірыңғай платформа. Бөлек құралдар арасында ауысудың қажеті жоқ."
    },
    "Instant transfers": {
        "en": "Instant transfers",
        "ru": "Мгновенные переводы",
        "kk": "Лездік аударымдар"
    },
    "Sub-second": {
        "en": "Sub-second",
        "ru": "Доли секунды",
        "kk": "Лездік"
    },
    "190+ countries": {
        "en": "190+ countries",
        "ru": "190+ стран",
        "kk": "190+ ел"
    },
    "Zero fees": {
        "en": "Zero fees",
        "ru": "0% комиссий",
        "kk": "0% комиссия"
    },
    "Smart analytics": {
        "en": "Smart analytics",
        "ru": "Умная аналитика",
        "kk": "Ақылды талдау"
    },
    "AI forecasting": {
        "en": "AI forecasting",
        "ru": "Прогнозы ИИ",
        "kk": "ЖИ болжамы"
    },
    "Anomaly alerts": {
        "en": "Anomaly alerts",
        "ru": "Оповещения об аномалиях",
        "kk": "Аномалия ескертулері"
    },
    "Custom reports": {
        "en": "Custom reports",
        "ru": "Пользовательские отчеты",
        "kk": "Арнайы есептер"
    },
    "Multi-currency accounts": {
        "en": "Multi-currency accounts",
        "ru": "Мультивалютные счета",
        "kk": "Мультивалюталық шоттар"
    },
    "35+ currencies": {
        "en": "35+ currencies",
        "ru": "35+ валют",
        "kk": "35+ валюта"
    },
    "Interbank rates": {
        "en": "Interbank rates",
        "ru": "Межбанковский курс",
        "kk": "Банкаралық бағам"
    },
    "Live FX swap": {
        "en": "Live FX swap",
        "ru": "Мгновенный FX своп",
        "kk": "Лездік FX своп"
    },
    "Enterprise security": {
        "en": "Enterprise security",
        "ru": "Корпоративная безопасность",
        "kk": "Корпоративтік қауіпсіздік"
    },
    "AI fraud detection": {
        "en": "AI fraud detection",
        "ru": "ИИ защита от мошенничества",
        "kk": "Алаяқтықтан ЖИ қорғау"
    },
    "256-bit AES": {
        "en": "256-bit AES",
        "ru": "256-битное AES",
        "kk": "256-биттік AES"
    },
    "Transfers": {
        "en": "Transfers",
        "ru": "Переводы",
        "kk": "Аударымдар"
    },
    "Analytics": {
        "en": "Analytics",
        "ru": "Аналитика",
        "kk": "Талдау"
    },
    "Multi-currency": {
        "en": "Multi-currency",
        "ru": "Мультивалюта",
        "kk": "Мультивалюта"
    },
    "Security": {
        "en": "Security",
        "ru": "Безопасность",
        "kk": "Қауіпсіздік"
    },
    "Sent today": {
        "en": "Sent today",
        "ru": "Отправлено сегодня",
        "kk": "Бүгін жіберілген"
    },
    "Avg. speed": {
        "en": "Avg. speed",
        "ru": "Средняя скорость",
        "kk": "Орташа жылдамдық"
    },
    "Atomic lock": {
        "en": "Atomic lock",
        "ru": "Атомарный лок",
        "kk": "Атомдық қорғау"
    },
    "Completed": {
        "en": "Completed",
        "ru": "Завершено",
        "kk": "Орындалды"
    },
    "Forecasted balance": {
        "en": "Forecasted balance",
        "ru": "Прогнозный баланс",
        "kk": "Болжамды теңгерім"
    },
    "Next 30 days": {
        "en": "Next 30 days",
        "ru": "Следующие 30 дней",
        "kk": "Алдағы 30 күн"
    },
    "Anomalies": {
        "en": "Anomalies",
        "ru": "Аномалии",
        "kk": "Аномалиялар"
    },
    "All clean": {
        "en": "All clean",
        "ru": "Все в норме",
        "kk": "Барлығы дұрыс"
    },
    "Volume trend — 8 weeks": {
        "en": "Volume trend — 8 weeks",
        "ru": "Тренд объема — 8 недель",
        "kk": "Көлем тренді — 8 апта"
    },
    "Operations": {
        "en": "Operations",
        "ru": "Операции",
        "kk": "Операциялар"
    },
    "Cross-border": {
        "en": "Cross-border",
        "ru": "Трансграничные",
        "kk": "Халықаралық"
    },
    "Active Currencies": {
        "en": "Active Currencies",
        "ru": "Активные валюты",
        "kk": "Белсенді валюталар"
    },
    "Multi-IBAN active": {
        "en": "Multi-IBAN active",
        "ru": "Мульти-IBAN активен",
        "kk": "Мульти-IBAN белсенді"
    },
    "FX Saved": {
        "en": "FX Saved",
        "ru": "Экономия на FX",
        "kk": "FX бойынша үнемделген"
    },
    "Primary": {
        "en": "Primary",
        "ru": "Основной",
        "kk": "Негізгі"
    },
    "KDIF Deposit Guarantee": {
        "en": "KDIF Deposit Guarantee",
        "ru": "Гарантия депозитов КФГД",
        "kk": "ҚДКҚ депозиттік кепілдігі"
    },
    "24/7 SOC": {
        "en": "24/7 SOC",
        "ru": "Круглосуточный SOC",
        "kk": "Тәулік бойы SOC"
    },
    "AI Anomaly Guard": {
        "en": "AI Anomaly Guard",
        "ru": "ИИ защита от аномалий",
        "kk": "ЖИ аномалия күзеті"
    },
    "Protecting": {
        "en": "Protecting",
        "ru": "Защита активна",
        "kk": "Қорғалуда"
    },
    "Online": {
        "en": "Online",
        "ru": "В сети",
        "kk": "Желіде"
    },
    "Active": {
        "en": "Active",
        "ru": "Активно",
        "kk": "Белсенді"
    },
    "Guaranteed": {
        "en": "Guaranteed",
        "ru": "Гарантировано",
        "kk": "Кепілдендірілген"
    },
    "Live platform": {
        "en": "Live platform",
        "ru": "Интерактивная платформа",
        "kk": "Интерактивті платформа"
    },
    "Your financial command center": {
        "en": "Your financial command center",
        "ru": "Ваш финансовый командный центр",
        "kk": "Сіздің қаржылық басқару орталығыңыз"
    },
    "Portfolio overview": {
        "en": "Portfolio overview",
        "ru": "Обзор портфеля",
        "kk": "Портфельге шолу"
    },
    "Live data": {
        "en": "Live data",
        "ru": "Данные в реальном времени",
        "kk": "Нақты уақыттағы деректер"
    },
    "Cash flow": {
        "en": "Cash flow",
        "ru": "Денежный поток",
        "kk": "Ақша ағыны"
    },
    "Net positive this month": {
        "en": "Net positive this month",
        "ru": "Положительный баланс за месяц",
        "kk": "Осы айдағы оң динамика"
    },
    "Inbound": {
        "en": "Inbound",
        "ru": "Поступления",
        "kk": "Түсімдер"
    },
    "Outbound": {
        "en": "Outbound",
        "ru": "Списания",
        "kk": "Шығыстар"
    },
    "Monthly Transactions": {
        "en": "Monthly Transactions",
        "ru": "Транзакций за месяц",
        "kk": "Айлық транзакциялар"
    },
    "Sub-second execution": {
        "en": "Sub-second execution",
        "ru": "Мгновенное исполнение",
        "kk": "Лездік орындалу"
    },
    "Successful": {
        "en": "Successful",
        "ru": "Успешные",
        "kk": "Сәтті"
    },
    "Failed": {
        "en": "Failed",
        "ru": "Отклоненные",
        "kk": "Қабылданбаған"
    },
    "Bank Card Tiers": {
        "en": "Bank Card Tiers",
        "ru": "Уровни банковских карт",
        "kk": "Банк карталарының деңгейлері"
    },
    "Tailored for every ambition": {
        "en": "Tailored for every ambition",
        "ru": "Создано для любых амбиций",
        "kk": "Әрбір мақсат үшін жасалған"
    },
    "Monthly": {
        "en": "Monthly",
        "ru": "В месяц",
        "kk": "Ай сайын"
    },
    "Annual": {
        "en": "Annual",
        "ru": "В год",
        "kk": "Жылдық"
    },
    "Save 35%": {
        "en": "Save 35%",
        "ru": "Скидка 35%",
        "kk": "35% үнемдеу"
    },
    "Save 35%%": {
        "en": "Save 35%%",
        "ru": "Скидка 35%",
        "kk": "35% үнемдеу"
    },
    "Gold Card": {
        "en": "Gold Card",
        "ru": "Карта Gold",
        "kk": "Gold Card"
    },
    "Platinum Card": {
        "en": "Platinum Card",
        "ru": "Карта Platinum",
        "kk": "Platinum Card"
    },
    "Black Card": {
        "en": "Black Card",
        "ru": "Карта Black",
        "kk": "Black Card"
    },
    "RocketBank Gold": {
        "en": "RocketBank Gold",
        "ru": "RocketBank Gold",
        "kk": "RocketBank Gold"
    },
    "RocketBank Platinum": {
        "en": "RocketBank Platinum",
        "ru": "RocketBank Platinum",
        "kk": "RocketBank Platinum"
    },
    "RocketBank Black": {
        "en": "RocketBank Black",
        "ru": "RocketBank Black",
        "kk": "RocketBank Black"
    },
    "per month": {
        "en": "per month",
        "ru": "в месяц",
        "kk": "айына"
    },
    "free forever": {
        "en": "free forever",
        "ru": "бесплатно навсегда",
        "kk": "мәңгілікке тегін"
    },
    "Zero annual maintenance fees": {
        "en": "Zero annual maintenance fees",
        "ru": "0 ₸ за годовое обслуживание",
        "kk": "Жылдық қызмет көрсету 0 ₸"
    },
    "per month, billed": {
        "en": "per month, billed",
        "ru": "в месяц, при оплате",
        "kk": "айына, төлем түрі"
    },
    "monthly": {
        "en": "monthly",
        "ru": "ежемесячно",
        "kk": "ай сайын"
    },
    "annually": {
        "en": "annually",
        "ru": "за год",
        "kk": "жылдық"
    },
    "billed annually": {
        "en": "billed annually",
        "ru": "при оплате за год",
        "kk": "жылдық төлем кезінде"
    },
    "billed": {
        "en": "billed",
        "ru": "списание",
        "kk": "төлем"
    },
    "Most popular": {
        "en": "Most popular",
        "ru": "Популярный выбор",
        "kk": "Ең танымал"
    },
    "Cashback on all purchases": {
        "en": "Cashback on all purchases",
        "ru": "Кэшбэк на все покупки",
        "kk": "Барлық сатып алуларға кэшбэк"
    },
    "Instant digital & physical issuance": {
        "en": "Instant digital & physical issuance",
        "ru": "Мгновенный выпуск цифровой и физической карты",
        "kk": "Цифрлық және пластикалық картаны лездік шығару"
    },
    "Zero fee KZT transfers by IBAN": {
        "en": "Zero fee KZT transfers by IBAN",
        "ru": "Бесплатные переводы в KZT по IBAN",
        "kk": "IBAN арқылы теңгемен комиссиясыз аударымдар"
    },
    "Up to 5 multi-currency accounts": {
        "en": "Up to 5 multi-currency accounts",
        "ru": "До 5 мультивалютных счетов",
        "kk": "5-ке дейін мультивалюталық шот"
    },
    "Standard 24/7 chat support": {
        "en": "Standard 24/7 chat support",
        "ru": "Стандартная поддержка 24/7 в чате",
        "kk": "Чатта тәулік бойы стандартты қолдау"
    },
    "Cashback on dining & travel": {
        "en": "Cashback on dining & travel",
        "ru": "Кэшбэк в ресторанах и путешествиях",
        "kk": "Мейрамханалар мен саяхаттардағы кэшбэк"
    },
    "Titanium metallic physical card": {
        "en": "Titanium metallic physical card",
        "ru": "Титановая металлическая карта",
        "kk": "Титаннан жасалған металл карта"
    },
    "Airport lounge access (LoungeKey)": {
        "en": "Airport lounge access (LoungeKey)",
        "ru": "Доступ в бизнес-залы аэропортов (LoungeKey)",
        "kk": "Әуежайлардың бизнес-залдарына қолжетімділік (LoungeKey)"
    },
    "Priority 24/7 dedicated banker": {
        "en": "Priority 24/7 dedicated banker",
        "ru": "Персональный банкир 24/7",
        "kk": "Жеке банкир 24/7"
    },
    "15 foreign currencies with zero FX fee": {
        "en": "15 foreign currencies with zero FX fee",
        "ru": "15 иностранных валют без комиссий за конвертацию",
        "kk": "Айырбастау комиссиясынсыз 15 шетелдік валюта"
    },
    "Extended daily withdrawal limits": {
        "en": "Extended daily withdrawal limits",
        "ru": "Повышенные суточные лимиты на снятие наличных",
        "kk": "Қолма-қол ақша алуға ұлғайтылған тәуліктік лимиттер"
    },
    "Elite": {
        "en": "Elite",
        "ru": "Индивидуально",
        "kk": "Арнайы"
    },
    "tailored for high net worth": {
        "en": "tailored for high net worth",
        "ru": "для премиального капитала",
        "kk": "ірі капитал иелеріне арналған"
    },
    "Unlimited premium cashback": {
        "en": "Unlimited premium cashback",
        "ru": "Неограниченный премиальный кэшбэк",
        "kk": "Шектеусіз премиум кэшбэк"
    },
    "PVD-coated obsidian steel card": {
        "en": "PVD-coated obsidian steel card",
        "ru": "Карта из обсидиановой стали с PVD-покрытием",
        "kk": "PVD жабындысы бар обсидиан болат картасы"
    },
    "Personal executive wealth manager": {
        "en": "Personal executive wealth manager",
        "ru": "Персональный управляющий частным капиталом",
        "kk": "Жеке капиталды басқарушы менеджер"
    },
    "Unlimited international SWIFT transfers": {
        "en": "Unlimited international SWIFT transfers",
        "ru": "Безлимитные международные переводы SWIFT",
        "kk": "Шектеусіз халықаралық SWIFT аударымдары"
    },
    "All 35+ global currencies included": {
        "en": "All 35+ global currencies included",
        "ru": "Все 35+ мировых валют без ограничений",
        "kk": "Барлық 35+ әлемдік валюта қамтылған"
    },
    "Custom credit limits up to ₸50,000,000": {
        "en": "Custom credit limits up to ₸50,000,000",
        "ru": "Индивидуальный кредитный лимит до ₸50,000,000",
        "kk": "₸50 000 000-ға дейінгі жеке несиелік лимит"
    },
    "Order Gold Card": {
        "en": "Order Gold Card",
        "ru": "Оформить Gold",
        "kk": "Gold картасын ашу"
    },
    "Order Platinum Card": {
        "en": "Order Platinum Card",
        "ru": "Оформить Platinum",
        "kk": "Platinum картасын ашу"
    },
    "Request Black Card": {
        "en": "Request Black Card",
        "ru": "Запросить Black",
        "kk": "Black картасына өтінім беру"
    },
    "Compare Other Tiers": {
        "en": "Compare Other Tiers",
        "ru": "Сравнить другие карты",
        "kk": "Басқа карталарды салыстыру"
    },
    "Other Available Card Tiers": {
        "en": "Other Available Card Tiers",
        "ru": "Другие доступные карты",
        "kk": "Басқа қолжетімді карталар"
    },
    "Filter by tier": {
        "en": "Filter by tier",
        "ru": "Фильтр по уровню",
        "kk": "Деңгей бойынша сүзу"
    },
    "Search cards": {
        "en": "Search cards",
        "ru": "Поиск карт",
        "kk": "Карталарды іздеу"
    },
    "Search cards by name...": {
        "en": "Search cards by name...",
        "ru": "Поиск карт по названию...",
        "kk": "Карталарды атауы бойынша іздеу..."
    },
    "Sort cards": {
        "en": "Sort cards",
        "ru": "Сортировка карт",
        "kk": "Карталарды сұрыптау"
    },
    "Highest Cashback": {
        "en": "Highest Cashback",
        "ru": "Максимальный кэшбэк",
        "kk": "Ең жоғары кэшбэк"
    },
    "Lowest Annual Fee": {
        "en": "Lowest Annual Fee",
        "ru": "Минимальная годовая плата",
        "kk": "Ең төменгі жылдық төлем"
    },
    "My Payment Cards": {
        "en": "My Payment Cards",
        "ru": "Мои банковские карты",
        "kk": "Менің төлем карталарым"
    },
    "My Payment Cards | RocketBank": {
        "en": "My Payment Cards | RocketBank",
        "ru": "Мои банковские карты | RocketBank",
        "kk": "Менің төлем карталарым | RocketBank"
    },
    "RocketBank Payment Cards": {
        "en": "RocketBank Payment Cards",
        "ru": "Банковские карты RocketBank",
        "kk": "RocketBank төлем карталары"
    },
    "Order New Card (Wizard)": {
        "en": "Order New Card (Wizard)",
        "ru": "Заказать новую карту (Мастер)",
        "kk": "Жаңа картаға тапсырыс беру (Шебер)"
    },
    "Freeze card": {
        "en": "Freeze card",
        "ru": "Заморозить карту",
        "kk": "Картаны бұғаттау"
    },
    "Unfreeze card": {
        "en": "Unfreeze card",
        "ru": "Разморозить карту",
        "kk": "Картаны бұғаттан шығару"
    },
    "No hidden maintenance costs": {
        "en": "No hidden maintenance costs",
        "ru": "Без скрытых комиссий за обслуживание",
        "kk": "Жасырын қызмет ақысыз"
    },
    "Explore RocketBank's premium debit and credit cards with up to 10% cashback, zero maintenance fee, and instant digital issuing.": {
        "en": "Explore RocketBank's premium debit and credit cards with up to 10% cashback, zero maintenance fee, and instant digital issuing.",
        "ru": "Премиальные дебетовые и кредитные карты RocketBank с кэшбэком до 10%, бесплатным обслуживанием и мгновенным цифровым выпуском.",
        "kk": "RocketBank-тің 10%-ға дейін кэшбэгі, тегін қызмет көрсетуі және лездік цифрлық шығарылымы бар премиум дебеттік және несиелік карталары."
    },
    "Explore RocketBank's premium debit and credit cards with up to 10%% cashback, zero maintenance fee, and instant digital issuing.": {
        "en": "Explore RocketBank's premium debit and credit cards with up to 10%% cashback, zero maintenance fee, and instant digital issuing.",
        "ru": "Премиальные дебетовые и кредитные карты RocketBank с кэшбэком до 10%, бесплатным обслуживанием и мгновенным цифровым выпуском.",
        "kk": "RocketBank-тің 10%-ға дейін кэшбэгі, тегін қызмет көрсетуі және лездік цифрлық шығарылымы бар премиум дебеттік және несиелік карталары."
    },
    "Bank-grade protection": {
        "en": "Bank-grade protection",
        "ru": "Банковский уровень защиты",
        "kk": "Банктік деңгейдегі қорғаныс"
    },
    "Read architecture report": {
        "en": "Read architecture report",
        "ru": "Отчет об архитектуре",
        "kk": "Архитектуралық есеп"
    },
    "Compliant": {
        "en": "Compliant",
        "ru": "Соответствует",
        "kk": "Сәйкес келеді"
    },
    "Certified": {
        "en": "Certified",
        "ru": "Сертифицирован",
        "kk": "Сертификатталған"
    },
    "Always on": {
        "en": "Always on",
        "ru": "Всегда активно",
        "kk": "Әрдайым қосулы"
    },
    "Client experiences": {
        "en": "Client experiences",
        "ru": "Отзывы клиентов",
        "kk": "Клиенттердің пікірлері"
    },
    "Trusted by leaders across industries": {
        "en": "Trusted by leaders across industries",
        "ru": "Нам доверяют лидеры различных отраслей",
        "kk": "Бізге түрлі сала көшбасшылары сенеді"
    },
    "Pause": {
        "en": "Pause",
        "ru": "Пауза",
        "kk": "Кідірту"
    },
    "Play": {
        "en": "Play",
        "ru": "Воспроизвести",
        "kk": "Ойнату"
    },
    "Pause testimonials": {
        "en": "Pause testimonials",
        "ru": "Приостановить отзывы",
        "kk": "Пікірлерді кідірту"
    },
    "CFO at Hive Commerce": {
        "en": "CFO at Hive Commerce",
        "ru": "CFO в Hive Commerce",
        "kk": "Hive Commerce қаржы директоры"
    },
    "RocketBank cut our corporate international settlement time from 3 days to under 2 seconds. It completely redefined our treasury speed.": {
        "en": "RocketBank cut our corporate international settlement time from 3 days to under 2 seconds. It completely redefined our treasury speed.",
        "ru": "RocketBank сократил время наших международных расчетов с 3 дней до 2 секунд. Это полностью изменило скорость управления нашим капиталом.",
        "kk": "RocketBank халықаралық төлемдеріміздің мерзімін 3 күннен 2 секундқа дейін қысқартты. Бұл біздің қаржылық айналым жылдамдығымызды түбегейлі өзгертті."
    },
    "Finance Director, Nomad Labs": {
        "en": "Finance Director, Nomad Labs",
        "ru": "Финансовый директор, Nomad Labs",
        "kk": "Nomad Labs қаржы директоры"
    },
    "The multi-currency IBAN accounts saved us over ₸18M in FX conversions this year. The exchange rate transparency is unparalleled.": {
        "en": "The multi-currency IBAN accounts saved us over ₸18M in FX conversions this year. The exchange rate transparency is unparalleled.",
        "ru": "Мультивалютные счета IBAN сэкономили нам более ₸18 млн на конвертациях в этом году. Прозрачность обменного курса безупречна.",
        "kk": "Мультивалюталық IBAN шоттары биыл бізге валюта айырбастаудан ₸18 млн астам қаржы үнемдеді. Бағамдардың ашықтығы тамаша."
    },
    "Head of Ops, Stackflow": {
        "en": "Head of Ops, Stackflow",
        "ru": "Операционный директор, Stackflow",
        "kk": "Stackflow операциялық директоры"
    },
    "Finally a modern digital banking platform that feels ultra-fast and engineered for modern engineers and tech businesses.": {
        "en": "Finally a modern digital banking platform that feels ultra-fast and engineered for modern engineers and tech businesses.",
        "ru": "Наконец-то появился современный цифровой банк, работающий молниеносно и созданный специально для IT-компаний и технологичного бизнеса.",
        "kk": "Ақырында IT-компаниялар мен заманауи бизнеске арналған, өте жылдам жұмыс істейтін цифрлық банк пайда болды."
    },
    "CTO at Vaulted": {
        "en": "CTO at Vaulted",
        "ru": "Технический директор Vaulted",
        "kk": "Vaulted техникалық директоры"
    },
    "Migrated our business accounts in one afternoon. The REST API documentation and instant webhooks are exceptional.": {
        "en": "Migrated our business accounts in one afternoon. The REST API documentation and instant webhooks are exceptional.",
        "ru": "Перевели наши бизнес-счета за один день. Документация REST API и мгновенные вебхуки работают безупречно.",
        "kk": "Барлық бизнес-шоттарымызды бір күнде көшірдік. REST API құжаттамасы мен лездік вебхуктер өте керемет жасалған."
    },
    "Founder, CloudMint": {
        "en": "Founder, CloudMint",
        "ru": "Основатель CloudMint",
        "kk": "CloudMint негізін қалаушы"
    },
    "The automated fraud detection and instant card freeze give our executive team complete peace of mind.": {
        "en": "The automated fraud detection and instant card freeze give our executive team complete peace of mind.",
        "ru": "Автоматическая система предотвращения мошенничества и мгновенная блокировка карт дают полное спокойствие нашему руководству.",
        "kk": "Алаяқтықты автоматты түрде анықтау және картаны бірден бұғаттау біздің басшылыққа толық сенімділік береді."
    },
    "Controller, Drift Studio": {
        "en": "Controller, Drift Studio",
        "ru": "Финансовый контролер, Drift Studio",
        "kk": "Drift Studio қаржы бақылаушысы"
    },
    "Automated payroll and batch payments save our accounting team over 25 hours every month.": {
        "en": "Automated payroll and batch payments save our accounting team over 25 hours every month.",
        "ru": "Автоматическая зарплатная ведомость и реестровые платежи экономят нашей бухгалтерии более 25 часов каждый месяц.",
        "kk": "Жалақыны автоматты төлеу және жаппай аударымдар біздің есепшілерге ай сайын 25 сағаттан астам уақытты үнемдейді."
    },
    "Mobile app": {
        "en": "Mobile app",
        "ru": "Мобильное приложение",
        "kk": "Мобильді қосымша"
    },
    "Your bank, in your pocket": {
        "en": "Your bank, in your pocket",
        "ru": "Ваш банк всегда под рукой",
        "kk": "Сіздің банкіңіз әрқашан қалтаңызда"
    },
    "Download on the": {
        "en": "Download on the",
        "ru": "Загрузите в",
        "kk": "Жүктеп алыңыз:"
    },
    "Get it on": {
        "en": "Get it on",
        "ru": "Доступно в",
        "kk": "Қолжетімді:"
    },
    "Or scan our": {
        "en": "Or scan our",
        "ru": "Или отсканируйте",
        "kk": "Немесе сканерлеңіз:"
    },
    "Got questions?": {
        "en": "Got questions?",
        "ru": "Есть вопросы?",
        "kk": "Сұрақтарыңыз бар ма?"
    },
    "Frequently asked": {
        "en": "Frequently asked",
        "ru": "Часто задаваемые вопросы",
        "kk": "Жиі қойылатын сұрақтар"
    },
    "Expand all": {
        "en": "Expand all",
        "ru": "Развернуть все",
        "kk": "Барлығын ашу"
    },
    "Collapse all": {
        "en": "Collapse all",
        "ru": "Свернуть все",
        "kk": "Барлығын жинау"
    },
    "How quickly can I open an account and start sending payments?": {
        "en": "How quickly can I open an account and start sending payments?",
        "ru": "Как быстро я могу открыть счет и начать переводить деньги?",
        "kk": "Шотты қаншалықты жылдам ашып, төлемдерді бастауға болады?"
    },
    "You can be up and running in under 3 minutes. Register your account online, verify with instant biometric/document check, and start transacting with zero paperwork.": {
        "en": "You can be up and running in under 3 minutes. Register your account online, verify with instant biometric/document check, and start transacting with zero paperwork.",
        "ru": "Вы можете начать работу менее чем за 3 минуты. Зарегистрируйтесь онлайн, пройдите быструю биометрическую проверку и совершайте платежи без бумажной волокиты.",
        "kk": "Сіз 3 минуттан аз уақыт ішінде бастай аласыз. Онлайн тіркеліп, жылдам биометриялық тексеруден өтіңіз және құжаттарсыз төлемдерді жасаңыз."
    },
    "What are the transaction fees for domestic and global transfers?": {
        "en": "What are the transaction fees for domestic and global transfers?",
        "ru": "Каковы комиссии за внутренние и международные переводы?",
        "kk": "Ішкі және халықаралық аударымдар үшін комиссия қандай?"
    },
    "All standard domestic transfers and peer-to-peer RocketBank transfers are 100% free with 0.00 KZT commission. Multi-currency international rails start at interbank live FX rates with zero hidden markups.": {
        "en": "All standard domestic transfers and peer-to-peer RocketBank transfers are 100% free with 0.00 KZT commission. Multi-currency international rails start at interbank live FX rates with zero hidden markups.",
        "ru": "Все стандартные внутренние переводы и переводы между клиентами RocketBank бесплатны с комиссией 0,00 ₸. Международные переводы производятся по межбанковским курсам без скрытых наценок.",
        "kk": "RocketBank ішіндегі барлық стандартты ішкі және клиент арасындағы аударымдар 0,00 ₸ комиссиямен 100% тегін. Халықаралық аударымдар жасырын үстемеақысыз тікелей банкаралық бағамдар бойынша жүргізіледі."
    },
    "Are deposits insured by the Kazakhstan Deposit Insurance Fund?": {
        "en": "Are deposits insured by the Kazakhstan Deposit Insurance Fund?",
        "ru": "Застрахованы ли депозиты Казахстанским фондом гарантирования депозитов?",
        "kk": "Депозиттер Қазақстанның депозиттерге кепілдік беру қорымен сақтандырылған ба?"
    },
    "Yes. All deposits held in RocketBank are fully guaranteed up to 20,000,000 KZT per depositor in savings deposits by the KDIF under the laws of the Republic of Kazakhstan.": {
        "en": "Yes. All deposits held in RocketBank are fully guaranteed up to 20,000,000 KZT per depositor in savings deposits by the KDIF under the laws of the Republic of Kazakhstan.",
        "ru": "Да. Все сберегательные депозиты в RocketBank застрахованы на сумму до 20 000 000 ₸ на каждого вкладчика КФГД в соответствии с законодательством Республики Казахстан.",
        "kk": "Иә. RocketBank-тегі барлық жинақ депозиттеріне Қазақстан Республикасының заңнамасына сәйкес ҚДКҚ тарапынан әрбір салымшыға 20 000 000 ₸ дейін толық мемлекеттік кепілдік беріледі."
    },
    "How does RocketBank protect client funds and cards from fraud?": {
        "en": "How does RocketBank protect client funds and cards from fraud?",
        "ru": "Как RocketBank защищает средства клиентов и карты от мошенничества?",
        "kk": "RocketBank клиенттердің қаражаты мен карталарын алаяқтықтан қалай қорғайды?"
    },
    "We employ bank-grade 256-bit AES encryption, row-level ACID transactional concurrency locks, SOC 2 compliance, and AI-powered real-time anomaly detection to block fraud instantly.": {
        "en": "We employ bank-grade 256-bit AES encryption, row-level ACID transactional concurrency locks, SOC 2 compliance, and AI-powered real-time anomaly detection to block fraud instantly.",
        "ru": "Мы используем 256-битное шифрование AES банковского уровня, блокировки транзакций ACID на уровне строк, соответствие стандарту SOC 2 и ИИ-анализ аномалий в реальном времени.",
        "kk": "Біз банктік деңгейдегі 256-биттік AES шифрлауын, қатар деңгейіндегі ACID транзакциялық құлыптарын, SOC 2 стандартын және алаяқтықты лезде бұғаттау үшін ЖИ мониторингін қолданамыз."
    },
    "Can I integrate RocketBank with accounting tools and REST APIs?": {
        "en": "Can I integrate RocketBank with accounting tools and REST APIs?",
        "ru": "Могу ли я интегрировать RocketBank с бухгалтерскими системами и REST API?",
        "kk": "RocketBank-ті бухгалтерлік бағдарламалармен және REST API-мен біріктіруге бола ма?"
    },
    "Yes! RocketBank provides a full OpenAPI 3.0 / Swagger REST API with JWT authentication, webhook notifications, and automated export tools for finance and ERP platforms.": {
        "en": "Yes! RocketBank provides a full OpenAPI 3.0 / Swagger REST API with JWT authentication, webhook notifications, and automated export tools for finance and ERP platforms.",
        "ru": "Да! RocketBank предоставляет полный REST API (OpenAPI 3.0 / Swagger) с JWT-аутентификацией, вебхуками и автоматическим экспортом в учетные и ERP-системы.",
        "kk": "Иә! RocketBank қаржылық және ERP жүйелері үшін JWT аутентификациясы, вебхук хабарламалары және автоматты экспорт құралдары бар толық OpenAPI 3.0 / Swagger REST API ұсынады."
    },
    "How can I freeze my bank card if it is lost or compromised?": {
        "en": "How can I freeze my bank card if it is lost or compromised?",
        "ru": "Как заблокировать карту при утере или компрометации?",
        "kk": "Карта жоғалған немесе деректері бұзылған жағдайда оны қалай бұғаттауға болады?"
    },
    "You can freeze or unfreeze any debit or credit card instantly from your Client Dashboard or mobile interface with a single tap, blocking all physical and online transactions immediately.": {
        "en": "You can freeze or unfreeze any debit or credit card instantly from your Client Dashboard or mobile interface with a single tap, blocking all physical and online transactions immediately.",
        "ru": "Вы можете мгновенно заморозить или разморозить любую карту в личном кабинете или мобильном приложении одним нажатием, мгновенно заблокировав все операции.",
        "kk": "Сіз кез келген дебеттік немесе несиелік картаны клиенттік кабинеттен немесе мобильді қосымшадан бір басумен лезде бұғаттай немесе бұғаттан шығара аласыз."
    },
    "My Bank Accounts | RocketBank": {
        "en": "My Bank Accounts | RocketBank",
        "ru": "Мои банковские счета | RocketBank",
        "kk": "Менің банктік шоттарым | RocketBank"
    },
    "List of client accounts registered under your name in RocketBank": {
        "en": "List of client accounts registered under your name in RocketBank",
        "ru": "Список счетов, открытых на ваше имя в RocketBank",
        "kk": "RocketBank-те сіздің атыңызға ашылған шоттар тізімі"
    },
    "Open RocketBank Account": {
        "en": "Open RocketBank Account",
        "ru": "Открыть счет в RocketBank",
        "kk": "RocketBank шотын ашу"
    },
    "Open an Account | RocketBank": {
        "en": "Open an Account | RocketBank",
        "ru": "Открыть счет | RocketBank",
        "kk": "Шот ашу | RocketBank"
    },
    "Open account in 3 minutes": {
        "en": "Open account in 3 minutes",
        "ru": "Открытие счета за 3 минуты",
        "kk": "Шотты 3 минутта ашу"
    },
    "Checking Balance": {
        "en": "Checking Balance",
        "ru": "Баланс текущего счета",
        "kk": "Ағымдағы шот теңгерімі"
    },
    "Savings Balance": {
        "en": "Savings Balance",
        "ru": "Баланс сберегательного счета",
        "kk": "Жинақ шотының теңгерімі"
    },
    "Opened Date": {
        "en": "Opened Date",
        "ru": "Дата открытия",
        "kk": "Ашылған күні"
    },
    "SAVING GOALS": {
        "en": "SAVING GOALS",
        "ru": "ЦЕЛИ НАКОПЛЕНИЙ",
        "kk": "ЖИНАҚ МАҚСАТТАРЫ"
    },
    "Saving Goals Tracker": {
        "en": "Saving Goals Tracker",
        "ru": "Трекер целей накоплений",
        "kk": "Жинақ мақсаттары трекері"
    },
    "Active Saving Goals": {
        "en": "Active Saving Goals",
        "ru": "Активные цели накоплений",
        "kk": "Белсенді жинақ мақсаттары"
    },
    "Monthly budget expenditure meter": {
        "en": "Monthly budget expenditure meter",
        "ru": "Индикатор расходов ежемесячного бюджета",
        "kk": "Айлық бюджет шығыстарының өлшегіші"
    },
    "Critical (>85%)": {
        "en": "Critical (>85%)",
        "ru": "Критический (>85%)",
        "kk": "Қауіпті (>85%)"
    },
    "Critical (>85%%)": {
        "en": "Critical (>85%%)",
        "ru": "Критический (>85%)",
        "kk": "Қауіпті (>85%)"
    },
    "Optimal (<60%)": {
        "en": "Optimal (<60%)",
        "ru": "Оптимальный (<60%)",
        "kk": "Оңтайлы (<60%)"
    },
    "Optimal (<60%%)": {
        "en": "Optimal (<60%%)",
        "ru": "Оптимальный (<60%)",
        "kk": "Оңтайлы (<60%)"
    },
    "QUICK SERVICES": {
        "en": "QUICK SERVICES",
        "ru": "БЫСТРЫЕ ОПЕРАЦИИ",
        "kk": "ЖЫЛДАМ ҚЫЗМЕТТЕР"
    },
    "Instant Money Transfer": {
        "en": "Instant Money Transfer",
        "ru": "Мгновенный перевод денег",
        "kk": "Лездік ақша аударымы"
    },
    "Saved Beneficiaries": {
        "en": "Saved Beneficiaries",
        "ru": "Сохраненные получатели",
        "kk": "Сақталған алушылар"
    },
    "Payment Products": {
        "en": "Payment Products",
        "ru": "Платежные продукты",
        "kk": "Төлем өнімдері"
    },
    "RECENT TRANSACTIONS": {
        "en": "RECENT TRANSACTIONS",
        "ru": "ПОСЛЕДНИЕ ТРАНЗАКЦИИ",
        "kk": "СОҢҒЫ ТРАНЗАКЦИЯЛАР"
    },
    "Full History": {
        "en": "Full History",
        "ru": "Вся история",
        "kk": "Толық тарих"
    },
    "Support Tickets": {
        "en": "Support Tickets",
        "ru": "Обращения в поддержку",
        "kk": "Қолдау қызметіне өтініштер"
    },
    "Profile & Settings": {
        "en": "Profile & Settings",
        "ru": "Профиль и настройки",
        "kk": "Профиль және баптаулар"
    },
    "Dashboard | RocketBank": {
        "en": "Dashboard | RocketBank",
        "ru": "Кабинет | RocketBank",
        "kk": "Кабинет | RocketBank"
    },
    "RocketBank client dashboard. View financial balances, multi-currency accounts, and recent transactions.": {
        "en": "RocketBank client dashboard. View financial balances, multi-currency accounts, and recent transactions.",
        "ru": "Личный кабинет RocketBank. Просматривайте финансовые балансы, мультивалютные счета и историю операций.",
        "kk": "RocketBank клиенттік кабинеті. Қаржылық теңгерімді, мультивалюталық шоттарды және соңғы операцияларды қараңыз."
    },
    "Financial Analytics & Goals": {
        "en": "Financial Analytics & Goals",
        "ru": "Финансовая аналитика и цели",
        "kk": "Қаржылық талдау және мақсаттар"
    },
    "Open Term Deposit": {
        "en": "Open Term Deposit",
        "ru": "Открыть срочный депозит",
        "kk": "Мерзімді депозит ашу"
    },
    "Daily capitalization active": {
        "en": "Daily capitalization active",
        "ru": "Ежедневная капитализация активна",
        "kk": "Күнделікті капитализация белсенді"
    },
    "High-yield savings and term deposits with up to 18% annual return, daily capitalization, and state insurance protection up to 20M KZT.": {
        "en": "High-yield savings and term deposits with up to 18% annual return, daily capitalization, and state insurance protection up to 20M KZT.",
        "ru": "Высокодоходные сберегательные и срочные депозиты со ставкой до 18% годовых, ежедневной капитализацией и госгарантией КФГД до 20 млн тенге.",
        "kk": "Жылдық 18%-ға дейінгі мөлшерлемесі, күнделікті капитализациясы және 20 млн теңгеге дейін ҚДКҚ мемлекеттік кепілдігі бар жинақ және мерзімді депозиттер."
    },
    "High-yield savings and term deposits with up to 18%% annual return, daily capitalization, and state insurance protection up to 20M KZT.": {
        "en": "High-yield savings and term deposits with up to 18%% annual return, daily capitalization, and state insurance protection up to 20M KZT.",
        "ru": "Высокодоходные сберегательные и срочные депозиты со ставкой до 18% годовых, ежедневной капитализацией и госгарантией КФГД до 20 млн тенге.",
        "kk": "Жылдық 18%-ға дейінгі мөлшерлемесі, күнделікті капитализациясы және 20 млн теңгеге дейін ҚДКҚ мемлекеттік кепілдігі бар жинақ және мерзімді депозиттер."
    },
    "Maximize your savings with compound daily interest, flexible top-up options, and 100% state deposit guarantee by KDIF.": {
        "en": "Maximize your savings with compound daily interest, flexible top-up options, and 100% state deposit guarantee by KDIF.",
        "ru": "Умножайте сбережения с ежедневным сложным процентом, гибким пополнением и 100% государственной гарантией КФГД.",
        "kk": "Күнделікті күрделі пайызбен, икемді толықтырумен және ҚДКҚ-ның 100% мемлекеттік кепілдігімен жинақтарыңызды көбейтіңіз."
    },
    "Maximize your savings with compound daily interest, flexible top-up options, and 100%% state deposit guarantee by KDIF.": {
        "en": "Maximize your savings with compound daily interest, flexible top-up options, and 100%% state deposit guarantee by KDIF.",
        "ru": "Умножайте сбережения с ежедневным сложным процентом, гибким пополнением и 100% государственной гарантией КФГД.",
        "kk": "Күнделікті күрделі пайызбен, икемді толықтырумен және ҚДКҚ-ның 100% мемлекеттік кепілдігімен жинақтарыңызды көбейтіңіз."
    },
    "Paid automatically on the 1st": {
        "en": "Paid automatically on the 1st",
        "ru": "Выплачивается 1-го числа каждого месяца",
        "kk": "Әр айдың 1-жұлдызында төленеді"
    },
    "Sign In Now": {
        "en": "Sign In Now",
        "ru": "Войти сейчас",
        "kk": "Қазір кіру"
    },
    "Sign In to Portal": {
        "en": "Sign In to Portal",
        "ru": "Вход в личный кабинет",
        "kk": "Порталға кіру"
    },
    "Sign In | RocketBank": {
        "en": "Sign In | RocketBank",
        "ru": "Вход | RocketBank",
        "kk": "Кіру | RocketBank"
    },
    "Sign in here": {
        "en": "Sign in here",
        "ru": "Войдите здесь",
        "kk": "Осында кіріңіз"
    },
    "Sign in securely to your RocketBank account to manage cards, accounts, and payments.": {
        "en": "Sign in securely to your RocketBank account to manage cards, accounts, and payments.",
        "ru": "Безопасный вход в аккаунт RocketBank для управления картами, счетами и платежами.",
        "kk": "Карталарды, шоттарды және төлемдерді басқару үшін RocketBank аккаунтына қауіпсіз кіріңіз."
    },
    "Create My Account": {
        "en": "Create My Account",
        "ru": "Создать аккаунт",
        "kk": "Аккаунт ашу"
    },
    "Don't have a RocketBank account?": {
        "en": "Don't have a RocketBank account?",
        "ru": "Еще нет счета в RocketBank?",
        "kk": "RocketBank-те әлі шотыңыз жоқ па?"
    },
    "Register for RocketBank and gain access to multi-currency IBAN accounts, cashback debit cards, and instant transfers.": {
        "en": "Register for RocketBank and gain access to multi-currency IBAN accounts, cashback debit cards, and instant transfers.",
        "ru": "Зарегистрируйтесь в RocketBank и получите доступ к мультивалютным счетам IBAN, дебетовым картам с кэшбэком и мгновенным переводам.",
        "kk": "RocketBank-ке тіркеліп, мультивалюталық IBAN шоттарына, кэшбэгі бар дебеттік карталарға және лездік аударымдарға қол жеткізіңіз."
    },
    "Email or Username": {
        "en": "Email or Username",
        "ru": "Email или имя пользователя",
        "kk": "Email немесе логин"
    },
    "Username": {
        "en": "Username",
        "ru": "Имя пользователя",
        "kk": "Пайдаланушы аты"
    },
    "Phone Number": {
        "en": "Phone Number",
        "ru": "Номер телефона",
        "kk": "Телефон нөмірі"
    },
    "Security Password": {
        "en": "Security Password",
        "ru": "Пароль безопасности",
        "kk": "Қауіпсіздік құпиясөзі"
    },
    "New Password": {
        "en": "New Password",
        "ru": "Новый пароль",
        "kk": "Жаңа құпиясөз"
    },
    "Confirm New Password": {
        "en": "Confirm New Password",
        "ru": "Подтвердите новый пароль",
        "kk": "Жаңа құпиясөзді растаңыз"
    },
    "Change Password": {
        "en": "Change Password",
        "ru": "Изменить пароль",
        "kk": "Құпиясөзді өзгерту"
    },
    "Password Changed Successfully!": {
        "en": "Password Changed Successfully!",
        "ru": "Пароль успешно изменен!",
        "kk": "Құпиясөз сәтті өзгертілді!"
    },
    "Password Changed | RocketBank": {
        "en": "Password Changed | RocketBank",
        "ru": "Пароль изменен | RocketBank",
        "kk": "Құпиясөз өзгертілді | RocketBank"
    },
    "Forgot Your Password?": {
        "en": "Forgot Your Password?",
        "ru": "Забыли пароль?",
        "kk": "Құпиясөзді ұмыттыңыз ба?"
    },
    "Reset Password | RocketBank": {
        "en": "Reset Password | RocketBank",
        "ru": "Восстановление пароля | RocketBank",
        "kk": "Құпиясөзді қалпына келтіру | RocketBank"
    },
    "Reset Link Sent | RocketBank": {
        "en": "Reset Link Sent | RocketBank",
        "ru": "Ссылка для сброса отправлена | RocketBank",
        "kk": "Сілтеме жіберілді | RocketBank"
    },
    "Password Reset Link Expired": {
        "en": "Password Reset Link Expired",
        "ru": "Срок действия ссылки истек",
        "kk": "Сілтеменің мерзімі аяқталды"
    },
    "Request a New Link": {
        "en": "Request a New Link",
        "ru": "Запросить новую ссылку",
        "kk": "Жаңа сілтеме сұрау"
    },
    "Return to Sign In": {
        "en": "Return to Sign In",
        "ru": "Вернуться ко входу",
        "kk": "Кіруге оралу"
    },
    "name@example.com": {
        "en": "name@example.com",
        "ru": "name@example.com",
        "kk": "name@example.com"
    },
    "name@company.com or username": {
        "en": "name@company.com or username",
        "ru": "name@company.com или логин",
        "kk": "name@company.com немесе логин"
    },
    "username": {
        "en": "username",
        "ru": "логин",
        "kk": "логин"
    },
    "Modern Digital Banking": {
        "en": "Modern Digital Banking",
        "ru": "Современный цифровой банкинг",
        "kk": "Заманауи цифрлық банкинг"
    },
    "Experience effortless banking with high-yield deposits, zero-fee multi-currency transfers, and modern security.": {
        "en": "Experience effortless banking with high-yield deposits, zero-fee multi-currency transfers, and modern security.",
        "ru": "Ощутите легкость банкинга с высокодоходными депозитами, бесплатными мультивалютными переводами и современной защитой.",
        "kk": "Жоғары кірісті депозиттер, комиссиясыз мультивалюталық аударымдар және сенімді қорғаныспен банктік қызметтің жеңілдігін сезініңіз."
    },
    "Security & Guarantee": {
        "en": "Security & Guarantee",
        "ru": "Безопасность и гарантии",
        "kk": "Қауіпсіздік және кепілдіктер"
    },
    "Terms": {
        "en": "Terms",
        "ru": "Условия",
        "kk": "Шарттар"
    },
    "Privacy": {
        "en": "Privacy",
        "ru": "Конфиденциальность",
        "kk": "Құпиялылық"
    },
    "Adapted from": {
        "en": "Adapted from",
        "ru": "Адаптировано на основе",
        "kk": "Негізінде бейімделген"
    },
    "Welcome": {
        "en": "Welcome",
        "ru": "Добро пожаловать",
        "kk": "Қош келдіңіз"
    },
    "Details": {
        "en": "Details",
        "ru": "Детали",
        "kk": "Толық мәлімет"
    },
    "Date": {
        "en": "Date",
        "ru": "Дата",
        "kk": "Күні"
    },
    "Type": {
        "en": "Type",
        "ru": "Тип",
        "kk": "Түрі"
    },
    "View All": {
        "en": "View All",
        "ru": "Посмотреть все",
        "kk": "Барлығын көру"
    },
    "Multi-currency enabled": {
        "en": "Multi-currency enabled",
        "ru": "Мультивалюта включена",
        "kk": "Мультивалюта қосылған"
    },
    "Rating must be between 1 and 5. Got %(value)s.": {
        "en": "Rating must be between 1 and 5. Got %(value)s.",
        "ru": "Оценка должна быть от 1 до 5. Получено: %(value)s.",
        "kk": "Бағалау 1 мен 5 аралығында болуы керек. Берілгені: %(value)s."
    },
    "Image file size cannot exceed %(max)s MB. Got %(actual).1f MB.": {
        "en": "Image file size cannot exceed %(max)s MB. Got %(actual).1f MB.",
        "ru": "Размер изображения не должен превышать %(max)s МБ. Текущий размер: %(actual).1f МБ.",
        "kk": "Сурет файлының өлшемі %(max)s МБ-тан аспауы керек. Қазіргі өлшемі: %(actual).1f МБ."
    },
    "24/7 Client Relations": {
        "en": "24/7 Client Relations",
        "ru": "Клиентский сервис 24/7",
        "kk": "Клиенттерге тәулік бойы қызмет көрсету"
    },
    "24/7 Priority Emergency Line": {
        "en": "24/7 Priority Emergency Line",
        "ru": "Приоритетная линия экстренной связи 24/7",
        "kk": "Тәулік бойы шұғыл байланыс желісі"
    },
    "Al-Farabi Avenue 77/7, Bostandyk District": {
        "en": "Al-Farabi Avenue 77/7, Bostandyk District",
        "ru": "Проспект Аль-Фараби 77/7, Бостандыкский район",
        "kk": "Әл-Фараби даңғылы 77/7, Бостандық ауданы"
    },
    "Account": {
        "en": "Account",
        "ru": "Счет",
        "kk": "Шот"
    },
    "Actions": {
        "en": "Actions",
        "ru": "Действия",
        "kk": "Әрекеттер"
    },
    "Active Accounts": {
        "en": "Active Accounts",
        "ru": "Активные счета",
        "kk": "Белсенді шоттар"
    },
    "All Categories": {
        "en": "All Categories",
        "ru": "Все категории",
        "kk": "Барлық санаттар"
    },
    "All Statuses": {
        "en": "All Statuses",
        "ru": "Все статусы",
        "kk": "Барлық мәртебелер"
    },
    "IBAN": {
        "en": "IBAN",
        "ru": "IBAN",
        "kk": "IBAN"
    },
    "Sarah Kim": {
        "en": "Sarah Kim",
        "ru": "Сара Ким",
        "kk": "Сара Ким"
    },
    "James Adler": {
        "en": "James Adler",
        "ru": "Джеймс Адлер",
        "kk": "Джеймс Адлер"
    },
    "Priya Mehta": {
        "en": "Priya Mehta",
        "ru": "Прия Мехта",
        "kk": "Прия Мехта"
    },
    "Tom Brennan": {
        "en": "Tom Brennan",
        "ru": "Том Бреннан",
        "kk": "Том Бреннан"
    },
    "Liu Wei": {
        "en": "Liu Wei",
        "ru": "Лю Вэй",
        "kk": "Лю Вэй"
    },
    "Amara Osei": {
        "en": "Amara Osei",
        "ru": "Амара Осей",
        "kk": "Амара Осей"
    }
}


def t(key, lang=None):
    """
    Returns translated text for `key` in `lang` (defaults to active django language).
    Falls back to non-empty translation: requested lang -> Russian -> English original -> key.
    NEVER returns empty string when key is non-empty.
    """
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
    """
    Template-friendly wrapper allowing {{ tr.Cards }} or {{ tr["About RocketBank"] }}.
    Always resolves using the currently active request language and never returns empty strings.
    """

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
