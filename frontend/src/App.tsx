import { useEffect, useState } from "react";
import axios from "axios";
import { ChartWidget } from "./components/ChartWidget";
import { SignalCard } from "./components/SignalCard";
import { Activity, AlertTriangle, RefreshCw, Layers, TrendingUp, BarChart3 } from "lucide-react";

function App() {
    const [timeframe, setTimeframe] = useState("1h");
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [activeTab, setActiveTab] = useState<"chart" | "analysis">("chart");

    const fetchData = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`http://127.0.0.1:8000/api/analysis?timeframe=${timeframe}`);
            if (response.data.error) {
                setError(response.data.error);
            } else {
                setData(response.data);
                setError("");
            }
        } catch (err) {
            setError("Fallo al conectar con el servidor");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 60000); // Poll every minute
        return () => clearInterval(interval);
    }, [timeframe]);

    return (
        <div className="min-h-screen p-4 md:p-8 flex flex-col gap-6 max-w-[1600px] mx-auto">
            {/* Header */}
            <header className="flex flex-col md:flex-row justify-between items-center glass-panel p-6">
                <div>
                    <h1 className="text-3xl font-black text-primary tracking-tight">XAU/USD PRO</h1>
                    <p className="text-zinc-400 text-sm">Análisis de Oro en Tiempo Real</p>
                </div>

                <div className="flex items-center gap-4 mt-4 md:mt-0">
                    <div className="flex bg-zinc-900 rounded-lg p-1 border border-zinc-700">
                        {["5m", "15m", "1h"].map((tf) => (
                            <button
                                key={tf}
                                onClick={() => setTimeframe(tf)}
                                className={`px-4 py-1.5 rounded-md text-sm font-bold transition-all ${timeframe === tf
                                    ? "bg-zinc-700 text-white shadow-sm"
                                    : "text-zinc-500 hover:text-zinc-300"
                                    }`}
                            >
                                {tf.toUpperCase()}
                            </button>
                        ))}
                    </div>
                    <button onClick={fetchData} className="p-2 hover:bg-zinc-800 rounded-full transition-colors">
                        <RefreshCw className={`w-5 h-5 text-zinc-400 ${loading ? "animate-spin" : ""}`} />
                    </button>
                </div>
            </header>

            {/* Main Grid */}
            <main className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1">

                {/* Left Column - Chart/Analysis */}
                <div className="lg:col-span-2 flex flex-col gap-6">
                    {/* Tab Selector */}
                    <div className="flex gap-2">
                        <button
                            onClick={() => setActiveTab("chart")}
                            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-bold transition-all ${activeTab === "chart"
                                    ? "bg-zinc-800 text-white"
                                    : "text-zinc-500 hover:text-zinc-300"
                                }`}
                        >
                            <TrendingUp className="w-4 h-4" />
                            Gráfica
                        </button>
                        <button
                            onClick={() => setActiveTab("analysis")}
                            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-bold transition-all ${activeTab === "analysis"
                                    ? "bg-zinc-800 text-white"
                                    : "text-zinc-500 hover:text-zinc-300"
                                }`}
                        >
                            <BarChart3 className="w-4 h-4" />
                            Análisis Detallado
                        </button>
                    </div>

                    {/* Chart View */}
                    {activeTab === "chart" && (
                        <div className="glass-panel p-1 relative overflow-hidden flex-1 min-h-[500px]">
                            {data ? (
                                <ChartWidget data={data.chart_data} />
                            ) : (
                                <div className="absolute inset-0 flex items-center justify-center text-zinc-500">
                                    {error || "Cargando datos del mercado..."}
                                </div>
                            )}
                        </div>
                    )}

                    {/* Analysis View */}
                    {activeTab === "analysis" && data && (
                        <div className="glass-panel p-6 flex-1">
                            <h2 className="text-2xl font-bold text-primary mb-6">¿Por qué esta recomendación?</h2>

                            <div className="space-y-6">
                                {/* Signal Breakdown */}
                                <div>
                                    <h3 className="text-lg font-bold text-zinc-300 mb-3">Desglose de Señal</h3>
                                    <div className="bg-zinc-900/50 p-4 rounded-lg space-y-2">
                                        <div className="flex justify-between">
                                            <span className="text-zinc-400">Recomendación:</span>
                                            <span className={`font-bold ${data.signal.recommendation.includes("BUY") ? "text-green-500" :
                                                    data.signal.recommendation.includes("SELL") ? "text-red-500" :
                                                        "text-yellow-500"
                                                }`}>{data.signal.recommendation}</span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span className="text-zinc-400">Confianza:</span>
                                            <span className="font-bold text-white">{data.signal.confidence}%</span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span className="text-zinc-400">Puntuación técnica:</span>
                                            <span className="font-bold text-white">{data.signal.score.toFixed(1)}</span>
                                        </div>
                                    </div>
                                </div>

                                {/* Indicators Explanation */}
                                <div>
                                    <h3 className="text-lg font-bold text-zinc-300 mb-3">Indicadores Técnicos</h3>
                                    <div className="space-y-3">
                                        <div className="bg-zinc-900/50 p-4 rounded-lg">
                                            <div className="flex justify-between items-center mb-2">
                                                <span className="font-bold text-zinc-200">RSI (14)</span>
                                                <span className={`font-mono font-bold ${data.signal.rsi > 70 ? "text-red-500" :
                                                        data.signal.rsi < 30 ? "text-green-500" :
                                                            "text-zinc-300"
                                                    }`}>{data.signal.rsi.toFixed(2)}</span>
                                            </div>
                                            <p className="text-sm text-zinc-400">
                                                {data.signal.rsi > 70 ? "⚠️ Sobrecompra - Posible corrección a la baja" :
                                                    data.signal.rsi < 30 ? "✅ Sobreventa - Posible rebote alcista" :
                                                        "➡️ Zona neutral - Sin señal clara"}
                                            </p>
                                        </div>

                                        <div className="bg-zinc-900/50 p-4 rounded-lg">
                                            <div className="flex justify-between items-center mb-2">
                                                <span className="font-bold text-zinc-200">Precio Actual</span>
                                                <span className="font-mono font-bold text-primary">${data.signal.price.toFixed(2)}</span>
                                            </div>
                                            <p className="text-sm text-zinc-400">
                                                Precio de referencia para cálculos de SL/TP
                                            </p>
                                        </div>
                                    </div>
                                </div>

                                {/* Reasons */}
                                <div>
                                    <h3 className="text-lg font-bold text-zinc-300 mb-3">Razones Principales</h3>
                                    <ul className="space-y-2">
                                        {data.signal.reasons.map((reason: string, idx: number) => (
                                            <li key={idx} className="flex items-start gap-3 bg-zinc-900/50 p-3 rounded-lg">
                                                <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                                                    <span className="text-primary text-xs font-bold">{idx + 1}</span>
                                                </div>
                                                <span className="text-zinc-300">{reason}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>

                                {/* Risk Warning */}
                                <div className="border border-yellow-900/30 bg-yellow-900/5 p-4 rounded-lg">
                                    <p className="text-xs text-yellow-600/80 leading-relaxed">
                                        💡 <strong>Nota:</strong> Esta recomendación se basa en análisis técnico automatizado.
                                        Siempre considera múltiples factores antes de tomar decisiones de trading.
                                    </p>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Risk Management Bar */}
                    {data && data.risk_management && (
                        <div className="glass-panel p-6 flex flex-wrap gap-8 items-center justify-between">
                            <div className="flex items-center gap-3">
                                <div className="bg-blue-500/20 p-2 rounded-lg">
                                    <Layers className="text-blue-500 w-6 h-6" />
                                </div>
                                <div>
                                    <div className="text-xs text-zinc-400 uppercase font-bold">Gestión de Riesgo</div>
                                    <div className="text-sm text-zinc-300">Niveles Sugeridos</div>
                                </div>
                            </div>

                            <div className="flex gap-8">
                                <div>
                                    <div className="text-xs text-zinc-500 mb-1">STOP LOSS</div>
                                    <div className="text-xl font-mono text-red-500 font-bold">{data.risk_management.stop_loss}</div>
                                </div>
                                <div>
                                    <div className="text-xs text-zinc-500 mb-1">TAKE PROFIT</div>
                                    <div className="text-xl font-mono text-green-500 font-bold">{data.risk_management.take_profit}</div>
                                </div>
                                <div className="hidden md:block border-l border-zinc-800 pl-8">
                                    <div className="text-xs text-zinc-500 mb-1">RATIO R:R</div>
                                    <div className="text-xl font-mono text-white font-bold">{data.risk_management.risk_reward_ratio}</div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                {/* Right Column - Stats & Signals */}
                <div className="flex flex-col gap-6">
                    {data && data.signal && (
                        <SignalCard signal={data.signal} />
                    )}

                    <div className="glass-panel p-6 flex-1">
                        <h3 className="flex items-center gap-2 text-zinc-300 font-bold mb-6">
                            <Activity className="w-5 h-5 text-zinc-500" />
                            Indicadores Clave
                        </h3>

                        {data && (
                            <div className="space-y-4">
                                <div className="flex justify-between items-center p-3 bg-zinc-900/50 rounded-lg">
                                    <span className="text-zinc-400 text-sm">RSI (14)</span>
                                    <span className={`font-mono font-bold ${data.signal.rsi > 70 || data.signal.rsi < 30 ? 'text-primary' : 'text-zinc-300'}`}>
                                        {data.signal.rsi.toFixed(2)}
                                    </span>
                                </div>
                                <div className="flex justify-between items-center p-3 bg-zinc-900/50 rounded-lg">
                                    <span className="text-zinc-400 text-sm">Volatilidad (ATR)</span>
                                    <span className="font-mono font-bold text-zinc-300">
                                        Alta
                                    </span>
                                </div>
                            </div>
                        )}
                    </div>

                    <div className="p-4 border border-yellow-900/30 bg-yellow-900/5 rounded-xl flex gap-3 items-start">
                        <AlertTriangle className="w-5 h-5 text-yellow-600 shrink-0 mt-0.5" />
                        <p className="text-xs text-yellow-600/80 leading-relaxed">
                            <strong>Descargo:</strong> Este dashboard es solo para fines educativos. El trading de XAUUSD conlleva alto riesgo. Las señales "COMPRAR" y "VENDER" son generadas por algoritmos y no deben tomarse como asesoría financiera.
                        </p>
                    </div>
                </div>
            </main>
        </div>
    );
}

export default App;
