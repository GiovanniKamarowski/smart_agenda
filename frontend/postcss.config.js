export default {
    // PostCSS processa CSS antes de ser enviado ao navegador
    // Tailwind usa PostCSS para gerar as classes CSS
    plugins: {
        // Tailwind CSS: framework de utilidade que gera classes CSS automaticamente
        tailwindcss: {},
        // Autoprefixer: adiciona prefixos de navegador automaticamente (ex: -webkit-, -moz-)
        autoprefixer: {},
    },
}
