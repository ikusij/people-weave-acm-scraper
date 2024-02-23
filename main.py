import titles
import info

import json
import time

if __name__ == "__main__":

    conference_abb = titles.main()

    with open("titles.json", "r") as read:
        json_file = json.load(read)
    
    write = open("info.json", "w")
    
    try:
        
        for json_object, abb in zip(json_file.values(), conference_abb):
        
            print(abb)
            info.main(abb, json_object)
            time.sleep(60)
        
        write.write(json.dumps(json_file, indent = 4))
    
    except Exception as error:

        print(error)
        
        write.write(json.dumps(json_file, indent = 4))
    
