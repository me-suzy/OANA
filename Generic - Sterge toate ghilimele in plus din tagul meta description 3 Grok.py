import os
import regex

def remove_quotes_from_meta_description(html_content):
    """Curăță meta name="description" """
    pattern = regex.compile(r'(<meta name="description" content=")(.*?)(">)', regex.DOTALL)
    
    def replace_quotes(match):
        content = match.group(2)
        quote_chars = ['"', '„', '”', "'", '|', '&quot;', '&#39;', '&ldquo;', '&rdquo;', '&lsquo;', '&rsquo;']
        quotes_found = {char: content.count(char) for char in quote_chars if content.count(char) > 0}
        if quotes_found:
            print(f"   - Meta description: found quotes {quotes_found}")
        
        content_clean = content
        for char in quote_chars:
            content_clean = content_clean.replace(char, '')
        content_clean = content_clean.replace('\\"', '')  # Handle escaped quotes
        
        chars_removed = len(content) - len(content_clean)
        if chars_removed > 0:
            print(f"   - Meta description: eliminat {chars_removed} caractere")
        return match.group(1) + content_clean + match.group(3)
    
    return pattern.sub(replace_quotes, html_content)

def remove_quotes_from_og_description(html_content):
    """Curăță meta property="og:description" """
    pattern = regex.compile(r'(<meta property="og:description" content=")(.*?)("\s*/>)', regex.DOTALL)
    
    def replace_quotes(match):
        content = match.group(2)
        quote_chars = ['"', '„', '”', "'", '|', '&quot;', '&#39;', '&ldquo;', '&rdquo;', '&lsquo;', '&rsquo;']
        quotes_found = {char: content.count(char) for char in quote_chars if content.count(char) > 0}
        if quotes_found:
            print(f"   - OG description: found quotes {quotes_found}")
        
        content_clean = content
        for char in quote_chars:
            content_clean = content_clean.replace(char, '')
        content_clean = content_clean.replace('\\"', '')  # Handle escaped quotes
        
        chars_removed = len(content) - len(content_clean)
        if chars_removed > 0:
            print(f"   - OG description: eliminat {chars_removed} caractere")
        return match.group(1) + content_clean + match.group(3)
    
    return pattern.sub(replace_quotes, html_content)

def remove_quotes_from_json_description_spaces(html_content):
    """Curăță "description": "..." """
    pattern = regex.compile(r'("description":\s*")(.*?)(",)', regex.DOTALL)
    
    def replace_quotes(match):
        content = match.group(2)
        quote_chars = ['"', '„', '”', "'", '|', '&quot;', '&#39;', '&ldquo;', '&rdquo;', '&lsquo;', '&rsquo;']
        quotes_found = {char: content.count(char) for char in quote_chars if content.count(char) > 0}
        if quotes_found:
            print(f"   - JSON description (with spaces): found quotes {quotes_found}")
        
        content_clean = content
        for char in quote_chars:
            content_clean = content_clean.replace(char, '')
        content_clean = content_clean.replace('\\"', '')  # Handle escaped quotes
        
        chars_removed = len(content) - len(content_clean)
        if chars_removed > 0:
            print(f"   - JSON description (with spaces): eliminat {chars_removed} caractere")
        return match.group(1) + content_clean + match.group(3)
    
    return pattern.sub(replace_quotes, html_content)

def remove_quotes_from_json_description_no_spaces(html_content):
    """Curăță "description":"..." """
    pattern = regex.compile(r'("description":")(.*?)(",)', regex.DOTALL)
    
    def replace_quotes(match):
        content = match.group(2)
        quote_chars = ['"', '„', '”', "'", '|', '&quot;', '&#39;', '&ldquo;', '&rdquo;', '&lsquo;', '&rsquo;']
        quotes_found = {char: content.count(char) for char in quote_chars if content.count(char) > 0}
        if quotes_found:
            print(f"   - JSON description (no spaces): found quotes {quotes_found}")
        
        content_clean = content
        for char in quote_chars:
            content_clean = content_clean.replace(char, '')
        content_clean = content_clean.replace('\\"', '')  # Handle escaped quotes
        
        chars_removed = len(content) - len(content_clean)
        if chars_removed > 0:
            print(f"   - JSON description (no spaces): eliminat {chars_removed} caractere")
        return match.group(1) + content_clean + match.group(3)
    
    return pattern.sub(replace_quotes, html_content)

def replace_h3_with_h2(html_content):
    """Înlocuiește h3 class="text_obisnuit2" cu h2 class="text_obisnuit2" """
    # For h3 without quotes on class
    pattern1 = regex.compile(r'<h3(\s+class=text_obisnuit2[^>]*)>(.*?)</h3>', regex.DOTALL)
    h3_matches1 = pattern1.findall(html_content)
    if h3_matches1:
        print(f"   - Found {len(h3_matches1)} h3 tags with class=text_obisnuit2 (no quotes)")
    
    # For h3 with quotes on class
    pattern2 = regex.compile(r'<h3(\s+class="text_obisnuit2"[^>]*)>(.*?)</h3>', regex.DOTALL)
    h3_matches2 = pattern2.findall(html_content)
    if h3_matches2:
        print(f"   - Found {len(h3_matches2)} h3 tags with class=\"text_obisnuit2\"")
    
    total_changes = len(h3_matches1) + len(h3_matches2)
    if total_changes > 0:
        print(f"   - Replaced {total_changes} h3 tags with h2")
    
    html_content = pattern1.sub(r'<h2 class="text_obisnuit2">\2</h2>', html_content)
    html_content = pattern2.sub(r'<h2 class="text_obisnuit2">\2</h2>', html_content)
    
    return html_content, total_changes

def process_html_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.html'):
            file_path = os.path.join(folder_path, filename)
            print(f'\nProcesare: {filename}')
            
            try:
                with open(file_path, 'r', encoding='utf-8-sig') as file:
                    content = file.read()
                print(f"Successfully read {filename} ({len(content)} characters)")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue
            
            original_length = len(content)
            
            # Apply all cleanups
            content = remove_quotes_from_meta_description(content)
            content = remove_quotes_from_og_description(content)
            content = remove_quotes_from_json_description_spaces(content)
            content = remove_quotes_from_json_description_no_spaces(content)
            content, h3_changes = replace_h3_with_h2(content)
            
            new_length = len(content)
            chars_removed = original_length - new_length
            
            if chars_removed > 0 or h3_changes > 0:
                try:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    print(f"   - File updated successfully! (Removed {chars_removed} characters, {h3_changes} h3 tags replaced)")
                except Exception as e:
                    print(f"   - Error writing {file_path}: {e}")
            else:
                print("   - No changes made to file")

    print('\nToate fișierele au fost procesate.')

# Test
folder_path = r'c:\Folder1\test'
if os.path.exists(folder_path):
    print(f'=== Procesare folder: {folder_path} ===')
    process_html_files(folder_path)
else:
    print(f"Folder not found: {folder_path}")