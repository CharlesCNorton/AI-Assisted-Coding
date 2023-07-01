# BioLineageExplorer

BioLineageExplorer is a Python program that allows you to search for and explore the taxonomic lineage of species using the NCBI Entrez API. It provides a command-line interface to perform the following actions:

1. Show Lineage Tree: Displays the taxonomic lineage tree of a given genus, species, common name, or alternate name.
2. Show Species in Genus: Retrieves and displays all known species in a given genus.
3. Exit: Exits the program.

## Prerequisites

- Python 3.x
- BioPython library
- Rich library

## Usage

1. Set your email address in the `Entrez.email` variable in the code.
2. Run the program: `python BioLineageExplorer.py`
3. Follow the prompts to choose an action and enter the required information.

## Example Usage

Welcome to the Species Search Program!

1. Show Lineage Tree
2. Show Species in Genus
3. Exit

Enter your choice: `1`

Enter a genus, species, common name, or alternate name: `Homo sapiens`

Life
└── Superkingdom: Bacteria
    └── Phylum: Firmicutes
        └── Class: Clostridia
            ├── Order: Clostridiales
            │   └── Family: Clostridiaceae
            │       └── Genus: Clostridium
            │           └── Species: Clostridium botulinum
            └── Order: Lactobacillales
                └── Family: Lactobacillaceae
                    ├── Genus: Lactobacillus
                    │   ├── Species: Lactobacillus acidophilus
                    │   ├── Species: Lactobacillus casei
                    │   ├── Species: Lactobacillus crispatus
                    │   └── Species: Lactobacillus delbrueckii
                    └── Genus: Streptococcus
                        ├── Species: Streptococcus pyogenes
                        └── Species: Streptococcus pneumoniae

Additional Information:
- Common Names: human
- Synonyms: Homo sapiens sapiens, Homo sapiens neanderthalensis
- Genetic Code: Standard
- Mitochondrial Genetic Code: Vertebrate Mitochondrial
- Creation Date: 2013/03/13
- Update Date: 2021/06/27

Enter your choice: `2`

Enter a genus: `Canis`

All known species in the Canis genus:
- Canis adustus
- Canis aureus
- Canis lupus
- Canis mesomelas
- Canis simensis

Enter your choice: `3`

Goodbye!

## License

This project is licensed under the [MIT License](LICENSE).