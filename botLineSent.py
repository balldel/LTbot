from linebot import LineBotApi
from linebot.models import TextSendMessage,TemplateSendMessage,ImageCarouselTemplate,ImageCarouselColumn,PostbackTemplateAction,ImagemapSendMessage,BaseSize,URIImagemapAction,ImagemapArea,MessageImagemapAction,URITemplateAction
from linebot.exceptions import LineBotApiError

line_bot_api = LineBotApi('fSDjokoamI2lnlDZE8GJ2+PoZBn8DHsDba8zCtW57zR++3X+Iiy5jwtMQFB1oynrcHd3pU4g5S3IikMXzTmCkPueLieW/ilvst42POA6I6cyt/+z3u13OPxjof+Jq12l046ITxA2+sSMC95uRwEdHQdB04t89/1O/w1cDnyilFU=')

try:
    # imagemap_message = ImagemapSendMessage(
    #     base_url='https://s.isanook.com/me/0/ud/6/30677/adidasxpharrellwilliamsnm.jpg',
    #     alt_text='this is an imagemap',
    #     base_size=BaseSize(height=1040, width=1040),
    #     actions=[
    #         URIImagemapAction(
    #             link_uri='https://example.com/',
    #             area=ImagemapArea(
    #                 x=0, y=0, width=520, height=1040
    #             )
    #         ),
    #         MessageImagemapAction(
    #             text='hello',
    #             area=ImagemapArea(
    #                 x=520, y=0, width=520, height=1040
    #             )
    #         )
    #     ]
    # )
    product1 =  ImageCarouselColumn(
                    image_url='https://freitag.rokka.io/neo-grid-2/933f62c0d35879c8156efca76c04f464c1de77c7/000002023230-7-0-uz.jpg',
                    action=URITemplateAction(
                        label='JOE',
                        uri='https://www.freitag.ch/en/f17%20?productID=418548',
                    )
                )
    product2 = ImageCarouselColumn(
                    image_url='https://freitag.rokka.io/neo-grid-2/eff05028b47afc7f01311dc226c5938f000b6618/000002038147-7-0-uz.jpg',
                    action=URITemplateAction(
                        label='DRAGNET',
                        uri='https://www.freitag.ch/en/f12?productID=443346',
                    )
                )
    newProduct = [product1,product2]
    image_carousel_template_message = TemplateSendMessage(
        alt_text='ImageCarousel template',
        template=ImageCarouselTemplate(
            columns= newProduct
        )
    )
    line_bot_api.push_message('U9d261d005044ab0f2cba21b69278a155', image_carousel_template_message)
    print('Done')
except LineBotApiError as e:
    print(e.error)
    pass