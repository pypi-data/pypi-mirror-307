import json
import re
import xml.etree.ElementTree as ET
'''
读取和分析： Eclipse source Template 
           VSCode Source Snippets
互相转换：  Eclipse source Template 和 VSCode Source Snippets 
返回数据： {'name':'','description':'','content':''}
'''
class SnippetConvertor():
    DATA={'name':'','description':'','content':''}
    NAME = 'name'
    DESC = 'description'
    CONTENT = 'content'
    def __init__(self) -> None:
        pass
    
    @classmethod
    def eclipseToVSCode(cls,xmlTemplateFile,jsonSnippetFile):
        '''
        Eclipse source Template  => VSCode Source Snippets 
        :xmlTemplateFile: Eclipse 模版文件
        :jsonSnippetFile: VSCode 模版文件
        '''
        contentList = cls.readEclipseTemplate(xmlTemplateFile)
        cls.generateVSCodeSinppets(jsonSnippetFile,contentList)

    @classmethod
    def vsCodeToEclipse(cls,jsonSnippetFile,xmlTemplateFile):
        '''
        VSCode Source Snippets => Eclipse source Template 
        :xmlTemplateFile: Eclipse 模版文件
        :jsonSnippetFile: VSCode 模版文件
        '''
        contentList = cls.readVSCodeSinppet(jsonSnippetFile)
        cls.generateEclipseTemplate(xmlTemplateFile,contentList)
    
    # <template autoinsert="true" context="ABAP" deleted="false" description="表技术字段赋值" 
    # enabled="true" name="addinfofields">source code 
    @classmethod
    def readEclipseTemplate(cls,xmlFile):
        '''
        读取和分析Eclipse 模板文件内容
        :xmlFile: Eclipse 模版文件
        返回:
            字典: {'name':'','description':'','content':''}
        '''
        xmlTree = ET.parse(xmlFile)
        root = xmlTree.getroot()
        templates = []
        # 遍历每一个 template 元素
        for template in root.findall('template'):
            # 获取 template 的名称和内容
            # Eclipse 中 copy 代码 尾部 有 '\r\n'
            templates.append({cls.NAME:template.get('name'),cls.DESC:template.get('description'),cls.CONTENT:cls.splitContentStringIntoList(template.text)})
        return templates
        
    @classmethod
    def generateEclipseTemplate(cls,xmlFile,contentList):
        '''
        生成 Eclipse 模板文件
        :xmlFile: Eclipse 模版文件
        contentList：{'name':'','description':'','content':''}
        '''
         # <template autoinsert="true" context="ABAP" deleted="false" description="表技术字段赋值" enabled="true" name="addinfofields">
        # 创建根元素
        root = ET.Element('templates')
        for contenet in contentList:
            templateElement = ET.SubElement(root, 'template')
            content= '\r'.join(contenet.get(cls.CONTENT))
            templateElement.text = content  
            templateElement.attrib['description']= contenet.get(cls.DESC)
            templateElement.attrib['autoinsert']="true" 
            templateElement.attrib['context']="ABAP" 
            templateElement.attrib['deleted']="false" 
            templateElement.attrib['enabled']="true" 
            templateElement.attrib['name']= str(contenet.get(cls.NAME)).lower
            templateElement.tag= 'template'
        # 创建ElementTree对象
        xmlTree = ET.ElementTree(root)
        # <?xml version="1.0" encoding="UTF-8" standalone="no"?>
        # 将XML保存到文件中
        xmlTree.write(xmlFile,encoding="UTF-8",xml_declaration=True)
    
    @classmethod
    def readVSCodeSinppet(cls,jsonFile):
        '''
        读取和分析 VSCode 模板文件内容
        :jsonFile: VSCode 模版文件
        返回:
            字典: {'name':'','description':'','content':''}
        '''
        resultList=[]
        fileContent = ''
        with open(jsonFile,'r',encoding='UTF-8',errors='ignore') as f:
            fileContent = f.read() 
        snipDict = eval(fileContent)  
        for key in  snipDict:
            resultList.append({
                cls.NAME:snipDict.get(key).get('prefix'),
                cls.DESC:snipDict.get(key).get('description'),
                cls.CONTENT:snipDict.get(key).get('body')
            })
        return resultList
    
    @classmethod
    def generateVSCodeSinppets(cls,jsonFile,contentList):
        '''
        生成 VSCode 模板文件
        :jsonFile: VSCode 模版文件
        contentList：{'name':'','description':'','content':''}
        '''
        snippets = {}
        for content in contentList:
            snipObj = cls.generateVSCodeSinppetObject(content.get(cls.CONTENT),content.get(cls.NAME),content.get(cls.DESC))
            snippets[content.get(cls.NAME)] = snipObj
        snippetJson= json.dumps(snippets,ensure_ascii=False)
        with open(jsonFile,'w',encoding='UTF-8') as f:
            f.write(snippetJson)
                
    @staticmethod
    def generateVSCodeSinppetObject(bodyList, prefix, description, tabSize=3)->dict:
        '''
        生成单个snippet 
        :bodyList:      内容
        :tabSize:           Tab占几位字符
        :prefix:            提示关键字
        :description:       描述
        返回:
            Dict:  {
                                "prefix": "#PREFIX#",
                                "description": "#DESCRIPTION#",
                                "body": [
                                    #TOKEN#
                                        ]
                                }
        '''
        tabIdentifier = tabSize * ' '
        tabDelimiter = '\t'
        escapeStr = '\\"'
        # bodyLineseparator = ',\n\t\t\t'
        sinppetObject = { "prefix": "",
                        "body": [ ],
                        "description": ""
                        }
        contentList = bodyList # contentString.split(endOfLineSequence)
        snippetBodyList = []
        bodyString = ''
        prefixLow=str(prefix).lower()
        for line in contentList:
            line = line.replace(tabDelimiter,tabIdentifier )  #tab和空格缩进
            # line = line.replace('"', escapeStr) #内容中有双引号需要加转义符 EscapeDoubleQuotes
            # line =  '"' + str(line) + '"'  #双引号 AddDoubleQuotes
            snippetBodyList.append(line)
        # bodyString = bodyLineseparator.join(snippetBodyList)   #换行符+3个Tab
        
        sinppetObject =  { "prefix": prefixLow,
                        "body": snippetBodyList,
                        "description": description
                        }
        return sinppetObject
   
    
    
    @staticmethod
    def splitContentStringIntoList(contentString, endOfLineSequence='\r\n|\n'):
        return re.split(endOfLineSequence,contentString)
        # return contentString.split(endOfLineSequence)

