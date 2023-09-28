#Programın düzgün çalışması için gerekli olan çeşitli kütüphaneleri ve modülleri içe aktarıyoruz.
import discord # Discord API ile etkileşime girmenizi ve Discord botları veya diğer uygulamaları oluşturmanızı sağlar.
from discord.ext import commands # Bu, kodunuzda commands modülü tarafından sağlanan işlevselliği kullanmanıza olanak tanır.
import requests # Bu modül, HTTP istekleri göndermenize ve Python kodunuzdaki yanıtları işlemenize olanak tanır. Web hizmetleri ve API'ler ile etkileşim için uygun bir yol sağlar.
from bs4 import BeautifulSoup # Bu, HTML veya XML belgelerini ayrıştırmak ve işlemek için BeautifulSoup sınıfını kullanmanızı sağlar.
import pandas as pd # Bu, pandas kütüphanesi tarafından sağlanan fonksiyonları ve sınıfları pd ile önekleyerek kullanmamızı sağlar.
import smtplib # Bu modül, Basit Posta Aktarım Protokolü (SMTP) kullanarak e-posta göndermenin bir yolunu sağlar.
from urllib.parse import urljoin # Bu işlev, mutlak bir URL oluşturmak üzere bir temel URL ile bir göreli URL'yi birleştirmek için kullanılır.
from email.mime.multipart import MIMEMultipart # Bu sınıf, metin, HTML ve ekler gibi birden fazla parça içerebilen çok parçalı e-posta iletileri oluşturmak için kullanılır.
from email.mime.text import MIMEText # Bu sınıf, düz metin içerikli e-posta mesajları oluşturmak için kullanılır.
from email.mime.base import MIMEBase # Bu sınıf, Python'da e-posta mesajlarını kodlamak ve kodlarını çözmek için kullanılan MIME nesnelerini oluşturmak için kullanılır.
from email.mime.application import MIMEApplication  # Bu sınıf, e-posta iletileri için MIME uygulama ekleri oluşturmak için kullanılır.
from email import encoders # Bu, kodunuzda encoders modülü tarafından sağlanan işlevleri ve sınıfları kullanmanıza olanak tanır.
import nest_asyncio #Bu modül, asyncio tabanlı kütüphaneleri Jupyter not defterlerinde veya halihazırda çalışan bir olay döngüsüne sahip diğer ortamlarda kullanmanıza olanak tanır. 
#Belirli ortamlarda asyncio kodunu çalıştırmak için gerekli olan iç içe geçmiş olay döngülerine izin vermek için asyncio olay döngüsüne yama yapar.


nest_asyncio.apply()
#nest_asyncio.apply(), asyncio'yu bir Jupyter not defterinde veya halihazırda çalışan bir olay döngüsüne sahip bir ortamda kullanmanızı sağlayan bir fonksiyondur. 
#İç içe geçmiş asyncio olay döngülerinin düzgün çalışmasını sağlamak için olay döngüsüne yama yapar.

intents= discord.Intents.all()
intents.members=True
intents.message_content = True
#Kod, discord modülünden Intents sınıfının bir örneğini oluşturuyor ve bunu intents değişkenine atıyor.

bot = commands.Bot(command_prefix='!', intents=intents)
''' commands modülünden Bot sınıfının bir örneğini oluşturur. 
Komut önekini '!' olarak ve niyetleri intents değişkenine ayarlar. 
Bu kod satırı tipik olarak bir Discord botu için bir bot nesnesi oluşturmak için kullanılır; 
burada komut öneki botun komutlara nasıl yanıt vereceğini ve amaçlar botun hangi olayları dinleyebileceğini belirler.
'''

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

#on_ready işlevi, oturum açıldığında botun adını yazdıran bir olay işleyicisidir.


