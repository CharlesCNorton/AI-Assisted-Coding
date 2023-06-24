from Bio import Entrez
from rich.tree import Tree
from rich import print

def get_lineage(genus_species):
    Entrez.email = "your.email@example.com"
    try:
        search = Entrez.esearch(term=f"{genus_species}[orgn]", db="taxonomy")
        record = Entrez.read(search)
        taxonomy_id = record['IdList'][0]
    except IndexError:
        print("Species not found. Please check your spelling or try a different species.")
        return None

    taxonomy = Entrez.efetch(id=taxonomy_id, db="taxonomy", retmode="xml")
    tax_record = Entrez.read(taxonomy)

    lineage = {rank: name for rank, name in map(lambda d: (d['Rank'], d['ScientificName']), tax_record[0]['LineageEx'])}

    # Fetch additional information
    additional_info = Entrez.efetch(id=taxonomy_id, db="taxonomy", retmode="xml")
    info_record = Entrez.read(additional_info)
    lineage["Info"] = info_record[0]

    return lineage

def format_additional_info(info):
    common_names = ', '.join(info["OtherNames"]["CommonName"])
    synonyms = ', '.join(info["OtherNames"]["Synonym"])
    genetic_code = info["GeneticCode"]["GCName"]
    mito_genetic_code = info["MitoGeneticCode"]["MGCName"]
    creation_date = info["CreateDate"]
    update_date = info["UpdateDate"]

    print(f"Common Names: {common_names}")
    print(f"Synonyms: {synonyms}")
    print(f"Genetic Code: {genetic_code}")
    print(f"Mitochondrial Genetic Code: {mito_genetic_code}")
    print(f"Creation Date: {creation_date}")
    print(f"Update Date: {update_date}")

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
        print("\n1. Show Lineage Tree")
        print("2. Exit")
        choice = input("\nEnter your choice: ")

        if choice == "1":
            genus_species = input('Enter a genus and species (e.g., "Homo sapiens"): ')
            lineage = get_lineage(genus_species)
            if lineage is not None:
                tree = lineage_to_tree(lineage)
                print(tree)
                format_additional_info(lineage["Info"])
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please enter 1 or 2.")

if __name__ == '__main__':
    main()# Write your code here :-)
