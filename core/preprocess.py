import re
import os
from pyvi import ViTokenizer

sentiment_stopwords = ["ufeff", "+", "\"", "", ".", ",", "!", "%", "....", "...", ")", "(", "thì", "là", "và", "bị", "với",
                       "thế_nào", "?", "", "một_số", "mot_so", "thi", "la", "va", "bi", "voi", "trong",
                       "the_nao", " j ", "gì", "có", "pin", "giá", "j7pro", "chứ", "máy", "tôi", "của", "để", "ai",
                       "sản_phẩm", "j7", "thấy", "bản", "vì", "nên", "ace", "pubg", "j5", "ip7", "ip7+", "nhé", "nhe",
                       "nhé'", "như", "từ ", "vậy", "2h", "thui", "thôi", "bin`", "fb", "facebook", "youtube", "pr", "phải"
                       "khi", "triệu", "triệu'", "18tr", "fan", "xài", "lại", "chụp", "camera", "plus", "điện_thoại",
                       "tới", "web", "reset", "nguyên_đán", "s9", "j8", "màn_hình", "64gb", "tết", "nhân_viên"]

stopwords_dash = []
with open('core/stopwords-dash.txt', encoding='utf-8') as f:
    stopwords_dash = [t.replace("\n", "") for t in f.readlines()]


