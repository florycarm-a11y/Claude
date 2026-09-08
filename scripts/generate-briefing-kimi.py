#!/usr/bin/env python3
"""
Inflexion — Générateur de briefing quotidien (remplacement API Anthropic)
Génère sentiment.json, alerts.json, macro-analysis.json, market-briefing.json, daily-briefing.json
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
HISTORY_DIR = DATA_DIR / "briefing-history"

DATE_STR = "2026-09-07"
GENERATED_AT = "2026-09-07T18:12:50Z"

def load_json(name):
    p = DATA_DIR / name
    if not p.exists():
        return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def save_json(name, data):
    p = DATA_DIR / name
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  📝 {name} sauvegardé")

def format_currency(val):
    if val >= 1e12:
        return f"{val/1e12:.2f} T$"
    if val >= 1e9:
        return f"{val/1e9:.1f} Mds $"
    if val >= 1e6:
        return f"{val/1e6:.1f} M$"
    return f"{val:,.2f} $"

def main():
    print("╔══════════════════════════════════════════════════╗")
    print("║  Inflexion — Briefing Kimi (sans API Claude)     ║")
    print("╚══════════════════════════════════════════════════╝")
    print(f"  📅 {DATE_STR}")

    # ── Chargement des données ──
    sources = {
        "news": load_json("news.json"),
        "newsapi": load_json("newsapi.json"),
        "markets": load_json("markets.json"),
        "crypto": load_json("crypto.json"),
        "fearGreed": load_json("fear-greed.json"),
        "macro": load_json("macro.json"),
        "globalMacro": load_json("global-macro.json"),
        "commodities": load_json("commodities.json"),
        "defi": load_json("defi.json"),
        "alphaVantage": load_json("alpha-vantage.json"),
        "onchain": load_json("onchain.json"),
        "europeanMarkets": load_json("european-markets.json"),
        "worldBank": load_json("world-bank.json"),
    }
    available = [k for k, v in sources.items() if v is not None]
    print(f"📊 Sources chargées : {', '.join(available)} ({len(available)}/{len(sources)})")

    # ── Extraction des données clés ──
    spy = next((q for q in sources["markets"]["quotes"] if q["symbol"] == "SPY"), None)
    qqq = next((q for q in sources["markets"]["quotes"] if q["symbol"] == "QQQ"), None)
    dia = next((q for q in sources["markets"]["quotes"] if q["symbol"] == "DIA"), None)
    gld = next((q for q in sources["markets"]["quotes"] if q["symbol"] == "GLD"), None)
    uso = next((q for q in sources["markets"]["quotes"] if q["symbol"] == "USO"), None)
    nvda = next((q for q in sources["markets"]["quotes"] if q["symbol"] == "NVDA"), None)
    aapl = next((q for q in sources["markets"]["quotes"] if q["symbol"] == "AAPL"), None)
    msft = next((q for q in sources["markets"]["quotes"] if q["symbol"] == "MSFT"), None)
    googl = next((q for q in sources["markets"]["quotes"] if q["symbol"] == "GOOGL"), None)
    tsla = next((q for q in sources["markets"]["quotes"] if q["symbol"] == "TSLA"), None)

    btc = next((c for c in sources["crypto"]["prices"] if c["symbol"] == "BTC"), None)
    eth = next((c for c in sources["crypto"]["prices"] if c["symbol"] == "ETH"), None)
    xrp = next((c for c in sources["crypto"]["prices"] if c["symbol"] == "XRP"), None)
    sol = next((c for c in sources["crypto"]["prices"] if c["symbol"] == "SOL"), None)
    doge = next((c for c in sources["crypto"]["prices"] if c["symbol"] == "DOGE"), None)
    ada = next((c for c in sources["crypto"]["prices"] if c["symbol"] == "ADA"), None)

    fng = sources["fearGreed"]["current"]["value"]
    fng_label = sources["fearGreed"]["current"]["label"]
    fng_week = sources["fearGreed"]["changes"]["week"]
    fng_month = sources["fearGreed"]["changes"]["month"]

    macro_indicators = {i["id"]: i for i in sources["macro"]["indicators"]}
    cpi = macro_indicators.get("CPIAUCSL")
    fed_funds = macro_indicators.get("DFF")
    gdp = macro_indicators.get("GDP")
    unrate = macro_indicators.get("UNRATE")
    t10y = macro_indicators.get("DGS10")
    dxy = macro_indicators.get("DTWEXBGS")
    spread10y2y = macro_indicators.get("T10Y2Y")
    m2 = macro_indicators.get("M2SL")
    walcl = macro_indicators.get("WALCL")
    mortgage30 = macro_indicators.get("MORTGAGE30US")

    ecb_rate = sources["globalMacro"]["ecb"]["main_rate"]["value"] if sources["globalMacro"].get("ecb") else None
    eurusd_ecb = sources["globalMacro"]["ecb"]["eurusd"]["rate"] if sources["globalMacro"].get("ecb") else None

    defi_tvl = sources["defi"]["totalTVL"] if sources["defi"] else None
    top_protocols = sources["defi"]["topProtocols"][:5] if sources["defi"] else []

    forex = {f["pair"]: f for f in sources["alphaVantage"]["forex"]} if sources["alphaVantage"] else {}
    eurusd_av = forex.get("EUR/USD")
    gbpusd_av = forex.get("GBP/USD")
    usdjpy_av = forex.get("USD/JPY")

    dax = sources["europeanMarkets"]["indices"][0] if sources["europeanMarkets"] and sources["europeanMarkets"]["indices"] else None

    hashrate = sources["onchain"]["btc_mining"]["hashrate_eh"] if sources["onchain"] and sources["onchain"].get("btc_mining") else None
    btc_fees_30min = sources["onchain"]["btc_fees"]["half_hour"] if sources["onchain"] and sources["onchain"].get("btc_fees") else None

    # ── Calcul sentiment ──
    sentiment_categories = {}

    # Géopolitique
    sentiment_categories["geopolitique"] = {
        "score": -0.40,
        "confidence": 0.70,
        "tendance": "baissier",
        "resume": "Tensions persistantes autour du détroit d'Ormuz et de la guerre Iran-US (6 mois) maintiennent le risque géopolitique élevé. Les sanctions européennes contre la Russie s'élargissent à 1 600 entités.",
        "signaux_cles": [
            "Trafic Ormuz sous les 20 traversées quotidiennes",
            "UE prépare des sanctions contre 1 600 entités russes",
            "Guerre Iran-US : 6 mois de conflit, pression économique croissante"
        ]
    }

    # Marchés : SPY -0.39%, DIA -0.53%, QQQ +0.18%, mais AAPL -2.51%, MSFT -2.04%, GOOGL -1.17%, TSLA -5.92%, NVDA +0.84%
    sentiment_categories["marches"] = {
        "score": -0.25,
        "confidence": 0.75,
        "tendance": "baissier",
        "resume": f"Le secteur tech subit une correction sévère : Tesla s'effondre de {abs(tsla['change']):.2f}%, Apple cède {abs(aapl['change']):.2f}% et Microsoft {abs(msft['change']):.2f}%. Le SPY (proxy S&P 500) recule de {abs(spy['change']):.2f}% et le Dow Jones (DIA) de {abs(dia['change']):.2f}%, tandis que le Nasdaq 100 (QQQ) résiste légèrement (+0,18%).",
        "signaux_cles": [
            f"Tesla à {tsla['price']:.2f} $ ({tsla['change']:+.2f}%) — pire performance du panel (Finnhub)",
            f"SPY (proxy S&P 500) à {spy['price']:.2f} $ ({spy['change']:+.2f}%) (Finnhub)",
            f"Nasdaq 100 (QQQ) à {qqq['price']:.2f} $ ({qqq['change']:+.2f}%) — résistance relative (Finnhub)"
        ]
    }

    # Crypto : BTC -1.71%, ETH -2.44%, market cap -3.16%, mais SOL +39% sur 30j
    sentiment_categories["crypto"] = {
        "score": -0.20,
        "confidence": 0.70,
        "tendance": "mixte",
        "resume": f"Le marché crypto corrige avec BTC à {btc['price']:,.0f} $ ({btc['change_24h']:+.1f}%) et une capitalisation totale en repli de 3,16%. Cependant, le Fear & Greed Index reste à {fng}/100 ({fng_label}), en hausse de {fng_week} points sur la semaine, signalant un sentiment encore positif malgré la pause technique.",
        "signaux_cles": [
            f"BTC à {btc['price']:,.0f} $ (24h: {btc['change_24h']:+.1f}%, 7j: +{btc['change_7d']:.1f}%, 30j: +{btc['change_30d']:.0f}%) (CoinGecko)",
            f"Fear & Greed Index à {fng}/100 ({fng_label}), +{fng_week} pts sur 7j (Alternative.me)",
            f"Capitalisation totale crypto à {format_currency(sources['crypto']['global']['total_market_cap'])} (-3,16% sur 24h) (CoinGecko)"
        ]
    }

    # Matières premières
    sentiment_categories["matieres_premieres"] = {
        "score": -0.20,
        "confidence": 0.55,
        "tendance": "baissier",
        "resume": f"L'or corrige légèrement avec GLD à {gld['price']:.2f} $ ({gld['change']:+.2f}%). Le pétrole (USO) est quasi-stable à {uso['price']:.2f} $ ({uso['change']:+.2f}%). Les données spot de métaux et d'énergie sont indisponibles.",
        "signaux_cles": [
            f"GLD (proxy or) à {gld['price']:.2f} $ ({gld['change']:+.2f}%) (Finnhub)",
            f"USO (proxy pétrole) à {uso['price']:.2f} $ ({uso['change']:+.2f}%) (Finnhub)",
            "Tensions Ormuz : trafic effondré sous 20 navires/jour"
        ]
    }

    # AI/Tech
    sentiment_categories["ai_tech"] = {
        "score": -0.15,
        "confidence": 0.60,
        "tendance": "baissier",
        "resume": "La tech corrige avec AAPL, MSFT et GOOGL en baisse, malgré une résistance de Nvidia (+0,84%). Les incidents d'IA 'rogue' doublent selon The Guardian, tandis que la régulation européenne sur ChatGPT se précise.",
        "signaux_cles": [
            f"Nvidia à {nvda['price']:.2f} $ (+{nvda['change']:.2f}%) — seule résistance du panel tech (Finnhub)",
            "Incidents d'IA rogue en hausse de ~100% le mois dernier (The Guardian)",
            "Commission européenne évalue le statut de ChatGPT comme 'très grande plateforme'"
        ]
    }

    # Score global
    total_weight = 0
    weighted_sum = 0
    for cat in sentiment_categories.values():
        w = cat["confidence"]
        weighted_sum += cat["score"] * w
        total_weight += w
    global_score = round(weighted_sum / total_weight, 2) if total_weight > 0 else 0
    if global_score > 0.2:
        global_tendance = "haussier"
    elif global_score < -0.2:
        global_tendance = "baissier"
    else:
        global_tendance = "mixte"

    dominant = max(sentiment_categories.items(), key=lambda x: abs(x[1]["score"]))
    global_resume = f"Le sentiment global est {global_tendance} ({global_score:+.2f}), dominé par la rubrique {dominant[0]} ({dominant[1]['tendance']})."

    # Historique sentiment
    historique = []
    hist_path = DATA_DIR / "sentiment.json"
    if hist_path.exists():
        try:
            with open(hist_path, "r", encoding="utf-8") as f:
                old = json.load(f)
                historique = old.get("historique", [])
        except Exception:
            pass
    historique = [h for h in historique if h.get("date") != DATE_STR]
    hist_entry = {"date": DATE_STR, "global": global_score}
    for rubrique, data in sentiment_categories.items():
        hist_entry[rubrique] = data["score"]
    historique.append(hist_entry)
    historique = historique[-30:]

    # ── Alertes ──
    alertes = []
    # TSLA -5.92%
    if tsla and abs(tsla["change"]) >= 3.0:
        alertes.append({
            "id": f"alert-{DATE_STR}-001",
            "titre": f"Tesla (TSLA) : {tsla['change']:+.2f}%, perte de {abs(tsla['change_abs']):.2f} $",
            "texte": f"Tesla s'effondre de {abs(tsla['change']):.2f}% à {tsla['price']:.2f} $, sous-performant largement le marché. Cette correction s'inscrit dans une tendance de prises de bénéfices sur les valeurs de croissance les plus chères.",
            "categorie": "marches",
            "severite": "urgent",
            "impact": "baissier",
            "horodatage": GENERATED_AT,
            "donnees": {"symbole": "TSLA", "prix": tsla["price"], "variation": round(tsla["change"], 2)}
        })
    # AAPL -2.51%
    if aapl and abs(aapl["change"]) >= 2.0:
        alertes.append({
            "id": f"alert-{DATE_STR}-002",
            "titre": f"Apple (AAPL) : {aapl['change']:+.2f}%, retour sous {aapl['price']:.0f} $",
            "texte": f"Apple chute de {abs(aapl['change']):.2f}% à {aapl['price']:.2f} $, dans le sillage d'une correction sectorielle tech. Microsoft et Alphabet subissent des pertes similaires.",
            "categorie": "marches",
            "severite": "attention",
            "impact": "baissier",
            "horodatage": GENERATED_AT,
            "donnees": {"symbole": "AAPL", "prix": aapl["price"], "variation": round(aapl["change"], 2)}
        })
    # BTC -1.71% (pas assez pour alerte crypto mais on le met en info si on veut)
    # ADA -3.54% sur 24h
    if ada and abs(ada["change_24h"]) >= 3.0:
        alertes.append({
            "id": f"alert-{DATE_STR}-003",
            "titre": f"Cardano (ADA) : {ada['change_24h']:+.1f}% sur 24h",
            "texte": f"Cardano recule de {abs(ada['change_24h']):.1f}% sur 24h à {ada['price']:.4f} $, sous-performant le marché crypto. La baisse s'inscrit dans une correction généralisée des altcoins.",
            "categorie": "crypto",
            "severite": "attention",
            "impact": "baissier",
            "horodatage": GENERATED_AT,
            "donnees": {"symbole": "ADA", "prix": ada["price"], "variation_24h": round(ada["change_24h"], 2)}
        })
    # Fear & Greed +5 pts sur 7j (info)
    if fng_week and abs(fng_week) >= 5:
        alertes.append({
            "id": f"alert-{DATE_STR}-004",
            "titre": f"Fear & Greed : +{fng_week} pts sur 7 jours (actuellement {fng})",
            "texte": f"L'indice de sentiment crypto gagne {fng_week} points en une semaine, passant à {fng}/100 ({fng_label}). Malgré la correction des prix, le sentiment reste dans la zone Greed, ce qui pourrait indiquer une surconfiance des investisseurs.",
            "categorie": "macro",
            "severite": "info",
            "impact": "neutre",
            "horodatage": GENERATED_AT,
            "donnees": {"score": fng, "label": fng_label, "variation_7j": fng_week}
        })

    alert_stats = {
        "total": len(alertes),
        "urgent": sum(1 for a in alertes if a["severite"] == "urgent"),
        "attention": sum(1 for a in alertes if a["severite"] == "attention"),
        "info": sum(1 for a in alertes if a["severite"] == "info"),
    }

    # ── Macro Analysis ──
    macro = {
        "titre": "Tech en correction, Fed en pause — le dollar repart à la hausse",
        "phase_cycle": "transition",
        "politique_monetaire": "neutre",
        "tendance_inflation": "stabilisation",
        "score_risque": 6,
        "analyse": f"<h2>Contexte macroéconomique</h2>\n<p>La Fed maintient ses taux directeurs à <strong>3,63 %</strong> (FRED, DFF), dans une pause technique qui s'éternise. L'inflation CPI affiche <strong>3,54 % en glissement annuel</strong> (juillet 2026), toujours au-dessus de la cible de 2 %. Le chômage reste stable à <strong>4,1 %</strong> (août 2026), signe d'une résilience du marché du travail américain.</p>\n\n<h2>Enjeux clés</h2>\n<ul>\n<li><strong>Politique monétaire</strong> : La BCE maintient son taux directeur à <strong>2,40 %</strong> (ECB Data), tandis que la Fed reste à 3,63 %. Cette divergence a poussé l'<strong>EUR/USD à 1,1628</strong> (ECB fixing), mais le <strong>dollar index (DXY) repart à la hausse à 118,75</strong> (+0,39 point, FRED), limitant l'appréciation de l'euro.</li>\n<li><strong>Courbe des taux</strong> : Le <strong>Treasury 10Y est stable à 4,77 %</strong> (-0,02 point, FRED), et le <strong>spread 10Y-2Y se maintient à 0,41 %</strong> (-0,02 point). L'aplatissement persistant de la courbe reste un signal de vigilance.</li>\n<li><strong>Liquidité</strong> : Le <strong>bilan Fed a légèrement augmenté de 6,3 Mds $</strong> (FRED, WALCL), à 6 737 Mds $, un mouvement technique qui ne change pas la trajectoire globale de normalisation. La masse monétaire M2 reste à <strong>23 218 Mds $</strong>. Le <strong>taux hypothécaire 30 ans remonte à 6,71 %</strong> (+0,05 point), pesant sur l'immobilier.</li>\n</ul>\n\n<h2>Risques & Opportunités</h2>\n<ul>\n<li><strong>Risque 1 — Correction tech prolongée</strong> : Tesla -5,92%, Apple -2,51%, Microsoft -2,04%. Une contagion au reste du marché est possible si les résultats déçoivent.</li>\n<li><strong>Risque 2 — Choc énergétique</strong> : Tensions Ormuz persistantes. Un blocage durable provoquerait un spike pétrolier et forcerait la Fed à réagir.</li>\n<li><strong>Risque 3 — Dollar fort</strong> : DXY à 118,75. Un dollar trop fort pèse sur les bénéfices des multinationales américaines et sur les économies émergentes.</li>\n<li><strong>Opportunité 1 — Rotation vers l'Europe</strong> : Le DAX résiste (-0,09%) et l'EUR/USD reste élevé, favorisant les valuations européennes.</li>\n<li><strong>Opportunité 2 — Accumulation crypto</strong> : La correction BTC (-1,71%) dans un contexte de Fear & Greed encore positif (73) pourrait offrir des points d'entrée.</li>\n</ul>\n\n<h2>Perspectives</h2>\n<p>Trois scénarios se dessinent : (1) <strong>consolidation</strong> — la correction tech reste circonscrite au secteur growth, le reste du marché résiste, et la Fed maintient son statu quo ; (2) <strong>contagion</strong> — si Tesla et Apple entraînent le SPY sous 760 $, un mouvement de risk-off généralisé pourrait s'enclencher ; (3) <strong>rebond tech</strong> — si les résultats de Nvidia et autres big tech rassurent, le capital pourrait revenir rapidement sur le secteur.</p>",
        "indicateurs_cles": [
            {"nom": "CPI", "valeur": "3,54 % YoY", "signal": "neutre", "commentaire": "Au-dessus de la cible Fed mais stable"},
            {"nom": "Fed Funds", "valeur": "3,63 %", "signal": "neutre", "commentaire": "Pause technique prolongée"},
            {"nom": "Chômage", "valeur": "4,1 %", "signal": "neutre", "commentaire": "Stable, marché du travail résilient"},
            {"nom": "Treasury 10Y", "valeur": "4,77 %", "signal": "neutre", "commentaire": "Stable, pas de panique obligataire"},
            {"nom": "Spread 10Y-2Y", "valeur": "0,41 %", "signal": "baissier", "commentaire": "Aplatissement persistant, vigilance"},
            {"nom": "Bilan Fed", "valeur": "6 737 Mds $", "signal": "neutre", "commentaire": "Légère hausse technique (+6,3 Mds $)"},
            {"nom": "Taux BCE", "valeur": "2,40 %", "signal": "haussier", "commentaire": "Divergence accommodante vs Fed"},
            {"nom": "EUR/USD", "valeur": "1,1628", "signal": "neutre", "commentaire": "Stable malgré la force du dollar"},
            {"nom": "Dollar Index (DXY)", "valeur": "118,75", "signal": "baissier", "commentaire": "Reprise à la hausse, +0,39 point"},
            {"nom": "Taux hypothécaire 30 ans", "valeur": "6,71 %", "signal": "baissier", "commentaire": "Hausse de 0,05 point, pression immobilier"},
        ],
        "perspectives": "Le scénario central reste un statu quo monétaire américain jusqu'à la fin 2026, avec une Fed qui privilégie la stabilité face à l'incertitude géopolitique et sectorielle. La correction tech pourrait s'étendre si les résultats déçoivent, mais le fondamental macro reste solide (chômage bas, croissance positive). Le principal catalyseur de basculement reste un choc énergétique majeur (Ormuz).",
        "updated": GENERATED_AT,
        "source": "Kimi + FRED + BCE + ECB Data",
        "indicators_count": len(sources["macro"]["indicators"]) if sources["macro"] else 0,
        "mode": "consolidated"
    }

    # ── Market Briefing ──
    briefing_sections = [
        {
            "titre": "Contexte & Régime de marché",
            "contenu": f"<p>Le régime de marché est <strong>baissier sur le secteur tech</strong>, mitigé sur les indices larges. Le <strong>SPY (proxy S&P 500) recule de {abs(spy['change']):.2f}%</strong> à {spy['price']:.2f} $, le <strong>Dow Jones (DIA) cède {abs(dia['change']):.2f}%</strong> à {dia['price']:.2f} $, tandis que le <strong>Nasdaq 100 (QQQ) résiste légèrement (+{qqq['change']:.2f}%)</strong> à {qqq['price']:.2f} $ (Finnhub). Cette divergence reflète une segmentation au sein même du secteur technologique, où Nvidia (+0,84%) résiste mais Tesla, Apple et Microsoft corrigent fortement.</p>",
            "tendance": "mixte"
        },
        {
            "titre": "Actions & Indices",
            "contenu": f"<p>Le secteur tech affiche une <strong>bifurcation marquée et à la baisse</strong> : <strong>Tesla s'effondre de {abs(tsla['change']):.2f}%</strong> à {tsla['price']:.2f} $, <strong>Apple chute de {abs(aapl['change']):.2f}%</strong> à {aapl['price']:.2f} $, <strong>Microsoft cède {abs(msft['change']):.2f}%</strong> à {msft['price']:.2f} $ et <strong>Alphabet recule de {abs(googl['change']):.2f}%</strong> à {googl['price']:.2f} $ (Finnhub). Seul <strong>Nvidia résiste avec +{nvda['change']:.2f}%</strong> à {nvda['price']:.2f} $. En Europe, le <strong>DAX est quasi-stable ({dax['change_pct']:+.2f}%)</strong> à {dax['price']:.3f} (Twelve Data), montrant une meilleure résilience.</p>",
            "tendance": "baissier"
        },
        {
            "titre": "Crypto & DeFi",
            "contenu": f"<p>Le marché crypto connaît une <strong>correction technique</strong> après un rallye de 30 jours spectaculaire. <strong>Bitcoin cède {abs(btc['change_24h']):.1f}%</strong> à {btc['price']:,.0f} $, <strong>Ethereum recule de {abs(eth['change_24h']):.1f}%</strong> à {eth['price']:,.0f} $, et la capitalisation totale perd 3,16% (CoinGecko). Le <strong>Fear & Greed Index à {fng}/100</strong> ({fng_label}) reste élevé malgré une légère baisse, suggérant que le sentiment des investisseurs reste globalement positif. La <strong>TVL DeFi s'établit à {format_currency(defi_tvl)}</strong> (DefiLlama), stable malgré la correction.</p>",
            "tendance": "neutre"
        },
        {
            "titre": "Matières premières & Forex",
            "contenu": f"<p>L'<strong>or corrige légèrement</strong> : l'ETF GLD perd {abs(gld['change']):.2f}% à {gld['price']:.2f} $ (Finnhub). Le <strong>pétrole (USO) est quasi-stable</strong> à {uso['price']:.2f} $ ({uso['change']:+.2f}%). Sur le front des devises, l'<strong>EUR/USD se maintient à {eurusd_av['rate']:.4f}</strong> (Alpha Vantage) malgré la <strong>force du dollar index (DXY) à 118,75</strong> (+0,39 point, FRED). Le <strong>USD/JPY recule à {usdjpy_av['rate']:.2f}</strong>, allégeant la pression sur la BoJ. Le <strong>GBP/USD est à {gbpusd_av['rate']:.4f}</strong>.</p>",
            "tendance": "mixte"
        },
    ]

    market_briefing = {
        "titre": "Correction tech sévère — Tesla et big tech sous pression, crypto en pause",
        "date": DATE_STR,
        "resume_executif": f"Les marchés affichent une configuration <strong>fragmentée et à la baisse sur le secteur tech</strong> : Tesla s'effondre de {abs(tsla['change']):.2f}%, Apple chute de {abs(aapl['change']):.2f}% et Microsoft cède {abs(msft['change']):.2f}%, tandis que le Nasdaq 100 (QQQ) résiste légèrement (+0,18%). Le crypto corrige (BTC -1,71%, market cap -3,16%) mais le Fear & Greed reste à {fng}/100 (Greed). Le dollar repart à la hausse (DXY 118,75) et l'or corrige légèrement (GLD -0,84%).",
        "sections": briefing_sections,
        "sentiment_global": "mixte",
        "vigilance": [
            f"Tesla à {tsla['price']:.2f} $ ({tsla['change']:+.2f}%) — surveiller un rebond ou une extension de la correction",
            "Dollar Index (DXY) à 118,75 — force du dollar pouvant peser sur les bénéfices des multinationales",
            "Fear & Greed Index à 73/100 — zone Greed, risque de surconfiance malgré la correction",
            "Tensions Ormuz : trafic sous les 20 navires/jour — risque de choc énergétique"
        ],
        "tags": ["tech", "correction", "tesla", "crypto", "fed", "dollar", "ormuz"],
        "updated": GENERATED_AT,
        "source": "Kimi + multi-sources",
        "sources_used": available,
        "mode": "consolidated"
    }

    # ── Daily Briefing ──
    briefing_type = "complet"

    signal_du_jour = f"Le <strong>secteur tech subit une correction sévère</strong> avec Tesla qui s'effondre de <strong>{abs(tsla['change']):.2f}%</strong> à {tsla['price']:.2f} $, Apple qui chute de <strong>{abs(aapl['change']):.2f}%</strong> et Microsoft de <strong>{abs(msft['change']):.2f}%</strong> (Finnhub), tandis que le <strong>crypto marque une pause technique</strong> (BTC {btc['change_24h']:+.1f}%, Fear & Greed à {fng}/100). Le <strong>dollar repart à la hausse</strong> (DXY 118,75) et l'<strong>or corrige légèrement</strong> (GLD {gld['change']:+.2f}%). Cette configuration appelle une approche défensive sur le tech et une vigilance accrue sur les supports clés."

    synthese_contenu = f"""<h2>Évolutions du jour</h2>
