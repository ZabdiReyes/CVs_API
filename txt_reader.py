import re
class TxtReader:
    file_path = None
    
    margin = 0
    number_of_pages = 0
    pages = {}
    
    name = None
    
    full_dictionary = {}
    dic1 = {}
    dic2 = {}
    dic1_indexes = {}
    mongodic1 = {}
    mongodic2 = {}
    

    def read(self, file_path: str):
        #file_path = self.directory_path + file_path
        try:
            with open(file_path, 'r', newline="",encoding='utf-8') as file:
                self.__var_reset()
                content = file.read()
                lineas = re.split(r'\r\n|\f', content)
                self.full_dictionary = {i: linea for i, linea in enumerate(lineas, start=1)} # Crear el diccionario enumerado
                self.__calculate_margin() ##checked
                self.__calculate_pages_properties() ##checked
                '''self.__extract_pages_indexes() ##Legacy'''
                ##self.__calculate_experience_index()
                self.__fill_split_dictionaries()
                self.name = self.full_dictionary[1][self.margin:]
                self.transform_dic_to_mongo(self.dic1,self.dic2)
                
        except FileNotFoundError:
            print(f"The file {super.file} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def __var_reset(self):
            
            self.margin = 0
            self.number_of_pages = 0
            self.pages = {}
            
            self.name = None
            
            self.full_dictionary = {}
            self.dic1 = {}
            self.dic2 = {}
            self.dic1_indexes = {}
    
    def __calculate_margin(self):
        line = self.full_dictionary[1]
        #print(line)
        margin = 0
        flag = 0
        if line.startswith("Contactar"):
            #print("Flag 1")
            flag = 1
        elif line.startswith("Contact"):
            #print("Flag 2")
            flag = 2
        
        if flag == 1:
            line = line[9:]
        if flag == 2:
            line = line[7:]
        if flag == 0:
            print("Failed to calculate margin.")
            return -1
        
        #Check for each char until a non-space char is found
        for char in line:
            if char == ' ':
                margin += 1
            else:
                break
        
        if flag == 1:
            margin += 9
        if flag == 2:
            margin += 7
        
        self.margin = margin -1
        
        return 0
    
    def look_for_in_dictionary(self,dictionary : dict,keyword : str):
        res = []
        for i in range(1,len(dictionary)+1):
            
            if keyword in dictionary.get(i):
                res.append(i)
        
            
        return res
    
    def __calculate_pages_properties(self):
        
        if self.full_dictionary == 0:
            print("File content is empty or doesnt follow the expected format.")
            self.number_of_pages = 0
            return -1
        
        first_page = self.look_for_in_dictionary(self.full_dictionary,f"Page 1 of ")
        number_of_pages_line = self.full_dictionary[int(first_page[0])]
        self.number_of_pages = int(number_of_pages_line.split("Page 1 of ")[1])
        
        pages_indexes = []
        for i in range(1,self.number_of_pages+1):
            pages_indexes.append(self.look_for_in_dictionary(self.full_dictionary,f"Page {i} of {self.number_of_pages}"))
            index_line = int(pages_indexes[i-1][0])
            #Dictionary with page_id and index_line{i : index_line}
            #self.full_dictionary[index_line] = f"Page {i} of {self.number_of_pages}"
            self.pages[i] = index_line
        return 0
    
    def get_current_page(self, line_index: int):
        
        if not self.full_dictionary:
            print("File content is empty. a")
            return 0
          
        for i in range(1, self.number_of_pages+1):
            
            #print(line_index," :", self.pages[i])
            if (line_index <= self.pages[i]):
                return i
        
        print("line_index out of range in get_current_page")
        return -1
    
    def print_content_full_dictionary(self):
        for i in range(1,len(self.full_dictionary)+1):
            print(i," : ",self.full_dictionary[i])
    
    def __calculate_dic1_indexes(self):
        
        for i in range(1,len(self.dic1)+1):
            line = self.dic1[i]
            
    
    def __fill_split_dictionaries(self):
        
        dic2_pages = 1
        for i in range(self.number_of_pages,0,-1):
            empty_lines = 0
            for j in range(self.pages[i]-5,self.pages[i]):
                line = self.full_dictionary[j]
                line = line[:self.margin]
                line = line.replace(" ","")
                if(line == ""):
                    empty_lines += 1
                    
            if empty_lines > 4:
                dic2_pages = i
                break
            
        #print("esta es la ultima pagina con contenido :",dic2_pages)
        
        for i in range(1,len(self.full_dictionary)+1):
            line = self.full_dictionary[i]
            if i <= self.pages[dic2_pages]:
                self.dic2[i] = line[:self.margin]
                self.dic1[i] = line[self.margin:]
            else:
                self.dic1[i] = line
                
    def print_dic(self, dictionary : dict):
        for i in range(1,len(dictionary)+1):
            print(i," : ",dictionary[i])
            
    def transform_dic_to_mongo(self,dic1 : dict,dic2 : dict):
        self.mongodic1 = {f'p{key}': value for key, value in dic1.items()}
        self.mongodic2 = {f'p{key}': value for key, value in dic2.items()}