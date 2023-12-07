import json, csv, sys

results = []
for line in list(csv.reader(sys.stdin))[1:]:
    try:
        results.append({
            'tag': line[0],
            'file_name': line[1],
            'full_arch': line[2],
            'chunk_arch': line[3],
            'full_length': int(line[4]),
            'chunk_length': int(line[5]),
            'chunk_count': int(line[6]),
            'file_type': line[7],
            'sha256': line[8],
            'shannon_entropy': float(line[9])
            })
    except:
        pass
    
print(json.dumps(results))
