import Web_Component    from '../../core/Web_Component.mjs';
import Layout          from '../../css/grid/Layout.mjs';
import CSS__Grid       from '../../css/grid/CSS__Grid.mjs';
import CSS__Typography from '../../css/CSS__Typography.mjs';
import CSS__Cards      from '../../css/CSS__Cards.mjs';
import API__Invoke     from '../../data/API__Invoke.mjs';
import Div             from '../../core/Div.mjs';
import H               from '../../core/H.mjs';

export default class WebC__Home__Container extends Web_Component {
    load_attributes() {
        new CSS__Grid      (this).apply_framework()
        new CSS__Typography(this).apply_framework()
        new CSS__Cards     (this).apply_framework()
        this.api_invoke = new API__Invoke()
    }

    async connectedCallback() {
        super.connectedCallback()
        await this.render()
    }

    create_video_section(title, url) {

        const container = new Div({ class: 'video-card card' })
        const body = new Div({ class: 'card-body p-0' })
        const title_div = new H({
            level: 3,
            class: 'video-title',
            value: title
        })

        // Video element wrapped in container for aspect ratio
        const video_container = new Div({ class: 'video-container' })
        const video = new Div({tag: 'video',
                              class: 'video-player',
                              controls: '',
                              width: '100%',
                              height: '275'})
        const source = new Div({tag: 'source', src: url,  type: 'video/mp4'})

        video          .add_element (source         )
        video_container.add_element (video          )
        body           .add_elements(video_container)
        container      .add_elements(title_div, body)

        return container
    }

    async render() {
        const layout = new Layout({ class: 'home-container' })

        // Welcome section
        const welcome = new Div({ class: 'welcome-section card mb-4 m-1' })
        welcome.add_tag({
            tag: 'webc-api-markdown-to-html',
            attributes: {
                'content-path': 'en/web-site/home-page/welcome.md',
                'apply-css': ''
            }
        })
        layout.add_element(welcome)

        // Videos section
        const videos_row = layout.add_row({ class: 'mb-4 m-1' })

        const video1_col = videos_row.add_col({ class: 'col-6' })
        video1_col.add_element(this.create_video_section(
            'An Introduction to The Cyber Boardroom',
            'https://470426667096-cbr.s3.eu-west-2.amazonaws.com/cbr_website_static/assets/videos/video-tcb__introduction__27-feb-2024.mp4'
        ))

        const video2_col = videos_row.add_col({ class: 'col-6' })
        video2_col.add_element(this.create_video_section(
            'Meet Athena, your GenAI Cyber Security Advisor',
            'https://470426667096-cbr.s3.eu-west-2.amazonaws.com/cbr_website_static/assets/videos/video-tcb__meet-athena__25-feb-2024.mp4'
        ))

        // Cards section
        const cards_row = layout.add_row({ class: 'mb-4' })

        const card1_col = cards_row.add_col({ class: 'col-6' })
        const div_card_1 = new Div({ class: 'cards-section' })
        div_card_1.add_tag({
            tag: 'webc-markdown-card',
            class: 'cards-section',
            'content-path': 'en/web-site/home-page/card-1.md',
            'apply-css': ''
        })
        card1_col.add_element(div_card_1)

        const card2_col = cards_row.add_col({ class: 'col-6' })
        const div_card_2 = new Div({ class: 'cards-section' })
        div_card_2.add_tag({
            tag: 'webc-markdown-card',
            attributes: {
                'content-path': 'en/web-site/home-page/card-2.md',
                'apply-css': ''
            }
        })
        card2_col.add_element(div_card_2)


        this.set_inner_html(layout.html())
        this.add_css_rules(this.css_rules())
    }

    css_rules() {
        return {
            ".home-container": {
                padding: "1rem"
            },
            ".welcome-section": {
                backgroundColor: "#ffffff",
                padding: "2rem",
                marginBottom: "2rem",
                borderRadius: "8px"
            },
            ".video-card": {
                backgroundColor: "#ffffff",
                borderRadius: "8px",
                overflow: "hidden",
                marginLeft: "10px",
                marginRight: "10px"
            },
            ".video-title": {
                padding: "1rem",
                margin: "0",
                fontSize: "1.2rem",
                fontWeight: "500"
            },
            ".video-container": {
                position: "relative",
                width: "100%",
                backgroundColor: "#f8f9fa"
            },
            ".video-player": {
                width: "100%",
                height: "auto"
            },
            ".cards-section": {
                marginLeft: "14px",
                marginRight: "21px"
            },
            // Remove card bottom margin on mobile
            "@media (max-width: 768px)": {
                ".card": {
                    marginBottom: "1rem"
                }
            }
        }
    }
}

WebC__Home__Container.define()