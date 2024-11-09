export default class CBR__Route__Handler {

    base_path = '/webc/cbr-webc-dev'

    constructor(component) {
        this.component = component
        this.setupEventListeners()
    }

    setupEventListeners() {
        // Listen for popstate events (browser back/forward)
        window.addEventListener('popstate', (event) => {
            this.handleRoute(window.location.pathname)
        })

        // Intercept navigation clicks
        document.addEventListener('click', (event) => {
            const path = event.composedPath();
            const link = path.find(el => el.tagName === 'A');

            if (link && link.href.startsWith(window.location.origin)) {
                if (link.href.includes('/web/') || link.href.includes('/athena/index#' )) {           // don't intercept links to other pages
                    return
                }
                event.preventDefault()
                const path = link.href.replace(window.location.origin, '')
                this.navigate(path)
            }
        })
    }

    navigate(path) {
        window.history.pushState({}, '', path)
        this.handleRoute(path)
    }

    async handleRoute(path) {
        const contentEl = this.component.shadowRoot.querySelector('#content')
        if (!contentEl) return

        const placeholder = contentEl

        const routePath = path.replace(this.base_path, '').replace(/^\/+/, '') || 'home'

        try {
            const content = await this.component.routeContent.fetch_content(routePath)
            placeholder.innerHTML = content
        } catch (error) {
            console.error('Error loading content:', error)
            placeholder.innerHTML = '<div class="content-error">Error loading content. Please try again.</div>'
        }
    }
}