emotion_icons = {
    '😀': "positive", '😬': "positive", '😁': ' positive ', '😂': "positive ",
    '😃': "positive", '😄': "positive", '🤣': "positive", '😅': "positive", '😆': "positive", '😇': "positive",
    '😉': "positive", '😊': "positive",  '🙂': "positive", '🙃': "positive", '☺': "positive", '😋':' positive ',
    '😌': ' positive ', '😍': ' positive ', '😘': ' positive ', '😗': ' positive ', '😙': ' positive ',
    '😚': ' positive ', '🤪': ' positive ', '😜': ' positive ', '😝': ' positive ',
    '😛': ' positive ', '🤑': ' positive ', "😎": "positive", "🤓": "positive", '🧐': ' positive ', '🤠': ' positive ',
    "🤗": "positive", "🤡": "positive", "😏": "negative", "😶": "negative", "😐": "negative", "😑": "negative",
    "😒": "negative", "🙄": "negative", "🤨": "negative", "🤔": "negative", "🤫": "negative", '🤭': ' positive ',
    '🤥': ' negative ', '😳': ' positive ', '😞': ' negative ', '😟': ' negative ', '😠': ' negative ',
    '😡': ' negative ', '🤬': ' negative ', '😔': ' negative ', '😕': ' negative ',
    '🙁': ' negative ', '☹': ' negative ', "🤢": "negative", "🤧": "negative", '😴': ' positive ', '💤': ' positive ',
    "😈": "negative", "👿": "negative", "👹": "negative", "👺": "negative", "💩": "negative", "👻": "positive",
    "💀": "negative", "☠": "negative", "👽": "negative", "🤖": "positive", "🎃": "positive", '😺': ' positive ',
    '😸': ' positive ', '😹': ' positive ', '😻': ' positive ', '😼': ' positive ', '😽': ' positive ',
    '🙀': ' negative ', '😿': ' negative ', '😾': ' negative ', '👐': ' positive ',
    '🤲': ' positive ', '🙌': ' positive ', "👏": "positive", "🙏": "positive", '🤝': ' positive ', '👍': ' positive ',
    "👎": "negative", "👊": "positive", "✊": "positive", "🤛": "positive", "🤜": "positive", "🤞": "positive",
    "✌": "positive", "🤘": "positive", "🤟": "positive", "👌": "positive", "👈": "positive", '👉': ' positive ',
    '👆': ' positive ', '👇': ' positive ', '☝': ' positive ', '✋': ' positive ', '🤚': ' positive ',
    '🖐': ' positive ', '🖖': ' positive ', '👋': ' positive ', '🤙': ' positive ',
    '💪': ' positive ', '🖕': ' negative ', '✍': "positive", '🤳': "positive", '💅': ' positive ', '👄': ' positive ',
    '👅': "positive", '👂': "positive", '👃': "positive", '👁': "positive", '👀': "positive", '🧠': "positive",
    '👤': "negative", '👥': "negative", '🗣': "negative", '👶': "positive", '🧒': "positive", '👦': ' positive ',
    '👧': ' positive ', '🧑': ' positive ', '👨': ' negative ', '🧔': ' negative ', '👱‍♂️': ' positive ',
    '👩': ' positive ', '👱‍♀️': ' positive ', '️🧓': ' positive ', '👴': ' positive ',
    '👵': ' positive ', '👲': ' positive ', '👳‍♀️': "positive", '👳‍♂️': "positive", '🧕': ' positive ', '🤶': "positive ",
    '🎅': "positive", '👼': "positive", '👸': "positive", '🤴': "positive", '👰': "positive", '🤵‍♀️': "positive",
    '🤵': "positive", '🕴️‍♀️': "positive", '🕴': "positive", '🧙‍♀️': "positive", '🧙‍♂️': "positive", '🧝‍♀️': ' positive ',
    '🧝‍♂️': ' positive ', '🧚‍♀️': ' positive ', '🧚‍♂️': ' positive ', '🧞‍♀️': ' positive ', '🧞‍♂️': ' positive ',
    '🧜‍♀️': ' positive ', '🧜‍♂️': ' positive ', '🧛‍♀️': ' positive ', '🧛‍♂️': ' positive ',
    '🧟‍♀️': ' positive ', '🧟‍♂️': ' positive ', '🙇‍♀️': "positive", '🙇‍♂️': "positive", '💁‍♀️': ' positive ',
    '💁‍♂️': "positive ",  '🙅‍♀️': "negative", '🙅‍♂️': "negative", '🙆‍♀️': "positive", '🙆‍♂️': "positive",
    '🤷‍♀️': "negative", '🤷‍♂️': "negative", '🙋‍♀️': "positive", '🙋‍♂️': "positive", '🤦‍♀️': "negative",
    '🤦‍♂️': "negative", '🙎‍♀️': "positive", '🙎‍♂️': ' positive ',
    '🙍‍♀️': ' positive ', '🙍‍♂️': ' positive ', '💇‍♀️': ' positive ', '💇‍♂️': ' positive ', '💆‍♀️': ' positive ',
    '💆‍♂️': ' positive ', '🤰': ' positive ', '🤱': ' positive ', '🚶‍♀️': ' positive ',
    '🚶‍♂️': ' positive ', '🏃‍♀️': ' positive ', '🏃‍♂️': "positive", '👫': "positive", '👬': ' positive ',
    '👭': "positive ", '💑': "positive", '👩‍❤️‍👩': "positive", '👨‍❤️‍👨': "positive", '💏': "positive",
    '👩‍❤️‍💋‍👩': "positive", '👨‍❤️‍💋‍👨': "positive", '❤': "positive", '🧡': "positive", '💛': "positive",
    '💚': "positive", '💙': "positive", '💜': ' positive ', '🖤': ' positive ', '💔': ' negative ',
    '❣': ' positive ', '💕': ' positive ', '💞': ' positive ', '💓': ' positive ', '💗': ' positive ',
    '💖': ' positive ', '💘': ' positive ', '💝': ' positive ', '💟': ' positive ', '🌼': ' positive ',
    "🚫": "negative", 'like': ' positive', '💌': ' positive ', ':(': ' negative ', '?': ' ? ',
    '💯': ' positive ', '^^': ' positive ', ':((': ' negative ', '️🆗️': ' positive ', ':v': '  positive ',
    '=))': '  positive ', ':3': ' positive ', '❌': ' negative ', ';)': ' positive ','(y)': ' positive',
    '<3': ' positive ', ':))': ' negative ', ': ) )': ' positive ',
    '^ ^': 'positive', '^_^': 'positive', ':V': 'positive', ';))': 'positive', ': D': ' positive', ': P': 'positive',
    '= . =': 'negative', '=.=': 'negative', "=='": 'negative', '^ o ^': 'positive', '^o^': ' positive',
    'haizzz': 'negative', 'haiz': 'negative', 'haizz': 'negative', 'kkk': 'positive',
    'he he': ' positive ', 'hehe': ' positive ', 'hihi': ' positive ', 'haha': ' positive ',
    'hjhj': ' positive ', ' lol ': ' positive ', 'huhu': ' negative ', ' 4sao ': ' positive ', ' 5sao ': ' positive ',
    ' 1sao ': ' negative ', ' 2sao ': ' negative ', 'kaka': 'positive', 'ka ka': 'positive', 'ka ka ka': 'positive'

}

