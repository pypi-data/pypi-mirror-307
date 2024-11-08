import Web_Component        from '../../core/Web_Component.mjs';
import Layout               from '../../css/grid/Layout.mjs';
import CSS__Grid            from '../../css/grid/CSS__Grid.mjs';
import CSS__Typography      from '../../css/CSS__Typography.mjs';
import CSS__Cards           from '../../css/CSS__Cards.mjs';
import H                    from '../../core/H.mjs';
import Div                  from '../../core/Div.mjs';
import Raw_Html             from '../../core/Raw_Html.mjs';
import API__Invoke          from '../../data/API__Invoke.mjs';

export default class WebC__Athena__Banner extends Web_Component {
    load_attributes() {
        new CSS__Grid       (this).apply_framework()
        new CSS__Typography (this).apply_framework()
        new CSS__Cards      (this).apply_framework()
        this.api_invoke = new API__Invoke()
    }

    async render() {
        const content = await this.load_content()

        const content_card = new Div     ({ class: 'card m-1'      })
        const content_body = new Div     ({ class: 'card-body' })
        const card_title   = new H       ({ level: 1,  class: 'card-title',  value: content?.metadata?.title})
        const card_text    = new Raw_Html({ class: 'card-text',  value: content?.html })
        content_card.add_element(content_body)
        content_body.add_elements(card_title , card_text)

        this.set_inner_html(content_card.html())
    }

    async load_content() {
        try {
            return await this.api_invoke.invoke_api(
                '/markdown/render/markdown-file-to-html-and-metadata?path=en/site/athena/banner.md',
                'GET'
            )
        } catch (error) {
            console.error('Error loading banner content:', error)
            return {
                html: '<p>Welcome to Athena</p>',
                metadata: { title: 'Athena' }
            }
        }
    }
}

WebC__Athena__Banner.define()