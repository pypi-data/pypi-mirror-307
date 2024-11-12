import os, re, subprocess, json

patterns = [
    r'(?i)api[_-]?key\s*[:=]\s*[\'"]?[a-zA-Z0-9]{32,}[\'"]?',               
    r'(?i)secret[_-]?key\s*[:=]\s*[\'"]?[a-zA-Z0-9]{32,}[\'"]?',             
    r'(?i)password\s*[:=]\s*[\'"]?[a-zA-Z0-9@#%]{8,}[\'"]?',                
    r'(?i)(aws|amazon|aws_)?_?access[_-]?key[_-]?id\s*[:=]\s*[\'"]?[A-Z0-9]{20}[\'"]?', 
    r'(?i)(aws|amazon|aws_)?_?secret[_-]?access[_-]?key\s*[:=]\s*[\'"]?[A-Za-z0-9/+=]{40}[\'"]?',
    r'(?i)(AWSSQSSECRETACCESSKEY|AWSSQSACCESSKEY|AWSBUCKET)\s*[:=]\s*[\'"]?[A-Za-z0-9/+=]{20,}[\'"]?', 
    r'(?i)AWSSQSACCESSKEY\s*[:=]\s*\${AWS_SQS_ACCESS_KEY:[\w/-]+}',
    r'(?i)AWSSQSSECRETACCESSKEY\s*[:=]\s*\${AWS_SQS_SECRET_ACCESS_KEY:[\w/-]+}',   
    r'(?i)AWSS3SECRETACCESSKEY\s*[:=]\s*\${AWS_S3_SECRET_ACCESS_KEY:[\w/-]+}',
    r'(?i)AWSS3ACCESSKEY\s*[:=]\s*[\'"]?[A-Za-z0-9/+=]{20,}[\'"]?', 
    r'(?i)AWSS3ACCESSKEY\s*[:=]\s*\${AWS_S3_ACCESSKEY:[\w/-]+}',
    r'(?i)(x-)?auth[-_]token\s*[:=]\s*[\'"]?[a-zA-Z0-9-_]{20,}[\'"]?',       
    r'(?i)oauth[_-]?client[_-]?id\s*[:=]\s*[\'"]?[a-zA-Z0-9-_]{20,}[\'"]?',  
    r'(?i)oauth[_-]?client[_-]?secret\s*[:=]\s*[\'"]?[a-zA-Z0-9-_]{20,}[\'"]?', 
    r'(?i)bearer\s+[a-zA-Z0-9-_]{20,}',                                     
    r'(?i)jwt\s*[:=]\s*[\'"]?[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+[\'"]?', 
    r'(?i)slack[_-]?token\s*[:=]\s*[\'"]?[a-zA-Z0-9-]{20,}[\'"]?',          
    r'(?i)database[_-]?url\s*[:=]\s*[\'"]?[^\'"\s]+[\'"]?',                 
    r'(?i)(access|auth|api|client|token|jwt|bearer|password|key)[-_]?(key|token|secret)?\s*[:=]\s*[\'"]?[a-zA-Z0-9-_]{20,}[\'"]?'
    r'\b([A-Za-z0-9+/]{32,}==)\b',                                          
    r'(?i)azure[_-]?access[_-]?key\s*[:=]\s*[\'"]?[A-Za-z0-9/+=]{40}[\'"]?', 
    r'(?i)google[_-]?cloud[_-]?api[_-]?key\s*[:=]\s*[\'"]?[A-Za-z0-9]{39}[\'"]?', 
    r'(?i)gcp[_-]?service[_-]?account[_-]?key\s*[:=]\s*[\'"]?[A-Za-z0-9/+=]{40}[\'"]?', 
    r'(?i)heroku[_-]?api[_-]?key\s*[:=]\s*[\'"]?[A-Za-z0-9]{32}[\'"]?',    
    r'(?i)digitalocean[_-]?api[_-]?key\s*[:=]\s*[\'"]?[A-Za-z0-9]{64}[\'"]?', 
    r'(?i)stripe[_-]?secret[_-]?key\s*[:=]\s*[\'"]?[sk_test|sk_live]\_[a-zA-Z0-9]{32}[\'"]?',  
    r'(?i)sendgrid[_-]?api[_-]?key\s*[:=]\s*[\'"]?[A-Za-z0-9]{32}[\'"]?',   
    r'(?i)twilio[_-]?auth[_-]?token\s*[:=]\s*[\'"]?[a-zA-Z0-9]{32}[\'"]?', 
    r'(?i)github[_-]?token\s*[:=]\s*[\'"]?[a-zA-Z0-9]{40}[\'"]?',            
    r'(?i)gitlab[_-]?ci[_-]?token\s*[:=]\s*[\'"]?[a-zA-Z0-9]{20}[\'"]?',     
    r'(?i)bitbucket[_-]?access[_-]?token\s*[:=]\s*[\'"]?[a-zA-Z0-9]{40}[\'"]?', 
    r'(?i)docker[_-]?hub[_-]?token\s*[:=]\s*[\'"]?[a-zA-Z0-9]{32}[\'"]?',    
    r'(?i)firebase[_-]?auth[_-]?token\s*[:=]\s*[\'"]?[a-zA-Z0-9]{64}[\'"]?', 
    r'(?i)mailgun[_-]?api[_-]?key\s*[:=]\s*[\'"]?[A-Za-z0-9]{32}[\'"]?',    
    r'(?i)zoom[_-]?jwt[_-]?token\s*[:=]\s*[\'"]?[a-zA-Z0-9]{64}[\'"]?',     
    r'(?i)aws[_-]?s3[_-]?access[_-]?key[_-]?id\s*[:=]\s*[\'"]?[A-Z0-9]{20}[\'"]?', 
    r'(?i)aws[_-]?s3[_-]?secret[_-]?access[_-]?key\s*[:=]\s*[\'"]?[A-Za-z0-9/+=]{40}[\'"]?', 
    r'(?i)mongodb[_-]?url\s*[:=]\s*[\'"]?mongodb\+srv:\/\/[a-zA-Z0-9]+:[a-zA-Z0-9]+@[\w.-]+\/[\w.-]+[\'"]?', 
    r'(?i)postgresql[_-]?url\s*[:=]\s*[\'"]?postgres:\/\/[a-zA-Z0-9]+:[a-zA-Z0-9]+@[\w.-]+\/[\w.-]+[\'"]?', 
    r'(?i)mysql[_-]?url\s*[:=]\s*[\'"]?mysql:\/\/[a-zA-Z0-9]+:[a-zA-Z0-9]+@[\w.-]+\/[\w.-]+[\'"]?', 
    r'(?i)redis[_-]?url\s*[:=]\s*[\'"]?redis:\/\/[a-zA-Z0-9]+:[a-zA-Z0-9]+@[\w.-]+:[0-9]+[\'"]?',
    r'(?i)azure\s*storage\s*account\s*key\s*[:=]\s*[\'"]?[A-Za-z0-9]{88}[\'"]?',
    r'(?i)google\s*cloud\s*api\s*key\s*[:=]\s*[\'"]?[A-Za-z0-9-_]{39}[\'"]?',
    r'(?i)google_cloud_access_key\s*[:=]\s*[\'"]?[A-Za-z0-9]{32}[\'"]?',  
    r'(?i)google_cloud_secret_key\s*[:=]\s*[\'"]?[A-Za-z0-9/+=]{40}[\'"]?', 
    r'(?i)ghp_[A-Za-z0-9]{36}',  
    r'(?i)AIza[0-9A-Za-z-_]{35}', 
    r'(?i)glpat-[A-Za-z0-9]{20}', 
    r'(?i)mysql[_-]?password\s*[:=]\s*[\'"]?[A-Za-z0-9!@#$%^&*()_+]{8,}[\'"]?',  
    r'(?i)mysql[_-]?user\s*[:=]\s*[\'"]?[A-Za-z0-9]{3,}[\'"]?',  
    r'(?i)mysql[_-]?host\s*[:=]\s*[\'"]?[A-Za-z0-9.-]+[\'"]?', 
    r'(?i)postgres[_-]?password\s*[:=]\s*[\'"]?[A-Za-z0-9!@#$%^&*()_+]{8,}[\'"]?',  
    r'(?i)postgres[_-]?user\s*[:=]\s*[\'"]?[A-Za-z0-9]{3,}[\'"]?',
    r'(?i)postgres[_-]?host\s*[:=]\s*[\'"]?[A-Za-z0-9.-]+[\'"]?',  

]

