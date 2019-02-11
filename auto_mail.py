#Editor Evan Lee
def sendDD():
    import smtplib
    from email.mime.text import MIMEText
    from IPython.display import HTML
    from email.mime.multipart import MIMEMultipart
    import pandas as pd 


    def send_data(html_msg):
        smtp_ssl_host = 'smtp.mail.yahoo.com'  # smtp.mail.yahoo.com
        smtp_ssl_port = 465

        user = 'slps20425' 
        passwd = "bb-PO68Q27"


        sender = 'slps20425@yahoo.com.tw' 
        targets ='eason_s@hotmail.com'

        msg = MIMEMultipart('related')
        #msg = MIMEText('Hi, how are you today?','plain','utf-8')
        msg['From'] = sender
        msg['To'] = targets
        msg['Subject'] = 'Hello'
        #msg.attach(MIMEText('hello', 'plain', 'utf-8'))

        content_html = MIMEText(html_msg, "html", "utf-8")
        msg.attach(content_html)

        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port, timeout=10)
        print('server')
        server.set_debuglevel(1)

        server.login(user, passwd)
        print('login')
        server.sendmail(sender, targets, msg.as_string())
        server.quit()

    def path_to_image_html(path):

        return '<img src="'+ path + '" style=max-height:124px;"/>'
        
    def path_to_url_clickable(path):
        return '<a href="{}"></a>'.format(path)


    def get_html_msg():

        df =pd.read_csv('Data_test.csv',sep=',')
        pd.set_option('display.max_colwidth', -1) 
        df['Image']=path_to_image_html(df['Image'])
        html_string = '''
        <html><head><Title>Filtered Rent info</Title><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous"></head><body>{table}</body></html>
        '''

        path_to_url_clickable(df['SubURL'])
        with open('test.html', 'w') as f:
              f.write(html_string.format(table=df.to_html(classes="dataframe table table-hover table-condensed table-bordered",escape=False)))    
        html_msg = open('test.html').read() 

        # with open('test.html', 'w') as fobj:
        # fobj.write('<html><head>('<link href="css/bootstrap.css" rel="stylesheet"></head><body>')
        # df.to_html(fobj,classes="dataframe table table-hover table-condensed table-bordered",escape=False)
        # fobj.write('</body></html>')
        # html_msg= '11'
        # 这里是将HTML文件输出，作为测试的时候，查看格式用的，正式脚本中可以注释掉
        
        # fout = open('t4.html', 'w', encoding='UTF-8', newline='')
        # fout.write(html_msg)
        return html_msg
    html_msg = get_html_msg()
    send_data(html_msg)
                
if __name__ == '__main__':
    sendDD()
    