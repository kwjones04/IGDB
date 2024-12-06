# IGDB Client Folder

## Get data using CSV file
- Add titles of games you want to add in the CSV file "Games-To-Add.csv"
- If you are not getting the information you expect using the title, you can add the game's IGDB id next to the title, separated by a comma.
- When you run the script, it will retrieve information from this CSV file first.

## How to Use this Project
- In your terminal or command prompt, make sure this folder is the current directory.
- Make sure the required dependencies are installed by running: `pip install -r requirements.txt`
- Copy the below command into your terminal with your own IGDB `client_id` and `client_secret`.
- If you wish to retrieve information using a range of IGDB game ids, add integer values to both of the `min_id` and `max_id` arguments.
- If you have an existing db file, you can add a value to `db_path`.
- You can specify which format(s) you want the results in by adding any of the following values to `results`: `csv`, `json`, `db`. If you don't specify this value, the default is `db`.

**The command should look like this with your own information in place of the brackets:**
`python3 script.py --client_id="[Client ID]" --client_secret="[Client Secret]" --min_id=[An integer] --max_id=[An integer] --db_path="[Current db File]" --results="[csv, json, and/or db]"`

## Other Information
- This script can retrieve information that you may already have in your database file or have retrieved via the CSV file. However, the duplicate data will not be saved to the result files.
- This script retrieves the following game information from IGDB: **id, title, summary, platform along with its release date on that platform, cover id**