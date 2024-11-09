import Web_Component    from '../../core/Web_Component.mjs';
import CSS__Grid       from '../../css/grid/CSS__Grid.mjs';
import CSS__Typography from '../../css/CSS__Typography.mjs';
import CSS__Cards      from '../../css/CSS__Cards.mjs';
import API__Invoke     from '../../data/API__Invoke.mjs';
import H               from '../../core/H.mjs';
import Div             from '../../core/Div.mjs';

export default class WebC__Athena__Examples extends Web_Component {
    load_attributes() {
        new CSS__Grid      (this).apply_framework()
        new CSS__Typography(this).apply_framework()
        new CSS__Cards     (this).apply_framework()
        this.add_css_rules(this.css_rules())
        this.api_invoke = new API__Invoke()
        this.channel = this.getAttribute('channel') || null
    }

    async render() {
        const content = await this.load_content()

        // Container with title
        const container = new Div({class: 'm-1'})
        const title     = new H({ level: 2,
                                  value: content?.title || 'Prompt examples',
                                  class: 'mb-4 text-center' })
        container.add_element(title)

        // Add each example as a card
        content?.examples?.forEach(example => {const card = new Div({ class: 'card mb-3 example-card'})
            const card_body = new Div({ class: 'card-body text-center',  value: example })
            card.add_element(card_body)
            container.add_element(card)
        })

        this.set_inner_html(container.html())
        this.setup_event_handlers()
    }

    setup_event_handlers() {
        this.shadowRoot.querySelectorAll('.example-card').forEach(card => {
            card.addEventListener('click', () => this.handle_example_click(card))
        })
    }

    handle_example_click(card) {
        const example_text = card.querySelector('.card-body').textContent
        this.raise_example_event(example_text)
    }

    raise_example_event(example_text) {
        const event = this.create_input_message_event(example_text)
        window.dispatchEvent(event)
    }

    create_input_message_event(example_text) {
        return new CustomEvent('new_input_message', {
            bubbles: true,
            composed: true,
            detail: {
                channel: this.channel,
                user_prompt: example_text,
                images: []
            }
        })
    }

    async load_content() {
        try {
            const url = '/markdown/static_content/data-file?path=en/site/athena/questions.toml'
            return await this.api_invoke.invoke_api(url)
        } catch (error) {
            console.error('Error loading examples:', error)
            return {
                title: 'Prompt examples',
                examples: [
                    'Hello, what do you know about me?',
                    'What questions should I ask my CISO?',
                    'What is DORA?',
                    'What are my legal responsibilities?',
                    'What is the best way to learn more about cyber security?'
                ]
            }
        }
    }

    css_rules() {
        return {
            ".example-card": {
                cursor: "pointer",
                transition: "all 0.2s ease-in-out",
                backgroundColor: "#f8f9fa"
            },
            ".example-card:hover": {
                transform: "translateY(-2px)",
                boxShadow: "0 4px 6px rgba(0,0,0,0.1)"
            },
            ".mb-4": {
                marginBottom: "1.5rem"
            },
            ".mb-3": {
                marginBottom: "1rem"
            },
            ".text-center": {
                textAlign: "center"
            }
        }
    }
}

WebC__Athena__Examples.define()