wrong_terms = {
    ' acc ': ' tài_khoản ', ' fb ': ' facebook ', ' ad ': ' admin ', ' ahbp ': ' anh_hùng_bàn_phím ',
    ' atsm ': ' ảo_tưởng_sức_mạnh ', ' avt ': ' ảnh_đại_diện ', ' ava ': ' ảnh_đại_diện',' ac ': ' anh_chị ',
    ' bb ': ' tạm_biệt ',  ' bla bla ': ' vân_vân ', ' bsvv ': ' buổi_sáng_vui_vẻ ', ' bùng ': ' không_trả_tiền',
    ' fa ': ' cô_đơn ', ' nn ': ' ngủ_ngon ', ' pr ': ' quảng_cáo ',' bn ': ' bao_nhiêu ',
    ' pp ': ' tạm_biệt ',  ' bth ': ' bình_thường ', ' bt ': ' biết ',' cute ': ' dễ_thương ',
    ' chs ': ' chả_hiểu_sao ', ' cmt ': ' bình_luận ', ' ccmnr ': ' chuẩn ', ' đhn ': ' đéo_hiểu_nỗi ',
    ' đhs ': ' đéo_hiểu_sao ', ' g9 ': ' ngủ_ngon ', ' hpbd ': ' sinh_nhật_vui_vẻ ',
    ' snvv': ' sinh_nhật_vui_vẻ ', ' ib ': ' nhắn_tin_riêng ', ' kb ': ' kết_bạn ', ' sml ': ' sấp_mặt_luôn ',
    ' dz ': ' đẹp_trai ',' dth ': ' dễ_thương ', ' dt ': ' dễ_thương ',  ' ex ': ' người_yêu_cũ ',
    ' klq ': ' không_liên_quan ', ' mem ': ' thành_viên ', ' mng ': ' mọi_người ', ' mn ': ' mọi_người ',
    ' nx ': ' nhận_xét ', ' nyc ': ' người_yêu_cũ ', ' omg ': ' oh_my_god ', ' ps ': ' ghi_chú ',
    ' qtqđ ': ' quá_trời_quá_đát ', ' rep ': ' trả_lời ', ' scđ ': ' sao_cũng_được ', ' ố cê ': ' ok ',
    ' stt ': ' trạng_thái ', ' sub ': ' phụ_đề ', ' tag ': ' gắn_thẻ ', ' tđn ': ' thế_đéo_nào ',
    ' troll ': ' chơi_khăm ', ' vs ': ' với ', ' ny ': ' người_yêu ', ' plz ': ' năn_nỉ ', ' app ': ' ứng_dụng ',
    ' nt ': ' nhắn_tin ', ' trc ': ' trước ',  ' t ': ' tôi ', ' m ': ' mình ',
    ' cs ': ' cuộc_sống ', ' ố kê ': ' ok ', ' kp ': ' không_phải ', ' ô cê ': ' ok ', ' giề ': ' gì ',
    ' zth ': ' dễ_thương ', ' ô kêi ': ' ok ', ' okie ': ' ok ', ' o kê ': ' ok ', ' okey ': ' ok ', ' ôkê ': ' ok ',
    ' oki ': ' ok ', ' ote ':  ' ok ', ' okay ': ' ok ', ' okê ': ' ok ', ' oke ': ' ok ', ' ố sì kê ': ' ok ',
    ' khong ': ' không ', ' not ': ' không ', ' kh ': ' không ', ' kô ': ' không ', ' hok ': ' hông ',
    ' ko ': ' không ', ' hk ': ' hông ', ' k ': ' không ',  ' gút gút ': ' tốt ',
    'kg ': ' không ', 'not': ' không ', ' kg ': ' không ', ' "k ': ' không ',
    'kô': ' không ', 'hok': ' không ', '"ko ': ' không ',' mik ': ' mình ', ' mìn ': ' mình', ' mềnh ': ' mình ',
    'khong': ' không ', ' mk ': ' mình ', ' wá ': ' quá ', ' qá ': ' quá ', ' tẹc vời ': ' tuyệt_vời ', ' tiệc dời ': ' tuyệt_vời ',
    ' tẹc zời ': ' tuyệt_vời ', ' đc ': ' được ', ' dc ': ' được ', ' j ': ' gì ',
    ' nv ': ' nhân_viên ', ' sv ': ' sinh_viên ', ' hs ': ' học_sinh ', ' đt ': ' điện_thoại ', ' ng ': ' người ',
    ' màng hình ': ' màn_hình ', ' màn hìn ': 'màn_hình', ' tet ': ' kiểm_tra ', ' test ': ' kiểm_tra ',
    ' tét ': ' kiểm_tra ', ' sg ': ' sài_gòn ', ' nvien ': ' nhân_viên ', ' siu ': ' siêu ', ' pải ': ' phải ',
    ' fai ': ' phải ', ' fải ': ' phải ', ' ph ': ' phải ', ' h ': ' giờ ', ' sd ': ' sử_dụng ',
    ' of ': ' của ', ' kon ': ' con ', ' way ': ' quay ', ' s ': ' sao ', ' cã ': ' cả ', ' v ': ' vậy ',
    ' r ': ' rồi ', ' kiu ': ' kêu ', ' tl ': ' trả_lời ', ' thik ': 'thích', ' thíc ': 'thích', ' ns ': ' nói ',
    ' nviên ': ' nhân_viên ', ' nhiu ': ' nhiêu ', ' oder ': ' gọi_món ', ' ỏder ': 'gọi_món', ' hỉu ': ' hiểu ',
    ' film ': 'phim', ' phin ': ' phim ', ' fim ': ' phim ', ' nh ': ' nhưng ', ' hnay ': ' hôm_nay ',
    ' nhìu ': 'nhiều', ' qay ': ' quay ', ' nc ': ' nói_chuyện ', ' nch ': ' nói_chuyện ', ' tp ': ' thành_phố ',
    ' lun ': ' luôn ', ' rất tiết ': ' rất_tiếc ', ' rất tiêc ': ' rất_tiếc ', ' toẹt zời ': ' tuyệt_vời ',
    ' thất zọng ': ' thất_vọng ', ' thất dọng ': ' thất_vọng ', ' nhưg ': ' nhưng ', ' ms ': ' mới ',
    ' so ciu ': ' dễ_thương ', ' iu ': ' yêu ', ' hn ': ' hôm_nay '
}