@bot.command(name='scrape')
async def scrape(ctx):
'''
scrape fonksiyonu botun bir web sitesinden veri kazımasını sağlayan bir komuttur.
  ctx: ctx parametresi "bağlam" anlamına gelir ve komutun yürütüldüğü bağlamı temsil eder. Mesaj, mesajı gönderen kullanıcı, mesajın gönderildiği kanal ve diğer ilgili ayrıntılar hakkında bilgi içerir.
'''

    def scrape_and_save_data():
        data = {
            'Site': [],
            'Title': [],
            'Link': [],
            'Date': []
        }

        def scrape_cbr_anime():
            site_name = "CBR/Anime"
            base_url = 'https://www.cbr.com/'

            url = 'https://www.cbr.com/category/anime/'

            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                article_blocks = soup.find_all('div', class_='w-display-card-content')
                for block in article_blocks:
                    title_element = block.find('h5', class_='display-card-title').find('a')
                    title = title_element.text.strip()
                    relative_link = title_element['href']
                    full_link = urljoin(base_url, relative_link)
                    date_element = block.find('time', class_='display-card-date')['datetime']
                    date = date_element.split('T')[0]

                    data['Site'].append(site_name)
                    data['Title'].append(title)
                    data['Link'].append(full_link)
                    data['Date'].append(date)
        #Buradaki kodların işlevi CBR/Anime web sitesindeki verileri kazır ve bir sözlüğe kaydeder.

        def scrape_hashnode_data_science():
            site_name = "Hashnode/Data Science"
            base_url = 'https://hashnode.com/n/data-science'

            url = 'https://hashnode.com/n/data-science'

            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                post_sections = soup.find_all('section', class_='flex flex-col gap-2 sm:gap-4')
                for section in post_sections:
                    title_element = section.find('h1', class_='font-heading text-base sm:text-xl font-semibold sm:font-bold text-slate-700 dark:text-slate-200 hn-break-words cursor-pointer')
                    title = title_element.text.strip()
                    link_element = title_element.find_parent('a', href=True)
                    link = link_element['href']
                    date_element = section.find('p', class_='text-sm text-slate-500 dark:text-slate-400 font-normal')
                    date = date_element.text.strip()

                    data['Site'].append(site_name)
                    data['Title'].append(title)
                    data['Link'].append(link)
                    data['Date'].append(date)
        #Buradaki kodların işlevi Hashnode web sitesindeki verileri kazır ve bir sözlüğe kaydeder.

        def scrape_wired_science():
            site_name = "Wired/Science"
            base_url = 'https://www.wired.com/'

            url = 'https://www.wired.com/category/science/'

            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                article_blocks = soup.find_all('div', class_='SummaryItemContent-eiDYMl')
                for block in article_blocks:
                    title_element = block.find('h3', class_='SummaryItemHedBase-hiFYpQ')
                    title = title_element.text.strip()
                    relative_link = block.find('a', class_='SummaryItemHedLink-civMjp')['href']
                    full_link = urljoin(base_url, relative_link)
                    category_element = block.find('span', class_='RubricName-fVtemz')
                    category = category_element.text.strip() if category_element else "N/A"
                    date_element = block.find('time')
                    date = date_element.text.strip() if date_element else category

                    data['Site'].append(site_name)
                    data['Title'].append(title)
                    data['Link'].append(full_link)
                    data['Date'].append(date)
        #Buradaki kodların işlevi Wired-Science web sitesindeki verileri kazır ve bir sözlüğe kaydeder.

        def scrape_interesting_engineering():
            site_name = "InterestingEngineering"
            base_url = 'https://interestingengineering.com/'

            url = 'https://interestingengineering.com/news/page/1'

            # Web sitesine bir HTTP GET isteği gönderir
            response = requests.get(url)

            # İsteğin başarılı olup olmadığını kontrol et.
            if response.status_code == 200:
                # BeautifulSoup kullanarak sayfanın HTML içeriğini ayrıştırın.
                soup = BeautifulSoup(response.text, 'html.parser')

                # Makale başlıklarını, URL'leri ve tarih bilgilerini bulun ve yazdırın.
                article_blocks = soup.find_all('div', class_='Category_result__description__iz_rw')  # Gerçek HTML öğesi ve sınıf adıyla değiştirin.
                for block in article_blocks:
                    title_link_element = block.find('a', href=True)
                    title = title_link_element.find('h2', class_='Category_result__header__HQgVv').text.strip()
                    link = urljoin(base_url, title_link_element['href'])  # Temel URL yi göreli bağlantılara ön ekleme
                    author_element = block.find('a', class_='Category_result__author__name__In7jd')
                    author = author_element.text.strip()
                    date_element = block.find('span', class_='Category_result__author__publishTime__nwLBU')
                    date = date_element.text.strip()

                    data['Site'].append(site_name)
                    data['Title'].append(title)
                    data['Link'].append(link)
                    data['Date'].append(date)
        #Buradaki kodların işlevi Interesting-Engineering web sitesindeki verileri kazır ve bir sözlüğe kaydeder.

        def scrape_techcrunch_startups():
            site_name = 'TechCrunch'
            # Burada Techcrunch' ifadesini kazımak istediğiniz web sitesinin gerçek URL'si ile değiştirin..
            url = 'https://techcrunch.com/category/startups/'
           ''' !!! NOT: kazımak istediğiniz wen sitesinin html kodlarını lütfen kontrol ediniz. Her site aynı kazıma işlemleri ile veri çıkarmanıza izin vermeyebilir.'''

            # Web sitesine bir HTTP GET isteği gönderin.
            response = requests.get(url)

            # İsteğin başarılı olup olmadığını kontrol edin.
            if response.status_code == 200:
                # BeautifulSoup kullanarak sayfanın HTML içeriğini ayrıştırın.
                soup = BeautifulSoup(response.text, 'html.parser')

                # Blog gönderilerinin başlıklarını, bağlantılarını ve tarihlerini bulun ve yazdırın.
                post_blocks = soup.find_all('div', class_='post-block')  
                for block in post_blocks:
                    title = block.find('h2', class_='post-block__title').text.strip()
                    link = block.find('a', class_='post-block__title__link')['href']
                    date_element = block.find('time')
                    date = date_element.text  
                    data['Site'].append(site_name)
                    data['Title'].append(title)
                    data['Link'].append(link)
                    data['Date'].append(date)
        #Buradaki kodların işlevi Techcrunch web sitesindeki verileri kazır ve bir sözlüğe kaydeder.

        # Her site için kazıma işlevlerini çağırın
        scrape_cbr_anime()
        scrape_hashnode_data_science()
        scrape_interesting_engineering()
        scrape_wired_science()
        scrape_techcrunch_startups()
        # Toplanan verilerden bir DataFrame oluşturun

        '''Bu işlevler CBR Anime, Hashnode Data Science, Interesting Engineering, Wired Science ve TechCrunch Startups gibi web sitelerinden veri kazıyor.'''
        df = pd.DataFrame(data)
        # DataFrame'i bir Excel dosyasına kaydedin.
        df.to_excel('web_scraping_results.xlsx', index=False)
        '''Verileri kazıdıktan sonra, toplanan verilerden bir DataFrame oluşturur ve bunu "web_scraping_results.xlsx" adlı bir Excel dosyasına kaydeder. '''
        # E-Posta Yapılandırılması
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'ortakallan@gmail.com'  # Gmail e-posta adresinizle değiştirin
        smtp_password = 'iubq cogz nxyi nnqs'  # Oluşturulan uygulama parolanızla değiştirin
        '''Ayrıca, e-posta göndermek için SMTP sunucusu, bağlantı noktası, kullanıcı adı ve parola ile e-posta yapılandırmasını ayarlar.'''

        # Alıcı e-posta adresleri
        recipient_emails = ['fatih.821@outlook.com', 'yusuf.cinarci@gmail.com']  # Replace with your recipient email addresses

        '''Bu e-posta adreslerinin bir e-postanın alıcıları olması amaçlanmıştır. Açıklama # Alıcı e-posta adresleri sadece kodun amacını belirtmek için açıklayıcı bir yorumdur. 
        Çoklu e-posta adresleri ekleyerek birden fazla mail adresine gönderim yapılmaktadır.'''

        # Email içeriği
        body = 'Please find the attached web scraping results.'
        '''e-posta gövdesinin içeriğini saklamak için kullanılan body değişkenine atar.'''

        # Excel dosyasını ekleyin.
        with open('web_scraping_results.xlsx', 'rb') as file:
            attachment = MIMEApplication(file.read(), _subtype="xlsx")
            attachment.add_header('Content-Disposition', 'attachment', filename='web_scraping_results.xlsx')
        
        '''Kod parçacığı open() fonksiyonunu kullanarak ikili modda 'web_scraping_results.xlsx' adlı bir dosya açmaktadır. 
            Daha sonra read() yöntemini kullanarak dosyanın içeriğini okur ve attachment değişkenine atar. Burada attachment = ek dosyası olarak atanan scraping işlemlerinin kaydedildiği excel dosyasıdır.'''

        # E-postayı her alıcıya ayrı ayrı gönderin
        for recipient_email in recipient_emails:
            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['To'] = recipient_email
            msg['Subject'] = 'Web Scraping Results'

            msg.attach(MIMEText(body, 'plain'))
            msg.attach(attachment)

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, recipient_email, msg.as_string())
            server.quit()

        print('Email sent successfully to the recipients:', ', '.join(recipient_emails))
        '''"Kod, SMTP protokolünü kullanarak birden fazla alıcıya e-posta gönderiyor. Dosya gönderildikten sonra Email başarı ile gönderildi mesajı gelir ve mail'in gönderildiği adresler ekrana 
        çıktı olarak yazılır.'''

    scrape_and_save_data() # işlevi web kazıma işlemi gerçekleştiriyor ve ardından bu verileri bir dosyaya veya veritabanına kaydediyor.
    await ctx.send('Web scraping completed!')
''' Tipik olarak Discord bot bağlamında kullanılan ctx nesnesine bir mesaj göndermektedir. Bu kod satırı bir Discord kanalına veya kullanıcısına web kazıma işleminin tamamlandığını belirten bir mesaj göndermek için kullanılır.'''

@bot.command(name='shutdown')
async def shutdown(ctx):
    await ctx.send('Shutting down...')
    await bot.close()
'''Shutdown fonksiyonu, botun kapatıldığını belirten bir mesaj gönderen ve ardından botu kapatan bir komuttur.
ctx: ctx parametresi "bağlam" anlamına gelir ve komutun çağrıldığı bağlamı temsil eder. Mesaj, mesajı gönderen kullanıcı, mesajın gönderildiği kanal vb. hakkında bilgi içerir.'''


bot.run('MTE1NTA5OTQ1OTA1OTk5MDYzOA.GJzIOW.3J7agezBEXXFPoQjoxSl2qE2FqMZrriicLhGH8') # Discord botunun çalışması için run fonksiyonu kullanılır. Burada tırnak içerisine kendi bot token kodunuzu yapıştırmanız gerekir.