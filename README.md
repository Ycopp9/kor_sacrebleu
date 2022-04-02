# Guidance to Pre-tokenization for SacreBLEU: <br />Meta-Evaluation in Korean
<img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>
<img src="https://img.shields.io/badge/Kakao-FFCD00?style=flat-square&logo=Kakao&logoColor=black"/></a>
<img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg"/></a>

This repository provides data sets and codes for MT evaluation employed in the given publication, written by **Ahrii Kim (김아리)** and **Jinhyeon Kim (김진현)** and submitted at [Preprints.org](https://www.preprints.org/manuscript/202201.0018/v1) and [HumEval 2022]().

---
### About
SacreBLEU, by incorporating a text normalizing step in the pipeline, has been well-received as an automatic evaluation metric in recent years. With agglutinative languages such as Korean, however, the metric cannot provide a conceivable result without the help of customized pre-tokenization. In this regard, this paper endeavors to examine the influence of diversified pre-tokenization schemes –word, morpheme, character, and subword– on the aforementioned metric by performing meta-evaluation with manually-constructed into-Korean human evaluation data.

Our empirical study demonstrates that the correlation of SacreBLEU, and other homogeneous metrics as an extension, vacillates greatly by the token type. The reliability of the metric even deteriorates due to some tokenization, and **MeCab-ko** is one of its culprits. Guiding through the proper usage of the tokenizer for each metric, we stress the significance of **Kiwi** as the most reliable Korean tokenizer and the insignificance of the subword level, **Jamo (자음 & 모음)**, in MT evaluation.

---
### Data Set
|Type|Detail|
|---|---|
|Source Text|WMT 20 ende source|
|System, Reference Text|-|
|Evaluation Scores|Human *Adequacy & Fluency* scores|
||Automatic Evaluation (segment & corpus level)|


### Toolkit
- Tokenizers
  - [KoNLPy](https://konlpy.org/ko/latest/) (Park and Cho, 2014)
  - [Kiwi](https://github.com/bab2min/Kiwi)
  - [Khaiii](https://github.com/kakao/khaiii)
  - [Jamo](https://pypi.org/project/jamo/)
  - [Sentencepiece](https://github.com/google/sentencepiece)
- Automatic Metrics
  - [SacreBLEU](https://github.com/mjpost/sacrebleu) (Post, 2018): BLEU, TER, CHRF 
  - [NLTK BLEU, GLEU, NIST, RIBES]()
  - EED (Stanchev et al., 2019)
  - CharacTER (Wang et al., 2016)
- Evaluation
  - Wilcoxon rank sum test
  - Bootstrap resampling
  - Pearson correlation coefficient
