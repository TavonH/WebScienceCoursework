import emoji

#USE THE SAME NUMBER OF EMOJIS IN EACH EMOJI LEXICON, WHICH IS 6

class emoji_list():
    excitement_emoji = [emoji.emojize(':laughing:', use_aliases=True), emoji.emojize(':satisfied:', use_aliases=True),
                        emoji.emojize(':heart_eyes:', use_aliases=True), emoji.emojize(':heart_eyes_cat:', use_aliases=True),
                        emoji.emojize(':stuck_out_tongue_closed_eyes:', use_aliases=True), emoji.emojize(':stuck_out_tongue_winking_eye:', use_aliases=True)]

    happy_emoji = [emoji.emojize(':smile:', use_aliases=True), emoji.emojize(':smiley:', use_aliases=True),
                   emoji.emojize(':grin:', use_aliases=True), emoji.emojize(':joy:', use_aliases=True),
                   emoji.emojize(':wink:', use_aliases=True), emoji.emojize(':heart:', use_aliases=True)]

    pleasant_emoji = [emoji.emojize(':blush:', use_aliases=True), emoji.emojize(':relaxed:', use_aliases=True),
                      emoji.emojize(':relieved:', use_aliases=True), emoji.emojize(':sun_with_face:', use_aliases=True),
                      emoji.emojize(':sunny:', use_aliases=True), emoji.emojize(':four_leaf_clover:', use_aliases=True)]

    surprise_emoji = [emoji.emojize(':flushed:', use_aliases=True), emoji.emojize(':frowning:', use_aliases=True),
                      emoji.emojize(':anguished:', use_aliases=True), emoji.emojize(':exclamation:', use_aliases=True),
                      emoji.emojize(':shit:', use_aliases=True), emoji.emojize(':open_mouth:', use_aliases=True)]

    fear_emoji = [emoji.emojize(':worried:', use_aliases=True), emoji.emojize(':scream:', use_aliases=True),
                  emoji.emojize(':scream_cat:', use_aliases=True), emoji.emojize(':fearful:', use_aliases=True),
                  emoji.emojize(':skull:', use_aliases=True), emoji.emojize(':cold_sweat:', use_aliases=True)]

    angry_emoji = [emoji.emojize(':angry:', use_aliases=True), emoji.emojize(':rage:', use_aliases=True),
                   emoji.emojize(':triumph:', use_aliases=True), emoji.emojize(':imp:', use_aliases=True),
                   emoji.emojize(':anger:', use_aliases=True), emoji.emojize(':fire:', use_aliases=True)]
    total_emoji = excitement_emoji + happy_emoji + pleasant_emoji + surprise_emoji + fear_emoji + angry_emoji


#USE THE SAME NUMBER OF TERMS IN EACH EMOTION LEXICON, WHICH IS 10

class emotion_lexicon():
    #Emotion lexicon used as hash tags. (positive)
    excitement = ['#excitement', '#exciting', '#amazing', '#passion', '#thrill',
                  '#exhilaration', '#heat', '#inspiring', '#moving', '#sensational',
                  emoji.emojize(':laughing:', use_aliases=True)]
    #'happy' includes 'joy', 'love'. (positive)
    happy = ["#happy", '#happiness', '#glad', '#love', '#cheer', '#cheerful', '#joy',
             '#delighted', '#joyful', '#lovely',
             emoji.emojize(':grin:', use_aliases=True)]
    #'pleasant' is a positive feeling. (positive)
    pleasant = ['#pleasant', '#pleasing', '#welcome', '#nice', '#pleasurable',
                '#comfortable', '#comfort', '#relax', '#relaxing', '#relaxed',
                emoji.emojize(':blush:', use_aliases=True)]
    #'surprise' is a negative feeling, and it includes 'sad', 'frustration'. (negative)
    surprise = ['#surprise', '#down', '#tragic', '#sad', '#tense', '#sorry',
                '#frustration', '#frustrated', '#disappointed', '#pathetic',
                emoji.emojize(':flushed:', use_aliases=True)]
    #'fear' includes 'disgust', 'depression'. (negative)
    fear = ['#fear', '#disgust', '#horror', '#horrible', '#dread', '#panic',
            '#terror', '#terrible', '#fright', '#frighten', emoji.emojize(':scream:', use_aliases=True)]
    #'angry'. (negative)
    angry = ['#angry', '#furious', '#mad', '#annoyed', '#pissed', '#mood', '#provoked',
             '#raging', '#infuriated', '#wrathful', emoji.emojize(':rage:', use_aliases=True)]
    #total emotion words
    total = excitement + happy + pleasant + surprise + fear + angry

class emotion_lexicon_tuple():
    excitement = ['excitement', 'exciting', 'amazing', 'passion', 'thrill',
                  'exhilaration', 'heat', 'inspiring', 'moving', 'sensational']
    happy = ['happy', 'happiness', 'glad', 'love', 'cheer', 'cheerful', 'joy',
             'delighted', 'joyful', 'lovely']
    pleasant = ['pleasant', 'pleasing', 'welcome', 'nice', 'pleasurable',
                'comfortable', 'comfort', 'relax', 'relaxing', 'relaxed']
    surprise = ['surprise', 'down', 'tragic', 'sad', 'tense', 'sorry',
                'frustration', 'frustrated', 'disappointed', 'pathetic']
    fear = ['fear', 'disgust', 'horror', 'horrible', 'dread', 'panic',
            'terror', 'terrible', 'fright', 'frighten']
    angry = ['angry', 'furious', 'mad', 'annoyed', 'pissed', 'mood', 'provoked',
             'raging', 'infuriated', 'wrathful']

    total = [excitement, happy, pleasant, surprise, fear, angry]
    emo = emoji_list()
    total_emoji = [emo.excitement_emoji, emo.happy_emoji, emo.pleasant_emoji, emo.surprise_emoji, emo.fear_emoji, emo.angry_emoji]