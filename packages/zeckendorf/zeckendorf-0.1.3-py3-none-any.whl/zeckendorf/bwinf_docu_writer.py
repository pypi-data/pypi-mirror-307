import json
import os
import subprocess


class DocumentationWriter:
    def __init__(self):
        self.global_config = None
        self.local_config = None

    def create_global_config(self):
        config = {
            #"openai_api_key": self.get_input("OpenAI API key: ", lambda text: text.isprintable()),
            "team_id": self.get_input("Team ID: ", lambda text: text.isnumeric()),
            "team_name": self.get_input("Teamname: ", lambda text: text.isalpha()),
            "vorname": self.get_input("Vorname: ", lambda text: text.istitle() and not (" " in text or "\n" in text)),
            "nachname": self.get_input("Nachname: ", lambda text: text.istitle() and not (" " in text or "\n" in text))
        }
        self.write_json("config.json", config)

    def create_local_config(self, path: str):
        junior = self.get_input("Junioraufgabe (y/n): ", lambda text: text in ["y", "n"]) == "y"
        nummer = self.get_input("Aufgabennummer: ", lambda text: text.isnumeric())
        config = {
            "name": ("Juniora" if junior else "A") + f"ufgabe {nummer}",
            "bezeichnung": self.get_input("Bezeichnung: ", lambda text: text.isprintable())
        }
        self.write_json(f"{path}/config.json", config)

    def get_example_outputs(self, path: str):
        file_names = sorted(os.listdir(f"{path}/in"))
        text = ""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, path, "main.py")

        for file_name in file_names:
            result = subprocess.run(
                ['python3', script_path],
                input=f"{path}/in/{file_name}",
                text=True,
                capture_output=True,
                check=True
            )
            output = result.stdout.removeprefix("Pfad zur .txt Datei: ").strip()
            text += f"\n\n\\subsection*{{in/{file_name}}}\n\\begin{{lstlisting}}\n{output}\n\\end{{lstlisting}}"

        return text

    def create_documentation(self, path: str):
        if not os.path.isfile("config.json"):
            self.create_global_config()

        if not os.path.isfile(f"{path}/config.json"):
            self.create_local_config(path)

        self.global_config = self.load_json("config.json")
        self.local_config = self.load_json(f"{path}/config.json")
        example_outputs = self.get_example_outputs(path)
        code = self.read_file(f"{path}/main.py")
        try:
            idea = open(f"{path}/idea.txt", "r").read()
            implementation = open(f"{path}/implementation.txt", "r").read()
        except FileNotFoundError:
            raise Exception("No idea or implementation provided.")

        documentation = f"""
\\documentclass[a4paper,10pt,ngerman]{{scrartcl}}
\\usepackage{{babel}}
\\usepackage[T1]{{fontenc}}
\\usepackage[utf8x]{{inputenc}}
\\usepackage[a4paper,margin=2.5cm,footskip=0.5cm]{{geometry}}

\\newcommand{{\\Aufgabe}}{{{self.local_config["name"]}: {self.local_config["bezeichnung"]}}}
\\newcommand{{\\TeamId}}{{{self.global_config["team_id"]}}}
\\newcommand{{\\TeamName}}{{{self.global_config["team_name"]}}}
\\newcommand{{\\Namen}}{{{self.global_config["vorname"]} {self.global_config["nachname"]}}}

\\usepackage{{scrlayer-scrpage, lastpage}}
\\setkomafont{{pageheadfoot}}{{\\large\\textrm}}
\\lohead{{\\Aufgabe}}
\\rohead{{Team-ID: \\TeamId}}
\\cfoot*{{\\thepage{{}}/\\pageref{{LastPage}}}}

\\usepackage{{titling}}
\\setlength{{\\droptitle}}{{-1.0cm}}

\\usepackage{{amsmath}}
\\usepackage{{amssymb}}
\\usepackage{{graphicx}}
\\usepackage{{algpseudocode}}
\\usepackage{{listings}}
\\usepackage{{color}}
\\definecolor{{mygreen}}{{rgb}}{{0,0.6,0}}
\\definecolor{{mygray}}{{rgb}}{{0.5,0.5,0.5}}
\\definecolor{{mymauve}}{{rgb}}{{0.58,0,0.82}}
\\lstset{{
  keywordstyle=\\color{{blue}},commentstyle=\\color{{mygreen}},
  stringstyle=\\color{{mymauve}},rulecolor=\\color{{black}},
  basicstyle=\\footnotesize\\ttfamily,numberstyle=\\tiny\\color{{mygray}},
  captionpos=b,
  keepspaces=true,
  numbers=left, numbersep=5pt, showspaces=false,showstringspaces=true,
  showtabs=false, stepnumber=1, tabsize=2, title=\\lstname,
  breaklines=true,
  extendedchars=true,
  literate={{ä}}{{{{\\"a}}}}1 {{ö}}{{{{\\"o}}}}1 {{ü}}{{{{\\"u}}}}1 {{ß}}{{{{\\ss}}}}1
}}

\\usepackage{{cleveref}}

\\title{{\\textbf{{\\Huge\\Aufgabe}}}}
\\author{{\\LARGE Team-ID: \\LARGE \\TeamId \\\\\\\\\n    \\LARGE Team-Name: \\LARGE \\TeamName \\\\\\\\\n    \\LARGE Bearbeiter dieser Aufgabe:\\\\\n    \\LARGE \\Namen\\\\\\\\}}
\\date{{\\LARGE\\today}}

\\begin{{document}}

\\maketitle
\\tableofcontents

\\vspace{{0.5cm}}

\\section{{Lösungsidee}}

{idea}

\\section{{Umsetzung}}

{implementation}

\\section{{Beispiele}}

Wir führen das Programm für die folgenden Dateien aus.
{example_outputs}

\\section{{Quellcode}}

\\lstset{{language=Python}}
\\begin{{lstlisting}}
{code}
\\end{{lstlisting}}

\\end{{document}}
        """

        self.write_file(f"{path}/documentation.txt", documentation)

    @staticmethod
    def get_input(prompt: str, verifier=None):
        while True:
            inp = input(prompt)
            if verifier(inp):
                return inp.strip()
            print("Wrong input format.")

    @staticmethod
    def read_file(path: str) -> str:
        with open(path, 'r') as f:
            return f.read()

    @staticmethod
    def write_file(path: str, content: str):
        with open(path, 'w') as f:
            f.write(content)

    @staticmethod
    def write_json(path: str, content: dict):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)

    @staticmethod
    def load_json(path: str) -> dict:
        with open(path, 'r') as f:
            return json.load(f)

    @staticmethod
    def clean_text(text: str) -> str:
        return "\n".join(line for line in text.splitlines() if line.strip())

