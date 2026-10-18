"""
Script to populate and update all PO translation catalogs (RU, KK, EN) with complete,
high-quality translations, and compile them to MO files.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from scripts.compile_mo import compile_all  # noqa: E402

# Complete Trilingual Translation Catalog: English msgid -> (Russian msgstr, Kazakh msgstr)
TRANSLATIONS = {
    # ── Navbar, Header & General ──
    "Home": ("Главная", "Басты бет"),
    "Cards": ("Карты", "Карталар"),
    "Loans": ("Кредиты", "Несиелер"),
    "Deposits": ("Депозиты", "Депозиттер"),
    "About": ("О банке", "Банк туралы"),
    "FAQ": ("FAQ", "FAQ"),
    "Contacts": ("Контакты", "Байланыс"),
    "Sign in": ("Войти", "Кіру"),
    "Get started": ("Открыть счёт", "Шот ашу"),
    "Get started free": ("Открыть счёт", "Шот ашу"),
    "Dashboard": ("Кабинет", "Кабинет"),
    "Log out": ("Выйти", "Шығу"),
    "Sign out": ("Выйти", "Шығу"),
    "Profile": ("Профиль", "Профиль"),
    "Notifications": ("Уведомления", "Хабарламалар"),
    "Client Portal": ("Личный кабинет", "Клиенттік кабинет"),
    "Live": ("Онлайн", "Тікелей"),
    "Toggle theme": ("Сменить тему", "Тақырыпты ауыстыру"),
    "Toggle dark/light theme": ("Переключить темную/светлую тему", "Күңгірт/жарық тақырыпты ауыстыру"),
    "Skip to main content": ("Перейти к основному содержимому", "Негізгі мазмұнға өту"),
    "Close menu": ("Закрыть меню", "Мәзірді жабу"),
    "Open menu": ("Открыть меню", "Мәзірді ашу"),
    "Dashboard navigation": ("Навигация панели", "Панель навигациясы"),
    "Dashboard sections": ("Разделы панели", "Панель бөлімдері"),
    "Enterprise Digital Banking": ("Цифровой банкинг для бизнеса и частных лиц", "Бизнес пен жеке тұлғаларға арналған цифрлық банкинг"),
    "Accounts": ("Счета", "Шоттар"),
    "Transfer Money": ("Перевести деньги", "Ақша аудару"),
    "Transactions": ("Транзакции", "Транзакциялар"),
    "My Cards": ("Мои карты", "Менің карталарым"),
    "Order Card (Wizard)": ("Заказ карты (Мастер)", "Картаға тапсырыс беру"),
    "Loans & Credit": ("Кредиты и займы", "Несиелер мен қарыздар"),
    "Term Deposits": ("Срочные депозиты", "Мерзімді депозиттер"),
    "Analytics & Goals": ("Аналитика и цели", "Талдау және мақсаттар"),
    "Support & Tickets": ("Поддержка и тикеты", "Қолдау қызметі"),
    "Security Settings": ("Настройки безопасности", "Қауіпсіздік баптаулары"),
    "Current Session": ("Текущая сессия", "Ағымдағы сессия"),
    "unread notifications": ("непрочитанных уведомлений", "оқылмаған хабарламалар"),
    "View notifications": ("Посмотреть уведомления", "Хабарламаларды көру"),
    "User profile avatar": ("Аватар профиля", "Профиль аватары"),

    # ── Footer ──
    "Products": ("Продукты", "Өнімдер"),
    "Debit & Credit Cards": ("Дебетовые и кредитные карты", "Дебеттік және несиелік карталар"),
    "Consumer & Auto Loans": ("Потребительские и автокредиты", "Тұтынушылық және автонесиелер"),
    "Fixed-Term Deposits": ("Срочные депозиты", "Мерзімді депозиттер"),
    "Loan Calculator": ("Кредитный калькулятор", "Несие калькуляторы"),
    "Company": ("О компании", "Компания туралы"),
    "About RocketBank": ("О RocketBank", "RocketBank туралы"),
    "Help Center & FAQ": ("Центр помощи и FAQ", "Көмек орталығы және FAQ"),
    "Contacts & Headquarters": ("Контакты и штаб-квартира", "Байланыс және бас кеңсе"),
    "System Health Status": ("Статус работы сервисов", "Жүйенің жұмыс күйі"),
    "Legal & Security": ("Безопасность и право", "Құқықтық ақпарат және қауіпсіздік"),
    "Terms of Service": ("Условия обслуживания", "Қызмет көрсету шарттары"),
    "Privacy Policy": ("Политика конфиденциальности", "Құпиялылық саясаты"),
    "Security Standards": ("Стандарты безопасности", "Қауіпсіздік стандарттары"),
    "Regulatory Disclosures": ("Раскрытие информации", "Ақпаратты ашу"),
    "Next-generation digital banking platform empowering clients worldwide with real-time payments, smart cards, high-yield deposits, and enterprise security.": (
        "Цифровая банковская платформа нового поколения: мгновенные платежи, умные карты, доходные депозиты и корпоративный уровень безопасности.",
        "Жаңа буын цифрлық банк платформасы: лездік төлемдер, смарт карталар, жоғары кірісті депозиттер және сенімді қауіпсіздік."
    ),
    "Regulated by the Agency for Regulation and Development of the Financial Market.": (
        "Регулируется Агентством Республики Казахстан по регулированию и развитию финансового рынка.",
        "Қазақстан Республикасының Қаржы нарығын реттеу және дамыту агенттігімен реттеледі."
    ),
    "Deposits insured up to 20,000,000 KZT by the Kazakhstan Deposit Insurance Fund (KDIF).": (
        "Вклады застрахованы Казахстанским фондом гарантирования депозитов (КФГД) на сумму до 20 000 000 тенге.",
        "Салымдар Қазақстанның депозиттерге кепілдік беру қорымен (ҚДКБҚ) 20 000 000 теңгеге дейін сақтандырылған."
    ),
    "256-bit AES banking encryption & SOC 2 Type II certified infrastructure.": (
        "256-битное шифрование AES банковского уровня и инфраструктура, сертифицированная по стандарту SOC 2 Type II.",
        "256-биттік AES банктік шифрлауы және SOC 2 Type II сертификатталған инфрақұрылымы."
    ),
    "Licensed by the Agency for Regulation and Development of the Financial Market. All rights reserved.": (
        "Лицензия Агентства Республики Казахстан по регулированию и развитию финансового рынка. Все права защищены.",
        "Қазақстан Республикасының Қаржы нарығын реттеу және дамыту агенттігінің лицензиясы. Барлық құқықтар қорғалған."
    ),

    # ── Home Landing Page ──
    "Modern Digital Financial Platform": ("Современная цифровая финансовая платформа", "Заманауи цифрлық қаржылық платформа"),
    "RocketBank is the modern financial platform engineered for speed. Real-time payments, intelligent analytics, enterprise-grade security, and zero-commission multi-currency accounts.": (
        "RocketBank — современная финансовая платформа, созданная для скорости: расчеты в реальном времени, интеллектуальная аналитика, надежная безопасность и мультивалютные счета без комиссий.",
        "RocketBank — жылдамдық үшін жасалған заманауи қаржылық платформа: нақты уақыттағы төлемдер, интеллектуалды талдау, сенімді қауіпсіздік және комиссиясыз көпвалюталық шоттар."
    ),
    "Now with AI-powered financial insights": ("Теперь с финансовой аналитикой на базе ИИ", "Енді ЖИ негізіндегі қаржылық талдаумен"),
    "Finance that": ("Финансы, которые", "Сіздің"),
    "moves at": ("движутся со скоростью", "жылдамдығыңыздағы"),
    "your speed": ("ваших решений", "қаржылық жүйе"),
    "RocketBank is the modern financial platform built for businesses and individuals who refuse to wait. Real-time payments, intelligent analytics, and enterprise-grade security — all in one dashboard.": (
        "RocketBank — современная финансовая платформа для бизнеса и частных лиц, ценящих время. Мгновенные платежи, умная аналитика и безопасность корпоративного уровня — в едином интерфейсе.",
        "RocketBank — уақытын бағалайтын бизнес пен жеке тұлғаларға арналған заманауи қаржылық платформа. Бірыңғай интерфейстегі лездік төлемдер, ақылды аналитика және сенімді қауіпсіздік."
    ),
    "Start for free": ("Начать бесплатно", "Тегін бастау"),
    "Explore Products": ("Посмотреть продукты", "Өнімдерді көру"),
    "Open Client Dashboard": ("Перейти в кабинет", "Кабинетке өту"),
    "Trusted by modern teams & financial institutions": ("Нам доверяют технологичные компании и финансовые институты", "Бізге заманауи компаниялар мен қаржы институттары сенеді"),
    "Daily Transaction Volume": ("Дневной объем транзакций", "Күндік транзакция көлемі"),
    "Financial License Protection": ("Защита государственной лицензией", "Мемлекеттік лицензиямен қорғалған"),
    "Real-Time Ledger Latency": ("Задержка финансового реестра", "Қаржылық тізілім кідірісі"),
    "Continuous System Uptime": ("Бесперебойная доступность", "Үздіксіз қолжетімділік"),
    "Everything You Need": ("Всё необходимое для финансов", "Қаржыға қажеттінің барлығы"),
    "A Complete Suite for Personal & Business Capital": ("Полный набор решений для частного и корпоративного капитала", "Жеке және корпоративтік капиталға арналған толық шешімдер кешені"),
    "Instant Settlement Rails": ("Мгновенные финансовые рельсы", "Лездік қаржылық есеп айырысу"),
    "Move money in real-time across domestic and international banking rails with sub-second atomic settlement and zero hidden commissions.": (
        "Переводите средства в реальном времени по внутренним и международным банковским каналам с атомарным расчетом быстрее секунды и без скрытых комиссий.",
        "Ішкі және халықаралық банктік бағыттар бойынша қаражатты жасырын комиссиясыз, секундына жетпейтін атомарлық есеп айырысумен аударыңыз."
    ),
    "Predictive Intelligence": ("Предиктивная аналитика", "Болжамдық аналитика"),
    "AI-powered dashboards that surface what matters. Cashflow forecasting, automated anomaly detection, and real-time expense classification.": (
        "Интеллектуальные панели управления: прогнозирование денежных потоков, автоматическое выявление аномалий и классификация расходов в реальном времени.",
        "Маңыздыны көрсететін интеллектуалды панельдер: ақша ағындарын болжау, аномалияларды автоматты анықтау және шығыстарды жіктеу."
    ),
    "Multi-Currency Treasury": ("Мультивалютное казначейство", "Көпвалюталық қазынашылық"),
    "Hold, convert, and pay in KZT, USD, EUR, GBP, and 30+ currencies at interbank rates. Lock live rates and eliminate foreign exchange loss.": (
        "Храните, конвертируйте и оплачивайте в KZT, USD, EUR, GBP и еще более 30 валютах по межбанковскому курсу. Фиксируйте курсы без потерь на конвертации.",
        "KZT, USD, EUR, GBP және 30-дан астам валютада банкаралық бағам бойынша сақтаңыз, айырбастаңыз және төлеңіз."
    ),
    "Zero-Trust Architecture": ("Архитектура Zero-Trust", "Zero-Trust қауіпсіздік архитектурасы"),
    "Bank-grade encryption, SOC 2 compliance, KDIF state deposit guarantee up to 20,000,000 KZT, and instant 1-click card freeze.": (
        "Банковское шифрование, соответствие SOC 2, государственная гарантия КФГД до 20 000 000 тенге и мгновенная заморозка карты в 1 клик.",
        "Банктік шифрлау, SOC 2 сәйкестігі, ҚДКБҚ 20 000 000 теңгеге дейінгі мемлекеттік кепілдігі және картаны 1 басумен лезде бұғаттау."
    ),
    "Real-Time Overview": ("Обзор в реальном времени", "Нақты уақыттағы шолу"),
    "Built for Speed, Control & Clarity": ("Создано для скорости, контроля и прозрачности", "Жылдамдық, бақылау және ашықтық үшін жасалған"),
    "Real-time liquidity, multi-currency balances, and full control over cards and transfers.": (
        "Мгновенная ликвидность, мультивалютные балансы и полный контроль над картами и переводами.",
        "Лездік өтімділік, көпвалюталық теңгерімдер және карталар мен аударымдарды толық бақылау."
    ),
    "Open Free Account": ("Открыть бесплатный счет", "Тегін шот ашу"),
    "View Analytics": ("Перейти к аналитике", "Аналитиканы қарау"),
    "Transparent Pricing": ("Прозрачные тарифы", "Ашық тарифтер"),
    "Card Tiers Engineered for You": ("Уровни карт, созданные под ваши задачи", "Сіздің мақсаттарыңызға арналған карталар"),
    "Start with zero maintenance, unlock high-yield privileges and priority concierge.": (
        "Начните с бесплатного обслуживания, открывайте премиальные привилегии и персональный консьерж-сервис.",
        "Тегін қызмет көрсетуден бастаңыз, артықшылықтар мен жеке консьерж-сервисті пайдаланыңыз."
    ),
    "Monthly billing": ("Ежемесячно", "Ай сайын"),
    "Annual billing": ("Ежегодно", "Жыл сайын"),
    "Save 20%": ("Скидка 20%", "20% жеңілдік"),
    "Institutional Security": ("Институциональная безопасность", "Институционалдық қауіпсіздік"),
    "Security is not a feature — it's the foundation": ("Безопасность — это не опция, а фундамент", "Қауіпсіздік — бұл басты негіз"),
    "Every transaction is shielded by multiple layers of enterprise-grade cryptographic security. We are audited, regulated, and monitored around the clock.": (
        "Каждая операция защищена многоуровневым криптографическим шифрованием. Система круглосуточно проверяется и контролируется регуляторами.",
        "Әрбір операция көпдеңгейлі криптографиялық қорғаныспен қорғалған. Жүйе тәулік бойы реттеушілердің қадағалауында."
    ),
    "KDIF Insured": ("Гарантия КФГД", "ҚДКБҚ кепілдігі"),
    "Insured up to 20,000,000 KZT per depositor": ("Страхование до 20 000 000 тенге на вкладчика", "Әр салымшыға 20 000 000 теңгеге дейін кепілдендірілген"),
    "PCI DSS Level 1": ("Сертификат PCI DSS Level 1", "PCI DSS Level 1 сертификаты"),
    "Highest tier of international payment card security": ("Высший международный стандарт защиты платежных карт", "Төлем карталарын қорғаудың халықаралық жоғары стандарты"),
    "ISO 27001": ("Стандарт ISO 27001", "ISO 27001 стандарты"),
    "Global standard for information security management": ("Мировой стандарт управления информационной безопасностью", "Ақпараттық қауіпсіздікті басқарудың жаһандық стандарты"),
    "AI Fraud Shield": ("ИИ-защита от мошенничества", "Алаяқтықтан қорғайтын ЖИ"),
    "Blocks 99.98% of fraudulent attempts in sub-seconds": ("Блокирует 99.98% попыток мошенничества за доли секунды", "Алаяқтық әрекеттердің 99.98%-ын лезде бұғаттайды"),
    "RocketBank Mobile Experience": ("Мобильное приложение RocketBank", "RocketBank мобильді қосымшасы"),
    "Full dashboard access, biometric approval for high-value transfers, and instant transaction push notifications — anywhere in the world.": (
        "Полный доступ к счетам, биометрическое подтверждение крупных переводов и мгновенные пуш-уведомления в любой точке мира.",
        "Шоттарға толық қолжетімділік, ірі аударымдарды биометриялық растау және әлемнің кез келген жерінде лездік хабарламалар."
    ),
    "Available for iOS & Android": ("Доступно для iOS и Android", "iOS және Android үшін қолжетімді"),
    "Common Questions": ("Частые вопросы", "Жиі қойылатын сұрақтар"),
    "Everything You Need to Know": ("Все, что вам нужно знать о банке", "Банк туралы білуіңіз керек барлық ақпарат"),

    # ── About RocketBank Page ──
    "About RocketBank — Architecture & Leadership": ("О RocketBank — Архитектура и руководство", "RocketBank туралы — Архитектура және басшылық"),
    "Corporate Overview": ("Корпоративный обзор", "Корпоративтік шолу"),
    "Engineered to redefine digital finance through real-time distributed architecture, strict ACID atomicity, and uncompromising human-centric design.": (
        "Создан для трансформации цифровых финансов благодаря распределенной архитектуре реального времени, строгой атомарности ACID и бескомпромиссному дизайну.",
        "Нақты уақыттағы үлестірілген архитектура, ACID атомарлығы және клиентке бағдарланған дизайн арқылы қаржы саласын жаңғырту үшін құрылған."
    ),
    "Engineering Architecture": ("Инженерная архитектура", "Инженерлік архитектура"),
    "High-Concurrency Real-Time Infrastructure": ("Высоконагруженная инфраструктура реального времени", "Жоғары жүктемелі нақты уақыттағы инфрақұрылым"),
    "RocketBank is architected on a high-availability Django core coupled with PostgreSQL transactional persistence, Celery asynchronous pipelines, and Redis low-latency caching.": (
        "RocketBank построен на высоконадежном ядре Django в связке с транзакционным хранилищем PostgreSQL, асинхронными очередями Celery и быстрой памятью Redis.",
        "RocketBank жоғары сенімді Django өзегінде, PostgreSQL транзакциялық базасымен, Celery асинхронды кезегімен және жылдам Redis кэшімен жасалған."
    ),
    "Our financial ledger guarantees full ACID atomicity with row-level locks (select_for_update) to prevent race conditions during peak transaction spikes, processing sub-second multi-currency transfers across domestic and international banking rails.": (
        "Наш финансовый реестр гарантирует полную атомарность ACID с блокировками на уровне строк (select_for_update) для исключения состояния гонки при пиковых нагрузках, обрабатывая мультивалютные переводы быстрее секунды.",
        "Біздің қаржылық тізілім жоғары жүктеме кезінде қателіктерді болдырмау үшін жолдар деңгейіндегі құлыптаумен (select_for_update) толық ACID атомарлығына кепілдік береді."
    ),
    "Ledger Latency": ("Задержка реестра", "Тізілім кідірісі"),
    "Platform Uptime": ("Доступность платформы", "Платформа қолжетімділігі"),
    "Operational": ("Работает стабильно", "Тұрақты жұмыс істейді"),
    "Regulatory Licensing & Protection": ("Лицензирование и государственная защита", "Лицензиялау және мемлекеттік қорғаныс"),
    "Licensed by the ARDFM of Kazakhstan. Deposits insured up to 20,000,000 KZT by the KDIF.": (
        "Лицензировано АРРФР Казахстана. Депозиты застрахованы КФГД на сумму до 20 000 000 тенге.",
        "Қазақстанның ҚНРДА тарапынан лицензияланған. Депозиттерге ҚДКБҚ тарапынан 20 000 000 теңгеге дейін кепілдік берілген."
    ),
    "Sub-second Atomic Payments": ("Атомарные платежи быстрее секунды", "Секундына жетпейтін атомарлық төлемдер"),
    "Indexed IBAN routing and precomputed aggregation algorithms enable instant domestic and international clearance.": (
        "Индексированная маршрутизация IBAN и алгоритмы предварительной агрегации обеспечивают мгновенный клиринг внутри страны и за рубежом.",
        "Индекстелген IBAN бағыттауы және алдын ала есептелген алгоритмдер лездік клирингті қамтамасыз етеді."
    ),
    "Zero-Trust Security Perimeter": ("Периметр безопасности Zero-Trust", "Zero-Trust қауіпсіздік шеңбері"),
    "256-bit AES encryption at rest and in transit, PBKDF2 credential hashing, and AI-driven fraud anomaly detection.": (
        "256-битное шифрование AES при хранении и передаче данных, хэширование паролей PBKDF2 и выявление аномалий с помощью ИИ.",
        "Деректерді сақтау және тасымалдаудағы 256-биттік AES шифрлауы, PBKDF2 хэштеуі және алаяқтықты анықтауға арналған ЖИ."
    ),
    "Governance": ("Корпоративное управление", "Басқару"),
    "Leadership & Architecture": ("Руководство и архитектура", "Басшылық және архитектура"),
    "Ayan": ("Аян", "Аян"),
    "Founder & CEO • Chief System Architect": ("Основатель и CEO • Главный системный архитектор", "Негізін қалаушы және CEO • Бас жүйелік архитектор"),
    "Executive Direction": ("Видение руководства", "Басшылықтың көзқарасы"),
    "We architected RocketBank from the ground up on modern, open principles: elimination of opaque banking bureaucracy, execution speed measured in milliseconds, and rock-solid cryptographic security. Every component is designed to give individuals and businesses complete, effortless command over their financial destiny.": (
        "Мы создали RocketBank с нуля на современных принципах: устранение непрозрачной бюрократии, скорость операций за миллисекунды и несокрушимая криптографическая безопасность. Каждый элемент спроектирован так, чтобы дать частным лицам и бизнесу легкий и полный контроль над своим капиталом.",
        "Біз RocketBank-ті басынан бастап заманауи қағидаттар бойынша құрдық: бюрократияны жою, миллисекундтық жылдамдық және мықты криптографиялық қауіпсіздік. Әрбір құрамдас бөлік клиенттерге өз қаражатын оңай әрі толық басқаруға мүмкіндік беру үшін жасалған."
    ),
    "Global Presence": ("Штаб-квартира", "Бас кеңсе"),
    "Headquarters & Operations": ("Главный офис и управление", "Бас кеңсе және операциялық орталық"),
    "Located in the heart of Almaty's premier financial and technology corridor.": (
        "Расположен в главном финансовом и технологическом деловом центре Алматы.",
        "Алматы қаласының басты қаржылық және технологиялық орталығында орналасқан."
    ),
    "RocketBank Headquarters": ("Штаб-квартира RocketBank", "RocketBank бас кеңсесі"),
    "Esentai Tower, Al-Farabi Avenue 77/7, Almaty Financial District, Republic of Kazakhstan, 050040.": (
        "Esentai Tower, проспект Аль-Фараби 77/7, Финансовый район Алматы, Республика Казахстан, 050040.",
        "Esentai Tower, Әл-Фараби даңғылы 77/7, Алматы қ., Қазақстан Республикасы, 050040."
    ),
    "Interactive Location Map": ("Интерактивная карта", "Интерактивті карта"),
    "Central operations, engineering labs, and client relations center. Open Mon–Fri, 09:00–18:00 (UTC+5).": (
        "Операционный центр, лаборатории разработки и центр обслуживания клиентов. Пн–Пт, 09:00–18:00 (UTC+5).",
        "Операциялық орталық, әзірлеу зертханалары және клиенттерге қызмет көрсету бөлімі. Дүйсенбі–Жұма, 09:00–18:00 (UTC+5)."
    ),

    # ── Internal Dashboard, Accounts, Cards, Transfers ──
    "Financial Portfolio": ("Финансовый портфель", "Қаржылық портфель"),
    "Here is your real-time financial portfolio overview for today": (
        "Обзор вашего финансового портфеля в реальном времени на сегодня",
        "Бүгінгі күнгі нақты уақыттағы қаржылық портфеліңіздің шолуы"
    ),
    "Total Net Liquidity": ("Общая чистая ликвидность", "Жалпы таза өтімділік"),
    "Estimated across all accounts": ("Оценка по всем вашим счетам", "Барлық шоттар бойынша бағалау"),
    "Active Accounts Total": ("Всего активных счетов", "Белсенді шоттар саны"),
    "Checking & Savings": ("Текущие и сберегательные", "Ағымдағы және жинақ"),
    "Active Plastic & Virtual": ("Активные пластиковые и виртуальные", "Белсенді пластикалық және виртуалды"),
    "Active Loans Balance": ("Остаток по кредитам", "Несиелер бойынша қалдық"),
    "Pending repayment": ("К погашению", "Өтеуге жатады"),
    "Quick Banking Services": ("Быстрые банковские операции", "Жылдам банктік қызметтер"),
    "Send Money": ("Отправить деньги", "Ақша аудару"),
    "Instant IBAN & P2P": ("Мгновенно по IBAN и P2P", "IBAN және P2P бойынша лезде"),
    "Order Card": ("Заказать карту", "Картаға тапсырыс беру"),
    "Take a Loan": ("Оформить кредит", "Несие алу"),
    "Open Deposit": ("Открыть депозит", "Депозит ашу"),
    "Recent Transactions": ("Последние транзакции", "Соңғы транзакциялар"),
    "View Full History": ("Вся история", "Толық тарих"),
    "My Bank Accounts": ("Мои банковские счета", "Менің банктік шоттарым"),
    "Bank Accounts": ("Банковские счета", "Банктік шоттар"),
    "Manage all your checking, savings, business, and deposit IBAN accounts": (
        "Управляйте всеми текущими, сберегательными и депозитными счетами IBAN",
        "Барлық ағымдағы, жинақ және депозиттік IBAN шоттарыңызды басқарыңыз"
    ),
    "Open New Account": ("Открыть новый счет", "Жаңа шот ашу"),
    "Search by IBAN...": ("Поиск по IBAN...", "IBAN бойынша іздеу..."),
    "Filter by account type": ("Фильтр по типу счета", "Шот түрі бойынша сүзу"),
    "All Account Types": ("Все типы счетов", "Шоттардың барлық түрлері"),
    "Checking": ("Текущий", "Ағымдағы"),
    "Savings": ("Сберегательный", "Жинақ"),
    "Filter": ("Применить", "Сүзу"),
    "Reset": ("Сбросить", "Қалпына келтіру"),
    "Send instant, zero-commission payments to any RocketBank account": (
        "Мгновенные переводы без комиссий на любые счета RocketBank",
        "Кез келген RocketBank шоттарына комиссиясыз лездік аударымдар"
    ),
    "Confirm & Send Transfer": ("Подтвердить и перевести", "Растау және аудару"),
    "Cancel": ("Отмена", "Бас тарту"),
    "Transaction History": ("История транзакций", "Транзакциялар тарихы"),
    "New Transfer": ("Новый перевод", "Жаңа аударым"),

    # ── Auth Screens ──
    "Sign In to RocketBank": ("Вход в RocketBank", "RocketBank-ке кіру"),
    "Enter your credentials to access your digital command center": (
        "Введите ваши учетные данные для доступа к личному кабинету",
        "Жеке кабинетке кіру үшін деректеріңізді енгізіңіз"
    ),
    "Remember this device for 30 days": ("Запомнить это устройство на 30 дней", "Бұл құрылғыны 30 күнге сақтау"),
    "Forgot password?": ("Забыли пароль?", "Құпиясөзді ұмыттыңыз ба?"),
    "Don't have an account?": ("Еще нет аккаунта?", "Әлі тіркелмедіңіз бе?"),
    "Create Free Account": ("Зарегистрироваться бесплатно", "Тегін тіркелу"),
    "Create Your RocketBank Account": ("Регистрация в RocketBank", "RocketBank-те тіркелу"),
    "Join next-generation banking with zero monthly maintenance fee": (
        "Откройте счет в банке нового поколения с бесплатным обслуживанием",
        "Тегін қызмет көрсететін жаңа буын банкінде шот ашыңыз"
    ),
    "Already have an account?": ("Уже зарегистрированы?", "Бұрыннан тіркелгенсіз бе?"),
    "Reset Your Password": ("Восстановление пароля", "Құпиясөзді қалпына келтіру"),
    "Back to Sign In": ("Вернуться ко входу", "Кіруге оралу"),
}


def escape_str(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n"\n"')


def update_po_file(filepath, lang):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines(keepends=True)
    out_lines = []

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
            continue

        elif line.startswith("msgstr "):
            if current_msgid and current_msgid in TRANSLATIONS:
                ru_val, kk_val = TRANSLATIONS[current_msgid]
                chosen = ru_val if lang == "ru" else (kk_val if lang == "kk" else current_msgid)
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
                if current_msgid and (current_msgid in TRANSLATIONS or lang == "en"):
                    i += 1
                else:
                    out_lines.append(lines[i])
                    i += 1
            current_msgid = ""
            continue

        out_lines.append(line)
        i += 1

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(out_lines)
    print(f"Updated {filepath} for lang={lang}")


def main():
    update_po_file(BASE_DIR / "locale/ru/LC_MESSAGES/django.po", "ru")
    update_po_file(BASE_DIR / "locale/kk/LC_MESSAGES/django.po", "kk")
    update_po_file(BASE_DIR / "locale/en/LC_MESSAGES/django.po", "en")
    compile_all(BASE_DIR)


if __name__ == "__main__":
    main()
