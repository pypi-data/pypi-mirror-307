import Web_Component    from '../../core/Web_Component.mjs';
import CSS__Cards       from '../../css/CSS__Cards.mjs';
import CSS__Forms       from '../../css/CSS__Forms.mjs';
import CSS__Typography  from '../../css/CSS__Typography.mjs';
import Div              from '../../core/Div.mjs';
import H                from '../../core/H.mjs';
import Raw_Html         from "../../core/Raw_Html.mjs";
import CSS__Grid from "../../css/grid/CSS__Grid.mjs";

export default class WebC__Athena__Config extends Web_Component {
    load_attributes() {
        new CSS__Grid      (this).apply_framework()
        new CSS__Cards     (this).apply_framework()
        new CSS__Forms     (this).apply_framework()
        new CSS__Typography(this).apply_framework()

        this.channel = this.getAttribute('channel')
        this.show_system_prompt = localStorage.getItem('athena_show_system_prompt') === 'true'
        this.edit_mode = localStorage.getItem('athena_edit_mode') === 'true'
    }

    connectedCallback() {
        super.connectedCallback()
        this.add_event_listeners()
    }

    add_event_listeners() {
        this.shadowRoot.querySelector('#system-prompt-toggle')
            .addEventListener('change', this.handle_system_prompt_change.bind(this))

        this.shadowRoot.querySelector('#edit-mode-toggle')
            .addEventListener('change', this.handle_edit_mode_change.bind(this))
    }

    handle_system_prompt_change(event) {
        const show_system_prompt = event.target.checked
        localStorage.setItem('athena_show_system_prompt', show_system_prompt)
        this.dispatch_config_update()
    }

    handle_edit_mode_change(event) {
        const edit_mode = event.target.checked
        localStorage.setItem('athena_edit_mode', edit_mode)
        this.dispatch_config_update()
    }

    dispatch_config_update() {
        const event = new CustomEvent('config-update', {
            bubbles: true,
            composed: true,
            detail: {
                channel: this.channel,
                show_system_prompt: localStorage.getItem('athena_show_system_prompt') === 'true',
                edit_mode: localStorage.getItem('athena_edit_mode') === 'true'
            }
        })
        this.dispatchEvent(event)
    }

    render() {
        const card       = new Div({ class: 'card m-1 bg-light-cyan' })
        const body       = new Div({ class: 'card-body' })
        const title      = new H({ level: 3, class: 'card-title', value: 'Configuration' })
        const form       = new Raw_Html({ class: 'form-group' })

        const system_prompt_toggle = `
            <div class="mb-3">
                <div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" id="system-prompt-toggle"
                           ${this.show_system_prompt ? 'checked' : ''}>
                    <label class="form-check-label" for="system-prompt-toggle">
                        Show System Prompt
                    </label>
                </div>
            </div>`

        const edit_mode_toggle = `
            <div class="mb-3">
                <div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" id="edit-mode-toggle"
                           ${this.edit_mode ? 'checked' : ''}>
                    <label class="form-check-label" for="edit-mode-toggle">
                        Edit Mode
                    </label>
                </div>
            </div>`

        form.raw_html = system_prompt_toggle + edit_mode_toggle

        body      .add_elements(title, form)
        card      .add_element(body)

        this.set_inner_html(card.html())
    }
}

WebC__Athena__Config.define()