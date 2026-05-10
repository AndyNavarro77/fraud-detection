# 🔍 Detección de Fraude Financiero — Scoring de Riesgo en Tiempo Real

> **Pipeline end-to-end de detección de fraude que identifica el 97% de transacciones fraudulentas en 284K+ registros — combinando machine learning, optimización de threshold e impacto de negocio para generar $55.002 de beneficio neto.**

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0-red?logo=xgboost)](https://xgboost.ai)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4-orange?logo=scikitlearn)](https://scikit-learn.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql)](https://mysql.com)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?logo=powerbi)](https://powerbi.microsoft.com)
[![Estado](https://img.shields.io/badge/Estado-Completo-brightgreen)]()

---

## 🧠 El Problema de Negocio

Una empresa de pagos digitales procesa cientos de miles de transacciones por día. Solo el 0,17% son fraudulentas — pero ese pequeño porcentaje representa millones en pérdidas anuales por contracargos, costos operativos y daño reputacional.

El equipo de fraude no puede revisar cada transacción manualmente. Necesitan un sistema que:
- **Detecte fraude automáticamente** con alta precisión
- **Minimice falsos positivos** — bloquear una transacción legítima también tiene costo
- **Priorice alertas por nivel de riesgo** — para que el equipo se enfoque donde más importa
- **Cuantifique el impacto de negocio** — no solo métricas de modelo, sino dólares reales ahorrados

**Este proyecto construye ese sistema desde cero.**

---

## ✅ La Solución

Un pipeline completo de detección de fraude que entrena y compara tres modelos de machine learning sobre 284K+ transacciones reales de tarjetas de crédito, aplica SMOTE para manejar el desbalance extremo de clases (0,17% de fraude), optimiza el threshold de decisión para maximizar el valor de negocio, y entrega un dashboard de monitoreo de riesgo en tiempo real en Power BI.

> *De 284K transacciones brutas a un sistema de scoring de fraude listo para producción — detectando el 97% del fraude con solo 292 falsas alarmas y $55.002 de beneficio neto.*

---

## 📐 Arquitectura

```
┌─────────────────────┐    ┌──────────────────────┐    ┌─────────────────────┐
│  Credit Card Fraud  │───▶│  Pipeline ML Python  │───▶│     MySQL DB        │
│  (Dataset Kaggle)   │    │  EDA · SMOTE · Train │    │  3 tablas           │
│  284K transacc.     │    │  LR · RF · XGBoost   │    │  transactions       │
└─────────────────────┘    └──────────────────────┘    │  model_metrics      │
                                                        │  business_impact    │
                                                        └──────────┬──────────┘
                                                                   │
                                                    ┌──────────────▼──────────────┐
                                                    │  Dashboard Power BI Dark     │
                                                    │  Monitor de Riesgo en Tiempo │
                                                    └─────────────────────────────┘
```

---

## 🔄 Pipeline — Paso a Paso

| Paso | Acción | Tecnología | Valor de Negocio |
|------|--------|------------|------------------|
| 1 | EDA — desbalance, análisis de montos y tiempo | Python · pandas · seaborn | Entender patrones de comportamiento del fraude |
| 2 | Feature engineering — indicadores de riesgo | Python · pandas | Mejorar señal del modelo con variables de negocio |
| 3 | SMOTE — manejar tasa de fraude 0,17% | imbalanced-learn | Entrenar modelos con datos balanceados |
| 4 | Entrenar 3 modelos — LR, RF, XGBoost | scikit-learn · xgboost | Comparar enfoques interpretables vs ensemble |
| 5 | Optimización de threshold — maximizar beneficio | Python · pandas | Convertir métricas ML en decisiones de negocio |
| 6 | Cuantificación de impacto de negocio | Python · pandas | Traducir performance del modelo a dólares |
| 7 | Scoring de todas las transacciones por riesgo | Python · scikit-learn | Niveles de riesgo accionables para el equipo |
| 8 | Carga de datos a base de datos relacional | MySQL · SQLAlchemy | Modelo de datos escalable y consultable |
| 9 | Dashboard de monitoreo de riesgo en tiempo real | Power BI · DAX | Visibilidad operacional para analistas de fraude |

---

## 📊 Resultados Clave

| Métrica | Valor |
|---------|-------|
| Transacciones totales analizadas | 284.807 |
| Casos de fraude reales | 492 (0,17%) |
| Fraude detectado | **477 — 97,0% recall** |
| Falsas alarmas | 292 (0,10% tasa de falsos positivos) |
| Fraude no detectado | 15 |
| Fraude prevenido | $58.295 |
| Costo de revisión | $1.460 |
| **Beneficio neto** | **$55.002** |
| Mejor AUC-ROC | 0,9823 (Random Forest) |
| Threshold óptimo | 0,63 |

---

## 🤖 Comparación de Modelos

| Modelo | AUC-ROC | Avg Precision | Recall | Precision | F1 |
|-------|---------|---------------|--------|-----------|-----|
| Logistic Regression | 0,9697 | 0,7148 | 90,8% | 6,5% | 0,12 |
| Random Forest | 0,9823 | 0,7891 | 87,8% | 33,5% | 0,48 |
| **XGBoost** ★ | **0,9759** | **0,8240** | **84,7%** | **41,1%** | **0,55** |

> XGBoost seleccionado como modelo de producción — mejor balance entre precisión y recall, mayor F1 score y mejor Average Precision (0,824). Threshold optimizado en 0,63 para máximo beneficio de negocio.

---

## ⚠️ Desbalance de Clases — El Desafío Central

Con solo 0,17% de tasa de fraude, los modelos estándar entrenados sobre datos sin procesar simplemente predecirían "legítima" para todo y lograrían 99,83% de accuracy — completamente inútil para detección de fraude.

**Solución aplicada:**
- **SMOTE** aplicado solo al conjunto de entrenamiento — nunca al test set
- Ratio de fraude elevado de 0,17% a 9% en datos de entrenamiento
- Split estratificado para preservar distribución de clases
- Evaluación enfocada en Recall, Precision, AUC-ROC y Average Precision — no accuracy

---

## 🎯 Segmentación por Nivel de Riesgo

Todas las transacciones puntuadas y clasificadas en 4 niveles:

| Nivel de Riesgo | Transacciones | Tasa de Fraude | Score Promedio | Acción |
|-----------------|--------------|----------------|----------------|--------|
| Critical | 604 | **78,5%** | 0,974 | Bloqueo inmediato |
| High | 196 | 1,5% | 0,689 | Revisión prioritaria |
| Medium | 752 | 0,3% | 0,413 | Revisión estándar |
| Low | 283.255 | 0,0% | 0,006 | Aprobación automática |

> **Insight clave:** Cuando el modelo marca una transacción como Critical, acierta el 78,5% de las veces — una mejora de 455x sobre la tasa base de fraude.

---

## 🔍 Análisis en Detalle

**Análisis Exploratorio — Desbalance de Clases y Patrones de Transacciones**
![EDA Overview](img/eda_overview.png)
Distribución de clases mostrando el desbalance 99,83% vs 0,17%, análisis de montos revelando que el 73,6% de los fraudes son menores a $100, y scatter temporal mostrando fraude distribuido uniformemente en todas las horas.

**Evaluación de Modelos — Curvas ROC, Matrices de Confusión e Importancia de Features**
![Model Evaluation](img/model_evaluation.png)
Curvas ROC para los tres modelos (zoom en región crítica 0-10% FPR), matrices de confusión con desglose TP/FP/FN, comparación de performance y top 10 features de XGBoost — V14 y V4 dominan, con features engineered `Is_round_amount` e `Is_small_amount` en el top 10.

**Optimización de Threshold — Decisión Orientada al Negocio**
![Threshold Optimization](img/threshold_optimization.png)
Curvas Precision-Recall-F1 en todos los thresholds, curva de beneficio neto de negocio identificando threshold óptimo en 0,63, evolución TP/FP/FN, y desglose de impacto de negocio en threshold óptimo.

**Resumen Ejecutivo — Impacto de Negocio en Dataset Completo**
![Executive Summary](img/executive_summary.png)
Distribución por nivel de riesgo, tasa de fraude por nivel, cascada de impacto de negocio ($58K prevenido → $55K neto), comparación de modelos y tabla KPI con todas las métricas clave.

---

## 📊 Dashboard

**Monitor de Riesgo en Tiempo Real** — Dashboard Power BI en dark mode diseñado para equipos de analistas de fraude en sistemas de monitoreo en vivo.

![Fraud Risk Monitor](img/dashboard_fraud_monitor.png)

**Lo que muestra:**
- Cards KPI: Total de Transacciones · Fraude Detectado · Fraude No Detectado · Falsas Alarmas · Beneficio Neto
- Distribución de Fraud Score por Nivel de Riesgo (escala logarítmica)
- Impacto de Negocio ($) — prevenido vs no detectado vs costo de revisión vs beneficio neto
- Performance de Modelos — comparación AUC-ROC entre 3 modelos
- Tasa de Fraude por Nivel de Riesgo — 78,5% en nivel Critical
- Transacciones por Nivel de Riesgo — anillo de distribución

---

## 💡 Feature Engineering

Más allá de los features PCA anonimizados (V1-V28), se diseñaron los siguientes indicadores de riesgo orientados al negocio:

| Feature | Lógica | Señal de Fraude |
|---------|--------|----------------|
| `Amount_log` | Transformación logarítmica del monto | Reduce sesgo, mejora el modelo |
| `Amount_scaled` | Monto estandarizado | Normalizado para input del modelo |
| `Is_small_amount` | Monto < $10 | 2x mayor tasa de fraude |
| `Is_round_amount` | Monto % 1 == 0 | 1,9x mayor tasa de fraude |
| `Is_night` | Hora entre 22hs-6hs | Indicador de riesgo comportamental |

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología | Propósito |
|------|------------|-----------|
| Análisis | Python · pandas · numpy | Limpieza, EDA, feature engineering |
| Machine Learning | scikit-learn · XGBoost | Entrenamiento, evaluación y scoring |
| Manejo de desbalance | imbalanced-learn · SMOTE | Sobremuestreo sintético de clase minoritaria |
| Visualización | matplotlib · seaborn | Gráficos de análisis y evaluación |
| Base de datos | MySQL 8.0 · SQLAlchemy | Almacenamiento estructurado con tablas indexadas |
| ETL | Python · pymysql | Pipeline de carga automatizado |
| Dashboard | Power BI · DAX | Monitoreo de riesgo en tiempo real |

---

## 📁 Estructura del Repositorio

```
fraud-detection/
│
├── notebooks/
│   └── 01_fraud_detection.ipynb      # Pipeline ML completo: EDA, SMOTE, modelos, threshold
├── scripts/
│   └── load_to_mysql.py              # ETL: transacciones scored → MySQL
├── dashboard/
│   └── fraud_detection.pbix          # Dashboard Power BI dark mode
├── data/
│   └── creditcard.csv                # Dataset fuente (no incluido en git)
├── img/                              # Capturas de análisis y dashboard
├── .env.example                      # Plantilla de variables de entorno
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md                         # Versión en inglés
```

---

## 👤 Autor

**Andrés Navarro**
Analista de Datos · Machine Learning · Financial Analytics · Python · SQL

[![GitHub](https://img.shields.io/badge/GitHub-AndyNavarro77-black?logo=github)](https://github.com/AndyNavarro77)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Conectar-blue?logo=linkedin)](https://www.linkedin.com/in/andr%C3%A9s-navarro77/)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visitar-orange?logo=netlify)](https://andres-navarro-portfolio.netlify.app/)

---

*Desarrollado para demostrar capacidades de detección de fraude a nivel producción — manejo de desbalance de clases, comparación multi-modelo, optimización de threshold orientada al negocio y diseño de dashboard operacional — habilidades directamente aplicables a fintech, banca, e-commerce y cualquier entorno de riesgo orientado a datos.*