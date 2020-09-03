#評論TSV改存TXT
with open ('./summary_reviews_raw/imdbreviews_f3_08.tsv','r',encoding='utf-8') as e:
    while True:
        text = e.readline().split('\t')
        try:
            with open('./imdb_reviews_OLD_txt/{}.txt'.format(str(text[0])), 'a', encoding='utf-8') as f:
                f.write(str(text[6]))
        except :
            pass
        if str(text[0]) == '':
            break

