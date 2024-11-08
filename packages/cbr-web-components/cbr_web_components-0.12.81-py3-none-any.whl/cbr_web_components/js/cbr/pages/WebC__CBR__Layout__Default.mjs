import Web_Component             from '../../core/Web_Component.mjs'
import Layout                    from '../../css/grid/Layout.mjs'
import CSS__Alerts               from "../../css/CSS__Alerts.mjs"
import CSS__Grid                 from '../../css/grid/CSS__Grid.mjs'
import CSS__Typography           from '../../css/CSS__Typography.mjs'
import CSS__Side_Menu            from "../../css/menus/CSS__Side_Menu.mjs"
import Left_Menu                 from "../../css/menus/Left_Menu.mjs"
import CBR__Left_Footer          from "../elements/CBR__Left_Footer.mjs"
import CBR__Top_Banner           from "../elements/CBR__Top_Banner.mjs"
import CBR__Left_Logo            from "../elements/CBR__Left_Logo.mjs"
import CBR__Important_Alert      from "../elements/CBR__Important_Alert.mjs"
import CBR__Content__Placeholder from "../elements/CBR__Content__Placeholder.mjs"
import CBR__Route__Handler       from "../router/CBR__Route__Handler.mjs"
import CBR__Route__Content       from "../router/CBR__Route__Content.mjs"
import CBR__Error__Boundary      from "../router/CBR__Error__Boundary.mjs";
import API__Invoke               from "../../data/API__Invoke.mjs";

export default class WebC__CBR__Layout__Default extends Web_Component {
    constructor() {
        super()
        this.routeContent   = new CBR__Route__Content()
        this.routeHandler   = new CBR__Route__Handler(this)
        this.api_invoke     = new API__Invoke()
    }

    load_attributes() {
        new CSS__Alerts              (this).apply_framework()
        new CSS__Grid                (this).apply_framework()
        new CSS__Typography          (this).apply_framework()
        new CSS__Side_Menu           (this).apply_framework()

        this.add_css_rules(CBR__Top_Banner          .css_rules())
        this.add_css_rules(CBR__Left_Footer         .css_rules())
        this.add_css_rules(CBR__Left_Logo           .css_rules())
        this.add_css_rules(CBR__Important_Alert     .css_rules())
        this.add_css_rules(CBR__Content__Placeholder.css_rules())
        this.add_css_rules(CBR__Error__Boundary     .css_rules())

        // Add new CSS rules for routing functionality
        this.add_css_rules({
            ".content-loader": {
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100%',
                fontSize: '1.2em',
                color: '#666'
            },
            ".content-error": {
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100%',
                color: '#ff0000',
                fontSize: '1.2em'
            },
            ".route-content": {
                padding: '20px'
            }
        })
    }

    async render() {
        let layout, row_banner, row_content

        layout      = new Layout({ id:'main-page', class: 'h-100vh p-0' })
        row_banner  = layout.add_row()
        row_content = layout.add_row({class: 'flex-fill flex-nowrap'                           })

        row_banner .add_col({ id: 'top-banner' , class: 'h-75px'                               })
        row_content.add_col({                    class: 'w-250px flex-column d-flex'           })
                   .add_col({ id: 'left-menu'  , class: 'flex-fill bg-white'                   }).parent()
                   .add_col({ id: 'left-footer', class: 'h-75px bg-light-gray'                 })
        row_content.add_col({ id: 'content'    , class: 'd-flex bg-light-gray m-1'             })

        layout.with_id('left-menu' ).add_tag({ tag: 'webc-api-side-menu'   })

        layout     .with_id('left-menu'  ).add_element(new CBR__Left_Logo  ()                                )
        layout     .with_id('left-menu'  ).add_element(new Left_Menu       ({ menu_items: this.menu_items()  }))
        layout     .with_id('left-menu'  ).add_element(new CBR__Important_Alert()                            )
        layout     .with_id('left-footer').add_element(new CBR__Left_Footer()                                )
        layout     .with_id('top-banner' ).add_element(new CBR__Top_Banner()                                 )
        layout     .with_id('content'    ).add_element(new CBR__Content__Placeholder()                       )

        this.set_inner_html(layout.html())

        // Handle initial route
        this.routeHandler.handleRoute(window.location.pathname)


    }

    menu_items() {                                                                                                  // todo: load this data from toml.json
        return  [{ icon: 'home'     , label: 'Home'           , href: '/webc/cbr-webc-dev/home/index'         },
                 { icon: 'robot'    , label: 'Athena'         , href: '/webc/cbr-webc-dev/athena/index'       },
                 { icon: 'profile'  , label: 'Profile'        , href: '/webc/cbr-webc-dev/profile/index'      },
                 { icon: 'history'  , label: 'Past Chats'     , href: '/webc/cbr-webc-dev/past-chats/index'   },
                 { icon: 'person'   , label: 'Personas'       , href: '/webc/cbr-webc-dev/personas/index'     },
                 { icon: 'chat'     , label: 'Chat with LLMs' , href: '/webc/cbr-webc-dev/chat/index'         },
                 { icon: 'docs'     , label: 'Docs'           , href: '/webc/cbr-webc-dev/docs/index'         }]
    }
}


WebC__CBR__Layout__Default.define()