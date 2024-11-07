import os


class AyehYab():

    def standard_text(self, text):
        text = (text.replace('\n', ' ')
                .replace('  ', ' ')
                .replace('ً', '')
                .replace('ٌ', '')
                .replace('ٍ', '')
                .replace('َ', '')
                .replace('ُ', '')
                .replace('ِ', '')
                .replace('ّ', '')
                .replace('ْ', '')
                .replace('ة', 'ه')
                .replace('ك', 'ک')
                .replace('ي', 'ی')
                .replace('ی', 'ی')
                .replace('ى', 'ی')
                .replace('ئ', 'ی')
                .replace('إ', 'ا')
                .replace('أ', 'ا')
                .replace('آ', 'ا')
                .replace('ء', 'ا')
                .replace('ؤ', 'و')
                .replace('.', '')
                .replace('؟', '')
                .replace('،', '')
                .replace('؛', '')
                .replace('-', '')
                .replace('_', '')
                .replace('(', '')
                .replace(')', '')
                .replace('{', '')
                .replace('}', '')
                .replace(']', '')
                .replace('[', '')
                .replace(']', '')
                .replace('[', '')
                .replace('»', '')
                .replace('«', '')
                .replace(':', '')
                .replace('"', '')
                .replace("'", '')
                .replace('\\', '')
                .replace('/', '')
                .replace('<', '')
                .replace('>', '')
                .replace('1', '')
                .replace('2', '')
                .replace('3', '')
                .replace('4', '')
                .replace('5', '')
                .replace('6', '')
                .replace('7', '')
                .replace('8', '')
                .replace('9', '')
                .replace('0', '')
                .replace('‏', '')
                )
        text = text.strip()
        return text

    def ayeh_find(self, text):
        quran_url = 'https://data.belquran.com/fa-IR/Quran/s/'
        ayeh_class = 'ayeh'
        paragrapg_mark = '</br>'

        current_dir = os.path.dirname(__file__)

        ayeh_ids = list(range(1, 6236))

        ayat_file = open(os.path.join(current_dir, "packages", "ayat.txt"), 'r', encoding='utf-8')
        ayat_list = ayat_file.readlines()
        ayat_list_text = '@'.join(ayat_list)
        ayat_list_text = ayat_list_text.replace('\n', '')
        ayat_list_text = self.standard_text(ayat_list_text)
        ayat_list = ayat_list_text.split('@')

        surehname_ayehnumber_file = open(os.path.join(current_dir, "packages", "surehname_ayehnumber.txt"), 'r',
                                         encoding='utf-8')
        surehname_ayehnumber_list = surehname_ayehnumber_file.readlines()
        surehname_ayehnumber_list = list(map(lambda x: x.replace("\n", ""), surehname_ayehnumber_list))

        surehnumber_ayehnumber_file = open(os.path.join(current_dir, "packages", "surehnumber_ayehnumber.txt"), 'r',
                                           encoding='utf-8')
        surehnumber_ayehnumber_list = surehnumber_ayehnumber_file.readlines()
        surehnumber_ayehnumber_list = list(map(lambda x: x.replace("\n", ""), surehnumber_ayehnumber_list))

        adress_ayeh_dict = dict(zip(ayeh_ids, surehname_ayehnumber_list))
        ayeh_link_dict = dict(zip(ayeh_ids, surehnumber_ayehnumber_list))

        ayeh_id = 0
        ayat_text = ''
        ayat_text_dict = {}  # حاوی ایندکس کاراکتر در رشته  ayat_text به عنوان کلید و ayehid به عنوان مقدار
        index_counter = 0
        # لیست قرآن را تبدیل به یک رشته میکند
        # ضمنا در یک دیکشنری به ازای هر index ، شماره آیه متناظرش را قرار میدهد(index کلید و ayehid مقدار است)
        for ayeh in ayat_list:
            ayat_text += ayeh + ' '
            ayeh_id += 1
            len_ayeh = len(ayeh) + 1
            for index in range(0, len_ayeh + 1):
                ayat_text_dict[index_counter + index] = ayeh_id
            index_counter += len_ayeh

        output = []
        # متن ورودی(فعلا باید یک پاراگراف باشد)

        rows = text
        if type(rows) == str:
            rows = [rows]
        if type(rows) != list: return ''
        rows_len = len(rows)
        # row = rows[0].replace('\n', '')
        for row in rows:
            row.replace('\n', '')
            if not row:
                output.append([])
                continue
            # لیستی از ایندکس های فاصله در متن ایجاد میکند ، 0 و ایندکس آخرین کاراکتر نیز در این لیست اضافه میشود
            # دلیل این کار این است که مرو در متن بر اساس فاصله ها باشد و نه بر اساس کاراکتر(کلمه مهم است و نه حروف)
            list_index = [0]
            for index in range(len(row)):
                if row[index] == ' ':
                    list_index.append(index)
            list_index.append(len(row))

            out = []
            start = 0
            start_index = 0
            end = len(list_index) - 1
            end_index = list_index[end]
            '''
            مرور در متن ورودی به این شکل است که از ابتدا تا انتهای متن در متن قرآن جستجو میشود
            اگر پیدا نشد یک space از انتها کم میشود و دوباره جستجو، اگر پیدا نشد دوباره و دوباره تا اینکه انتها به ابتدا میچسبد و یا اینکه یکی دو تا فاصله هنوز مانده باشد
            در این حالت انتها به انتهای متن ورودی میچسبد و ابتدا یکی بیشتر میشود و دوباره جستجو و اگر پیدا نشد یکی از انتها کم میشود
            تا اینکه ابتدا به انتها میچسبد و یا اینکه یکی دوتا هنوز به انتها مانده باشد که از حلقه خارج میشود
            (در هر جا ایندکس شروه یا پایان تغییر میکند و متن جدیدی از متن اصلی انتخاب میشود عملیات استانداردسازی انجام میشود)
            در هر کجا که پیدا شد ایندکس ابتدا و انتها متن در دیکشنری متن قرآن بررسی شده و ayehid آن که ممکن است یک یا چند آیه متوالی باشد استخراج میشود
            به همراه ایندکس در متن اصلی بدون استانداردسازی 
             البته اگر آیه پیدا شد از آنجاییکه ممکن است در جاهای مختلف قرآن آمده باشد، دوباره از آنجای قرآن به بعد دوباره جستجو میشود
            
            '''
            while start_index < end_index - 2:
                start_index = list_index[start]
                end_index = list_index[end]
                text = row[start_index:end_index]
                pure_text = self.standard_text(text)
                ayeh_ids = []
                if pure_text.count(' ') > 2 and len(pure_text) > 12 and pure_text in ayat_text:
                    i = 0
                    while True:
                        index0 = ayat_text.find(pure_text, i)
                        if index0 == -1:
                            break
                        index1 = index0 + len(pure_text) - 1
                        i = index1
                        ayehid0 = ayat_text_dict[index0]
                        ayehid1 = ayat_text_dict[index1]
                        ayeh_ids.append(",".join(map(str, range(ayehid0, ayehid1 + 1))))

                    ayeh_adress_text = []
                    link_ayeh = ''
                    if ayeh_ids:
                        for ayehid in ayeh_ids:
                            if ',' in ayehid:
                                ayehid = ayehid.split(',')
                                ayeh_adress_temp0 = adress_ayeh_dict.get(int(ayehid[0]))
                                ayeh_adress_temp1 = adress_ayeh_dict.get(int(ayehid[-1]))
                                if ayeh_adress_temp0 and ayeh_adress_temp1:
                                    ayeh_adress_text.append(ayeh_adress_temp0 + '-' + ayeh_adress_temp1)
                            else:
                                ayeh_adress_temp = adress_ayeh_dict.get(int(ayehid))
                                if ayeh_adress_temp:
                                    ayeh_adress_text.append(ayeh_adress_temp)
                        ayeh_adress_text = ', '.join(ayeh_adress_text)

                        ayeh_id_for_link = ayeh_ids[0]
                        if ',' in ayeh_id_for_link:
                            ayeh_id_for_link = ayeh_id_for_link.split(',')[0]
                        link_ayeh = quran_url + ayeh_link_dict.get(int(ayeh_id_for_link))

                    out.append({'ayehid': ayeh_ids,
                                'ayeh_text': row[start_index:end_index],
                                'index_start_end': (start_index, end_index),
                                'ayeh_adress_text': ayeh_adress_text,
                                'link_ayeh': link_ayeh,
                                })
                    start += pure_text.count(' ') + 1
                    end = len(list_index) - 1
                else:
                    if end < 2: break
                    end -= 1
                    if end <= start + 1:
                        end = len(list_index) - 1
                        start += 1
            output.append(out)

        html_output = []
        for index in range(rows_len):
            row = rows[index]
            output_items = output[index]
            if not output_items: continue
            for item in output_items[::-1]:
                start_index, end_index = item['index_start_end']
                ayehids = item["ayehid"]
                ayeh_adress_text = item["ayeh_adress_text"]
                link_ayeh = item["link_ayeh"]
                start_tag = f'<a href="{link_ayeh}" target="_blank" rel="noopener noreferrer" class="{ayeh_class}" ayeh_id="{str(ayehids)}" title="{ayeh_adress_text}">'
                end_tag = '</a>'
                row = row[:start_index] + start_tag + row[start_index:end_index] + end_tag + row[end_index:]

            html_output.append(row)
        html_output = f'{paragrapg_mark}'.join(html_output)
        return {
            'html_output': html_output,
            'list_output': output,
        }
