SQLite-Carver
=============

Script to recover deleted entries in an SQLite database and places the output into either a TSV file or text file (-r)

### Usage for sqlite-carver

    sqlite-carver -f /home/sanforensics/smsmms.db -o report.tsv
    sqlite-carver -f /home/sanforensics/smssms.db -r -o report.txt
	
	Optional switch -p to print out re purposed B-Leaf pages:
	
	sqlite-carver -p -f /home/sanforensics/smsmms.db -o report.tsv
    sqlite-carver -p -f /home/sanforensics/smssms.db -r -o report.txt
	

### More Information

View the blog post at https://az4n6.blogspot.com/2013/11/python-parser-to-recover-deleted-sqlite.html for more information

Raise an [issue](https://github.com/digitalsleuth/SQLite-Deleted-Records-Parser/issues) if you need support or find a bug!
