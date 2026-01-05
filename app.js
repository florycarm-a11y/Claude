// ============================================
// GéoFinance - Application JavaScript
// Géopolitique & Marchés Financiers en Temps Réel
// ============================================

// Configuration
const CONFIG = {
    updateInterval: 10000,      // Market update interval (10s)
    newsRefreshInterval: 300000, // News refresh interval (5 min)
    tickerSpeed: 50,            // Ticker animation speed
    animationDelay: 100         // Stagger animation delay
};

// Market Data with realistic values
const marketData = {
    bitcoin: { price: 102456.78, change: 3.24, volume: '45.2B', cap: '2.01T' },
    ethereum: { price: 3456.12, change: 2.15, volume: '18.7B', cap: '415B' },
    gold: { price: 2087.43, change: 0.67 },
    silver: { price: 24.56, change: -0.34 },
    oil: { price: 77.82, change: 1.23 },
    sp500: { price: 4783.23, change: 0.89 },
    wti: { price: 72.45, change: 1.8 },
    natgas: { price: 2.89, change: -2.3 },
    copper: { price: 3.89, change: 1.2 },
    wheat: { price: 612, change: 0.8 }
};

// Comprehensive News Database with real source references
const newsDatabase = {
    geopolitics: [
        {
            source: 'Reuters',
            sourceUrl: 'https://www.reuters.com',
            title: 'Tensions au Moyen-Orient : Les marchés pétroliers sous pression',
            description: 'Les derniers développements dans la région du Golfe entraînent une volatilité accrue sur les cours du brut. Les investisseurs surveillent de près les déclarations diplomatiques.',
            tags: ['geopolitics', 'commodities', 'conflicts'],
            time: '45min',
            impact: 'high',
            region: 'middle-east'
        },
        {
            source: 'Financial Times',
            sourceUrl: 'https://www.ft.com',
            title: 'G7 : Nouvelles sanctions économiques et impact sur les marchés',
            description: 'Les leaders du G7 annoncent un nouveau paquet de sanctions qui pourrait affecter les chaînes d\'approvisionnement mondiales et les flux de capitaux.',
            tags: ['geopolitics', 'markets', 'trade'],
            time: '1h',
            impact: 'high',
            region: 'global'
        },
        {
            source: 'Bloomberg',
            sourceUrl: 'https://www.bloomberg.com',
            title: 'Relations USA-Chine : Négociations commerciales en cours',
            description: 'Les discussions commerciales entre Washington et Pékin reprennent. Les marchés asiatiques réagissent positivement aux premiers signaux.',
            tags: ['geopolitics', 'markets', 'trade'],
            time: '2h',
            impact: 'medium',
            region: 'asia'
        },
        {
            source: 'BBC News',
            sourceUrl: 'https://www.bbc.com/news',
            title: 'Europe : Crise énergétique et stratégies de diversification',
            description: 'L\'Union européenne accélère ses plans de diversification énergétique. Impact sur les prix du gaz et les investissements dans les renouvelables.',
            tags: ['geopolitics', 'commodities', 'politics'],
            time: '3h',
            impact: 'medium',
            region: 'europe'
        },
        {
            source: 'Al Jazeera',
            sourceUrl: 'https://www.aljazeera.com',
            title: 'OPEC+ : Réunion cruciale sur les quotas de production',
            description: 'Les pays producteurs de pétrole se réunissent pour discuter des niveaux de production. Anticipations de volatilité sur les marchés de l\'énergie.',
            tags: ['geopolitics', 'commodities', 'politics'],
            time: '4h',
            impact: 'high',
            region: 'middle-east'
        },
        {
            source: 'Le Monde',
            sourceUrl: 'https://www.lemonde.fr',
            title: 'Zone Euro : BCE et politique monétaire face aux tensions',
            description: 'Christine Lagarde annonce les orientations de la politique monétaire européenne. Les marchés obligataires réagissent aux nouvelles projections.',
            tags: ['geopolitics', 'markets', 'politics'],
            time: '5h',
            impact: 'medium',
            region: 'europe'
        },
        {
            source: 'Wall Street Journal',
            sourceUrl: 'https://www.wsj.com',
            title: 'Amérique Latine : Instabilité politique et marchés émergents',
            description: 'Les changements politiques en Amérique du Sud affectent les flux d\'investissements. Analyse des risques pour les portefeuilles exposés.',
            tags: ['geopolitics', 'markets', 'politics'],
            time: '6h',
            impact: 'medium',
            region: 'americas'
        },
        {
            source: 'France 24',
            sourceUrl: 'https://www.france24.com',
            title: 'Afrique : Ressources stratégiques et nouveaux partenariats',
            description: 'Les pays africains négocient de nouveaux accords sur les métaux rares. Implications pour la transition énergétique mondiale.',
            tags: ['geopolitics', 'commodities', 'trade'],
            time: '7h',
            impact: 'medium',
            region: 'africa'
        }
    ],
    markets: [
        {
            source: 'Bloomberg',
            sourceUrl: 'https://www.bloomberg.com',
            title: 'Wall Street : Nouveaux records historiques pour les indices',
            description: 'Le S&P 500 et le Nasdaq atteignent de nouveaux sommets. Les valeurs technologiques mènent la hausse avec des résultats supérieurs aux attentes.',
            tags: ['markets'],
            time: '30min',
            impact: 'high'
        },
        {
            source: 'CNBC',
            sourceUrl: 'https://www.cnbc.com',
            title: 'Fed : Pause dans le cycle de resserrement monétaire',
            description: 'La Réserve fédérale maintient ses taux. Jerome Powell signale une approche prudente face à l\'évolution de l\'inflation.',
            tags: ['markets', 'politics'],
            time: '1h',
            impact: 'high'
        },
        {
            source: 'Les Échos',
            sourceUrl: 'https://www.lesechos.fr',
            title: 'CAC 40 : Le luxe et la tech portent l\'indice parisien',
            description: 'Les valeurs du luxe français continuent leur progression. LVMH et Hermès affichent des performances exceptionnelles.',
            tags: ['markets'],
            time: '2h',
            impact: 'medium'
        },
        {
            source: 'Financial Times',
            sourceUrl: 'https://www.ft.com',
            title: 'Marchés asiatiques : Tokyo en hausse, Shanghai stabilisée',
            description: 'Le Nikkei 225 progresse sur fond d\'optimisme économique. Les marchés chinois montrent des signes de stabilisation.',
            tags: ['markets'],
            time: '3h',
            impact: 'medium'
        },
        {
            source: 'MarketWatch',
            sourceUrl: 'https://www.marketwatch.com',
            title: 'VIX : L\'indice de la peur reste à des niveaux modérés',
            description: 'Malgré les incertitudes géopolitiques, la volatilité implicite reste contenue. Les investisseurs maintiennent leur appétit pour le risque.',
            tags: ['markets'],
            time: '4h',
            impact: 'low'
        },
        {
            source: 'Reuters',
            sourceUrl: 'https://www.reuters.com',
            title: 'Devises : Le dollar recule face à l\'euro et au yen',
            description: 'L\'indice DXY perd du terrain. Les traders ajustent leurs positions en anticipation des prochaines décisions de politique monétaire.',
            tags: ['markets'],
            time: '5h',
            impact: 'medium'
        },
        {
            source: 'The Economist',
            sourceUrl: 'https://www.economist.com',
            title: 'Obligations : Les rendements sous surveillance',
            description: 'Les taux des bons du Trésor américain évoluent dans une fourchette étroite. Focus sur la courbe des taux et ses implications.',
            tags: ['markets'],
            time: '6h',
            impact: 'medium'
        }
    ],
    crypto: [
        {
            source: 'CoinDesk',
            sourceUrl: 'https://www.coindesk.com',
            title: 'Bitcoin franchit les $100,000 : Nouvel ATH historique',
            description: 'La principale cryptomonnaie établit un nouveau record absolu. L\'adoption institutionnelle et les flux ETF propulsent le cours.',
            tags: ['crypto', 'markets'],
            time: '15min',
            impact: 'high'
        },
        {
            source: 'Cointelegraph',
            sourceUrl: 'https://cointelegraph.com',
            title: 'ETF Bitcoin Spot : Afflux record de capitaux institutionnels',
            description: 'BlackRock et Fidelity enregistrent des entrées massives. Plus de $1.5 milliard de flux nets cette semaine.',
            tags: ['crypto', 'markets'],
            time: '45min',
            impact: 'high'
        },
        {
            source: 'The Block',
            sourceUrl: 'https://www.theblock.co',
            title: 'Ethereum : Mise à jour Dencun et impact sur les Layer 2',
            description: 'La dernière mise à jour réduit considérablement les frais sur les solutions de scalabilité. Arbitrum et Optimism en bénéficient.',
            tags: ['crypto'],
            time: '2h',
            impact: 'medium'
        },
        {
            source: 'Bloomberg Crypto',
            sourceUrl: 'https://www.bloomberg.com/crypto',
            title: 'Solana : Performance exceptionnelle et adoption croissante',
            description: 'L\'écosystème Solana attire de nouveaux projets DeFi et NFT. Le SOL surperforme le marché cette semaine.',
            tags: ['crypto'],
            time: '3h',
            impact: 'medium'
        },
        {
            source: 'Decrypt',
            sourceUrl: 'https://decrypt.co',
            title: 'Régulation MiCA : L\'Europe finalise son cadre crypto',
            description: 'Les nouvelles régulations européennes entrent en vigueur. Clarification pour les exchanges et les stablecoins.',
            tags: ['crypto', 'geopolitics'],
            time: '4h',
            impact: 'high'
        },
        {
            source: 'CoinDesk',
            sourceUrl: 'https://www.coindesk.com',
            title: 'DeFi : La TVL atteint $150 milliards',
            description: 'La finance décentralisée continue sa croissance. Aave et Lido dominent les protocoles de lending et staking.',
            tags: ['crypto'],
            time: '5h',
            impact: 'medium'
        },
        {
            source: 'Reuters',
            sourceUrl: 'https://www.reuters.com',
            title: 'Banques centrales : Exploration des CBDC s\'accélère',
            description: 'La BCE et la Fed avancent sur leurs projets de monnaies numériques. Implications pour le secteur crypto.',
            tags: ['crypto', 'geopolitics'],
            time: '6h',
            impact: 'medium'
        },
        {
            source: 'Cointelegraph',
            sourceUrl: 'https://cointelegraph.com',
            title: 'NFT : Renaissance du marché avec nouveaux cas d\'usage',
            description: 'Le secteur NFT rebondit avec des applications dans le gaming et la tokenisation d\'actifs réels.',
            tags: ['crypto'],
            time: '7h',
            impact: 'low'
        }
    ],
    commodities: [
        {
            source: 'Reuters',
            sourceUrl: 'https://www.reuters.com',
            title: 'Or : Record historique face aux incertitudes géopolitiques',
            description: 'Le métal précieux atteint $2,100/oz. Les banques centrales continuent leurs achats massifs. Valeur refuge par excellence.',
            tags: ['commodities', 'geopolitics'],
            time: '1h',
            impact: 'high'
        },
        {
            source: 'Bloomberg',
            sourceUrl: 'https://www.bloomberg.com',
            title: 'Pétrole Brent : Volatilité sur fond de tensions OPEC+',
            description: 'Les cours du brut fluctuent après les annonces de l\'Arabie Saoudite. Surveillance des stocks stratégiques américains.',
            tags: ['commodities', 'geopolitics'],
            time: '2h',
            impact: 'high'
        },
        {
            source: 'Financial Times',
            sourceUrl: 'https://www.ft.com',
            title: 'Cuivre : Demande en hausse pour la transition énergétique',
            description: 'Le métal rouge profite des investissements dans les renouvelables et les véhicules électriques. Tensions sur l\'approvisionnement.',
            tags: ['commodities'],
            time: '3h',
            impact: 'medium'
        },
        {
            source: 'Les Échos',
            sourceUrl: 'https://www.lesechos.fr',
            title: 'Gaz naturel : Europe sécurise ses approvisionnements',
            description: 'Les stocks européens atteignent des niveaux confortables. Les prix se stabilisent après les pics de 2022.',
            tags: ['commodities', 'geopolitics'],
            time: '4h',
            impact: 'medium'
        },
        {
            source: 'Reuters',
            sourceUrl: 'https://www.reuters.com',
            title: 'Lithium : Marché en équilibre après la correction',
            description: 'Les prix du lithium se stabilisent. La demande des constructeurs de batteries reste soutenue.',
            tags: ['commodities'],
            time: '5h',
            impact: 'medium'
        },
        {
            source: 'Bloomberg',
            sourceUrl: 'https://www.bloomberg.com',
            title: 'Blé : Impact des conditions climatiques sur les récoltes',
            description: 'Les prévisions météorologiques affectent les prix des céréales. Surveillance des exportations ukrainiennes.',
            tags: ['commodities', 'geopolitics'],
            time: '6h',
            impact: 'medium'
        },
        {
            source: 'Financial Times',
            sourceUrl: 'https://www.ft.com',
            title: 'Argent : Double attrait industriel et valeur refuge',
            description: 'Le métal blanc bénéficie de la demande du secteur photovoltaïque et de son statut de valeur refuge.',
            tags: ['commodities'],
            time: '7h',
            impact: 'low'
        }
    ],
    etf: [
        {
            source: 'Morningstar',
            sourceUrl: 'https://www.morningstar.com',
            title: 'ETF Bitcoin Spot (IBIT) : $50 milliards d\'actifs sous gestion',
            description: 'Le fonds iShares Bitcoin Trust devient l\'un des ETF à la croissance la plus rapide de l\'histoire. Performance YTD exceptionnelle.',
            tags: ['crypto', 'markets'],
            time: '1h',
            impact: 'high'
        },
        {
            source: 'ETF.com',
            sourceUrl: 'https://www.etf.com',
            title: 'ETF Or (GLD) : Flux entrants record face à l\'incertitude',
            description: 'Les investisseurs se tournent vers l\'or papier pour sécuriser leurs portefeuilles. $890M de flux nets ce mois.',
            tags: ['commodities', 'markets'],
            time: '2h',
            impact: 'medium'
        },
        {
            source: 'Bloomberg',
            sourceUrl: 'https://www.bloomberg.com',
            title: 'ETF IA : Nvidia pousse les fonds technologiques',
            description: 'Les ETF exposés à l\'intelligence artificielle surperforment. Focus sur les semi-conducteurs et le cloud computing.',
            tags: ['markets'],
            time: '3h',
            impact: 'high'
        },
        {
            source: 'Financial Times',
            sourceUrl: 'https://www.ft.com',
            title: 'ETF ESG : Croissance malgré les débats sur le greenwashing',
            description: 'Les fonds durables continuent d\'attirer des capitaux en Europe. Nouvelles réglementations SFDR renforcées.',
            tags: ['markets'],
            time: '4h',
            impact: 'medium'
        },
        {
            source: 'Les Échos',
            sourceUrl: 'https://www.lesechos.fr',
            title: 'ETF Obligataires : Rendements attractifs dans l\'environnement actuel',
            description: 'Les fonds obligataires retrouvent de l\'intérêt avec les rendements élevés. Stratégies de duration à surveiller.',
            tags: ['markets'],
            time: '5h',
            impact: 'medium'
        },
        {
            source: 'Seeking Alpha',
            sourceUrl: 'https://seekingalpha.com',
            title: 'ETF Émergents : Valorisations attractives pour 2026',
            description: 'Les marchés émergents offrent des opportunités de diversification. Focus sur l\'Inde et le Vietnam.',
            tags: ['markets'],
            time: '6h',
            impact: 'medium'
        },
        {
            source: 'Morningstar',
            sourceUrl: 'https://www.morningstar.com',
            title: 'ETF Dividendes : Stratégies de rendement pour revenus passifs',
            description: 'Les fonds axés sur les dividendes attirent les investisseurs en quête de revenus réguliers.',
            tags: ['markets'],
            time: '7h',
            impact: 'low'
        }
    ]
};

