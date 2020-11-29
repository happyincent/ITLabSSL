# ./calc.sh nginx-star | tr '\n' '%' | sed 's/\%-\%/MB\n/g'

for f in `ls *.log | sort -V`; do
    #echo $f
    cat $f | grep $1 | column -t | cut -d ' ' -f3 | awk '{ total += $1; count++ } END { printf("%.2f\n", (total/16)/count) }'
    cat $f | grep $1 | column -t | cut -d'M' -f1 | rev | cut -d' ' -f 1 | rev | awk '{ total += $1; count++ } END { printf("%.2f\n", (total)/count)  }'
    echo -
done
