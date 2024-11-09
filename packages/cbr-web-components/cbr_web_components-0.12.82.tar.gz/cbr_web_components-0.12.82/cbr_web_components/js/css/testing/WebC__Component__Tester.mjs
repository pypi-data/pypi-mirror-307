import Web_Component   from '../../core/Web_Component.mjs';
import Button          from '../../core/Button.mjs';
import Div             from '../../core/Div.mjs';
import Input           from '../../core/Input.mjs';
import Label           from '../../core/Label.mjs';
import Select          from '../../core/Select.mjs';
import Option          from '../../core/Option.mjs';
import Icon            from '../icons/Icon.mjs';
import CSS__Forms      from '../CSS__Forms.mjs';
import CSS__Typography from '../CSS__Typography.mjs';
import CSS__Cards      from '../CSS__Cards.mjs';
import CSS__Buttons    from '../CSS__Buttons.mjs';
import CSS__Icons      from '../icons/CSS__Icons.mjs';
import CSS__Alerts     from '../CSS__Alerts.mjs';

export default class WebC__Component__Tester extends Web_Component {

    base_path = '/web_components/js/'
    presets = [ { label: 'User Session'       , path: 'cbr/session/WebC__CBR__User_Session.mjs'            },
                { label: 'Athena Examples'    , path: 'cbr/web_components/WebC__Athena__Examples.mjs'      },
                { label: 'Athena Welcome'     , path: 'cbr/web_components/WebC__Athena__Welcome.mjs'       },
                { label: 'Past Chats Welcome' , path: 'cbr/web_components/WebC__PastChats__Welcome.mjs'    }]

    load_attributes() {
        new CSS__Forms     (this).apply_framework()
        new CSS__Typography(this).apply_framework()
        new CSS__Cards     (this).apply_framework()
        new CSS__Buttons   (this).apply_framework()
        new CSS__Icons     (this).apply_framework()
        new CSS__Alerts    (this).apply_framework()
        this.script_path              = this.presets[0].path        // chose the first one
    }

    connectedCallback() {
        super.connectedCallback()
        this.build()
        this.setup_event_handlers()
    }

    build() {
        this.add_css_rules(this.css_rules())
        this.set_inner_html(this.html())
    }

    css_rules() {
        return {
            ".tester-container" : { display         : "flex"           ,        // Container for the whole component
                                    flexDirection   : "column"         ,
                                    gap            : "1rem"           },
            ".card"             : { padding         : "1.5rem"         },       // Card wrapper
            ".controls"         : { display         : "grid"           ,        // Controls section
                                    gap            : "1rem"           ,
                                    gridTemplateColumns: "1fr 1fr auto",
                                    marginBottom   : "1rem"           },
            ".path-input"       : { gridColumn      : "1 / -1"         },       // Script path input spans full width
            ".host-container"   : { backgroundColor : "var(--table-striped-bg)",// Container for tested component
                                    borderRadius    : "0.375rem"       ,
                                    padding        : "1.5rem"         ,
                                    minHeight      : "200px"          },
            ".load-indicator"   : { display         : "flex"           ,        // Loading indicator
                                    justifyContent  : "center"         ,
                                    alignItems      : "center"         ,
                                    height         : "100%"           },
            ".status-bar"       : { display         : "flex"           ,        // Status information
                                    justifyContent  : "space-between"  ,
                                    alignItems      : "center"         ,
                                    marginTop      : "1rem"           },
            ".status-text"      : { fontSize        : "0.875rem"       ,        // Status text
                                    color          : "var(--color-muted)" },
            ".auto-reload"      : { display        : "flex"     ,
                                    alignItems     : "center"   ,
                                    gap            : "0.5rem"   }
        }
    }

    html() {
        const container = new Div({ class: 'tester-container' })
        const card      = new Div({ class: 'card' })
        const controls  = new Div({ class: 'controls' })
        const input     = new Input({class: 'input path-input',  value: this.script_path})
        const select    = new Select({ class: 'input' })

        this.presets.forEach(preset => {
            select.add_element(new Option({ value: preset.path, text: preset.label }))
        })

        const refresh_btn   = new Button({ class: 'btn btn-primary',  title: 'Reload component'}).add_element(new Icon({icon: 'arrow-refresh', color: 'white', size: 'lg'}))
        const auto_reload   = new Div({ class: 'auto-reload' })
        const checkbox      = new Input({ type: 'checkbox',  id: 'auto-reload',  class: 'checkbox' })
        const label         = new Label({ for: 'auto-reload',  value: 'Reload on enter', class: 'checkbox-label'})
        const host          = new Div({ class: 'host-container',  id: 'component-host'})
        const status_bar    = new Div({ class: 'status-bar', id: 'status-bar'})

        auto_reload.add_elements(checkbox, label)
        controls   .add_elements(select, refresh_btn, auto_reload, input)
        card       .add_elements(controls, host, status_bar)
        container  .add_element (card)

        return container.html()
    }

    setup_event_handlers() {
        const path_input    = this.shadowRoot.querySelector('.path-input')
        const preset_select = this.shadowRoot.querySelector('select')
        const refresh_btn   = this.shadowRoot.querySelector('.btn-primary')
        const container     = this.shadowRoot.querySelector('.tester-container')
        const auto_reload   = this.shadowRoot.querySelector('#auto-reload')
        path_input.addEventListener('change', (e) => this.load_component(e.target.value))

        preset_select.addEventListener('change', (e) => {
            if (e.target.value) {
                path_input.value = e.target.value
                this.load_component(e.target.value)
            }
        })
        refresh_btn.addEventListener('click'     , () => this.refresh_component())
        container  .addEventListener('mouseenter', () => { if (auto_reload.checked) { this.refresh_component() }})

        this.refresh_component()
    }

    async load_component(component_path) {
        const path = this.base_path + component_path
        const host = this.shadowRoot.querySelector('#component-host')
        const timestamp = Date.now()
        try {
            this.script_path        = component_path
            const module            = await import(path + '?t=' + timestamp)
            const original_name     = this.get_component_name(module.default.name)              // we need to do this to break the current cache of the defined web-component
            const versioned_name    = `${original_name}-${timestamp}`
            customElements.define(versioned_name, module.default)
            host.innerHTML      = `<${versioned_name}></${versioned_name}>`
            this.update_status('Component loaded successfully', 'success')
        } catch (error) {
            console.error('Failed to load component:', error)
            this.show_error(error.message)
        }
    }

    get_component_name(class_name) {
        return class_name.replace(/_/g, '-')                                        // Replace underscores with hyphens
                         .replace(/--/g, '-')                                       // Clean up double hyphens
                         .toLowerCase()                                             // Convert to lowercase
    }

    refresh_component() {
        if (this.script_path) {
            this.load_component(this.script_path)
        }
    }

    show_error(message) {
        const host = this.shadowRoot.querySelector('#component-host')
        const error_div = new Div({ class: 'alert alert-error' })
                            .add_element(new Div({
                                class: 'alert-content',
                                value: `Error: ${message}`
                            }))

        host.innerHTML = error_div.html()
        this.update_status('Failed to load component', 'error')
    }

    update_status(message, type = 'info') {
        const status_bar    = this.shadowRoot.querySelector('#status-bar')
        const status_text   = new Div({ class: `status-text color-${type}`,  value: message })
        const timestamp     = new Div({ class: 'status-text', value: new Date().toLocaleTimeString() })

        status_bar.innerHTML = ''
        status_bar.appendChild(status_text.dom_create())
        status_bar.appendChild(timestamp  .dom_create())
    }
}

WebC__Component__Tester.define()