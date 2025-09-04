import os
import regex

def remove_quotes_with_advanced_regex(html_content):
    """Folosește formulele avansate regex pentru curățare precisă"""
    
    changes_made = 0
    
    # 1. Meta name="description" - folosind formula generică
    # BSR: <meta name="description" content="
    # ESR: ">
    # FR: ghilimelele problematice
    BSR1 = r'<meta name="description" content="'
    ESR1 = r'">'
    
    # Găsește întreaga zonă și apoi curăță conținutul
    pattern1 = fr'({BSR1})(.*?)({ESR1})'
    
    def clean_meta_desc(match):
        nonlocal changes_made
        prefix = match.group(1)
        content = match.group(2)
        suffix = match.group(3)
        
        original_len = len(content)
        cleaned_content = (content
                          .replace('„', '')
                          .replace('"', '')
                          .replace('"', '')
                          .replace('"', '')
                          .replace('|', ''))
        
        if len(cleaned_content) != original_len:
            changes_made += 1
            chars_removed = original_len - len(cleaned_content)
            print(f'   - Meta description: eliminat {chars_removed} caractere')
        
        return prefix + cleaned_content + suffix
    
    html_content = regex.sub(pattern1, clean_meta_desc, html_content, flags=regex.DOTALL)
    
    # 2. Meta property="og:description" - cu formula adaptată
    BSR2 = r'<meta property="og:description" content="'
    ESR2 = r'"/>'
    
    pattern2 = fr'({BSR2})(.*?)({ESR2})'
    
    def clean_og_desc(match):
        nonlocal changes_made
        prefix = match.group(1)
        content = match.group(2)
        suffix = match.group(3)
        
        original_len = len(content)
        cleaned_content = (content
                          .replace('„', '')
                          .replace('"', '')
                          .replace('"', '')
                          .replace('"', '')
                          .replace('|', ''))
        
        if len(cleaned_content) != original_len:
            changes_made += 1
            chars_removed = original_len - len(cleaned_content)
            print(f'   - OG description: eliminat {chars_removed} caractere')
        
        return prefix + cleaned_content + suffix
    
    html_content = regex.sub(pattern2, clean_og_desc, html_content, flags=regex.DOTALL)
    
    # 3. JSON "description": "..." - cu spații
    BSR3 = r'"description":\s*"'
    ESR3 = r'",'
    
    pattern3 = fr'({BSR3})(.*?)({ESR3})'
    
    def clean_json_desc(match):
        nonlocal changes_made
        prefix = match.group(1)
        content = match.group(2)
        suffix = match.group(3)
        
        original_len = len(content)
        cleaned_content = (content
                          .replace('„', '')
                          .replace('"', '')
                          .replace('"', '')
                          .replace('"', '')
                          .replace('|', ''))
        
        if len(cleaned_content) != original_len:
            changes_made += 1
            chars_removed = original_len - len(cleaned_content)
            print(f'   - JSON description: eliminat {chars_removed} caractere')
        
        return prefix + cleaned_content + suffix
    
    html_content = regex.sub(pattern3, clean_json_desc, html_content, flags=regex.DOTALL)
    
    # 4. JSON "description":"..." - fără spații  
    BSR4 = r'"description":"'
    ESR4 = r'",'
    
    pattern4 = fr'({BSR4})(.*?)({ESR4})'
    
    def clean_json_desc_nospace(match):
        nonlocal changes_made
        prefix = match.group(1)
        content = match.group(2)
        suffix = match.group(3)
        
        original_len = len(content)
        cleaned_content = (content
                          .replace('„', '')
                          .replace('"', '')
                          .replace('"', '')
                          .replace('"', '')
                          .replace('|', ''))
        
        if len(cleaned_content) != original_len:
            changes_made += 1
            chars_removed = original_len - len(cleaned_content)
            print(f'   - JSON description (no space): eliminat {chars_removed} caractere')
        
        return prefix + cleaned_content + suffix
    
    html_content = regex.sub(pattern4, clean_json_desc_nospace, html_content, flags=regex.DOTALL)
    
    return html_content, changes_made

def advanced_h3_to_h2_conversion(html_content):
    """Convertește h3 la h2 folosind regex avansat"""
    
    # Folosind formula generică pentru h3 conversion
    # BSR: <h3
    # ESR: </h3>
    # FR: class="text_obisnuit2" sau class=text_obisnuit2
    
    pattern = r'<h3(\s+class=(?:"text_obisnuit2"|text_obisnuit2)[^>]*?)>(.*?)</h3>'
    replacement = r'<h2 class="text_obisnuit2">\2</h2>'
    
    converted_content = regex.sub(pattern, replacement, html_content, flags=regex.DOTALL)
    
    # Verifică dacă s-au făcut schimbări
    changes = len(regex.findall(pattern, html_content, flags=regex.DOTALL))
    if changes > 0:
        print(f'   - H3 to H2: convertit {changes} tag-uri')
    
    return converted_content, changes

def process_html_files_advanced(folder_path):
    """Procesează fișierele HTML cu regex avansat"""
    
    if not os.path.exists(folder_path):
        print(f'Folderul nu există: {folder_path}')
        return
    
    total_files = 0
    total_changes = 0
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.html'):
            file_path = os.path.join(folder_path, filename)
            total_files += 1
            
            print(f'Procesare: {filename}')
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                original_length = len(content)
                
                # Aplică curățarea avansată
                content, desc_changes = remove_quotes_with_advanced_regex(content)
                content, h3_changes = advanced_h3_to_h2_conversion(content)
                
                new_length = len(content)
                file_changes = desc_changes + h3_changes
                
                if file_changes > 0:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    
                    total_changes += file_changes
                    chars_removed = original_length - new_length
                    print(f'   ✓ Total modificări: {file_changes}, caractere eliminate: {chars_removed}')
                else:
                    print(f'   - Nu s-au făcut modificări')
                    
            except Exception as e:
                print(f'   ✗ Eroare la {filename}: {e}')
    
    print(f'\n=== SUMAR ===')
    print(f'Fișiere procesate: {total_files}')
    print(f'Total modificări: {total_changes}')

# Test și procesare
def main():
    print("HTML Cleaner - Advanced Regex Version")
    print("Folosind biblioteca 'regex' cu formule avansate")
    print("=" * 60)
    
    # Verifică dacă biblioteca regex este instalată
    try:
        import regex
        print("✓ Biblioteca 'regex' este disponibilă")
    except ImportError:
        print("✗ Biblioteca 'regex' nu este instalată")
        print("Rulează: pip install regex")
        return
    
    folders = [
        r'c:\Folder1\test'
    ]
    
    for folder_path in folders:
        print(f'\n--- Procesare folder: {folder_path} ---')
        process_html_files_advanced(folder_path)

if __name__ == "__main__":
    main()