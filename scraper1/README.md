# University Web Scraper
Built using Python and Beautiful Soup. Parses University academic sites and compiles 
papers, articles,  and other academic material into a .csv file.

## Creating Virtual Environment
These instructions assume you're using Windows CMD. Creating the virtual environment:
```
cd rad-db-data-collect/scraper1
python -m venv venv
"venv/Scripts/activate"
pip install -r requirements.txt
```

## Running the Program
You can run build.bat to create an executable binary. After running the batch file, 
execute the following to output the usage:
```
PyUniScraper --help
```
You can use this executable to get .csv files that contain academic material 
information for your chosen university. A typical command may look like:
```
PyUniScraper birmingham 1 Tech
```
You can also run the python source files directly using the python interpreter. The 
same functionality using the interpreter will look like:
```
python src/main.py birmingham 1 Tech
```