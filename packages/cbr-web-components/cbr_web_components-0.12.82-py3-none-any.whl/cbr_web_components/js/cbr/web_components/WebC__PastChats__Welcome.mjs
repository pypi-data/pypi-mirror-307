import Web_Component    from '../../core/Web_Component.mjs';
import CSS__Cards      from '../../css/CSS__Cards.mjs';
import CSS__Typography from '../../css/CSS__Typography.mjs';
import CSS__Grid       from '../../css/grid/CSS__Grid.mjs';
import API__Invoke     from '../../data/API__Invoke.mjs';
import Div             from '../../core/Div.mjs';
import Raw_Html        from '../../core/Raw_Html.mjs';
import H               from '../../core/H.mjs';

export default class WebC__PastChats__Welcome extends Web_Component {
    load_attributes() {
        new CSS__Grid      (this).apply_framework()
        new CSS__Cards     (this).apply_framework()
        new CSS__Typography(this).apply_framework()
        this.api_invoke = new API__Invoke()
        this.welcome_message = ''
    }

    async connectedCallback() {
        super.connectedCallback()
        await this.generate_welcome()
        this.render()
    }

    async fetch_user_data() {
        try {
            const [profile, chats] = await Promise.all([
                this.api_invoke.invoke_api('/api/user-data/user/user-profile', 'GET'),
                this.api_invoke.invoke_api('/api/user-data/chats/chats', 'GET')
            ])
            return { profile, chats: chats.saved_chats || {} }
        } catch (error) {
            console.error('Error fetching data:', error)
            return null
        }
    }

    analyze_chat_history(chats) {
        // Extract key metrics and patterns
        const total_chats = Object.keys(chats).length
        const total_messages = Object.values(chats).reduce((sum, chat) => sum + (chat.history_size || 0), 0)
        const prompts = Object.values(chats).map(chat => chat.last_user_prompt).filter(Boolean)

        // Get unique topics (removing duplicates and empty values)
        const topics = [...new Set(prompts)].filter(Boolean)

        // Calculate total data size
        const total_prompts_size = Object.values(chats).reduce((sum, chat) => sum + (chat.prompts_size || 0), 0)
        const total_responses_size = Object.values(chats).reduce((sum, chat) => sum + (chat.responses_size || 0), 0)

        return {
            total_chats,
            total_messages,
            topics,
            total_prompts_size,
            total_responses_size
        }
    }

    async generate_welcome() {
        const data = await this.fetch_user_data()
        if (!data) return

        const { profile, chats } = data
        const analytics = this.analyze_chat_history(chats)

        const user_prompt = `Create a personalized welcome message for a user's chat history page. Here are the key statistics:
            - Total conversations: ${analytics.total_chats}
            - Total messages exchanged: ${analytics.total_messages}
            - Recent topics discussed: ${analytics.topics.slice(0, 3).join(', ')}
            - Total data exchanged: ${((analytics.total_prompts_size + analytics.total_responses_size) / 1024).toFixed(1)}KB

            Please create a friendly, engaging message that:
            1. Acknowledges their level of engagement
            2. References their recent topics of interest
            3. Encourages continued interaction
            Keep it concise (max 100 words) and conversational.`

        const system_prompt = `You are Athena, analyzing chat history for ${profile.first_name}. 
                             Focus on being encouraging and highlight the value of their conversations.
                             Your role is to help them understand their engagement patterns.`

        const path = '/api/llms/chat/completion'
        const payload = {
            chat_thread_id: this.random_uuid(),
            temperature: 0,
            user_prompt: user_prompt,
            images: [],
            system_prompts: [system_prompt],
            histories: [],
            user_data: {
                session_id: this.random_uuid(),
                selected_platform: 'Groq (Free)',
                selected_provider: '1. Meta',
                selected_model: "llama-3.1-70b-versatile"
            },
            stream: true
        }

        try {
            const response = await fetch(path, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            })

            const reader = response.body.getReader()
            const decoder = new TextDecoder('utf-8')

            let message = ''
            while (true) {
                const { value, done } = await reader.read()
                if (done) break

                const decoded_value = decoder.decode(value, { stream: true })
                const fixed_value = decoded_value.replace(/[\r\n]+/g, '')
                message += fixed_value
                this.show_message(message)
            }
        } catch (error) {
            console.error('Error generating welcome:', error)
        }
    }

    show_message(message) {
        const marked_message = marked.marked(message)
        this.welcome_message = marked_message
        this.render()
    }

    render() {
        const card = new Div({ class: 'card mb-4 m-1' })
        const body = new Div({ class: 'card-body' })
        const content = new Raw_Html({
            class: 'card-text welcome-message',
            value: this.welcome_message
        })

        body.add_element(content)
        card.add_element(body)

        this.set_inner_html(card.html())
        this.add_css_rules(this.css_rules())
    }

    css_rules() {
        return {
            ".card": {
                backgroundColor: "#ffffff",
                borderRadius: "8px"
            },
            ".welcome-message": {
                fontSize: "1.1rem",
                lineHeight: "1.5",
                color: "#2c3e50"
            },
            ".welcome-message p": {
                margin: "0"
            }
        }
    }
}

WebC__PastChats__Welcome.define()