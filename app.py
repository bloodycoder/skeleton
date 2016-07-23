#coding=utf-8 
# -*- coding:cp936 -*-
import re
import urls
from cgi import parse_qs
from model import Model
class application:
    """
    造轮子计划1073(a clean python web frame):
    使用方法
    常量:self.method,用来判断是post,get
    内置的几个方法:getTemplate,getPost
    如果要访问数据库,
    Model.build_connect 
    Model.exec_ins()
    Model.close()
    """
    def __init__(self,environ,start_response):
        self.environ = environ
        self.start = start_response
        self.status = '200 OK'
        self.response_headers = [('Content-type','text/html')]
        self.urls = urls.urls
    def __iter__(self):
        self.method = self.environ['REQUEST_METHOD']
        content = self.getPage()
        self.start(self.status,self.response_headers)
        yield content
    def getPage(self):
        path = self.environ['PATH_INFO']
        for pattern in self.urls:
            m = re.match(pattern[0],path)
            if m:
                function = getattr(self,pattern[1])
                return function()
        return '404 not found'
    def getTemplate(self,tem_name,rep=0):
        #这个函数返回内容,tem_name是文件名字
        #参数rep是一个字典，默认为0
        f = open('template/'+tem_name)
        html = f.read()
        if(rep!=0):
            for to_replace in rep:
                strinfo = re.compile('\{\%\s*'+str(to_replace)+'\s*\%\}')
                html = strinfo.sub(rep[to_replace],html)
        return html
    def getPost(self,item):
        if(self.environ['REQUEST_METHOD'] == 'POST'):
            request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
            request_body = self.environ['wsgi.input'].read(request_body_size)
            d = parse_qs(request_body)
            return d.get(item,[])[0]
    """
    *********************************************
    *add your function here.                    *
    *For example                                *
    *def func_index(self):                      *
    *    self.status = '200 OK'                 *
    *    return self.getTemplate('about_me.htm')*
    *********************************************
    """
    def func_index(self):
        self.status = '200 OK'
        return self.getTemplate('about_me.htm')
    def func_comment(self):
        self.status = '200 OK'
        return self.getTemplate('about_me.htm',{'pig':'lol'})
    def get_environ(self):
        self.status = '200 OK'
        html = ''
        for x in self.environ:
            html = html + str(x) + ':::'+str(self.environ[x]) + '<br>'
        return html
    def post_test(self):
        self.status = '200 OK'
        if(self.method == 'GET'):
            return self.getTemplate('post.html')
        elif(self.method == 'POST'):
            html = ''+self.getPost('fname')+'<br>'
            for x in self.environ:
                html = html + str(x) + ':::'+ str(self.environ[x])+'<br>'
            return html