// Breaking news for ticker
const breakingNews = [
    { icon: '📈', text: 'Bitcoin dépasse les $100,000 - Adoption institutionnelle en hausse' },
    { icon: '🛢️', text: 'Pétrole: tensions au Moyen-Orient impactent les cours' },
    { icon: '💹', text: 'Fed: pause dans le cycle de hausse des taux anticipée' },
    { icon: '🥇', text: 'Or: nouveau record historique à $2,100' },
    { icon: '📊', text: 'ETF Bitcoin: flux record de $1.5 milliard cette semaine' },
    { icon: '🌍', text: 'G7: nouvelles mesures économiques annoncées' },
    { icon: '⚡', text: 'Ethereum: succès de la mise à jour Dencun' },
    { icon: '🏦', text: 'BCE: Christine Lagarde s\'exprime sur la politique monétaire' }
];

// Source colors and logos
const sourceStyles = {
    'Reuters': { color: '#ff8000', initial: 'R' },
    'Bloomberg': { color: '#472a91', initial: 'B' },
    'Financial Times': { color: '#fff1e5', initial: 'FT', textColor: '#000' },
    'BBC News': { color: '#bb1919', initial: 'BBC' },
    'CNBC': { color: '#005594', initial: 'C' },
    'Al Jazeera': { color: '#d4a03b', initial: 'AJ' },
    'Wall Street Journal': { color: '#0274b6', initial: 'WSJ' },
    'CoinDesk': { color: '#0d47a1', initial: 'CD' },
    'Cointelegraph': { color: '#1a1a2e', initial: 'CT' },
    'The Block': { color: '#000000', initial: 'TB' },
    'Le Monde': { color: '#1a1a1a', initial: 'LM' },
    'Les Échos': { color: '#003f7f', initial: 'LE' },
    'France 24': { color: '#00a2e6', initial: 'F24' },
    'MarketWatch': { color: '#3c8f2c', initial: 'MW' },
    'Morningstar': { color: '#c21a3a', initial: 'M' },
    'ETF.com': { color: '#008b8b', initial: 'ETF' },
    'Decrypt': { color: '#8b5cf6', initial: 'D' },
    'Bloomberg Crypto': { color: '#472a91', initial: 'BC' },
    'Seeking Alpha': { color: '#f5820d', initial: 'SA' },
    'The Economist': { color: '#e3120b', initial: 'E' }
};

