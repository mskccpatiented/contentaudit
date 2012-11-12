for f in `ls`; do
filename="${PWD}/$f"
echo $filename
python /Users/paulmay/Dropbox/BMT Patient Ed Content/04. JargonApp/jargon.py -i filename -t 800
done
