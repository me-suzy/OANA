import os
import regex

def remove_quotes_from_meta_description(html_content):
    """Curăță meta name="description" """
    pattern = regex.compile(r'(<meta name="description" content=")(.*?)(">)', regex.DOTALL)
    
    def replace_quotes(match):
        content_clean = (match.group(2)
                        .replace('„', '')
                        .replace('"', '')  
                        .replace('"', '')
                        .replace('"', '')
                        .replace('|', ''))
        return match.group(1) + content_clean + match.group(3)
    
    return pattern.sub(replace_quotes, html_content)

def remove_quotes_from_og_description(html_content):
    """Curăță meta property="og:description" - CORECTAT"""
    # Pattern simplu și direct pentru tag-ul care se termină cu "/>
    pattern = regex.compile(r'(<meta property="og:description" content=")(.*?)("\s*/>)', regex.DOTALL)
    
    def replace_quotes(match):
        content_clean = (match.group(2)
                        .replace('„', '')
                        .replace('"', '')
                        .replace('"', '')  
                        .replace('"', '')
                        .replace('|', ''))
        chars_removed = len(match.group(2)) - len(content_clean)
        if chars_removed > 0:
            print(f'   - OG description: eliminat {chars_removed} caractere')
        return match.group(1) + content_clean + match.group(3)
    
    return pattern.sub(replace_quotes, html_content)

def remove_quotes_from_json_description_spaces(html_content):
    """Curăță "description": "..." """
    pattern = regex.compile(r'("description":\s*")(.*?)(",)', regex.DOTALL)
    
    def replace_quotes(match):
        content_clean = (match.group(2)
                        .replace('„', '')
                        .replace('"', '')
                        .replace('"', '')
                        .replace('"', '')  
                        .replace('|', ''))
        return match.group(1) + content_clean + match.group(3)
    
    return pattern.sub(replace_quotes, html_content)

def remove_quotes_from_json_description_no_spaces(html_content):
    """Curăță "description":"..." """
    pattern = regex.compile(r'("description":")(.*?)(",)', regex.DOTALL)
    
    def replace_quotes(match):
        content_clean = (match.group(2)
                        .replace('„', '')
                        .replace('"', '')
                        .replace('"', '')
                        .replace('"', '')
                        .replace('|', ''))
        return match.group(1) + content_clean + match.group(3)
    
    return pattern.sub(replace_quotes, html_content)

def replace_h3_with_h2(html_content):
    """Înlocuiește h3 class="text_obisnuit2" cu h2 class="text_obisnuit2" """
    # Pentru h3 fără ghilimele la class
    pattern1 = regex.compile(r'<h3(\s+class=text_obisnuit2[^>]*)>(.*?)</h3>', regex.DOTALL)
    html_content = pattern1.sub(r'<h2 class="text_obisnuit2">\2</h2>', html_content)
    
    # Pentru h3 cu ghilimele la class  
    pattern2 = regex.compile(r'<h3(\s+class="text_obisnuit2"[^>]*)>(.*?)</h3>', regex.DOTALL)
    html_content = pattern2.sub(r'<h2 class="text_obisnuit2">\2</h2>', html_content)
    
    return html_content

def process_html_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.html'):
            file_path = os.path.join(folder_path, filename)
            print(f'Procesare: {filename}')
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            original_length = len(content)
            
            # Aplică toate curățările
            content = remove_quotes_from_meta_description(content)
            content = remove_quotes_from_og_description(content) 
            content = remove_quotes_from_json_description_spaces(content)
            content = remove_quotes_from_json_description_no_spaces(content)
            content = replace_h3_with_h2(content)
            
            new_length = len(content)
            chars_removed = original_length - new_length
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            print(f'   - Total caractere eliminate: {chars_removed}')

# Test
folder_path = r'c:\Folder1\test'
if os.path.exists(folder_path):
    print(f'=== Procesare folder: {folder_path} ===')
    process_html_files(folder_path)