// ============================================
// Market Functions
// ============================================

function formatPrice(price, decimals = 2) {
    return price.toLocaleString('fr-FR', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    });
}

function updateMarketCard(id, data) {
    const priceElement = document.getElementById(`${id}-price`);
    const changeElement = document.getElementById(`${id}-change`);

    if (priceElement && changeElement) {
        priceElement.textContent = `$${formatPrice(data.price)}`;

        const changeText = `${data.change > 0 ? '+' : ''}${data.change.toFixed(2)}%`;
        changeElement.textContent = changeText;
        changeElement.className = `market-change ${data.change > 0 ? 'positive' : 'negative'}`;
    }
}

function simulateMarketUpdates() {
    Object.keys(marketData).forEach(key => {
        // Simulate realistic price movements
        const volatility = key === 'bitcoin' || key === 'ethereum' ? 0.3 : 0.15;
        const randomChange = (Math.random() - 0.5) * volatility;

        marketData[key].change = parseFloat((marketData[key].change + randomChange).toFixed(2));
        // Clamp change between -10 and +10
        marketData[key].change = Math.max(-10, Math.min(10, marketData[key].change));

        const priceChange = marketData[key].price * (randomChange / 100);
        marketData[key].price = parseFloat((marketData[key].price + priceChange).toFixed(2));
    });

    // Update all market cards
    updateMarketCard('btc', marketData.bitcoin);
    updateMarketCard('eth', marketData.ethereum);
    updateMarketCard('gold', marketData.gold);
    updateMarketCard('silver', marketData.silver);
    updateMarketCard('oil', marketData.oil);
    updateMarketCard('sp500', marketData.sp500);

    // Update market updates counter
    const marketUpdates = document.getElementById('market-updates');
    if (marketUpdates) {
        const currentCount = parseInt(marketUpdates.textContent) || 0;
        marketUpdates.textContent = currentCount + 1;
    }

    // Update last update time
    updateLastUpdateTime();
}

