FILE=$1
format=$2
columns=$3
preprocessing=$4

python tool/preprocessor.py \
    --input=$FILE.$format \
    --spm=tool/tokenizer/spm.ko.model \
    --preprocessing="${preprocessing}" \
    --columns="${columns}"

mkdir -p result
python tool/csv2txt.py \
    --input=$FILE.ppc.$format \
    --preprocessing="${preprocessing}" \
    --columns="${columns}"