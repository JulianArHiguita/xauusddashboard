import { ArrowUp, ArrowDown, Minus } from "lucide-react";
import clsx from "clsx";

interface SignalCardProps {
    signal: {
        recommendation: string;
        confidence: number;
        score: number;
        reasons: string[];
        price: number;
    };
}

export const SignalCard: React.FC<SignalCardProps> = ({ signal }) => {
    const { recommendation, confidence, reasons, price } = signal;

    const getColor = (rec: string) => {
        if (rec.includes("BUY")) return "text-green-500 border-green-500/50 bg-green-500/10";
        if (rec.includes("SELL")) return "text-red-500 border-red-500/50 bg-red-500/10";
        return "text-yellow-500 border-yellow-500/50 bg-yellow-500/10";
    };

    const Icon = recommendation.includes("BUY") ? ArrowUp : recommendation.includes("SELL") ? ArrowDown : Minus;

    return (
        <div className={clsx("glass-panel p-6 flex flex-col items-center justify-center border-2", getColor(recommendation))}>
            <h2 className="text-zinc-400 text-sm uppercase tracking-wider font-semibold mb-2">Recomendación</h2>
            <div className="flex items-center gap-3 mb-4">
                <Icon className="w-12 h-12" strokeWidth={3} />
                <span className="text-5xl font-black">{recommendation}</span>
            </div>

            <div className="flex items-center gap-2 mb-6">
                <span className="text-sm text-zinc-400">Confianza:</span>
                <div className="h-2 w-24 bg-zinc-700 rounded-full overflow-hidden">
                    <div
                        className="h-full bg-current transition-all duration-500"
                        style={{ width: `${confidence}%` }}
                    />
                </div>
                <span className="font-bold">{confidence}%</span>
            </div>

            <div className="w-full text-left bg-black/20 p-4 rounded-lg">
                <h3 className="text-xs font-bold text-zinc-500 uppercase mb-2">Factores Clave</h3>
                <ul className="text-sm space-y-1">
                    {reasons.slice(0, 4).map((r, i) => (
                        <li key={i} className="flex items-center gap-2">
                            <div className="w-1.5 h-1.5 rounded-full bg-zinc-500" />
                            {r}
                        </li>
                    ))}
                </ul>
            </div>

            <div className="mt-4 text-xs text-zinc-500">
                Basado en precio: <span className="text-zinc-300 font-mono">${price.toFixed(2)}</span>
            </div>
        </div>
    );
};