<p>Les marchés affichent une <strong>configuration fragmentée avec une correction sévère sur le secteur technologique</strong>. <strong>Tesla s'effondre de {abs(tsla['change']):.2f}%</strong> à {tsla['price']:.2f} $, <strong>Apple chute de {abs(aapl['change']):.2f}%</strong> à {aapl['price']:.2f} $, <strong>Microsoft cède {abs(msft['change']):.2f}%</strong> à {msft['price']:.2f} $ et <strong>Alphabet recule de {abs(googl['change']):.2f}%</strong> (Finnhub). Seul <strong>Nvidia résiste avec +{nvda['change']:.2f}%</strong> à {nvda['price']:.2f} $. Les indices larges sont mitigés : le <strong>SPY (proxy S&P 500) perd {abs(spy['change']):.2f}%</strong> à {spy['price']:.2f} $, le <strong>Dow Jones (DIA) cède {abs(dia['change']):.2f}%</strong>, tandis que le <strong>Nasdaq 100 (QQQ) gagne {qqq['change']:.2f}%</strong> à {qqq['price']:.2f} $.</p>

<p>Le <strong>marché crypto corrige légèrement</strong> : <strong>Bitcoin cède {abs(btc['change_24h']):.1f}%</strong> à {btc['price']:,.0f} $, <strong>Ethereum recule de {abs(eth['change_24h']):.1f}%</strong> à {eth['price']:,.0f} $, et la capitalisation totale perd 3,16% (CoinGecko). Le <strong>Fear & Greed Index se maintient à {fng}/100 ({fng_label})</strong> (Alternative.me), en <strong>hausse de {fng_week} points sur 7 jours</strong>, signalant un sentiment encore positif malgré la pause technique. La <strong>TVL DeFi reste stable à {format_currency(defi_tvl)}</strong> (DefiLlama).</p>

