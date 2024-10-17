# Election Data Processing Tool

**Author:** Tomáš Škuta  
**Email:** tomasskuta@seznam.cz
**Discord:** smajlikskutik  
______________________________________________________________________________________________________________________________________________________________________________________
## Project Description

This project is part of the **Engeto Online Python Academy** and provides a tool to scrape and process Czech election data from 2017. The script extracts election results from the official Czech elections website and stores them in a CSV file for further analysis.
______________________________________________________________________________________________________________________________________________________________________________________
## Features

- Scrapes election data from the Czech elections website.
- Collects detailed results, including registered voters, valid votes, and party-specific results.
______________________________________________________________________________________________________________________________________________________________________________________
## Requirements

- **Python 3.6+**
- The following Python libraries, which can be installed via `pip`:
  - `requests`
  - `beautifulsoup4`

You can install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

or

```bash
pip install requests
pip install bs4
```

The `requirements.txt` file should contain:

beautifulsoup4
requests

It containts more libraries, but those are downloaded as dependencies of requests/bs4 libraries.
Project using also csv, argparse and sys libraries - but no need to install them since those are part of standard Python libraries.
______________________________________________________________________________________________________________________________________________________________________________________
## Usage

To run the script, you'll need to provide the URL of the election data and the name of the output CSV file. The usage looks like this:

```bash
python main.py <url> <output_file.csv>
```

### Example :

#### For normal usage:
```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100" "praha.csv"
```
This will download election data from the specified URL(Praha) and save it to file as `praha.csv`.

#### Help:
```bash
python main.py -h
```
This will show help for this script.
______________________________________________________________________________________________________________________________________________________________________________________
## Command-Line Arguments

- `url`: The URL of the election data page. It must be in the format `https://www.volby.cz/pls/ps2017nss/...` or same with http
- `output_file`: The name of the output CSV file. The file name must end with `.csv`.
______________________________________________________________________________________________________________________________________________________________________________________
## CSV Output Format

The CSV file will contain the following columns:

- **code**: District code.
- **location**: Name of the location (e.g., district).
- **registered**: Number of registered voters.
- **envelopes**: Number of distributed voting envelopes.
- **valid**: Number of valid votes.
- **party_1, party_2, ..., party_N**: Votes for each party, with party names as column headers.

______________________________________________________________________________________________________________________________________________________________________________________
## Example Output

Deliminator is ;. That means when opening in for example Excel every value after ; will be in new cell.
```csv
code;location;registered;envelopes;valid;Občanská demokratická strana;Řád národa - Vlastenecká unie;CESTA ODPOVĚDNÉ SPOLEČNOSTI;Česká str.sociálně demokrat.;Volte Pr.Blok www.cibulka.net;Radostné Česko;STAROSTOVÉ A NEZÁVISLÍ;Komunistická str.Čech a Moravy;Strana zelených;ROZUMNÍ-stop migraci,diktát.EU;Společ.proti výst.v Prok.údolí;Strana svobodných občanů;Blok proti islam.-Obran.domova;Občanská demokratická aliance;Česká pirátská strana;OBČANÉ 2011-SPRAVEDL. PRO LIDI;Unie H.A.V.E.L.;Referendum o Evropské unii;TOP 09;ANO 2011;Dobrá volba 2016;SPR-Republ.str.Čsl. M.Sládka;Křesť.demokr.unie-Čs.str.lid.;Česká strana národně sociální;REALISTÉ;SPORTOVCI;Dělnic.str.sociální spravedl.;Svob.a př.dem.-T.Okamura (SPD);Strana Práv Občanů
500054;Praha 1;32140;21655;21479;4300;9;13;999;12;1;1152;581;901;59;6;349;32;71;3610;5;0;30;4313;2554;1;16;1377;3;214;11;2;815;43
500224;Praha 10;110313;56006;55536;8918;62;56;3318;50;17;2400;2672;1289;230;15;1127;46;67;10158;9;8;30;6871;11362;37;53;2475;12;510;69;64;3438;173
547034;Praha 11;72419;49823;49529;6608;61;18;2916;30;17;2055;2622;978;257;13;1171;42;96;8856;24;5;23;5301;11955;31;35;2090;27;542;86;66;3428;176
```
______________________________________________________________________________________________________________________________________________________________________________________
## Error Handling

The script includes basic error handling for:
- Invalid URLs (URL must start with `https://www.volby.cz/pls/ps2017nss/`).
- Invalid output file format (output file must end with `.csv`).
- First must be link and then name of the file (like in usage)
______________________________________________________________________________________________________________________________________________________________________________________
## Contact

If you have any questions, feel free to reach out via email or Discord!
