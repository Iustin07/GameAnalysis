import json
import nltk
from nltk import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from arms_processing_data.game import Game
snow_stemmer = SnowballStemmer(language='english')

def load_json():
    games=[]
    with open('data/sample.json', 'r') as fcc_file:
        fcc_data = json.load(fcc_file)
        for data in fcc_data:
            print(data)
            g=Game(data["id"],data["title"],data["description"],data["review"],data["developer"],data["publisher"],data["category"])
            games.append(g)
    return games
def write_into_json_dictionary(path,dictionary):
    with open(path, "w") as outfile:
        json.dump(dictionary, outfile,indent=2)

def tokenize(games_list:list):

    adj_group={}
    nouns_group={}
    for game in games_list:
        sentence = game.description
        universals=pos_tag(word_tokenize(sentence), tagset="universal")

        for tag in universals:
            base_form = snow_stemmer.stem(tag[0].lower()) # pentru forme de baza ale cuvintelor
            #base_form=tag[0].lower() #extragere normala: cu pluraluri si derivari
            if tag[1]=='NOUN':
                if base_form not in nouns_group.keys():
                    nouns_group[base_form]=[]
                    nouns_group[base_form].append(game.id)
                elif game.id not in nouns_group[base_form]:
                    nouns_group[base_form].append(game.id)
            elif tag[1]=='ADJ':
                if base_form not in adj_group.keys():
                    adj_group[base_form]=[]
                    adj_group[base_form].append(game.id)
                elif game.id not in adj_group[base_form]:#apare duplicat daca apare de mai multe ori in descriere
                    adj_group[base_form].append(game.id)
    write_into_json_dictionary("data/nouns.json", nouns_group)
    counts=get_frequencies(nouns_group)
    write_into_json_dictionary("data/nouns_frequency.json", counts)
    write_into_json_dictionary("data/adjectives.json", adj_group)
    counts = get_frequencies(adj_group)
    write_into_json_dictionary("data/adjectives_frequency.json", counts)

    print(adj_group)
def get_frequencies(dictionary):
    counts = dict()
    for key in dictionary:
        counts[key] = len(dictionary.get(key))
    return  sorted(counts.items(), key=lambda x: x[1], reverse=True)

def findPattern(game_list:list):#functia pentru n-grame bazata pe gramatica si parsarea arborelui obtinut din match-urile pe gramatica
    grammar1 = "NP: {<J.*>+<N.*>}\n" \
              "Np: {<N.*>+<J.*>}\n" \
              "np2: {<N.*><N.*>}" #<DT>?
    expressions_dict={}
    for game in game_list:
        tokens = nltk.word_tokenize(game.description)
        tagged = nltk.pos_tag(tokens)
        cp = nltk.RegexpParser(grammar1)
        result = cp.parse(tagged)
        for element in result:
           if str(type(element)) =='<class \'nltk.tree.tree.Tree\'>':
                print(element.leaves())
                leaves=element.leaves()
                #pentru a lua cobinatii de mai multe cuvinte pentru n-grame trebuie modificat for-ul de mai jos
                for i in range(0,len(element.leaves())-1):
                    expression=leaves[i][0]+" "+leaves[i+1][0] # n-grame de cate doua cuvinte
                    uniform_expression=expression.lower()
                    if uniform_expression not in expressions_dict.keys():
                        expressions_dict[uniform_expression]=[]
                        expressions_dict[uniform_expression].append(game.id)
                    else:
                        expressions_dict[uniform_expression].append(game.id)
    write_into_json_dictionary("data/expressions.json",expressions_dict)




games_list=load_json()

tokenize(games_list)
findPattern(games_list)