# Guidance to Pre-tokenization for SacreBLEU: Meta-Evaluation in Korean

<img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>
[<img src="https://img.shields.io/badge/Kakao-FFCD00?style=flat-square&logo=Kakao&logoColor=black"/></a>](https://www.kakaoenterprise.com)
<img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg"/></a>

This repository provides datasets and codes for MT evaluation employed in the given publication, written by **Ahrii Kim (김아리)** and **Jinhyeon Kim (김진현)** and submitted at [Preprints.org](https://www.preprints.org/manuscript/202201.0018/v1) (version 1) and [HumEval 2022](https://openreview.net/forum?id=BWVeZdViVW5&referrer=%5BAuthor%20Console%5D(%2Fgroup%3Fid%3Daclweb.org%2FACL%2F2022%2FWorkshop%2FHumEval%2FAuthors%23your-submissions)) (the final version).


## Abstract
SacreBLEU, by incorporating a text normalizing step in the pipeline, has been well-received as an automatic evaluation metric in recent years. With agglutinative languages such as Korean, however, the metric cannot provide a conceivable result without the help of customized pre-tokenization. In this regard, this paper endeavors to examine the influence of diversified pre-tokenization schemes –word, morpheme, character, and subword– on the aforementioned metric by performing meta-evaluation with manually-constructed into-Korean human evaluation data.

Our empirical study demonstrates that the correlation of SacreBLEU, and other homogeneous metrics as an extension, vacillates greatly by the token type. The reliability of the metric even deteriorates due to some tokenization, and **MeCab-ko** is one of its culprits. Guiding through the proper usage of the tokenizer for each metric, we stress the significance of [**Korean Intelligent Word Identifier (Kiwi)**](https://github.com/bab2min/Kiwi) as the most reliable Korean tokenizer and the insignificance of the subword level, **Jamo (자음 & 모음)**, in MT evaluation.


## Dataset
- Base
    - Source Text: English from WMT 20 en-de (2,048 sentences/61 documents)
    - Reference Text: Korean* (manually created)
    - System Translation: 4
- Judgment
    - Human: Direct Assessment (DA) of adequacy & fluency
    - Automatic: [SacreBLEU](https://github.com/mjpost/sacrebleu), BLEU, GLEU, RIBES, NIST, TER, ChrF, [EED](https://aclanthology.org/W19-5359/), and [CharacTER](https://aclanthology.org/W16-2342/)   
    *_For legal issue, a sample of the reference set is publicly available._


## Tokenization
1. **Word Level**
2. **Morpheme Level**
    - [KoNLPy](https://konlpy.org/ko/latest/) (Park and Cho, 2014)
    - [Korean Intelligent Word Identifier (Kiwi)](https://github.com/bab2min/Kiwi)
    - [Kakao Hangul Analyzer III (Khaiii)](https://github.com/kakao/khaiii)
3. **Character Level**
4. **Subword Level**
    - [Sentencepiece](https://github.com/google/sentencepiece)
    - [Jamo](https://pypi.org/project/jamo/)


The implementation of the given tokenizers:
```sh
from tool.tokenizer import *

# the morpheme level
mecab = koNLPy.KoNLPy('mecab') # one of the five
kiwi = kakao.Kiwi()
khaiii = kakao.Khaiii()

# the character level
char = base.Character()

# the subword level
spm = subword.SPM()
jamo = subword.Jamo(jamo_split=True)
```


#### Examplary Tokens

|Type|Tokens|
|---|---|
|Sentence|"모델 레옹 데임은 아직 그 누구도 시도한 적 없는 방식으로 캣워크를 활보했다"|
|Word|`['모델', '레옹', '데임은', '아직', '그', '누구도', '시도한', '적', '없는', '방식으로', '캣워크를', '활보했다']`|
|MeCab-ko|`['모델', '레옹', '데임', '은', '아직', '그', '누구', '도', '시도', '한', '적', '없', '는', '방식', '으로', '캣', '워크', '를', '활보', '했', '다']`|
|Kiwi|`['모델', '레옹', '데이', 'ᆷ', '은', '아직', '그', '누구', '도', '시도', '하', 'ᆫ', '적', '없', '는', '방식', '으로', '캣워크', '를', '활보', '하', '었', '다']`|
|Khaiii|`['모델', '레옹', '데임', '은', '아직', '그', '누구', '도', '시도', '하', 'ㄴ', '적', '없', '는', '방식', '으로', '캣워크', '를', '활보', '하', '였', '다']`|
|Character|`['모', '델', '레', '옹', '데', '임', '은', '아', '직', '그', '누', '구', '도', '시', '도', '한', '적', '없', '는', '방', '식', '으', '로', '캣', '워', '크', '를', '활', '보', '했', '다']`|
|SPM|`['모델', '레', '옹', '데', '임', '은', '아직', '그', '누구', '도', '시도', '한', '적', '없', '는', '방식', '으로', '', '캣', '워크', '를', '활', '보', '했', '다']`|
|Jamo|`['ㅁ', 'ㅗ', 'ㄷ', 'ㅔ', 'ㄹ', ' ', 'ㄹ', 'ㅔ', 'ㅇ', 'ㅗ', 'ㅇ', ' ', 'ㄷ', 'ㅔ', 'ㅇ', 'ㅣ', 'ㅁ', 'ㅇ', 'ㅡ', 'ㄴ', ' ', 'ㅇ', 'ㅏ', 'ㅈ', 'ㅣ', 'ㄱ', ' ', 'ㄱ', 'ㅡ', ' ', 'ㄴ', 'ㅜ', 'ㄱ', 'ㅜ', 'ㄷ', 'ㅗ', ' ', 'ㅅ', 'ㅣ', 'ㄷ', 'ㅗ', 'ㅎ', 'ㅏ', 'ㄴ', ' ', 'ㅈ', 'ㅓ', 'ㄱ', ' ', 'ㅇ', 'ㅓ', 'ㅄ', 'ㄴ', 'ㅡ', 'ㄴ', ' ', 'ㅂ', 'ㅏ', 'ㅇ', 'ㅅ', 'ㅣ', 'ㄱ', 'ㅇ', 'ㅡ', 'ㄹ', 'ㅗ', ' ', 'ㅋ', 'ㅐ', 'ㅅ', 'ㅇ', 'ㅝ', 'ㅋ', 'ㅡ', 'ㄹ', 'ㅡ', 'ㄹ', ' ', 'ㅎ', 'ㅘ', 'ㄹ', 'ㅂ', 'ㅗ', 'ㅎ', 'ㅐ', 'ㅆ', 'ㄷ', 'ㅏ']`|


![table1](./table1.png)


## Evaluation Metrics
The following two metrics are copied from the original libraries. You can test their scores with our example as follows:

```sh
[EED]
$ python3 ./tool/metric/ExtendedEditDistance/EED.py \
                -ref data/ref_example.txt \
                -hyp data/hyp_example.txt

[CharacTER]
$ python3 ./tool/metric/CharacTER/CharacTER.py \
                -r data/ref_example.txt \
                -o data/hyp_example.txt
```


## Citation
    @inproceedings{kor-sacrebleu22,
        title={Guidance to Pre-tokenization for SacreBLEU: Meta-Evaluation in Korean},
        author={Kim, Ahrii and Kim, Jinhyeon},
        booktitle={Proceedings of the Workshop on Human Evaluation of NLP Systems (HumEval)}
        year={2022}
    }
    
## License
Apache License Version 2.0