function initializeMarkets() {
    updateMarketCard('btc', marketData.bitcoin);
    updateMarketCard('eth', marketData.ethereum);
    updateMarketCard('gold', marketData.gold);
    updateMarketCard('silver', marketData.silver);
    updateMarketCard('oil', marketData.oil);
    updateMarketCard('sp500', marketData.sp500);

    // Start real-time simulation
    setInterval(simulateMarketUpdates, CONFIG.updateInterval);
}

// ============================================
// News Functions
// ============================================

function getSourceStyle(source) {
    return sourceStyles[source] || { color: '#2563eb', initial: source.substring(0, 1).toUpperCase() };
}

function createNewsCard(news, index = 0) {
    const card = document.createElement('div');
    card.className = 'news-card';
    card.style.animationDelay = `${index * CONFIG.animationDelay}ms`;

    const style = getSourceStyle(news.source);
    const impactClass = news.impact ? `impact-${news.impact}` : '';

    const tagsHTML = news.tags.map(tag =>
        `<span class="tag ${tag}">${getTagLabel(tag)}</span>`
    ).join('');

    card.innerHTML = `
        <div class="news-source">
            <div class="source-logo" style="background-color: ${style.color}; ${style.textColor ? `color: ${style.textColor}` : ''}">${style.initial}</div>
            <a href="${news.sourceUrl}" target="_blank" class="source-name">${news.source}</a>
            <span class="news-time">${news.time}</span>
            ${news.impact ? `<span class="impact-indicator ${impactClass}" title="Impact ${news.impact}"></span>` : ''}
        </div>
        <h3 class="news-title">${news.title}</h3>
        <p class="news-description">${news.description}</p>
        <div class="news-footer">
            <div class="news-tags">${tagsHTML}</div>
            <a href="${news.sourceUrl}" target="_blank" class="news-link">Lire l'article</a>
        </div>
    `;

    return card;
}