<p>Sur le front macro, le <strong>Treasury 10Y est stable à 4,77%</strong> (-0,02 point, FRED), mais le <strong>dollar index (DXY) repart à la hausse à 118,75</strong> (+0,39 point), portant l'<strong>EUR/USD à {eurusd_av['rate']:.4f}</strong> (Alpha Vantage). L'<strong>or corrige légèrement</strong> : GLD perd {abs(gld['change']):.2f}% à {gld['price']:.2f} $ (Finnhub). En Europe, le <strong>DAX est quasi-stable ({dax['change_pct']:+.2f}%)</strong> (Twelve Data). Le <strong>taux hypothécaire 30 ans remonte à 6,71%</strong> (+0,05 point), pesant sur l'immobilier.</p>

<h2>Perspectives</h2>
<p>Trois scénarios se dessinent pour les 48h à venir : (1) <strong>rebond tech sélectif</strong> — si Nvidia et les big tech rassurent, le capital pourrait revenir rapidement sur le secteur, profitant aux valeurs de qualité ; (2) <strong>contagion de la correction</strong> — si Tesla et Apple entraînent le SPY sous 760 $, un mouvement de risk-off généralisé pourrait s'enclencher, profitant à l'or et aux obligations ; (3) <strong>choc géopolitique</strong> — un blocage durable d'Ormuz forcerait une réévaluation immédiate des actifs risqués et un spike énergétique.</p>

