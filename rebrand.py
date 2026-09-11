import os
import re

dirs_to_scan = ['backend', 'netramitra-frontend', 'docs', 'deployment']
ignore_dirs = ['.git', 'node_modules', 'venv', '__pycache__', '.next', 'out', 'build', '.pytest_cache']
ignore_exts = ['.png', '.jpg', '.jpeg', '.mat', '.whl', '.pyc']

replacements = [
    (r'NetraMitra', 'NetraMitra'),
    (r'NETRAMITRA', 'NETRAMITRA'),
    (r'Netra Mitra', 'Netra Mitra'),
    (r'netramitra-frontend', 'netramitra-frontend'),
    (r'netramitra-backend', 'netramitra-backend'),
]

for d in dirs_to_scan:
    if not os.path.exists(d): continue
    for root, dirs, files in os.walk(d):
        dirs[:] = [di for di in dirs if di not in ignore_dirs]
        for f in files:
            if any(f.endswith(ext) for ext in ignore_exts):
                continue
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                new_content = content
                for old, new in replacements:
                    new_content = re.sub(old, new, new_content)
                
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    print(f'Updated: {path}')
            except Exception as e:
                pass

# Also check root files
for f in os.listdir('.'):
    if os.path.isfile(f) and not any(f.endswith(ext) for ext in ignore_exts):
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
            new_content = content
            for old, new in replacements:
                new_content = re.sub(old, new, new_content)
            if new_content != content:
                with open(f, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f'Updated: {f}')
        except:
            pass