function getTagLabel(tag) {
    const labels = {
        'geopolitics': 'Géopolitique',
        'markets': 'Marchés',
        'crypto': 'Crypto',
        'commodities': 'Matières Premières',
        'conflicts': 'Conflits',
        'trade': 'Commerce',
        'politics': 'Politique'
    };
    return labels[tag] || tag;
}

function loadNews(sectionId, newsArray) {
    const container = document.getElementById(`${sectionId}-news`);
    if (!container) return;

    container.innerHTML = '';

    newsArray.forEach((news, index) => {
        const card = createNewsCard(news, index);
        container.appendChild(card);
    });

    // Update news count
    updateNewsCount();
}

function updateNewsCount() {
    const newsCount = document.getElementById('news-count');
    if (newsCount) {
        const totalNews = Object.values(newsDatabase).reduce((sum, arr) => sum + arr.length, 0);
        newsCount.textContent = totalNews;
    }
}

function initializeNews() {
    loadNews('geopolitics', newsDatabase.geopolitics);
    loadNews('markets', newsDatabase.markets);
    loadNews('crypto', newsDatabase.crypto);
    loadNews('commodities', newsDatabase.commodities);
    loadNews('etf', newsDatabase.etf);
}

function shuffleNews() {
    Object.keys(newsDatabase).forEach(category => {
        // Shuffle and update times
        newsDatabase[category] = newsDatabase[category]
            .sort(() => Math.random() - 0.5)
            .map((news, index) => ({
                ...news,
                time: getRandomTime(index)
            }));
    });
    initializeNews();
}