<p><em>Disclaimer : Ce briefing est produit à des fins d'information uniquement. Il ne constitue pas une recommandation d'investissement. Inflexion n'est pas agréé pour fournir des conseils en investissement au sens de l'AMF.</em></p>"""

    signaux = [
        {
            "titre": f"Correction tech sévère : Tesla -{abs(tsla['change']):.2f}%, AAPL -{abs(aapl['change']):.2f}%",
            "description": f"<p>Le secteur technologique subit une <strong>correction sévère et segmentée</strong>. <strong>Tesla s'effondre de {abs(tsla['change']):.2f}%</strong> à {tsla['price']:.2f} $, <strong>Apple chute de {abs(aapl['change']):.2f}%</strong> à {aapl['price']:.2f} $, <strong>Microsoft cède {abs(msft['change']):.2f}%</strong> et <strong>Alphabet recule de {abs(googl['change']):.2f}%</strong> (Finnhub). Seul <strong>Nvidia résiste avec +{nvda['change']:.2f}%</strong> à {nvda['price']:.2f} $. Cette segmentation suggère que le marché punit les valeurs aux fondamentaux les plus dépendants de la croissance (Tesla, Apple services) tout en récompensant les pures-plays IA (Nvidia). La correction pourrait s'étendre si les résultats du trimestre déçoivent.</p>",
            "categorie": "marches",
            "interconnexions": [
                {
                    "secteur": "Crypto",
                    "impact": f"BTC {btc['change_24h']:+.1f}%, ETH {eth['change_24h']:+.1f}% (CoinGecko)",
                    "explication": "La correction tech et la pause crypto sont corrélées : le capital quitte les actifs de croissance risqués simultanément."
                },
                {
                    "secteur": "Macro",
                    "impact": "DXY à 118,75 (+0,39 point)",
                    "explication": "La force du dollar pèse sur les bénéfices des multinationales tech américaines, exacerbant la correction."
                },
                {
                    "secteur": "DeFi",
                    "impact": f"TVL stable à {format_currency(defi_tvl)} (DefiLlama)",
                    "explication": "La TVL crypto résiste, indiquant que la correction est spéculative et non structurelle."
                }
            ],
            "regions": ["Amérique du Nord", "Europe"],
            "severite": "urgent"
        },
        {
            "titre": f"Crypto en pause technique : Fear & Greed à {fng}/100 (+{fng_week} pts sur 7j)",
            "description": f"<p>Le marché crypto corrige après un rallye de 30 jours historique : <strong>BTC à {btc['price']:,.0f} $ ({btc['change_24h']:+.1f}%)</strong>, <strong>ETH à {eth['price']:,.0f} $ ({eth['change_24h']:+.1f}%)</strong>, capitalisation totale -3,16% (CoinGecko). Cependant, le <strong>Fear & Greed Index reste à {fng}/100 ({fng_label})</strong>, en <strong>hausse de {fng_week} points sur la semaine</strong> (Alternative.me), ce qui est paradoxal : les prix baissent mais le sentiment s'améliore. Cette divergence pourrait indiquer que les investisseurs institutionnels (whales) accumulent pendant que le retail panique, comme documenté par Crypto Briefing (accumulation de 39 000 BTC par les whales).</p>",
            "categorie": "crypto",
            "interconnexions": [
                {
                    "secteur": "Actions tech",
                    "impact": f"Nasdaq 100 (QQQ) {qqq['change']:+.2f}%, TSLA {tsla['change']:+.2f}% (Finnhub)",
                    "explication": "La déconnexion crypto/tech persiste mais s'inverse : le crypto corrige moins sévèrement que le secteur tech."
                },
                {
                    "secteur": "Macro",
                    "impact": "Treasury 10Y à 4,77%, Fed en pause",
                    "explication": "Un environnement de taux stable favorise les actifs à duration longue, mais la force du dollar limite l'appétit pour le risque."
                }
            ],
            "regions": ["Global"],
            "severite": "attention"
        },
        {
            "titre": "Dollar fort et or en correction : la divergence DXY/or se résorbe",
            "description": f"<p>Le <strong>dollar index (DXY) repart à la hausse à 118,75</strong> (+0,39 point, FRED), tandis que l'<strong>or corrige légèrement</strong> (GLD -{abs(gld['change']):.2f}% à {gld['price']:.2f} $, Finnhub). Cette cohérence signale que la relation inverse dollar/or se rétablit après une période de divergence. L'<strong>EUR/USD se maintient à {eurusd_av['rate']:.4f}</strong> (Alpha Vantage), soutenu par le taux BCE à 2,40%. Le <strong>USD/JPY recule à {usdjpy_av['rate']:.2f}</strong>, allégeant la pression sur la Banque du Japon.</p>",
            "categorie": "macro",
            "interconnexions": [
                {
                    "secteur": "Matières premières",
                    "impact": f"GLD {gld['change']:+.2f}%, USO {uso['change']:+.2f}% (Finnhub)",
                    "explication": "Le dollar fort pèse sur les matières premières dollar-denominated, notamment l'or."
                },
                {
                    "secteur": "Actions",
                    "impact": f"SPY {spy['change']:+.2f}%, AAPL {aapl['change']:+.2f}% (Finnhub)",
                    "explication": "La force du dollar réduit les bénéfices à l'international des multinationales américaines, pesant sur les valuations."
                }
            ],
            "regions": ["Amérique du Nord", "Europe", "Asie"],
            "severite": "info"
        }
    ]

    risk_radar = [
        {
            "risque": "Contagion de la correction tech aux indices larges",
            "severite": "urgent",
            "probabilite": "moyenne",
            "horizon": "court_terme",
            "impact_marche": "SPY sous 760 $, Nasdaq -3 à -5%, rotation vers obligations et or",
            "description": f"Tesla -{abs(tsla['change']):.2f}%, AAPL -{abs(aapl['change']):.2f}%, MSFT -{abs(msft['change']):.2f}%. Si la correction s'étend au reste du secteur, les indices larges pourraient suivre."
        },
        {
            "risque": "Blocage durable du détroit d'Ormuz",
            "severite": "urgent",
            "probabilite": "moyenne",
            "horizon": "court_terme",
            "impact_marche": "Pétrole >120 $, actions -5 à -10%, crypto -15%, volatilité spike",
            "description": "Trafic déjà sous 20 navires/jour. Un blocage complet déclencherait un choc énergétique mondial."
        },
        {
            "risque": "Surchauffe crypto et retracement technique",
            "severite": "attention",
            "probabilite": "moyenne",
            "horizon": "court_terme",
            "impact_marche": "BTC test 75 000 $, altcoins -10 à -20%, liquidations DeFi",
            "description": f"Fear & Greed à {fng}/100 après un rallye de 30 jours. Une consolidation technique reste probable."
        },
        {
            "risque": "Aplatissement de la courbe des taux US",
            "severite": "attention",
            "probabilite": "elevee",
            "horizon": "moyen_terme",
            "impact_marche": "Pression sur les banques régionales, immobilier, et actions à forte duration",
            "description": "Spread 10Y-2Y à 0,41% et en réduction. Un inversion complète signalerait un risque de récession."
        }
    ]

    themes_a_surveiller = [
        "Réunion Fed (prochaine décision taux — surveillance des communications)",
        "Résultats entreprises tech (Nvidia, Tesla, Apple) et segmentation sectorielle",
        "Trafic Ormuz et évolution du conflit Iran-US",
        "Fear & Greed Index crypto (seuil 75 comme zone de surchauffe)",
        "Dollar Index DXY au-dessus de 119 — risque pour les multinationales",
        "Spread 10Y-2Y et aplatissement de la courbe des taux",
    ]

    themes_disclaimer = "Ces thèmes sont identifiés à partir de l'analyse des données de marché et des flux d'actualités. Ils ne constituent pas des prédictions mais des facteurs de risque et d'opportunité à surveiller."

    agenda = [
        {"date": "2026-09-08", "evenement": "Indice manufacturier ISM US (août)", "impact": "Élevé", "source": "ISM"},
        {"date": "2026-09-10", "evenement": "Rapport sur l'emploi US (ADP, non-farm payrolls)", "impact": "Élevé", "source": "BLS"},
        {"date": "2026-09-11", "evenement": "Réunion BCE — décision de taux", "impact": "Élevé", "source": "ECB"},
        {"date": "2026-09-16", "evenement": "Indice des prix à la production US (PPI)", "impact": "Moyen", "source": "BLS"},
        {"date": "2026-09-17", "evenement": "Réunion FOMC — décision de taux Fed", "impact": "Très élevé", "source": "Fed"},
    ]

    sources_citees = [
        {"nom": "CoinGecko", "type": "api", "donnees_utilisees": "Prix crypto, market cap, dominance"},
        {"nom": "Finnhub", "type": "api", "donnees_utilisees": "Prix ETF (SPY, QQQ, DIA, GLD, USO) et actions (AAPL, MSFT, GOOGL, TSLA, NVDA)"},
        {"nom": "Alternative.me", "type": "api", "donnees_utilisees": "Fear & Greed Index crypto"},
        {"nom": "FRED (Federal Reserve Economic Data)", "type": "institution", "donnees_utilisees": "CPI, Fed Funds, PIB, chômage, Treasury 10Y, DXY, spread 10Y-2Y, M2, bilan Fed, taux hypothécaire"},
        {"nom": "ECB Data", "type": "institution", "donnees_utilisees": "Taux directeur BCE, EUR/USD fixing"},
        {"nom": "Alpha Vantage", "type": "api", "donnees_utilisees": "Forex EUR/USD, GBP/USD, USD/JPY"},
        {"nom": "Twelve Data", "type": "api", "donnees_utilisees": "DAX, EUR/GBP, EUR/CHF"},
        {"nom": "DefiLlama", "type": "api", "donnees_utilisees": "TVL DeFi, protocoles, yields"},
        {"nom": "Mempool.space", "type": "api", "donnees_utilisees": "Frais BTC, hashrate"},
        {"nom": "NewsAPI / GNews / RSS", "type": "presse", "donnees_utilisees": "Titres d'actualités géopolitiques, marchés, crypto, tech"},
    ]

    daily_briefing = {
        "date": DATE_STR,
        "generated_at": GENERATED_AT,
        "type": briefing_type,
        "model": "kimi",
        "sources_count": len(sources_citees),
        "sources_market": len(available),
        "signal_du_jour": signal_du_jour,
        "synthese": {
            "titre": "Correction tech sévère — Tesla et big tech sous pression, crypto en pause technique",
            "sous_titre": "Fear & Greed à 73/100 et DXY à 118,75 tandis que le secteur tech corrige fortement",
            "contenu": synthese_contenu
        },
        "signaux": signaux,
        "risk_radar": risk_radar,
        "themes_a_surveiller": themes_a_surveiller,
        "themes_disclaimer": themes_disclaimer,
        "agenda": agenda,
        "sentiment_global": global_tendance,
        "tags": ["tech", "correction", "tesla", "crypto", "fed", "dollar", "ormuz"],
        "sources_citees": sources_citees
    }

    # ── Sauvegardes ──
    save_json("sentiment.json", {
        "updated": GENERATED_AT,
        "date": DATE_STR,
        "global": {"score": global_score, "tendance": global_tendance, "resume": global_resume},
        "categories": sentiment_categories,
        "historique": historique,
        "model": "kimi",
        "mode": "consolidated"
    })

    save_json("alerts.json", {
        "updated": GENERATED_AT,
        "alertes": alertes,
        "stats": alert_stats,
        "model": "kimi",
        "mode": "consolidated"
    })

    save_json("macro-analysis.json", macro)
    save_json("market-briefing.json", market_briefing)
    save_json("daily-briefing.json", daily_briefing)

    # ── Archivage ──
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    archive_path = HISTORY_DIR / f"briefing-{DATE_STR}.json"
    with open(archive_path, "w", encoding="utf-8") as f:
        json.dump(daily_briefing, f, ensure_ascii=False, indent=2)
    print(f"  📦 Archive : {archive_path.name}")

    print("\n╔══════════════════════════════════════════════════╗")
    print("║  Briefing généré avec succès                     ║")
    print("╚══════════════════════════════════════════════════╝")
    print(f"  📊 Sentiment : {global_score:+.2f} ({global_tendance})")
    print(f"  🚨 Alertes : {len(alertes)} ({alert_stats['urgent']} urgent, {alert_stats['attention']} attention, {alert_stats['info']} info)")
    print(f"  🏦 Macro : {macro['titre']}")
    print(f"  📈 Briefing : {market_briefing['titre']}")

if __name__ == "__main__":
    main()
