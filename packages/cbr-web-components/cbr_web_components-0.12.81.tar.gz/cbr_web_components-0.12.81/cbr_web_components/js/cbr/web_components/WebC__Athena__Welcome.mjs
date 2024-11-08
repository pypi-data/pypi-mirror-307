import Web_Component    from '../../core/Web_Component.mjs';
import CSS__Cards      from '../../css/CSS__Cards.mjs';
import CSS__Typography from '../../css/CSS__Typography.mjs';
import API__Invoke     from '../../data/API__Invoke.mjs';
import Div             from '../../core/Div.mjs';
import Raw_Html        from '../../core/Raw_Html.mjs';
import H               from '../../core/H.mjs';
import CSS__Grid       from "../../css/grid/CSS__Grid.mjs";
import CBR__Session__Event__Handler from "../session/CBR__Session__Event__Handler.mjs";

export default class WebC__Athena__Welcome extends Web_Component {
    load_attributes() {
        new CSS__Grid      (this).apply_framework()
        new CSS__Cards     (this).apply_framework()
        new CSS__Typography(this).apply_framework()
        this.event_handler = new CBR__Session__Event__Handler()
        this.api_invoke    = new API__Invoke()
        this.welcome_message = ''
    }

    async connectedCallback() {
        super.connectedCallback()
        await this.generate_welcome()
        this.render()
        this.setup_event_listeners()
    }

    async fetch_user_data() {
        try {
            return await this.api_invoke.invoke_api('/api/user-data/user/user-profile', 'GET')
        } catch (error) {
            console.error('Error fetching user data:', error)
            return null
        }
    }

    async generate_welcome() {
        const user_data     = await this.fetch_user_data()
        const user_prompt   = "Generate a one-paragraph (max 100 words) personalized welcome message for this user, based on their profile preferences. " +
                              "reply as if speaking directly to the user, don't start your answer with quotes "
        const system_prompt = `You are called Athena, here is what you know about this user: ${JSON.stringify(user_data)}`

        if (!user_data) return

        //const path = '/api/open_ai/prompt_with_system__stream'
        const path     = '/api/llms/chat/completion'
        const platform = 'Groq (Free)'
        const provider = '1. Meta'
        const model    = "llama-3.1-70b-versatile"
        const payload = {
            chat_thread_id: this.random_uuid(),
            temperature: 0,
            user_prompt: user_prompt,
            images: [],
            system_prompts: [system_prompt],
            histories: [],
            user_data: { session_id: this.random_uuid() ,
                         selected_platform: platform,
                         selected_provider : provider ,
                         selected_model    : model
            },
            stream: true
        }


        try {
            const response = await fetch(path, {method: 'POST', headers: { 'Accept': 'application/json',  'Content-Type': 'application/json' },
                                                body : JSON.stringify(payload) })
            const reader = response.body.getReader();                     // Handling the stream
            const decoder = new TextDecoder('utf-8');
            let { value, done } = await reader.read();
            let message = '';
            let decoded_value = ''
            let fixed_value = ''
            while (!done) {
                decoded_value = decoder.decode(value, { stream: true });
                fixed_value   = decoded_value.replace(/[\r\n]+/g, '')
                message      += fixed_value;
                ({ value, done } = await reader.read());
                this.show_message(message)
            }
            message += decoder.decode();
            this.show_message(message)

        } catch (error) {
            console.error('Error generating welcome:', error)
        }
    }

    handle__active_session_changed = async () => {
        await this.generate_welcome()
    }
    setup_event_listeners() {
        this.event_handler.subscribe(this.event_handler.events.ACTIVE_SESSION_CHANGED, this.handle__active_session_changed)
    }
    show_message(message) {
        const marked_message = marked.marked(message)
        this.welcome_message = marked_message
        this.render()
    }

    render() {
        const card = new Div({ class: 'card h-100 m-1' })
        const body = new Div({ class: 'card-body' })
        //const title = new H({ level: 3, class: 'card-title mb-3', value: 'Welcome' })
        const content = new Raw_Html({ class: 'card-text', value: this.welcome_message })

        body.add_elements(content)
        card.add_element(body)

        this.set_inner_html(card.html())
    }
}

WebC__Athena__Welcome.define()