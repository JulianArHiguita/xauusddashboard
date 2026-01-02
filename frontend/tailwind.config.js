/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                background: "#09090b", // Zinc 950
                "card": "#18181b", // Zinc 900
                "card-hover": "#27272a",
                primary: "#fbbf24", // Amber 400 (Gold)
                "primary-foreground": "#000000",
                secondary: "#27272a",
                destructive: "#ef4444", // Red 500
                success: "#22c55e", // Green 500
                muted: "#a1a1aa",
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            }
        },
    },
    plugins: [],
}
