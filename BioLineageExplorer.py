from Bio import Entrez
from rich.tree import Tree
from rich import print, box
from rich.panel import Panel
from rich.console import Console
from rich.prompt import Prompt

Entrez.email = "ENTER_YOUR_EMAIL_HERE"
console = Console()

def fetch_from_entrez(term=None, db="", id=None, retmode=None):
    try:
        if id is None:
            handle = Entrez.esearch(term=term, db=db)
        else:
            handle = Entrez.efetch(id=id, db=db, retmode=retmode)
        return Entrez.read(handle)
    except RuntimeError as e:
        console.print(f"[red]Error: {e}. Please check your connection or try again later.[/red]")
        return None

def get_lineage(genus_species):
    search_record = fetch_from_entrez(term=genus_species, db="taxonomy")
    if search_record is None or not search_record['IdList']:
        console.print("[red]Species not found or an error occurred. Please check your spelling or try a different species.[/red]")
        return None

    taxonomy_id = search_record['IdList'][0]
    tax_record = fetch_from_entrez(id=taxonomy_id, db="taxonomy", retmode="xml")

    if tax_record is None:
        console.print("[red]Error fetching taxonomy data. Please try again later.[/red]")
        return None

    lineage = {rank: name for rank, name in map(lambda d: (d['Rank'], d['ScientificName']), tax_record[0]['LineageEx'])}

    info_record = fetch_from_entrez(id=taxonomy_id, db="taxonomy", retmode="xml")

    if info_record is None:
        console.print("[red]Error fetching additional information. Please try again later.[/red]")
        return None

    lineage["Info"] = info_record[0]

    return lineage

def fetch_species_of_genus(genus):
    term = f"{genus}[Organism]"
    record = fetch_from_entrez(term=term, db="taxonomy")
    if record is None:
        return []

    id_list = record["IdList"]
    species = []
    for tax_id in id_list:
        records = fetch_from_entrez(id=tax_id, db="taxonomy", retmode="xml")
        for record in records:
            species.append(record["ScientificName"])

    return species

def format_additional_info(info):
    common_names = ', '.join(info["OtherNames"]["CommonName"])
    synonyms = ', '.join(info["OtherNames"]["Synonym"])
    genetic_code = info["GeneticCode"]["GCName"]
    mito_genetic_code = info["MitoGeneticCode"]["MGCName"]
    creation_date = info["CreateDate"]
    update_date = info["UpdateDate"]

    console.print(f"Common Names: {common_names}")
    console.print(f"Synonyms: {synonyms}")
    console.print(f"Genetic Code: {genetic_code}")
    console.print(f"Mitochondrial Genetic Code: {mito_genetic_code}")
    console.print(f"Creation Date: {creation_date}")
    console.print(f"Update Date: {update_date}")

def lineage_to_tree(lineage):
    rank_names = ['superkingdom', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    tree = Tree(":dna: Life")
    current_level = tree
    for rank in rank_names:
        if rank in lineage:
            new_level = current_level.add(f"{rank.capitalize()}: [green]{lineage[rank]}[/green]")
            current_level = new_level
    return tree

def main():
    while True:
        console.print(Panel("[bold green]Welcome to the Species Search Program![/bold green]\n\n1. [yellow]Show Lineage Tree[/yellow]\n2. [yellow]Show Species in Genus[/yellow]\n3. [red]Exit[/red]", box=box.ROUNDED))
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3"], default="1")

        if choice == "1":
            genus_species = input('Enter a genus, species, common name, or alternate name: ')
            lineage = get_lineage(genus_species)
            if lineage is not None:
                tree = lineage_to_tree(lineage)
                console.print(tree)
                format_additional_info(lineage["Info"])
        elif choice == "2":
            genus = input("Enter a genus: ")
            species = fetch_species_of_genus(genus)
            if species:
                console.print(f"All known species in the {genus} genus:")
                for sp in species:
                    console.print(f"- {sp}")
            else:
                console.print(f"No known species found for the {genus} genus.")
        elif choice == "3":
            console.print("[blue]Goodbye![/blue]")
            break

if __name__ == '__main__':
    main()
