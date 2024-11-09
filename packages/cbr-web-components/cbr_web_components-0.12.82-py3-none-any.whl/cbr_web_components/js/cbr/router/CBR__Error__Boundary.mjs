export default class CBR__Error__Boundary {
    constructor() {
        this.defaultErrorMessage = 'An error occurred while loading the content.';
    }

    renderError(error) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-boundary';

        const errorContent = `
            <div class="error-container">
                <h2>Content Loading Error</h2>
                <p>${this._formatErrorMessage(error)}</p>
                <button onclick="window.location.reload()">Retry</button>
            </div>
        `;

        errorDiv.innerHTML = errorContent;
        return errorDiv;
    }

    _formatErrorMessage(error) {
        if (error.message) {
            // Strip any sensitive information from error message
            return error.message.replace(/https?:\/\/[^\s<>"]+/g, '[URL]');
        }
        return this.defaultErrorMessage;
    }

    static css_rules() {
        return {
            ".error-boundary": {
                padding: "2rem",
                textAlign: "center",
                color: "#721c24",
                backgroundColor: "#f8d7da",
                border: "1px solid #f5c6cb",
                borderRadius: "0.375rem"
            },
            ".error-container h2": {
                marginBottom: "1rem",
                color: "#721c24"
            },
            ".error-container button": {
                marginTop: "1rem",
                padding: "0.5rem 1rem",
                backgroundColor: "#dc3545",
                color: "white",
                border: "none",
                borderRadius: "0.25rem",
                cursor: "pointer"
            },
            ".error-container button:hover": {
                backgroundColor: "#c82333"
            }
        }
    }
}