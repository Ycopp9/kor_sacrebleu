# Guidance to Pre-tokenization for SacreBLEU: Meta-Evaluation in Korean
<img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>
<img src="https://img.shields.io/badge/Kakao-FFCD00?style=flat-square&logo=Kakao&logoColor=black"/></a>
<img src="https://img.shields.io/apm/l/vim-mode"/></a>

This repository provides data sets for MT evaluation run in the following publication written by Ahrii Kim and Jinhyeon Kim, submitted at [Preprints.org](https://www.preprints.org/manuscript/202201.0018/v1) and [HumEval 2022]().

---
### Data Set
|Type|Detail|
|---|---|
|Source Text|WMT 20 ende source|
|System, Reference Text|-|
|Evaluation Scores|Human *Adequacy & Fluency* scores|
||Automatic Evaluation (segment & corpus level)|

### Tool
- Tokenizers
  - KoNLPy
  - Kiwi
  - Khaiii
  - Jamo
  - Sentencepiece
- Metrics
  - SacreBLEU: BLEU, TER, CHRF
  - NLTK BLEU, GLEU, NIST, RIBES
  - EED
  - CharacTER 
