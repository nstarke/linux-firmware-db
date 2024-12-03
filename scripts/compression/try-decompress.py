import zlib, sys, lzma, bz2, threading, copy, json

DECOMPRESSION_CHAMBER_PATH = "/tmp/decompression-chamber"
DIVISOR = 4

def do_bz2(compressed_data, metadata):
    data_length = len(compressed_data)
    for i in range(int(data_length * 0.65)):
        try: 
            unzipped = bz2.decompress(compressed_data[i:])
        except Exception as ex:
            continue
        if len(unzipped) > int((data_length / DIVISOR)):
            print ('BZ2: Offset Found', i)
            with open(DECOMPRESSION_CHAMBER_PATH + '/result-bz2-' + metadata['sha256'] + '.bin', 'wb') as result:
                result.write(unzipped);
                result.close()
                break
        

def do_lzma(compressed_data, metadata):
    data_length = len(compressed_data)
    for i in range(int(data_length * 0.65)):
        try: 
            unzipped = lzma.decompress(compressed_data[i:])
        except Exception as ex:
            continue
        if len(unzipped) > int((data_length / DIVISOR)):
            print ('LZMA: Offset Found', i)
            with open(DECOMPRESSION_CHAMBER_PATH + '/result-lzma-' + metadata['sha256'] + '.bin', 'wb') as result:
                result.write(unzipped);
                result.close()
                break
        
        
def do_zlib(compressed_data, metadata):
    data_length = len(compressed_data)
    for i in range(int(data_length * 0.65)):
        try:
            unzipped = zlib.decompress(compressed_data[i:], -zlib.MAX_WBITS)
        except Exception as ex:
            continue

        if len(unzipped) > int((data_length / DIVISOR)):
            print ('GZIP: Offset found', i)
            with open(DECOMPRESSION_CHAMBER_PATH + '/result-gz-' + metadata['sha256']  + '.bin', 'wb') as result:
                result.write(unzipped);
                result.close()
                break
        
tag = sys.argv[1]
with open("../data/json/linux-firmware-db-" + tag + "-cpu_rec.json", 'r') as f:
    j = json.loads(f.read())
    for i in j:
        if float(i['shannon_entropy']) > 6.9:
            print ("trying: " + i['file_name'])
            with open("../git/linux-firmware/" + i['file_name'], 'rb') as compressed_data:
                compressed_data = compressed_data.read()
                thread_zlib = threading.Thread(target=do_zlib, args=(copy.copy(compressed_data),i))
                thread_lzma = threading.Thread(target=do_lzma, args=(copy.copy(compressed_data),i))
                thread_bz2 = threading.Thread(target=do_bz2, args=(copy.copy(compressed_data),i))
                thread_zlib.start()
                thread_lzma.start()
                thread_bz2.start()
                thread_zlib.join()
                thread_lzma.join()
                thread_bz2.join()