def get_files_in_repo():
    result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True, encoding='utf-8')
    return result.stdout.splitlines()

def detect_secrets(text):
    secrets_found = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        secrets_found.extend(matches)
    return secrets_found

def is_binary_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            f.read()
        return False
    except (UnicodeDecodeError, FileNotFoundError):
        return True
    
def get_repo_root():
    result = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True, encoding='utf-8')
    return result.stdout.strip()
def create_file_link(file_path):
    repo_root = get_repo_root()  
    return f"{repo_root}/{file_path}"


def analyze_repository():
    files = get_files_in_repo()
    results = []
    total_secrets_count = 0  
    seen_files = set() 

    for file_path in files:
        file_path = file_path.strip('"').strip()  

        if not os.path.exists(file_path):
            print(f"Arquivo não encontrado ou inacessível: {file_path}")
            continue
        
        if is_binary_file(file_path):
            continue
        
        if file_path in seen_files:  
            continue

        seen_files.add(file_path)  

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                file_content = f.read()
                detected_secrets = detect_secrets(file_content)
                
                if detected_secrets:
                    unique_secrets = list(set(detected_secrets))
                    results.append({
                        'file': create_file_link(file_path),
                        'secrets': unique_secrets
                    })
                    total_secrets_count += len(unique_secrets)
        except Exception as e:
            print(f"Erro ao ler o arquivo {file_path}: {str(e)}")

    report = {
        'total_secrets': total_secrets_count,
        'files': results
    }
    
    with open('secrets_report.json', 'w') as report_file:
        json.dump(report, report_file, indent=4)
    
    print(f"Relatório gerado: secrets_report.json")
    print(f"Quantidade de secrets detectadas: {total_secrets_count}")

if __name__ == "__main__":
    report = analyze_repository()
    print(report)
