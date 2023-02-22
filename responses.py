import random

aleatorio = ['https://media.discordapp.net/attachments/812336837405835295/981714863804010566/unknown.png',
             'https://media.discordapp.net/attachments/812336837405835295/930216241568813076/unknown.png',
             'https://media.discordapp.net/attachments/812336837405835295/900787980749406258/unknown.png',
             'https://media.discordapp.net/attachments/812336837405835295/869802618074062858/unknown.png',
             'https://media.discordapp.net/attachments/812336837405835295/981714813635952701/unknown.png',
             'https://media.discordapp.net/attachments/812336837405835295/869802193027494000/unknown.png',
             'https://cdn.discordapp.com/attachments/812336837405835295/866205591456972850/YBF9Fd_hZkYT-O6f.mp4',
             'https://cdn.discordapp.com/attachments/812336837405835295/866205363896713216/2p71KwIbUkQDIeLu.mp4',
             'https://media.discordapp.net/attachments/781660586618257470/860668730828652574/a6903bb3-763d-410d-ac02-34620262fa65.png',
             'https://cdn.discordapp.com/attachments/812336837405835295/858927876825284639/tPa5A4SwH9FaWEVo.mp4',
             'https://media.discordapp.net/attachments/812336837405835295/854236075358945290/unknown.png',
             'https://cdn.discordapp.com/attachments/812336837405835295/854230645647998986/gato.mp4',
             'https://media.discordapp.net/attachments/812336837405835295/854227337524936745/20200222_115330.jpg',
             'https://media.discordapp.net/attachments/812336837405835295/854227221974351892/20200108_163944.jpg?width=497&height=662',
             'https://media.discordapp.net/attachments/812336837405835295/854225928262516756/20190503_165203.jpg?width=884&height=663',
             'https://media.discordapp.net/attachments/812336837405835295/854224034778316810/IMG-20181102-WA0022.jpg?width=372&height=662',
             'https://media.discordapp.net/attachments/812336837405835295/854222111270633512/IMG-20180905-WA0029.jpg',
             'https://media.discordapp.net/attachments/812336837405835295/854216807338344448/IMG-20180104-WA0000.jpg',
             'https://media.discordapp.net/attachments/812336837405835295/854216424619638844/IMG-20190117-WA0011.jpeg?width=372&height=662',
             'https://media.discordapp.net/attachments/812336837405835295/854215538993659904/IMG-20180219-WA0049.jpg',
             'https://media.discordapp.net/attachments/812336837405835295/854214813077340160/IMG-20170717-WA0001.jpg?width=373&height=662',
             'https://media.discordapp.net/attachments/812336837405835295/854214648155602974/SPOILER_Screenshot_20181107-124530_WhatsApp.jpg',
             'https://media.discordapp.net/attachments/812336837405835295/854214429436936192/Screenshot_20180722-093647_WhatsApp.jpg',
             'https://media.discordapp.net/attachments/812336837405835295/854213627190837278/IMG-20181015-WA0009.jpg?width=373&height=662',
             'https://cdn.discordapp.com/attachments/812336837405835295/854212827350958080/invadiramacasadogustavo.mp4',
             'https://media.discordapp.net/attachments/812336837405835294/852385140847542293/unknown.png',
             'https://media.discordapp.net/attachments/812336837405835295/849876367301410816/unknown.png?width=474&height=663',
             'https://media.discordapp.net/attachments/812336837405835295/830232267225563143/IMG-20181109-WA0007.png?width=373&height=662',
             'https://media.discordapp.net/attachments/812336837405835295/830231778206810172/unknown.png',
             'https://media.discordapp.net/attachments/812336837405835295/830231726177124352/unknown.png?width=855&height=663',
             'https://cdn.discordapp.com/attachments/812336837405835295/830231676725887007/video-1582070899.mp4',
             'https://cdn.discordapp.com/attachments/812336837405835295/830231665077911613/50106208_313519859267720_2684224778973216768_n.mp4',
             'https://www.youtube.com/watch?v=pKc-YvuwdMI Comentarios',
             'https://www.youtube.com/watch?v=XTkXLqX2e7Y',
             'https://www.youtube.com/watch?v=Llpii85mzBo&ab_channel=KSAT12',
             'https://media.discordapp.net/attachments/812336837405835295/830228591165964358/IMG-20180412-WA0068.png?width=494&height=663',
             'https://media.discordapp.net/attachments/812336837405835295/830228574497013810/IMG-20170919-WA0005.png?width=372&height=662',
             'https://media.discordapp.net/attachments/812336837405835295/830228516125016094/IMG-20180425-WA0008.png',
             'https://cdn.discordapp.com/attachments/812336837405835295/830228316341796874/103789772_268944407762949_4507133784994496465_n.mp4',
             'https://media.discordapp.net/attachments/812336837405835295/830225642401693726/IMG-20180426-WA0063.png?width=372&height=662',
             'https://media.discordapp.net/attachments/812336837405835295/830225593655492681/IMG-20180706-WA0034.png?width=372&height=662',
             'https://cdn.discordapp.com/attachments/812336837405835295/830225439317295104/WhatsApp_Video_2020-11-16_at_01.59.38.mp4',
             'https://media.discordapp.net/attachments/812336837405835295/828160544367706112/unknown.png?width=748&height=662',
             'https://media.discordapp.net/attachments/812336837405835295/813483458813755412/Eu2hg6sWYAErOfD.png?width=1184&height=663',
             'https://www.youtube.com/watch?v=dO0FQUMQhPY',
             'https://cdn.discordapp.com/attachments/794662340154490930/1066217374308638720/chogathmago.mp4',
             'https://cdn.discordapp.com/attachments/794662340154490930/1066217105868996719/foxxin_slowmotion.mp4',
             'https://cdn.discordapp.com/attachments/794662340154490930/1066216989669998682/JabaioV2.mp4',
             'https://cdn.discordapp.com/attachments/794662340154490930/1066216989078597682/suamaequandoontemanoite.mp4',
             'https://cdn.discordapp.com/attachments/794662340154490930/1066217690898903050/TAPAO.mp4',
             'https://cdn.discordapp.com/attachments/812336837405835294/1066224130904576020/WhatsApp_Video_2023-01-21_at_02.13.52.mp4',
             'https://media.discordapp.net/attachments/735944232874934392/1070124862955327568/20230122_012910.jpg?width=497&height=662',
             'https://cdn.discordapp.com/attachments/735944232874934392/1070875659066409091/image.png',

             ]


def handle_response(choice) -> str:
    if choice == "vid":
        while True:
            link = random.choice(aleatorio)
            if ".mp4" not in link:
                continue
            else:
                return link
    elif choice == "img":
        while True:
            link = random.choice(aleatorio)
            if ".mp4" not in link or "youtube" not in link:
                return link
            else:
                continue
    else:
        return random.choice(aleatorio)