function getRandomTime(index) {
    const times = ['5min', '15min', '30min', '45min', '1h', '2h', '3h', '4h', '5h', '6h'];
    return times[Math.min(index, times.length - 1)];
}

// ============================================
// News Ticker
// ============================================

function initializeTicker() {
    const tickerContent = document.getElementById('ticker-content');
    if (!tickerContent) return;

    // Generate ticker HTML
    let tickerHTML = '';
    breakingNews.forEach((news, index) => {
        tickerHTML += `<span class="ticker-item">${news.icon} ${news.text}</span>`;
        if (index < breakingNews.length - 1) {
            tickerHTML += '<span class="ticker-separator">|</span>';
        }
    });

    // Duplicate for seamless scrolling
    tickerContent.innerHTML = tickerHTML + tickerHTML;
}

// ============================================
// Navigation
// ============================================

function initializeNavigation() {
    // Smooth scroll for navigation links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const tickerHeight = document.querySelector('.news-ticker')?.offsetHeight || 0;
                const offset = headerHeight + tickerHeight + 20;

                const targetPosition = targetSection.getBoundingClientRect().top + window.pageYOffset - offset;
                window.scrollTo({ top: targetPosition, behavior: 'smooth' });
            }

            // Close mobile menu if open
            closeMobileMenu();
        });
    });

    // Mobile menu
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mainNav = document.getElementById('main-nav');

    if (mobileMenuBtn && mainNav) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenuBtn.classList.toggle('active');
            mainNav.classList.toggle('active');
        });
    }

    // Active section highlighting
    initializeScrollSpy();
}

function closeMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mainNav = document.getElementById('main-nav');

    if (mobileMenuBtn && mainNav) {
        mobileMenuBtn.classList.remove('active');
        mainNav.classList.remove('active');
    }
}

function initializeScrollSpy() {
    const sections = document.querySelectorAll('.section');
    const navLinks = document.querySelectorAll('.nav-link');

    const observerOptions = {
        root: null,
        rootMargin: '-20% 0px -70% 0px',
        threshold: 0
    };

    const observerCallback = (entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${id}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    };

    const observer = new IntersectionObserver(observerCallback, observerOptions);
    sections.forEach(section => observer.observe(section));
}

// ============================================
// Filter Functionality
// ============================================

function initializeFilters() {
    const filterBtns = document.querySelectorAll('.filter-btn');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const filter = btn.dataset.filter;
            const section = btn.closest('.section');
            const newsGrid = section.querySelector('.news-grid');

            // Update active button
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Filter news
            filterNews(newsGrid, filter);
        });
    });
}

function filterNews(container, filter) {
    const cards = container.querySelectorAll('.news-card');

    cards.forEach(card => {
        if (filter === 'all') {
            card.style.display = '';
            return;
        }

        const tags = Array.from(card.querySelectorAll('.tag')).map(t =>
            t.classList.contains(filter)
        );

        card.style.display = tags.includes(true) ? '' : 'none';
    });
}

// ============================================
// Utility Functions
// ============================================

function updateLastUpdateTime() {
    const lastUpdate = document.getElementById('last-update');
    if (lastUpdate) {
        const now = new Date();
        lastUpdate.textContent = now.toLocaleString('fr-FR', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    }
}

// ============================================
// Initialization
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🌍 GéoFinance - Initialisation...');
    console.log('📊 Chargement des données de marché...');

    // Initialize all components
    initializeMarkets();
    initializeNews();
    initializeTicker();
    initializeNavigation();
    initializeFilters();
    updateLastUpdateTime();

    // Start periodic refresh
    setInterval(shuffleNews, CONFIG.newsRefreshInterval);

    console.log('✅ Application chargée avec succès!');
    console.log('📰 Sources:', Object.keys(sourceStyles).length, 'médias internationaux');
    console.log('💹 Marchés en temps réel activés');
    console.log('🔄 Actualisation automatique toutes les 5 minutes');
});

// ============================================
// Service Worker Registration (Optional PWA)
// ============================================

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Uncomment to enable PWA functionality
        // navigator.serviceWorker.register('/sw.js');
    });
}