def load_list(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = [ViTokenizer.tokenize(t.replace("\n", "")) for t in f.readlines()]
    return text


pos_list = load_list("core/pos.txt")
neg_list = load_list("core/neg.txt")
not_list = load_list("core/not.txt")
neutral_list = load_list("core/neutral.txt")

s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'


class VietnameseProcess:
    def __init__(self, sentence):
        self.sentence = sentence

    def tokenize(self):
        sentence = ViTokenizer.tokenize(self.sentence)
        self.sentence = ' ' + sentence + ' '

    def lowercase(self):
        self.sentence = self.sentence.lower()

    def remove_stopwords(self):
        self.sentence = ' ' + self.sentence + ' '
        for w in stopwords_dash:
            #self.sentence = self.sentence.replace("%s " % w, " ")
            self.sentence = self.sentence.replace(" %s " % w, " ")
        for w in sentiment_stopwords:
            self.sentence = self.sentence.replace(" %s " % w, " ")

    def remove_URLs(self):
        self.sentence = re.split('http\S+', self.sentence)
        self.sentence = " ".join(self.sentence)

    def replace_wrong_terms(self):
        self.sentence = ' ' + self.sentence + ' '
        for key, value in wrong_terms.items():
            if self.sentence.find(key) >= 0:
                self.sentence = self.sentence.replace(key, value)

    def remove_repeated_characters(self):
        self.sentence = re.sub(r'([A-Z\s])\1+', lambda m: m.group(1), self.sentence, flags=re.IGNORECASE)

    def remove_punctuation(self):
        """
        Remove all of the special characters in the sentence

        :return: the sentence after removing the special characters
        """
        punctuation = """!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~"""
        translator = str.maketrans(punctuation, ' ' * len(punctuation))

        self.sentence = self.sentence.translate(translator)

    def replace_emotion(self):
        for key, value in emotion_icons.items():
            if self.sentence.find(key) >= 0:
                self.sentence = self.sentence.replace(key, value)

    def remove_numbers(self):
        self.sentence = re.split('[0-9]+', self.sentence)
        self.sentence = " ".join(self.sentence)

    def replace_not_terms(self):
        text = re.split("\s*[\s,;]\s*", self.sentence)
        for idx in range(len(text)):
            if idx < len(text)-1 and text[idx] in not_list:
                if text[idx+1] in pos_list:
                    text[idx] = "notpositive"
                    text[idx+1] = ""
                if text[idx+1] in neg_list:
                    text[idx] = "notnegative"
                    text[idx+1] = ""
            elif text[idx] not in not_list:
                if text[idx] in pos_list:
                    text.append(" positive ")
                elif text[idx] in neg_list:
                    text.append(" negative ")

        self.sentence = " ".join(text)

    def remove_punctuation2(self):
        result = ''
        for c in self.sentence:
            result += s0[s1.index(c)] if c in s1 else c

        self.sentence = result

    def split_attached_words(self):
        self.sentence = " ".join(re.findall('[A-Z][^A-Z]*', self.sentence))

    def progress(self):
        self.remove_URLs()
        self.replace_emotion()
        self.remove_punctuation()
        self.lowercase()
        self.tokenize()
        self.remove_numbers()
        self.remove_repeated_characters()
        self.replace_wrong_terms()
        self.replace_not_terms()
        # self.remove_stopwords()

    def progress_DBSCAN(self):
        self.remove_URLs()
        self.replace_emotion()
        self.remove_punctuation()
        self.lowercase()
        self.tokenize()
        self.remove_numbers()
        self.remove_repeated_characters()
        self.replace_wrong_terms()
        self.replace_not_terms()
        self.remove_stopwords()
