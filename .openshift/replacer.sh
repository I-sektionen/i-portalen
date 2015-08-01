pwd

old_val="js/iportalen.js"
new_val="dist/iportalen.min.js"

echo 'hej'
s1="s,$old_val,$new_val,g"

old_val2="css/app.css"
new_val2="dist/iportalen.min.css"

s2="s,$old_val2,$new_val2,g"

echo $s1
echo $s2


sed -i $s1 ../wsgi/templates/scripts.html
sed -i $s2 ../wsgi/templates/stylesheets.html
