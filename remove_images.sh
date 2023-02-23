ls  | grep -E "(jpg)|(JPG)$" > liste_images
(while read line; do
	rm -v $line 
done) < liste_images
ls
