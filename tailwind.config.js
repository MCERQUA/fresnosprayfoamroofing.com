/** Compiled-CSS config (WO-1) — theme mirrors the former inline Play-CDN config exactly. */
module.exports = {
  darkMode: "class",
  content: ["./site/**/*.html"],
  theme: {
    extend: {
      colors: {
        "surface-container": "#e6eeff", "outline": "#75777f", "surface-variant": "#d7e3f9",
        "on-surface": "#101c2c", "on-primary-fixed": "#041a3f", "on-primary-fixed-variant": "#34466d",
        "primary-container": "#0a1f44", "on-error-container": "#93000a", "secondary-fixed-dim": "#ffb3ad",
        "inverse-primary": "#b4c6f4", "surface-tint": "#4c5e86", "inverse-on-surface": "#eaf1ff",
        "secondary": "#bb001b", "surface-container-lowest": "#ffffff", "primary-fixed": "#d9e2ff",
        "inverse-surface": "#253141", "primary": "#00081e", "background": "#f8f9ff",
        "on-secondary-fixed-variant": "#930013", "surface-container-high": "#dde9ff",
        "secondary-container": "#e1252f", "on-tertiary-fixed-variant": "#44474a",
        "surface-container-low": "#eff4ff", "on-primary": "#ffffff", "outline-variant": "#c5c6cf",
        "surface-bright": "#f8f9ff", "surface-dim": "#cedbf0", "on-tertiary": "#ffffff",
        "error": "#ba1a1a", "on-secondary": "#ffffff", "on-surface-variant": "#44464e",
        "on-error": "#ffffff", "secondary-fixed": "#ffdad7", "error-container": "#ffdad6",
        "on-tertiary-fixed": "#191c1e", "surface-container-highest": "#d7e3f9",
        "tertiary-fixed-dim": "#c4c7ca", "tertiary-fixed": "#e0e3e6", "on-primary-container": "#7687b2",
        "tertiary": "#06090b", "on-background": "#101c2c", "surface": "#f8f9ff",
        "tertiary-container": "#1d2123", "primary-fixed-dim": "#b4c6f4",
        "on-secondary-container": "#fffbff", "on-tertiary-container": "#85888b",
        "on-secondary-fixed": "#410004",
      },
      borderRadius: { DEFAULT: "0.25rem", lg: "0.5rem", xl: "0.75rem", full: "9999px" },
      spacing: { "gutter": "24px", "base": "8px", "margin-mobile": "16px", "container-max": "1280px", "section-gap": "120px" },
      fontFamily: {
        "body-md": ["Hanken Grotesk"], "headline-lg": ["Archivo Narrow"], "body-lg": ["Hanken Grotesk"],
        "headline-xl": ["Archivo Narrow"], "label-caps": ["JetBrains Mono"], "headline-lg-mobile": ["Archivo Narrow"],
      },
      fontSize: {
        "body-md": ["16px", { lineHeight: "1.5", fontWeight: "400" }],
        "headline-lg": ["40px", { lineHeight: "1.2", fontWeight: "700" }],
        "body-lg": ["18px", { lineHeight: "1.6", fontWeight: "400" }],
        "headline-xl": ["64px", { lineHeight: "1.1", letterSpacing: "-0.02em", fontWeight: "700" }],
        "label-caps": ["12px", { lineHeight: "1.0", letterSpacing: "0.1em", fontWeight: "600" }],
        "headline-lg-mobile": ["32px", { lineHeight: "1.2", fontWeight: "700" }],
      },
    },
  },
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/container-queries")],
};
