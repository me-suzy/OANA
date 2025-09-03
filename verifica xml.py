import xml.etree.ElementTree as ET

def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        print("Fișierul XML este parsat corect.")
        return root
    except ET.ParseError as e:
        print(f"Eroare de parsare XML: {e}")
        print(f"Detalii suplimentare: Linie {e.position[0]}, Coloană {e.position[1]}")
        return None

def find_errors(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Verifică existența spațiilor de nume necesare
    image_namespace = "{http://neculaifantanaru.com/imagini}"

    for url in root.findall(".//url"):
        for image_tag in url.findall(f"{image_namespace}image"):
            for loc_tag in image_tag.findall(f"{image_namespace}loc"):
                print(f"URL: {loc_tag.text}")

def main():
    file_path = r'C:\calea\rss.xml'  # Schimbă cu calea către fișierul tău XML
    parse_xml(file_path)
    find_errors(file_path)

if __name__ == "__main__":
    main()
